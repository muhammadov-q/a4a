# Tools against no tools, on the questions about each database; a row is a database (db1)

A tool call that the model wrote as text is run as a call, and the Python tool's output is shown as text.

Model `qwen3-1.7b`. 3 repositories with every condition, 118 questions, 3 runs each. Right answers: no tools 2.0 (2%) (2, 2, 2); one sql tool 52.0 (44%) (51, 50, 55).

A cell is the number of right answers: the mean of the runs, then each run in brackets.

| Package | Questions | Tools accepted | No tools | One SQL tool |
| --- | --- | --- | --- | --- |
| `chinook` | 40 | none | 2.0 (2, 2, 2) | 18.0 (18, 18, 18) |
| `northwind` | 39 | none | 0.0 (0, 0, 0) | 17.0 (15, 18, 18) |
| `sakila` | 39 | none | 0.0 (0, 0, 0) | 17.0 (18, 14, 19) |
| **3 repositories with every condition** | **118** | | **2.0 (2%) (2, 2, 2)** | **52.0 (44%) (51, 50, 55)** |

## How the tools were used

Means over the runs.

| Package | Condition | Questions with a tool call | Right among those | Tool calls | Calls that gave an error | Calls written as text, and run |
| --- | --- | --- | --- | --- | --- | --- |
| `chinook` | one sql tool | 40.0 of 40 | 18.0 | 123.7 | 82.7 | 26.0 |
| `northwind` | one sql tool | 39.0 of 39 | 17.0 | 129.7 | 89.7 | 62.7 |
| `sakila` | one sql tool | 38.7 of 39 | 17.0 | 45.3 | 2.0 | 4.7 |

## By kind of answer

First run. A true-or-false question can be answered right by guessing half of the time.

| The answer is | Questions | No tools | One SQL tool |
| --- | --- | --- | --- |
| true or false | 0 | none | none |
| another value | 118 | 2 (2%) | 51 (43%) |

## Question by question

First run. p is the exact two-sided sign test on the questions that only one of the two got right.

| A | B | Only A right | Only B right | p |
| --- | --- | --- | --- | --- |
| no tools | one sql tool | 0 | 49 | 3.6e-15 |
