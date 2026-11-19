"""Library questions with changed input values, so that an answer remembered from the documentation no longer fits.

    uv run a4a corpus-variant [--tasks tasks] [--seed 1] [--only package ...]

A documentation question asks for the value that a documented example shows, and the documentation is
public. A model may remember the value instead of knowing how to get it. For every question in
out/corpus/<tasks>/ this command

  1. changes the input values of its code: in every number, and in every text that contains digits, the
     last digit of the last run of digits goes up by one (a 9 goes down by one). "1.0.2" becomes "1.0.3",
     "2003-09-25" becomes "2003-09-26", 7 becomes 8, 2.5 becomes 2.6. The change is as small as possible, so
     that the question stays as hard as it was. Texts without digits stay as they are.
  2. runs the changed code twice in the library's own environment and sandbox, with the names of its module
     in scope where the example came from a docstring, and keeps it if both runs give the same plain value
     that is not empty (an empty list, text or object makes a poor question).
  3. writes the request again by replacing each old input value with the new one; every input value appears
     in the request character for character (`a4a corpus-tasks` checks that), so no model is needed. A
     request in which a new value cannot be found afterwards is dropped.

A question is "changed" when its new answer differs from the old one. `--seed` only names the variant here:
the change is the same every time.

Writes out/corpus/<tasks>-v<seed>/<repository>.jsonl (same ids, with `provenance.original_answer`) and
out/corpus/<tasks>-v<seed>.json and .md.
"""

import argparse
import ast
import json
import re
from collections import Counter
from pathlib import Path

from a4a.corpus.exercises import judge
from a4a.corpus.scan import OUT, folder_name
from a4a.corpus.tasks import literals_of
from a4a.evaluation.exercise_check import check
from a4a.sources.base import run_drafts
from a4a.sources.python_repository import box_for, drop_box


def bumped(text: str) -> str:
    """The last digit of the text one up (a 9 one down); a text without digits as it is."""
    last = max((m.end() - 1 for m in re.finditer(r"\d", text)), default=None)
    if last is None:
        return text
    digit = int(text[last])
    return text[:last] + str(digit + 1 if digit != 9 else 8) + text[last + 1:]


def changes_of(literals: list[str]) -> dict[str, str]:
    """Old input value -> new one, for the values that contain a digit. Numbers come as JSON text, as `literals_of` gives them."""
    return {old: new for old in literals if (new := bumped(old)) != old}


class Replace(ast.NodeTransformer):
    def __init__(self, changes: dict[str, str]):
        self.changes = changes

    def visit_Constant(self, node: ast.Constant) -> ast.Constant:
        value = node.value
        if isinstance(value, str) and value in self.changes:
            return ast.copy_location(ast.Constant(self.changes[value]), node)
        if isinstance(value, (int, float)) and not isinstance(value, bool) and json.dumps(value) in self.changes:
            return ast.copy_location(ast.Constant(json.loads(self.changes[json.dumps(value)])), node)
        return node


def changed_code(steps: list[str], expression: str, changes: dict[str, str]) -> tuple[list[str], str]:
    """The code with every changed input value replaced."""
    new_steps = [ast.unparse(Replace(changes).visit(ast.parse(step))) for step in steps]
    new_expression = ast.unparse(Replace(changes).visit(ast.parse(expression, mode="eval")).body)
    return new_steps, new_expression


def changed_text(text: str, changes: dict[str, str]) -> str:
    """The request with each old value replaced by its new one, where it does not stand inside a longer word or number."""
    if not changes:
        return text
    pattern = re.compile("(?<![A-Za-z0-9])(" + "|".join(re.escape(old) for old in sorted(changes, key=len, reverse=True)) + ")(?![A-Za-z0-9])")
    return pattern.sub(lambda m: changes[m.group(1)], text)


def examples_by_id(*folders: Path) -> dict[str, dict]:
    """Every verified example, from documentation and from a model, by id: for the module a docstring example needs."""
    found = {}
    for folder in folders:
        for path in sorted(folder.glob("*.jsonl")):
            found |= {e["id"]: e for e in map(json.loads, path.read_text(encoding="utf-8").splitlines())}
    return found


def drafts_for(questions: list[dict], examples: dict[str, dict]) -> tuple[list[tuple[dict, dict, dict]], Counter]:
    """(question, draft of the changed code, changes) for each question whose inputs can be changed, and why the others cannot."""
    found, outcomes = [], Counter()
    for question in questions:
        example = examples.get(question["id"])
        if example is None:
            outcomes["no_example"] += 1
            continue
        changes = changes_of(literals_of("\n".join(question["reference_code"])))
        if not changes:
            outcomes["no_digits"] += 1
            continue
        try:
            steps, expression = changed_code(example["steps"], example["expression"], changes)
        except (SyntaxError, ValueError):
            outcomes["not_parsed"] += 1
            continue
        found.append((question, {"module": example.get("module"), "steps": steps, "expression": expression, "documented": None, "printed": False}, changes))
    return found, outcomes


