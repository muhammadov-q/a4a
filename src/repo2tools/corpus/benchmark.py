"""Do generated tools help a model answer questions about the library they were made from?

    uv run repo2tools corpus-benchmark --writer-base-url http://127.0.0.1:18000/v1 --writer-model qwen3-coder \\
        --base-url http://127.0.0.1:18001/v1 --model qwen3-8b --tag small-r1
    uv run repo2tools corpus-benchmark --tag small-r1 --report-only

For every repository that has at least `--min-tasks` questions in out/corpus/tasks/ (`repo2tools corpus-tasks`):

  1. generate a tool set from the repository at the scanned commit (`repo2tools generate --follow-reexports
     --classes`, one tool per function: the small level),
  2. let the model answer the repository's questions without tools,
  3. let it answer them with the generated tools,
  4. delete the tool set's environment.

Both runs use the same instruction, one reminder if the reply is not a bare value, and the same cap on tool
output. The report is built from the saved runs in out/runs/, so `--report-only` gives it again at any time.

Writes out/corpus/benchmark-<tag>.json and benchmark-<tag>.md.
"""

import argparse
import json
import os
import re
import shutil
import subprocess
import sys
import time
from pathlib import Path

from repo2tools.corpus.scan import OUT
from repo2tools.paths import API_KEY_FILE, REPO_ROOT
from repo2tools.synthesis.pipeline import repo_name


def repositories(min_tasks: int) -> list[dict]:
    """The repositories with enough questions: {"stem", "package", "url", "tasks", "set"-less}."""
    found = []
    for path in sorted((OUT / "tasks").glob("*.jsonl")):
        tasks = [json.loads(line) for line in path.read_text().splitlines()]
        if len(tasks) >= min_tasks:
            found.append({"stem": path.stem, "path": path, "package": tasks[0]["kind"], "url": "https://github.com/" + tasks[0]["source_repo"].split("@")[0], "tasks": len(tasks)})
    return found


def run_file(model: str, mode: str, tag: str, stem: str) -> Path:
    return REPO_ROOT / "out" / "runs" / f"{model}-{mode}-{tag}-{stem}.jsonl"


def summarize(repos: list[dict], model: str, tag: str) -> list[dict]:
    """One row per repository from the saved runs: questions, tools, and right answers without and with tools."""
    rows = []
    for repo in repos:
        row = {"package": repo["package"], "repo": repo["url"], "questions": repo["tasks"], "tools_picked": None, "tools_accepted": None}
        report = REPO_ROOT / "out" / "generated" / f"{repo_name(repo['url'])}-{tag}" / "report.json"
        if report.is_file():
            generated = json.loads(report.read_text())
            row |= {"tools_picked": len(generated["tools"]), "tools_accepted": generated["accepted"]}
        for mode in ("none", "tools"):
            path = run_file(model, mode, tag, repo["stem"])
            runs = [json.loads(line) for line in path.read_text().splitlines()] if path.is_file() else None
            row[mode] = sum(r["passed"] for r in runs) if runs is not None else None
            if mode == "tools" and runs is not None:
                called = [r for r in runs if r.get("tool_calls")]
                row |= {"called_a_tool": len(called), "right_when_called": sum(r["passed"] for r in called), "tool_errors": sum(r.get("tool_errors", 0) for r in runs)}
        rows.append(row)
    return rows


