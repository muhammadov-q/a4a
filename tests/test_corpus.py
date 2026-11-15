"""Tests for the candidate list of the many-repo experiments. No network: PyPI's answers are written here."""

import asyncio
import json
import shutil
import subprocess
from pathlib import Path
from types import SimpleNamespace

import pytest

from helpers import ScriptedLLM
from repo2tools.corpus import benchmark, python_tool
from repo2tools.corpus.candidates import assess, github_repo, report as candidates_report, select
from repo2tools.corpus.exercises import drafts_of, examples_of, exercises_for, names_of, report as exercises_report, setup_for
from repo2tools.corpus.granularity import level_counts, tool_candidates
from repo2tools.corpus.saturation import count_groups, curve, embed, exponent, pairs_report, report as saturation_report, similar_pairs
from repo2tools.corpus.scan import likely_names, report, scan_one
from repo2tools.corpus.tasks import answer_form, as_exercise, as_item, choose, literals_of, reference_of, report as tasks_report, solvable, task_problem, write_tasks
from repo2tools.evaluation.exercise_check import check as exercise_check
from repo2tools.synthesis import pipeline
from repo2tools.synthesis.scrape import public_api


def meta(wheels=("x-1.0-py3-none-any.whl",), sdist_mb=0.1, links=None, **info):
    files = [{"packagetype": "bdist_wheel", "filename": w, "size": 1000} for w in wheels]
    files.append({"packagetype": "sdist", "filename": "x-1.0.tar.gz", "size": int(sdist_mb * 1e6)})
    return {"info": {"version": "1.0", "summary": "A thing.", "project_urls": links if links is not None else {"Source": "https://github.com/me/x"}, **info}, "urls": files}


def test_a_pure_python_package_with_a_repository_is_a_candidate():
    row = assess("x", meta(license_expression="MIT", requires_dist=["a>=1", "b; extra == 'dev'"]))
    assert row["reason"] is None and row["repo"] == "https://github.com/me/x" and row["license"] == "MIT" and row["dependencies"] == 1


def test_reasons_to_leave_a_package_out():
    assert assess("types-x", meta())["reason"] == "stubs" and assess("x-stubs", meta())["reason"] == "stubs"
    assert assess("x", meta(wheels=()))["reason"] == "no wheel"
    assert assess("x", meta(wheels=("x-1.0-cp312-cp312-manylinux_2_17_x86_64.whl", "x-1.0-py3-none-any.whl")))["reason"] == "native"
    assert assess("x", meta(sdist_mb=9))["reason"] == "too large"
    assert assess("x", meta(links={"Docs": "https://x.readthedocs.io"}))["reason"] == "no repo"


def test_the_repository_is_read_from_the_links():
    assert github_repo({"project_urls": {"Homepage": "https://x.org", "Source Code": "https://github.com/me/x.git"}}) == "https://github.com/me/x"
    assert github_repo({"project_urls": {"Changelog": "https://github.com/me/x/blob/main/HISTORY.md"}}) == "https://github.com/me/x"
    assert github_repo({"project_urls": {"Funding": "https://github.com/sponsors/me"}, "home_page": "https://github.com/me/x"}) == "https://github.com/me/x"
    assert github_repo({"project_urls": None, "home_page": "https://gitlab.com/me/x"}) is None
    assert assess("x", meta(license="BSD\nlong text", classifiers=[]))["license"] == "BSD"
    assert assess("x", meta())["license"] == "not stated"


def test_one_candidate_per_repository_in_download_order():
    rows = [{"rank": i, **assess(name, meta(links={"Source": f"https://github.com/me/{repo}"}))}
            for i, (name, repo) in enumerate([("a", "mono"), ("b", "Mono"), ("c", "other"), ("d", "third")], 1)]
    chosen = select(rows, 2)
    assert [r["package"] for r in chosen] == ["a", "c"]
    assert [r["reason"] for r in rows] == [None, "same repo", None, "beyond the number asked for"]
    text = candidates_report(chosen, rows, {"list_updated": "2026-11-01", "read_on": "2026-11-13"})
    assert "2 pure-Python packages" in text and "| 2 | 3 | `c` 1.0 | https://github.com/me/other |" in text and "1 same repo" in text


# --- the static pass --------------------------------------------------------------------------

