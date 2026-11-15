"""Exercises with known answers, made from a repository's own documentation examples.

    uv run repo2tools corpus-exercises [--limit N] [--only name ...] [--jobs 3]

A doctest example is a small exercise that the library's authors wrote and checked: some code, and what its
last expression gives. For every scanned repository this command

  1. reads the doctest examples in its documentation files and in the docstrings of its package,
  2. turns each example that shows a value into a draft: the expression, the documented output, and the
     earlier lines of the same text that the expression needs (found by following the names it reads),
  3. runs every draft in the library's own environment and sandbox, twice,
  4. keeps a draft as **verified** only if both runs give the same plain JSON value and that value is what
     the documentation shows.

So a verified answer has two independent sources: the documentation, and the library as it is at the scanned
commit. Each exercise also lists what it uses of the API (from the usage scan), which is the number of tools
a task built on it would need.

This runs code of the repository, so it runs only in the environment and sandbox of `repo2tools generate`
(no network, the home folder unreadable, one scratch folder writable), and only for repositories on the
approved list. The environment is deleted afterwards.

Writes out/corpus/exercises/<repository>.jsonl (the verified ones), out/corpus/exercises.json (one record
per repository, with what happened to every draft) and out/corpus/exercises.md.
"""

import argparse
import ast
import doctest
import json
import shutil
import subprocess
import time
import warnings
from collections import Counter
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path

import httpx

from repo2tools.corpus.scan import CLONES, OUT, folder_name, likely_names, locate
from repo2tools.paths import REPO_ROOT
from repo2tools.synthesis import pipeline
from repo2tools.synthesis.pipeline import native_code, project_metadata
from repo2tools.synthesis.usage import DOC_SUFFIXES, SKIP_DIRS, Api, Usage, absolute_imports, is_test_file

WORKER = Path(__file__).resolve().parent / "example_worker.py"
MAX_STEPS, MAX_CODE, MAX_EXPRESSION, MAX_DRAFTS = 12, 1500, 300, 400
BATCH_SECONDS = 600
CHECKER = doctest.OutputChecker()


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


def run_drafts(box, drafts: list[dict]) -> list[dict] | None:
    """What every draft gives, from one run of the sandboxed worker. None if the worker itself failed."""
    request = {"items": [{"module": d["module"], "steps": d["steps"], "expression": d["expression"], "printed": d.get("printed", False)} for d in drafts]}
    try:
        process = subprocess.run(box.command(str(WORKER)), input=json.dumps(request), text=True, capture_output=True,
                                 timeout=BATCH_SECONDS, env=box.clean_env, cwd=box.scratch)
        return json.loads(process.stdout)["results"]
    except (subprocess.TimeoutExpired, json.JSONDecodeError, KeyError):
        return None


def judge(draft: dict, first: dict, second: dict) -> str:
    """verified, or why not: error, timeout, not_json, not_repeatable, differs_from_docs."""
    if first["status"] != "ok":
        return first["status"]
    if second["status"] != "ok" or first["value"] != second["value"] or first["text"] != second["text"]:
        return "not_repeatable"
    if not CHECKER.check_output(draft["documented"] + "\n", first["text"] + "\n", doctest.NORMALIZE_WHITESPACE):
        return "differs_from_docs"
    return "verified"


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


def box_for(candidate: dict, set_name: str, clones: Path = CLONES, readable: Path = WORKER):
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


def exercises_for(candidate: dict, clones: Path = CLONES, scans: Path | None = None, keep_environment: bool = False) -> tuple[dict, list[dict]]:
    """(record of what happened, verified exercises) for one scanned repository. Never raises."""
    name = folder_name(candidate["repo"])
    record = {"package": candidate["package"], "repo": candidate["repo"], "commit": candidate.get("commit"), "error": None, "drafts": 0, "outcomes": {}}
    started = time.monotonic()
    set_name = f"examples-{name}"
    try:
        root = clones / name
        base, package, single_file = locate(root, likely_names(candidate))
        package_dir = base / f"{package}.py" if single_file else base / package
        if not single_file and native_code(package_dir):
            raise RuntimeError("the package has compiled code")
        with warnings.catch_warnings():
            warnings.simplefilter("ignore", SyntaxWarning)
            drafts = collect(root, package_dir, package)
        record["drafts"] = len(drafts)
        if not drafts:
            return record | {"seconds": round(time.monotonic() - started, 1)}, []
        box = box_for(candidate, set_name, clones)
        first, second = run_drafts(box, drafts), run_drafts(box, drafts)
        if first is None or second is None:
            raise RuntimeError("the sandboxed run did not finish")
        api = json.loads((scans / name / "api.json").read_text()) if scans and (scans / name / "api.json").is_file() else None
        verified = []
        outcomes, errors = Counter(), Counter()
        for draft, a, b in zip(drafts, first, second):
            outcome = judge(draft, a, b)
            outcomes[outcome] += 1
            if outcome == "error":
                errors[a["error"].split(":")[0]] += 1
            if outcome != "verified":
                continue
            uses = uses_of(draft, api, root) if api else []
            verified.append({"id": f"{name}-{len(verified) + 1:03d}", "repo": candidate["repo"], "commit": candidate.get("commit"), "package": package,
                             "file": draft["file"], "module": draft["module"], "steps": draft["steps"], "expression": draft["expression"],
                             "answer": a["value"], "answer_kinds": a.get("kinds", []), "documented": draft["documented"], "uses": uses})
        record["outcomes"] = dict(outcomes)
        record["errors"] = dict(errors.most_common(5))
    except (Exception, SystemExit) as error:  # noqa: BLE001 (one repository must not stop the pass)
        text = str(error).strip().splitlines()[0][:200] if str(error).strip() else ""
        record["error"] = f"{type(error).__name__}: {text}".replace(str(clones) + "/", "")
        verified = []
    finally:
        if not keep_environment:
            drop_box(set_name)
    return record | {"seconds": round(time.monotonic() - started, 1)}, verified


