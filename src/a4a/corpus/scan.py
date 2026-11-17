"""Static pass over the approved candidate repositories: clone, count, scan. No repository code is run.

    uv run a4a corpus-scan [--limit N] [--jobs 4]

For every repository in out/corpus/candidates.json it

  1. clones it (hooks off, no LFS, no submodules) and records the commit,
  2. finds the package and counts files and lines,
  3. scans the public API, following re-exports (`scrape.public_api`), and how the repository's own
     documentation and tests use it (`a4a usage`), both with `ast` only,
  4. counts tool candidates at three levels of granularity, see `corpus.granularity`.

Only files inside the checkout are read; links are not followed. A repository that cannot be handled
(no package found, a monorepo, a scan that takes too long) is recorded with the reason, not dropped.

Writes out/corpus/static.json (one record per repository), out/corpus/static.md (the table), and the full
scans under out/corpus/scans/<repository>/ (large and rebuildable, so not kept in git).
"""

import argparse
import json
import re
import signal
import time
import warnings
from collections import Counter
from concurrent.futures import ProcessPoolExecutor
from dataclasses import asdict
from pathlib import Path
from statistics import median

from a4a.corpus.granularity import level_counts
from a4a.paths import REPO_ROOT
from a4a.repo2tools.pipeline import checked_url, clone, find_package, native_code
from a4a.repo2tools.scrape import constructors, public_api
from a4a.repo2tools.usage import DOC_SUFFIXES, SKIP_DIRS, count_usage, is_test_file

OUT = REPO_ROOT / "out" / "corpus"
CLONES = REPO_ROOT / ".cache" / "corpus"
TIME_LIMIT = 600  # seconds for one repository

def folder_name(repo_url: str) -> str:
    owner, name = repo_url.rstrip("/").removesuffix(".git").split("/")[-2:]
    return f"{owner}__{name}".lower()


def likely_names(candidate: dict) -> list[str]:
    """Import names to try first: the PyPI name and the repository name, also without a `python-` or `py` prefix."""
    names = []
    for raw in (candidate["package"], candidate["repo"].rstrip("/").removesuffix(".git").rsplit("/", 1)[-1]):
        name = re.sub(r"[-_.]+", "_", raw).lower()
        names += [name, name.removeprefix("python_"), name.removesuffix("_python"), name.removeprefix("py")]
    return [n for n in dict.fromkeys(names) if n]


def locate(root: Path, names: list[str]) -> tuple[Path, str, bool]:
    """(folder that holds it, import name, is it a single file?). A package wins over a single-file module."""
    for name in names:
        try:
            return (*find_package(root, name), False)
        except SystemExit:
            continue
    for base in (root / "src", root):
        for name in names:
            if (base / f"{name}.py").is_file() and not (base / f"{name}.py").is_symlink():
                return base, name, True
    return (*find_package(root, None), False)


def count_files(root: Path, package_dir: Path) -> dict:
    """Python files and lines of the package, and the test and documentation files of the whole checkout."""
    counts = {"python": 0, "lines": 0, "tests": 0, "docs": 0}
    for path in root.rglob("*"):
        if path.is_symlink() or not path.is_file() or SKIP_DIRS & set(path.relative_to(root).parts):
            continue
        inside = package_dir in path.parents or path == package_dir
        if path.suffix == ".py" and inside:
            counts["python"] += 1
            counts["lines"] += sum(1 for line in path.read_text(encoding="utf-8", errors="replace").splitlines() if line.strip())
        elif path.suffix == ".py" and is_test_file(path, root):
            counts["tests"] += 1
        elif path.suffix.lower() in DOC_SUFFIXES and not inside:
            counts["docs"] += 1
    return counts


