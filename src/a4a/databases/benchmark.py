"""Can a model answer the database questions, without a tool and with one tool that runs SQL?

    uv run a4a db-benchmark --tag db1 --model qwen3-8b --base-url http://127.0.0.1:18001/v1 [--runs 1] [--only name ...]
    uv run a4a db-benchmark --tag db1v1 --tasks tasks-v1 --variant 1 ...     # the questions of `a4a db-variant`, on the changed databases

For every database with questions (`a4a db-tasks`) the model answers them twice:

    none   no tool: it can only answer from what it remembers of a well-known sample database, or guess
    sql    one tool, `run_sql`, that runs a read-only query on the database inside the sandbox (`sql_tool.py`)

The runs are made by `a4a run-model` with the same harness as `a4a corpus-benchmark`, and the report is
built by the same code, so the two can be read side by side. A saved run is not made again. `--no-repeat` does
not run a call that is the same as an earlier one of the run; its runs and report end in `-norepeat`.

Writes out/databases/benchmark-<tag>-<model>.json and .md; the runs are in out/runs/, the traces in out/traces/.
"""

import argparse
import json
import os
import re
import subprocess
import sys
import time
from pathlib import Path

from a4a.corpus.benchmark import breakdown, report, run_file, run_tag, summarize
from a4a.databases.exercises import OUT
from a4a.databases.fetch import LIST, database_path
from a4a.databases.variant import variant_path
from a4a.paths import API_KEY_FILE, REPO_ROOT
from a4a.sources.python_repository import drop_box
from a4a.sources.sqlite_database import DATABASE, SqliteDatabase

SQL_TOOL = Path(__file__).resolve().parent / "sql_tool.py"
WAYS = {"none": "No tools", "sql": "One SQL tool"}


def databases(min_tasks: int, tasks: str = "tasks", variant: int | None = None) -> list[dict]:
    """The approved databases with enough questions in out/databases/<tasks>/, in the shape the benchmark's summary reads:
    {"stem", "path", "package", "url", "tasks"}, the candidate, and the database file the SQL tool serves (a variant's, with `variant`)."""
    found = []
    for candidate in json.loads(LIST.read_text(encoding="utf-8"))["databases"]:
        path = OUT / tasks / f"{candidate['name']}.jsonl"
        count = len(path.read_text(encoding="utf-8").splitlines()) if path.is_file() else 0
        if count >= min_tasks:
            file = database_path(candidate) if variant is None else variant_path(candidate, variant)
            found.append({"stem": candidate["name"], "path": path, "package": candidate["name"], "url": candidate["repo"], "tasks": count, "candidate": candidate, "file": file})
    return found


def sql_server(candidate: dict, set_name: str, file: Path) -> list[str]:
    """The command that serves the SQL tool inside a sandbox that holds a copy of the database file."""
    box = SqliteDatabase(candidate, file).box(set_name, readable=SQL_TOOL)
    return ["env", "-i", *(f"{name}={value}" for name, value in box.clean_env.items()), *box.command(str(SQL_TOOL), "--database", str(box.scratch / DATABASE))]


def run_database(database: dict, args, env: dict) -> None:
    """Every run of this database that is not saved yet."""
    wanted = [(way, k) for way in WAYS for k in range(1, args.runs + 1) if not run_file(args.model, way, args.tag, database["stem"], k, no_repeat=args.no_repeat).is_file()]
    if not wanted:
        return
    started, set_name = time.monotonic(), f"sql-{database['stem']}"
    try:
        server = sql_server(database["candidate"], set_name, database["file"]) if any(way == "sql" for way, _ in wanted) else []
        for way, k in wanted:
            command = [sys.executable, "-m", "a4a.cli", "run-model", str(database["path"]), "--mode", "none" if way == "none" else "tools",
                       "--base-url", args.base_url, "--model", args.model, "--topic", f"the SQLite database {database['package']} ({database['candidate']['what']})", "--remind",
                       "--tag", run_tag(args.tag, database["stem"], way, k)]
            if way == "sql":
                command += ["--repair-calls", "--plain-text", *(["--no-repeat"] if args.no_repeat else []), "--", *server]
            done = subprocess.run(command, env=env, cwd=REPO_ROOT, capture_output=True, text=True)
            if done.returncode != 0:
                print(f"{database['package']}: {way} run {k} failed: {done.stderr.strip()[-300:]}", flush=True)
    finally:
        drop_box(set_name)
    print(f"{database['package']}: done in {time.monotonic() - started:.0f} s", flush=True)


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("--tag", required=True, help="names this benchmark: runs <model>-<mode>-<tag>-<database>")
    parser.add_argument("--model", default="qwen3-8b", help="the model that answers")
    parser.add_argument("--base-url")
    parser.add_argument("--runs", type=int, default=1, help="how often the model answers in each way")
    parser.add_argument("--only", nargs="+", metavar="DATABASE", help="run only these databases; the report still covers all")
    parser.add_argument("--min-tasks", type=int, default=5)
    parser.add_argument("--tasks", default="tasks", help="the question set: a folder under out/databases/")
    parser.add_argument("--variant", type=int, help="serve the database of `a4a db-variant --seed N` to the SQL tool")
    parser.add_argument("--report-only", action="store_true", help="only build the report from the saved runs")
    parser.add_argument("--no-repeat", action="store_true", help="do not run a call that is the same as an earlier one of the run (run-model --no-repeat)")
    args = parser.parse_args()
    found = databases(args.min_tasks, args.tasks, args.variant)
    if args.variant is not None and args.tasks == "tasks":
        parser.error("--variant needs the questions of that variant: --tasks tasks-v<seed>")
    if not args.report_only:
        if not args.base_url:
            parser.error("--base-url is needed to run a model")
        env = {**os.environ, "OPENAI_API_KEY": os.environ.get("OPENAI_API_KEY") or API_KEY_FILE.read_text().strip()}  # the key reaches the model runs, never a sandbox
        for database in found:
            if not args.only or database["package"] in args.only:
                run_database(database, args, env)
    rows = summarize(found, args.model, args.tag, conditions=WAYS, no_repeat=args.no_repeat)
    details = breakdown(found, args.model, args.tag, conditions=WAYS, no_repeat=args.no_repeat)
    name = re.sub(r"[^A-Za-z0-9._-]+", "-", f"benchmark-{args.tag}-{args.model}{'-norepeat' if args.no_repeat else ''}")
    record = {"model": args.model, "tag": args.tag, **({"no_repeat": True} if args.no_repeat else {}), "min_tasks": args.min_tasks}
    (OUT / f"{name}.json").write_text(json.dumps({**record, "repositories": rows, **details}, indent=1) + "\n", encoding="utf-8")
    (OUT / f"{name}.md").write_text(report(rows, args.model, args.tag, False, details, where="the questions about each database; a row is a database", conditions=WAYS,
                                           no_repeat=args.no_repeat), encoding="utf-8")
    print(f"-> out/databases/{name}.md")


if __name__ == "__main__":
    main()
