"""Training data from the teachers' runs: every step of a run that got the right answer with one tool.

    uv run a4a train-data --name sft1 [--teachers qwen3-32b qwen3-8b] [--sets bench2 aimed1 db1] [--test-share 0.3] [--seed 1]
    uv run a4a train-data --name sft1-f2 --folds 3 --fold 2

`a4a corpus-benchmark` (the Python tool) and `a4a db-benchmark` (the SQL tool) save every request of a run in
out/traces/. Each request of a passed run becomes one example: the conversation so far, the tool list, and the
assistant message that came next. The student learns to write that message. It is tested later with the same
harness, so it sees the same instruction, tool description and output format as in training.

Kept: runs of the harness that repairs calls written as text (`-repair`), by one of the teachers, with the right
answer and without the reminder (its first reply was not a bare value, and would be learned). A call that the
teacher wrote as text is learned in the form the harness ran it: as a real tool call. A step whose call came
back as an error is not learned (`--keep-failed-calls` keeps it); it stays in the history of the later steps, so
what is learned there is how the teacher went on after the error. Runs at temperature 0 repeat each other, so an
example that is already there is not added again.

The sources are split first. The test sources (a share of the repositories and of the databases, chosen at
random with --seed) give no example at all, so the trained model is tested only on sources it has not seen.
With --folds 3, every source is tested in one of three folds: fold 1 is that split, and the sources it trains on
are dealt at random to folds 2 and 3. One model is trained per fold.

Writes out/training/<name>/train.jsonl (one example per line: messages, tools, target, meta), split.json
(which source is where, with the questions to test on) and report.md.
"""

import argparse
import hashlib
import json
import random
import re
from collections import Counter, defaultdict
from pathlib import Path

from a4a.evaluation.run_model import REMINDER
from a4a.paths import REPO_ROOT
from a4a.traces.format import read_traces

OUT = REPO_ROOT / "out" / "training"
TRACES = REPO_ROOT / "out" / "traces"
RUN = re.compile(r"^(?P<model>.+?)-tools-(?P<set>[a-z0-9]+)-(?P<stem>.+)-(?P<tool>python|sql)-repair(?:-r(?P<run>\d+))?\.jsonl\.gz$")
KINDS = {"python": "repository", "sql": "database"}
QUESTIONS = {"repository": [REPO_ROOT / "out" / "corpus" / "tasks", REPO_ROOT / "out" / "corpus" / "tasks-aimed"],
             "database": [REPO_ROOT / "out" / "databases" / "tasks"]}


def assistant(message: dict) -> dict:
    """An assistant message with only what a chat template reads; reasoning that stayed in the text is dropped, as the harness does."""
    found = {"role": "assistant", "content": re.sub(r"<think>.*?</think>", "", message.get("content") or "", flags=re.S).strip()}
    if message.get("tool_calls"):
        found["tool_calls"] = [{"id": call.get("id") or f"call_{i}", "type": "function",
                                "function": {"name": call["function"]["name"], "arguments": call["function"].get("arguments") or "{}"}}
                               for i, call in enumerate(message["tool_calls"])]
    return found


def cleaned(messages: list[dict]) -> list[dict]:
    return [assistant(m) if m["role"] == "assistant" else {k: m[k] for k in ("role", "content", "tool_call_id") if k in m} for m in messages]


def failed(messages: list[dict]) -> bool:
    """Whether a tool reply in these messages is an error (the harness and the MCP server both start it with "Error")."""
    return any(m["role"] == "tool" and str(m.get("content", "")).lstrip('"').startswith("Error") for m in messages)


