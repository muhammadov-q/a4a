"""Tests for the public benchmarks: small stand-ins made here, run in the real sandbox. Needs uv; no download, no model."""

import gzip
import json
import sqlite3
import zipfile

import pytest

from a4a.downstream import fetch, humaneval, report, spider, spider_tasks
from a4a.evaluation.exercise_check import check, rows_match
from a4a.repo2tools import pipeline
from a4a.training import data


def test_an_answer_gives_the_rows_of_the_query_in_any_reasonable_shape():
    assert rows_match(6, [[6]], False) and rows_match("6", [[6]], False) and rows_match(6.0, [[6]], False)
    assert rows_match(["a", "b"], [["b"], ["a"]], False) and not rows_match(["a", "b"], [["b"], ["a"]], True)
    assert rows_match([["a", "b"]], [["b"], ["a"]], False) and rows_match([["a", "b"]], [["a", "b"]], False)  # one column wrapped once more, or one row
    assert rows_match(["Bern", 3], [["Bern", 3]], False)  # one row as a flat list
    assert rows_match([[3, "Bern"], [1, "Basel"]], [["Bern", 3], ["Basel", 1]], True)  # columns in another order
    assert rows_match([{"city": "Bern", "n": 3}], [["Bern", 3]], False)  # rows as objects
    assert rows_match(31.50004, [[31.5]], False) and not rows_match(31.6, [[31.5]], False)
    assert rows_match([], [], False) and rows_match(None, [], False) and rows_match(None, [[None]], False)
    assert not rows_match([["a"], ["a"]], [["a"]], False)  # a row twice is not the same result
    assert not rows_match([[1, 2]], [[1, 2, 3]], False)
    assert check({"answer": [[2]], "check": {"kind": "rows"}}, 2)


def test_only_an_order_by_outside_every_bracket_orders_the_result():
    assert spider_tasks.ordered("SELECT name FROM singer ORDER BY age DESC")
    assert not spider_tasks.ordered("SELECT name FROM singer WHERE age = (SELECT age FROM singer ORDER BY age LIMIT 1)")
    assert not spider_tasks.ordered("SELECT name FROM singer WHERE note = 'order by me'")


def spider_zip(path, names=("shop",), dev_name="dev.json"):
    with zipfile.ZipFile(path, "w") as zipped:
        questions = [{"db_id": names[0], "question": "How many shops are there?", "query": "SELECT count(*) FROM shop"},
                     {"db_id": names[0], "question": "List the cities.", "query": "SELECT city FROM shop"},
                     {"db_id": names[0], "question": "List all ids.", "query": "SELECT id FROM shop ORDER BY id"}]
        zipped.writestr(f"spider_data/{dev_name}", json.dumps(questions))
        for name in names:
            database = path.parent / f"{name}.sqlite"
            db = sqlite3.connect(database)
            db.executescript("CREATE TABLE shop (id INTEGER PRIMARY KEY, city TEXT); INSERT INTO shop VALUES (1, 'Bern'), (2, 'Basel'), (3, 'Bern');")
            db.commit()
            db.close()
            zipped.write(database, f"spider_data/database/{name}/{name}.sqlite")
    return path


def test_only_the_dev_set_is_taken_out_of_the_zip_and_names_must_be_plain(tmp_path):
    found = fetch.extract_spider(spider_zip(tmp_path / "spider.zip"), tmp_path / "dev")
    assert found["questions"] == 3 and found["databases"] == 1
    assert sorted(p.name for p in (tmp_path / "dev" / "database").iterdir()) == ["shop.sqlite"]
    (tmp_path / "bad").mkdir()
    with pytest.raises(RuntimeError, match="not plain names"):
        fetch.extract_spider(spider_zip(tmp_path / "bad" / "spider.zip", names=("shop; DROP",)), tmp_path / "dev2")
    assert not (tmp_path / "dev2" / "dev.json").exists()


