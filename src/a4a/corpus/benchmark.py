"""Do generated tools help a model answer questions about the library they were made from?

    uv run a4a corpus-benchmark --writer-base-url http://127.0.0.1:18000/v1 --writer-model qwen3-coder \\
        --base-url http://127.0.0.1:18001/v1 --model qwen3-8b --tag bench2 --runs 3
    uv run a4a corpus-benchmark --tag bench2 --model qwen3-8b --report-only

For every repository that has at least `--min-tasks` questions in out/corpus/tasks/ (`a4a corpus-tasks`),
the model answers the repository's questions under three conditions, `--runs` times each:

    none    without tools
    tools   with a tool set generated from the repository at the scanned commit (`a4a generate
            --follow-reexports --classes`, one tool per function: the small level). The set is generated once per
            tag; if it is already in toolsets/generated/, only its environment is rebuilt and no writer is needed
    python  with one tool that runs Python where the library is installed (python_tool.py): the baseline that
            generated tools have to beat

All conditions use the same instruction, one reminder if the reply is not a bare value, and the same cap on
tool output. In the two conditions with tools, a tool call that the model wrote as text is run as a call, and the
Python tool's output is shown as text (`run-model --repair-calls`, `--plain-text`). `--strict` leaves both out:
that is how the first runs were made, and they showed that the harness, not the tools, then decides a quarter of
the answers of a small model. Strict runs and reports have their own names.

A run that is already saved in out/runs/ is not repeated, so the command can be stopped and started again, and
`--report-only` builds the report from the saved runs at any time.

Writes out/corpus/benchmark-<tag>-<model>.json and .md (with --strict: ...-strict.json and .md).
"""

import argparse
import json
import math
import os
import re
import subprocess
import sys
import time
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path
from statistics import mean

from a4a.corpus.scan import OUT, folder_name
from a4a.paths import API_KEY_FILE, REPO_ROOT
from a4a.repo2tools.pipeline import repo_name
from a4a.sources.python_repository import box_for, drop_box

CONDITIONS = {"none": "No tools", "tools": "Generated tools", "python": "One Python tool"}
PYTHON_TOOL = Path(__file__).resolve().parent / "python_tool.py"


def repositories(min_tasks: int) -> list[dict]:
    """The repositories with enough questions: {"stem", "path", "package", "url", "tasks"}."""
    found = []
    for path in sorted((OUT / "tasks").glob("*.jsonl")):
        tasks = [json.loads(line) for line in path.read_text().splitlines()]
        if len(tasks) >= min_tasks:
            found.append({"stem": path.stem, "path": path, "package": tasks[0]["kind"], "url": "https://github.com/" + tasks[0]["source_repo"].split("@")[0], "tasks": len(tasks)})
    return found


def run_tag(tag: str, stem: str, condition: str, run: int = 1, strict: bool = False) -> str:
    """Names a run. Without tools there is nothing to repair, so those runs are the same for both harnesses."""
    repair = "" if strict or condition == "none" else "-repair"
    return f"{tag}-{stem}" + ("-python" if condition == "python" else "") + repair + ("" if run == 1 else f"-r{run}")


def run_file(model: str, condition: str, tag: str, stem: str, run: int = 1, strict: bool = False) -> Path:
    """Where `a4a run-model` saves this run. The Python tool is a tool set too, so its mode is `tools`."""
    return REPO_ROOT / "out" / "runs" / f"{model}-{'none' if condition == 'none' else 'tools'}-{run_tag(tag, stem, condition, run, strict)}.jsonl"


def saved_runs(model: str, condition: str, tag: str, stem: str, strict: bool = False) -> list[list[dict]]:
    """The saved runs of one condition, in order: run 1, run 2, ... up to the first that is missing."""
    runs = []
    while (path := run_file(model, condition, tag, stem, len(runs) + 1, strict)).is_file():
        runs.append([json.loads(line) for line in path.read_text().splitlines()])
    return runs


def call_as_text(record: dict) -> bool:
    """Whether a run ended with a tool call that the model wrote as its message (the saved text is cut, so it is not parsed)."""
    raw = (record.get("raw") or "").lstrip()
    return raw.startswith('{"name"') and '"arguments"' in raw


