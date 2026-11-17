"""What every kind of source gives the commands that extract something from it.

A source is a place information comes from: today a Python repository (its documentation files and the
docstrings of its package). A command that makes exercises from a source, or measures them, uses only the
methods below, so a new kind of source needs a new class here and no change in those commands.

    parts()        the text of the source, in lines, by part: what density is measured against
    part_of(item)  the part a draft or an exercise comes from
    elements()     what the source offers, by name: what coverage is measured against
    drafts()       candidate exercises, found by reading the source
    uses(draft)    the elements a draft touches
    origin(draft)  where a draft comes from: the fields that identify the source and the place in it
    box(name)      the sandbox in which anything from this source is run

A draft is a dict with `steps` (statements that set it up), `expression` (what the question is about),
`documented` (the result the source shows for it, or None if it shows none), and `module` and `file` (where
it was found). The worker `corpus/example_worker.py` runs it. A draft becomes an exercise when two runs in
the box give the same plain value and, if the source shows a result, that value is what it shows.

Reading a repository runs nothing. A database file is someone else's data, so even reading its schema
happens in the box.

Not behind this interface yet: tool generation (`a4a generate`), which reads a repository in its own way.
"""

import json
import subprocess
from abc import ABC, abstractmethod
from pathlib import Path

EXAMPLE_WORKER = Path(__file__).resolve().parents[1] / "corpus" / "example_worker.py"
BATCH_SECONDS = 600


def run_drafts(box, drafts: list[dict]) -> list[dict] | None:
    """What every draft gives, from one run of the sandboxed worker. None if the worker itself failed."""
    request = {"items": [{"module": d["module"], "steps": d["steps"], "expression": d["expression"], "printed": d.get("printed", False)} for d in drafts]}
    try:
        process = subprocess.run(box.command(str(EXAMPLE_WORKER)), input=json.dumps(request), text=True, capture_output=True,
                                 timeout=BATCH_SECONDS, env=box.clean_env, cwd=box.scratch)
        return json.loads(process.stdout)["results"]
    except (subprocess.TimeoutExpired, json.JSONDecodeError, KeyError):
        return None


class Source(ABC):
    kind: str  # the name of the kind of source, for reports
    PARTS: dict[str, str]  # part -> its title in reports
    name: str  # a name that is safe in file names and unique among the sources of a run

    @property
    def box_name(self) -> str:
        """The name of the environment that `corpus-exercises` builds for this source and deletes afterwards."""
        return f"examples-{self.name}"

    @abstractmethod
    def parts(self) -> dict[str, int]:
        """Lines of text (not blank) in each part."""

    @abstractmethod
    def part_of(self, item: dict) -> str:
        """The part a draft or an exercise was found in."""

    @abstractmethod
    def elements(self) -> set[str]:
        """The names of everything the source offers; empty if that is not known."""

    @abstractmethod
    def drafts(self) -> list[dict]:
        """Candidate exercises. Raises if the source cannot be run safely."""

    @abstractmethod
    def uses(self, draft: dict) -> list[str]:
        """The elements a draft touches, in the names of `elements()` where it can be told."""

    @abstractmethod
    def origin(self, draft: dict) -> dict:
        """The first fields of an exercise made from this draft: the source, its version, and the place in it."""

    @abstractmethod
    def box(self, set_name: str, readable: Path):
        """The sandboxed environment for this source; `readable` is the one file of ours that may run in it."""