def scan_one(candidate: dict, clones: Path = CLONES, scans: Path | None = None) -> dict:
    """One repository, start to end. Never raises: a failure is a record with `error`."""
    record = {"package": candidate["package"], "repo": candidate["repo"], "commit": None, "error": None}
    started = time.monotonic()

    def too_slow(signum, frame):
        raise TimeoutError(f"took longer than {TIME_LIMIT} s")

    signal.signal(signal.SIGALRM, too_slow)
    signal.alarm(TIME_LIMIT)
    try:
        root = clones / folder_name(candidate["repo"])
        record["commit"] = clone(checked_url(candidate["repo"]), candidate.get("commit"), root)
        base, package, single_file = locate(root, likely_names(candidate))
        package_dir = (base / f"{package}.py" if single_file else base / package).resolve()
        with warnings.catch_warnings():
            warnings.simplefilter("ignore", SyntaxWarning)  # old escape sequences in other people's code
            callables = public_api(base, package)
        api = {"repo": candidate["repo"], "package": package, "commit": record["commit"], "callables": [asdict(c) for c in callables],
               "classes": constructors(base, callables)}
        with warnings.catch_warnings():
            warnings.simplefilter("ignore", SyntaxWarning)
            usage = count_usage(api, root, package_dir).as_json()
        kinds = Counter(c["kind"] for c in api["callables"])
        record |= {"import_name": package, "layout": ("src" if base.name == "src" else "top level") + (", one file" if single_file else ""), "files": count_files(root.resolve(), package_dir),
                   "native_files": 0 if single_file else len(native_code(package_dir)),
                   "api": {"callables": len(callables), "classes": len(api["classes"]), **{k: kinds[k] for k in ("function", "method", "property", "classmethod", "staticmethod")}},
                   "usage": {"doc_files": usage["files"]["docs"], "test_files": usage["files"]["tests"], "unparsed_pieces": usage["unparsed_pieces"],
                             "callables_used_in_docs": len(usage["ranking"]["docs"]), "callables_used_in_tests": len(usage["ranking"]["tests"]),
                             "classes_built_in_docs": sum(1 for c in usage["classes"].values() if c["built"]["docs"]),
                             "classes_with_operators": sum(1 for c in usage["classes"].values() if c["operators"])},
                   "levels": level_counts(api, usage)}
        if scans is not None:
            folder = scans / folder_name(candidate["repo"])
            folder.mkdir(parents=True, exist_ok=True)
            (folder / "api.json").write_text(json.dumps(api, indent=1), encoding="utf-8")
            (folder / "usage.json").write_text(json.dumps(usage, indent=1), encoding="utf-8")
    except (Exception, SystemExit) as error:  # noqa: BLE001 (one repository must not stop the pass)
        text = str(error).strip().splitlines()[0][:200] if str(error).strip() else ""
        record["error"] = f"{type(error).__name__}: {text}".replace(str(clones) + "/", "").replace(str(clones.resolve()) + "/", "")
    finally:
        signal.alarm(0)
    record["seconds"] = round(time.monotonic() - started, 1)
    return record


def report(records: list[dict]) -> str:
    good = [r for r in records if not r["error"]]
    total = lambda key, sub: sum(r[key][sub] for r in good)  # noqa: E731
    mid = lambda key, sub: median(r[key][sub] for r in good) if good else 0  # noqa: E731
    lines = ["# Static pass over the candidate repositories", "",
             f"{len(good)} of {len(records)} repositories scanned. Nothing was run: the counts come from reading the files.", ""]
    if good:
        lines += ["| | Total | Median per repository |", "| --- | --- | --- |",
                  f"| Python files in the package | {total('files', 'python'):,} | {mid('files', 'python'):g} |",
                  f"| Lines of code (not blank) | {total('files', 'lines'):,} | {mid('files', 'lines'):g} |",
                  f"| Public functions, methods and properties | {total('api', 'callables'):,} | {mid('api', 'callables'):g} |",
                  f"| Classes with public members | {total('api', 'classes'):,} | {mid('api', 'classes'):g} |",
                  f"| Documentation examples that use the API | {total('levels', 'examples'):,} | {mid('levels', 'examples'):g} |", "",
                  "## Tool candidates by level", "",
                  "| Level | One tool is | Candidates | Median per repository | Used in the repository's own docs |", "| --- | --- | --- | --- | --- |"]
        for level, what in (("low", "one function, method or property"), ("medium", "one operation on an object"), ("high", "one documented example with two or more uses")):
            used = f"{total('levels', level + '_used_in_docs'):,} ({total('levels', level + '_used_in_docs') / max(total('levels', level), 1):.0%})" if level != "high" else "all, by definition"
            lines.append(f"| {level} | {what} | {total('levels', level):,} | {mid('levels', level):g} | {used} |")
        lines += ["", "## Per repository", "",
                  "| Package | Commit | Files | Lines | API | Classes | Used in docs | Low | Medium | High |", "| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |"]
        lines += [f"| `{r['package']}` | `{r['commit'][:7]}` | {r['files']['python']} | {r['files']['lines']:,} | {r['api']['callables']} | {r['api']['classes']} | "
                  f"{r['usage']['callables_used_in_docs']} | {r['levels']['low']} | {r['levels']['medium']} | {r['levels']['high']} |" for r in good]
    failed = [r for r in records if r["error"]]
    if failed:
        lines += ["", "## Not scanned", "", "| Package | Repository | Reason |", "| --- | --- | --- |"]
        lines += [f"| `{r['package']}` | {r['repo']} | {r['error'].replace('|', '/')} |" for r in failed]
    return "\n".join(lines) + "\n"


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("--candidates", type=Path, default=OUT / "candidates.json", help="the approved list, from `a4a corpus-candidates`")
    parser.add_argument("--limit", type=int, help="only the first N repositories")
    parser.add_argument("--jobs", type=int, default=4)
    args = parser.parse_args()
    candidates = json.loads(args.candidates.read_text())["candidates"][:args.limit]
    with ProcessPoolExecutor(args.jobs) as pool:
        records = list(pool.map(scan_one, candidates, [CLONES] * len(candidates), [OUT / "scans"] * len(candidates)))
    OUT.mkdir(parents=True, exist_ok=True)
    (OUT / "static.json").write_text(json.dumps({"repositories": records}, indent=1) + "\n", encoding="utf-8")
    (OUT / "static.md").write_text(report(records), encoding="utf-8")
    failed = [r for r in records if r["error"]]
    print(f"{len(records) - len(failed)} of {len(records)} repositories scanned -> out/corpus/static.md")
    for r in failed:
        print(f"  not scanned: {r['package']}: {r['error']}")


if __name__ == "__main__":
    main()