SHAPES = '''"""Shapes with an area."""


class Square:
    """A square with a side length, built from text such as "3"."""

    def __init__(self, text: str):
        self.side = float(text)

    @property
    def area(self) -> float:
        """The area."""
        return self.side ** 2

    @property
    def corners(self) -> int:
        """Always 4."""
        return 4

    def scaled(self, factor: float) -> "Square":
        """A square with the side multiplied by factor."""
        return Square(str(self.side * factor))

    def __lt__(self, other: "Square") -> bool:
        return self.side < other.side

    def __eq__(self, other) -> bool:
        return self.side == other.side


def parse(text: str) -> Square:
    """Read a square from text."""
    return Square(text)


def unused(text: str) -> str:
    """Nobody calls this."""
    return text
'''
SHAPES_DOCS = """Shapes
======

>>> from shapes import Square, parse
>>> small = parse("2")
>>> small.area
4.0
>>> small < Square("3")
True

One use only::

    from shapes import parse
    parse("5")
"""


def git_repo(path, files):
    for name, text in files.items():
        (path / name).parent.mkdir(parents=True, exist_ok=True)
        (path / name).write_text(text)
    git = ["git", "-c", "user.email=t@example.com", "-c", "user.name=t", "-C", str(path)]
    for command in (["init", "--quiet"], ["add", "."], ["commit", "--quiet", "-m", "init"]):
        subprocess.run([*git, *command], check=True)
    return path


def test_the_static_pass_counts_a_package_without_running_it(tmp_path):
    marker = tmp_path / "ran"
    repo = git_repo(tmp_path / "me" / "shapes", {
        "shapes/__init__.py": SHAPES, "README.rst": SHAPES_DOCS, "pyproject.toml": '[project]\nname = "shapes"\n',
        "tests/test_shapes.py": f"from shapes import Square\nopen({str(marker)!r}, 'w').write('x')\n\ndef test_eq():\n    assert Square('1') == Square('1')\n"})
    record = scan_one({"package": "shapes", "repo": str(repo)}, clones=tmp_path / "clones", scans=tmp_path / "scans")
    assert record["error"] is None and len(record["commit"]) == 40 and not marker.exists()
    assert record["import_name"] == "shapes" and record["layout"] == "top level"
    assert record["files"] == {"python": 1, "lines": 26, "tests": 1, "docs": 1}
    assert record["api"]["callables"] == 5 and record["api"]["classes"] == 1 and record["api"]["property"] == 2
    # low: parse, unused, Square.area, Square.corners, Square.scaled; the docs use parse and area
    # medium: parse, unused, and for Square: build it, read its properties, scaled, and the comparisons (one family)
    # high: one example uses two or more things (parse, Square(), area, <); the other uses only parse
    assert record["levels"] == {"low": 5, "low_used_in_docs": 2, "medium": 6, "medium_used_in_docs": 4, "high": 1, "examples": 2, "examples_with_two_or_more": 1}
    saved = json.loads((tmp_path / "scans" / "me__shapes" / "usage.json").read_text())
    assert saved["examples"][0]["uses"] == ["Square <", "Square()", "shapes.Square.area", "shapes.parse"] and "small.area" in saved["examples"][0]["code"]
    api = json.loads((tmp_path / "scans" / "me__shapes" / "api.json").read_text())
    texts = {c["id"]: (c["level"], c["text"], c["used_in_docs"]) for c in tool_candidates(api, saved)}
    assert texts["shapes.Square#build"] == ("medium", "Square(text: str): build a Square. A square with a side length, built from text such as \"3\".", True)
    assert texts["shapes.Square#properties"] == ("medium", "Square: read its properties: area, corners", True)
    assert texts["shapes.Square#compare"] == ("medium", "Square: compare two of them (smaller, equal, greater)", True)
    assert texts["shapes.Square.scaled"][1] == "Square.scaled(factor: float) -> 'Square': A square with the side multiplied by factor." and not texts["shapes.Square.scaled"][2]
    high = [c for c in tool_candidates(api, saved) if c["level"] == "high"]
    assert len(high) == 1 and high[0]["text"].startswith("Example that uses Square <, Square(), Square.area, parse:\nfrom shapes import Square, parse")
    text = report([record])
    assert "1 of 1 repositories scanned" in text and "| `shapes` |" in text and "| low | one function, method or property | 5 | 5 | 2 (40%) |" in text


def test_a_one_file_library_and_a_repository_without_a_package(tmp_path):
    single = git_repo(tmp_path / "me" / "python-tiny", {"tiny.py": 'def twice(text: str) -> str:\n    """Repeat."""\n    return text * 2\n'})
    record = scan_one({"package": "tiny", "repo": str(single)}, clones=tmp_path / "clones")
    assert record["error"] is None and record["layout"] == "top level, one file" and record["api"]["function"] == 1 and record["levels"]["low"] == 1
    empty = git_repo(tmp_path / "me" / "notes", {"README.md": "Nothing here.\n"})
    record = scan_one({"package": "notes", "repo": str(empty)}, clones=tmp_path / "clones")
    assert record["commit"] and "no Python package" in record["error"] and str(tmp_path) not in record["error"]
    assert "## Not scanned" in report([record])


