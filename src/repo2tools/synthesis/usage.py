"""Count how often a repository's own documentation and tests use each function of its public API.

    uv run repo2tools usage out/generated/packaging-coder-60/api.json .cache/repos/packaging -o out/usage/packaging.json

Which functions should become tools? An LLM can guess from names and docstrings. The repository
itself knows better: what its documentation shows in examples, and what its tests exercise, is what
the library is used for. This script counts those uses, without running anything (`ast` only).

Sources, kept apart because they are not equally independent of a benchmark built from the tests:
  docs    examples in documentation files (`>>>` lines and Python code blocks in .rst and .md files,
          and the README) and in the docstrings of the package itself
  tests   Python files in test folders

What counts as a use of `pkg.mod.Class.method`:
  - a call of an imported function, or of a function reached through an imported module;
  - an attribute on a value whose class is known: built by the class, returned by an API function
    whose return annotation names the class, or the class itself (class methods).
"guessed" uses are attributes on values of unknown class, where exactly the classes used in that
file have a member of this name. They are reported, and only used to break ties.
Class constructions and operators on known values (`<`, `==`, `in`, `&`) are counted per class:
they are uses of the library that no single function stands for.
"""

import argparse
import ast
import json
import re
from collections import Counter, defaultdict
from pathlib import Path

SOURCES = ("docs", "tests")
DOC_SUFFIXES = {".rst", ".md", ".txt"}
SKIP_DIRS = {".git", ".tox", ".nox", ".venv", "venv", "node_modules", "build", "dist", "__pycache__", "site-packages"}
OPERATORS = {ast.Lt: "<", ast.LtE: "<=", ast.Gt: ">", ast.GtE: ">=", ast.Eq: "==", ast.NotEq: "!=", ast.In: "in", ast.NotIn: "not in",
             ast.BitAnd: "&", ast.BitOr: "|", ast.BitXor: "^", ast.Add: "+", ast.Sub: "-"}


class Api:
    """The scraped public API, indexed for lookups by name."""

    def __init__(self, api: dict):
        self.package = api["package"]
        self.functions: dict[str, str] = {}  # "pkg.mod.name" -> path
        self.members: dict[str, dict[str, str]] = defaultdict(dict)  # class -> member name -> path
        self.returns: dict[str, str | None] = {}  # path -> class name it returns
        self.classes: dict[str, str] = {name: info["module"] for name, info in api.get("classes", {}).items()}
        for c in api["callables"]:
            path = f"{c['module']}.{c['qualname']}"
            if "." in c["qualname"]:
                owner, member = c["qualname"].split(".", 1)
                self.members[owner][member] = path
                self.classes.setdefault(owner, c["module"])
            else:
                self.functions[path] = path
        for c in api["callables"]:
            path = f"{c['module']}.{c['qualname']}"
            owner = c["qualname"].split(".")[0] if "." in c["qualname"] else None
            names = re.findall(r"[A-Za-z_][A-Za-z0-9_]*", c.get("returns") or "")
            self.returns[path] = owner if "Self" in names and owner else next((n for n in names if n in self.classes), None)
        by_name: dict[str, list[str]] = defaultdict(list)
        for path in self.functions:
            by_name[path.rsplit(".", 1)[1]].append(path)
        self.unique_functions = {name: paths[0] for name, paths in by_name.items() if len(paths) == 1}

    def lookup(self, dotted: str):
        """("function", path) or ("class", name) for a dotted name inside the package, else None. Follows re-exports by name."""
        if dotted in self.functions:
            return "function", dotted
        module, _, name = dotted.rpartition(".")
        if not (module == self.package or module.startswith(self.package + ".")):
            return None
        if name in self.classes:
            return "class", name
        if name in self.unique_functions:
            return "function", self.unique_functions[name]
        return None


