"""Questions in plain words for the verified database exercises: exercises a model can be scored on.

    uv run a4a db-tasks --base-url http://127.0.0.1:18003/v1 --model qwen3-32b \\
        --solver-base-url http://127.0.0.1:18000/v1 --solver-model qwen3-coder [--per-database 40] [--only name ...]

`a4a db-exercises` leaves, per database, queries whose answer is known. Here an LLM writes, for each, the
request of a person who needs that value and does not see the query. As for the library questions
(`a4a corpus-tasks`), a request must contain every input value of the query, show no SQL, and not give the
answer away; and it is kept only if it says enough: a second model gets the request and the schema of the
database, writes one query, and that query must give the verified answer when it runs in the sandbox.

At most `--per-database` exercises are taken, in turn from each template, so that no template fills the set.
The answer is never the LLM's: it stays the verified value.

Writes out/databases/tasks/<name>.jsonl in the exercise format of `a4a run-model`, and out/databases/tasks.md.
"""

import argparse
import asyncio
import json
import random
import re
from collections import Counter, defaultdict

from a4a.corpus.tasks import ROUNDS
from a4a.databases.exercises import OUT
from a4a.databases.fetch import LIST, database_path
from a4a.evaluation.exercise_check import check
from a4a.repo2tools.pipeline import LLM, extract_json
from a4a.sources.base import run_drafts
from a4a.sources.python_repository import drop_box
from a4a.sources.sqlite_database import STEPS, TEMPLATES, SqliteDatabase

FORMS = {"rows": "a number", "distinct": "a number", "filter": "a number", "range": "a JSON list of two values: the smallest, then the largest",
         "most": "a JSON list of two values: the key of that row, then the number of rows that refer to it"}
SQL_WORDS = re.compile(r"\b(SELECT|FROM|WHERE|GROUP BY|ORDER BY|JOIN|COUNT\s*\(|DISTINCT)\b")


def literals_of(sql: str) -> list[str]:
    """The input values written in a query: texts in single quotes, and numbers that are compared with a column."""
    texts = [t.replace("''", "'") for t in re.findall(r"'((?:[^']|'')*)'", sql)]
    numbers = re.findall(r"=\s*(-?\d+(?:\.\d+)?)\b", re.sub(r"'(?:[^']|'')*'", "''", sql))
    return list(dict.fromkeys([*texts, *numbers]))


def choose(exercises: list[dict], count: int, seed: int = 0) -> list[dict]:
    """At most `count` exercises, taken in turn from each template."""
    by_template: dict[str, list[dict]] = defaultdict(list)
    for exercise in exercises:
        by_template[exercise["template"]].append(exercise)
    rng = random.Random(seed)
    for group in by_template.values():
        rng.shuffle(group)
    chosen: list[dict] = []
    while len(chosen) < count and any(by_template.values()):
        for template in TEMPLATES:
            if by_template[template] and len(chosen) < count:
                chosen.append(by_template[template].pop())
    return sorted(chosen, key=lambda e: e["id"])


def schema_text(schema: dict, tables: list[str] | None = None) -> str:
    """Tables with their columns as one line each: `Album(AlbumId INTEGER key, ArtistId INTEGER -> Artist.ArtistId)`, and the number of rows."""
    lines = []
    for name, table in schema["tables"].items():
        if tables is not None and name not in tables:
            continue
        refers = {column: f"{parent}.{target}" if target else parent for parent, column, target in table["keys"]}
        columns = [f"{c} {facts['type']}".strip() + (" key" if facts["key"] else "") + (f" -> {refers[c]}" if c in refers else "") for c, facts in table["columns"].items()]
        lines.append(f"- {name}({', '.join(columns)}): {table['rows']:,} rows")
    return "\n".join(lines)


def task_messages(exercise: dict, what: str, schema: dict) -> list[dict]:
    tables = [use for use in exercise["uses"] if "." not in use]
    return [
        {"role": "system", "content": "You write short requests that test whether an AI model can find a fact in a database. Reply with JSON only."},
        {"role": "user", "content": f"""This SQL query runs on the SQLite database `{exercise['database']}` ({what}). Its result is the answer.

```sql
{exercise['sql']}
```
Answer: {json.dumps(exercise['answer'])[:400]}

The tables it uses:
{schema_text(schema, tables)}

Write the request of a person who needs exactly this answer and does not see the query. Rules:
- One or two sentences in plain words. Name the database, and say precisely what is to be found, so that a person
  who knows the database could do it without guessing. Names of tables and columns are fine; SQL is not.
- Give every input value exactly as written in the query, character for character: {json.dumps(literals_of(exercise['sql']))}
- Say what the answer must look like: {FORMS[exercise['template']]}.
- Do not give away the answer.

Reply with one JSON object: {{"task": "..."}}"""},
    ]


