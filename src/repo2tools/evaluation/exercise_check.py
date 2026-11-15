"""Check answers to exercises, and resolve references to earlier tool outputs. Stdlib only.

An exercise (one JSON object per line) has, among other fields:
  answer            the correct answer, a JSON value
  check             {"kind": "exact" | "set_equal" | "number"}: how an answer is compared with `answer`
  reference_calls   [{"tool": name, "arguments": {...}}, ...], one known-good solution
  reference_answer  the answer built from the outputs of reference_calls

In `arguments` and `reference_answer`, {"$ref": [i, key, ...]} stands for the output of
reference call i, followed by object keys or list indexes.
"""

import json
import math


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
    raise ValueError(f"unknown check kind: {kind!r}")


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
