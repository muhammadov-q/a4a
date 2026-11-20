# Tools against no tools, on the questions about each database; a row is a database (db1v1)

A tool call that the model wrote as text is run as a call, and the Python tool's output is shown as text.

Model `qwen3-32b`. 3 repositories with every condition, 116 questions, 1 run each. Right answers: no tools 12 (10%); one sql tool 108 (93%).

A cell is the number of right answers: the mean of the runs, then each run in brackets.

| Package | Questions | Tools accepted | No tools | One SQL tool |
| --- | --- | --- | --- | --- |
| `chinook` | 39 | none | 2 | 33 |
| `northwind` | 39 | none | 8 | 39 |
| `sakila` | 38 | none | 2 | 36 |
| **3 repositories with every condition** | **116** | | **12 (10%)** | **108 (93%)** |

## How the tools were used

Means over the runs.

| Package | Condition | Questions with a tool call | Right among those | Tool calls | Calls that gave an error | Calls written as text, and run |
| --- | --- | --- | --- | --- | --- | --- |
| `chinook` | one sql tool | 39.0 of 39 | 33.0 | 39.0 | 6.0 | 0.0 |
| `northwind` | one sql tool | 39.0 of 39 | 39.0 | 41.0 | 1.0 | 0.0 |
| `sakila` | one sql tool | 38.0 of 38 | 36.0 | 38.0 | 0.0 | 0.0 |

## By kind of answer

First run. A true-or-false question can be answered right by guessing half of the time.

| The answer is | Questions | No tools | One SQL tool |
| --- | --- | --- | --- |
| true or false | 0 | none | none |
| another value | 116 | 12 (10%) | 108 (93%) |

## Question by question

First run. p is the exact two-sided sign test on the questions that only one of the two got right.

| A | B | Only A right | Only B right | p |
| --- | --- | --- | --- | --- |
| no tools | one sql tool | 1 | 97 | 6.2e-28 |