def test_names_to_try_and_operator_families():
    assert likely_names({"package": "python-dateutil", "repo": "https://github.com/dateutil/dateutil"}) == ["python_dateutil", "dateutil", "thon_dateutil"]
    assert likely_names({"package": "pyjwt", "repo": "https://github.com/jpadilla/pyjwt"})[:2] == ["pyjwt", "jwt"]
    api = {"callables": [{"module": "m", "qualname": "Box.size", "kind": "property"}], "classes": {"Box": {}}}
    usage = {"callables": {"m.Box.size": {"docs": 0, "guessed_docs": 0}}, "examples": [{"uses": u, "code": "x"} for u in (["a"], ["a", "b"], ["a", "b"])],
             "classes": {"Box": {"built": {"docs": 1}, "operators": {"<": {"docs": 0}, ">=": {"docs": 2}, "in": {"docs": 0}, "&": {"docs": 0}}}}}
    found = level_counts(api, usage)
    assert found["medium"] == 5  # build, properties, compare, contains, &
    assert found["medium_used_in_docs"] == 2 and found["high"] == 1 and found["examples_with_two_or_more"] == 2


# --- the public API, with re-exports followed ---------------------------------------------------


def write(root, files):
    for name, text in files.items():
        (root / name).parent.mkdir(parents=True, exist_ok=True)
        (root / name).write_text(text)
    return root


def paths(callables):
    return sorted(f"{c.module}.{c.qualname}" for c in callables)


def test_re_exports_are_followed_to_the_definition(tmp_path):
    root = write(tmp_path, {
        "lib/__init__.py": "from ._core import Thing, make as build\nfrom .extra import *\nfrom . import tools\nimport os\nfrom os.path import join\n",
        "lib/_core/__init__.py": "from ._impl import Thing, make\n",
        "lib/_core/_impl.py": "class Thing:\n    def size(self) -> int:\n        return 1\n\n    def _hidden(self):\n        pass\n\n\ndef make(text: str) -> Thing:\n    return Thing()\n\n\ndef not_exported():\n    pass\n",
        "lib/extra.py": "__all__ = ['listed']\n\n\ndef listed():\n    pass\n\n\ndef unlisted():\n    pass\n",
        "lib/tools.py": "def helper():\n    pass\n\n\ndef _private():\n    pass\n",
        "lib/tests/test_x.py": "def test_x():\n    pass\n"})
    found = public_api(root, "lib")
    # under the shortest module that offers it, once each; `make` under its public name; nothing from outside the package
    assert paths(found) == ["lib.Thing.size", "lib.build", "lib.listed", "lib.tools.helper"]
    assert next(c for c in found if c.qualname == "build").file == "lib/_core/_impl.py"


def test_names_defined_under_a_condition_and_plain_all_lists(tmp_path):
    root = write(tmp_path, {
        "one.py": "import sys\n__all__ = ('new', 'Old')\nif sys.version_info >= (3, 99):\n    def new():\n        pass\nelse:\n    def new():\n        pass\ntry:\n    from typing import Old\nexcept ImportError:\n    class Old:\n        def m(self):\n            pass\n\n\ndef left_out():\n    pass\n",
        "typed/__init__.py": "from typing import TYPE_CHECKING\nif TYPE_CHECKING:\n    from .main import Model\n",
        "typed/main.py": "class Model:\n    def dump(self) -> dict:\n        return {}\n"})
    assert paths(public_api(root, "one")) == ["one.Old.m", "one.new"]
    assert paths(public_api(root, "typed")) == ["typed.Model.dump"]


def test_a_thin_public_package_over_a_private_one(tmp_path):
    root = write(tmp_path, {
        "nice/__init__.py": "from _nice.core import run\nfrom _nice import Config\n__all__ = ['run', 'Config']\n",
        "_nice/__init__.py": "from .core import Config\n",
        "_nice/core.py": "class Config:\n    def get(self, key: str) -> str:\n        return key\n\n\ndef run() -> int:\n    return 0\n"})
    assert paths(public_api(root, "nice")) == ["nice.Config.get", "nice.run"]
    assert public_api(root, "missing") == []


# --- saturation ------------------------------------------------------------------------------

np = pytest.importorskip("numpy")  # in the `analysis` group


def unit(*rows):
    vectors = np.asarray(rows, dtype=np.float32)
    return vectors / np.linalg.norm(vectors, axis=1, keepdims=True)