def examples_of(trace: dict) -> tuple[list[dict], str]:
    """The examples of one run, each with `failed` if its call came back as an error, and why there are none ("" if there are)."""
    if not (trace.get("outcome") or {}).get("passed"):
        return [], "runs with a wrong answer"
    requests = trace["requests"]
    if any(m["role"] == "user" and m.get("content") == REMINDER for r in requests for m in r["messages"]):
        return [], "runs that needed the reminder"
    found = []
    for i, request in enumerate(requests):
        if i + 1 < len(requests):  # what the harness put into the history: a call written as text is there as a real call
            target = requests[i + 1]["messages"][len(request["messages"])]
            replies = requests[i + 1]["messages"][len(request["messages"]) + 1:]
        else:
            target, replies = request["response"], []
        if target.get("role") != "assistant":
            return [], "runs whose history does not match"
        tools = trace["tool_lists"].get(request["tool_list_id"]) if request["tool_list_id"] else None
        found.append({"messages": cleaned(request["messages"]), "tools": tools, "target": assistant(target), "step": i, "steps": len(requests), "failed": failed(replies)})
    return found, ""


def teacher_runs(teachers: list[str], sets: list[str], traces: Path = TRACES):
    """(source, kind, set, model, path) for every saved run of a teacher with one tool, in a stable order."""
    for path in sorted(traces.glob("*.jsonl.gz")):
        match = RUN.match(path.name)
        if match and match["model"] in teachers and match["set"] in sets:
            yield match["stem"], KINDS[match["tool"]], match["set"], match["model"], path


def split_sources(sources: dict[str, str], share: float, seed: int, folds: int = 1, fold: int = 1) -> dict[str, list[str]]:
    """The test sources: `share` of each kind, at least one, at random. The rest train.

    With `folds` > 1 every source is tested once: fold 1 is that split, and the sources it trains on are dealt at
    random, kind by kind, to folds 2 to `folds`. Fold `fold` is tested."""
    rng, parts = random.Random(seed), [[] for _ in range(folds)]
    kinds = sorted(set(sources.values()))
    for kind in kinds:
        names = sorted(s for s, k in sources.items() if k == kind)
        parts[0] += rng.sample(names, max(1, round(share * len(names))))
    for kind in kinds if folds > 1 else ():
        rest = sorted(s for s, k in sources.items() if k == kind and s not in parts[0])
        for i, name in enumerate(rng.sample(rest, len(rest))):
            parts[1 + i % (folds - 1)].append(name)
    test = parts[fold - 1]
    return {"test": sorted(test), "train": sorted(s for s in sources if s not in test)}


def questions_of(stem: str, kind: str) -> dict[str, int]:
    """The question sets of a source and how many questions each has."""
    return {folder.name: len(path.read_text(encoding="utf-8").splitlines()) for folder in QUESTIONS[kind] if (path := folder / f"{stem}.jsonl").is_file()}


def key(example: dict) -> str:
    return hashlib.sha256(json.dumps([example["messages"], example["target"]], sort_keys=True).encode()).hexdigest()


