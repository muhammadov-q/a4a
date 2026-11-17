"""Does a target help? A model writes examples for a repository's API in four ways, with the same number of requests each.

    uv run a4a corpus-targets --base-url http://127.0.0.1:18000/v1 --model qwen3-coder [--only package ...] [--requests 40]
    uv run a4a corpus-targets ... --tag full --only packaging rsa --all-open     # every open element once
    uv run a4a corpus-targets ... --tag seed2 --seed 1000                        # the same again with other seeds

The exercises from documentation use a small part of a library, because the documentation decides what is
shown (`a4a corpus-density`). Here a model writes the examples, and the question is what decides their
coverage: what the model is told.

    free     only the name of the library
    listed   also the names of its public API (at most LISTED of them)
    named    one API element that no verified documentation exercise uses, by its name; the example must use it
    target   the same element, with its signature and documentation

`named` and `target` are asked for the same elements, so the two can be compared element by element: what
the target does, and what the reference adds.

Every reply becomes a draft (statements, then one expression), is run twice in the library's own
environment and sandbox, and is verified when both runs give the same plain value. Which API elements an
example uses comes from the static usage scan, as for the documentation exercises. An example has no
documented result, so its answer comes from the run alone.

All ways sample with the same temperature and with the request number (plus `--seed`) as seed, so a rerun
asks the same.

Writes out/corpus/targets/<repository>.jsonl (the verified examples), out/corpus/targets.json and
out/corpus/targets.md, and logs every request in out/corpus/targets_llm_log.jsonl. With `--tag name` the
four are called targets-<name>...; a run with `--only` and no tag writes only the examples.
"""

import argparse
import ast
import asyncio
import json
import random
from collections import Counter

from a4a.corpus.benchmark import sign_test
from a4a.corpus.exercises import judge
from a4a.corpus.scan import CLONES, OUT, folder_name
from a4a.corpus.tasks import reference_of
from a4a.repo2tools.pipeline import LLM, extract_json
from a4a.sources.base import run_drafts
from a4a.sources.python_repository import PythonRepository, drop_box

WAYS = {"free": "Only the name of the library", "listed": "Also the names of the public API", "named": "One API element per request, by name",
        "target": "The same element, with its signature and documentation"}
AIMED = ("named", "target")
LISTED = 300
TEMPERATURE = 0.8
REASONS = ("verified", "no_code", "error", "not_repeatable", "not_json", "timeout")
RULES = ("The last line is an expression whose value is a plain value: a number, text, true or false, or a list or dict of those. "
         "Import what you use. No printing, no files, no network, no random values, no current date or time.")


def messages_for(way: str, package: str, names: list[str], target: str | None, reference: str) -> list[dict]:
    told = {"free": "",
            "listed": "Its public API:\n" + "\n".join(names) + "\n\n",
            "named": f"The example must use `{target}`: the value of the last line has to come from it.\n\n",
            "target": f"The example must use `{target}`: the value of the last line has to come from it.\n{reference}\n\n"}[way]
    return [{"role": "system", "content": "You write short Python examples for a library. Reply with JSON only."},
            {"role": "user", "content": f"Library: `{package}`.\n\n{told}Write one short example that uses the library. {RULES}\n\nReply with one JSON object: {{\"code\": \"...\"}}"}]


def draft_of(code) -> dict | None:
    """Code from the model as a draft: the statements, and the last line as the expression. A last line `name = ...` is read as that name."""
    if not isinstance(code, str):
        return None
    try:
        body = ast.parse(code.strip()).body
    except (SyntaxError, ValueError):
        return None
    if body and isinstance(body[-1], ast.Assign) and len(body[-1].targets) == 1 and isinstance(body[-1].targets[0], ast.Name):
        return {"module": None, "steps": [ast.unparse(node) for node in body], "expression": body[-1].targets[0].id}
    if not body or not isinstance(body[-1], ast.Expr):
        return None
    return {"module": None, "steps": [ast.unparse(node) for node in body[:-1]], "expression": ast.unparse(body[-1].value)}


