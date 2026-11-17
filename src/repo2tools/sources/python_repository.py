"""A Python repository as a source: the doctest examples in its documentation files and in the docstrings of its package.

It reads a clone made by `repo2tools corpus-scan` (.cache/corpus/<owner>__<name>) and the saved scan of its
public API. Reading runs nothing. Running a draft happens only in the box: the library's own environment
under the sandbox of `repo2tools generate` (no network, the home folder unreadable, one scratch folder writable).
"""

import ast
import doctest
import json
import shutil
import subprocess
import warnings
from functools import cached_property
from pathlib import Path

import httpx

from repo2tools.corpus.scan import CLONES, folder_name, likely_names, locate
from repo2tools.sources.base import Source
from repo2tools.synthesis import pipeline
from repo2tools.synthesis.pipeline import native_code, project_metadata
from repo2tools.synthesis.usage import DOC_SUFFIXES, SKIP_DIRS, Api, Usage, absolute_imports, is_test_file

EXAMPLE_WORKER = Path(__file__).resolve().parents[1] / "corpus" / "example_worker.py"
MAX_STEPS, MAX_CODE, MAX_EXPRESSION, MAX_DRAFTS = 12, 1500, 300, 400


def filled(text: str) -> int:
    return sum(1 for line in text.splitlines() if line.strip())


def text_lines(root: Path, package_dir: Path) -> dict:
    """Lines of documentation files outside the package, and of docstrings inside it: the same files `corpus-exercises` reads."""
    counts = {"files": 0, "docstrings": 0}
    root, package_dir = root.resolve(), package_dir.resolve()
    for path in root.rglob("*"):
        if path.is_symlink() or not path.is_file() or SKIP_DIRS & set(path.relative_to(root).parts):
            continue
        inside = package_dir in path.parents or path == package_dir
        if path.suffix == ".py" and inside:
            try:
                with warnings.catch_warnings():
                    warnings.simplefilter("ignore", SyntaxWarning)  # old escape sequences in other people's code
                    tree = ast.parse(path.read_text(encoding="utf-8", errors="replace"))
            except (SyntaxError, ValueError):
                continue
            counts["docstrings"] += sum(filled(ast.get_docstring(node) or "") for node in ast.walk(tree)
                                        if isinstance(node, (ast.Module, ast.ClassDef, ast.FunctionDef, ast.AsyncFunctionDef)))
        elif path.suffix.lower() in DOC_SUFFIXES and not inside and not is_test_file(path, root):
            counts["files"] += filled(path.read_text(encoding="utf-8", errors="replace"))
    return counts


def examples_of(text: str) -> list[doctest.Example]:
    """The doctest examples of a text, in order."""
    try:
        return doctest.DocTestParser().get_examples(text)
    except ValueError:  # a prompt that doctest itself cannot read
        return []


def names_of(source: str) -> tuple[set[str], set[str], set[str]]:
    """(names a piece of code binds, names it changes through a call or an item or attribute assignment, names it reads)."""
    try:
        tree = ast.parse(source)
    except (SyntaxError, ValueError):
        return set(), set(), set()

    def root(node) -> str | None:
        """The name an attribute or item chain hangs on: `d` in `d.items[0].x`. A call in the chain (`Thing(1).method()`) makes a new object, so it has none."""
        while isinstance(node, (ast.Attribute, ast.Subscript)):
            node = node.value
        return node.id if isinstance(node, ast.Name) else None

    binds, changes, reads = set(), set(), set()
    for node in ast.walk(tree):
        if isinstance(node, ast.Name):
            (binds if isinstance(node.ctx, ast.Store) else reads).add(node.id)
        elif isinstance(node, (ast.Import, ast.ImportFrom)):
            binds |= {(alias.asname or alias.name).split(".")[0] for alias in node.names}
        elif isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef, ast.ClassDef)):
            binds.add(node.name)
        elif isinstance(node, (ast.Attribute, ast.Subscript)) and isinstance(node.ctx, ast.Store) and root(node):
            changes.add(root(node))
    for statement in tree.body:  # `items.append(3)` changes items
        if isinstance(statement, ast.Expr) and isinstance(statement.value, ast.Call) and isinstance(statement.value.func, ast.Attribute) and root(statement.value.func):
            changes.add(root(statement.value.func))
    return binds, changes, reads