class Usage:
    def __init__(self, api: Api):
        self.api = api
        self.callables = {path: {"docs": 0, "tests": 0, "guessed_docs": 0, "guessed_tests": 0}
                          for path in [*api.functions, *(p for members in api.members.values() for p in members.values())]}
        self.classes = {name: {"built": {"docs": 0, "tests": 0}, "operators": defaultdict(lambda: {"docs": 0, "tests": 0})} for name in api.classes}
        self.files = {"docs": 0, "tests": 0}
        self.unparsed = 0
        self.examples: list[dict] = []  # per documentation example that uses the API: {"uses": [...], "code": "..."}, see uses()

    def scan(self, code: str, source: str, names: dict | None = None) -> dict:
        """Count the uses in one piece of code. `names` carries imports and known values on to the next piece of the same file."""
        names = {} if names is None else names  # local name -> ("module", dotted) | ("function", path) | ("class", name) | ("value", {classes})
        try:
            tree = ast.parse(code)
        except (SyntaxError, ValueError, RecursionError):
            self.unparsed += 1
            return names
        api = self.api

        for node in ast.walk(tree):
            if isinstance(node, ast.Import):
                for alias in node.names:
                    if alias.name == api.package or alias.name.startswith(api.package + "."):
                        names[alias.asname or alias.name.split(".")[0]] = ("module", alias.name if alias.asname else alias.name.split(".")[0])
            elif isinstance(node, ast.ImportFrom) and node.module and not node.level and (node.module == api.package or node.module.startswith(api.package + ".")):
                for alias in node.names:
                    if alias.name == "*":  # `from pkg.mod import *`: the package's own names are known from here on
                        names |= self.own_names()
                        continue
                    found = api.lookup(f"{node.module}.{alias.name}")
                    names[alias.asname or alias.name] = found or ("module", f"{node.module}.{alias.name}")

        def kind_of(node) -> tuple | None:
            """What an expression is: a module, an API function, an API class, or a value of known classes."""
            if isinstance(node, ast.Name):
                return names.get(node.id)
            if isinstance(node, ast.Attribute):
                base = kind_of(node.value)
                if base and base[0] == "module":
                    return api.lookup(f"{base[1]}.{node.attr}") or ("module", f"{base[1]}.{node.attr}")
                if base and base[0] in ("class", "value"):
                    owners = [base[1]] if base[0] == "class" else sorted(base[1])
                    paths = [api.members[o][node.attr] for o in owners if node.attr in api.members.get(o, {})]
                    return ("member", paths) if paths else None
            if isinstance(node, ast.Call):
                called = kind_of(node.func)
                if called and called[0] == "class":
                    return "value", {called[1]}
                if called and called[0] == "function" and api.returns.get(called[1]):
                    return "value", {api.returns[called[1]]}
                if called and called[0] == "member":
                    classes = {api.returns[p] for p in called[1] if api.returns.get(p)}
                    return ("value", classes) if classes else None
            if isinstance(node, ast.BinOp):  # spec1 & spec2 is again a specifier set
                left = kind_of(node.left)
                return left if left and left[0] == "value" else None
            return None

        # what variables hold: two rounds, so that `b = a.method()` after `a = Class(...)` is known as well
        for _ in range(2):
            for node in ast.walk(tree):
                targets = node.targets if isinstance(node, ast.Assign) else [node.target] if isinstance(node, (ast.AnnAssign, ast.NamedExpr)) and node.value else []
                found = kind_of(node.value) if targets else None
                for target in targets:
                    if isinstance(target, ast.Name) and found and found[0] in ("value", "class", "function", "module"):
                        old = names.get(target.id)
                        names[target.id] = ("value", old[1] | found[1]) if found[0] == "value" and old and old[0] == "value" else found

        in_file = {v[1] for v in names.values() if v[0] == "class"} | {c for v in names.values() if v[0] == "value" for c in v[1]}
        for node in ast.walk(tree):
            if isinstance(node, ast.Call):
                called = kind_of(node.func)
                if called and called[0] == "function" and isinstance(node.func, ast.Name):
                    self.callables[called[1]][source] += 1
                elif called and called[0] == "class":
                    self.classes[called[1]]["built"][source] += 1
            if isinstance(node, ast.Attribute):
                found = kind_of(node)
                if found and found[0] == "function":
                    self.callables[found[1]][source] += 1
                elif found and found[0] == "member":
                    for path in found[1]:
                        self.callables[path]["guessed_" + source if len(found[1]) > 1 else source] += 1
                elif not found and not kind_of(node.value):
                    for owner in in_file:
                        if node.attr in api.members.get(owner, {}):
                            self.callables[api.members[owner][node.attr]]["guessed_" + source] += 1
            operands, operators = [], []
            if isinstance(node, ast.Compare):
                operands, operators = [node.left, *node.comparators], node.ops
            elif isinstance(node, ast.BinOp):
                operands, operators = [node.left, node.right], [node.op]
            for operator in operators:
                symbol = OPERATORS.get(type(operator))
                for owner in {c for o in operands for k in [kind_of(o)] if k and k[0] == "value" for c in k[1]} if symbol else ():
                    self.classes[owner]["operators"][symbol][source] += 1
        return names

    def uses(self, source: str) -> Counter:
        """Every use counted so far in one source, under one name each: a function's path, `Class()` for building, `Class <` for an operator."""
        found = Counter({path: row[source] + row["guessed_" + source] for path, row in self.callables.items()})
        for name, row in self.classes.items():
            found[f"{name}()"] = row["built"][source]
            found.update({f"{name} {symbol}": n[source] for symbol, n in row["operators"].items()})
        return +found

    def scan_python(self, path: Path, source: str) -> None:
        self.files[source] += 1
        self.scan(path.read_text(encoding="utf-8", errors="replace"), source)

    def own_names(self) -> dict:
        """The package's functions and classes by their bare names, as code inside the package or after a star import sees them."""
        return {name: ("function", path) for name, path in self.api.unique_functions.items()} | {name: ("class", name) for name in self.api.classes}

    def scan_examples(self, text: str, source: str = "docs", own_names: bool = False, preamble: str = "") -> None:
        """The Python examples in a documentation text: doctest lines, rst code blocks and Markdown fences.

        `own_names`: the text is a docstring inside the package, where examples use the package's functions and
        classes without importing them. `preamble`: the imports of the module the docstring is in, whose names
        (`import networkx as nx`) its examples use as well.
        """
        names: dict = self.own_names() if own_names else {}
        if preamble:
            names = self.scan(preamble, source, names)
        for group in example_groups(text):
            before = self.uses(source)
            for block in group:
                self.scan(block, source, names)
            used = sorted(self.uses(source) - before)
            if used:
                self.examples.append({"uses": used, "code": "\n".join(group)[:1500]})

    def score(self, path: str, by: str) -> tuple:
        """Sort key, larger is more used. Docs and tests have very different sizes, so each is taken as a share of its total."""
        row = self.callables[path]
        totals = {s: sum(r[s] for r in self.callables.values()) or 1 for s in SOURCES}
        sources = SOURCES if by == "both" else (by,)
        return (sum(row[s] / totals[s] for s in sources), sum(row["guessed_" + s] for s in sources))

    def ranking(self, by: str = "both") -> list[str]:
        """API paths that are used at least once, most used first."""
        sources = SOURCES if by == "both" else (by,)
        used = [p for p, row in self.callables.items() if any(row[s] or row["guessed_" + s] for s in sources)]
        return sorted(used, key=lambda p: (self.score(p, by), p), reverse=True)

    def as_json(self) -> dict:
        return {"package": self.api.package, "files": self.files, "unparsed_pieces": self.unparsed, "callables": self.callables,
                "classes": {n: {"built": c["built"], "operators": dict(c["operators"])} for n, c in self.classes.items()},
                "ranking": {by: self.ranking(by) for by in ("docs", "tests", "both")}, "examples": self.examples}


