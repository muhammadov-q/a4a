"""An API reference under each question, for the conditions python-ref and python-search of `a4a corpus-benchmark`.

Both ways read only the library's static scan (out/corpus/scans/<repository>/api.json); nothing from the repository is run.

    ref     the reference of the API elements that the question's verified code uses: the same text the second model
            got when the question was checked as solvable (`a4a corpus-tasks`). The best a look-up can give.
    search  the reference of the SEARCH_K elements that a word search (BM25) over the library's API finds for the
            question's wording: what a model gets without knowing the answer.

A reference is the signature and the first lines of the documentation of each element (`tasks.reference_of`).

Writes out/corpus/references/<tasks>/<repository>-<way>.jsonl ({id, reference, elements}) for `run-model --reference`,
and out/corpus/references/<tasks>/search.md: how many of the elements each answer uses the search found.
"""

import json
import math
import os
import re
from collections import Counter

from a4a.corpus.scan import OUT
from a4a.corpus.tasks import reference_of

WAYS = {"python-ref": "ref", "python-search": "search"}
SEARCH_K = 8
NAME_WEIGHT = 2  # an element's name counts twice: a question names what it wants more often than it quotes the documentation
STOPWORDS = set("""a an and are as at be by can for from given has have how if in into is it its library must of on one or python that the
their then this to two use using value what when which whether with""".split())


def words(text: str) -> list[str]:
    """Lowercase words, with names split at dots, underscores and capitals (`SpecifierSet.to_range` gives specifier, set,
    to, range) and a plural made singular, so that a question's words meet the names."""
    found = []
    for part in re.findall(r"[A-Z]+(?![a-z])|[A-Z]?[a-z]+|\d+", text):
        word = part.lower()
        if word.endswith("ies") and len(word) > 4:
            word = word[:-3] + "y"
        elif word.endswith("s") and not word.endswith("ss") and len(word) > 3:
            word = word[:-1]
        if word not in STOPWORDS:
            found.append(word)
    return found


def elements_of(api: dict) -> dict[str, list[str]]:
    """Every element a reference can show, by the name `reference_of` takes, with the words of its name and documentation."""
    found = {}
    for c in api["callables"]:
        name = f"{c['module']}.{c['qualname']}"
        found[name] = words(name) * NAME_WEIGHT + words(" ".join(p["name"] for p in c["params"])) + words((c.get("docstring") or c.get("summary") or "")[:400])
    for short, info in api.get("classes", {}).items():
        found[f"{short}()"] = words(f"{info['module']}.{short}") * NAME_WEIGHT + words(" ".join(p["name"] for p in info.get("params") or [])) + words((info.get("summary") or "")[:400])
    return found


def search(question: str, documents: dict[str, list[str]], k: int = SEARCH_K, k1: float = 1.2, b: float = 0.75) -> list[str]:
    """The k elements with the highest BM25 score for the question's words, best first; an element that shares no word scores nothing."""
    counts = {name: Counter(doc) for name, doc in documents.items()}
    average = sum(map(len, documents.values())) / max(len(documents), 1)
    df = Counter(word for count in counts.values() for word in count)
    asked = set(words(question))
    scores = {}
    for name, count in counts.items():
        length = len(documents[name])
        score = sum(math.log(1 + (len(counts) - df[w] + 0.5) / (df[w] + 0.5)) * count[w] * (k1 + 1) / (count[w] + k1 * (1 - b + b * length / average)) for w in asked if w in count)
        if score > 0:
            scores[name] = score
    return sorted(scores, key=lambda name: (-scores[name], name))[:k]


def references(tasks: list[dict], api: dict, way: str) -> list[dict]:
    """Per question: {id, reference, elements}. For "search", also `used` and `found`: the elements the answer uses that a
    reference can show, and those of them the search found."""
    documents = elements_of(api) if way == "search" else {}
    rows = []
    for task in tasks:
        if way == "ref":
            rows.append({"id": task["id"], "reference": reference_of(task["library_functions"], api), "elements": task["library_functions"]})
            continue
        top = search(task["task"], documents)
        used = [u for u in task["library_functions"] if u in documents]
        rows.append({"id": task["id"], "reference": reference_of(top, api), "elements": top, "used": used, "found": [u for u in used if u in top]})
    return rows


def short(element: str) -> str:
    """The last part of an element's name: `networkx.Graph.degree` and `networkx.DiGraph.degree` are both `degree`."""
    return element.removesuffix("()").rsplit(".", 1)[-1]


def reference_file(stem: str, tasks: str, condition: str):
    return OUT / "references" / tasks / f"{stem}-{WAYS[condition]}.jsonl"


def write_if_changed(path, text: str) -> None:
    """Write only a changed file, and whole: benchmarks running at the same time all write the references, and a run
    that read a half-written file would ask some questions without one."""
    if path.is_file() and path.read_text(encoding="utf-8") == text:
        return
    path.parent.mkdir(parents=True, exist_ok=True)
    partial = path.with_name(f"{path.name}.{os.getpid()}.tmp")
    partial.write_text(text, encoding="utf-8")
    os.replace(partial, path)


def write_references(repos: list[dict], tasks: str) -> str:
    """Both references for every repository's questions, and the report on the search. Returns the report's path."""
    rows = []
    for repo in repos:
        api = json.loads((OUT / "scans" / repo["stem"] / "api.json").read_text())
        questions = [json.loads(line) for line in repo["path"].read_text().splitlines()]
        for condition, way in WAYS.items():
            found = references(questions, api, way)
            write_if_changed(reference_file(repo["stem"], tasks, condition), "".join(json.dumps(r) + "\n" for r in found))
            if way == "search":
                used = [{short(u) for u in r["used"]} for r in found]
                hit = [{short(u) for u in r["elements"]} & names for r, names in zip(found, used)]
                rows.append({"package": repo["package"], "elements": len(elements_of(api)), "questions": len(found), "used": sum(map(len, used)), "found": sum(map(len, hit)),
                             "all_found": sum(bool(names) and names == h for names, h in zip(used, hit)), "with_used": sum(map(bool, used)),
                             "characters": round(sum(len(r["reference"]) for r in found) / max(len(found), 1))})
    lines = [f"# The search reference for out/corpus/{tasks}/", "",
             f"Per question, a word search (BM25) over the library's API finds {SEARCH_K} elements; their signatures and the start of their documentation go under the question. "
             "Names used: the names of the elements of the verified answer that a reference can show (functions, methods, properties and classes; not operators). "
             "A name counts as found if the search found an element of that name: the scan cannot tell `G.degree` of a `Graph` from that of a `DiGraph`, so it lists both.", "",
             "| Package | API elements | Questions | Names used | Found by the search | Questions with every used name found | Characters per reference |",
             "| --- | --- | --- | --- | --- | --- | --- |"]
    for r in rows:
        lines.append(f"| `{r['package']}` | {r['elements']} | {r['questions']} | {r['used']} | {r['found']} ({r['found'] / max(r['used'], 1):.0%}) | "
                     f"{r['all_found']} of {r['with_used']} | {r['characters']} |")
    used, found = sum(r["used"] for r in rows), sum(r["found"] for r in rows)
    lines.append(f"| **all** | | **{sum(r['questions'] for r in rows)}** | **{used}** | **{found} ({found / max(used, 1):.0%})** | "
                 f"**{sum(r['all_found'] for r in rows)} of {sum(r['with_used'] for r in rows)}** | |")
    report = OUT / "references" / tasks / "search.md"
    write_if_changed(report, "\n".join(lines) + "\n")
    return str(report.relative_to(OUT.parent.parent))
