"""The `a4a` command: one entry point for every step.

    uv run a4a <command> [arguments]
    uv run a4a <command> --help

Each command is the `main()` of one module and is imported only when it is used, so `a4a --help` stays
fast and a command never needs the optional dependencies of another.
"""

import importlib
import sys

from a4a import __version__

# command -> (module, one line for --help), grouped as in the README
COMMANDS: dict[str, dict[str, tuple[str, str]]] = {
    "repo2tools: repository -> tools": {
        "generate": ("a4a.repo2tools.pipeline", "repository link -> checked tools, in their own environment and sandbox"),
        "scrape": ("a4a.repo2tools.scrape", "list a package's public API without importing it"),
        "usage": ("a4a.repo2tools.usage", "count how a repository's own docs and tests use its API"),
        "repair-chains": ("a4a.repo2tools.chain_repair", "rewrite tools whose output no other tool accepts"),
        "usability": ("a4a.repo2tools.usability", "let a small model try each tool; rewrite unclear names and descriptions"),
    },
    "Evaluation: exercises and model runs": {
        "make-exercises": ("a4a.evaluation.packaging_exercises", "build exercises with known answers from packaging's test cases"),
        "check-tools": ("a4a.evaluation.reference_calls", "replay every known-good solution through a tool server"),
        "run-model": ("a4a.evaluation.run_model", "let a model solve the exercises, with or without tools"),
        "compare-runs": ("a4a.evaluation.compare_runs", "put two model runs side by side"),
        "handover": ("a4a.evaluation.handover", "build a self-contained zip of exercises and tools"),
    },
    "Traces": {
        "reference-traces": ("a4a.traces.reference", "known-good solutions as traces"),
        "analyze-traces": ("a4a.traces.analyze", "what repeats in traces, and what compression would save"),
    },
    "Corpus: many repositories": {
        "corpus-candidates": ("a4a.corpus.candidates", "list pure-Python PyPI packages with a GitHub repository, for a person to approve"),
        "corpus-scan": ("a4a.corpus.scan", "clone the approved repositories and scan them without running anything"),
        "corpus-saturation": ("a4a.corpus.saturation", "group similar tool candidates across repositories; do the distinct ones saturate?"),
        "corpus-exercises": ("a4a.corpus.exercises", "exercises with known answers from documentation examples, confirmed by running them in the sandbox"),
        "corpus-density": ("a4a.corpus.density", "verified exercises per 1,000 lines of each kind of source, and the share of the public API they cover"),
        "corpus-targets": ("a4a.corpus.targets", "a model writes examples for a repository in three ways: free, with the API listed, or one target per request"),
        "corpus-tasks": ("a4a.corpus.tasks", "a question in plain words for each verified example, in the format of run-model"),
        "corpus-benchmark": ("a4a.corpus.benchmark", "per repository: score a model on its questions without tools, with generated tools, and with one Python tool"),
    },
    "Databases: a database -> exercises": {
        "db-fetch": ("a4a.databases.fetch", "download the approved databases and check each file against its SHA-256"),
        "db-exercises": ("a4a.databases.exercises", "exercises from templates over a database's schema, verified by two sandboxed runs"),
    },
    "ToolGym": {
        "toolgym-types": ("a4a.toolgym.type_inference", "ToolGym types for a generated tool set, checked by running the tools"),
        "toolgym-export": ("a4a.toolgym.catalog_export", "write the hand-made tools into a ToolGym catalog"),
        "toolgym-local": ("a4a.toolgym.local", "run ToolGym's chain check and pipeline on tools served from this computer"),
        "toolgym-traces": ("a4a.toolgym.traces", "ToolGym run results as traces"),
        "toolgym-exercises": ("a4a.toolgym.exercises", "ToolGym's synthetic tasks as exercises with known answers"),
        "toolgym-chains": ("a4a.toolgym.catalog_chains", "summarise ToolGym's chain listings"),
        "toolgym-edges": ("a4a.toolgym.exercise_edges", "check that the links the exercises need are in ToolGym's graph"),
    },
}
MODULES = {name: module for group in COMMANDS.values() for name, (module, _) in group.items()}


def usage() -> str:
    lines = ["usage: a4a <command> [arguments]", "       a4a <command> --help", ""]
    for title, group in COMMANDS.items():
        lines.append(f"{title}:")
        lines += [f"  {name:<18} {text}" for name, (_, text) in group.items()]
        lines.append("")
    return "\n".join(lines)


def main(argv: list[str] | None = None) -> None:
    argv = sys.argv[1:] if argv is None else argv
    if not argv or argv[0] in ("-h", "--help"):
        print(usage())
        return
    if argv[0] == "--version":
        print(f"a4a {__version__}")
        return
    command, rest = argv[0], argv[1:]
    if command not in MODULES:
        sys.exit(f"a4a: unknown command {command!r}\n\n{usage()}")
    sys.argv = [f"a4a {command}", *rest]  # the module's own argument parser reads the rest
    importlib.import_module(MODULES[command]).main()


if __name__ == "__main__":
    main()