def summarize(repos: list[dict], model: str, tag: str, strict: bool = False) -> list[dict]:
    """One row per repository from the saved runs: questions, tools, and per condition the right answers of each run."""
    rows = []
    for repo in repos:
        row = {"package": repo["package"], "repo": repo["url"], "questions": repo["tasks"], "tools_picked": None, "tools_accepted": None, "right": {}, "use": {}}
        report = REPO_ROOT / "out" / "generated" / f"{repo_name(repo['url'])}-{tag}" / "report.json"
        if report.is_file():
            generated = json.loads(report.read_text())
            row |= {"tools_picked": len(generated["tools"]), "tools_accepted": generated["accepted"]}
        for condition in CONDITIONS:
            runs = saved_runs(model, condition, tag, repo["stem"], strict)
            row["right"][condition] = [sum(r["passed"] for r in run) for run in runs]
            if condition != "none" and runs:
                called = [[r for r in run if r.get("tool_calls")] for run in runs]
                row["use"][condition] = {"called_a_tool": [len(c) for c in called], "right_when_called": [sum(r["passed"] for r in c) for c in called],
                                         "tool_calls": [sum(r.get("tool_calls", 0) for r in run) for run in runs],
                                         "tool_errors": [sum(r.get("tool_errors", 0) for r in run) for run in runs],
                                         "repaired_calls": [sum(r.get("repaired_calls", 0) for r in run) for run in runs],
                                         "ended_with_a_call_as_text": [sum(call_as_text(r) for r in run) for run in runs]}
        rows.append(row)
    return rows


def sign_test(only_a: int, only_b: int) -> float:
    """How likely a split at least this uneven is if both are equally good: the exact two-sided sign test (McNemar's exact test)."""
    n, k = only_a + only_b, min(only_a, only_b)
    return 1.0 if n == 0 else min(1.0, 2 * sum(math.comb(n, i) for i in range(k + 1)) / 2**n)


def breakdown(repos: list[dict], model: str, tag: str, strict: bool = False) -> dict:
    """Question by question, from the first run of the repositories that have every condition.

    by_answer: right answers for questions whose answer is true or false (half of them can be guessed) and for the rest.
    pairs: for two conditions, the questions only one of them got right, and the sign test on that split.
    """
    runs = {repo["stem"]: {c: saved_runs(model, c, tag, repo["stem"], strict) for c in CONDITIONS} for repo in repos}
    shown = [c for c in CONDITIONS if any(by_condition[c] for by_condition in runs.values())]
    passed, kinds = {c: {} for c in shown}, {}
    for repo in repos:
        if shown and all(runs[repo["stem"]][c] for c in shown):
            kinds |= {t["id"]: "true or false" if isinstance(t["answer"], bool) else "another value" for t in map(json.loads, repo["path"].read_text().splitlines())}
            for c in shown:
                passed[c] |= {r["id"]: bool(r["passed"]) for r in runs[repo["stem"]][c][0]}
    by_answer = [{"answer": kind, "questions": sum(k == kind for k in kinds.values()), **{c: sum(passed[c].get(i, False) for i, k in kinds.items() if k == kind) for c in shown}}
                 for kind in ("true or false", "another value")]
    pairs = []
    for a, b in (("none", "tools"), ("none", "python"), ("tools", "python")):
        if a in shown and b in shown:
            only_a, only_b = (sum(passed[x].get(i, False) and not passed[y].get(i, False) for i in kinds) for x, y in ((a, b), (b, a)))
            pairs.append({"a": a, "b": b, "only_a": only_a, "only_b": only_b, "p": float(f"{sign_test(only_a, only_b):.2g}")})
    return {"conditions": shown, "by_answer": by_answer, "pairs": pairs}


def cell(values: list, of: int | None = None) -> str:
    """Right answers over the runs: the number, or the mean with every run in brackets. With `of`, also the share."""
    if not values:
        return "none"
    share = f" ({mean(values) / of:.0%})" if of else ""
    if len(values) == 1:
        return f"{values[0]}{share}"
    return f"{mean(values):.1f}{share} ({', '.join(map(str, values))})"


