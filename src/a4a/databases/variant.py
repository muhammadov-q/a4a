"""A database the models have not seen: the same schema with part of its rows removed, and the same questions with their answers computed again.

    uv run a4a db-variant [--seed 1] [--keep 0.7] [--only name ...]

The approved databases are public samples, copied all over the web, and a large model remembers much of
them. For every database with questions (`a4a db-tasks`) this command

  1. copies the database into a sandbox and removes rows there: each row of each table is kept with
     probability `--keep`, drawn with a generator seeded by `--seed` and the table name. Foreign keys are not
     enforced, so a row that refers to a removed row stays; a join simply does not find it.
  2. runs the query of every question twice on that copy, in the sandbox, and keeps the question with the new
     answer if both runs give the same plain value. The wording stays the same.
  3. marks a question as "changed" when the new answer is not the old one. Only those can tell memory from
     skill: a model that answers from memory gives the old answer.

Writes .cache/databases/<name>/variant-<seed>.sqlite, out/databases/tasks-v<seed>/<name>.jsonl (the questions,
same ids, with `provenance.original_answer`), and out/databases/variant-<seed>.json and .md.
"""

import argparse
import json
import shutil
import subprocess
from collections import Counter
from pathlib import Path

from a4a.databases.exercises import OUT
from a4a.databases.fetch import CACHE, LIST, database_path, sha256_of
from a4a.evaluation.exercise_check import check
from a4a.repo2tools import pipeline
from a4a.sources.base import EXAMPLE_WORKER, run_drafts
from a4a.sources.python_repository import drop_box
from a4a.sources.sqlite_database import DATABASE, STEPS, SqliteDatabase, one_row, one_value

SECONDS = 600
SHRINK = """
import random, sqlite3, sys
seed, keep = sys.argv[1], float(sys.argv[2])
db = sqlite3.connect(sys.argv[3])
tables = [r[0] for r in db.execute("SELECT name FROM sqlite_master WHERE type = 'table' AND name NOT LIKE 'sqlite_%' ORDER BY name")]
for table in tables:
    quoted = '"' + table.replace('"', '""') + '"'
    try:
        ids = [r[0] for r in db.execute(f"SELECT rowid FROM {quoted} ORDER BY rowid")]
    except sqlite3.OperationalError:
        continue  # a table without rowid keeps its rows
    rng = random.Random(f"{seed}:{table}")
    db.executemany(f"DELETE FROM {quoted} WHERE rowid = ?", [(i,) for i in ids if rng.random() >= keep])
db.commit()
db.execute("VACUUM")
db.close()
"""
ONE_ROW = ("range", "most")


def variant_path(candidate: dict, seed: int, cache: Path = CACHE) -> Path:
    return cache / candidate["name"] / f"variant-{seed}.sqlite"


def shrink(source: Path, target: Path, seed: int, keep: float) -> None:
    """Remove rows from a copy of the database, inside a sandbox, and copy the result to `target`."""
    set_name = f"shrink-{target.parent.name}-{seed}"
    try:
        box = pipeline.make_box(set_name, None, None, [], EXAMPLE_WORKER)
        shutil.copy2(source, box.scratch / DATABASE)
        done = subprocess.run(box.command("-c", SHRINK, str(seed), str(keep), DATABASE), capture_output=True, text=True,
                              timeout=SECONDS, env=box.clean_env, cwd=box.scratch)
        if done.returncode != 0:
            raise RuntimeError((done.stderr.strip().splitlines() or ["removing rows failed"])[-1][:200])
        shutil.copy2(box.scratch / DATABASE, target)
    finally:
        drop_box(set_name)


def plain(value) -> bool:
    """A value a question can have as its answer: not missing, and no missing part."""
    return value is not None and value != [] and not (isinstance(value, list) and None in value)


def recomputed(questions: list[dict], source: SqliteDatabase, run=run_drafts) -> tuple[list[dict], Counter]:
    """The questions with their answers on this database, and what happened to each: changed, unchanged, no_answer, not_repeatable."""
    items = [{"module": None, "steps": STEPS, "expression": (one_row if q["provenance"]["template"] in ONE_ROW else one_value)(q["reference_code"][0])} for q in questions]
    box = source.box(source.box_name)
    first, second = run(box, items), run(box, items)
    if first is None or second is None:
        raise RuntimeError("the sandboxed run did not finish")
    kept, outcomes = [], Counter()
    for question, a, b in zip(questions, first, second):
        if a["status"] != "ok" or b["status"] != "ok" or a["value"] != b["value"]:
            outcomes["not_repeatable" if a["status"] == "ok" else "no_answer"] += 1
            continue
        if not plain(a["value"]):
            outcomes["no_answer"] += 1
            continue
        changed = not check(question, a["value"])
        outcomes["changed" if changed else "unchanged"] += 1
        number = isinstance(a["value"], (int, float)) and not isinstance(a["value"], bool)
        kept.append(question | {"answer": a["value"], "check": {"kind": "number" if number else "exact"}, "changed": changed,
                                "provenance": question["provenance"] | {"original_answer": question["answer"],
                                                                         "answer_from": "the same query on a copy of the database with part of its rows removed, run twice in the sandbox"}})
    return kept, outcomes


