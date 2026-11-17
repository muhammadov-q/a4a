"""How many verified exercises a source holds, and how much of the source they cover. Nothing is run.

    uv run a4a corpus-density [--jobs 4]

Reads what `corpus-scan` and `corpus-exercises` (and, if present, `corpus-tasks`) wrote, and the clones in
.cache/corpus/ to count lines of text. For every scanned repository it reports

  density   verified exercises per 1,000 lines, for each kind of source with its own denominator:
            documentation files (lines of the files), docstrings (lines of the docstrings), and all of
            them per 1,000 lines of code
  yield     of the documentation examples that could become an exercise, the share that was verified
  coverage  the share of the public API (functions, methods, properties) that at least one verified
            exercise uses, next to the share the repository's own documentation uses at all
  spread    the share of verified exercises that use the single most used API element

Lines are counted without blank lines. An example counts for the kind of source it was found in. Which API
elements an exercise uses comes from the static usage scan, so a method called on a value whose class the
scan cannot tell is missed. `corpus-exercises` reads at most MAX_DRAFTS examples of a repository; for a
repository at that limit the numbers are a lower bound, and the report names it.

Writes out/corpus/density.json (the counts) and out/corpus/density.md (the tables).
"""

import argparse
import json
from collections import Counter
from concurrent.futures import ProcessPoolExecutor
from statistics import median

from a4a.corpus.scan import CLONES, OUT
from a4a.sources.python_repository import MAX_DRAFTS, PythonRepository

KINDS = PythonRepository.PARTS


def density_of(source: PythonRepository, outcome: dict | None, exercises: list[dict], questions: int | None) -> dict:
    """The counts for one scanned repository. `lines` is None when the clone is missing or at another commit; `examples` also when the exercise pass did not run them."""
    static, paths, classes = source.candidate, source.elements(), (source.api or {}).get("classes", {})
    used = Counter(use for e in exercises for use in set(e["uses"]))
    covered = sorted(paths & set(used))
    record = {"package": static["package"], "repo": static["repo"], "commit": static["commit"], "code_lines": static["files"]["lines"], "lines": None, "examples": None,
              "not_run": outcome["error"] if outcome else "no exercise pass", "verified": dict(Counter(source.part_of(e) for e in exercises)), "questions": questions,
              "api": len(paths), "api_in_docs": static["usage"]["callables_used_in_docs"], "api_covered": len(covered),
              "classes": len(classes), "classes_built": sum(1 for name in classes if f"{name}()" in used),
              "without_api": sum(1 for e in exercises if not paths & set(e["uses"])),
              "most_used": max(((used[p], p) for p in covered), default=(0, None))}
    if source.at_scanned_commit():
        record["lines"] = source.parts()
        if outcome and not outcome["error"]:
            record["examples"] = dict(Counter(source.part_of(d) for d in source.drafts()))
    return record


def one(job: tuple) -> dict:
    static, outcome, questions, scans, exercises_dir, clones = job
    source = PythonRepository(static, clones, scans)
    file = exercises_dir / f"{source.name}.jsonl"
    exercises = [json.loads(line) for line in file.read_text(encoding="utf-8").splitlines()] if file.is_file() else []
    return density_of(source, outcome, exercises, questions)


def rank_correlation(xs: list[float], ys: list[float]) -> float | None:
    """Spearman's rank correlation, ties given their mean rank. None for fewer than three pairs or no variation."""
    def ranks(values: list[float]) -> list[float]:
        order = sorted(range(len(values)), key=values.__getitem__)
        result = [0.0] * len(values)
        start = 0
        while start < len(order):
            end = start
            while end + 1 < len(order) and values[order[end + 1]] == values[order[start]]:
                end += 1
            for i in order[start:end + 1]:
                result[i] = (start + end) / 2
            start = end + 1
        return result

    if len(xs) < 3:
        return None
    a, b = ranks(xs), ranks(ys)
    mean_a, mean_b = sum(a) / len(a), sum(b) / len(b)
    spread = (sum((x - mean_a) ** 2 for x in a) * sum((y - mean_b) ** 2 for y in b)) ** 0.5
    return sum((x - mean_a) * (y - mean_b) for x, y in zip(a, b)) / spread if spread else None


