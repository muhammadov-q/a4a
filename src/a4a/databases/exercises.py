"""Exercises with known answers from the approved databases, and what they cover.

    uv run a4a db-exercises [--only name ...]

For every database that `a4a db-fetch` has put in .cache/databases/ this command

  1. reads the schema inside a sandbox and makes drafts from templates over it (`sources.sqlite_database`),
  2. runs every draft twice in the sandbox and keeps it as verified if both runs give the same plain value,
  3. reports density (verified exercises per 1,000 rows and per line of schema) and coverage (the share of
     tables and columns that at least one verified exercise uses).

The pass is the same one that `a4a corpus-exercises` runs on repositories; only the source differs. A
database shows no expected result, so the answer of an exercise comes from its query alone.

Writes out/databases/exercises/<name>.jsonl, out/databases/exercises.json and out/databases/exercises.md.
"""

import argparse
import json
from collections import Counter
from pathlib import Path

from a4a.corpus.exercises import exercises_from
from a4a.databases.fetch import LIST, database_path, sha256_of
from a4a.paths import REPO_ROOT
from a4a.sources.sqlite_database import TEMPLATES, SqliteDatabase

OUT = REPO_ROOT / "out" / "databases"


def exercises_of(candidate: dict, path: Path, keep_environment: bool = False) -> tuple[dict, list[dict]]:
    """(record of what happened and what the exercises cover, verified exercises) for one database file. Never raises."""
    source = SqliteDatabase(candidate | {"sha256": sha256_of(path)}, path)
    record, exercises = exercises_from(source, {"database": candidate["name"], "sha256": source.candidate["sha256"]}, keep_environment=keep_environment)
    if record["error"]:
        return record, exercises
    elements, used = source.elements(), {use for e in exercises for use in e["uses"]}
    tables = source.schema["tables"]
    record |= {"tables": len(tables), "columns": sum(len(t["columns"]) for t in tables.values()), "parts": source.parts(),
               "elements": len(elements), "covered": len(elements & used), "not_covered": sorted(elements - used),
               "templates": {name: [made, kept] for name in TEMPLATES
                             for made, kept in [(sum(1 for d in source.drafts() if d["template"] == name), sum(1 for e in exercises if e["template"] == name))]}}
    return record, exercises


def per_thousand(count: int, size: int) -> str:
    return f"{1000 * count / size:.1f}" if size else "n/a"


def report(records: list[dict]) -> str:
    good = [r for r in records if not r["error"]]
    lines = ["# Exercises from databases", "",
             f"{len(good)} of {len(records)} databases. Drafts come from templates over the schema, without a model. "
             "A draft is verified if two sandboxed runs give the same plain value; there is no documented result to compare with.", ""]
    if good:
        lines += ["| Database | Tables | Columns | Rows | Lines of schema | Drafts | Verified | Per 1,000 rows | Per line of schema | Tables and columns covered |",
                  "| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |"]
        for r in good:
            verified = r["outcomes"].get("verified", 0)
            lines.append(f"| `{r['database']}` | {r['tables']} | {r['columns']} | {r['parts']['rows']:,} | {r['parts']['schema']:,} | {r['drafts']} | {verified} | "
                         f"{per_thousand(verified, r['parts']['rows'])} | {verified / r['parts']['schema'] if r['parts']['schema'] else 0:.2f} | "
                         f"{r['covered']} of {r['elements']} ({r['covered'] / max(r['elements'], 1):.0%}) |")
        lines += ["", "## By template", "", "| Template | What it asks | Drafts | Verified |", "| --- | --- | --- | --- |"]
        for name, what in TEMPLATES.items():
            lines.append(f"| {name} | {what} | {sum(r['templates'][name][0] for r in good)} | {sum(r['templates'][name][1] for r in good)} |")
        outcomes = Counter()
        for r in good:
            outcomes.update(r["outcomes"])
        lines += ["", "What happened to the drafts: " + ", ".join(f"{name} {count}" for name, count in outcomes.most_common()) + ".", ""]
        missing = [(r["database"], r["not_covered"]) for r in good if r["not_covered"]]
        if missing:
            lines += ["## Not covered", "", "Tables and columns that no verified exercise uses (an empty table, or values that are not plain JSON):", ""]
            lines += [f"- `{name}`: {', '.join(f'`{e}`' for e in elements[:20])}" + (f" and {len(elements) - 20} more" if len(elements) > 20 else "") for name, elements in missing]
            lines.append("")
    failed = [r for r in records if r["error"]]
    if failed:
        lines += ["## Failed", "", "| Database | Reason |", "| --- | --- |"]
        lines += [f"| `{r['database']}` | {r['error'].replace('|', '/')} |" for r in failed]
    return "\n".join(lines).rstrip("\n") + "\n"


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("--only", nargs="+", help="only these databases")
    args = parser.parse_args()
    candidates = [c for c in json.loads(LIST.read_text(encoding="utf-8"))["databases"] if not args.only or c["name"] in args.only]
    folder = OUT / "exercises"
    folder.mkdir(parents=True, exist_ok=True)
    records = []
    for candidate in candidates:
        path = database_path(candidate)
        if not path.is_file():
            print(f"{candidate['name']}: no file; run `a4a db-fetch` first")
            continue
        record, exercises = exercises_of(candidate, path)
        target = folder / f"{candidate['name']}.jsonl"
        if exercises:
            target.write_text("".join(json.dumps(e) + "\n" for e in exercises), encoding="utf-8")
        else:
            target.unlink(missing_ok=True)
        print(f"{candidate['name']}: {record['outcomes'].get('verified', 0)} verified of {record['drafts']} {record['outcomes']}" + (f" ({record['error']})" if record["error"] else ""), flush=True)
        records.append(record)
    if not args.only:
        (OUT / "exercises.json").write_text(json.dumps({"databases": records}, indent=1) + "\n", encoding="utf-8")
        (OUT / "exercises.md").write_text(report(records), encoding="utf-8")
    print(f"{sum(r['outcomes'].get('verified', 0) for r in records):,} verified exercises from {len(records)} databases -> out/databases/exercises.md")


if __name__ == "__main__":
    main()
