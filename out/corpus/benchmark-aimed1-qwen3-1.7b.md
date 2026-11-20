# Tools against no tools, on the questions of out/corpus/tasks-aimed/ (aimed1)

A tool call that the model wrote as text is run as a call, and the Python tool's output is shown as text.

Model `qwen3-1.7b`. 7 repositories with every condition, 62 questions, 3 runs each. Right answers: no tools 11.0 (18%) (11, 11, 11); one python tool 20.7 (33%) (20, 21, 21).

A cell is the number of right answers: the mean of the runs, then each run in brackets.

| Package | Questions | Tools accepted | No tools | One Python tool |
| --- | --- | --- | --- | --- |
| `dateutil` | 14 | none | 7.0 (7, 7, 7) | 8.7 (8, 9, 9) |
| `mcp` | 4 | none | none | none |
| `more_itertools` | 5 | none | 0.0 (0, 0, 0) | 1.0 (1, 1, 1) |
| `networkx` | 14 | none | 2.0 (2, 2, 2) | 5.0 (5, 5, 5) |
| `jinja2` | 3 | none | 1.0 (1, 1, 1) | 0.0 (0, 0, 0) |
| `werkzeug` | 13 | none | 0.0 (0, 0, 0) | 3.0 (3, 3, 3) |
| `packaging` | 10 | none | 1.0 (1, 1, 1) | 2.0 (2, 2, 2) |
| `rsa` | 3 | none | 0.0 (0, 0, 0) | 1.0 (1, 1, 1) |
| **7 repositories with every condition** | **62** | | **11.0 (18%) (11, 11, 11)** | **20.7 (33%) (20, 21, 21)** |

## How the tools were used

Means over the runs.

| Package | Condition | Questions with a tool call | Right among those | Tool calls | Calls that gave an error | Calls written as text, and run |
| --- | --- | --- | --- | --- | --- | --- |
| `dateutil` | one python tool | 14.0 of 14 | 8.7 | 80.3 | 71.7 | 38.0 |
| `more_itertools` | one python tool | 5.0 of 5 | 1.0 | 23.0 | 20.0 | 2.0 |
| `networkx` | one python tool | 14.0 of 14 | 5.0 | 107.7 | 98.7 | 40.3 |
| `jinja2` | one python tool | 3.0 of 3 | 0.0 | 35.7 | 35.7 | 18.7 |
| `werkzeug` | one python tool | 13.0 of 13 | 3.0 | 141.3 | 136.3 | 35.3 |
| `packaging` | one python tool | 10.0 of 10 | 2.0 | 36.3 | 31.3 | 5.7 |
| `rsa` | one python tool | 3.0 of 3 | 1.0 | 52.0 | 52.0 | 0.0 |

## By kind of answer

First run. A true-or-false question can be answered right by guessing half of the time.

| The answer is | Questions | No tools | One Python tool |
| --- | --- | --- | --- |
| true or false | 9 | 6 (67%) | 1 (11%) |
| another value | 53 | 5 (9%) | 19 (36%) |

## Question by question

First run. p is the exact two-sided sign test on the questions that only one of the two got right.

| A | B | Only A right | Only B right | p |
| --- | --- | --- | --- | --- |
| no tools | one python tool | 8 | 17 | 0.11 |
