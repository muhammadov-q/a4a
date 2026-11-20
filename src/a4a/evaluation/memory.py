"""Memory or skill? A model's answers to the same questions before and after their answers were changed.

    uv run a4a memory-check --area databases --tasks tasks-v1 --original db1 --variant db1v1 --model qwen3-32b --conditions none sql
    uv run a4a memory-check --area corpus --tasks tasks-v1 --original bench2 --variant bench2v1 --model qwen3-8b --conditions none python

`a4a db-variant` keeps the wording of a question and changes the data under it; `a4a corpus-variant`
changes the input values in the wording. Both compute the answer again and keep the old one in
`provenance.original_answer`, with `changed` telling whether they differ. For the questions whose answer
changed, this command reads the first run of each condition on the original questions (tag `--original`) and
on the changed ones (tag `--variant`) and counts, question by question:

    right before   right on the original question
    right after    right on the changed question
    old answer     on the changed question, the model gave the original answer: an answer from memory

If the model knows how to find the answer, "right after" stays near "right before". If it remembers the
source, "right after" drops and "old answer" rises. With a tool, the second should not happen.

Writes out/<area>/memory-<variant>-<model>.json and .md.
"""

import argparse
import json
import re
from pathlib import Path

from a4a.corpus.benchmark import CONDITIONS, run_file, sign_test
from a4a.evaluation.exercise_check import check
from a4a.paths import REPO_ROOT

NAMES = CONDITIONS | {"sql": "One SQL tool"}


def original_question(question: dict) -> dict:
    """The question as it was: its old answer, compared the same way."""
    old = question["provenance"]["original_answer"]
    number = isinstance(old, (int, float)) and not isinstance(old, bool)
    kind = "number" if number else "set_equal" if question["check"]["kind"] == "set_equal" else "exact"
    return {"answer": old, "check": {"kind": kind}}


def first_run(model: str, condition: str, tag: str, stem: str) -> dict[str, dict] | None:
    path = run_file(model, condition, tag, stem)
    return {r["id"]: r for r in map(json.loads, path.read_text(encoding="utf-8").splitlines())} if path.is_file() else None


def compare(questions_by_stem: dict[str, list[dict]], model: str, original: str, variant: str, conditions: list[str]) -> dict:
    """Counts per condition and per source, over the questions that both runs answered."""
    result = {}
    for condition in conditions:
        rows, missing = [], []
        for stem, questions in questions_by_stem.items():
            before, after = first_run(model, condition, original, stem), first_run(model, condition, variant, stem)
            if before is None or after is None:
                missing.append(stem)
                continue
            row = {"source": stem, "changed": 0, "right_before": 0, "right_after": 0, "old_answer": 0, "only_before": 0, "only_after": 0,
                   "same": 0, "same_right_before": 0, "same_right_after": 0}
            for q in questions:
                if q["id"] not in before or q["id"] not in after:
                    continue
                was, now = bool(before[q["id"]]["passed"]), bool(after[q["id"]]["passed"])
                if q["changed"]:
                    row["changed"] += 1
                    row["right_before"] += was
                    row["right_after"] += now
                    row["only_before"] += was and not now
                    row["only_after"] += now and not was
                    answer = after[q["id"]].get("answer")
                    row["old_answer"] += answer is not None and check(original_question(q), answer)
                else:
                    row["same"] += 1
                    row["same_right_before"] += was
                    row["same_right_after"] += now
            rows.append(row)
        total = {key: sum(r[key] for r in rows) for key in ("changed", "right_before", "right_after", "old_answer", "only_before", "only_after", "same", "same_right_before", "same_right_after")}
        total["p"] = float(f"{sign_test(total['only_before'], total['only_after']):.2g}")
        result[condition] = {"rows": rows, "total": total, "missing": missing}
    return result


def share(part: int, whole: int) -> str:
    return f"{part} ({part / whole:.0%})" if whole else "none"


def report(result: dict, model: str, original: str, variant: str, tasks: str) -> str:
    lines = [f"# Memory or skill: `{model}` on {tasks} ({variant}) against the original questions ({original})", "",
             "Only questions whose answer changed. \"Old answer\": on the changed question, the model gave the original answer, so it answered from memory. "
             "p is the exact two-sided sign test on the questions right only before or only after.", "",
             "| Condition | Questions with a changed answer | Right before | Right after | Old answer | Right only before | Right only after | p |",
             "| --- | --- | --- | --- | --- | --- | --- | --- |"]
    for condition, part in result.items():
        t = part["total"]
        lines.append(f"| {NAMES.get(condition, condition)} | {t['changed']} | {share(t['right_before'], t['changed'])} | {share(t['right_after'], t['changed'])} | "
                     f"{share(t['old_answer'], t['changed'])} | {t['only_before']} | {t['only_after']} | {t['p']:g} |")
    lines += ["", "For comparison, the questions whose answer did not change (the same question twice, so any difference is noise):", "",
              "| Condition | Questions | Right before | Right after |", "| --- | --- | --- | --- |"]
    for condition, part in result.items():
        t = part["total"]
        lines.append(f"| {NAMES.get(condition, condition)} | {t['same']} | {share(t['same_right_before'], t['same'])} | {share(t['same_right_after'], t['same'])} |")
    lines += ["", "## Per source", "", "| Source | Condition | Changed | Right before | Right after | Old answer |", "| --- | --- | --- | --- | --- | --- |"]
    for condition, part in result.items():
        lines += [f"| `{r['source']}` | {NAMES.get(condition, condition)} | {r['changed']} | {r['right_before']} | {r['right_after']} | {r['old_answer']} |" for r in part["rows"]]
        if part["missing"]:
            lines.append(f"| {', '.join(f'`{s}`' for s in part['missing'])} | {NAMES.get(condition, condition)} | no runs | | | |")
    return "\n".join(lines) + "\n"


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("--area", choices=("corpus", "databases"), required=True, help="where the questions and reports live: out/corpus or out/databases")
    parser.add_argument("--tasks", required=True, help="the changed questions: a folder under out/<area>/, e.g. tasks-v1")
    parser.add_argument("--original", required=True, help="the tag of the runs on the original questions")
    parser.add_argument("--variant", required=True, help="the tag of the runs on the changed questions")
    parser.add_argument("--model", required=True)
    parser.add_argument("--conditions", nargs="+", default=["none"], choices=tuple(NAMES))
    args = parser.parse_args()
    out = REPO_ROOT / "out" / args.area
    questions = {path.stem: [json.loads(line) for line in path.read_text(encoding="utf-8").splitlines()] for path in sorted((out / args.tasks).glob("*.jsonl"))}
    result = compare(questions, args.model, args.original, args.variant, args.conditions)
    name = re.sub(r"[^A-Za-z0-9._-]+", "-", f"memory-{args.variant}-{args.model}")
    (out / f"{name}.json").write_text(json.dumps({"model": args.model, "tasks": args.tasks, "original": args.original, "variant": args.variant, "conditions": result}, indent=1) + "\n",
                                      encoding="utf-8")
    (out / f"{name}.md").write_text(report(result, args.model, args.original, args.variant, args.tasks), encoding="utf-8")
    print(f"-> {Path('out') / args.area / name}.md")


if __name__ == "__main__":
    main()
