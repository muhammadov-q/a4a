"""Tests for the memory check: database variants, library questions with changed inputs, and the comparison. Real sandbox, no model."""

import json
import sqlite3

from a4a.corpus import benchmark
from a4a.corpus.scan import scan_one
from a4a.corpus.variant import bumped, changed_code, changed_text, changes_of, drafts_for, variant_of
from a4a.databases import tasks as db_tasks
from a4a.databases.exercises import exercises_of
from a4a.databases.variant import plain, recomputed, shrink
from a4a.evaluation.memory import compare, original_question, report
from a4a.repo2tools import pipeline
from a4a.sources.base import run_drafts
from a4a.sources.python_repository import box_for, drop_box
from a4a.sources.sqlite_database import SqliteDatabase
from test_corpus import SHAPES, SHAPES_DOCS, git_repo
from test_databases import shop_database


def test_a_database_variant_keeps_the_schema_and_changes_the_answers(tmp_path, monkeypatch):
    monkeypatch.setattr(pipeline, "CACHE", tmp_path / "cache")
    path = shop_database(tmp_path / "shop.sqlite")
    _, exercises = exercises_of({"name": "shop"}, path)
    questions = [db_tasks.as_exercise(e, f"A question about {e['sql']} in the shop database.") for e in exercises]
    target = tmp_path / "variant-1.sqlite"
    shrink(path, target, 1, 0.5)
    shrink(path, tmp_path / "again.sqlite", 1, 0.5)
    rows = lambda p, t: sqlite3.connect(p).execute(f"SELECT COUNT(*) FROM {t}").fetchone()[0]  # noqa: E731
    assert (rows(path, "sale"), rows(path, "shop")) == (5, 3)  # the original is not touched
    assert rows(target, "sale") < 5 and (rows(target, "sale"), rows(target, "shop")) == (rows(tmp_path / "again.sqlite", "sale"), rows(tmp_path / "again.sqlite", "shop"))  # the same seed, the same rows
    assert sqlite3.connect(target).execute("SELECT sql FROM sqlite_master WHERE name = 'sale'").fetchone() == sqlite3.connect(path).execute("SELECT sql FROM sqlite_master WHERE name = 'sale'").fetchone()

    source = SqliteDatabase({"name": "shop-v1"}, target)
    try:
        kept, outcomes = recomputed(questions, source)
    finally:
        drop_box(source.box_name)
    assert sum(outcomes.values()) == len(questions) and outcomes["changed"] >= 1
    sale_rows = next(q for q in kept if q["reference_code"] == ['SELECT COUNT(*) FROM "sale"'])
    assert sale_rows["answer"] == rows(target, "sale") and sale_rows["changed"] and sale_rows["provenance"]["original_answer"] == 5
    assert sale_rows["task"] == next(q for q in questions if q["id"] == sale_rows["id"])["task"]  # the wording stays
    assert all(plain(q["answer"]) for q in kept) and not plain(None) and not plain([None, 3]) and not plain([])


def test_input_values_are_changed_in_the_code_and_in_the_wording():
    assert bumped("1.0.2") == "1.0.3" and bumped("2003-09-25") == "2003-09-26" and bumped("x9") == "x8" and bumped("7") == "8" and bumped("abc") == "abc"
    assert bumped("1e-05") == "1e-06" and bumped("-3") == "-4" and bumped("v1.2rc1 or later") == "v1.2rc2 or later"
    assert changes_of(["2", "abc", "1.5", "v10"]) == {"2": "3", "1.5": "1.6", "v10": "v11"}
    steps, expression = changed_code(["from shapes import parse", "s = parse('2')"], "s.area * 2", {"2": "3"})
    assert steps == ["from shapes import parse", "s = parse('3')"] and expression == "s.area * 3"  # the text '2' and the number 2 both change
    assert changed_text("Read the square from the text '2', double it, and compare with 12 or 2.5.", {"2": "3", "2.5": "2.6"}) == \
        "Read the square from the text '3', double it, and compare with 12 or 2.6."  # 12 is another number
    assert changed_text("Nothing to change.", {}) == "Nothing to change."


