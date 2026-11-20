# Tools against no tools, on the questions of out/corpus/tasks-aimed/ (aimed1, no repeated calls)

A tool call that the model wrote as text is run as a call, and the Python tool's output is shown as text. A call that is the same as an earlier call of the run is not run again; the model is told so.

Model `qwen3-1.7b`. 2 repositories with every condition, 27 questions, 3 runs each. Right answers: no tools 7.0 (26%) (7, 7, 7); one python tool 9.3 (35%) (10, 9, 9).

A cell is the number of right answers: the mean of the runs, then each run in brackets.

| Package | Questions | Tools accepted | No tools | One Python tool |
| --- | --- | --- | --- | --- |
| `dateutil` | 14 | none | 7.0 (7, 7, 7) | 5.7 (6, 5, 6) |
| `mcp` | 4 | none | none | none |
| `more_itertools` | 5 | none | 0.0 (0, 0, 0) | none |
| `networkx` | 14 | none | 2.0 (2, 2, 2) | none |
| `jinja2` | 3 | none | 1.0 (1, 1, 1) | none |
| `werkzeug` | 13 | none | 0.0 (0, 0, 0) | 3.7 (4, 4, 3) |
| `packaging` | 10 | none | 1.0 (1, 1, 1) | none |
| `rsa` | 3 | none | 0.0 (0, 0, 0) | none |
| **2 repositories with every condition** | **27** | | **7.0 (26%) (7, 7, 7)** | **9.3 (35%) (10, 9, 9)** |

## How the tools were used

Means over the runs.

| Package | Condition | Questions with a tool call | Right among those | Tool calls | Calls that gave an error | Calls written as text, and run |
| --- | --- | --- | --- | --- | --- | --- |
| `dateutil` | one python tool | 14.0 of 14 | 5.7 | 126.7 | 118.7 | 42.7 |
| `werkzeug` | one python tool | 13.0 of 13 | 3.7 | 67.3 | 63.0 | 24.7 |

## By kind of answer

First run. A true-or-false question can be answered right by guessing half of the time.

| The answer is | Questions | No tools | One Python tool |
| --- | --- | --- | --- |
| true or false | 7 | 4 (57%) | 2 (29%) |
| another value | 20 | 3 (15%) | 8 (40%) |

## Question by question

First run. p is the exact two-sided sign test on the questions that only one of the two got right.

| A | B | Only A right | Only B right | p |
| --- | --- | --- | --- | --- |
| no tools | one python tool | 4 | 7 | 0.55 |
