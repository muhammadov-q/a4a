"""Questions in plain words for the verified documentation examples: exercises a model can be scored on.

    uv run a4a corpus-tasks --base-url http://127.0.0.1:18003/v1 --model qwen3-32b \\
        --solver-base-url http://127.0.0.1:18000/v1 --solver-model qwen3-coder [--per-repo 40] [--only package ...]

`a4a corpus-exercises` leaves, per repository, examples whose answer is known: some code and the
value of its last expression. A model cannot be asked "what does this code give" if the question is whether
it knows or can use the library, so an LLM writes, for each example, the request of a person who needs that
value and does not see the code. The request must

  - contain every input value of the code, character for character (checked),
  - not contain the answer (checked where the answer is a text),
  - not show code or call syntax (checked),
  - say enough to be solved (checked with `--solver-model`: a second model gets only the request and the
    reference of the API elements the example uses, writes code, and that code must give the verified answer
    when it runs in the library's sandbox).

A request that fails one of the first three checks goes back to the LLM with the reason, a few times; then the
example is dropped. One that cannot be solved from its wording is dropped. The answer itself is never the
LLM's: it stays the verified value.

Only examples that use the public API at least once and define no class or function of their own are taken,
and per repository at most `--per-repo`,
spread over the number of API elements an example uses (1, 2, 3, ...), because that number is how many tools
a solution needs.

Writes out/corpus/tasks/<repository>.jsonl in the exercise format of `a4a run-model`, and
out/corpus/tasks.md.

The examples do not have to come from documentation. `--examples out/corpus/targets --name tasks-aimed`
reads the examples a model wrote for one API element each (`a4a corpus-targets`) and writes
out/corpus/tasks-aimed/ and tasks-aimed.md. Of those, an example is taken only if it uses the element it was
written for, and one per element.
"""

import argparse
import ast
import asyncio
import json
import random
import re
from collections import Counter, defaultdict
from pathlib import Path

from a4a.corpus.exercises import run_drafts
from a4a.corpus.scan import OUT, folder_name
from a4a.evaluation.exercise_check import check
from a4a.repo2tools.pipeline import LLM, extract_json
from a4a.sources.python_repository import box_for, drop_box

MAX_LITERALS, MAX_LITERAL, ROUNDS = 8, 120, 3
FORMS = {"datetime": "a date and time as ISO 8601 text, like 2003-09-25T10:36:00", "date": "a date as ISO 8601 text, like 2003-09-25",
         "time": "a time as ISO 8601 text, like 10:36:00", "timedelta": "a time span as a number of seconds", "Decimal": "a decimal number as text",
         "Fraction": "a fraction as text, like 3/4", "path": "a path as text", "set": "a list, in sorted order"}


def literals_of(code: str) -> list[str]:
    """The input values written in the code: texts and numbers, as a request must repeat them. Docstrings and names are not inputs."""
    found: list[str] = []
    for node in ast.walk(ast.parse(code)):
        if isinstance(node, ast.Constant) and not isinstance(node.value, bool) and node.value is not None:
            if isinstance(node.value, str) and node.value.strip():
                found.append(node.value)
            elif isinstance(node.value, (int, float)):
                found.append(json.dumps(node.value))
    return list(dict.fromkeys(found))


def choose(examples: list[dict], per_repo: int, seed: int = 0) -> list[dict]:
    """At most `per_repo` examples that use the API and can be asked in words, taken in turn from each number of uses."""
    by_uses: dict[int, list[dict]] = defaultdict(list)
    for example in on_target(examples):
        try:
            code = "\n".join([*example["steps"], example["expression"]])
            values = literals_of(code)
            defines = any(isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef, ast.ClassDef, ast.Lambda)) for node in ast.walk(ast.parse(code)))
        except (SyntaxError, ValueError):
            continue
        if defines:
            continue  # a class or function written for the example cannot be given in plain words
        if example["uses"] and len(values) <= MAX_LITERALS and all(len(v) <= MAX_LITERAL for v in values) and example["answer"] is not None:
            by_uses[len(example["uses"])].append(example)
    rng = random.Random(seed)
    for group in by_uses.values():
        rng.shuffle(group)
    chosen: list[dict] = []
    while len(chosen) < per_repo and any(by_uses.values()):
        for k in sorted(by_uses):
            if by_uses[k] and len(chosen) < per_repo:
                chosen.append(by_uses[k].pop())
    return sorted(chosen, key=lambda e: e["id"])