def example_groups(text: str) -> list[list[str]]:
    """The examples of a documentation text, in order; each is a list of pieces of Python code.

    One example is one code block (rst directive, Markdown fence, or a plain `::` block that is Python as a
    whole), or one doctest session: prompt lines with their outputs, across blank lines, until prose follows.
    A doctest piece that does not parse is tried statement by statement.
    """
    groups: list[list[str]] = []
    session: list[str] = []
    prompt: list[str] = []
    block, indent, literal, blank = None, 0, False, False

    def flush_prompt():
        if prompt:
            session.extend(statements(prompt))
            prompt.clear()

    def close_session():
        flush_prompt()
        if session:
            groups.append(list(session))
            session.clear()

    def close_block():
        nonlocal block
        code = ("\n".join(block) if indent < 0 else dedent(block)).strip("\n")
        block = None
        if literal:  # a plain `::` block may hold anything: keep it only if it is Python as a whole
            try:
                ast.parse(code)
            except (SyntaxError, ValueError, RecursionError):
                return
        if code.strip():
            groups.append([code])

    for line in text.splitlines():
        stripped = line.strip()
        if stripped.startswith(">>>"):
            prompt.append(stripped[3:].removeprefix(" "))
            blank = False
            continue
        if stripped.startswith("...") and prompt and not stripped.startswith("....") and block is None:
            prompt.append(stripped[3:].removeprefix(" "))
            continue
        flush_prompt()
        if block is not None:  # inside a code block or a Markdown fence
            if indent < 0:
                if stripped.startswith("```"):
                    close_block()
                else:
                    block.append(line)
                continue
            if not stripped or len(line) - len(line.lstrip()) > indent:
                block.append(line)
                continue
            close_block()
        if re.match(r"\s*\.\. (code-block|code|sourcecode|ipython)::\s*(python|py|pycon|python3|ipython)?\s*$", line):
            close_session()
            block, indent, literal = [], len(line) - len(line.lstrip()), False
        elif re.match(r"\s*```\s*(python|py|pycon|python3)\s*$", line):
            close_session()
            block, indent, literal = [], -1, False
        elif stripped.endswith("::") and not stripped.startswith(".."):
            close_session()
            block, indent, literal = [], len(line) - len(line.lstrip()), True
        elif not stripped:
            blank = True
        elif blank:  # prose after a blank line ends a doctest session; a line right after a prompt is its output
            close_session()
    close_session()
    if block is not None:
        close_block()
    return [[b for b in group if b.strip() and ">>>" not in b] for group in groups if any(b.strip() and ">>>" not in b for b in group)]


def example_blocks(text: str) -> list[str]:
    """Pieces of Python code in a documentation text, in order: the examples of example_groups(), flattened."""
    return [b.strip("\n") for group in example_groups(text) for b in group]


