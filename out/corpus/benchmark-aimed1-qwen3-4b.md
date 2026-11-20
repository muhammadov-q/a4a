# Tools against no tools, on the questions of out/corpus/tasks-aimed/ (aimed1)

A tool call that the model wrote as text is run as a call, and the Python tool's output is shown as text.

Model `qwen3-4b`. 7 repositories with every condition, 62 questions, 3 runs each. Right answers: no tools 23.0 (37%) (23, 23, 23); one python tool 32.3 (52%) (33, 33, 31).

A cell is the number of right answers: the mean of the runs, then each run in brackets.

| Package | Questions | Tools accepted | No tools | One Python tool |
| --- | --- | --- | --- | --- |
| `dateutil` | 14 | none | 8.0 (8, 8, 8) | 7.3 (7, 8, 7) |
| `mcp` | 4 | none | none | none |
| `more_itertools` | 5 | none | 2.0 (2, 2, 2) | 3.0 (3, 3, 3) |
| `networkx` | 14 | none | 5.0 (5, 5, 5) | 8.7 (9, 9, 8) |
| `jinja2` | 3 | none | 1.0 (1, 1, 1) | 0.0 (0, 0, 0) |
| `werkzeug` | 13 | none | 3.0 (3, 3, 3) | 6.0 (6, 6, 6) |
| `packaging` | 10 | none | 3.0 (3, 3, 3) | 6.0 (6, 6, 6) |
| `rsa` | 3 | none | 1.0 (1, 1, 1) | 1.3 (2, 1, 1) |
| **7 repositories with every condition** | **62** | | **23.0 (37%) (23, 23, 23)** | **32.3 (52%) (33, 33, 31)** |

## How the tools were used

Means over the runs.

| Package | Condition | Questions with a tool call | Right among those | Tool calls | Calls that gave an error | Calls written as text, and run |
| --- | --- | --- | --- | --- | --- | --- |
| `dateutil` | one python tool | 13.0 of 14 | 7.3 | 171.3 | 164.7 | 33.0 |
| `more_itertools` | one python tool | 5.0 of 5 | 3.0 | 23.7 | 20.3 | 2.3 |
| `networkx` | one python tool | 14.0 of 14 | 8.7 | 27.7 | 16.7 | 0.0 |
| `jinja2` | one python tool | 3.0 of 3 | 0.0 | 7.0 | 6.0 | 0.0 |
| `werkzeug` | one python tool | 13.0 of 13 | 6.0 | 34.3 | 25.3 | 0.0 |
| `packaging` | one python tool | 10.0 of 10 | 6.0 | 12.3 | 5.3 | 0.0 |
| `rsa` | one python tool | 3.0 of 3 | 1.3 | 55.7 | 54.7 | 19.7 |

## By kind of answer

First run. A true-or-false question can be answered right by guessing half of the time.

| The answer is | Questions | No tools | One Python tool |
| --- | --- | --- | --- |
| true or false | 9 | 6 (67%) | 3 (33%) |
| another value | 53 | 17 (32%) | 30 (57%) |

## Question by question

First run. p is the exact two-sided sign test on the questions that only one of the two got right.

| A | B | Only A right | Only B right | p |
| --- | --- | --- | --- | --- |
| no tools | one python tool | 8 | 18 | 0.076 |
