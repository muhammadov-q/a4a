"""Run documentation examples of a library and report what the last expression gives. Standard library only.

`repo2tools corpus-exercises` runs this file inside the library's own environment and sandbox, because it
imports the library and runs code from its documentation:

    <env>/bin/python -I example_worker.py < request.json

Request: {"items": [{"module": dotted name or null, "steps": [source, ...], "expression": source, "printed": bool}, ...]}
Result (one JSON object on stdout): {"results": [{"status", "value", "text", "error"}, ...]}, in the same order.

    module      a docstring example sees the names of its module, like `doctest` gives it; null for a text file
    steps       statements that set the example up; each item starts from a fresh namespace
    expression  the expression the question is about
    printed     the documentation prints it (`print(x)`), so its text is `str(x)`, not `repr(x)`

status: "ok" (value is a plain JSON value; `kinds` names standard types that were converted, see plain()), "not_json" (an object; only
`text` is given), "error", "timeout".
"""

import contextlib
import datetime
import decimal
import fractions
import importlib
import io
import json
import math
import os
import pathlib
import signal
import sys

SECONDS = 5
MAX_TEXT = 2000


class TooSlow(BaseException):
    """Derived from BaseException so that an example's `except Exception` cannot swallow it."""


def plain(value, kinds: set, depth: int = 0):
    """The value as plain JSON, or raise TypeError.

    Numbers, text, true/false, null, lists (also from tuples) and objects with text keys stay as they are.
    A few standard types have one obvious plain form and are converted; `kinds` collects their names, so that
    a question can say which form is asked for: dates and times as ISO 8601 text, a time span as seconds,
    Decimal and Fraction and paths as text, a set as a sorted list.
    """
    if value is None or isinstance(value, (bool, str)):
        return value
    if type(value) is int:
        return value
    if type(value) is float:
        if math.isnan(value) or math.isinf(value):
            raise TypeError("not a JSON number")
        return value
    if depth > 6:
        raise TypeError("too deep")
    if type(value) in (list, tuple):
        return [plain(v, kinds, depth + 1) for v in value]
    if type(value) is dict and all(isinstance(k, str) for k in value):
        return {k: plain(v, kinds, depth + 1) for k, v in value.items()}
    if type(value) in (datetime.datetime, datetime.date, datetime.time):
        kinds.add(type(value).__name__)
        return value.isoformat()
    if type(value) is datetime.timedelta:
        kinds.add("timedelta")
        return value.total_seconds()
    if type(value) in (decimal.Decimal, fractions.Fraction) or isinstance(value, pathlib.PurePath):
        kinds.add("path" if isinstance(value, pathlib.PurePath) else type(value).__name__)
        return str(value)
    if type(value) in (set, frozenset):
        kinds.add("set")
        return sorted(plain(v, kinds, depth + 1) for v in value)  # TypeError if the members cannot be ordered
    raise TypeError(type(value).__name__)


def run_one(item: dict) -> dict:
    def on_alarm(signum, frame):
        raise TooSlow

    names: dict = {"__name__": "__example__"}
    signal.signal(signal.SIGALRM, on_alarm)
    signal.alarm(SECONDS)
    try:
        if item.get("module"):
            names.update(vars(importlib.import_module(item["module"])))
            names["__name__"] = "__example__"
        for step in item["steps"]:
            exec(compile(step, "<example>", "exec"), names)  # noqa: S102 (this is the sandboxed worker)
        value = eval(compile(item["expression"], "<example>", "eval"), names)  # noqa: S307
        text = str(value) if item.get("printed") else repr(value)
    except TooSlow:
        return {"status": "timeout", "error": f"took longer than {SECONDS} s"}
    except BaseException as error:  # noqa: BLE001 (SystemExit and KeyboardInterrupt from an example are failures too)
        return {"status": "error", "error": f"{type(error).__name__}: {str(error)[:200]}"}
    finally:
        signal.alarm(0)
    if len(text) > MAX_TEXT:
        return {"status": "error", "error": "the result is too long"}
    try:
        kinds: set = set()
        return {"status": "ok", "value": plain(value, kinds), "text": text, "kinds": sorted(kinds)}
    except TypeError:
        return {"status": "not_json", "text": text, "type": type(value).__name__}


def main() -> None:
    request = json.load(sys.stdin)
    real_stdout = sys.stdout
    results = []
    with contextlib.redirect_stdout(io.StringIO()), contextlib.redirect_stderr(io.StringIO()):  # an example must not write into our result
        for item in request["items"]:
            results.append(run_one(item))
    real_stdout.write(json.dumps({"results": results}))
    real_stdout.flush()
    os._exit(0)  # a leftover thread from an example must not keep the process alive


if __name__ == "__main__":
    main()
