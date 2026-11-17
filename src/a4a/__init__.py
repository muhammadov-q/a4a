"""A4A, Anything for Agents: turn a source of information into verified exercises and tools for LLM agents, and measure whether they help.

Sub-packages:
    sources     the kinds of source, behind one interface (today: a Python repository)
    repo2tools  the first part that was built: repository link -> checked tools (API scan, usage scan, generation, sandboxed checks, repairs)
    corpus      many repositories at once: scans, exercises from documentation, questions, density, benchmark
    evaluation  exercises with known answers, reference calls, model runs
    traces      one format for agent traces, and what repeats in them
    toolgym     types, catalog folders and runs for ToolGym

Everything is used from a checkout of the repository: tool sets, results and caches live next to the code.
"""

__version__ = "0.2.0"