def setup_for(earlier: list[str], expression: str) -> list[str]:
    """The earlier lines of the same text that the expression needs, in order: those that bind or change a name it reads, and what they need in turn.

    Documentation shows values between the lines that matter (`v1`, `v1 < v2`), and imports once at the top of
    a page. Following the names keeps the setup of an exercise short and complete.
    """
    needed = names_of(expression)[2]
    chosen = []
    for source in reversed(earlier):
        binds, changes, reads = names_of(source)
        if (binds | changes) & needed or "*" in binds:  # `from x import *` may bind any name, so it always stays
            chosen.append(source)
            needed |= reads
    return chosen[::-1]


def drafts_of(examples: list[doctest.Example]) -> list[dict]:
    """One draft per example that shows a value: {"steps", "expression", "printed", "documented"}."""
    out = []
    for i, example in enumerate(examples):
        documented, source = example.want.strip(), example.source.strip()
        if not documented or "Traceback (most recent call last)" in documented or "..." in documented or len(source) > MAX_EXPRESSION:
            continue
        try:
            node = ast.parse(source, mode="eval").body
        except (SyntaxError, ValueError):
            continue  # a statement, not an expression
        printed = isinstance(node, ast.Call) and isinstance(node.func, ast.Name) and node.func.id == "print" and len(node.args) == 1 and not node.keywords
        expression = ast.unparse(node.args[0]) if printed else source
        steps = setup_for([e.source.rstrip("\n") for e in examples[:i]], expression)
        if len(steps) > MAX_STEPS or sum(map(len, steps)) > MAX_CODE:
            continue
        out.append({"steps": steps, "expression": expression, "printed": printed, "documented": documented})
    return out


def collect(root: Path, package_dir: Path, package: str) -> list[dict]:
    """Every draft of a checkout, with where it comes from. Docstring examples carry their module, text files do not."""
    found = []
    root, package_dir = root.resolve(), package_dir.resolve()
    base = package_dir.parent
    for path in sorted(root.rglob("*")):
        if path.is_symlink() or not path.is_file() or SKIP_DIRS & set(path.relative_to(root).parts):
            continue
        inside = package_dir in path.parents or path == package_dir
        texts: list[tuple[str | None, str]] = []
        if path.suffix == ".py" and inside:
            try:
                tree = ast.parse(path.read_text(encoding="utf-8", errors="replace"))
            except (SyntaxError, ValueError):
                continue
            parts = path.relative_to(base).with_suffix("").parts
            module = ".".join(parts[:-1] if parts[-1] == "__init__" else parts)
            texts = [(module, doc) for node in ast.walk(tree) if isinstance(node, (ast.Module, ast.ClassDef, ast.FunctionDef, ast.AsyncFunctionDef))
                     and ">>>" in (doc := ast.get_docstring(node) or "")]
        elif path.suffix.lower() in DOC_SUFFIXES and not inside and not is_test_file(path, root):
            texts = [(None, path.read_text(encoding="utf-8", errors="replace"))]
        for module, text in texts:
            found += [{**draft, "module": module, "file": str(path.relative_to(root))} for draft in drafts_of(examples_of(text))]
    unique: dict[tuple, dict] = {}
    for draft in found:  # the same example in two places is one exercise; the first one stays
        unique.setdefault((draft["module"], tuple(draft["steps"]), draft["expression"]), draft)
    return list(unique.values())[:MAX_DRAFTS]


def dependencies_of(root: Path, package: str) -> list[str]:
    """What the library needs: from its pyproject.toml, else from PyPI's description of the package (read as data)."""
    _, declared = project_metadata(root)
    if declared:
        return declared
    try:
        reply = httpx.get(f"https://pypi.org/pypi/{package}/json", headers={"User-Agent": "repo2tools-corpus"}, timeout=20, follow_redirects=True)
        return [r for r in reply.json()["info"].get("requires_dist") or [] if "extra ==" not in r]
    except (httpx.HTTPError, KeyError, ValueError):
        return []