def test_a_candidate_joins_the_group_of_a_similar_earlier_one():
    first = unit([1, 0, 0], [0, 1, 0])
    second = unit([0.99, 0.1, 0], [0, 0, 1], [0, 0.05, 1])  # like the first of `first`; new; like the one before it
    third = np.zeros((0, 3), dtype=np.float32)  # a repository with nothing at this level
    assert count_groups([first, second, third], threshold=0.9) == [2, 3, 3]
    assert count_groups([first, second, third], threshold=0.9999) == [2, 5, 5]
    assert count_groups([second, first], threshold=0.9) == [2, 3]


def test_the_exponent_tells_repetition_from_growth():
    same = [unit([1, 0, 0], [0, 1, 0])] * 12  # every repository repeats the first
    result = curve(same, threshold=0.9, orders=3)
    assert result["groups"] == [2.0] * 12 and result["candidates"][-1] == 24 and result["exponent"] == 0.0 and result["new_in_last_tenth"] == 0.0
    assert result["distinct_within_repositories"] == 24 and result["seen_before_second_tenth"] == 1.0 and result["seen_before_last_tenth"] == 1.0
    different = [unit(*np.eye(24, dtype=np.float32)[2 * i:2 * i + 2]) for i in range(12)]  # every repository brings two new directions
    result = curve(different, threshold=0.9, orders=3)
    assert result["groups"][-1] == 24 and result["exponent"] == 1.0 and result["new_in_last_tenth"] == 1.0
    assert result["seen_before_last_tenth"] == 0.0
    inside = curve([unit([1, 0], [1, 0.001], [0, 1])] * 2 + [unit([0.6, 0.8])] * 10, threshold=0.9, orders=2)  # repetition inside a repository is kept apart
    assert inside["candidates"][-1] == 16 and inside["distinct_within_repositories"] == 14 and inside["groups"][-1] == 3
    assert exponent([1, 2], [1, 2]) is None


def test_pairs_come_from_different_repositories_and_the_report_reads(tmp_path):
    vectors = unit([1, 0], [1, 0.01], [0.7, 0.7], [0, 1])
    pairs = similar_pairs(["a", "b", "c", "d"], ["parse a date", "parse a date again", "format a date", "sort a list"], ["one", "one", "two", "three"], vectors, sample=4)
    flat = [row for rows in pairs.values() for row in rows]
    assert all(row["a"].split("]")[0] != row["b"].split("]")[0] for row in flat) and len(flat) >= 2
    assert not pairs["0.95 to 1.00"]  # the two nearly equal texts are in the same repository
    result = {"model": "m", "repositories": 12, "orders": 3, "curves": {s: {level: {"0.90": curve([unit([1, 0])] * 12, 0.9, 3)} for level in ("low", "medium", "high")} for s in ("all", "used_in_docs")}}
    text = saturation_report(result)
    assert "| low | 0.90 | 12 | 12 | 1 | 0.0 | 100% | 100% | 1 | 1 | 1 | 1 |" in text and "k=12" in text
    assert "## low" in pairs_report({"low": pairs})


def test_vectors_are_cut_and_made_unit_length():
    class Client:
        class embeddings:  # noqa: N801
            @staticmethod
            def create(model, input):  # noqa: A002
                data = [SimpleNamespace(index=i, embedding=[3.0, 4.0] + [0.0] * 2000) for i, _ in enumerate(input)]
                return SimpleNamespace(data=list(reversed(data)))

    vectors = embed(["a", "b", "c"], Client, "m", batch=2)
    assert vectors.shape == (3, 1024) and np.allclose(np.linalg.norm(vectors, axis=1), 1) and np.allclose(vectors[0, :2], [0.6, 0.8])


# --- exercises from documentation examples -----------------------------------------------------

EXAMPLES = """Shapes
======

>>> from shapes import Square, parse
>>> small = parse("2")
>>> small.area
4.0
>>> small.corners
4
>>> small
<a square>
>>> small.area + 1
6.0

Prose in between does not matter: `small` and `parse` are still known on this page.

>>> small.corners
4
>>> import random
>>> random.random()
0.5
>>> print(parse("3").area)
9.0
>>> sides = [parse("1").corners]
>>> sides.append("x")
>>> sides
[4, 'x']
>>> parse("x")
Traceback (most recent call last):
ValueError: no
"""


