"""The baseline tool set: one tool, `run_python`, that runs code where the library is installed. Standard library and `mcp` only.

`a4a corpus-benchmark` starts this file as an MCP server on stdio, inside the library's own environment
and sandbox, because the code it runs is written by a model:

    <env>/bin/python -I python_tool.py --library networkx

It is what generated tools have to beat: a model that can run Python needs no tool per function.

Every call runs in a new interpreter (this same file with `--run`, the code on stdin) and in a new empty folder,
so nothing is kept between calls and a call that hangs or crashes does not take the server down. The reply is what the code printed, then
the `repr` of its last line if that line is an expression, like a notebook cell. An exception, or more than
SECONDS, is a tool error.
"""

import ast
import asyncio
import os
import sys
import tempfile
import traceback

SECONDS = 10
MAX_TEXT = 20_000
DESCRIPTION = ("Run Python code in a new Python interpreter that has the library `{library}` installed. Returns what the code prints, "
               "and the value of its last line if that line is an expression. Every call starts from nothing: import what you need "
               "and put all steps into one call. No network. A call is stopped after {seconds} seconds.")


def run_cell(source: str) -> int:
    """Run code like a notebook cell: print the value of a last expression. Returns the exit status."""
    names: dict = {"__name__": "__main__"}
    try:
        body = ast.parse(source, "<code>").body
        last = body.pop() if body and isinstance(body[-1], ast.Expr) else None
        exec(compile(ast.Module(body, []), "<code>", "exec"), names)  # noqa: S102 (this runs inside the sandbox)
        if last is not None:
            value = eval(compile(ast.Expression(last.value), "<code>", "eval"), names)  # noqa: S307
            if value is not None:
                print(repr(value))
    except BaseException as error:  # noqa: BLE001 (SystemExit from the code is a failure too)
        lines = [frame.lineno for frame in traceback.extract_tb(error.__traceback__) if frame.filename == "<code>"]
        where = f" (line {lines[-1]} of the code)" if lines else ""
        sys.stdout.flush()
        print("".join(traceback.format_exception_only(type(error), error)).strip()[:2000] + where, file=sys.stderr)
        return 1
    return 0


async def run_python(code: str) -> str:
    with tempfile.TemporaryDirectory(ignore_cleanup_errors=True) as folder:  # inside $TMPDIR, the one folder the sandbox lets us write
        process = await asyncio.create_subprocess_exec(sys.executable, "-I", os.path.abspath(__file__), "--run", stdin=asyncio.subprocess.PIPE,
                                                       stdout=asyncio.subprocess.PIPE, stderr=asyncio.subprocess.PIPE, cwd=folder)
        try:
            printed, problem = await asyncio.wait_for(process.communicate(code.encode()), SECONDS)
        except TimeoutError:
            process.kill()
            await process.wait()
            raise RuntimeError(f"the code did not finish in {SECONDS} seconds") from None
    text = printed.decode(errors="replace").strip()
    if len(text) > MAX_TEXT:
        text = text[:MAX_TEXT] + f"\n[output cut: {len(text):,} characters in all]"
    if process.returncode != 0:
        raise RuntimeError("\n".join(part for part in (text, problem.decode(errors="replace").strip() or f"the interpreter ended with status {process.returncode}") if part))
    return text


def main() -> None:
    if sys.argv[1:] == ["--run"]:
        sys.exit(run_cell(sys.stdin.read()))
    if len(sys.argv) != 3 or sys.argv[1] != "--library":
        sys.exit("usage: python_tool.py --library <import name>")
    from mcp.server.fastmcp import FastMCP

    server = FastMCP(f"python-{sys.argv[2]}", log_level="WARNING")
    server.add_tool(run_python, description=DESCRIPTION.format(library=sys.argv[2], seconds=SECONDS))
    server.run()


if __name__ == "__main__":
    main()
