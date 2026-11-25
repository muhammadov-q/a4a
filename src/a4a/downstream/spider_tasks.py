"""Spider's dev questions in the format of run-model, with answers from running the gold query in the sandbox.

    uv run a4a spider-tasks [--max-rows 20]

For each question of Spider's dev set (`a4a public-fetch` first) the gold query is run twice on its database,
in a sandbox that holds a copy of the database file, read-only. A question is kept when both runs give the same
rows, every value is plain (no binary data), and there are at most --max-rows rows: a model writes its answer
as a JSON value, so a long result would test copying more than SQL. The answer of a kept question is the rows.

A model answers with a value, not a query, as in `a4a db-benchmark`. The answer is right when it gives the same
rows as the gold query, in the same order if the gold query orders its result at the top level, with the
columns in any order (`rows_match` in evaluation/exercise_check.py). This is close to Spider's execution match,
but it is not Spider's official metric, which runs the model's query.

Writes out/downstream/spider/tasks/<database>.jsonl and out/downstream/spider/tasks.md. Spider is under
CC BY-SA 4.0, and so are these files.
"""

import argparse
import json
import os
import re
from collections import Counter
from pathlib import Path

from a4a.databases.fetch import sha256_of
from a4a.downstream.fetch import CACHE, spider_dev
from a4a.paths import REPO_ROOT
from a4a.sources.base import run_drafts
from a4a.sources.python_repository import drop_box
from a4a.sources.sqlite_database import SqliteDatabase, probe

OUT = REPO_ROOT / "out" / "downstream" / "spider"
MAX_ROWS = 20
TASK = "In the SQLite database `{database}`: {question}\n\nGive the result as a JSON value: one value, a list of values, or a list of rows (each row a list)."


def ordered(sql: str) -> bool:
    """Whether a query orders its result: an ORDER BY outside every bracket (and outside quoted text)."""
    text = re.sub(r"'[^']*'|\"[^\"]*\"", "''", sql)
    while (inner := re.sub(r"\([^()]*\)", "", text)) != text:
        text = inner
    return re.search(r"\border\s+by\b", text, re.IGNORECASE) is not None


def rows_expression(sql: str) -> str:
    return f"[list(row) for row in db.execute({sql!r}).fetchall()]"


def answers(database: str, file: Path, queries: list[str]) -> list[tuple[list | None, str]]:
    """Per query (its rows, "ok"), or (None, why not), from two runs in a sandbox with a copy of the database."""
    source = SqliteDatabase({"name": f"spider-{database}-{os.getpid()}"}, file)
    try:
        box = source.box(source.box_name)
        drafts = [probe(rows_expression(q)) for q in queries]
        first, second = run_drafts(box, drafts), run_drafts(box, drafts)
    finally:
        drop_box(source.box_name)
    if first is None or second is None:
        raise RuntimeError(f"{database}: the sandboxed run did not finish")
    found = []
    for a, b in zip(first, second):
        if a["status"] != "ok":
            error = str(a.get("error") or "")
            found.append((None, "the result is too long for the worker" if "too long" in error else "not plain JSON" if a["status"] == "not_json" else
                          "text that is not UTF-8" if "decode to UTF-8" in error else "the gold query fails"))
        else:
            found.append((a["value"], "ok") if b["status"] == "ok" and a["value"] == b["value"] else (None, "two runs differ"))
    return found


def task(index: int, question: dict, rows: list, zip_sha256: str) -> dict:
    database = question["db_id"]
    return {"id": f"{database}-{index:04d}", "kind": database, "horizon": "short", "task": TASK.format(database=database, question=question["question"].strip()),
            "answer": rows, "check": {"kind": "rows", "ordered": ordered(question["query"])}, "reference_calls": [], "reference_call_count": 1,
            "library_functions": [], "source_repo": f"spider-dev@{zip_sha256[:7]}", "reference_code": [question["query"]],
            "provenance": {"benchmark": "spider", "split": "dev", "index": index, "answer_from": "the gold query, run twice in the sandbox with the same result"}}


def build(dev: Path, out: Path, max_rows: int, zip_sha256: str) -> dict:
    """Every kept question, by database, written to out/tasks/. Returns what was kept and why the rest was not."""
    questions = json.loads((dev / "dev.json").read_text(encoding="utf-8"))
    by_database: dict[str, list[int]] = {}
    for index, question in enumerate(questions):
        by_database.setdefault(question["db_id"], []).append(index)
    (out / "tasks").mkdir(parents=True, exist_ok=True)
    summary = {"questions": len(questions), "databases": {}, "dropped": Counter(), "rows": Counter()}
    for database, indexes in sorted(by_database.items()):
        rows = answers(database, dev / "database" / f"{database}.sqlite", [questions[i]["query"] for i in indexes])
        kept = []
        for index, (result, why) in zip(indexes, rows):
            if result is None:
                summary["dropped"][why] += 1
            elif len(result) > max_rows:
                summary["dropped"][f"more than {max_rows} rows"] += 1
            else:
                kept.append(task(index, questions[index], result, zip_sha256))
                summary["rows"]["0" if not result else "1" if len(result) == 1 else "2 to 5" if len(result) <= 5 else f"6 to {max_rows}"] += 1
        (out / "tasks" / f"{database}.jsonl").write_text("".join(json.dumps(t) + "\n" for t in kept), encoding="utf-8")
        summary["databases"][database] = {"questions": len(indexes), "kept": len(kept), "ordered": sum(t["check"]["ordered"] for t in kept)}
        print(f"{database}: {len(kept)} of {len(indexes)}", flush=True)
    return summary


def report(summary: dict, max_rows: int) -> str:
    kept = sum(d["kept"] for d in summary["databases"].values())
    lines = ["# Spider's dev questions, with answers from the gold query", "",
             f"{kept} of {summary['questions']} questions kept, on {len(summary['databases'])} databases. A question is kept when its gold query, run twice in the sandbox, "
             f"gives the same plain rows, at most {max_rows} of them. A model answers with a value; it is right when the value gives the same rows as the gold query "
             "(in order if the query orders them at the top level, columns in any order). This is close to Spider's execution match, not its official metric.", "",
             "| Not kept | Questions |", "| --- | --- |", *(f"| {reason} | {n} |" for reason, n in summary["dropped"].most_common()), "",
             "| Rows in the answer | Questions |", "| --- | --- |", *(f"| {k} | {summary['rows'][k]} |" for k in ("0", "1", "2 to 5", f"6 to {max_rows}") if summary["rows"][k]), "",
             "| Database | Questions | Kept | Ordered |", "| --- | --- | --- | --- |",
             *(f"| `{name}` | {d['questions']} | {d['kept']} | {d['ordered']} |" for name, d in summary["databases"].items()), "",
             "Spider is under CC BY-SA 4.0 (https://yale-lily.github.io/spider), and so are the files in this folder.", ""]
    return "\n".join(lines)


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("--max-rows", type=int, default=MAX_ROWS, help="keep a question only if its answer has at most this many rows")
    args = parser.parse_args()
    if not (spider_dev() / "dev.json").is_file():
        parser.error("run `a4a public-fetch --only spider` first")
    summary = build(spider_dev(), OUT, args.max_rows, sha256_of(CACHE / "spider" / "spider_data.zip"))
    (OUT / "tasks.md").write_text(report(summary, args.max_rows), encoding="utf-8")
    print(f"-> {(OUT / 'tasks.md').relative_to(REPO_ROOT)}")


if __name__ == "__main__":
    main()
