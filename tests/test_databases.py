"""Tests for databases as sources: a small database made here, run in the real sandbox. Needs uv; no network data, no model."""

import asyncio
import hashlib
import json
import sqlite3

import pytest

from a4a.corpus.exercises import judge
from a4a.databases import sql_tool, tasks
from a4a.databases.benchmark import databases
from a4a.databases.exercises import exercises_of, report
from a4a.databases.fetch import checked
from a4a.repo2tools import pipeline
from a4a.sources.base import Source
from a4a.sources.sqlite_database import SqliteDatabase, literal, quoted
from helpers import ScriptedLLM


def shop_database(path):
    db = sqlite3.connect(path)
    db.executescript("""
        CREATE TABLE shop (id INTEGER PRIMARY KEY, city TEXT, "open since" INTEGER, parent INTEGER REFERENCES shop(id));
        CREATE TABLE sale (id INTEGER PRIMARY KEY, shop_id INTEGER REFERENCES shop(id), amount REAL, receipt BLOB);
        CREATE TABLE closed (id INTEGER PRIMARY KEY, reason TEXT);
        INSERT INTO shop VALUES (1, 'Bern', 1990, NULL), (2, 'Basel', 2005, 1), (3, 'Bern', 2011, 1);
        INSERT INTO sale VALUES (1, 1, 9.5, x'00'), (2, 1, 20.0, x'01'), (3, 2, 5.25, x'02'), (4, 1, 20.0, x'03'), (5, 3, 1.0, x'04');
    """)
    db.commit()
    db.close()
    return path


def test_a_database_becomes_exercises_whose_answers_come_from_its_queries(tmp_path, monkeypatch):
    monkeypatch.setattr(pipeline, "CACHE", tmp_path / "cache")
    path = shop_database(tmp_path / "shop.sqlite")
    record, exercises = exercises_of({"name": "shop"}, path)
    assert record["error"] is None and record["sha256"] == hashlib.sha256(path.read_bytes()).hexdigest()
    assert (record["tables"], record["columns"]) == (3, 10) and record["parts"]["rows"] == 8 and record["parts"]["schema"] == 3
    assert not (tmp_path / "cache" / "envs" / "examples-shop").exists()  # the environment is deleted afterwards

    by_sql = {e["sql"]: e for e in exercises}
    assert by_sql['SELECT COUNT(*) FROM "sale"']["answer"] == 5 and by_sql['SELECT COUNT(*) FROM "sale"']["uses"] == ["sale"]
    assert by_sql['SELECT COUNT(DISTINCT "city") FROM "shop"']["answer"] == 2
    assert by_sql['SELECT MIN("amount"), MAX("amount") FROM "sale"']["answer"] == [1.0, 20.0]
    assert by_sql['SELECT COUNT(*) FROM "shop" WHERE "city" = \'Bern\'']["answer"] == 2
    assert by_sql['SELECT MIN("open since"), MAX("open since") FROM "shop"']["answer"] == [1990, 2011]  # a name with a space is quoted
    most = {tuple(e["uses"]): e["answer"] for e in exercises if e["template"] == "most"}
    assert most == {("sale", "sale.shop_id", "shop", "shop.id"): [1, 3], ("shop", "shop.id", "shop.parent"): [1, 2]}  # the second is a table that refers to itself
    first = exercises[0]
    assert first["id"] == "shop-001" and first["database"] == "shop" and first["documented"] is None and first["module"] is None
    assert first["steps"] == ["import sqlite3", "db = sqlite3.connect('file:database.sqlite?mode=ro', uri=True)"]  # no path of this computer
    assert {e["sql"] for e in exercises if e["template"] == "range"} == {'SELECT MIN("amount"), MAX("amount") FROM "sale"', 'SELECT MIN("open since"), MAX("open since") FROM "shop"'}  # no range of a key

    # the empty table and its columns cannot be covered; everything else is, also the column of bytes (by counting its values)
    assert record["not_covered"] == ["closed", "closed.id", "closed.reason"] and (record["covered"], record["elements"]) == (10, 13)
    assert record["templates"]["rows"] == [2, 2] and record["templates"]["most"] == [2, 2] and record["outcomes"] == {"verified": len(exercises)}
    text = report([record])
    assert "| `shop` | 3 | 10 | 8 | 3 |" in text and "10 of 13 (77%)" in text and "- `shop`: `closed`, `closed.id`, `closed.reason`" in text


def test_a_file_that_is_not_a_database_is_reported_and_stops_nothing(tmp_path, monkeypatch):
    monkeypatch.setattr(pipeline, "CACHE", tmp_path / "cache")
    path = tmp_path / "notes.sqlite"
    path.write_text("this is not a database\n")
    record, exercises = exercises_of({"name": "notes"}, path)
    assert exercises == [] and record["error"] == "RuntimeError: the file could not be read as a SQLite database"
    assert "| `notes` | RuntimeError: the file could not be read as a SQLite database |" in report([record])


