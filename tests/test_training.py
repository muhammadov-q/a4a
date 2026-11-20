import json

from a4a.evaluation.run_model import REMINDER
from a4a.training import compare as compare_module
from a4a.training.compare import compare, stuck
from a4a.training.data import examples_of, split_sources, teacher_runs

TOOLS = [{"type": "function", "function": {"name": "run_python", "description": "Run Python.", "parameters": {"type": "object", "properties": {"code": {"type": "string"}}}}}]
SYSTEM, USER = {"role": "system", "content": "You solve tasks."}, {"role": "user", "content": "What is 1 + 1?"}


def call(code: str, i: int) -> dict:
    return {"role": "assistant", "content": "", "tool_calls": [{"id": f"c{i}", "type": "function", "function": {"name": "run_python", "arguments": json.dumps({"code": code})}}]}


def trace(passed: bool = True, reminded: bool = False) -> dict:
    """A run of three requests: a call written as text that fails, a call that works, and the answer."""
    first, second = call("1/0", 0), call("1 + 1", 1)
    history = [SYSTEM, USER, first, {"role": "tool", "tool_call_id": "c0", "content": "Error executing tool run_python: ZeroDivisionError"}]
    later = [*history, second, {"role": "tool", "tool_call_id": "c1", "content": "2"}] + ([{"role": "assistant", "content": "two"}, {"role": "user", "content": REMINDER}] if reminded else [])
    requests = [{"messages": [SYSTEM, USER], "tool_list_id": "t", "response": {"role": "assistant", "content": '{"name": "run_python", "arguments": {"code": "1/0"}}'}},
                {"messages": history, "tool_list_id": "t", "response": {**second, "refusal": None}},
                {"messages": later, "tool_list_id": "t", "response": {"role": "assistant", "content": "<think>easy</think>\n2"}}]
    return {"task_id": "q1", "tool_lists": {"t": TOOLS}, "requests": requests, "outcome": {"passed": passed}}


def test_every_step_of_a_passed_run_is_an_example_and_a_call_written_as_text_is_learned_as_a_real_call():
    found, why = examples_of(trace())
    assert why == "" and [e["step"] for e in found] == [0, 1, 2] and all(e["tools"] == TOOLS and e["steps"] == 3 for e in found)
    assert found[0]["target"]["tool_calls"][0]["function"]["arguments"] == json.dumps({"code": "1/0"}) and found[0]["target"]["content"] == ""
    assert [e["failed"] for e in found] == [True, False, False]  # the first call came back as an error; the later steps still show it
    assert found[1]["messages"][-1]["content"].startswith("Error") and "refusal" not in found[1]["target"]
    assert found[2]["target"] == {"role": "assistant", "content": "2"}  # reasoning left in the text is dropped, as the harness does


def test_a_run_with_a_wrong_answer_or_the_reminder_gives_no_example():
    assert examples_of(trace(passed=False)) == ([], "runs with a wrong answer")
    assert examples_of(trace(reminded=True)) == ([], "runs that needed the reminder")


def test_the_split_keeps_a_share_of_each_kind_for_the_test_and_is_repeatable():
    sources = {**{f"repo{i}": "repository" for i in range(7)}, **{f"db{i}": "database" for i in range(3)}}
    split = split_sources(sources, 0.3, seed=1)
    assert split == split_sources(sources, 0.3, seed=1)
    assert sorted(split["test"] + split["train"]) == sorted(sources) and not set(split["test"]) & set(split["train"])
    assert sum(sources[s] == "repository" for s in split["test"]) == 2 and sum(sources[s] == "database" for s in split["test"]) == 1


def test_with_folds_every_source_is_tested_once_and_fold_1_is_the_plain_split():
    sources = {**{f"repo{i}": "repository" for i in range(7)}, **{f"db{i}": "database" for i in range(3)}}
    folds = [split_sources(sources, 0.3, seed=1, folds=3, fold=f) for f in (1, 2, 3)]
    assert folds[0] == split_sources(sources, 0.3, seed=1)
    assert sorted(s for fold in folds for s in fold["test"]) == sorted(sources)
    assert all(sum(sources[s] == "database" for s in fold["test"]) == 1 for fold in folds)


def test_only_the_teachers_runs_with_one_tool_and_the_repairing_harness_are_read(tmp_path):
    for name in ("qwen3-32b-tools-bench2-pypa__packaging-python-repair-r2", "qwen3-8b-tools-db1-chinook-sql-repair", "qwen3-8b-tools-bench2-pypa__packaging-python",
                 "qwen3-8b-none-bench2-pypa__packaging", "qwen3-1.7b-tools-bench2-pypa__packaging-python-repair", "qwen3-8b-tools-other1-pypa__packaging-python-repair"):
        (tmp_path / f"{name}.jsonl.gz").write_bytes(b"")
    found = [(stem, kind, set_name, model) for stem, kind, set_name, model, _ in teacher_runs(["qwen3-32b", "qwen3-8b"], ["bench2", "db1"], tmp_path)]
    assert found == [("pypa__packaging", "repository", "bench2", "qwen3-32b"), ("chinook", "database", "db1", "qwen3-8b")]


def test_the_comparison_adds_up_the_test_sources_and_pairs_the_questions_of_the_first_run(monkeypatch):
    def answers(passed: list[bool], calls: int = 1) -> list[dict]:
        return [{"id": f"q{i}", "passed": ok, "tool_calls": calls, "finish": "answered"} for i, ok in enumerate(passed)]

    saved = {("base", "python", "bench2", "a"): [answers([True, False, False]), answers([True, True, False])],
             ("trained", "python", "bench2", "a"): [answers([True, True, True]), answers([True, True, True])],
             ("base", "python", "bench2", "b"): [answers([False])], ("trained", "python", "bench2", "b"): [answers([True]), answers([True])]}
    monkeypatch.setattr(compare_module, "saved_runs", lambda model, condition, tag, stem: saved.get((model, condition, tag, stem), []))
    test = {"a": {"kind": "repository", "questions": {"tasks": 3, "tasks-aimed": 2}}, "b": {"kind": "repository", "questions": {"tasks": 1}}}
    [row] = compare(test, "base", "trained")  # the aimed questions and the runs without a tool have no runs, so no row
    assert (row["questions_set"], row["condition"], row["questions"], row["sources"]) == ("Documentation questions", "python", 4, ["a", "b"])
    assert row["right"] == {"base": [1], "trained": [4]}  # one run: source b has only one run of the base model
    assert (row["only_base"], row["only_trained"]) == (0, 3) and row["habits"]["trained"]["called_the_tool"] == 1.0


def test_a_model_is_stuck_when_it_sends_the_same_call_three_times_in_a_row():
    same, other = {"tool": "run_python", "arguments": "{\"code\": \"1/0\"}"}, {"tool": "run_python", "arguments": "{\"code\": \"1\"}"}
    assert stuck({"trace": [other, same, same, same]}) and not stuck({"trace": [same, same, other, same]}) and not stuck({})
