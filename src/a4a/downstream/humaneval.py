"""Score a model on HumanEval: write a Python function from its signature and docstring; right if its tests pass.

    uv run a4a humaneval-benchmark --model qwen3-4b --base-url http://127.0.0.1:18004/v1

A check that training on our tasks did not make a model worse at plain Python. No tools: the model gets the
start of the function (HumanEval's prompt) and is asked for the whole function, at temperature 0 with thinking
off, so the score is pass@1 from one greedy answer. The code it writes is untrusted: each program (the imports
and helpers of the prompt, the model's code, then HumanEval's tests) runs in a sandbox with no network, no
access to the home folder, nothing written outside its own folder, and a time limit of SECONDS.

If the reply defines the function, it replaces the prompt's function; otherwise the reply is read as the body
and put under the prompt. A block under `if __name__ == "__main__":` is cut off, so a demo cannot wait for input.

Writes out/downstream/humaneval/<model>.jsonl (per problem: the reply, passed, status) and report-<model>.md.
"""

import argparse
import asyncio
import gzip
import json
import os
import re
import subprocess
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path

from openai import AsyncOpenAI

from a4a.downstream.fetch import CACHE
from a4a.paths import API_KEY_FILE, REPO_ROOT
from a4a.repo2tools import pipeline
from a4a.sources.python_repository import drop_box

OUT = REPO_ROOT / "out" / "downstream" / "humaneval"
SECONDS = 10
WORKERS = 8
ASK = "Complete the following Python function. Reply with the complete function, with its imports, in one ```python code block, and nothing else.\n\n```python\n{prompt}```"


def problems(path: Path = CACHE / "humaneval" / "HumanEval.jsonl.gz") -> list[dict]:
    with gzip.open(path, "rt", encoding="utf-8") as file:
        return [json.loads(line) for line in file if line.strip()]


def code_of(reply: str) -> str:
    """The code in a reply: the first fenced block, or the whole reply without a model's thinking."""
    reply = re.sub(r"<think>.*?</think>", "", reply or "", flags=re.S)
    block = re.search(r"```(?:python|py)?[ \t]*\n(.*?)(?:```|$)", reply, re.S)
    code = block.group(1) if block else reply
    return re.split(r"^if __name__\s*==\s*['\"]__main__['\"]\s*:", code, flags=re.M)[0]


def program(problem: dict, code: str) -> str:
    """What runs: the prompt's imports and helpers with the model's function (or the prompt with the model's body), then the tests."""
    entry, prompt = problem["entry_point"], problem["prompt"]
    if re.search(rf"^def {re.escape(entry)}\s*\(", code, re.M):
        start = prompt.rfind(f"def {entry}(")
        body = (prompt[:start] if start >= 0 else "") + "\n" + code
    else:
        body = prompt + code
    return f"{body}\n\n{problem['test']}\n\ncheck({entry})\n"


def run_programs(programs: list[str], set_name: str, seconds: int = SECONDS) -> list[dict]:
    """Run each program in one sandbox, WORKERS at a time. Per program {"passed", "status", "error"}."""
    box = pipeline.make_box(set_name, None, None, [], Path(__file__).resolve().parent)
    try:
        def one(numbered: tuple[int, str]) -> dict:
            number, text = numbered
            path = box.scratch / f"program_{number:03d}.py"
            path.write_text(text, encoding="utf-8")
            try:
                done = subprocess.run(box.command(path.name), capture_output=True, text=True, timeout=seconds, env=box.clean_env, cwd=box.scratch,
                                      stdin=subprocess.DEVNULL)
            except subprocess.TimeoutExpired:
                return {"passed": False, "status": "timeout", "error": f"more than {seconds} s"}
            lines = done.stderr.strip().splitlines()
            if done.returncode == 0:
                return {"passed": True, "status": "passed", "error": ""}
            return {"passed": False, "status": "failed" if any(line.startswith("AssertionError") for line in lines) else "error", "error": (lines or [""])[-1][:200]}

        with ThreadPoolExecutor(WORKERS) as pool:
            return list(pool.map(one, enumerate(programs)))
    finally:
        drop_box(set_name)


async def replies(items: list[dict], model: str, base_url: str, key: str, concurrency: int) -> list[str]:
    client = AsyncOpenAI(base_url=base_url, api_key=key, timeout=300, max_retries=2)
    limit = asyncio.Semaphore(concurrency)

    async def one(problem: dict) -> str:
        async with limit:
            response = await client.chat.completions.create(model=model, messages=[{"role": "user", "content": ASK.format(prompt=problem["prompt"])}], temperature=0,
                                                            max_tokens=1024, extra_body={"chat_template_kwargs": {"enable_thinking": False}})
            return response.choices[0].message.content or ""

    return await asyncio.gather(*(one(p) for p in items))


def report(model: str, results: list[dict]) -> str:
    right = sum(r["passed"] for r in results)
    statuses = {s: sum(r["status"] == s for r in results) for s in ("passed", "failed", "error", "timeout")}
    return "\n".join([f"# HumanEval: `{model}`", "", f"{len(results)} problems, one answer each at temperature 0 (pass@1). Right: {right} ({right / max(len(results), 1):.0%}).", "",
                      "| Status | Problems |", "| --- | --- |", *(f"| {s} | {n} |" for s, n in statuses.items()), "",
                      "failed = a test assertion failed; error = the program raised something else (also a syntax error); timeout = more than "
                      f"{SECONDS} s.", ""])


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("--model", required=True, help="the model that answers, as the server names it")
    parser.add_argument("--base-url", required=True)
    parser.add_argument("--concurrency", type=int, default=16)
    parser.add_argument("--limit", type=int, help="only the first N problems (for a smoke test)")
    args = parser.parse_args()
    out = OUT / f"{re.sub(r'[^A-Za-z0-9._-]+', '-', args.model)}{f'-first{args.limit}' if args.limit else ''}.jsonl"  # a smoke test never stands for the model
    if out.is_file():
        print(f"{out.relative_to(REPO_ROOT)} is saved; delete it to run again")
    else:
        items = problems()[: args.limit]
        key = os.environ.get("OPENAI_API_KEY") or API_KEY_FILE.read_text().strip()
        texts = asyncio.run(replies(items, args.model, args.base_url, key, args.concurrency))
        ran = run_programs([program(p, code_of(t)) for p, t in zip(items, texts)], f"humaneval-{os.getpid()}")  # the key never reaches the sandbox
        OUT.mkdir(parents=True, exist_ok=True)
        out.write_text("".join(json.dumps({"task_id": p["task_id"], **r, "reply": t}) + "\n" for p, t, r in zip(items, texts, ran)), encoding="utf-8")
    results = [json.loads(line) for line in out.read_text(encoding="utf-8").splitlines()]
    (OUT / f"report-{out.stem}.md").write_text(report(args.model, results), encoding="utf-8")
    print(f"{args.model}: {sum(r['passed'] for r in results)} of {len(results)} -> {out.relative_to(REPO_ROOT)}")


if __name__ == "__main__":
    main()
