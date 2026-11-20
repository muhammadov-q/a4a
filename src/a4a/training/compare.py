"""Before and after training: the student on the questions of the test sources, which gave no training example.

    uv run a4a train-compare --name sft1 --base qwen3-1.7b --trained qwen3-1.7b-sft1
    uv run a4a train-compare --name sft1 sft1-f2 sft1-f3 --base qwen3-1.7b --trained qwen3-1.7b-sft1 qwen3-1.7b-sft1-f2 qwen3-1.7b-sft1-f3
    uv run a4a train-compare --name rec17 rec17-f2 rec17-f3 --base qwen3-1.7b-sft1 qwen3-1.7b-sft1-f2 qwen3-1.7b-sft1-f3 \
        --trained qwen3-1.7b-rec17 qwen3-1.7b-rec17-f2 qwen3-1.7b-rec17-f3

The runs are made by the usual commands, with the student's model names and the tags of the teachers' runs,
only on the test sources of out/training/<name>/split.json:

    uv run a4a corpus-benchmark --tag bench2 --model <model> --conditions none python --runs 3 --only <packages>
    uv run a4a corpus-benchmark --tag aimed1 --tasks tasks-aimed --model <model> --conditions none python --runs 3 --only <packages>
    uv run a4a db-benchmark --tag db1 --model <model> --runs 3 --only <databases>

The conditions python-ref and python-search of `corpus-benchmark` (the Python tool with an API reference under each
question) get rows of their own when both models have runs of them.

For each question set and condition: the right answers of both models over the runs, and question by question
on the first run, the questions that only one of them got right, with the exact sign test. Then how the student
worked: how often it called the tool, sent the same call three times in a row, wrote a call as text, needed the
reminder, or gave no answer.

With the folds of `a4a train-data --folds`, give every fold's data and its trained model, in the same order: each
test source is scored with the model of its fold, which did not see it, and the table adds up all folds. `--base`
is one model, or one per fold: then two ways of training are compared, fold by fold.

`--no-repeat` compares the runs made with `--no-repeat` (a call the same as an earlier one is not run again).

Writes out/training/<name>/compare-<trained>.json and .md; with folds, in the folder of the first name, with
`-folds` added; with one base model per fold, `-against-<first base>`; with --no-repeat, `-norepeat`.
"""

import argparse
import json
import re
from collections import defaultdict
from statistics import mean

from a4a.corpus.benchmark import cell, saved_runs, sign_test
from a4a.training.data import OUT

TAGS = {("repository", "tasks"): "bench2", ("repository", "tasks-aimed"): "aimed1", ("database", "tasks"): "db1"}
LABELS = {("repository", "tasks"): "Documentation questions", ("repository", "tasks-aimed"): "Aimed questions", ("database", "tasks"): "Database questions"}
CONDITIONS = {"repository": ("none", "python", "python-ref", "python-search"), "database": ("none", "sql")}
NAMES = {"none": "no tool", "python": "Python tool", "python-ref": "Python tool + reference (elements used)", "python-search": "Python tool + reference (search)", "sql": "SQL tool"}


def stuck(record: dict, times: int = 3) -> bool:
    """Whether the model sent the same call `times` times in a row: it repeats itself instead of changing what failed."""
    calls = [(c["tool"], c["arguments"]) for c in record.get("trace", [])]
    return any(len(set(calls[i:i + times])) == 1 for i in range(len(calls) - times + 1))


def habits(runs: list[list[dict]]) -> dict:
    """How a model worked, as shares of all its answers over the runs."""
    records = [r for run in runs for r in run]
    if not records:
        return {}
    share = lambda test: round(sum(map(test, records)) / len(records), 3)  # noqa: E731
    return {"answers": len(records), "called_the_tool": share(lambda r: r.get("tool_calls", 0) > 0), "call_as_text": share(lambda r: r.get("repaired_calls", 0) > 0),
            "reminded": share(lambda r: r.get("reminded", False)), "no_answer": share(lambda r: r.get("finish") != "answered"), "same_call_3_times": share(stuck),
            "tool_calls_per_answer": round(mean(r.get("tool_calls", 0) for r in records), 2)}


