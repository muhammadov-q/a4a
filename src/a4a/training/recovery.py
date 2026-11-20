"""Recovery examples: a teacher goes on from the point where the student's call failed.

    uv run a4a train-recovery --student qwen3-1.7b --teacher qwen3-32b --base-url http://127.0.0.1:18009/v1 --tag rec17
    uv run a4a train-data --name rec17 --sets bench2 aimed1 db1 bench2rec17 aimed1rec17 db1rec17

The teachers' passed runs answer right after a call that worked, so a student trained on them never learns to
answer after a call that failed, and on a library it does not know it calls until the step limit. Here the
student's own saved runs (`corpus-benchmark` and `db-benchmark`, run 1, the repairing harness) are cut right
after its first failed call: the instruction, the question, the student's calls and the real error. The teacher
gets that conversation and goes on with the same harness and tool (`run-model --start`). A continuation with the
right answer shows a way out of the student's own mistake. The student's call is in the history, never a target.

The continuations are saved like any run, under the set `<set><tag>` (for example `bench2rec17`), so that
`a4a train-data --sets ... bench2rec17` takes them, and its split keeps the test sources out.

Writes out/training/recovery-<tag>.json and .md: per source, the student's runs, the ones with a failed call, and
the teacher's right continuations.
"""

import argparse
import json
import os
import re
import subprocess
import sys
import tempfile
import time
from pathlib import Path

from a4a.corpus.benchmark import python_server, repositories, run_file, run_tag
from a4a.corpus.scan import OUT as CORPUS, folder_name
from a4a.databases.benchmark import databases, sql_server
from a4a.evaluation.run_model import REMINDER
from a4a.paths import API_KEY_FILE, REPO_ROOT
from a4a.sources.python_repository import drop_box
from a4a.traces.format import read_traces
from a4a.training.data import OUT

TASKS = {"bench2": "tasks", "aimed1": "tasks-aimed", "db1": "tasks"}
TOOL = {"bench2": "python", "aimed1": "python", "db1": "sql"}


def is_error(message: dict) -> bool:
    """A tool reply that is an error (the harness and the MCP server both start it with "Error")."""
    return message["role"] == "tool" and str(message.get("content", "")).lstrip('"').startswith("Error")


def failed_state(trace: dict) -> list[dict] | None:
    """The conversation of the first request that follows a failed call, or None. Not after the reminder: the
    reminder is the harness's, and a continuation from it would teach an answer to it."""
    for request in trace["requests"]:
        messages = request["messages"]
        if any(m["role"] == "user" and m.get("content") == REMINDER for m in messages):
            return None
        if messages and is_error(messages[-1]):
            return messages
    return None


def sources(sets: list[str]) -> list[dict]:
    """Every source with questions in one of the sets: {set, stem, path, topic, kind, tool, and how to serve its tool}."""
    found = []
    for set_name in sets:
        if TOOL[set_name] == "python":
            for repo in repositories(1, TASKS[set_name]):
                found.append({"set": set_name, "stem": repo["stem"], "path": repo["path"], "topic": f"the Python library {repo['package']}", "kind": "repository"})
        else:
            for database in databases(1, TASKS[set_name]):
                found.append({"set": set_name, "stem": database["stem"], "path": database["path"], "kind": "database", "database": database,
                              "topic": f"the SQLite database {database['package']} ({database['candidate']['what']})"})
    return found


def server(source: dict, scanned: dict) -> tuple[list[str], str]:
    """The command that serves the source's one tool in its sandbox, and the sandbox's name (to drop it after)."""
    if source["kind"] == "database":
        name = f"sql-{source['stem']}-{os.getpid()}"
        return sql_server(source["database"]["candidate"], name, source["database"]["file"]), name
    name = f"python-{source['stem']}-{os.getpid()}"
    return python_server(scanned[source["stem"]], name), name


def continue_runs(source: dict, states: list[dict], args, scanned: dict, env: dict) -> str:
    """Let the teacher go on from each state; returns "" or why it could not."""
    command, box = server(source, scanned)
    try:
        with tempfile.NamedTemporaryFile("w", suffix=".jsonl", delete=False) as start:
            start.write("".join(json.dumps(state) + "\n" for state in states))
        done = subprocess.run([sys.executable, "-m", "a4a.cli", "run-model", str(source["path"]), "--mode", "tools", "--base-url", args.base_url, "--model", args.teacher,
                               "--topic", source["topic"], "--remind", "--repair-calls", "--plain-text", "--start", start.name,
                               "--tag", run_tag(source["set"] + args.tag, source["stem"], TOOL[source["set"]]), "--", *command],
                              env=env, cwd=REPO_ROOT, capture_output=True, text=True)
        Path(start.name).unlink()
        return "" if done.returncode == 0 else done.stderr.strip()[-300:]
    finally:
        drop_box(box)


