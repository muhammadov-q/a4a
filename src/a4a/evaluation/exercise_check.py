"""Check answers to exercises, and resolve references to earlier tool outputs. Stdlib only.

An exercise (one JSON object per line) has, among other fields:
  answer            the correct answer, a JSON value
  check             {"kind": "exact" | "set_equal" | "number" | "rows"}: how an answer is compared with `answer`;
                    "rows" is for the result of a query (`answer` is its rows), see rows_match()
  reference_calls   [{"tool": name, "arguments": {...}}, ...], one known-good solution
  reference_answer  the answer built from the outputs of reference_calls

In `arguments` and `reference_answer`, {"$ref": [i, key, ...]} stands for the output of
reference call i, followed by object keys or list indexes.
"""

import itertools
import json
import math
from collections import Counter


def _canonical(value) -> str:
    # JSON keeps true and 1 apart, unlike Python's ==
    return json.dumps(value, sort_keys=True)


def check(exercise: dict, answer) -> bool:
    """Return whether `answer` (a JSON value) is correct for `exercise`."""
    expected = exercise["answer"]
    kind = exercise["check"]["kind"]
    if kind == "exact":
        return _canonical(answer) == _canonical(expected)
    if kind == "set_equal":
        return isinstance(answer, list) and sorted(map(_canonical, answer)) == sorted(map(_canonical, expected))
    if kind == "number":  # 4 and 4.0 are the same number; true is not a number
        return isinstance(answer, (int, float)) and not isinstance(answer, bool) and math.isclose(answer, expected, rel_tol=1e-9, abs_tol=1e-12)
    if kind == "rows":
        return rows_match(answer, expected, exercise["check"].get("ordered", False))
    raise ValueError(f"unknown check kind: {kind!r}")


MAX_PERMUTED = 6  # columns up to this number may come in any order


def _cell(value) -> tuple:
    """A cell of a result in the form it is compared in: 3, 3.0, true-as-1 and "3" are one number (to 4 decimals), text without outer spaces."""
    if isinstance(value, (bool, int, float)):
        number = float(value)
        return ("number", round(number, 4) + 0.0) if math.isfinite(number) else ("text", str(value))
    if isinstance(value, str):
        text = value.strip()
        try:
            number = float(text)
        except ValueError:
            return ("text", text)
        return ("number", round(number, 4) + 0.0) if math.isfinite(number) else ("text", text)
    if value is None:
        return ("null", None)
    return ("other", json.dumps(value, sort_keys=True))


def _readings(answer) -> list[list]:
    """The ways an answer can be read as rows: one value, one column, one row, a list of rows, or rows as objects."""
    if answer is None:
        return [[[None]], []]
    if isinstance(answer, dict):
        return [[list(answer.values())]]
    if not isinstance(answer, list):
        return [[[answer]]]
    readings = []
    if all(isinstance(row, list) for row in answer):
        readings.append(answer)
    if answer and all(isinstance(row, dict) for row in answer):
        readings.append([list(row.values()) for row in answer])
    if answer and not any(isinstance(row, (list, dict)) for row in answer):
        readings += [[[value] for value in answer], [answer]]
    return readings


def rows_match(answer, expected: list[list], ordered: bool) -> bool:
    """Whether an answer gives the same rows as a query's result, the way Spider compares two results by running them:
    the same rows (in the same order if the query orders them), with the columns in any order. The answer may be one
    value, a list of values (one column or one row), a list of rows, or rows as objects."""
    width = len(expected[0]) if expected else 0
    wanted = [tuple(map(_cell, row)) for row in expected]
    for rows in _readings(answer):
        if len(rows) != len(expected) or any(not isinstance(row, list) or len(row) != width for row in rows):
            continue
        given = [tuple(map(_cell, row)) for row in rows]
        for order in itertools.permutations(range(width)) if width <= MAX_PERMUTED else [tuple(range(width))]:
            moved = [tuple(row[i] for i in order) for row in given]
            if (moved == wanted) if ordered else (Counter(moved) == Counter(wanted)):
                return True
    return False


def resolve(template, outputs: list):
    """Replace every {"$ref": [i, *path]} in `template` with that part of outputs[i]."""
    if isinstance(template, dict):
        if set(template) == {"$ref"}:
            index, *path = template["$ref"]
            value = outputs[index]
            for key in path:
                value = value[key]
            return value
        return {k: resolve(v, outputs) for k, v in template.items()}
    if isinstance(template, list):
        return [resolve(v, outputs) for v in template]
    return template