def on_target(examples: list[dict]) -> list[dict]:
    """Examples from documentation as they are. Of examples written for an API element: those that use it, one per element, with its reference first."""
    if not any(e.get("target") for e in examples):
        return examples
    kept: dict[str, dict] = {}
    for example in sorted(examples, key=lambda e: (e.get("way") != "target", e["id"])):
        if example.get("target") and example["target"] in example["uses"]:
            kept.setdefault(example["target"], example)
    return sorted(kept.values(), key=lambda e: e["id"])


def answer_form(example: dict) -> str:
    """How the answer is to be given, in words for the request."""
    answer, kinds = example["answer"], example.get("answer_kinds") or []
    special = [FORMS[k] for k in kinds if k in FORMS]
    if isinstance(answer, bool):
        return "true or false"
    if isinstance(answer, list):
        return "a JSON list" + (f" (each {special[0]})" if special and "set" not in kinds else " in sorted order" if "set" in kinds else "")
    if isinstance(answer, dict):
        return "a JSON object"
    if special:
        return special[0]
    return "a number" if isinstance(answer, (int, float)) else "a text"


def task_messages(example: dict) -> list[dict]:
    code = "\n".join([*example["steps"], example["expression"]])
    return [
        {"role": "system", "content": "You write short requests that test whether an AI model knows or can use a software library. Reply with JSON only."},
        {"role": "user", "content": f"""This Python code uses the library `{example['package']}`. The value of its last line is the answer.

```python
{code}
```
Answer: {json.dumps(example['answer'])[:600]}

Write the request of a person who needs exactly this answer and does not see the code. Rules:
- One to three sentences in plain words. Name the library, and say precisely what is to be found, so that a person
  who knows the library could do it without guessing. The library's own terms are fine ("version specifier",
  "time zone"); code is not: no call syntax, no parentheses of a call.
- Ask only for the value of the last line. Lines before it are setup: describe what they set up, not their results.
- Give every input value exactly as written in the code, character for character: {json.dumps(literals_of(code))}
- Say what the answer must look like: {answer_form(example)}.
- Do not give away the answer.

Reply with one JSON object: {{"task": "..."}}"""},
    ]


def task_problem(text, example: dict) -> str | None:
    """Why a request is not acceptable, or None."""
    if not isinstance(text, str) or len(text.strip()) < 15:
        return 'reply with {"task": "..."}'
    code = "\n".join([*example["steps"], example["expression"]])
    values = literals_of(code)
    missing = [v for v in values if v not in text]
    if missing:
        return f"these input values must appear exactly: {json.dumps(missing)}"
    if re.search(r"[A-Za-z_][A-Za-z0-9_.]*\(", text) or "```" in text or ">>>" in text:
        return "no code: write the request in plain words, without the parentheses of a call"
    answer = example["answer"]
    if isinstance(answer, str) and len(answer) >= 4 and answer not in values and answer in text:
        return "the request gives away the answer"
    return None


def as_exercise(example: dict, task: str) -> dict:
    """The exercise in the format of `a4a run-model`."""
    answer, kinds = example["answer"], example.get("answer_kinds") or []
    number = isinstance(answer, (int, float)) and not isinstance(answer, bool)
    check = "number" if number else "set_equal" if "set" in kinds and isinstance(answer, list) else "exact"
    owner_repo = "/".join(example["repo"].rstrip("/").removesuffix(".git").split("/")[-2:])
    return {"id": example["id"], "kind": example["package"], "horizon": "short", "task": task.strip(), "answer": answer, "check": {"kind": check},
            "reference_calls": [], "reference_call_count": len(example["uses"]), "library_functions": example["uses"],
            "source_repo": f"{owner_repo}@{(example.get('commit') or '')[:7]}", "reference_code": [*example["steps"], example["expression"]],
            "provenance": {"file": example["file"], "documented": example["documented"],
                           "answer_from": (f"an example a model wrote for `{example['target']}`, run twice at this commit with the same result" if example.get("target")
                                           else "the documentation's example, confirmed by running it twice at this commit")}}


