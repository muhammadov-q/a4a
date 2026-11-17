"""A SQLite database as a source: exercises are queries over its tables, and the answer is what the query gives.

A database file is someone else's data, so it is never opened in our own process. The box gets a copy named
`database.sqlite` in its scratch folder, and everything, also reading the schema, happens there with the
standard library's `sqlite3`, read-only.

Drafts are made from templates over the schema, without a model:

    rows       how many rows a table has
    distinct   how many different values a column has
    range      the smallest and the largest value of a column
    filter     how many rows have a column's most frequent value
    most       along a foreign key: which parent row has the most child rows

Every draft names the tables and columns it uses, so what the exercises cover is known when they are made,
and can be chosen. There is no documented result to compare with: an exercise is a draft whose two runs give
the same plain value, and its answer comes from the query alone.
"""

import shutil
from pathlib import Path

from a4a.repo2tools import pipeline
from a4a.sources.base import EXAMPLE_WORKER, Source, run_drafts

DATABASE = "database.sqlite"  # the name of the copy in the box; the steps of every exercise open it by this name
STEPS = ["import sqlite3", f"db = sqlite3.connect('file:{DATABASE}?mode=ro', uri=True)"]
MAX_VALUE = 60  # a longer text value is not used in a filter
TEMPLATES = {"rows": "the number of rows of a table", "distinct": "the number of different values of a column", "range": "the smallest and the largest value of a column",
             "filter": "the number of rows with a column's most frequent value", "most": "along a foreign key, the parent row with the most child rows"}


def quoted(name: str) -> str:
    """A table or column name as SQL."""
    return '"' + name.replace('"', '""') + '"'


def literal(value) -> str | None:
    """A value as SQL, or None for a value that should not be written into a query."""
    if isinstance(value, bool) or value is None:
        return None
    if isinstance(value, (int, float)):
        return repr(value)
    if isinstance(value, str) and len(value) <= MAX_VALUE and value.isprintable():
        return "'" + value.replace("'", "''") + "'"
    return None


def probe(expression: str) -> dict:
    return {"module": None, "steps": STEPS, "expression": expression}


def one_value(sql: str) -> str:
    return f"db.execute({sql!r}).fetchone()[0]"


def one_row(sql: str) -> str:
    return f"list(db.execute({sql!r}).fetchone())"