def compare(test: dict, base: dict[str, str], trained: dict[str, str], no_repeat: bool = False) -> list[dict]:
    """One row per question set and condition, summed over the test sources that have runs of both models.

    `base` and `trained` give the two models of each test source: with folds, the models of the fold it was tested in."""
    groups = defaultdict(lambda: {"questions": 0, "sources": [], "right": [], "pairs": {"base": set(), "trained": set()}, "runs": {"base": [], "trained": []}})
    for stem, source in sorted(test.items()):
        kind = source["kind"]
        for folder, count in source["questions"].items():
            if (kind, folder) not in TAGS:
                continue
            for condition in CONDITIONS[kind]:
                runs = {side: saved_runs(model, condition, TAGS[(kind, folder)], stem, no_repeat=no_repeat) for side, model in (("base", base[stem]), ("trained", trained[stem]))}
                if not (runs["base"] and runs["trained"]):
                    continue
                group = groups[(LABELS[(kind, folder)], condition)]
                group["questions"] += count
                group["sources"].append(stem)
                group["right"].append({side: [sum(r["passed"] for r in run) for run in runs[side]] for side in runs})
                for side in ("base", "trained"):
                    group["runs"][side] += runs[side]
                first = {side: {r["id"]: bool(r["passed"]) for r in runs[side][0]} for side in runs}
                for side, other in (("base", "trained"), ("trained", "base")):
                    group["pairs"][side] |= {(stem, i) for i, ok in first[side].items() if ok and not first[other].get(i, False)}
    rows = []
    for (label, condition), group in groups.items():
        count = min(len(source[side]) for source in group["right"] for side in source)  # runs that every source has, for both models
        right = {side: [sum(source[side][k] for source in group["right"]) for k in range(count)] for side in ("base", "trained")}
        only_base, only_trained = len(group["pairs"]["base"]), len(group["pairs"]["trained"])
        rows.append({"questions_set": label, "condition": condition, "sources": group["sources"], "questions": group["questions"], "right": right,
                     "only_base": only_base, "only_trained": only_trained, "p": float(f"{sign_test(only_base, only_trained):.2g}"),
                     "habits": {side: habits(group["runs"][side]) for side in ("base", "trained")}})
    return rows