def report(records: list[dict]) -> str:
    outcomes = Counter()
    for r in records:
        outcomes.update(r["outcomes"])
    drafts, verified = sum(r["drafts"] for r in records), outcomes["verified"]
    with_some = [r for r in records if r["outcomes"].get("verified")]
    lines = ["# Exercises from documentation examples", "",
             f"{len(records)} repositories. {drafts:,} examples in their documentation show a value; {verified:,} of them are verified: run twice in the "
             f"library's own environment and sandbox, a plain JSON value both times, and the value the documentation shows. "
             f"{len(with_some)} repositories have at least one.", "",
             "| What happened to an example | Number |", "| --- | --- |"]
    names = {"verified": "verified", "error": "the code raised an error (also: needs earlier context, the network or a file)", "not_json": "the result is an object, not a plain value",
             "differs_from_docs": "the result is not what the documentation shows", "not_repeatable": "two runs gave different results", "timeout": "took longer than 5 s"}
    lines += [f"| {names.get(outcome, outcome)} | {n:,} |" for outcome, n in outcomes.most_common()]
    lines += ["", "| Package | Examples that show a value | Verified | Error | Object | Differs | Not scanned or run because |", "| --- | --- | --- | --- | --- | --- | --- |"]
    for r in sorted(records, key=lambda r: -r["outcomes"].get("verified", 0)):
        o = r["outcomes"]
        lines.append(f"| `{r['package']}` | {r['drafts']} | {o.get('verified', 0)} | {o.get('error', 0) + o.get('timeout', 0)} | {o.get('not_json', 0)} | "
                     f"{o.get('differs_from_docs', 0) + o.get('not_repeatable', 0)} | {(r['error'] or '').replace('|', '/')} |")
    return "\n".join(lines) + "\n"


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("--static", type=Path, default=OUT / "static.json", help="the scanned repositories, from `repo2tools corpus-scan`")
    parser.add_argument("--only", nargs="+", help="only these packages")
    parser.add_argument("--limit", type=int, help="only the first N repositories")
    parser.add_argument("--jobs", type=int, default=3)
    args = parser.parse_args()
    scanned = [r for r in json.loads(args.static.read_text())["repositories"] if not r["error"]]
    scanned = [r for r in scanned if not args.only or r["package"] in args.only][:args.limit]
    folder = OUT / "exercises"
    folder.mkdir(parents=True, exist_ok=True)

    def one(candidate: dict) -> dict:
        record, verified = exercises_for(candidate, scans=OUT / "scans")
        target = folder / f"{folder_name(candidate['repo'])}.jsonl"
        if verified:
            target.write_text("".join(json.dumps(e) + "\n" for e in verified), encoding="utf-8")
        else:
            target.unlink(missing_ok=True)
        print(f"{candidate['package']}: {record['outcomes'].get('verified', 0)} verified of {record['drafts']} {record['outcomes']} {record.get('errors', '')}"
              + (f" ({record['error']})" if record["error"] else ""), flush=True)
        return record

    with ThreadPoolExecutor(args.jobs) as pool:
        records = list(pool.map(one, scanned))
    if not args.only and not args.limit:
        (OUT / "exercises.json").write_text(json.dumps({"repositories": records}, indent=1) + "\n", encoding="utf-8")
        (OUT / "exercises.md").write_text(report(records), encoding="utf-8")
    total = sum(r["outcomes"].get("verified", 0) for r in records)
    print(f"{total:,} verified exercises from {sum(1 for r in records if r['outcomes'].get('verified'))} of {len(records)} repositories -> {(OUT / 'exercises.md').relative_to(REPO_ROOT)}")


if __name__ == "__main__":
    main()
