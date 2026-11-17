"""Exercises with known answers, made from a repository's own documentation examples.

    uv run repo2tools corpus-exercises [--limit N] [--only name ...] [--jobs 3]

A doctest example is a small exercise that the library's authors wrote and checked: some code, and what its
last expression gives. For every scanned repository this command

  1. reads the doctest examples in its documentation files and in the docstrings of its package,
  2. turns each example that shows a value into a draft: the expression, the documented output, and the
     earlier lines of the same text that the expression needs (found by following the names it reads),
  3. runs every draft in the library's own environment and sandbox, twice,
  4. keeps a draft as **verified** only if both runs give the same plain JSON value and that value is what
     the documentation shows.

So a verified answer has two independent sources: the documentation, and the library as it is at the scanned
commit. Each exercise also lists what it uses of the API (from the usage scan), which is the number of tools
a task built on it would need.

This runs code of the repository, so it runs only in the environment and sandbox of `repo2tools generate`
(no network, the home folder unreadable, one scratch folder writable), and only for repositories on the
approved list. The environment is deleted afterwards.

Writes out/corpus/exercises/<repository>.jsonl (the verified ones), out/corpus/exercises.json (one record
per repository, with what happened to every draft) and out/corpus/exercises.md.
"""

import argparse
import doctest
import json
import subprocess
import time
from collections import Counter
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path

from repo2tools.corpus.scan import CLONES, OUT, folder_name
from repo2tools.paths import REPO_ROOT
from repo2tools.sources.python_repository import EXAMPLE_WORKER, PythonRepository, drop_box

BATCH_SECONDS = 600
CHECKER = doctest.OutputChecker()


def run_drafts(box, drafts: list[dict]) -> list[dict] | None:
    """What every draft gives, from one run of the sandboxed worker. None if the worker itself failed."""
    request = {"items": [{"module": d["module"], "steps": d["steps"], "expression": d["expression"], "printed": d.get("printed", False)} for d in drafts]}
    try:
        process = subprocess.run(box.command(str(EXAMPLE_WORKER)), input=json.dumps(request), text=True, capture_output=True,
                                 timeout=BATCH_SECONDS, env=box.clean_env, cwd=box.scratch)
        return json.loads(process.stdout)["results"]
    except (subprocess.TimeoutExpired, json.JSONDecodeError, KeyError):
        return None


def judge(draft: dict, first: dict, second: dict) -> str:
    """verified, or why not: error, timeout, not_json, not_repeatable, differs_from_docs."""
    if first["status"] != "ok":
        return first["status"]
    if second["status"] != "ok" or first["value"] != second["value"] or first["text"] != second["text"]:
        return "not_repeatable"
    if not CHECKER.check_output(draft["documented"] + "\n", first["text"] + "\n", doctest.NORMALIZE_WHITESPACE):
        return "differs_from_docs"
    return "verified"


def exercises_for(candidate: dict, clones: Path = CLONES, scans: Path | None = None, keep_environment: bool = False) -> tuple[dict, list[dict]]:
    """(record of what happened, verified exercises) for one scanned repository. Never raises."""
    source = PythonRepository(candidate, clones, scans)
    record = {"package": candidate["package"], "repo": candidate["repo"], "commit": candidate.get("commit"), "error": None, "drafts": 0, "outcomes": {}}
    started = time.monotonic()
    set_name = f"examples-{source.name}"
    try:
        drafts = source.drafts()
        record["drafts"] = len(drafts)
        if not drafts:
            return record | {"seconds": round(time.monotonic() - started, 1)}, []
        box = source.box(set_name)
        first, second = run_drafts(box, drafts), run_drafts(box, drafts)
        if first is None or second is None:
            raise RuntimeError("the sandboxed run did not finish")
        verified = []
        outcomes, errors = Counter(), Counter()
        for draft, a, b in zip(drafts, first, second):
            outcome = judge(draft, a, b)
            outcomes[outcome] += 1
            if outcome == "error":
                errors[a["error"].split(":")[0]] += 1
            if outcome != "verified":
                continue
            verified.append({"id": f"{source.name}-{len(verified) + 1:03d}", "repo": candidate["repo"], "commit": candidate.get("commit"), "package": source.package,
                             "file": draft["file"], "module": draft["module"], "steps": draft["steps"], "expression": draft["expression"],
                             "answer": a["value"], "answer_kinds": a.get("kinds", []), "documented": draft["documented"], "uses": source.uses(draft)})
        record["outcomes"] = dict(outcomes)
        record["errors"] = dict(errors.most_common(5))
    except (Exception, SystemExit) as error:  # noqa: BLE001 (one repository must not stop the pass)
        text = str(error).strip().splitlines()[0][:200] if str(error).strip() else ""
        record["error"] = f"{type(error).__name__}: {text}".replace(str(clones) + "/", "")
        verified = []
    finally:
        if not keep_environment:
            drop_box(set_name)
    return record | {"seconds": round(time.monotonic() - started, 1)}, verified