def targets_for(elements: set[str], covered: set[str], count: int | None, seed: int = 0) -> list[str]:
    """API elements that no documentation exercise uses, chosen without looking at them. All of them, in a fixed order, if `count` is None."""
    open_ones = sorted(elements - covered)
    return random.Random(seed).sample(open_ones, len(open_ones) if count is None else min(count, len(open_ones)))


async def examples_for(source: PythonRepository, covered: set[str], llm, requests: int, run=run_drafts, keep_environment: bool = False,
                       seed: int = 0, all_open: bool = False) -> tuple[dict, list[dict]]:
    """(what happened in each way, verified examples) for one scanned repository. With `all_open`, the aimed ways ask for every open element once."""
    api, elements, package = source.api, source.elements(), source.candidate["import_name"]
    names = sorted(elements) if len(elements) <= LISTED else sorted(random.Random(0).sample(sorted(elements), LISTED))
    targets = targets_for(elements, covered, None if all_open else requests)
    asked = [(way, n, targets[n] if way in AIMED else None) for way in WAYS for n in range(len(targets) if way in AIMED else requests)]
    replies = await asyncio.gather(*(llm.chat(way, f"{source.name}-{n}", messages_for(way, package, names, target, reference_of([target], api) if target else ""),
                                              max_tokens=600, temperature=TEMPERATURE, seed=seed + n) for way, n, target in asked))
    drafts = []
    outcomes = {way: Counter() for way in WAYS}
    for (way, n, target), reply in zip(asked, replies):
        try:
            item = draft_of(extract_json(reply).get("code"))
        except (ValueError, AttributeError):
            item = None
        if item:
            drafts.append(item | {"file": f"model:{way}", "documented": None, "way": way, "request": n, "target": target})
        else:
            outcomes[way]["no_code"] += 1
    record = {"package": source.candidate["package"], "repo": source.candidate["repo"], "commit": source.candidate.get("commit"), "error": None, "api": len(elements),
              "covered_by_documentation": len(covered & elements), "open": len(elements - covered),
              "ways": {way: {"requests": sum(1 for a in asked if a[0] == way), "drafts": sum(1 for d in drafts if d["way"] == way)} for way in WAYS}}
    verified = []
    set_name = f"targets-{source.name}"
    try:
        if drafts:
            box = source.box(set_name)
            first, second = run(box, drafts), run(box, drafts)
            if first is None or second is None:
                raise RuntimeError("the sandboxed run did not finish")
            for draft, a, b in zip(drafts, first, second):
                outcome = judge(draft, a, b)
                outcomes[draft["way"]][outcome] += 1
                if outcome == "verified":
                    verified.append({"id": f"{source.name}-{draft['way']}-{draft['request']:03d}", **source.origin(draft), "way": draft["way"], "target": draft["target"],
                                     "steps": draft["steps"], "expression": draft["expression"], "answer": a["value"], "answer_kinds": a.get("kinds", []),
                                     "documented": None, "uses": source.uses(draft)})
    except (Exception, SystemExit) as error:  # noqa: BLE001 (one repository must not stop the run)
        text = str(error).strip().splitlines()[0][:200] if str(error).strip() else ""
        record["error"] = f"{type(error).__name__}: {text}".replace(str(source.clones) + "/", "")
        verified = []
    finally:
        if not keep_environment:
            drop_box(set_name)
    for way in WAYS:
        mine = [e for e in verified if e["way"] == way]
        used = {use for e in mine for use in e["uses"]} & elements
        record["ways"][way] |= {"outcomes": dict(outcomes[way]), "verified": len(mine), "use_the_api": sum(1 for e in mine if elements & set(e["uses"])),
                                "different": len({("\n".join(e["steps"]), e["expression"]) for e in mine}),
                                "elements": len(used), "new_elements": len(used - covered), "used": sorted(used)}
    hit = {way: {e["target"] for e in verified if e["way"] == way and e["target"] in e["uses"]} for way in AIMED}
    for way in AIMED:
        record["ways"][way]["hits"] = len(hit[way])
    record["paired"] = {"both": len(hit["named"] & hit["target"]), "only_with_reference": len(hit["target"] - hit["named"]),
                        "only_by_name": len(hit["named"] - hit["target"]), "neither": len(set(targets) - hit["named"] - hit["target"])}
    record["together"] = {"elements": len(set().union(*(set(record["ways"][w]["used"]) for w in WAYS))),
                          "with_documentation": len(covered & elements | set().union(*(set(record["ways"][w]["used"]) for w in WAYS)))}
    return record, verified