def dedent(lines: list[str]) -> str:
    body = [line for line in lines if line.strip()]
    cut = min((len(line) - len(line.lstrip()) for line in body), default=0)
    return "\n".join(line[cut:] for line in lines)


def statements(lines: list[str]) -> list[str]:
    """Doctest input lines as code: the whole run if it parses, else one piece per statement."""
    whole = "\n".join(lines)
    try:
        ast.parse(whole)
        return [whole]
    except (SyntaxError, ValueError):
        pieces, current = [], []
        for line in lines:
            if current and not line.startswith((" ", "\t", ")", "]", "}")):
                pieces.append("\n".join(current))
                current = []
            current.append(line)
        return pieces + ["\n".join(current)]


def is_test_file(path: Path, root: Path) -> bool:
    parts = path.relative_to(root).parts
    return any(p in ("tests", "test", "testing") for p in parts[:-1]) or path.name.startswith("test_") or path.name.endswith("_test.py") or path.name == "conftest.py"


def absolute_imports(tree: ast.Module) -> str:
    """The `import x` and `from x import y` lines at the top level of a module, as code. Relative imports bring names the package already knows."""
    return "\n".join(ast.unparse(node) for node in tree.body if isinstance(node, ast.Import) or (isinstance(node, ast.ImportFrom) and not node.level))


def count_usage(api_json: dict, repo: Path, package_dir: Path | None = None) -> Usage:
    """Scan a repository checkout. `package_dir` is the folder of the package itself: only its docstring examples are read."""
    usage = Usage(Api(api_json))
    package_dir = package_dir.resolve() if package_dir else None
    for path in sorted(repo.rglob("*")):
        if path.is_symlink() or not path.is_file() or SKIP_DIRS & set(path.relative_to(repo).parts):
            continue  # a link may point outside the checkout; nothing outside it is read
        inside = package_dir is not None and (package_dir in path.resolve().parents or path.resolve() == package_dir)  # a package, or a one-file module
        if path.suffix == ".py":
            if is_test_file(path, repo) and not inside:
                usage.scan_python(path, "tests")
            elif inside:  # the package's own docstrings are documentation
                try:
                    tree = ast.parse(path.read_text(encoding="utf-8", errors="replace"))
                except (SyntaxError, ValueError):
                    continue
                for node in ast.walk(tree):
                    if isinstance(node, (ast.Module, ast.ClassDef, ast.FunctionDef, ast.AsyncFunctionDef)) and ">>>" in (ast.get_docstring(node) or ""):
                        usage.scan_examples(ast.get_docstring(node), own_names=True, preamble=absolute_imports(tree))
        elif path.suffix.lower() in DOC_SUFFIXES and not inside and not is_test_file(path, repo):
            usage.files["docs"] += 1
            usage.scan_examples(path.read_text(encoding="utf-8", errors="replace"))
    return usage


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("api", type=Path, help="api.json written by `repo2tools generate` or `repo2tools scrape`")
    parser.add_argument("repo", type=Path, help="checkout of the repository")
    parser.add_argument("--package-dir", type=Path, help="folder of the package itself, for the examples in its docstrings")
    parser.add_argument("-o", "--out", type=Path)
    parser.add_argument("--top", type=int, default=25)
    args = parser.parse_args()
    usage = count_usage(json.loads(args.api.read_text()), args.repo, args.package_dir)
    result = usage.as_json()
    if args.out:
        args.out.parent.mkdir(parents=True, exist_ok=True)
        args.out.write_text(json.dumps(result, indent=1), encoding="utf-8")
    used = {by: len(result["ranking"][by]) for by in result["ranking"]}
    print(f"{usage.files['docs']} documentation files and {usage.files['tests']} test files scanned; {usage.unparsed} pieces did not parse")
    print(f"of {len(usage.callables)} API functions, used in the docs: {used['docs']}, in the tests: {used['tests']}, in either: {used['both']}")
    print(f"{'docs':>5} {'tests':>6} {'guessed':>8}  function")
    for path in result["ranking"]["both"][: args.top]:
        row = usage.callables[path]
        print(f"{row['docs']:>5} {row['tests']:>6} {row['guessed_docs'] + row['guessed_tests']:>8}  {path}")
    for name, c in sorted(usage.classes.items(), key=lambda item: -sum(item[1]["built"].values())):
        ops = ", ".join(f"{op} {n['docs'] + n['tests']}" for op, n in sorted(c["operators"].items(), key=lambda item: -sum(item[1].values())))
        if sum(c["built"].values()) or ops:
            print(f"  class {name}: built {c['built']['docs']} times in the docs, {c['built']['tests']} in the tests" + (f"; operators: {ops}" if ops else ""))


if __name__ == "__main__":
    main()