def per_thousand(count: int, lines: int | None) -> float | None:
    return 1000 * count / lines if lines else None


def shown(value: float | None, form: str = ".1f") -> str:
    return "n/a" if value is None else format(value, form)


def percent(share: float | None, form: str = ".1f") -> str:
    return "n/a" if share is None else format(100 * share, form) + "%"


def verified_of(record: dict, kind: str | None = None) -> int:
    return record["verified"].get(kind, 0) if kind else sum(record["verified"].values())


def report(records: list[dict]) -> str:
    counted = [r for r in records if r["lines"] is not None]
    productive = [r for r in records if verified_of(r)]
    total = lambda rows, get: sum(get(r) for r in rows)  # noqa: E731
    lines = ["# Density and coverage of verified exercises", "",
             f"{len(records)} scanned repositories. {len(productive)} give at least one verified exercise. "
             f"Lines of text were counted in {len(counted)} clones; nothing was run.", "",
             "## By kind of source", "",
             "| Kind of source | Lines | Examples | Verified | Yield | Verified per 1,000 lines | Repositories with one or more | Median per 1,000 lines in those |", "| --- | --- | --- | --- | --- | --- | --- | --- |"]
    for kind, title in KINDS.items():
        text, examples, verified = (total(counted, lambda r, k=kind, f=field: (r[f] or {}).get(k, 0)) for field in ("lines", "examples", "verified"))
        rates = [per_thousand(verified_of(r, kind), r["lines"][kind]) for r in counted if verified_of(r, kind) and r["lines"][kind]]
        lines.append(f"| {title} | {text:,} | {examples:,} | {verified:,} | {percent(verified / examples if examples else None, '.0f')} | "
                     f"{shown(per_thousand(verified, text), '.2f')} | {len(rates)} | {shown(median(rates) if rates else None, '.2f')} |")
    code, verified = total(records, lambda r: r["code_lines"]), total(records, verified_of)
    rates = [per_thousand(verified_of(r), r["code_lines"]) for r in productive if r["code_lines"]]
    not_run = [r for r in records if r["not_run"]]
    capped = [r for r in records if r["examples"] is not None and sum(r["examples"].values()) >= MAX_DRAFTS]
    ranked = sorted((verified_of(r) for r in records), reverse=True)
    lines += [f"| All, against lines of code | {code:,} | | {verified:,} | | {shown(per_thousand(verified, code), '.2f')} | {len(rates)} | {shown(median(rates) if rates else None, '.2f')} |", "",
              "Yield is verified exercises out of the examples that could become one. An example counts for the kind of source it was found in."
              + (f" Left out, because the examples were not run: {', '.join(f'`{r['package']}` ({r['not_run']})' for r in not_run)}." if not_run else ""), "",
              *([f"At most {MAX_DRAFTS} examples of a repository are read. At that limit, so with numbers that are a lower bound: {', '.join(f'`{r['package']}`' for r in capped)}.", ""] if capped else []),
              "## Where the exercises are", "",
              "| Repositories | Count |", "| --- | --- |",
              f"| with no example that could become an exercise | {sum(1 for r in records if r['examples'] is not None and not sum(r['examples'].values()))} |",
              f"| with examples, none verified | {sum(1 for r in records if r['examples'] is not None and sum(r['examples'].values()) and not verified_of(r))} |",
              f"| with at least one verified exercise | {len(productive)} |", "",
              "Share of all verified exercises held by the repositories with the most: "
              + ", ".join(f"top {k}: {percent(sum(ranked[:k]) / verified if verified else None, '.0f')}" for k in (1, 3, 5, 10)) + ".", "",
              "## Coverage of the public API", "",
              "| | Count | Share of the public API |", "| --- | --- | --- |"]
    api, in_docs, covered = (total(records, lambda r, f=field: r[f]) for field in ("api", "api_in_docs", "api_covered"))
    classes, built = total(records, lambda r: r["classes"]), total(records, lambda r: r["classes_built"])
    shares = [r["api_covered"] / r["api"] for r in records if r["api"]]
    with_exercises = [r["api_covered"] / r["api"] for r in productive if r["api"]]
    lines += [f"| Functions, methods and properties | {api:,} | |",
              f"| used somewhere in the repository's documentation | {in_docs:,} | {in_docs / max(api, 1):.1%} |",
              f"| used by at least one verified exercise | {covered:,} | {covered / max(api, 1):.1%} |",
              f"| Classes | {classes:,} | |",
              f"| built by at least one verified exercise | {built:,} | {built / max(classes, 1):.1%} |", "",
              f"Median coverage per repository: {percent(median(shares) if shares else None)} over all scanned repositories, "
              f"{percent(median(with_exercises) if with_exercises else None)} over those with a verified exercise.", ""]
    without, tops = total(productive, lambda r: r["without_api"]), [r["most_used"][0] / verified_of(r) for r in productive if r["most_used"][0]]
    lines += [f"{without:,} of {verified:,} verified exercises use no function, method or property that the scan can name "
              "(they build a class, use an operator, or call something the scan cannot resolve).",
              f"In the median repository with exercises, {percent(median(tops) if tops else None, '.0f')} of the exercises use the single most used element.", "",
              "## Does size explain the number of exercises?", "",
              "Spearman rank correlation with the number of verified exercises, over the repositories whose lines were counted:", "",
              "| Measure of size | Correlation |", "| --- | --- |"]
    for title, get in (("Lines of code", lambda r: r["code_lines"]), ("Lines of documentation files", lambda r: r["lines"]["files"]),
                       ("Lines of docstrings", lambda r: r["lines"]["docstrings"]), ("Public API elements", lambda r: r["api"])):
        lines.append(f"| {title} | {shown(rank_correlation([get(r) for r in counted], [verified_of(r) for r in counted]), '.2f')} |")
    lines += ["", "## Per repository", "",
              "| Package | Lines of code | Doc lines | Docstring lines | Examples | Verified | From files | From docstrings | Per 1,000 lines of code | Questions | API | In docs | Covered | Coverage |",
              "| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |"]
    for r in sorted(records, key=lambda r: (-verified_of(r), r["package"])):
        text = r["lines"] or {}
        lines.append(f"| `{r['package']}` | {r['code_lines']:,} | {shown(text.get('files'), ',')} | {shown(text.get('docstrings'), ',')} | "
                     f"{shown(sum(r['examples'].values()) if r['examples'] is not None else None, ',')} | {verified_of(r)} | {verified_of(r, 'files')} | {verified_of(r, 'docstrings')} | "
                     f"{shown(per_thousand(verified_of(r), r['code_lines']), '.2f')} | {shown(r['questions'], 'd')} | {r['api']} | {r['api_in_docs']} | {r['api_covered']} | "
                     f"{percent(r['api_covered'] / r['api'] if r['api'] else None)} |")
    return "\n".join(lines) + "\n"


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("--jobs", type=int, default=4)
    args = parser.parse_args()
    statics = [r for r in json.loads((OUT / "static.json").read_text())["repositories"] if not r["error"]]
    outcomes = {r["repo"]: r for r in json.loads((OUT / "exercises.json").read_text())["repositories"]}
    tasks = OUT / "tasks.json"
    questions = {r["package"]: r["written"] for r in json.loads(tasks.read_text())["repositories"]} if tasks.is_file() else {}
    jobs = [(s, outcomes.get(s["repo"]), questions.get(s["import_name"]), OUT / "scans", OUT / "exercises", CLONES) for s in statics]
    with ProcessPoolExecutor(args.jobs) as pool:
        records = list(pool.map(one, jobs))
    (OUT / "density.json").write_text(json.dumps({"repositories": records}, indent=1) + "\n", encoding="utf-8")
    (OUT / "density.md").write_text(report(records), encoding="utf-8")
    missing = [r["package"] for r in records if r["lines"] is None]
    print(f"{len(records)} repositories, {sum(verified_of(r) for r in records):,} verified exercises -> out/corpus/density.md")
    if missing:
        print(f"  no clone at the scanned commit, lines not counted: {', '.join(missing)}")


if __name__ == "__main__":
    main()