def test_a_database_source_keeps_the_interface_and_writes_safe_sql():
    assert issubclass(SqliteDatabase, Source) and set(SqliteDatabase.PARTS) == {"schema", "rows"}
    assert quoted('odd"name') == '"odd""name"' and literal("O'Hara") == "'O''Hara'" and literal(3) == "3" and literal(2.5) == "2.5"
    assert literal(None) is None and literal(True) is None and literal("x" * 61) is None and literal("two\nlines") is None


def test_a_downloaded_file_is_kept_only_with_the_approved_checksum(tmp_path):
    calls = []

    def fetch(url, target):
        calls.append(url)
        target.parent.mkdir(parents=True, exist_ok=True)
        target.write_bytes(b"data")

    good = hashlib.sha256(b"data").hexdigest()
    file = {"name": "a.db", "url": "https://example.org/a.db", "sha256": good}
    assert checked(file, tmp_path / "ok", False, fetch) == "ok" and checked(file, tmp_path / "ok", False, fetch) == "ok" and calls == ["https://example.org/a.db"]  # fetched once
    wrong = {"name": "a.db", "url": "https://example.org/a.db", "sha256": "0" * 64}
    assert "not the approved one" in checked(wrong, tmp_path / "wrong", False, fetch) and not (tmp_path / "wrong" / "a.db").exists()
    new = {"name": "a.db", "url": "https://example.org/a.db"}
    assert checked(new, tmp_path / "new", False, fetch).startswith("no SHA-256") and "sha256" not in new
    assert checked(new, tmp_path / "new", True, fetch) == "pinned" and new["sha256"] == good


def test_a_draft_without_a_documented_result_is_judged_by_its_two_runs():
    run = {"status": "ok", "value": 5, "text": "5"}
    assert judge({"documented": None}, run, run) == "verified"
    assert judge({"documented": None}, run, {"status": "ok", "value": 6, "text": "6"}) == "not_repeatable"
    assert judge({"documented": "6"}, run, run) == "differs_from_docs" and judge({"documented": "5"}, run, run) == "verified"


SCHEMA = {"lines": 3, "tables": {"shop": {"rows": 3, "keys": [], "columns": {"id": {"type": "INTEGER", "key": True}, "city": {"type": "TEXT", "key": False}}},
                                 "sale": {"rows": 5, "keys": [["shop", "shop_id", "id"]], "columns": {"id": {"type": "INTEGER", "key": True}, "shop_id": {"type": "INTEGER", "key": False}}}}}


def query(name, template, sql, answer, uses):
    return {"id": name, "database": "shop", "sha256": "ab" * 32, "file": "shop.sqlite", "module": None, "template": template, "sql": sql, "answer": answer, "uses": uses}


def test_a_question_about_a_query_keeps_its_values_and_shows_no_sql():
    bern = query("shop-004", "filter", "SELECT COUNT(*) FROM \"shop\" WHERE \"city\" = 'Bern'", 2, ["shop", "shop.city"])
    assert tasks.literals_of(bern["sql"]) == ["Bern"] and tasks.literals_of("SELECT 1 FROM t WHERE a = 'O''Hara' AND b = 2.5") == ["O'Hara", "2.5"]
    assert tasks.literals_of('SELECT COUNT(*) FROM "t2"') == []  # a digit in a name is not an input value
    assert tasks.schema_text(SCHEMA) == "- shop(id INTEGER key, city TEXT): 3 rows\n- sale(id INTEGER key, shop_id INTEGER -> shop.id): 5 rows"
    assert tasks.schema_text(SCHEMA, ["shop"]) == "- shop(id INTEGER key, city TEXT): 3 rows"
    asked = tasks.task_messages(bern, "a shop", SCHEMA)[1]["content"]
    assert "`shop` (a shop)" in asked and "- shop(id INTEGER key, city TEXT): 3 rows" in asked and "sale(" not in asked and '["Bern"]' in asked and "a number" in asked
    good = "In the shop database, how many shops are in the city Bern? Answer with a number."
    assert tasks.task_problem(good, bern) is None
    assert tasks.task_problem("In the shop database, how many shops are in the capital?", bern) == 'these input values must appear exactly: ["Bern"]'
    assert tasks.task_problem("Run SELECT COUNT(*) FROM shop for Bern in the shop database.", bern) == "no SQL: write the request in plain words"
    made = tasks.as_exercise(bern, good)
    assert made["check"] == {"kind": "number"} and made["kind"] == "shop" and made["reference_code"] == [bern["sql"]] and made["source_repo"] == "shop@abababa"
    assert made["provenance"]["answer_from"].startswith("a query on the database") and tasks.as_exercise(query("x", "range", "q", [1, 9], []), good)["check"] == {"kind": "exact"}
    many = [query(f"shop-{i:03d}", template, "q", i, []) for i, template in enumerate(["distinct"] * 6 + ["rows"] * 2 + ["most"])]
    assert [e["template"] for e in tasks.choose(many, 5)].count("distinct") == 2 and len(tasks.choose(many, 50)) == 9  # in turn from each template


