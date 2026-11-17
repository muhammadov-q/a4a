"""Tests for databases as sources: a small database made here, run in the real sandbox. Needs uv; no network data, no model."""

import hashlib
import sqlite3

from a4a.corpus.exercises import judge
from a4a.databases.exercises import exercises_of, report
from a4a.databases.fetch import checked
from a4a.repo2tools import pipeline
from a4a.sources.base import Source
from a4a.sources.sqlite_database import SqliteDatabase, literal, quoted


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
