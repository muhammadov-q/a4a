# Tools against no tools, on the questions about each database; a row is a database (db1)

A tool call that the model wrote as text is run as a call, and the Python tool's output is shown as text.

Model `qwen3-1.7b-sft2`. 1 repositories with every condition, 40 questions, 3 runs each. Right answers: no tools 0.0 (0%) (0, 0, 0); one sql tool 33.0 (82%) (33, 33, 33).

A cell is the number of right answers: the mean of the runs, then each run in brackets.

| Package | Questions | Tools accepted | No tools | One SQL tool |
| --- | --- | --- | --- | --- |
| `chinook` | 40 | none | 0.0 (0, 0, 0) | 33.0 (33, 33, 33) |
| `northwind` | 39 | none | none | none |
| `sakila` | 39 | none | none | none |
| **1 repositories with every condition** | **40** | | **0.0 (0%) (0, 0, 0)** | **33.0 (82%) (33, 33, 33)** |

## How the tools were used

Means over the runs.

| Package | Condition | Questions with a tool call | Right among those | Tool calls | Calls that gave an error | Calls written as text, and run |
| --- | --- | --- | --- | --- | --- | --- |
| `chinook` | one sql tool | 40.0 of 40 | 33.0 | 313.7 | 280.7 | 0.0 |

## By kind of answer

First run. A true-or-false question can be answered right by guessing half of the time.

| The answer is | Questions | No tools | One SQL tool |
| --- | --- | --- | --- |
| true or false | 0 | none | none |
| another value | 40 | 0 (0%) | 33 (82%) |

## Question by question

First run. p is the exact two-sided sign test on the questions that only one of the two got right.

| A | B | Only A right | Only B right | p |
| --- | --- | --- | --- | --- |
| no tools | one sql tool | 0 | 33 | 2.3e-10 |