def test_spider_questions_get_their_answers_from_the_gold_query_in_the_sandbox(tmp_path, monkeypatch):
    monkeypatch.setattr(pipeline, "CACHE", tmp_path / "cache")
    fetch.extract_spider(spider_zip(tmp_path / "spider.zip"), tmp_path / "dev")
    summary = spider_tasks.build(tmp_path / "dev", tmp_path / "out", max_rows=2, zip_sha256="abc1234567")
    assert summary["dropped"] == {"more than 2 rows": 2} and summary["databases"]["shop"]["kept"] == 1
    kept = [json.loads(line) for line in (tmp_path / "out" / "tasks" / "shop.jsonl").read_text().splitlines()]
    assert kept[0]["id"] == "shop-0000" and kept[0]["answer"] == [[3]] and kept[0]["check"] == {"kind": "rows", "ordered": False}
    assert "`shop`" in kept[0]["task"] and kept[0]["source_repo"] == "spider-dev@abc1234"
    assert not list((tmp_path / "cache" / "envs").glob("examples-spider-shop-*"))  # the sandbox is deleted afterwards
    found = spider.databases(tmp_path / "out" / "tasks", tmp_path / "dev")
    assert found == [{"stem": "shop", "path": tmp_path / "out" / "tasks" / "shop.jsonl", "tasks": 1, "file": tmp_path / "dev" / "database" / "shop.sqlite"}]


def test_spider_runs_never_become_training_data():
    match = data.RUN.match("qwen3-32b-tools-spider1-concert_singer-sql-repair.jsonl.gz")
    parser_default = ["bench2", "aimed1", "db1"]
    assert match["set"] == spider.TAG and spider.TAG not in parser_default


PROBLEM = {"task_id": "HumanEval/0", "entry_point": "add", "prompt": "import math\n\n\ndef helper(x):\n    return x\n\n\ndef add(a, b):\n    \"\"\"Add two numbers.\"\"\"\n",
           "test": "def check(candidate):\n    assert candidate(1, 2) == 3\n    assert helper(4) == 4\n", "canonical_solution": "    return a + b\n"}


def test_a_humaneval_reply_is_read_as_a_function_or_as_a_body():
    whole = humaneval.code_of("Here it is:\n```python\ndef add(a, b):\n    return a + b\n\nif __name__ == '__main__':\n    print(add(input(), 1))\n```\nDone.")
    assert "input" not in whole and whole.startswith("def add(")
    program = humaneval.program(PROBLEM, whole)
    assert program.count("def add(") == 1 and "def helper(x)" in program and program.endswith("check(add)\n")
    assert humaneval.program(PROBLEM, "    return a + b\n").startswith(PROBLEM["prompt"])


def test_humaneval_programs_run_in_the_sandbox_with_a_time_limit(tmp_path, monkeypatch):
    monkeypatch.setattr(pipeline, "CACHE", tmp_path / "cache")
    programs = [humaneval.program(PROBLEM, "    return a + b\n"), humaneval.program(PROBLEM, "    return a - b\n"),
                humaneval.program(PROBLEM, "    while True:\n        pass\n"), humaneval.program(PROBLEM, "    return open('/etc/hosts', 'w')\n")]
    ran = humaneval.run_programs(programs, "humaneval-test", seconds=3)
    assert [r["status"] for r in ran] == ["passed", "failed", "timeout", "error"]
    assert not (tmp_path / "cache" / "envs" / "humaneval-test").exists()


def test_humaneval_problems_are_read_from_the_pinned_file(tmp_path):
    path = tmp_path / "HumanEval.jsonl.gz"
    with gzip.open(path, "wt") as file:
        file.write(json.dumps(PROBLEM) + "\n")
    assert humaneval.problems(path) == [PROBLEM]


def test_each_trained_student_is_compared_with_its_untrained_base():
    found = {"spider": {"qwen3-4b": {"a": True, "b": False, "c": False}, "qwen3-4b-rec4-f2": {"a": True, "b": True, "c": True}, "qwen3-8b": {"a": True, "b": True, "c": False}},
             "humaneval": {"qwen3-4b": {"h": True}}}
    table = {r["model"]: r for r in report.rows(found)}
    trained = table["qwen3-4b-rec4-f2"]
    assert (trained["base"], trained["recipe"], trained["fold"]) == ("qwen3-4b", "rec4", "f2")
    assert trained["spider"] == {"right": 3, "questions": 3, "against_base": {"only_base": 0, "only_model": 2, "p": 0.5}}
    assert "against_base" not in table["qwen3-8b"]["spider"] and "humaneval" not in trained
    text = report.report(list(table.values()))
    assert "| `qwen3-4b-rec4-f2` | 3 of 3 (100%) | 0 / 2, p = 0.5 | not run |  |" in text and "| `qwen3-4b` | rec4 | 1 |" in text