class SqliteDatabase(Source):
    """One database file. `candidate` is its record from the approved list: `name`, and where the file came from."""

    kind = "SQLite database"
    PARTS = {"schema": "Schema", "rows": "Rows"}

    def __init__(self, candidate: dict, path: Path):
        self.candidate, self.path = candidate, path
        self.name = candidate["name"]
        self._box = None
        self._schema: dict | None = None

    def box(self, set_name: str, readable: Path = EXAMPLE_WORKER):
        if self._box is None:
            self._box = pipeline.make_box(set_name, None, None, [], readable)
            shutil.copy2(self.path, self._box.scratch / DATABASE)
        return self._box

    def ask(self, expressions: list[str]) -> list:
        """The value of each expression, run in the box; None where it failed or is not plain JSON."""
        if not expressions:
            return []
        results = run_drafts(self.box(self.box_name), [probe(e) for e in expressions])
        if results is None:
            raise RuntimeError("the sandboxed run did not finish")
        return [r["value"] if r["status"] == "ok" else None for r in results]

    @property
    def schema(self) -> dict:
        """Tables with their columns, foreign keys and row counts, and for each column what the templates need. Read once, in the box."""
        if self._schema is None:
            tables, lines = self.ask(["[r[0] for r in db.execute(\"SELECT name FROM sqlite_master WHERE type = 'table' AND name NOT LIKE 'sqlite_%' ORDER BY name\")]",
                                      "sum(len([line for line in (r[0] or '').splitlines() if line.strip()]) for r in db.execute('SELECT sql FROM sqlite_master'))"])
            if tables is None:
                raise RuntimeError("the file could not be read as a SQLite database")
            facts = self.ask([e for t in tables for e in (f"[[r[1], r[2], r[5]] for r in db.execute('PRAGMA table_info({quoted(t)})')]",
                                                          f"[[r[2], r[3], r[4]] for r in db.execute('PRAGMA foreign_key_list({quoted(t)})')]",
                                                          one_value(f"SELECT COUNT(*) FROM {quoted(t)}"))])
            schema = {"lines": lines or 0, "tables": {}}
            for i, table in enumerate(tables):
                columns, keys, rows = facts[3 * i:3 * i + 3]
                schema["tables"][table] = {"rows": rows or 0, "keys": keys or [], "columns": {name: {"type": kind or "", "key": bool(key)} for name, kind, key in columns or []}}
            wanted = [(t, c) for t, table in schema["tables"].items() if table["rows"] for c in table["columns"]]
            numbers = self.ask([e for t, c in wanted for e in (
                one_row(f"SELECT COUNT(DISTINCT {quoted(c)}), typeof(MAX({quoted(c)})) FROM {quoted(t)}"),
                one_row(f"SELECT {quoted(c)}, COUNT(*) FROM {quoted(t)} WHERE {quoted(c)} IS NOT NULL GROUP BY {quoted(c)} ORDER BY COUNT(*) DESC, {quoted(c)} LIMIT 1"))])
            for i, (t, c) in enumerate(wanted):
                counted, frequent = numbers[2 * i:2 * i + 2]
                schema["tables"][t]["columns"][c] |= {"distinct": counted[0] if counted else None, "stored_as": counted[1] if counted else None,
                                                      "frequent": frequent[0] if frequent else None, "frequent_rows": frequent[1] if frequent else None}
            self._schema = schema
        return self._schema

    def parts(self) -> dict[str, int]:
        return {"schema": self.schema["lines"], "rows": sum(t["rows"] for t in self.schema["tables"].values())}

    def part_of(self, item: dict) -> str:
        return "rows"

    def elements(self) -> set[str]:
        return {name for t, table in self.schema["tables"].items() for name in (t, *(f"{t}.{c}" for c in table["columns"]))}

    def drafts(self) -> list[dict]:
        found = []

        def add(template: str, sql: str, expression: str, uses: list[str]) -> None:
            found.append({"module": None, "file": self.path.name, "steps": STEPS, "expression": expression, "documented": None, "template": template, "sql": sql, "uses": sorted(set(uses))})

        for t, table in self.schema["tables"].items():
            if not table["rows"]:
                continue
            add("rows", sql := f"SELECT COUNT(*) FROM {quoted(t)}", one_value(sql), [t])
            references = {column for _, column, _ in table["keys"]}  # a key is a name for a row, not a quantity
            for c, column in table["columns"].items():
                if column.get("distinct") is None:
                    continue
                add("distinct", sql := f"SELECT COUNT(DISTINCT {quoted(c)}) FROM {quoted(t)}", one_value(sql), [t, f"{t}.{c}"])
                if column["stored_as"] in ("integer", "real") and column["distinct"] > 1 and not column["key"] and c not in references:
                    add("range", sql := f"SELECT MIN({quoted(c)}), MAX({quoted(c)}) FROM {quoted(t)}", one_row(sql), [t, f"{t}.{c}"])
                value = literal(column["frequent"])
                if value is not None and 1 < column["distinct"] < table["rows"]:
                    add("filter", sql := f"SELECT COUNT(*) FROM {quoted(t)} WHERE {quoted(c)} = {value}", one_value(sql), [t, f"{t}.{c}"])
            for parent, column, target in table["keys"]:
                if parent not in self.schema["tables"] or column not in table["columns"]:
                    continue
                target = target or next((c for c, facts in self.schema["tables"][parent]["columns"].items() if facts["key"]), None)
                if target is None:
                    continue
                key = f"parent.{quoted(target)}"  # the two tables get names of their own: a table may refer to itself
                sql = (f"SELECT {key}, COUNT(*) FROM {quoted(t)} AS child JOIN {quoted(parent)} AS parent ON child.{quoted(column)} = {key} "
                       f"GROUP BY {key} ORDER BY COUNT(*) DESC, {key} LIMIT 1")
                add("most", sql, one_row(sql), [t, f"{t}.{column}", parent, f"{parent}.{target}"])
        return found

    def uses(self, draft: dict) -> list[str]:
        return draft["uses"]

    def origin(self, draft: dict) -> dict:
        return {"database": self.name, "sha256": self.candidate.get("sha256"), "file": draft["file"], "module": None, "template": draft["template"], "sql": draft["sql"]}