def report(tag: str, rows: list[dict], student: str, teacher: str) -> str:
    lines = [f"# Recovery examples `{tag}`", "",
             f"The runs of `{student}` (run 1) are cut right after the first failed call; `{teacher}` goes on from there. Saved as the sets `<set>{tag}`.", "",
             "| Set | Source | Student's runs | With a failed call | Student right anyway | Teacher went on | Teacher right |", "| --- | --- | --- | --- | --- | --- | --- |"]
    for r in rows:
        lines.append(f"| {r['set']} | {r['stem']} | {r['runs']} | {r['failed']} | {r['student_right']} | {r['continued']} | {r['teacher_right']} |")
    total = {k: sum(r[k] for r in rows) for k in ("runs", "failed", "student_right", "continued", "teacher_right")}
    lines.append(f"| **all** | | **{total['runs']}** | **{total['failed']}** | **{total['student_right']}** | **{total['continued']}** | **{total['teacher_right']}** |")
    return "\n".join(lines) + "\n"


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("--student", required=True, help="the model whose saved runs give the failed calls")
    parser.add_argument("--teacher", required=True, help="the model that goes on, as served")
    parser.add_argument("--base-url", help="the teacher's endpoint; without it, only the report is built")
    parser.add_argument("--tag", required=True, help="letters and digits; the continuations are saved as the sets <set><tag>")
    parser.add_argument("--sets", nargs="+", default=list(TOOL), choices=list(TOOL), help="the benchmark tags of the student's runs")
    parser.add_argument("--only", nargs="+", metavar="STEM", help="only these sources")
    args = parser.parse_args()
    if not re.fullmatch(r"[a-z0-9]+", args.tag):
        parser.error("--tag takes lowercase letters and digits only, so that `a4a train-data` reads the set names")

    scanned = {folder_name(r["repo"]): r for r in json.loads((CORPUS / "static.json").read_text())["repositories"] if not r["error"]}
    env = {**os.environ, "OPENAI_API_KEY": os.environ.get("OPENAI_API_KEY") or API_KEY_FILE.read_text().strip()}
    rows = []
    for source in sources(args.sets):
        if args.only and source["stem"] not in args.only:
            continue
        traces = REPO_ROOT / "out" / "traces" / (run_file(args.student, TOOL[source["set"]], source["set"], source["stem"]).name + ".gz")
        if not traces.is_file():
            continue
        runs = list(read_traces(traces))
        states = [{"id": trace["task_id"], "messages": state, "student_right": bool(trace["outcome"]["passed"])} for trace in runs if (state := failed_state(trace))]
        saved = run_file(args.teacher, TOOL[source["set"]], source["set"] + args.tag, source["stem"])
        if args.base_url and states and not saved.is_file():
            started = time.monotonic()
            why = continue_runs(source, [{"id": s["id"], "messages": s["messages"]} for s in states], args, scanned, env)
            print(f"{source['set']} {source['stem']}: {len(states)} continuations in {time.monotonic() - started:.0f} s{f' (failed: {why})' if why else ''}", flush=True)
        continued = [json.loads(line) for line in saved.read_text().splitlines()] if saved.is_file() else []
        rows.append({"set": source["set"], "stem": source["stem"], "runs": len(runs), "failed": len(states), "student_right": sum(s["student_right"] for s in states),
                     "continued": len(continued), "teacher_right": sum(bool(r["passed"]) for r in continued)})
    OUT.mkdir(parents=True, exist_ok=True)
    (OUT / f"recovery-{args.tag}.json").write_text(json.dumps({"student": args.student, "teacher": args.teacher, "tag": args.tag, "sources": rows}, indent=1) + "\n", encoding="utf-8")
    (OUT / f"recovery-{args.tag}.md").write_text(report(args.tag, rows, args.student, args.teacher), encoding="utf-8")
    print(f"-> out/training/recovery-{args.tag}.md")


if __name__ == "__main__":
    main()