def test_an_example_becomes_a_draft_with_the_lines_it_needs():
    drafts = drafts_of(examples_of(EXAMPLES))
    by_expression = {d["expression"]: d for d in drafts}
    assert list(by_expression) == ["small.area", "small.corners", "small", "small.area + 1", "random.random()", "parse('3').area", "sides"]  # statements are setup, not questions
    assert by_expression["small.area"] == {"steps": ["from shapes import Square, parse", 'small = parse("2")'], "expression": "small.area", "printed": False, "documented": "4.0"}
    assert by_expression["small.area + 1"]["steps"] == by_expression["small.area"]["steps"]  # lines that only showed a value are not setup
    assert by_expression["random.random()"]["steps"] == ["import random"]
    assert by_expression["parse('3').area"] == {"steps": ["from shapes import Square, parse"], "expression": "parse('3').area", "printed": True, "documented": "9.0"}
    assert by_expression["sides"]["steps"] == ["from shapes import Square, parse", 'sides = [parse("1").corners]', 'sides.append("x")']  # a call that changes it is setup
    assert setup_for(["a = 1", "b = a + 1", "c = 5", "print(b)", "d = {}", "d['k'] = b"], "d") == ["a = 1", "b = a + 1", "d = {}", "d['k'] = b"]
    assert examples_of("no examples here") == [] and names_of("not python (") == (set(), set(), set())
    assert setup_for(["from shapes import *", "import os", "x = 1"], "parse('1')") == ["from shapes import *"]
    # a method call on a new object changes nothing that a later line reads
    assert setup_for(['Square("1").scaled(2)', 'big = Square("9")', "big.scaled(2)", "items = []", "items.append(big)"], 'Square("3").area') == []
    assert setup_for(["items = []", 'Square("1").scaled(2)', "items.append(1)"], "items") == ["items = []", "items.append(1)"]


def test_only_examples_that_run_and_match_the_documentation_are_kept(tmp_path, monkeypatch):
    monkeypatch.setattr(pipeline, "CACHE", tmp_path / "cache")
    outside = Path.home() / ".repo2tools-example-test"
    assert not outside.exists()
    hostile = f"\nAn example that tries to write outside the scratch folder:\n\n>>> open({str(outside)!r}, 'w').write('x')\n1\n"
    docstring = '"""Shapes with an area.\n\n>>> parse("4").area\n16.0\n"""\n'
    repo = git_repo(tmp_path / "me" / "shapes", {"shapes/__init__.py": SHAPES.replace('"""Shapes with an area."""\n', docstring), "README.rst": EXAMPLES + hostile,
                                                 "pyproject.toml": '[project]\nname = "shapes"\n'})
    candidate = {"package": "shapes", "repo": str(repo)}
    scanned = scan_one(candidate, clones=tmp_path / "clones", scans=tmp_path / "scans")
    record, verified = exercises_for(candidate | {"commit": scanned["commit"]}, clones=tmp_path / "clones", scans=tmp_path / "scans")
    assert record["error"] is None and record["drafts"] == 9
    expected = {"verified": 5, "not_json": 1, "differs_from_docs": 1, "not_repeatable": 1, "error": 1}
    if shutil.which("sandbox-exec") is None:  # without the sandbox the write works and gives the documented 1
        expected = {"verified": 6, "not_json": 1, "differs_from_docs": 1, "not_repeatable": 1}
    assert record["outcomes"] == expected
    assert shutil.which("sandbox-exec") is None or not outside.exists()
    outside.unlink(missing_ok=True)
    by_expression = {e["expression"]: e for e in verified}
    assert by_expression["small.area"]["answer"] == 4.0 and by_expression["small.area"]["steps"] == ["from shapes import Square, parse", 'small = parse("2")']
    assert by_expression["small.area"]["uses"] == ["shapes.Square.area", "shapes.parse"] and by_expression["small.area"]["commit"] == scanned["commit"]
    assert by_expression["parse('3').area"]["answer"] == 9.0 and by_expression["sides"]["answer"] == [4, "x"]  # printed in the documentation; built in three lines
    assert by_expression['parse("4").area']["module"] == "shapes" and by_expression['parse("4").area']["steps"] == []  # a docstring example sees its module's names
    assert [e["id"] for e in verified] == [f"me__shapes-{i:03d}" for i in range(1, len(verified) + 1)]
    assert not (tmp_path / "cache" / "envs" / "examples-me__shapes").exists()  # the environment is deleted afterwards
    text = exercises_report([record])
    assert f"9 examples in their documentation show a value; {len(verified)} of them are verified" in text and f"| `shapes` | 9 | {len(verified)} |" in text
    assert record["errors"] == ({"PermissionError": 1} if shutil.which("sandbox-exec") else {})


