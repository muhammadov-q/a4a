# Tools against no tools, on each library's own documentation questions (bench2)

A tool call that the model wrote as text is run as a call, and the Python tool's output is shown as text.

Model `qwen3-1.7b`. 7 repositories with every condition, 120 questions, 3 runs each. Right answers: no tools 32.7 (27%) (32, 33, 33); one python tool 42.0 (35%) (44, 41, 41).

A cell is the number of right answers: the mean of the runs, then each run in brackets.

| Package | Questions | Tools accepted | No tools | One Python tool |
| --- | --- | --- | --- | --- |
| `dateutil` | 11 | 1 of 1 | 1.0 (1, 1, 1) | 2.3 (3, 2, 2) |
| `mcp` | 15 | 0 of 54 | none | none |
| `more_itertools` | 19 | 25 of 59 | 5.3 (5, 5, 6) | 7.3 (8, 7, 7) |
| `networkx` | 20 | 3 of 45 | 1.3 (1, 2, 1) | 6.7 (7, 6, 7) |
| `jinja2` | 9 | 11 of 58 | 5.0 (5, 5, 5) | 4.0 (4, 4, 4) |
| `werkzeug` | 16 | 26 of 60 | 3.0 (3, 3, 3) | 5.0 (5, 5, 5) |
| `packaging` | 28 | 41 of 60 | 15.0 (15, 15, 15) | 6.7 (7, 7, 6) |
| `rsa` | 17 | 11 of 24 | 2.0 (2, 2, 2) | 10.0 (10, 10, 10) |
| **7 repositories with every condition** | **120** | | **32.7 (27%) (32, 33, 33)** | **42.0 (35%) (44, 41, 41)** |

## How the tools were used

Means over the runs.

| Package | Condition | Questions with a tool call | Right among those | Tool calls | Calls that gave an error | Calls written as text, and run |
| --- | --- | --- | --- | --- | --- | --- |
| `dateutil` | one python tool | 10.3 of 11 | 2.3 | 183.0 | 179.0 | 96.3 |
| `more_itertools` | one python tool | 19.0 of 19 | 7.3 | 118.7 | 107.7 | 24.0 |
| `networkx` | one python tool | 19.7 of 20 | 6.7 | 318.0 | 302.7 | 127.7 |
| `jinja2` | one python tool | 9.0 of 9 | 4.0 | 57.7 | 51.7 | 2.7 |
| `werkzeug` | one python tool | 16.0 of 16 | 5.0 | 147.7 | 143.3 | 72.7 |
| `packaging` | one python tool | 27.7 of 28 | 6.7 | 363.7 | 348.0 | 156.3 |
| `rsa` | one python tool | 16.0 of 17 | 10.0 | 111.0 | 99.7 | 60.7 |

## By kind of answer

First run. A true-or-false question can be answered right by guessing half of the time.

| The answer is | Questions | No tools | One Python tool |
| --- | --- | --- | --- |
| true or false | 44 | 26 (59%) | 16 (36%) |
| another value | 76 | 6 (8%) | 28 (37%) |

## Question by question

First run. p is the exact two-sided sign test on the questions that only one of the two got right.

| A | B | Only A right | Only B right | p |
| --- | --- | --- | --- | --- |
| no tools | one python tool | 17 | 29 | 0.1 |
