# Tools against no tools, on the questions about each database; a row is a database (db1)

A tool call that the model wrote as text is run as a call, and the Python tool's output is shown as text.

Model `qwen3-4b-sft1-f3`. 1 repositories with every condition, 39 questions, 3 runs each. Right answers: no tools 5.0 (13%) (5, 5, 5); one sql tool 37.0 (95%) (37, 37, 37).

A cell is the number of right answers: the mean of the runs, then each run in brackets.

| Package | Questions | Tools accepted | No tools | One SQL tool |
| --- | --- | --- | --- | --- |
| `chinook` | 40 | none | none | none |
| `northwind` | 39 | none | 5.0 (5, 5, 5) | 37.0 (37, 37, 37) |
| `sakila` | 39 | none | none | none |
| **1 repositories with every condition** | **39** | | **5.0 (13%) (5, 5, 5)** | **37.0 (95%) (37, 37, 37)** |

## How the tools were used

Means over the runs.

| Package | Condition | Questions with a tool call | Right among those | Tool calls | Calls that gave an error | Calls written as text, and run |
| --- | --- | --- | --- | --- | --- | --- |
| `northwind` | one sql tool | 39.0 of 39 | 37.0 | 117.0 | 80.0 | 0.0 |

## By kind of answer

First run. A true-or-false question can be answered right by guessing half of the time.

| The answer is | Questions | No tools | One SQL tool |
| --- | --- | --- | --- |
| true or false | 0 | none | none |
| another value | 39 | 5 (13%) | 37 (95%) |

## Question by question

First run. p is the exact two-sided sign test on the questions that only one of the two got right.

| A | B | Only A right | Only B right | p |
| --- | --- | --- | --- | --- |
| no tools | one sql tool | 0 | 32 | 4.7e-10 |