def test_standard_types_get_one_plain_form():
    import datetime
    import decimal

    from repo2tools.corpus.example_worker import plain

    kinds: set = set()
    value = {"when": datetime.datetime(2003, 9, 25, 10, 36), "span": datetime.timedelta(minutes=2), "price": decimal.Decimal("1.50"), "tags": {"b", "a"}, "pair": (1, 2.5)}
    assert plain(value, kinds) == {"when": "2003-09-25T10:36:00", "span": 120.0, "price": "1.50", "tags": ["a", "b"], "pair": [1, 2.5]}
    assert kinds == {"datetime", "timedelta", "Decimal", "set"}
    for not_plain in (object(), float("nan"), {1: "a"}, {1, "a"}):
        with pytest.raises(TypeError):
            plain(not_plain, set())


# --- questions in plain words ------------------------------------------------------------------


def example(n, uses, steps=("from shapes import parse",), expression='parse("2").area', answer=4.0, kinds=()):
    return {"id": f"me__shapes-{n:03d}", "repo": "https://github.com/me/shapes", "commit": "abcdef1234", "package": "shapes", "file": "README.rst", "module": None,
            "steps": list(steps), "expression": expression, "answer": answer, "answer_kinds": list(kinds), "documented": "4.0", "uses": uses}


def test_examples_are_chosen_across_the_number_of_uses():
    pool = [example(i, ["a"]) for i in range(1, 7)] + [example(7, ["a", "b"]), example(8, ["a", "b", "c"]), example(9, []), example(10, ["a"], answer=None),
                                                         example(11, ["a"], expression='parse("' + "x" * 200 + '")')]
    chosen = choose(pool, per_repo=4)
    assert len(chosen) == 4 and {len(e["uses"]) for e in chosen} == {1, 2, 3}  # one, two and three uses each take a turn; no uses, no answer and a huge input are left out
    assert all(e["id"] not in ("me__shapes-009", "me__shapes-010", "me__shapes-011") for e in choose(pool, per_repo=20)) and len(choose(pool, per_repo=20)) == 8
    assert literals_of('x = parse("2", scale=1.5)\nx.area') == ["2", "1.5"]
    own_class = example(12, ["a"], steps=("class Mine:\n    pass",), expression="Mine()")
    with_lambda = example(13, ["a"], expression='parse("2").scaled(lambda x: x)')
    assert choose([own_class, with_lambda], per_repo=5) == []  # code written for the example cannot be said in plain words


def test_a_request_must_carry_the_inputs_and_hide_the_code_and_the_answer():
    e = example(1, ["shapes.parse", "shapes.Square.area"])
    assert task_problem("What is the area of the square with side 2? Answer with a number.", e) is None
    assert "must appear exactly" in task_problem("What is the area of the square? Answer with a number.", e)
    assert "no code" in task_problem("What does parse(2) give for the area? Answer with a number.", e)
    named = example(2, ["shapes.name"], expression='name("2")', answer="square")
    assert "gives away" in task_problem("What kind of shape has side 2? It is a square. Answer with a text.", named)
    assert task_problem(None, e) == 'reply with {"task": "..."}'
    assert answer_form(e) == "a number" and answer_form(example(3, ["a"], answer=True)) == "true or false"
    assert answer_form(example(4, ["a"], answer="2003-09-25", kinds=["date"])) == "a date as ISO 8601 text, like 2003-09-25"
    assert answer_form(example(5, ["a"], answer=["a", "b"], kinds=["set"])) == "a JSON list in sorted order"


def test_tasks_are_written_repaired_or_dropped_and_the_answer_stays_the_verified_one():
    good = json.dumps({"task": "What is the area of the square with side 2? Answer with a number."})
    llm = ScriptedLLM({("task", "me__shapes-001"): [good],
                       ("task", "me__shapes-002"): [json.dumps({"task": "What is the area of the square? Answer with a number."}), good],
                       ("task", "me__shapes-003"): ["not json"]})
    written, outcomes = asyncio.run(write_tasks([example(1, ["shapes.parse"]), example(2, ["shapes.parse", "shapes.Square.area"]), example(3, ["shapes.parse"])], llm))
    assert [e["id"] for e in written] == ["me__shapes-001", "me__shapes-002"] and outcomes == {"written": 2, 'reply with {"task"': 1}
    first = written[0]
    assert first["answer"] == 4.0 and first["check"] == {"kind": "number"} and first["kind"] == "shapes" and first["horizon"] == "short"
    assert first["source_repo"] == "me/shapes@abcdef1" and first["reference_code"] == ["from shapes import parse", 'parse("2").area'] and first["reference_calls"] == []
    assert written[1]["reference_call_count"] == 2 and written[1]["library_functions"] == ["shapes.parse", "shapes.Square.area"]
    assert "Not usable: these input values must appear exactly" in llm.chats[2][2][-1]["content"]  # the reason goes back to the writer
    assert "Answer: 4.0" in llm.chats[0][2][1]["content"] and 'character for character: ["2"]' in llm.chats[0][2][1]["content"]
    assert as_exercise(example(6, ["a"], answer=["b", "a"], kinds=["set"]), "t")["check"] == {"kind": "set_equal"}
    assert as_exercise(example(7, ["a"], answer=True), "t")["check"] == {"kind": "exact"}
    text = tasks_report([{"package": "shapes", "usable": 3, "chosen": 3, "written": 2, "by_tools": {1: 1, 2: 1}, "dropped": {}}])
    assert "2 exercises from 1 repositories" in text and "1: 1, 2: 1" in text and "| `shapes` | 3 | 3 | 2 | 2 |" in text


