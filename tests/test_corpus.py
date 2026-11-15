"""Tests for the candidate list of the many-repo experiments. No network: PyPI's answers are written here."""

import json
import subprocess
from types import SimpleNamespace

import pytest

from repo2tools.corpus.candidates import assess, github_repo, report as candidates_report, select
from repo2tools.corpus.granularity import level_counts, tool_candidates
from repo2tools.corpus.saturation import count_groups, curve, embed, exponent, pairs_report, report as saturation_report, similar_pairs
from repo2tools.corpus.scan import likely_names, report, scan_one
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
    different = [unit(*np.eye(24, dtype=np.float32)[2 * i:2 * i + 2]) for i in range(12)]  # every repository brings two new directions
    result = curve(different, threshold=0.9, orders=3)
    assert result["groups"][-1] == 24 and result["exponent"] == 1.0 and result["new_in_last_tenth"] == 1.0
    assert exponent([1, 2], [1, 2]) is None


def test_pairs_come_from_different_repositories_and_the_report_reads(tmp_path):
    vectors = unit([1, 0], [1, 0.01], [0.7, 0.7], [0, 1])
    pairs = similar_pairs(["a", "b", "c", "d"], ["parse a date", "parse a date again", "format a date", "sort a list"], ["one", "one", "two", "three"], vectors, sample=4)
    flat = [row for rows in pairs.values() for row in rows]
    assert all(row["a"].split("]")[0] != row["b"].split("]")[0] for row in flat) and len(flat) >= 2
    assert not pairs["0.95 to 1.00"]  # the two nearly equal texts are in the same repository
    result = {"model": "m", "repositories": 12, "orders": 3, "curves": {s: {level: {"0.90": curve([unit([1, 0])] * 12, 0.9, 3)} for level in ("low", "medium", "high")} for s in ("all", "used_in_docs")}}
    text = saturation_report(result)
    assert "| low | 0.90 | 12 | 1 | 0.08 | 0.0 | 0% | 1 | 1 | 1 | 1 |" in text and "k=12" in text
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
