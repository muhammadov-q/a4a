"""What every kind of source gives the commands that extract something from it.

A source is a place information comes from: today a Python repository (its documentation files and the
docstrings of its package). A command that makes exercises from a source, or measures them, uses only the
methods below, so a new kind of source needs a new class here and no change in those commands.

    parts()        the text of the source, in lines, by part: what density is measured against
    part_of(item)  the part a draft or an exercise comes from
    elements()     what the source offers, by name: what coverage is measured against
    drafts()       candidate exercises, found by reading; nothing is run
    uses(draft)    the elements a draft touches
    box(name)      the sandbox in which anything from this source is run

A draft is a dict with `steps` (statements that set it up), `expression` (what the question is about),
`documented` (the result the source shows for it), and `module` and `file` (where it was found). The worker
`corpus/example_worker.py` runs it. A draft becomes an exercise when two runs in the box give the same plain
value and that value is what the source shows (`repo2tools corpus-exercises`).

Not behind this interface yet: tool generation (`repo2tools generate`), which reads a repository in its own way.
"""

from abc import ABC, abstractmethod
from pathlib import Path


class Source(ABC):
    kind: str  # the name of the kind of source, for reports
    PARTS: dict[str, str]  # part -> its title in reports
    name: str  # a name that is safe in file names and unique among the sources of a run

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
    def box(self, set_name: str, readable: Path):
        """The sandboxed environment for this source; `readable` is the one file of ours that may run in it."""
