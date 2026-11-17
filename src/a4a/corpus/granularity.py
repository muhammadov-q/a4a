"""Tool candidates at three levels of granularity, made from a repository's scans. Nothing is generated or run.

    low     one tool per API element: every public function, method and property
    medium  one tool per operation on an object: a module function stays one tool; a class gives one tool that
            builds it, one that reads all its properties, one per method, and one per family of operators the
            repository uses with it (all comparisons together, `in` and `not in` together, others one each)
    high    one tool per documented example that uses at least two different things of the API

Each candidate has a short text that says what the tool would do, without the name of its library, so that
candidates of different libraries can be compared (`a4a corpus-saturation`).
"""

# operators that ask the same kind of question become one tool at the middle level
FAMILIES = {"<": "compare", "<=": "compare", ">": "compare", ">=": "compare", "==": "compare", "!=": "compare", "in": "contains", "not in": "contains"}
FAMILY_TEXT = {"compare": "compare two of them (smaller, equal, greater)", "contains": "test whether it contains a value", "&": "intersect two of them (&)",
               "|": "unite two of them (|)", "^": "symmetric difference of two of them (^)", "-": "subtract one from another (-)", "+": "add two of them (+)"}


def signature(c: dict, name: str | None = None) -> str:
    params = ", ".join(p["name"] + (f": {p['annotation']}" if p.get("annotation") else "") for p in c.get("params") or [])
    returns = f" -> {c['returns']}" if c.get("returns") else ""
    return f"{name or c['qualname']}({params}){returns}"


def describe(c: dict) -> str:
    return f"{signature(c)}: {c['summary']}" if c.get("summary") else signature(c)


def tool_candidates(api: dict, usage: dict) -> list[dict]:
    """Every candidate of one repository: {"level", "id", "text", "used_in_docs"}."""
    counts = usage["callables"]
    in_docs = lambda path: bool(counts.get(path, {}).get("docs") or counts.get(path, {}).get("guessed_docs"))  # noqa: E731
    path_of = lambda c: f"{c['module']}.{c['qualname']}"  # noqa: E731
    out = [{"level": "low", "id": path_of(c), "text": describe(c), "used_in_docs": in_docs(path_of(c))} for c in api["callables"]]

    by_class: dict[str, list[dict]] = {}
    for c in api["callables"]:
        if "." in c["qualname"]:
            by_class.setdefault(c["qualname"].split(".")[0], []).append(c)
        else:
            out.append({"level": "medium", "id": path_of(c), "text": describe(c), "used_in_docs": in_docs(path_of(c))})
    for name, members in by_class.items():
        info = api.get("classes", {}).get(name) or {}
        seen = usage["classes"].get(name, {"built": {}, "operators": {}})
        base = f"{members[0]['module']}.{name}"
        what = (info.get("summary") or "").strip()
        built = signature({"qualname": name, "params": info.get("params") or [], "returns": None})
        out.append({"level": "medium", "id": f"{base}#build", "text": f"{built}: build a {name}" + (f". {what}" if what else ""), "used_in_docs": bool(seen["built"].get("docs"))})
        properties = [m for m in members if m["kind"] == "property"]
        if properties:
            listed = ", ".join(m["qualname"].split(".", 1)[1] for m in properties)
            out.append({"level": "medium", "id": f"{base}#properties", "text": f"{name}: read its properties: {listed}",
                        "used_in_docs": any(in_docs(path_of(m)) for m in properties)})
        out += [{"level": "medium", "id": path_of(m), "text": describe(m), "used_in_docs": in_docs(path_of(m))} for m in members if m["kind"] != "property"]
        families: dict[str, int] = {}
        for symbol, n in seen["operators"].items():
            families[FAMILIES.get(symbol, symbol)] = families.get(FAMILIES.get(symbol, symbol), 0) + n.get("docs", 0)
        out += [{"level": "medium", "id": f"{base}#{family}", "text": f"{name}: {FAMILY_TEXT.get(family, 'use the operator ' + family)}", "used_in_docs": bool(n)}
                for family, n in families.items()]

    examples: dict[tuple, dict] = {}
    for example in usage.get("examples", []):
        if len(example["uses"]) >= 2:
            examples.setdefault(tuple(example["uses"]), example)  # the same set of uses is one tool
    short = lambda use: use.rsplit(".", 2)[-2] + "." + use.rsplit(".", 1)[-1] if use.count(".") >= 2 and use.rsplit(".", 2)[-2][:1].isupper() else use.rsplit(".", 1)[-1]  # noqa: E731
    out += [{"level": "high", "id": "example:" + " + ".join(uses), "text": "Example that uses " + ", ".join(short(u) for u in uses) + ":\n" + example["code"][:600],
             "used_in_docs": True} for uses, example in examples.items()]
    return out


def level_counts(api: dict, usage: dict) -> dict:
    """How many candidates each level has, how many the repository's own documentation uses, and how many examples there are."""
    found = tool_candidates(api, usage)
    count = lambda level, used=False: sum(1 for c in found if c["level"] == level and (c["used_in_docs"] or not used))  # noqa: E731
    examples = usage.get("examples", [])
    return {"low": count("low"), "low_used_in_docs": count("low", True), "medium": count("medium"), "medium_used_in_docs": count("medium", True),
            "high": count("high"), "examples": len(examples), "examples_with_two_or_more": sum(1 for e in examples if len(e["uses"]) >= 2)}