def share(part: int, whole: int) -> str:
    return f"{part / whole:.0%}" if whole else "n/a"


def report(records: list[dict], model: str, requests: int, all_open: bool = False) -> str:
    good = [r for r in records if not r["error"]]
    total = lambda way, key: sum(r["ways"][way].get(key, 0) for r in good)  # noqa: E731
    api, documented = sum(r["api"] for r in good), sum(r["covered_by_documentation"] for r in good)
    lines = ["# Examples written by a model, with and without a target", "",
             f"Model `{model}`, {requests} requests per way and repository" + (", and for the aimed ways one request for every open element" if all_open else "")
             + f", {len(good)} repositories with {api:,} public API elements together. "
             f"The verified documentation exercises of these repositories use {documented:,} of them ({share(documented, api)}).", "",
             "| Way | What the model is told | Requests | Drafts | Verified | Use the API | Different | API elements used | New (not used by documentation exercises) | Per request |",
             "| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |"]
    for way, what in WAYS.items():
        asked = total(way, "requests")
        lines.append(f"| {way} | {what} | {asked} | {total(way, 'drafts')} | {total(way, 'verified')} | {total(way, 'use_the_api')} | {total(way, 'different')} | "
                     f"{total(way, 'elements')} | {total(way, 'new_elements')} | {total(way, 'new_elements') / asked if asked else 0:.2f} |")
    together, with_docs = sum(r["together"]["elements"] for r in good), sum(r["together"]["with_documentation"] for r in good)
    pairs = {key: sum(r["paired"][key] for r in good) for key in ("both", "only_with_reference", "only_by_name", "neither")}
    lines.append("")
    for way in AIMED:
        hits = total(way, "hits")
        lines.append(f"Way `{way}`: {hits} of {total(way, 'requests')} requests give a verified example that uses the element it was asked to use ({share(hits, total(way, 'requests'))}).")
    lines += ["", f"The two aimed ways ask for the same {sum(pairs.values())} elements. Reached both ways: {pairs['both']}. Only with the signature and documentation: {pairs['only_with_reference']}. "
              f"Only by name: {pairs['only_by_name']}. Neither: {pairs['neither']}. Exact two-sided sign test on the elements reached one way only: p = {sign_test(pairs['only_with_reference'], pairs['only_by_name']):.2g}.",
              f"All ways together use {together:,} elements ({share(together, api)}); with the documentation exercises, {with_docs:,} ({share(with_docs, api)}).", "",
              "What happened to the requests (no_code: the reply held no code that ends in a value; error: the code raised; not_repeatable: two runs differ; not_json: the value is an object):", "",
              "| Way | " + " | ".join(REASONS) + " |", "| --- |" + " --- |" * len(REASONS),
              *(f"| {way} | " + " | ".join(str(sum(r["ways"][way]["outcomes"].get(reason, 0) for r in good)) for reason in REASONS) + " |" for way in WAYS), "",
              "\"Per request\" is new elements for one request: what a request buys. \"Different\" counts examples whose code is not the same as another one of the same way.", "",
              "## Per repository", "",
              "| Package | API | Used by documentation exercises | Open | Asked for | free: new | listed: new | named: hits | named: new | target: hits | target: new | Used at the end |",
              "| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |"]
    for r in good:
        w = r["ways"]
        lines.append(f"| `{r['package']}` | {r['api']} | {r['covered_by_documentation']} | {r['open']} | {w['target']['requests']} | {w['free']['new_elements']} | {w['listed']['new_elements']} | "
                     f"{w['named']['hits']} | {w['named']['new_elements']} | {w['target']['hits']} | {w['target']['new_elements']} | "
                     f"{r['together']['with_documentation']} ({share(r['together']['with_documentation'], r['api'])}) |")
    failed = [r for r in records if r["error"]]
    if failed:
        lines += ["", "## Failed", "", "| Package | Reason |", "| --- | --- |"]
        lines += [f"| `{r['package']}` | {r['error'].replace('|', '/')} |" for r in failed]
    return "\n".join(lines) + "\n"


