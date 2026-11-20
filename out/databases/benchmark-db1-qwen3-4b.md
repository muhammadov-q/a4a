# Tools against no tools, on the questions about each database; a row is a database (db1)

A tool call that the model wrote as text is run as a call, and the Python tool's output is shown as text.

Model `qwen3-4b`. 3 repositories with every condition, 118 questions, 3 runs each. Right answers: no tools 16.3 (14%) (16, 16, 17); one sql tool 97.3 (82%) (97, 97, 98).

A cell is the number of right answers: the mean of the runs, then each run in brackets.

| Package | Questions | Tools accepted | No tools | One SQL tool |
| --- | --- | --- | --- | --- |
| `chinook` | 40 | none | 3.0 (3, 3, 3) | 31.0 (31, 31, 31) |
| `northwind` | 39 | none | 4.3 (4, 4, 5) | 34.3 (34, 34, 35) |
| `sakila` | 39 | none | 9.0 (9, 9, 9) | 32.0 (32, 32, 32) |
| **3 repositories with every condition** | **118** | | **16.3 (14%) (16, 16, 17)** | **97.3 (82%) (97, 97, 98)** |

## How the tools were used

Means over the runs.

| Package | Condition | Questions with a tool call | Right among those | Tool calls | Calls that gave an error | Calls written as text, and run |
| --- | --- | --- | --- | --- | --- | --- |
| `chinook` | one sql tool | 40.0 of 40 | 31.0 | 60.7 | 22.7 | 10.3 |
| `northwind` | one sql tool | 39.0 of 39 | 34.3 | 40.0 | 2.0 | 0.0 |
| `sakila` | one sql tool | 39.0 of 39 | 32.0 | 39.0 | 0.0 | 0.0 |

## By kind of answer

First run. A true-or-false question can be answered right by guessing half of the time.

| The answer is | Questions | No tools | One SQL tool |
| --- | --- | --- | --- |
| true or false | 0 | none | none |
| another value | 118 | 16 (14%) | 97 (82%) |

## Question by question

First run. p is the exact two-sided sign test on the questions that only one of the two got right.

| A | B | Only A right | Only B right | p |
| --- | --- | --- | --- | --- |
| no tools | one sql tool | 0 | 81 | 8.3e-25 |