def report(rows: list[dict], seed: int, keep: float) -> str:
    total = Counter()
    for r in rows:
        total.update(r["outcomes"])
    lines = [f"# Database variants (seed {seed}, each row kept with probability {keep})", "",
             "The same questions on a copy of each database with part of its rows removed. A question whose answer changed can tell memory from skill: "
             "a model that answers from memory gives the old answer.", "",
             "| Database | Rows before | Rows after | Questions | Answer changed | Answer the same | No answer on the variant |", "| --- | --- | --- | --- | --- | --- | --- |"]
    lines += [f"| `{r['database']}` | {r['rows_before']:,} | {r['rows_after']:,} | {r['questions']} | {r['outcomes'].get('changed', 0)} | {r['outcomes'].get('unchanged', 0)} | "
              f"{r['outcomes'].get('no_answer', 0) + r['outcomes'].get('not_repeatable', 0)} |" for r in rows]
    lines += ["", f"Together: {total['changed']} questions with a changed answer, {total['unchanged']} with the same answer.", "",
              "## By template", "", "| Template | Questions | Answer changed |", "| --- | --- | --- |"]
    by_template: dict[str, Counter] = {}
    for r in rows:
        for name, (count, changed) in r["by_template"].items():
            by_template.setdefault(name, Counter()).update({"questions": count, "changed": changed})
    lines += [f"| {name} | {c['questions']} | {c['changed']} |" for name, c in by_template.items()]
    return "\n".join(lines) + "\n"


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("--seed", type=int, default=1)
    parser.add_argument("--keep", type=float, default=0.7, help="the probability that a row is kept")
    parser.add_argument("--only", nargs="+", help="only these databases")
    args = parser.parse_args()
    folder = OUT / f"tasks-v{args.seed}"
    folder.mkdir(parents=True, exist_ok=True)
    rows = []
    for candidate in json.loads(LIST.read_text(encoding="utf-8"))["databases"]:
        questions_file = OUT / "tasks" / f"{candidate['name']}.jsonl"
        if not questions_file.is_file() or (args.only and candidate["name"] not in args.only):
            continue
        target = variant_path(candidate, args.seed)
        if not target.is_file():
            shrink(database_path(candidate), target, args.seed, args.keep)
        questions = [json.loads(line) for line in questions_file.read_text(encoding="utf-8").splitlines()]
        original, variant = SqliteDatabase(candidate, database_path(candidate)), SqliteDatabase(candidate | {"name": f"{candidate['name']}-v{args.seed}"}, target)
        try:
            before, after = (sum(t["rows"] for t in s.schema["tables"].values()) for s in (original, variant))
            kept, outcomes = recomputed(questions, variant)
        finally:
            drop_box(original.box_name)
            drop_box(variant.box_name)
        sha = sha256_of(target)
        kept = [q | {"source_repo": f"{candidate['name']}-v{args.seed}@{sha[:7]}", "provenance": q["provenance"] | {"variant": {"seed": args.seed, "keep": args.keep, "sha256": sha}}} for q in kept]
        (folder / questions_file.name).write_text("".join(json.dumps(q) + "\n" for q in kept), encoding="utf-8")
        by_template = Counter(q["provenance"]["template"] for q in kept)
        changed = Counter(q["provenance"]["template"] for q in kept if q["changed"])
        rows.append({"database": candidate["name"], "rows_before": before, "rows_after": after, "questions": len(questions), "outcomes": dict(outcomes),
                     "by_template": {name: [count, changed[name]] for name, count in by_template.items()}, "sha256": sha})
        print(f"{candidate['name']}: rows {before:,} -> {after:,}; {dict(outcomes)}", flush=True)
    if not args.only:
        (OUT / f"variant-{args.seed}.json").write_text(json.dumps({"seed": args.seed, "keep": args.keep, "databases": rows}, indent=1) + "\n", encoding="utf-8")
        (OUT / f"variant-{args.seed}.md").write_text(report(rows, args.seed, args.keep), encoding="utf-8")
    print(f"-> out/databases/tasks-v{args.seed}/")


if __name__ == "__main__":
    main()