async def run_all(args) -> None:
    name = f"targets-{args.tag}" if args.tag else "targets"
    folder = OUT / name
    folder.mkdir(parents=True, exist_ok=True)
    llm = LLM(args.base_url, args.model, False, args.concurrency, OUT / f"{name}_llm_log.jsonl")
    asked_for = set(args.only or [r["package"] for r in json.loads((OUT / "tasks.json").read_text())["repositories"] if r["written"] >= args.min_tasks])
    scanned = [r for r in json.loads((OUT / "static.json").read_text())["repositories"] if not r["error"] and {r["package"], r["import_name"]} & asked_for]
    records = []
    for static in scanned:
        source = PythonRepository(static, CLONES, OUT / "scans")
        file = OUT / "exercises" / f"{folder_name(static['repo'])}.jsonl"
        covered = {use for line in (file.read_text().splitlines() if file.is_file() else []) for use in json.loads(line)["uses"]}
        record, verified = await examples_for(source, covered, llm, args.requests, seed=args.seed, all_open=args.all_open)
        target = folder / f"{source.name}.jsonl"
        if verified:
            target.write_text("".join(json.dumps(e) + "\n" for e in verified), encoding="utf-8")
        else:
            target.unlink(missing_ok=True)
        records.append(record)
        print(f"{static['package']}: " + ", ".join(f"{way} {record['ways'][way]['verified']} verified, {record['ways'][way].get('new_elements', 0)} new" for way in WAYS)
              + (f" ({record['error']})" if record["error"] else ""), flush=True)
    if args.tag or not args.only:
        (OUT / f"{name}.json").write_text(json.dumps({"model": args.model, "requests": args.requests, "temperature": TEMPERATURE, "seed": args.seed, "all_open": args.all_open,
                                                      "repositories": records}, indent=1) + "\n", encoding="utf-8")
        (OUT / f"{name}.md").write_text(report(records, args.model, args.requests, args.all_open), encoding="utf-8")
    print(f"{sum(Counter({w: r['ways'][w]['verified'] for w in WAYS}).total() for r in records):,} verified examples -> out/corpus/{name}/")


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("--base-url", required=True, help="OpenAI-compatible endpoint of the model that writes the examples")
    parser.add_argument("--model", required=True)
    parser.add_argument("--requests", type=int, default=40, help="requests per way and repository")
    parser.add_argument("--only", nargs="+", help="only these packages")
    parser.add_argument("--all-open", action="store_true", help="the aimed ways ask for every element that no documentation exercise uses, once")
    parser.add_argument("--seed", type=int, default=0, help="added to the request number; another value asks again with other samples")
    parser.add_argument("--tag", help="a name for this run's files, so that it does not replace the main run")
    parser.add_argument("--min-tasks", type=int, default=8, help="without --only: the repositories with at least this many checked questions, as in the benchmark")
    parser.add_argument("--concurrency", type=int, default=8)
    asyncio.run(run_all(parser.parse_args()))


if __name__ == "__main__":
    main()