def test_a_library_question_with_changed_inputs_gets_its_answer_from_a_new_run(tmp_path, monkeypatch):
    monkeypatch.setattr(pipeline, "CACHE", tmp_path / "cache")
    repo = git_repo(tmp_path / "me" / "shapes", {"shapes/__init__.py": SHAPES, "README.rst": SHAPES_DOCS, "pyproject.toml": '[project]\nname = "shapes"\n'})
    static = scan_one({"package": "shapes", "repo": str(repo)}, clones=tmp_path / "clones", scans=tmp_path / "scans")
    base = {"kind": "shapes", "check": {"kind": "number"}, "provenance": {"file": "README.rst"}}
    questions = [base | {"id": "s-1", "task": "With shapes, find the area of the square read from the text '3'.", "answer": 9.0, "reference_code": ["from shapes import parse", "parse('3').area"]},
                 base | {"id": "s-2", "task": "With shapes, how many corners has a square?", "answer": 4, "reference_code": ["from shapes import Square", "Square('x').corners"]},
                 base | {"id": "s-3", "task": "With shapes, give the corners of the square read from '5'.", "answer": 4, "reference_code": ["from shapes import parse", "parse('5').corners"]},
                 base | {"id": "s-4", "task": "Not a known example.", "answer": 1, "reference_code": ["1"]}]
    examples = {q["id"]: {"id": q["id"], "module": None, "steps": q["reference_code"][:-1], "expression": q["reference_code"][-1]} for q in questions[:3]}
    found, outcomes = drafts_for(questions, examples)
    assert [q["id"] for q, _, _ in found] == ["s-1", "s-3"] and outcomes == {"no_digits": 1, "no_example": 1}
    try:
        box = box_for(static, "variant-test", tmp_path / "clones")
        results = run_drafts(box, [draft for _, draft, _ in found])
    finally:
        drop_box("variant-test")
    area, corners = (variant_of(q, draft, changes, result["value"]) for (q, draft, changes), result in zip(found, results))
    assert area["task"] == "With shapes, find the area of the square read from the text '4'." and area["answer"] == 16.0 and area["changed"]
    assert area["provenance"]["original_answer"] == 9.0 and area["provenance"]["changed_inputs"] == {"3": "4"} and area["reference_code"] == ["from shapes import parse", "parse('4').area"]
    assert corners["answer"] == 4 and not corners["changed"]  # the input changed, the answer did not
    assert variant_of(questions[0] | {"task": "The text is not in this wording."}, found[0][1], found[0][2], 16.0) is None


def test_the_memory_check_counts_old_answers_on_changed_questions(tmp_path, monkeypatch):
    monkeypatch.setattr(benchmark, "REPO_ROOT", tmp_path)
    runs = tmp_path / "out" / "runs"
    runs.mkdir(parents=True)
    question = lambda i, answer, old, changed: {"id": i, "answer": answer, "check": {"kind": "number"}, "changed": changed, "provenance": {"original_answer": old}}  # noqa: E731
    questions = {"shop": [question("q1", 3, 5, True), question("q2", 7, 9, True), question("q3", 4, 4, False)]}

    def save(tag, condition, records):
        path = benchmark.run_file("m", condition, tag, "shop")
        path.write_text("".join(json.dumps(r) + "\n" for r in records))

    save("db1", "none", [{"id": "q1", "passed": True, "answer": 5}, {"id": "q2", "passed": True, "answer": 9}, {"id": "q3", "passed": False, "answer": 1}])
    save("db1v1", "none", [{"id": "q1", "passed": False, "answer": 5}, {"id": "q2", "passed": True, "answer": 7}, {"id": "q3", "passed": True, "answer": 4}])
    save("db1", "sql", [{"id": "q1", "passed": True, "answer": 5}, {"id": "q2", "passed": True, "answer": 9}, {"id": "q3", "passed": True, "answer": 4}])
    save("db1v1", "sql", [{"id": "q1", "passed": True, "answer": 3}, {"id": "q2", "passed": True, "answer": 7.0}, {"id": "q3", "passed": True, "answer": 4}])
    result = compare(questions, "m", "db1", "db1v1", ["none", "sql"])
    none, sql = result["none"]["total"], result["sql"]["total"]
    assert (none["changed"], none["right_before"], none["right_after"], none["old_answer"], none["only_before"], none["only_after"]) == (2, 2, 1, 1, 1, 0)
    assert (none["same"], none["same_right_before"], none["same_right_after"]) == (1, 0, 1)
    assert (sql["right_after"], sql["old_answer"]) == (2, 0)
    assert original_question({"check": {"kind": "set_equal"}, "provenance": {"original_answer": ["a"]}}) == {"answer": ["a"], "check": {"kind": "set_equal"}}
    assert compare(questions, "m", "db1", "missing", ["none"])["none"]["missing"] == ["shop"]
    text = report(result, "m", "db1", "db1v1", "tasks-v1")
    assert "| No tools | 2 | 2 (100%) | 1 (50%) | 1 (50%) | 1 | 0 | 1 |" in text and "| One SQL tool | 2 | 2 (100%) | 2 (100%) | 0 (0%) |" in text