def box_for(candidate: dict, set_name: str, clones: Path = CLONES, readable: Path = EXAMPLE_WORKER):
    """The sandboxed environment of a scanned repository: its package and what it needs, and one file of ours that may run in it (the worker here)."""
    root = clones / folder_name(candidate["repo"])
    base, package, single_file = locate(root, likely_names(candidate))
    if not single_file and native_code(base / package):
        raise RuntimeError("the package has compiled code")
    return pipeline.make_box(set_name, base, package, dependencies_of(root, candidate["package"]), readable)


def drop_box(set_name: str) -> None:
    envs = pipeline.CACHE / "envs"  # read when used: tests point the cache at a temporary folder
    for path in (envs / set_name, envs / f"{set_name}.tmp"):
        shutil.rmtree(path, ignore_errors=True)
    (envs / f"{set_name}.sb").unlink(missing_ok=True)


def uses_of(draft: dict, api: dict, root: Path) -> list[str]:
    """What of the public API a draft's code uses, in the names of the usage scan (a function's path, `Class()`, `Class <`)."""
    usage = Usage(Api(api))
    names: dict = {}
    with warnings.catch_warnings():
        warnings.simplefilter("ignore", SyntaxWarning)
        if draft["module"]:  # a docstring example sees its module's names
            names = usage.own_names()
            try:
                names = usage.scan(absolute_imports(ast.parse((root / draft["file"]).read_text(encoding="utf-8", errors="replace"))), "docs", names)
            except (SyntaxError, ValueError, OSError):
                pass
        before = usage.uses("docs")
        usage.scan("\n".join([*draft["steps"], draft["expression"]]), "docs", names)
    return sorted(usage.uses("docs") - before)


class PythonRepository(Source):
    """One scanned repository: `candidate` is its record from `corpus-scan` (package, repo, commit)."""

    kind = "Python repository"
    PARTS = {"files": "Documentation files", "docstrings": "Docstrings"}

    def __init__(self, candidate: dict, clones: Path = CLONES, scans: Path | None = None):
        self.candidate, self.clones, self.scans = candidate, clones, scans
        self.name = folder_name(candidate["repo"])
        self.root = clones / self.name

    @cached_property
    def located(self) -> tuple[Path, str, bool]:
        return locate(self.root, likely_names(self.candidate))

    @property
    def package(self) -> str:
        return self.located[1]

    @property
    def package_dir(self) -> Path:
        base, package, single_file = self.located
        return base / f"{package}.py" if single_file else base / package

    @cached_property
    def api(self) -> dict | None:
        """The saved scan of the public API, if there is one."""
        file = self.scans / self.name / "api.json" if self.scans else None
        return json.loads(file.read_text(encoding="utf-8")) if file and file.is_file() else None

    def at_scanned_commit(self) -> bool:
        """Is the clone there, and at the commit the scan recorded? Counts from another commit would not belong to the scan."""
        if not self.root.is_dir():
            return False
        head = subprocess.run(["git", "-C", str(self.root), "rev-parse", "HEAD"], capture_output=True, text=True).stdout.strip()
        return head == self.candidate.get("commit")

    def parts(self) -> dict[str, int]:
        return text_lines(self.root, self.package_dir)

    def part_of(self, item: dict) -> str:
        return "docstrings" if item["module"] else "files"

    def elements(self) -> set[str]:
        return {f"{c['module']}.{c['qualname']}" for c in self.api["callables"]} if self.api else set()

    def drafts(self) -> list[dict]:
        if not self.located[2] and native_code(self.package_dir):
            raise RuntimeError("the package has compiled code")
        with warnings.catch_warnings():
            warnings.simplefilter("ignore", SyntaxWarning)  # old escape sequences in other people's code
            return collect(self.root, self.package_dir, self.package)

    def uses(self, draft: dict) -> list[str]:
        return uses_of(draft, self.api, self.root) if self.api else []

    def box(self, set_name: str, readable: Path = EXAMPLE_WORKER):
        return box_for(self.candidate, set_name, self.clones, readable)
