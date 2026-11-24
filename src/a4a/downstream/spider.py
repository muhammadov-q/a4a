"""Score a model on Spider's dev questions with the SQL tool.

    uv run a4a spider-benchmark --model qwen3-4b --base-url http://127.0.0.1:18004/v1 [--parallel 4] [--only database ...]

Per database, `a4a run-model` answers its questions (`a4a spider-tasks`) with one tool, `run_sql`: the same
read-only tool, instruction and harness as `a4a db-benchmark`, inside a sandbox that holds a copy of the
database. One run per model: at temperature 0 more runs give nearly the same answers, and the uncertainty is
in the questions. Databases run --parallel at a time, each in a sandbox of its own.

Writes out/downstream/spider/benchmark-<model>.json and .md; the runs are out/runs/<model>-tools-spider1-<database>-sql-repair.jsonl.
`a4a train-data` reads only the tags it is given (bench2, aimed1, db1 by default), so these runs never become training data.
"""

import argparse
import json
import os
import re
import subprocess
import sys
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path

from a4a.corpus.benchmark import run_file, run_tag, saved_runs
from a4a.databases.benchmark import sql_server
from a4a.downstream.fetch import spider_dev
from a4a.downstream.spider_tasks import OUT
from a4a.paths import API_KEY_FILE, REPO_ROOT
from a4a.sources.python_repository import drop_box

TAG = "spider1"
WAY = "sql"


def databases(tasks: Path = OUT / "tasks", dev: Path | None = None) -> list[dict]:
    """The Spider databases with questions: {"stem", "path", "tasks", "file"}."""
    dev = dev or spider_dev()
    return [{"stem": path.stem, "path": path, "tasks": len(path.read_text(encoding="utf-8").splitlines()), "file": dev / "database" / f"{path.stem}.sqlite"}
            for path in sorted(tasks.glob("*.jsonl"))]


def run_database(database: dict, args, env: dict) -> str:
    """The run of one database, unless it is saved. Returns a line for the log."""
    if run_file(args.model, WAY, TAG, database["stem"]).is_file():
        return f"{database['stem']}: saved"
    set_name = f"sql-spider-{database['stem']}-{os.getpid()}"
    try:
        server = sql_server({"name": database["stem"]}, set_name, database["file"])
        command = [sys.executable, "-m", "a4a.cli", "run-model", str(database["path"]), "--mode", "tools", "--base-url", args.base_url, "--model", args.model,
                   "--topic", f"the SQLite database {database['stem']}", "--remind", "--tag", run_tag(TAG, database["stem"], WAY), "--concurrency", str(args.concurrency),
                   "--repair-calls", "--plain-text", "--", *server]
        done = subprocess.run(command, env=env, cwd=REPO_ROOT, capture_output=True, text=True)
    finally:
        drop_box(set_name)
    return f"{database['stem']}: " + ("done" if done.returncode == 0 else f"failed: {done.stderr.strip()[-300:]}")


def summary(found: list[dict], model: str) -> dict:
    """Right answers per database from the saved runs, and every question's result by id."""
    rows, passed = [], {}
    for database in found:
        runs = saved_runs(model, WAY, TAG, database["stem"])
        if runs:
            passed |= {r["id"]: bool(r["passed"]) for r in runs[0]}
            rows.append({"database": database["stem"], "questions": database["tasks"], "right": sum(r["passed"] for r in runs[0]),
                         "no_answer": sum(r.get("finish") != "answered" for r in runs[0]), "tool_calls": sum(r.get("tool_calls", 0) for r in runs[0])})
    return {"model": model, "tag": TAG, "databases": rows, "passed": passed}


def report(record: dict, total_databases: int) -> str:
    rows = record["databases"]
    questions, right = sum(r["questions"] for r in rows), sum(r["right"] for r in rows)
    lines = [f"# Spider dev with the SQL tool: `{record['model']}`", "",
             f"{len(rows)} of {total_databases} databases run, {questions} questions, one run. Right: {right} ({right / max(questions, 1):.0%}). "
             "An answer is right when it gives the same rows as the gold query (out/downstream/spider/tasks.md).", "",
             "| Database | Questions | Right | No answer | Tool calls |", "| --- | --- | --- | --- | --- |",
             *(f"| `{r['database']}` | {r['questions']} | {r['right']} ({r['right'] / r['questions']:.0%}) | {r['no_answer']} | {r['tool_calls']} |" for r in rows), ""]
    return "\n".join(lines)


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("--model", required=True, help="the model that answers, as the server names it")
    parser.add_argument("--base-url")
    parser.add_argument("--parallel", type=int, default=4, help="databases at a time")
    parser.add_argument("--concurrency", type=int, default=16, help="questions at a time within a database")
    parser.add_argument("--only", nargs="+", metavar="DATABASE", help="run only these databases; the report covers every saved run")
    parser.add_argument("--report-only", action="store_true", help="only build the report from the saved runs")
    args = parser.parse_args()
    found = databases()
    if not found:
        parser.error("no questions: run `a4a spider-tasks` first")
    if not args.report_only:
        if not args.base_url:
            parser.error("--base-url is needed to run a model")
        env = {**os.environ, "OPENAI_API_KEY": os.environ.get("OPENAI_API_KEY") or API_KEY_FILE.read_text().strip()}  # the key reaches the model runs, never a sandbox
        wanted = [d for d in found if not args.only or d["stem"] in args.only]
        with ThreadPoolExecutor(args.parallel) as pool:
            for line in pool.map(lambda d: run_database(d, args, env), wanted):
                print(line, flush=True)
    record = summary(found, args.model)
    name = re.sub(r"[^A-Za-z0-9._-]+", "-", f"benchmark-{args.model}")
    (OUT / f"{name}.json").write_text(json.dumps(record, indent=1) + "\n", encoding="utf-8")
    (OUT / f"{name}.md").write_text(report(record, len(found)), encoding="utf-8")
    print(f"-> {(OUT / name).relative_to(REPO_ROOT)}.md")


if __name__ == "__main__":
    main()