def task_problem(text, exercise: dict) -> str | None:
    """Why a request is not acceptable, or None."""
    if not isinstance(text, str) or len(text.strip()) < 15:
        return 'reply with {"task": "..."}'
    values = literals_of(exercise["sql"])
    missing = [v for v in values if v not in text]
    if missing:
        return f"these input values must appear exactly: {json.dumps(missing)}"
    if SQL_WORDS.search(text) or "```" in text:
        return "no SQL: write the request in plain words"
    answer = exercise["answer"]
    if isinstance(answer, str) and len(answer) >= 4 and answer not in values and answer in text:
        return "the request gives away the answer"
    return None


def as_exercise(exercise: dict, task: str) -> dict:
    """The exercise in the format of `a4a run-model`."""
    answer = exercise["answer"]
    number = isinstance(answer, (int, float)) and not isinstance(answer, bool)
    return {"id": exercise["id"], "kind": exercise["database"], "horizon": "short", "task": task.strip(), "answer": answer, "check": {"kind": "number" if number else "exact"},
            "reference_calls": [], "reference_call_count": 1, "library_functions": exercise["uses"], "source_repo": f"{exercise['database']}@{(exercise.get('sha256') or '')[:7]}",
            "reference_code": [exercise["sql"]],
            "provenance": {"file": exercise["file"], "template": exercise["template"], "documented": None,
                           "answer_from": "a query on the database, run twice in the sandbox with the same result"}}


async def write_tasks(exercises: list[dict], what: str, schema: dict, llm) -> tuple[list[dict], Counter]:
    """An exercise per query the LLM could phrase, and why the others were dropped."""

    async def one(exercise: dict) -> tuple[dict | None, str]:
        chat = task_messages(exercise, what, schema)
        problem = "no reply"
        for _ in range(ROUNDS):
            reply = await llm.chat("task", exercise["id"], chat, max_tokens=300)
            try:
                text = extract_json(reply).get("task")
            except (ValueError, AttributeError):
                text = None
            problem = task_problem(text, exercise)
            if problem is None:
                return as_exercise(exercise, text), "written"
            chat = [*chat, {"role": "assistant", "content": reply}, {"role": "user", "content": f"Not usable: {problem}. Write it again."}]
        return None, problem.split(":")[0]

    results = await asyncio.gather(*(one(e) for e in exercises))
    return [exercise for exercise, _ in results if exercise], Counter(outcome for _, outcome in results)


def solver_messages(exercise: dict, what: str, schema: dict) -> list[dict]:
    return [
        {"role": "system", "content": "You write one SQLite query that answers a request. Reply with JSON only."},
        {"role": "user", "content": f"""Request: {exercise['task']}

Database: `{exercise['kind']}` ({what}). Its tables:
{schema_text(schema)}

Write one SQLite query whose result is the answer: one value, or one row for a list.

Reply with one JSON object: {{"sql": "..."}}"""},
    ]


def as_answer(rows):
    """The rows of a query as the answer they stand for: one value, one row as a list, or the rows."""
    if isinstance(rows, list) and len(rows) == 1 and isinstance(rows[0], list):
        return rows[0][0] if len(rows[0]) == 1 else rows[0]
    return rows


async def solvable(exercises: list[dict], what: str, schema: dict, llm, run_items) -> tuple[list[dict], int]:
    """The exercises whose request is enough: a query written from the request and the schema gives the verified answer. Also how many were dropped."""
    replies = await asyncio.gather(*(llm.chat("solve", e["id"], solver_messages(e, what, schema), max_tokens=400) for e in exercises))
    with_query = []
    for exercise, reply in zip(exercises, replies):
        try:
            sql = extract_json(reply).get("sql")
        except (ValueError, AttributeError):
            sql = None
        if isinstance(sql, str) and sql.strip():
            with_query.append((exercise, {"module": None, "steps": STEPS, "expression": f"[list(row) for row in db.execute({sql!r}).fetchmany(50)]"}))
    results = run_items([item for _, item in with_query]) if with_query else []
    kept = [e for (e, _), result in zip(with_query, results or []) if result["status"] == "ok" and check(e, as_answer(result["value"]))]
    return kept, len(exercises) - len(kept)