def report(rows: list[dict], model: str, tag: str, strict: bool = False, details: dict | None = None) -> str:
    shown = [c for c in CONDITIONS if any(r["right"][c] for r in rows)]
    complete = [r for r in rows if shown and all(r["right"][c] for c in shown)]
    runs = min((len(r["right"][c]) for r in complete for c in shown), default=0)
    questions = sum(r["questions"] for r in complete)
    totals = {c: [sum(r["right"][c][k] for r in complete) for k in range(runs)] for c in shown}
    harness = ("Strict harness: a tool call that the model wrote as text was taken as its answer, and the Python tool's output was shown as a JSON string." if strict else
               "A tool call that the model wrote as text is run as a call, and the Python tool's output is shown as text.")
    lines = [f"# Tools against no tools, on each library's own documentation questions ({tag}{', strict harness' if strict else ''})", "", harness, "",
             f"Model `{model}`. {len(complete)} repositories with every condition, {questions} questions, {runs} run{'s' if runs != 1 else ''} each. Right answers: "
             + "; ".join(f"{CONDITIONS[c].lower()} {cell(totals[c], questions)}" for c in shown) + ".", "",
             "A cell is the number of right answers: the mean of the runs, then each run in brackets.", "",
             "| Package | Questions | Tools accepted | " + " | ".join(CONDITIONS[c] for c in shown) + " |", "| --- | --- | --- | " + " | ".join("---" for _ in shown) + " |"]
    for r in rows:
        accepted = "none" if r["tools_picked"] is None else f"{r['tools_accepted']} of {r['tools_picked']}"
        lines.append(f"| `{r['package']}` | {r['questions']} | {accepted} | " + " | ".join(cell(r["right"][c]) for c in shown) + " |")
    lines.append(f"| **{len(complete)} repositories with every condition** | **{questions}** | | " + " | ".join(f"**{cell(totals[c], questions)}**" for c in shown) + " |")
    lines += ["", "## How the tools were used", "", "Means over the runs.", "",
              "| Package | Condition | Questions with a tool call | Right among those | Tool calls | Calls that gave an error | "
              + ("Ended with a call written as text |" if strict else "Calls written as text, and run |"), "| --- | --- | --- | --- | --- | --- | --- |"]
    for r in rows:
        for condition, use in r["use"].items():
            lines.append(f"| `{r['package']}` | {CONDITIONS[condition].lower()} | {mean(use['called_a_tool']):.1f} of {r['questions']} | {mean(use['right_when_called']):.1f} | "
                         f"{mean(use['tool_calls']):.1f} | {mean(use['tool_errors']):.1f} | {mean(use['ended_with_a_call_as_text' if strict else 'repaired_calls']):.1f} |")
    if details and details["conditions"]:
        share = lambda right, of: f"{right} ({right / of:.0%})" if of else "none"  # noqa: E731
        lines += ["", "## By kind of answer", "", "First run. A true-or-false question can be answered right by guessing half of the time.", "",
                  "| The answer is | Questions | " + " | ".join(CONDITIONS[c] for c in details["conditions"]) + " |", "| --- | --- | " + " | ".join("---" for _ in details["conditions"]) + " |"]
        lines += [f"| {row['answer']} | {row['questions']} | " + " | ".join(share(row[c], row["questions"]) for c in details["conditions"]) + " |" for row in details["by_answer"]]
        lines += ["", "## Question by question", "", "First run. p is the exact two-sided sign test on the questions that only one of the two got right.", "",
                  "| A | B | Only A right | Only B right | p |", "| --- | --- | --- | --- | --- |"]
        lines += [f"| {CONDITIONS[pair['a']].lower()} | {CONDITIONS[pair['b']].lower()} | {pair['only_a']} | {pair['only_b']} | {pair['p']:g} |" for pair in details["pairs"]]
    return "\n".join(lines) + "\n"


def tool_set_server(repo: dict, commit: str, args, env: dict) -> list[str] | None:
    """The command that serves the repository's generated tools, or None if no tool passed. Generates the set if there is none yet."""
    set_name = f"{repo_name(repo['url'])}-{args.tag}"
    script = REPO_ROOT / "toolsets" / "generated" / set_name / "run_server.sh"
    generate = [sys.executable, "-m", "a4a.cli", "generate", repo["url"], "--commit", commit, "--tag", args.tag]
    if script.is_file():
        subprocess.run([*generate, "--env-only"], env=env, cwd=REPO_ROOT, capture_output=True)
    elif args.writer_base_url and args.writer_model:
        subprocess.run([*generate, "--base-url", args.writer_base_url, "--model", args.writer_model, "--max-tools", str(args.max_tools), "--follow-reexports", "--classes"],
                       env=env, cwd=REPO_ROOT, capture_output=True)
    has_tools = script.is_file() and any((script.parent / "tools").glob("*.py"))
    return [f"toolsets/generated/{set_name}/run_server.sh"] if has_tools else None


def python_server(candidate: dict, set_name: str) -> list[str]:
    """The command that serves the Python tool inside the repository's own environment and sandbox."""
    box = box_for(candidate, set_name, readable=PYTHON_TOOL)
    return ["env", "-i", *(f"{name}={value}" for name, value in box.clean_env.items()), *box.command(str(PYTHON_TOOL), "--library", candidate["import_name"])]