def test_a_question_is_kept_only_if_a_query_written_from_it_gives_the_answer():
    bern = tasks.as_exercise(query("shop-004", "filter", "q", 2, ["shop"]), "In the shop database, how many shops are in the city Bern? Answer with a number.")
    pair = tasks.as_exercise(query("shop-005", "range", "q", [1, 9], ["sale"]), "In the shop database, what are the smallest and the largest sale id? Answer with a JSON list.")
    lost = tasks.as_exercise(query("shop-006", "rows", "q", 5, ["sale"]), "In the shop database, how many sales are there? Answer with a number.")
    llm = ScriptedLLM({("solve", "shop-004"): ['{"sql": "SELECT COUNT(*) FROM shop WHERE city = \'Bern\'"}'], ("solve", "shop-005"): ['{"sql": "SELECT MIN(id), MAX(id) FROM sale"}'],
                       ("solve", "shop-006"): ["I do not know."]})
    seen = []

    def run_items(items):
        seen.extend(items)
        return [{"status": "ok", "value": [[2]]}, {"status": "ok", "value": [[1, 9]]}][:len(items)]

    kept, dropped = asyncio.run(tasks.solvable([bern, pair, lost], "a shop", SCHEMA, llm, run_items))
    assert [e["id"] for e in kept] == ["shop-004", "shop-005"] and dropped == 1 and len(seen) == 2  # a reply without a query is not run
    assert "fetchmany(50)" in seen[0]["expression"] and seen[0]["steps"][0] == "import sqlite3"
    assert "sale(id INTEGER key, shop_id INTEGER -> shop.id)" in llm.chats[0][2][1]["content"]  # the solver sees the whole schema
    assert tasks.as_answer([[7]]) == 7 and tasks.as_answer([[1, 9]]) == [1, 9] and tasks.as_answer([[1], [2]]) == [[1], [2]] and tasks.as_answer([]) == []
    text = tasks.report([{"database": "shop", "exercises": 20, "chosen": 3, "phrased": 3, "written": 2, "by_template": {"filter": [1, 1], "range": [1, 1], "rows": [1, 0]}}])
    assert "| `shop` | 20 | 3 | 3 | 2 |" in text and "| rows | the number of rows of a table | 1 | 0 |" in text


def test_the_sql_tool_reads_and_cannot_write(tmp_path):
    path = shop_database(tmp_path / "shop.sqlite")
    assert json.loads(sql_tool.rows_of(str(path), "SELECT city, COUNT(*) FROM shop GROUP BY city ORDER BY city")) == [["Basel", 1], ["Bern", 2]]
    assert json.loads(sql_tool.rows_of(str(path), "SELECT receipt FROM sale WHERE id = 2")) == [["01"]]  # bytes are shown as hex text
    with pytest.raises(RuntimeError, match="readonly"):
        sql_tool.rows_of(str(path), "DELETE FROM sale")
    with pytest.raises(RuntimeError, match="no such table"):
        sql_tool.rows_of(str(path), "SELECT * FROM missing_table")
    assert sqlite3.connect(path).execute("SELECT COUNT(*) FROM sale").fetchone()[0] == 5


def test_a_long_reply_of_the_sql_tool_is_cut_and_a_slow_query_is_stopped(tmp_path, monkeypatch):
    path = shop_database(tmp_path / "shop.sqlite")
    monkeypatch.setattr(sql_tool, "MAX_ROWS", 3)
    text = sql_tool.rows_of(str(path), "SELECT id FROM sale ORDER BY id")
    assert text.startswith("[[1], [2], [3]]") and text.endswith("[only the first 3 rows are shown]")
    monkeypatch.setattr(sql_tool, "SECONDS", 0)
    with pytest.raises(RuntimeError, match="did not finish in time"):
        sql_tool.rows_of(str(path), "WITH RECURSIVE n(i) AS (SELECT 1 UNION ALL SELECT i + 1 FROM n WHERE i < 5000000) SELECT COUNT(*) FROM n")


def test_the_database_benchmark_takes_approved_databases_with_enough_questions(tmp_path, monkeypatch):
    from a4a.databases import benchmark

    listed = tmp_path / "candidates.json"
    listed.write_text(json.dumps({"databases": [{"name": "shop", "what": "a shop", "repo": "https://example.org/shop", "database": "shop.sqlite", "files": []},
                                                {"name": "empty", "what": "nothing", "repo": "https://example.org/empty", "database": "e.sqlite", "files": []}]}))
    (tmp_path / "tasks").mkdir()
    (tmp_path / "tasks" / "shop.jsonl").write_text("{}\n" * 6)
    (tmp_path / "tasks" / "empty.jsonl").write_text("{}\n" * 2)
    monkeypatch.setattr(benchmark, "LIST", listed)
    monkeypatch.setattr(benchmark, "OUT", tmp_path)
    found = databases(5)
    assert [(d["stem"], d["tasks"], d["url"]) for d in found] == [("shop", 6, "https://example.org/shop")] and found[0]["candidate"]["what"] == "a shop"
    assert benchmark.run_tag("db1", "shop", "sql") == "db1-shop-sql-repair" and benchmark.run_file("m", "sql", "db1", "shop").name == "m-tools-db1-shop-sql-repair.jsonl"
