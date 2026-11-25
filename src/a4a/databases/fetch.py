"""Fetch the approved databases and check that each file is the one that was approved.

    uv run a4a db-fetch [--only name ...] [--pin]

Reads out/databases/candidates.json, the list a person approved. Every file has a fixed address (a release
or a commit) and a SHA-256. A file is downloaded only if it is not there yet, into .cache/databases/<name>/,
and is kept only if its SHA-256 matches. `--pin` writes the SHA-256 of a file that has none in the list yet;
that is done once, when a database is approved.

Nothing is opened here: a downloaded file is bytes. A database that comes as SQL scripts (`build` in the
list) is built by running the scripts with `sqlite3` inside a sandbox with no network, and only the finished
database file is copied out.
"""

import argparse
import hashlib
import json
import shutil
import subprocess
from pathlib import Path

import httpx

from a4a.paths import REPO_ROOT
from a4a.repo2tools import pipeline
from a4a.sources.base import EXAMPLE_WORKER
from a4a.sources.python_repository import drop_box

LIST = REPO_ROOT / "out" / "databases" / "candidates.json"
CACHE = REPO_ROOT / ".cache" / "databases"
MAX_BYTES = 100_000_000
BUILD_SECONDS = 600
BUILD = """
import sqlite3, sys
db = sqlite3.connect(sys.argv[1])
for name in sys.argv[2:]:
    db.executescript(open(name, encoding="utf-8").read())
db.commit()
db.close()
"""


def sha256_of(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as file:
        for block in iter(lambda: file.read(1 << 20), b""):
            digest.update(block)
    return digest.hexdigest()


def database_path(candidate: dict, cache: Path = CACHE) -> Path:
    return cache / candidate["name"] / candidate["database"]


def download(url: str, target: Path, max_bytes: int = MAX_BYTES) -> None:
    """The bytes at a fixed address, into a file. Stops at `max_bytes`."""
    target.parent.mkdir(parents=True, exist_ok=True)
    partial = target.with_name(target.name + ".part")
    with httpx.stream("GET", url, headers={"User-Agent": "a4a-corpus"}, timeout=120, follow_redirects=True) as reply:
        reply.raise_for_status()
        size = 0
        with partial.open("wb") as file:
            for block in reply.iter_bytes():
                size += len(block)
                if size > max_bytes:
                    partial.unlink()
                    raise RuntimeError(f"more than {max_bytes:,} bytes")
                file.write(block)
    partial.replace(target)


def checked(file: dict, folder: Path, pin: bool, fetch=download) -> str:
    """Make sure the file is in the folder and is the approved one. Returns "ok", "pinned", or what is wrong."""
    target = folder / file["name"]
    if not target.is_file():
        fetch(file["url"], target)
    found = sha256_of(target)
    if not file.get("sha256"):
        if not pin:
            return "no SHA-256 in the list; run with --pin once it is approved"
        file["sha256"] = found
        return "pinned"
    if found != file["sha256"]:
        target.unlink()
        return f"SHA-256 is {found}, not the approved one; the file was deleted"
    return "ok"


def build(candidate: dict, folder: Path) -> None:
    """Run the SQL scripts of a database inside a sandbox and copy the finished file out."""
    set_name = f"build-{candidate['name']}"
    try:
        box = pipeline.make_box(set_name, None, None, [], EXAMPLE_WORKER)
        for name in candidate["build"]:
            shutil.copy2(folder / name, box.scratch / name)
        done = subprocess.run(box.command("-c", BUILD, candidate["database"], *candidate["build"]), capture_output=True, text=True,
                              timeout=BUILD_SECONDS, env=box.clean_env, cwd=box.scratch)
        if done.returncode != 0:
            raise RuntimeError((done.stderr.strip().splitlines() or ["the build failed"])[-1][:200])
        shutil.copy2(box.scratch / candidate["database"], folder / candidate["database"])
    finally:
        drop_box(set_name)


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("--only", nargs="+", help="only these databases")
    parser.add_argument("--pin", action="store_true", help="write the SHA-256 of files that have none in the list yet")
    args = parser.parse_args()
    listed = json.loads(LIST.read_text(encoding="utf-8"))
    for candidate in listed["databases"]:
        if args.only and candidate["name"] not in args.only:
            continue
        folder = CACHE / candidate["name"]
        states = [checked(file, folder, args.pin) for file in candidate["files"]]
        problems = [s for s in states if s not in ("ok", "pinned")]
        if not problems and candidate.get("build") and not database_path(candidate).is_file():
            try:
                build(candidate, folder)
            except (RuntimeError, subprocess.TimeoutExpired, OSError) as error:
                problems.append(f"build: {error}")
        ready = database_path(candidate)
        print(f"{candidate['name']}: " + ("; ".join(problems) if problems else f"{ready.relative_to(REPO_ROOT)} ({ready.stat().st_size:,} bytes)" + (", pinned" if "pinned" in states else "")))
    if args.pin:
        LIST.write_text(json.dumps(listed, indent=1) + "\n", encoding="utf-8")


if __name__ == "__main__":
    main()
