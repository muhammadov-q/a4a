"""The public benchmarks side by side: every scored model, and each trained student against its untrained base.

    uv run a4a public-report

Reads the saved results of `a4a spider-benchmark` and `a4a humaneval-benchmark`. A trained student is named
<base>-<recipe>[-f<fold>] (for example qwen3-4b-rec4-f2); it is compared with <base> question by question: the
questions only one of the two gets right, and the exact sign test on that split. Every fold's student is scored
on the whole benchmark, since no fold saw any of it.

Writes out/downstream/report.md and report.json.
"""

import argparse
import json
import re
from statistics import mean

from a4a.corpus.benchmark import sign_test
from a4a.downstream.humaneval import OUT as HUMANEVAL
from a4a.downstream.spider_tasks import OUT as SPIDER
from a4a.paths import REPO_ROOT

OUT = REPO_ROOT / "out" / "downstream"
TRAINED = re.compile(r"^(?P<base>.+?)-(?P<recipe>sft\d+|rec\d+)(?:-(?P<fold>f\d+))?$")


def scores() -> dict[str, dict[str, dict[str, bool]]]:
    """benchmark -> model -> question id -> right."""
    found = {"spider": {}, "humaneval": {}}
    for path in sorted(SPIDER.glob("benchmark-*.json")):
        record = json.loads(path.read_text(encoding="utf-8"))
        found["spider"][record["model"]] = record["passed"]
    for path in sorted(p for p in HUMANEVAL.glob("*.jsonl") if not re.search(r"-first\d+$", p.stem)):  # smoke tests are left out
        found["humaneval"][path.stem] = {r["task_id"]: bool(r["passed"]) for r in map(json.loads, path.read_text(encoding="utf-8").splitlines())}
    return found


def against(base: dict[str, bool], model: dict[str, bool]) -> dict:
    """Questions only the base gets right, only the model gets right, and the sign test; over the questions both answered."""
    shared = base.keys() & model.keys()
    before = sum(base[q] and not model[q] for q in shared)
    after = sum(model[q] and not base[q] for q in shared)
    return {"only_base": before, "only_model": after, "p": sign_test(before, after)}


def rows(found: dict) -> list[dict]:
    models = sorted(set(found["spider"]) | set(found["humaneval"]), key=lambda m: (TRAINED.match(m).group("base") if TRAINED.match(m) else m, m))
    table = []
    for model in models:
        trained = TRAINED.match(model)
        base = trained.group("base") if trained else None
        row = {"model": model, "base": base, "recipe": trained.group("recipe") if trained else None, "fold": (trained.group("fold") or "f1") if trained else None}
        for benchmark, by_model in found.items():
            if model in by_model:
                answers = by_model[model]
                row[benchmark] = {"right": sum(answers.values()), "questions": len(answers)}
                if base in by_model:
                    row[benchmark]["against_base"] = against(by_model[base], answers)
        table.append(row)
    return table


def cell(row: dict, benchmark: str) -> str:
    if benchmark not in row:
        return "not run | "
    score = row[benchmark]
    text = f"{score['right']} of {score['questions']} ({score['right'] / max(score['questions'], 1):.0%}) | "
    if "against_base" in score:
        a = score["against_base"]
        text += f"{a['only_base']} / {a['only_model']}, p = {a['p']:.2g}"
    return text


def share(members: list[dict], benchmark: str) -> str:
    """The mean share of right answers over the folds, with the lowest and the highest."""
    values = [m[benchmark]["right"] / m[benchmark]["questions"] for m in members if benchmark in m]
    return f"{mean(values):.0%} ({min(values):.0%} to {max(values):.0%})" if values else "not run"


def report(table: list[dict]) -> str:
    lines = ["# Public benchmarks: does training on the verified tasks help or hurt elsewhere?", "",
             "Spider dev (questions on SQLite databases, with the SQL tool; `out/downstream/spider/tasks.md`) and HumanEval (plain Python, no tools, pass@1). "
             "One run each, temperature 0, thinking off. A trained student is compared with its untrained base on the same questions: "
             "\"only base / only trained\" counts the questions only one of the two gets right, with the exact sign test.", "",
             "| Model | Spider dev | Only base / only trained | HumanEval | Only base / only trained |", "| --- | --- | --- | --- | --- |",
             *(f"| `{r['model']}` | {cell(r, 'spider')} | {cell(r, 'humaneval')} |" for r in table), ""]
    groups: dict[tuple, list[dict]] = {}
    for r in table:
        if r["recipe"]:
            groups.setdefault((r["base"], r["recipe"]), []).append(r)
    if groups:
        lines += ["Mean over the folds (each fold's student saw different training sources and none of these benchmarks):", "",
                  "| Base | Recipe | Folds | Spider dev | HumanEval |", "| --- | --- | --- | --- | --- |"]
        for (base, recipe), members in groups.items():
            lines.append(f"| `{base}` | {recipe} | {len(members)} | {share(members, 'spider')} | {share(members, 'humaneval')} |")
        lines.append("")
    return "\n".join(lines)


def main() -> None:
    argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter).parse_args()
    table = rows(scores())
    (OUT / "report.json").write_text(json.dumps(table, indent=1) + "\n", encoding="utf-8")
    (OUT / "report.md").write_text(report(table), encoding="utf-8")
    print(f"{len(table)} models -> out/downstream/report.md")


if __name__ == "__main__":
    main()