def report(name: str, args, split: dict, sources: dict, counts: dict, dropped: Counter) -> str:
    lines = [f"# Training data `{name}`", "",
             f"Teachers: {', '.join(args.teachers)}. Runs: {', '.join(args.sets)}, the harness that repairs calls. Test sources: {args.test_share:.0%} of each kind, seed {args.seed}"
             + (f"; fold {args.fold} of {args.folds}, in which every source is tested once (fold 1 is that split)." if args.folds > 1 else "."), "",
             "| Source | Kind | Split | Runs used | Questions with an example | Examples | Questions to test on |", "| --- | --- | --- | --- | --- | --- | --- |"]
    for stem in sorted(sources, key=lambda s: (sources[s], s)):
        c = counts.get(stem, {})
        side = "test" if stem in split["test"] else "train"
        to_test = ", ".join(f"{n} {folder}" for folder, n in questions_of(stem, sources[stem]).items()) if side == "test" else ""
        lines.append(f"| {stem} | {sources[stem]} | {side} | {c.get('runs', 0)} | {len(c.get('questions', ()))} | {c.get('examples', 0)} | {to_test} |")
    train = split["train"]
    lines += ["", f"**{sum(counts.get(s, {}).get('examples', 0) for s in train)} examples** from {sum(len(counts.get(s, {}).get('questions', ())) for s in train)} questions of {len(train)} sources.",
              f"Left out: {'; '.join(f'{n} {why}' for why, n in dropped.most_common()) or 'nothing'}.",
              *([] if args.keep_failed_calls else ["A step whose call failed stays in the history of the later steps of its run."]),
              "Examples that repeat an earlier one are counted once.", ""]
    return "\n".join(lines)


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("--name", required=True, help="names the data: out/training/<name>/")
    parser.add_argument("--teachers", nargs="+", default=["qwen3-32b", "qwen3-8b"], help="the models whose passed runs are learned")
    parser.add_argument("--sets", nargs="+", default=["bench2", "aimed1", "db1"], help="the benchmark tags whose runs are used")
    parser.add_argument("--test-share", type=float, default=0.3, help="share of the repositories, and of the databases, kept for the test")
    parser.add_argument("--seed", type=int, default=1)
    parser.add_argument("--folds", type=int, default=1, help="with more than 1, every source is tested in one fold; fold 1 is the split of --test-share")
    parser.add_argument("--fold", type=int, default=1, help="the fold whose sources are tested, 1 to --folds")
    parser.add_argument("--keep-failed-calls", action="store_true", help="also learn the steps whose tool call came back as an error")
    args = parser.parse_args()
    if not 1 <= args.fold <= args.folds:
        parser.error("--fold must be between 1 and --folds")

    runs = list(teacher_runs(args.teachers, args.sets))
    sources = {stem: kind for stem, kind, *_ in runs}
    if not sources:
        parser.error("no saved runs of these teachers and sets in out/traces/")
    split = split_sources(sources, args.test_share, args.seed, args.folds, args.fold)
    if not split["test"]:
        parser.error(f"fold {args.fold} has no source; use fewer folds")
    seen, examples, dropped = set(), [], Counter()
    counts = defaultdict(lambda: {"runs": 0, "questions": set(), "examples": 0})
    for stem, kind, set_name, model, path in runs:
        if stem in split["test"]:
            continue
        counts[stem]["runs"] += 1
        for trace in read_traces(path):
            found, why = examples_of(trace)
            if why:
                dropped[why] += 1
                continue
            counts[stem]["questions"].add(trace["task_id"])
            for example in found:
                if example.pop("failed") and not args.keep_failed_calls:
                    dropped["steps with a failed call"] += 1
                    continue
                if (k := key(example)) not in seen:
                    seen.add(k)
                    step, steps = example.pop("step"), example.pop("steps")
                    examples.append(example | {"meta": {"source": stem, "kind": kind, "set": set_name, "teacher": model, "task_id": trace["task_id"], "step": step, "steps": steps}})
                    counts[stem]["examples"] += 1

    folder = OUT / args.name
    folder.mkdir(parents=True, exist_ok=True)
    (folder / "train.jsonl").write_text("".join(json.dumps(e, ensure_ascii=False) + "\n" for e in examples), encoding="utf-8")
    test = {stem: {"kind": sources[stem], "questions": questions_of(stem, sources[stem])} for stem in split["test"]}
    record = {"name": args.name, "teachers": args.teachers, "sets": args.sets, "test_share": args.test_share, "seed": args.seed,
              **({"folds": args.folds, "fold": args.fold} if args.folds > 1 else {}), "keep_failed_calls": args.keep_failed_calls,
              "train": split["train"], "test": test, "examples": len(examples), "dropped": dict(dropped),
              "per_source": {s: {**c, "questions": len(c["questions"])} for s, c in counts.items()},
              "sha256": hashlib.sha256((folder / "train.jsonl").read_bytes()).hexdigest()}
    (folder / "split.json").write_text(json.dumps(record, indent=1) + "\n", encoding="utf-8")
    (folder / "report.md").write_text(report(args.name, args, split, sources, counts, dropped), encoding="utf-8")
    print(f"{len(examples)} examples from {len(split['train'])} sources; test sources: {', '.join(split['test'])} -> out/training/{args.name}/")


if __name__ == "__main__":
    main()