async def write_tasks(examples: list[dict], llm) -> tuple[list[dict], Counter]:
    """An exercise per example the LLM could phrase, and why the others were dropped."""

    async def one(example: dict) -> tuple[dict | None, str]:
        chat = task_messages(example)
        problem = "no reply"
        for _ in range(ROUNDS):
            reply = await llm.chat("task", example["id"], chat, max_tokens=400)
            try:
                text = extract_json(reply).get("task")
            except (ValueError, AttributeError):
                text = None
            problem = task_problem(text, example)
            if problem is None:
                return as_exercise(example, text), "written"
            chat = [*chat, {"role": "assistant", "content": reply}, {"role": "user", "content": f"Not usable: {problem}. Write it again."}]
        return None, problem.split(":")[0]

    results = await asyncio.gather(*(one(e) for e in examples))
    return [exercise for exercise, _ in results if exercise], Counter(outcome for _, outcome in results)


def reference_of(uses: list[str], api: dict) -> str:
    """What a solver may look up: the signature and first lines of the documentation of each API element an example uses."""
    by_path = {f"{c['module']}.{c['qualname']}": c for c in api["callables"]}
    lines = []
    for use in uses:
        if use in by_path:
            c = by_path[use]
            lines.append(f"- {use}{'' if c['kind'] == 'property' else '(' + ', '.join(p['name'] for p in c['params']) + ')'}"
                         f" [{c['kind']}]: {(c.get('docstring') or c.get('summary') or '').strip()[:400]}")
        elif use.endswith("()") and use[:-2] in api.get("classes", {}):
            info = api["classes"][use[:-2]]
            lines.append(f"- {info['module']}.{use[:-2]}({', '.join(p['name'] for p in info.get('params') or [])}) [class]: {(info.get('summary') or '').strip()[:300]}")
        elif " " in use and use.split(" ", 1)[0] in api.get("classes", {}):
            name, operator = use.split(" ", 1)
            lines.append(f"- objects of {api['classes'][name]['module']}.{name} can be used with the operator `{operator}`")
    return "\n".join(lines)


def solver_messages(exercise: dict, reference: str) -> list[dict]:
    return [
        {"role": "system", "content": "You write short Python code that answers a request with a given library. Reply with JSON only."},
        {"role": "user", "content": f"""Request: {exercise['task']}

Library: `{exercise['kind']}`. The parts of it you need:
{reference}

Write Python code whose last line is an expression with the answer. Import what you use. No printing, no files, no network.

Reply with one JSON object: {{"code": "..."}}"""},
    ]


def as_item(code) -> dict | None:
    """Code from the solver as an item for the sandboxed worker: the statements, and the last line as the expression."""
    if not isinstance(code, str):
        return None
    try:
        body = ast.parse(code.strip()).body
    except (SyntaxError, ValueError):
        return None
    if not body or not isinstance(body[-1], ast.Expr):
        return None
    return {"module": None, "steps": [ast.unparse(node) for node in body[:-1]], "expression": ast.unparse(body[-1].value), "printed": False}


async def solvable(exercises: list[dict], api: dict, llm, run_items) -> tuple[list[dict], int]:
    """The exercises whose request is enough: code written from the request and the API reference gives the verified answer. Also how many were dropped."""
    replies = await asyncio.gather(*(llm.chat("solve", e["id"], solver_messages(e, reference_of(e["library_functions"], api)), max_tokens=600) for e in exercises))
    items = []
    for reply in replies:
        try:
            items.append(as_item(extract_json(reply).get("code")))
        except (ValueError, AttributeError):
            items.append(None)
    with_code = [(e, item) for e, item in zip(exercises, items) if item]
    results = run_items([item for _, item in with_code]) if with_code else []
    kept = [e for (e, _), result in zip(with_code, results or []) if result["status"] == "ok" and check(e, result["value"])]
    return kept, len(exercises) - len(kept)