def run_repository(repo: dict, candidate: dict, args, env: dict) -> None:
    """Every run of this repository that is not saved yet."""
    wanted = [(c, k) for c in args.conditions for k in range(1, args.runs + 1) if not run_file(args.model, c, args.tag, repo["stem"], k, args.strict).is_file()]
    if not wanted:
        return
    started = time.monotonic()
    set_name, python_set = f"{repo_name(repo['url'])}-{args.tag}", f"python-{repo['stem']}"
    servers = {"none": []}
    try:
        if any(c == "tools" for c, _ in wanted):
            servers["tools"] = tool_set_server(repo, candidate["commit"], args, env)
        if any(c == "python" for c, _ in wanted):
            try:
                servers["python"] = python_server(candidate, python_set)
            except (RuntimeError, SystemExit, subprocess.CalledProcessError) as error:
                print(f"{repo['package']}: no environment for the Python tool ({str(error)[:200]})", flush=True)

        def one(condition: str, run: int) -> None:
            command = [sys.executable, "-m", "a4a.cli", "run-model", str(repo["path"]), "--mode", "none" if condition == "none" else "tools",
                       "--base-url", args.base_url, "--model", args.model, "--topic", f"the Python library {repo['package']}", "--remind",
                       "--tag", run_tag(args.tag, repo["stem"], condition, run, args.strict)]
            if not args.strict and condition != "none":
                command += ["--repair-calls"] + (["--plain-text"] if condition == "python" else [])
            done = subprocess.run(command + (["--", *servers[condition]] if servers[condition] else []), env=env, cwd=REPO_ROOT, capture_output=True, text=True)
            if done.returncode != 0:
                print(f"{repo['package']}: {condition} run {run} failed: {done.stderr.strip()[-300:]}", flush=True)

        with ThreadPoolExecutor(max_workers=args.jobs) as pool:
            list(pool.map(lambda pair: one(*pair), [(c, k) for c, k in wanted if servers.get(c) is not None]))
    finally:
        for leftover in (set_name, python_set):
            drop_box(leftover)
    print(f"{repo['package']}: done in {time.monotonic() - started:.0f} s", flush=True)


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("--tag", required=True, help="names this benchmark: tool sets <repository>-<tag>, runs <model>-<mode>-<tag>-<repository>")
    parser.add_argument("--model", default="qwen3-8b", help="the model that answers")
    parser.add_argument("--base-url")
    parser.add_argument("--writer-model", help="the model that writes the tools; only needed for a repository that has no tool set with this tag yet")
    parser.add_argument("--writer-base-url")
    parser.add_argument("--conditions", nargs="+", choices=tuple(CONDITIONS), default=list(CONDITIONS))
    parser.add_argument("--runs", type=int, default=1, help="how often the model answers under each condition")
    parser.add_argument("--jobs", type=int, default=3, help="runs of one repository at the same time")
    parser.add_argument("--only", nargs="+", metavar="PACKAGE", help="run only these packages; the report still covers all")
    parser.add_argument("--min-tasks", type=int, default=8)
    parser.add_argument("--max-tools", type=int, default=60)
    parser.add_argument("--strict", action="store_true", help="without --repair-calls and --plain-text, as in the first runs")
    parser.add_argument("--report-only", action="store_true", help="only build the report from the saved runs")
    args = parser.parse_args()
    repos = repositories(args.min_tasks)
    if not args.report_only:
        if not args.base_url:
            parser.error("give --base-url, or --report-only")
        scanned = {folder_name(r["repo"]): r for r in json.loads((OUT / "static.json").read_text())["repositories"] if not r["error"]}
        env = {**os.environ, "OPENAI_API_KEY": os.environ.get("OPENAI_API_KEY") or API_KEY_FILE.read_text().strip()}
        for repo in repos:
            if not args.only or repo["package"] in args.only:
                run_repository(repo, scanned[repo["stem"]], args, env)
    rows, details = summarize(repos, args.model, args.tag, args.strict), breakdown(repos, args.model, args.tag, args.strict)
    name = re.sub(r"[^A-Za-z0-9._-]+", "-", f"benchmark-{args.tag}-{args.model}{'-strict' if args.strict else ''}")
    (OUT / f"{name}.json").write_text(json.dumps({"model": args.model, "tag": args.tag, "strict": args.strict, "min_tasks": args.min_tasks, "repositories": rows, **details}, indent=1) + "\n", encoding="utf-8")
    (OUT / f"{name}.md").write_text(report(rows, args.model, args.tag, args.strict, details), encoding="utf-8")
    print(f"-> out/corpus/{name}.md")


if __name__ == "__main__":
    main()
