# Tools against no tools, on the questions about each database; a row is a database (db1)

A tool call that the model wrote as text is run as a call, and the Python tool's output is shown as text.

Model `qwen3-4b-rec4-f3`. 1 repositories with every condition, 39 questions, 3 runs each. Right answers: no tools 6.0 (15%) (6, 6, 6); one sql tool 39.0 (100%) (39, 39, 39).

A cell is the number of right answers: the mean of the runs, then each run in brackets.

| Package | Questions | Tools accepted | No tools | One SQL tool |
| --- | --- | --- | --- | --- |
| `chinook` | 40 | none | none | none |
| `northwind` | 39 | none | 6.0 (6, 6, 6) | 39.0 (39, 39, 39) |
| `sakila` | 39 | none | none | none |
| **1 repositories with every condition** | **39** | | **6.0 (15%) (6, 6, 6)** | **39.0 (100%) (39, 39, 39)** |

## How the tools were used

Means over the runs.

| Package | Condition | Questions with a tool call | Right among those | Tool calls | Calls that gave an error | Calls written as text, and run |
| --- | --- | --- | --- | --- | --- | --- |
| `northwind` | one sql tool | 39.0 of 39 | 39.0 | 43.0 | 4.0 | 0.0 |

## By kind of answer

First run. A true-or-false question can be answered right by guessing half of the time.

| The answer is | Questions | No tools | One SQL tool |
| --- | --- | --- | --- |
| true or false | 0 | none | none |
| another value | 39 | 6 (15%) | 39 (100%) |

## Question by question

First run. p is the exact two-sided sign test on the questions that only one of the two got right.

| A | B | Only A right | Only B right | p |
| --- | --- | --- | --- | --- |
| no tools | one sql tool | 0 | 33 | 2.3e-10 |