def test_a_number_answer_may_be_written_with_or_without_a_point():
    number = {"answer": 4.0, "check": {"kind": "number"}}
    assert exercise_check(number, 4) and exercise_check(number, 4.0) and not exercise_check(number, 4.1) and not exercise_check(number, "4") and not exercise_check(number, True)
    assert not exercise_check({"answer": 1, "check": {"kind": "number"}}, True) and exercise_check({"answer": 0.1 + 0.2, "check": {"kind": "number"}}, 0.3)


def test_a_request_is_kept_only_if_code_written_from_it_gives_the_answer():
    api = {"callables": [{"module": "shapes", "qualname": "parse", "kind": "function", "params": [{"name": "text"}], "docstring": "Read a square from text.", "summary": ""},
                         {"module": "shapes", "qualname": "Square.area", "kind": "property", "params": [], "docstring": "The area.", "summary": ""}],
           "classes": {"Square": {"module": "shapes", "params": [{"name": "text"}], "summary": "A square."}}}
    reference = reference_of(["shapes.parse", "shapes.Square.area", "Square()", "Square <", "unknown.thing"], api)
    assert reference.splitlines() == ["- shapes.parse(text) [function]: Read a square from text.", "- shapes.Square.area [property]: The area.",
                                      "- shapes.Square(text) [class]: A square.", "- objects of shapes.Square can be used with the operator `<`"]
    assert as_item("from shapes import parse\nsmall = parse('2')\nsmall.area") == {"module": None, "steps": ["from shapes import parse", "small = parse('2')"],
                                                                                    "expression": "small.area", "printed": False}
    assert as_item("x = 1") is None and as_item("not python (") is None and as_item(None) is None
    exercises = [as_exercise(example(n, ["shapes.parse", "shapes.Square.area"]), f"What is the area of the square with side 2? Question {n}.") for n in (1, 2, 3, 4)]
    llm = ScriptedLLM({("solve", "me__shapes-001"): [json.dumps({"code": "from shapes import parse\nparse('2').area"})],
                       ("solve", "me__shapes-002"): [json.dumps({"code": "from shapes import parse\nparse('3').area"})],  # runs, but gives another value
                       ("solve", "me__shapes-003"): [json.dumps({"code": "x = 1"})],  # no expression at the end
                       ("solve", "me__shapes-004"): ["no json"]})
    ran = []

    def run_items(items):
        ran.extend(items)
        return [{"status": "ok", "value": 4.0 if "'2'" in item["expression"] else 9.0, "text": ""} for item in items]

    kept, dropped = asyncio.run(solvable(exercises, api, llm, run_items))
    assert [e["id"] for e in kept] == ["me__shapes-001"] and dropped == 3 and len(ran) == 2  # only code with an expression is run
    prompt = llm.chats[0][2][1]["content"]
    assert "Request: What is the area of the square with side 2? Question 1." in prompt and "- shapes.parse(text) [function]" in prompt and "4.0" not in prompt  # the solver never sees the answer