def variant_of(question: dict, draft: dict, changes: dict[str, str], value) -> dict | None:
    """The changed question, or None if a new input value does not appear in the new request."""
    task = changed_text(question["task"], changes)
    if not all(new in task for new in changes.values()) or task == question["task"]:
        return None
    number = isinstance(value, (int, float)) and not isinstance(value, bool)
    kind = "number" if number else "set_equal" if question["check"]["kind"] == "set_equal" and isinstance(value, list) else "exact"
    new = question | {"task": task, "answer": value, "check": {"kind": kind}, "reference_code": [*draft["steps"], draft["expression"]]}
    new["changed"] = not check(question, value)
    new["provenance"] = question["provenance"] | {"original_answer": question["answer"], "original_task": question["task"], "changed_inputs": changes,
                                                  "answer_from": "the example with changed input values, run twice at this commit with the same result"}
    return new


def report(rows: list[dict], tasks: str, seed: int) -> str:
    total = Counter()
    for r in rows:
        total.update(r["outcomes"])
    lines = [f"# Library questions with changed input values ({tasks}, variant {seed})", "",
             "In every number and every text with digits, the last digit of each run of digits is changed by one; the code runs again twice in the sandbox. "
             "A question whose answer changed can tell memory from skill.", "",
             "| Package | Questions | No digit to change | No answer from the new code (error, two runs differ, or empty) | Wording could not be updated | Answer changed | Answer the same |",
             "| --- | --- | --- | --- | --- | --- | --- |"]
    lines += [f"| `{r['package']}` | {r['questions']} | {r['outcomes'].get('no_digits', 0)} | {r['outcomes'].get('no_answer', 0)} | {r['outcomes'].get('wording', 0)} | "
              f"{r['outcomes'].get('changed', 0)} | {r['outcomes'].get('unchanged', 0)} |" for r in rows]
    lines += ["", f"Together: {sum(r['questions'] for r in rows)} questions, {total['changed']} with a changed answer, {total['unchanged']} with the same answer."]
    return "\n".join(lines) + "\n"


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("--tasks", default="tasks", help="the question set: a folder under out/corpus/")
    parser.add_argument("--seed", type=int, default=1, help="names the variant")
    parser.add_argument("--only", nargs="+", help="only these packages")
    args = parser.parse_args()
    name = f"{args.tasks}-v{args.seed}"
    folder = OUT / name
    folder.mkdir(parents=True, exist_ok=True)
    scanned = {folder_name(r["repo"]): r for r in json.loads((OUT / "static.json").read_text())["repositories"] if not r["error"]}
    examples = examples_by_id(OUT / "exercises", OUT / "targets")
    rows = []
    for path in sorted((OUT / args.tasks).glob("*.jsonl")):
        questions = [json.loads(line) for line in path.read_text(encoding="utf-8").splitlines()]
        if not questions or (args.only and questions[0]["kind"] not in args.only):
            continue
        found, outcomes = drafts_for(questions, examples)
        kept, set_name = [], f"variant-{path.stem}"
        try:
            if found:
                box = box_for(scanned[path.stem], set_name)
                drafts = [draft for _, draft, _ in found]
                first, second = run_drafts(box, drafts), run_drafts(box, drafts)
                if first is None or second is None:
                    raise RuntimeError("the sandboxed run did not finish")
                for (question, draft, changes), a, b in zip(found, first, second):
                    if judge(draft, a, b) != "verified" or a["value"] in (None, [], {}, ""):
                        outcomes["no_answer"] += 1
                        continue
                    new = variant_of(question, draft, changes, a["value"])
                    if new is None:
                        outcomes["wording"] += 1
                        continue
                    outcomes["changed" if new["changed"] else "unchanged"] += 1
                    kept.append(new)
        finally:
            drop_box(set_name)
        (folder / path.name).write_text("".join(json.dumps(q) + "\n" for q in kept), encoding="utf-8")
        rows.append({"package": questions[0]["kind"], "questions": len(questions), "outcomes": dict(outcomes)})
        print(f"{questions[0]['kind']}: {dict(outcomes)}", flush=True)
    if not args.only:
        (OUT / f"{name}.json").write_text(json.dumps({"tasks": args.tasks, "seed": args.seed, "repositories": rows}, indent=1) + "\n", encoding="utf-8")
        (OUT / f"{name}.md").write_text(report(rows, args.tasks, args.seed), encoding="utf-8")
    print(f"-> out/corpus/{name}/")


if __name__ == "__main__":
    main()
