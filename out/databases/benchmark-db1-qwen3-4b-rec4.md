# Tools against no tools, on the questions about each database; a row is a database (db1)

A tool call that the model wrote as text is run as a call, and the Python tool's output is shown as text.

Model `qwen3-4b-rec4`. 1 repositories with every condition, 40 questions, 3 runs each. Right answers: no tools 2.0 (5%) (2, 2, 2); one sql tool 38.3 (96%) (38, 39, 38).

A cell is the number of right answers: the mean of the runs, then each run in brackets.

| Package | Questions | Tools accepted | No tools | One SQL tool |
| --- | --- | --- | --- | --- |
| `chinook` | 40 | none | 2.0 (2, 2, 2) | 38.3 (38, 39, 38) |
| `northwind` | 39 | none | none | none |
| `sakila` | 39 | none | none | none |
| **1 repositories with every condition** | **40** | | **2.0 (5%) (2, 2, 2)** | **38.3 (96%) (38, 39, 38)** |

## How the tools were used

Means over the runs.

| Package | Condition | Questions with a tool call | Right among those | Tool calls | Calls that gave an error | Calls written as text, and run |
| --- | --- | --- | --- | --- | --- | --- |
| `chinook` | one sql tool | 40.0 of 40 | 38.3 | 52.7 | 14.0 | 0.0 |

## By kind of answer

First run. A true-or-false question can be answered right by guessing half of the time.

| The answer is | Questions | No tools | One SQL tool |
| --- | --- | --- | --- |
| true or false | 0 | none | none |
| another value | 40 | 2 (5%) | 38 (95%) |

## Question by question

First run. p is the exact two-sided sign test on the questions that only one of the two got right.

| A | B | Only A right | Only B right | p |
| --- | --- | --- | --- | --- |
| no tools | one sql tool | 0 | 36 | 2.9e-11 |