def test_the_benchmark_report_is_built_from_the_saved_runs(tmp_path, monkeypatch):
    monkeypatch.setattr(benchmark, "REPO_ROOT", tmp_path)
    monkeypatch.setattr(benchmark, "OUT", tmp_path / "out" / "corpus")
    (tmp_path / "out" / "corpus" / "tasks").mkdir(parents=True)
    (tmp_path / "out" / "runs").mkdir()
    task = as_exercise(example(1, ["shapes.parse"]), "What is the area of the square with side 2?")
    (tmp_path / "out" / "corpus" / "tasks" / "me__shapes.jsonl").write_text((json.dumps(task) + "\n") * 3)
    (tmp_path / "out" / "corpus" / "tasks" / "me__small.jsonl").write_text(json.dumps(task) + "\n")  # too few questions
    repos = benchmark.repositories(min_tasks=2)
    assert [(r["stem"], r["package"], r["url"], r["tasks"]) for r in repos] == [("me__shapes", "shapes", "https://github.com/me/shapes", 3)]
    (tmp_path / "out" / "generated" / "shapes-t1").mkdir(parents=True)
    (tmp_path / "out" / "generated" / "shapes-t1" / "report.json").write_text(json.dumps({"tools": [{}, {}], "accepted": 1}))

    def save(condition, run, records):
        benchmark.run_file("m", condition, "t1", "me__shapes", run).write_text("".join(json.dumps(r) + "\n" for r in records))

    assert [benchmark.run_file("m", c, "t1", "me__shapes", k).name for c, k in (("none", 1), ("tools", 2), ("python", 1), ("python", 3))] == [
        "m-none-t1-me__shapes.jsonl", "m-tools-t1-me__shapes-r2.jsonl", "m-tools-t1-me__shapes-python.jsonl", "m-tools-t1-me__shapes-python-r3.jsonl"]
    save("none", 1, [{"passed": p} for p in (True, True, False)])
    save("none", 2, [{"passed": p} for p in (True, False, False)])
    save("none", 4, [{"passed": True}] * 3)  # run 3 is missing, so this one is not counted
    for run in (1, 2):
        save("tools", run, [{"passed": True, "tool_calls": 2, "tool_errors": 1}, {"passed": False, "tool_calls": 1, "tool_errors": 0}, {"passed": False, "tool_calls": 0, "tool_errors": 0}])
        save("python", run, [{"passed": True, "tool_calls": 1, "tool_errors": 0}] * 3)
    rows = benchmark.summarize(repos, "m", "t1")
    assert rows == [{"package": "shapes", "repo": "https://github.com/me/shapes", "questions": 3, "tools_picked": 2, "tools_accepted": 1,
                     "right": {"none": [2, 1], "tools": [1, 1], "python": [3, 3]},
                     "use": {"tools": {"called_a_tool": [2, 2], "right_when_called": [1, 1], "tool_calls": [3, 3], "tool_errors": [1, 1]},
                             "python": {"called_a_tool": [3, 3], "right_when_called": [3, 3], "tool_calls": [3, 3], "tool_errors": [0, 0]}}}]
    text = benchmark.report(rows, "m", "t1")
    assert "1 repositories with every condition, 3 questions, 2 runs each. Right answers: no tools 1.5 (50%) (2, 1); generated tools 1.0 (33%) (1, 1); one python tool 3.0 (100%) (3, 3)." in text
    assert "| `shapes` | 3 | 1 of 2 | 1.5 (2, 1) | 1.0 (1, 1) | 3.0 (3, 3) |" in text and "| `shapes` | generated tools | 2.0 of 3 | 1.0 | 3.0 | 1.0 |" in text
    missing = benchmark.summarize(repos, "m", "missing")
    assert missing[0]["right"] == {"none": [], "tools": [], "python": []} and "0 repositories with every condition" in benchmark.report(missing, "m", "missing")
    assert benchmark.cell([4]) == "4" and benchmark.cell([4], 8) == "4 (50%)" and benchmark.cell([]) == "none"


def test_the_python_tool_runs_code_like_a_notebook_cell_and_keeps_nothing():
    run = lambda code: asyncio.run(python_tool.run_python(code))  # noqa: E731
    assert run("import json\nprint('a')\nx = [1, 2]\njson.dumps(x * 2)") == "a\n'[1, 2, 1, 2]'"  # what was printed, then the last line's value
    assert run("x = 1") == "" and run("print(5)") == "5"  # no value: nothing; None is not shown
    with pytest.raises(RuntimeError, match=r"NameError: name 'x' is not defined \(line 1 of the code\)"):
        run("x")  # the x of the call before is gone
    with pytest.raises(RuntimeError, match=r"shown\nZeroDivisionError: division by zero \(line 2 of the code\)"):
        run("print('shown')\n1 / 0")
    with pytest.raises(RuntimeError, match="SyntaxError"):
        run("not python (")
    with pytest.raises(RuntimeError, match="SystemExit: 3"):
        run("import sys\nsys.exit(3)")
    assert run("open('note.txt', 'w').write('hi')\nopen('note.txt').read()") == "'hi'"
    with pytest.raises(RuntimeError, match="FileNotFoundError"):
        run("open('note.txt').read()")  # every call has its own empty folder


def test_a_call_of_the_python_tool_that_does_not_end_is_stopped(monkeypatch):
    monkeypatch.setattr(python_tool, "SECONDS", 1)
    with pytest.raises(RuntimeError, match="did not finish in 1 seconds"):
        asyncio.run(python_tool.run_python("while True:\n    pass"))