def report(rows: list[dict], model: str, tag: str) -> str:
    both = [r for r in rows if r["none"] is not None and r["tools"] is not None]
    questions, none, tools = sum(r["questions"] for r in both), sum(r["none"] for r in both), sum(r["tools"] for r in both)
    show = lambda v: "none" if v is None else str(v)  # noqa: E731
    lines = [f"# Generated tools against no tools, on each library's own documentation questions ({tag})", "",
             f"Model `{model}`. {len(both)} repositories with both runs, {questions} questions: {none} right without tools ({none / max(questions, 1):.0%}), "
             f"{tools} right with the generated tools ({tools / max(questions, 1):.0%}). One run each.", "",
             "| Package | Questions | Tools picked | Tools accepted | Right without tools | Right with tools | Called a tool | Right when it called | Tool errors |",
             "| --- | --- | --- | --- | --- | --- | --- | --- | --- |"]
    lines += [f"| `{r['package']}` | {r['questions']} | {show(r['tools_picked'])} | {show(r['tools_accepted'])} | {show(r['none'])} | {show(r['tools'])} | "
              f"{show(r.get('called_a_tool'))} | {show(r.get('right_when_called'))} | {show(r.get('tool_errors'))} |" for r in rows]
    return "\n".join(lines) + "\n"


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("--tag", required=True, help="names this run: tool sets <repository>-<tag>, runs <model>-<mode>-<tag>-<repository>")
    parser.add_argument("--model", default="qwen3-8b", help="the model that answers")
    parser.add_argument("--base-url")
    parser.add_argument("--writer-model", help="the model that writes the tools")
    parser.add_argument("--writer-base-url")
    parser.add_argument("--min-tasks", type=int, default=8)
    parser.add_argument("--max-tools", type=int, default=60)
    parser.add_argument("--report-only", action="store_true", help="only build the report from the saved runs")
    args = parser.parse_args()
    repos = repositories(args.min_tasks)
    if not args.report_only:
        if not (args.base_url and args.writer_base_url and args.writer_model):
            parser.error("give --base-url, --writer-base-url and --writer-model, or --report-only")
        commits = {r["repo"]: r["commit"] for r in json.loads((OUT / "static.json").read_text())["repositories"] if not r["error"]}
        env = {**os.environ, "OPENAI_API_KEY": os.environ.get("OPENAI_API_KEY") or API_KEY_FILE.read_text().strip()}
        for repo in repos:
            started = time.monotonic()
            set_name = f"{repo_name(repo['url'])}-{args.tag}"
            subprocess.run([sys.executable, "-m", "repo2tools.cli", "generate", repo["url"], "--commit", commits[repo["url"]], "--base-url", args.writer_base_url,
                            "--model", args.writer_model, "--max-tools", str(args.max_tools), "--follow-reexports", "--classes", "--tag", args.tag],
                           env=env, cwd=REPO_ROOT, capture_output=True)
            accepted = (REPO_ROOT / "toolsets" / "generated" / set_name / "run_server.sh").is_file()
            for mode in ("none", "tools") if accepted else ("none",):
                command = [sys.executable, "-m", "repo2tools.cli", "run-model", str(repo["path"]), "--mode", mode, "--base-url", args.base_url, "--model", args.model,
                           "--topic", f"the Python library {repo['package']}", "--remind", "--tag", f"{args.tag}-{repo['stem']}"]
                subprocess.run(command + (["--", f"toolsets/generated/{set_name}/run_server.sh"] if mode == "tools" else []), env=env, cwd=REPO_ROOT, capture_output=True)
            for leftover in (set_name, f"{set_name}.tmp"):
                shutil.rmtree(REPO_ROOT / ".cache" / "envs" / leftover, ignore_errors=True)
            (REPO_ROOT / ".cache" / "envs" / f"{set_name}.sb").unlink(missing_ok=True)
            print(f"{repo['package']}: done in {time.monotonic() - started:.0f} s", flush=True)
    rows = summarize(repos, args.model, args.tag)
    safe = re.sub(r"[^A-Za-z0-9._-]+", "-", args.tag)
    (OUT / f"benchmark-{safe}.json").write_text(json.dumps({"model": args.model, "tag": args.tag, "min_tasks": args.min_tasks, "repositories": rows}, indent=1) + "\n", encoding="utf-8")
    (OUT / f"benchmark-{safe}.md").write_text(report(rows, args.model, args.tag), encoding="utf-8")
    print(f"-> out/corpus/benchmark-{safe}.md")


if __name__ == "__main__":
    main()