def report(records: list[dict]) -> str:
    outcomes = Counter()
    for r in records:
        outcomes.update(r["outcomes"])
    drafts, verified = sum(r["drafts"] for r in records), outcomes["verified"]
    with_some = [r for r in records if r["outcomes"].get("verified")]
    lines = ["# Exercises from documentation examples", "",
             f"{len(records)} repositories. {drafts:,} examples in their documentation show a value; {verified:,} of them are verified: run twice in the "
             f"library's own environment and sandbox, a plain JSON value both times, and the value the documentation shows. "
             f"{len(with_some)} repositories have at least one.", "",
             "| What happened to an example | Number |", "| --- | --- |"]
    names = {"verified": "verified", "error": "the code raised an error (also: needs earlier context, the network or a file)", "not_json": "the result is an object, not a plain value",
             "differs_from_docs": "the result is not what the documentation shows", "not_repeatable": "two runs gave different results", "timeout": "took longer than 5 s"}
    lines += [f"| {names.get(outcome, outcome)} | {n:,} |" for outcome, n in outcomes.most_common()]
    lines += ["", "| Package | Examples that show a value | Verified | Error | Object | Differs | Not scanned or run because |", "| --- | --- | --- | --- | --- | --- | --- |"]
    for r in sorted(records, key=lambda r: -r["outcomes"].get("verified", 0)):
        o = r["outcomes"]
        lines.append(f"| `{r['package']}` | {r['drafts']} | {o.get('verified', 0)} | {o.get('error', 0) + o.get('timeout', 0)} | {o.get('not_json', 0)} | "
                     f"{o.get('differs_from_docs', 0) + o.get('not_repeatable', 0)} | {(r['error'] or '').replace('|', '/')} |")
    return "\n".join(lines) + "\n"


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("--static", type=Path, default=OUT / "static.json", help="the scanned repositories, from `repo2tools corpus-scan`")
    parser.add_argument("--only", nargs="+", help="only these packages")
    parser.add_argument("--limit", type=int, help="only the first N repositories")
    parser.add_argument("--jobs", type=int, default=3)
    args = parser.parse_args()
    scanned = [r for r in json.loads(args.static.read_text())["repositories"] if not r["error"]]
    scanned = [r for r in scanned if not args.only or r["package"] in args.only][:args.limit]
    folder = OUT / "exercises"
    folder.mkdir(parents=True, exist_ok=True)

    def one(candidate: dict) -> dict:
        record, verified = exercises_for(candidate, scans=OUT / "scans")
        target = folder / f"{folder_name(candidate['repo'])}.jsonl"
        if verified:
            target.write_text("".join(json.dumps(e) + "\n" for e in verified), encoding="utf-8")
        else:
            target.unlink(missing_ok=True)
        print(f"{candidate['package']}: {record['outcomes'].get('verified', 0)} verified of {record['drafts']} {record['outcomes']} {record.get('errors', '')}"
              + (f" ({record['error']})" if record["error"] else ""), flush=True)
        return record

    with ThreadPoolExecutor(args.jobs) as pool:
        records = list(pool.map(one, scanned))
    if not args.only and not args.limit:
        (OUT / "exercises.json").write_text(json.dumps({"repositories": records}, indent=1) + "\n", encoding="utf-8")
        (OUT / "exercises.md").write_text(report(records), encoding="utf-8")
    total = sum(r["outcomes"].get("verified", 0) for r in records)
    print(f"{total:,} verified exercises from {sum(1 for r in records if r['outcomes'].get('verified'))} of {len(records)} repositories -> {(OUT / 'exercises.md').relative_to(REPO_ROOT)}")


if __name__ == "__main__":
    main()