def report(records: dict[str, dict], rows: list[dict], bases: list[str], trained: list[str], no_repeat: bool = False) -> str:
    """`records` are the split.json of each fold, by name, in the order of `bases` and `trained`."""
    base = bases[0] if len(set(bases)) == 1 else "before"
    if len(records) == 1:
        [(name, record)] = records.items()
        about = [f"# Before and after training: `{trained[0]}` against `{base}`", "",
                 f"Training data `{name}`: {record['examples']} examples from the passed runs of {', '.join(record['teachers'])} on {len(record['train'])} sources. "
                 f"The test sources gave no example: {', '.join(sorted(record['test']))}."]
    else:
        title = f"`{base}` and the model trained for each fold" if base != "before" else "two models for each fold"
        about = [f"# Before and after training, over {len(records)} folds: {title}", "",
                 "Every test source is scored with the model of its fold, whose training data did not include it.", "",
                 f"| Fold | Training data | Examples | {'' if base != 'before' else 'Before | '}Trained model | Test sources |",
                 f"| --- | --- | --- | {'' if base != 'before' else '--- | '}--- | --- |",
                 *(f"| {record.get('fold', i + 1)} | `{name}` | {record['examples']} | {'' if base != 'before' else f'`{before}` | '}`{model}` | {', '.join(sorted(record['test']))} |"
                   for i, ((name, record), before, model) in enumerate(zip(records.items(), bases, trained)))]
    after = trained[0] if len(trained) == 1 else "trained"
    lines = [*about, *(["", "Tool runs with `--no-repeat`: a call that is the same as an earlier call of the run is not run again; the model is told so."] if no_repeat else []), "",
             "A cell is the number of right answers: the mean of the runs, then each run in brackets. "
             "*Only* counts the questions that one model got right and the other did not, on the first run; p is the exact sign test on that split.", "",
             f"| Question set | Condition | Questions | {base} | {after} | Only {base} | Only {after} | p |", "| --- | --- | --- | --- | --- | --- | --- | --- |"]
    for row in rows:
        lines.append(f"| {row['questions_set']} | {NAMES[row['condition']]} | {row['questions']} | {cell(row['right'].get('base', []), row['questions'])} | "
                     f"{cell(row['right'].get('trained', []), row['questions'])} | {row['only_base']} | {row['only_trained']} | {row['p']:g} |")
    lines += ["", "## How the student worked", "", "Shares of all answers over the runs.", "",
              "| Question set | Condition | Model | Called the tool | Calls per answer | The same call 3 times in a row | A call written as text | Needed the reminder | No answer |",
              "| --- | --- | --- | --- | --- | --- | --- | --- | --- |"]
    for row in rows:
        for side, model in (("base", base), ("trained", after)):
            h = row["habits"][side]
            if h:
                lines.append(f"| {row['questions_set']} | {NAMES[row['condition']]} | {model} | {h['called_the_tool']:.0%} | {h['tool_calls_per_answer']} | "
                             f"{h['same_call_3_times']:.0%} | {h['call_as_text']:.0%} | {h['reminded']:.0%} | {h['no_answer']:.0%} |")
    return "\n".join(lines) + "\n"


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("--name", nargs="+", required=True, help="the training data: out/training/<name>/; with folds, one per fold")
    parser.add_argument("--base", nargs="+", required=True, help="the student before training, as served; or one model per --name, to compare two ways of training")
    parser.add_argument("--trained", nargs="+", required=True, help="the student after training: the name of its adapter on the server; with folds, one per --name")
    parser.add_argument("--no-repeat", action="store_true", help="compare the tool runs made with --no-repeat")
    args = parser.parse_args()
    if len(args.name) != len(args.trained) or len(args.base) not in (1, len(args.name)):
        parser.error("give one --trained model for each --name, and one --base model or one for each --name")
    bases = args.base * len(args.name) if len(args.base) == 1 else args.base
    records = {name: json.loads((OUT / name / "split.json").read_text(encoding="utf-8")) for name in args.name}
    test, before, models = {}, {}, {}
    for (name, record), base, model in zip(records.items(), bases, args.trained):
        if set(test) & set(record["test"]):
            parser.error(f"{name} tests a source that an earlier --name tests too")
        test |= record["test"]
        before |= dict.fromkeys(record["test"], base)
        models |= dict.fromkeys(record["test"], model)
    rows = compare(test, before, models, args.no_repeat)
    if not rows:
        parser.error("no question set has saved runs of both models on the test sources")
    against = f"-against-{args.base[0]}" if len(args.base) > 1 else ""  # two ways of training: name both, so neither report replaces the other
    stem = re.sub(r"[^A-Za-z0-9._-]+", "-", f"compare-{args.trained[0]}{'-folds' if len(args.name) > 1 else ''}{against}{'-norepeat' if args.no_repeat else ''}")
    folder = OUT / args.name[0]
    (folder / f"{stem}.json").write_text(json.dumps({"name": args.name[0] if len(args.name) == 1 else args.name, "base": args.base[0] if len(args.base) == 1 else before,
                                                     "trained": args.trained[0] if len(args.trained) == 1 else models,
                                                     **({"no_repeat": True} if args.no_repeat else {}), "rows": rows}, indent=1) + "\n", encoding="utf-8")
    (folder / f"{stem}.md").write_text(report(records, rows, bases, args.trained, args.no_repeat), encoding="utf-8")
    print(f"-> out/training/{args.name[0]}/{stem}.md")


if __name__ == "__main__":
    main()