def report(rows: list[dict], aimed: bool = False) -> str:
    kind = "an example that a model wrote for one API element" if aimed else "a documentation example"
    total = sum(r["written"] for r in rows)
    by_tools = Counter()
    for r in rows:
        by_tools.update({int(k): v for k, v in r["by_tools"].items()})
    lines = ["# Exercises in plain words, from " + ("examples a model wrote for one API element each" if aimed else "documentation examples"), "",
             f"{total:,} exercises from {sum(1 for r in rows if r['written'])} repositories. The answer of each is the verified value of {kind}; "
             "an LLM wrote only the request. Kept only if a second model, given the request and the reference of the API elements used, wrote code "
             "that gives that answer in the sandbox.", "",
             "By the number of API elements the example uses (the tools a solution needs): " + ", ".join(f"{k}: {v}" for k, v in sorted(by_tools.items())) + ".", "",
             f"| Package | {'Elements with a verified example' if aimed else 'Verified examples that use the API'} | Chosen | Request written | Solvable from the request (kept) |",
             "| --- | --- | --- | --- | --- |"]
    lines += [f"| `{r['package']}` | {r['usable']} | {r['chosen']} | {r.get('phrased', r['written'])} | {r['written']} |" for r in sorted(rows, key=lambda r: -r["written"])]
    return "\n".join(lines) + "\n"


async def run(args) -> None:
    folder = OUT / args.name
    folder.mkdir(parents=True, exist_ok=True)
    llm = LLM(args.base_url, args.model, False, args.concurrency, OUT / f"{args.name}_llm_log.jsonl")
    solver = LLM(args.solver_base_url or args.base_url, args.solver_model, False, args.concurrency, OUT / f"{args.name}_solver_log.jsonl") if args.solver_model else None
    scanned = {folder_name(r["repo"]): r for r in json.loads((OUT / "static.json").read_text())["repositories"] if not r["error"]}
    rows, aimed = [], False
    for path in sorted(args.examples.glob("*.jsonl")):
        examples = [json.loads(line) for line in path.read_text().splitlines()]
        if not examples or (args.only and examples[0]["package"] not in args.only):
            continue
        aimed = aimed or any(e.get("target") for e in examples)
        chosen = choose(examples, args.per_repo)
        written, outcomes = await write_tasks(chosen, llm) if chosen else ([], Counter())
        phrased = len(written)
        if solver and written:
            set_name = f"solve-{path.stem}"
            try:
                box = box_for(scanned[path.stem], set_name)
                written, unsolved = await solvable(written, json.loads((OUT / "scans" / path.stem / "api.json").read_text()), solver, lambda items, box=box: run_drafts(box, items))
                outcomes["not solvable from the request"] = unsolved
            finally:
                drop_box(set_name)
        target = folder / path.name
        if written:
            target.write_text("".join(json.dumps(e) + "\n" for e in written), encoding="utf-8")
        else:
            target.unlink(missing_ok=True)
        rows.append({"package": examples[0]["package"], "usable": sum(1 for e in on_target(examples) if e["uses"]), "chosen": len(chosen), "phrased": phrased, "written": len(written),
                     "by_tools": dict(Counter(e["reference_call_count"] for e in written)), "dropped": {k: v for k, v in outcomes.items() if k != "written"}})
        print(f"{examples[0]['package']}: {len(written)} written of {len(chosen)} chosen {rows[-1]['dropped'] or ''}", flush=True)
    if not args.only:
        (OUT / f"{args.name}.json").write_text(json.dumps({"model": args.model, "solver": args.solver_model, "per_repo": args.per_repo, "repositories": rows}, indent=1) + "\n", encoding="utf-8")
        (OUT / f"{args.name}.md").write_text(report(rows, aimed), encoding="utf-8")
    print(f"{sum(r['written'] for r in rows):,} exercises -> out/corpus/{args.name}/")


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("--base-url", required=True)
    parser.add_argument("--model", required=True)
    parser.add_argument("--solver-model", help="a second model that must be able to solve each request with code; requests it cannot solve are dropped")
    parser.add_argument("--solver-base-url", help="its endpoint, if it is not the same")
    parser.add_argument("--per-repo", type=int, default=40)
    parser.add_argument("--examples", type=Path, default=OUT / "exercises", help="the folder with verified examples, one file per repository")
    parser.add_argument("--name", default="tasks", help="the name of the folder and report this run writes under out/corpus/")
    parser.add_argument("--only", nargs="+", help="only these packages")
    parser.add_argument("--concurrency", type=int, default=8)
    asyncio.run(run(parser.parse_args()))


if __name__ == "__main__":
    main()
