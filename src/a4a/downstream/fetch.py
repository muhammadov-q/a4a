"""Fetch the approved public benchmarks and check that each file is the one that was approved.

    uv run a4a public-fetch [--only spider humaneval]

Public benchmarks are made by others, and the pipeline never saw them: they show whether a model trained on our
verified tasks gets better or worse at work it was not trained on. The list a person approved is
out/downstream/benchmarks.json: per benchmark its home page, license, and a fixed address and a SHA-256 for every
file. A file is downloaded only if it is not there yet, into .cache/downstream/<name>/, and is kept only if its
SHA-256 matches.

Spider comes as one zip. Only what its dev set needs is taken out: dev.json and the SQLite file of each of its
databases, into .cache/downstream/spider/dev/. A database name that is not a plain name, a file that is missing
or larger than MAX_MEMBER stops the extraction. The database files are not opened here: `a4a spider-tasks`
reads them only in the sandbox.
"""

import argparse
import functools
import json
import re
import shutil
import zipfile
from pathlib import Path

from a4a.databases.fetch import checked, download, sha256_of
from a4a.paths import REPO_ROOT

LIST = REPO_ROOT / "out" / "downstream" / "benchmarks.json"
CACHE = REPO_ROOT / ".cache" / "downstream"
MAX_BYTES = 300_000_000  # the Spider zip is about 206 MB
MAX_MEMBER = 200_000_000  # the largest dev database, wta_1, has 105 MB
SPIDER_ROOT = "spider_data/"


def spider_dev(cache: Path = CACHE) -> Path:
    """The folder with Spider's dev.json and database/<db_id>.sqlite."""
    return cache / "spider" / "dev"


def extract_spider(archive: Path, target: Path) -> dict:
    """Take dev.json and the dev databases out of Spider's zip. Returns {"questions", "databases"}."""
    marker = target / "extracted.json"
    digest = sha256_of(archive)
    if marker.is_file() and json.loads(marker.read_text())["zip_sha256"] == digest:
        return json.loads(marker.read_text())
    shutil.rmtree(target, ignore_errors=True)
    (target / "database").mkdir(parents=True)
    with zipfile.ZipFile(archive) as zipped:
        questions = json.loads(zipped.read(SPIDER_ROOT + "dev.json"))
        names = sorted({q["db_id"] for q in questions})
        if bad := [n for n in names if not re.fullmatch(r"[A-Za-z0-9_]+", n)]:
            raise RuntimeError(f"database names that are not plain names: {bad[:3]}")
        wanted = {target / "dev.json": SPIDER_ROOT + "dev.json"} | {target / "database" / f"{n}.sqlite": f"{SPIDER_ROOT}database/{n}/{n}.sqlite" for n in names}
        for path, member in wanted.items():
            info = zipped.getinfo(member)  # KeyError if it is missing
            if info.file_size > MAX_MEMBER:
                raise RuntimeError(f"{member} has {info.file_size:,} bytes")
            with zipped.open(info) as source, path.open("wb") as sink:
                shutil.copyfileobj(source, sink)
    record = {"zip_sha256": digest, "questions": len(questions), "databases": len(names)}
    marker.write_text(json.dumps(record) + "\n")
    return record


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("--only", nargs="+", help="only these benchmarks")
    args = parser.parse_args()
    for benchmark in json.loads(LIST.read_text(encoding="utf-8"))["benchmarks"]:
        if args.only and benchmark["name"] not in args.only:
            continue
        folder = CACHE / benchmark["name"]
        states = [checked(file, folder, False, fetch=functools.partial(download, max_bytes=MAX_BYTES)) for file in benchmark["files"]]
        problems = [s for s in states if s != "ok"]
        if not problems and benchmark["name"] == "spider":
            try:
                found = extract_spider(folder / benchmark["files"][0]["name"], spider_dev())
                states.append(f"dev set: {found['questions']} questions on {found['databases']} databases")
            except (RuntimeError, KeyError, zipfile.BadZipFile, json.JSONDecodeError) as error:
                problems.append(f"extraction: {error}")
        print(f"{benchmark['name']}: " + ("; ".join(problems) if problems else ", ".join(s for s in states if s != "ok") or "ok"))


if __name__ == "__main__":
    main()
