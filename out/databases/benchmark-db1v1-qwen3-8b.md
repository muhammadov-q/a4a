# Tools against no tools, on the questions about each database; a row is a database (db1v1)

A tool call that the model wrote as text is run as a call, and the Python tool's output is shown as text.

Model `qwen3-8b`. 3 repositories with every condition, 116 questions, 1 run each. Right answers: no tools 5 (4%); one sql tool 104 (90%).

A cell is the number of right answers: the mean of the runs, then each run in brackets.

| Package | Questions | Tools accepted | No tools | One SQL tool |
| --- | --- | --- | --- | --- |
| `chinook` | 39 | none | 1 | 36 |
| `northwind` | 39 | none | 2 | 35 |
| `sakila` | 38 | none | 2 | 33 |
| **3 repositories with every condition** | **116** | | **5 (4%)** | **104 (90%)** |

## How the tools were used

Means over the runs.

| Package | Condition | Questions with a tool call | Right among those | Tool calls | Calls that gave an error | Calls written as text, and run |
| --- | --- | --- | --- | --- | --- | --- |
| `chinook` | one sql tool | 39.0 of 39 | 36.0 | 47.0 | 5.0 | 0.0 |
| `northwind` | one sql tool | 39.0 of 39 | 35.0 | 41.0 | 2.0 | 0.0 |
| `sakila` | one sql tool | 38.0 of 38 | 33.0 | 38.0 | 0.0 | 0.0 |

## By kind of answer

First run. A true-or-false question can be answered right by guessing half of the time.

| The answer is | Questions | No tools | One SQL tool |
| --- | --- | --- | --- |
| true or false | 0 | none | none |
| another value | 116 | 5 (4%) | 104 (90%) |

## Question by question

First run. p is the exact two-sided sign test on the questions that only one of the two got right.

| A | B | Only A right | Only B right | p |
| --- | --- | --- | --- | --- |
| no tools | one sql tool | 0 | 99 | 3.2e-30 |