def report(rows: list[dict]) -> str:
    lines = ["# Exercises in plain words, from database queries", "",
             f"{sum(r['written'] for r in rows):,} exercises from {sum(1 for r in rows if r['written'])} databases. The answer of each is the verified result of a query made from a template; "
             "an LLM wrote only the request. Kept only if a second model, given the request and the schema, wrote a query that gives that answer in the sandbox.", "",
             "| Database | Verified exercises | Chosen | Request written | Solvable from the request (kept) |", "| --- | --- | --- | --- | --- |"]
    lines += [f"| `{r['database']}` | {r['exercises']} | {r['chosen']} | {r['phrased']} | {r['written']} |" for r in rows]
    lines += ["", "## By template", "", "| Template | What it asks | Chosen | Kept |", "| --- | --- | --- | --- |"]
    lines += [f"| {name} | {what} | {sum(r['by_template'].get(name, [0, 0])[0] for r in rows)} | {sum(r['by_template'].get(name, [0, 0])[1] for r in rows)} |" for name, what in TEMPLATES.items()]
    return "\n".join(lines) + "\n"


async def run(args) -> None:
    folder = OUT / "tasks"
    folder.mkdir(parents=True, exist_ok=True)
    llm = LLM(args.base_url, args.model, False, args.concurrency, OUT / "tasks_llm_log.jsonl")
    solver = LLM(args.solver_base_url or args.base_url, args.solver_model, False, args.concurrency, OUT / "tasks_solver_log.jsonl") if args.solver_model else None
    rows = []
    for candidate in json.loads(LIST.read_text(encoding="utf-8"))["databases"]:
        file = OUT / "exercises" / f"{candidate['name']}.jsonl"
        if not file.is_file() or (args.only and candidate["name"] not in args.only):
            continue
        exercises = [json.loads(line) for line in file.read_text(encoding="utf-8").splitlines()]
        chosen = choose(exercises, args.per_database)
        source = SqliteDatabase(candidate, database_path(candidate))
        try:
            schema = source.schema  # read inside the sandbox
            written, outcomes = await write_tasks(chosen, candidate["what"], schema, llm)
            phrased = len(written)
            if solver and written:
                written, unsolved = await solvable(written, candidate["what"], schema, solver, lambda items, source=source: run_drafts(source.box(source.box_name), items))
                outcomes["not solvable from the request"] = unsolved
        finally:
            drop_box(source.box_name)
        target = folder / file.name
        if written:
            target.write_text("".join(json.dumps(e) + "\n" for e in written), encoding="utf-8")
        else:
            target.unlink(missing_ok=True)
        kept = Counter(e["provenance"]["template"] for e in written)
        rows.append({"database": candidate["name"], "exercises": len(exercises), "chosen": len(chosen), "phrased": phrased, "written": len(written),
                     "by_template": {name: [count, kept[name]] for name, count in Counter(e["template"] for e in chosen).items()},
                     "dropped": {k: v for k, v in outcomes.items() if k != "written"}})
        print(f"{candidate['name']}: {len(written)} written of {len(chosen)} chosen {rows[-1]['dropped'] or ''}", flush=True)
    if not args.only:
        (OUT / "tasks.json").write_text(json.dumps({"model": args.model, "solver": args.solver_model, "per_database": args.per_database, "databases": rows}, indent=1) + "\n", encoding="utf-8")
        (OUT / "tasks.md").write_text(report(rows), encoding="utf-8")
    print(f"{sum(r['written'] for r in rows):,} exercises -> out/databases/tasks/")


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("--base-url", required=True)
    parser.add_argument("--model", required=True)
    parser.add_argument("--solver-model", help="a second model that must be able to answer each request with a query; requests it cannot answer are dropped")
    parser.add_argument("--solver-base-url", help="its endpoint, if it is not the same")
    parser.add_argument("--per-database", type=int, default=40)
    parser.add_argument("--only", nargs="+", help="only these databases")
    parser.add_argument("--concurrency", type=int, default=8)
    asyncio.run(run(parser.parse_args()))


if __name__ == "__main__":
    main()
