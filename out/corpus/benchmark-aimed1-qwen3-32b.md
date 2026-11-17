# Tools against no tools, on the questions of out/corpus/tasks-aimed/ (aimed1)

A tool call that the model wrote as text is run as a call, and the Python tool's output is shown as text.

Model `qwen3-32b`. 7 repositories with every condition, 62 questions, 1 run each. Right answers: no tools 32 (52%); one python tool 39 (63%).

A cell is the number of right answers: the mean of the runs, then each run in brackets.

| Package | Questions | Tools accepted | No tools | One Python tool |
| --- | --- | --- | --- | --- |
| `dateutil` | 14 | none | 11 | 9 |
| `mcp` | 4 | none | none | none |
| `more_itertools` | 5 | none | 2 | 1 |
| `networkx` | 14 | none | 5 | 9 |
| `jinja2` | 3 | none | 1 | 1 |
| `werkzeug` | 13 | none | 7 | 9 |
| `packaging` | 10 | none | 5 | 8 |
| `rsa` | 3 | none | 1 | 2 |
| **7 repositories with every condition** | **62** | | **32 (52%)** | **39 (63%)** |

## How the tools were used

Means over the runs.

| Package | Condition | Questions with a tool call | Right among those | Tool calls | Calls that gave an error | Calls written as text, and run |
| --- | --- | --- | --- | --- | --- | --- |
| `dateutil` | one python tool | 14.0 of 14 | 9.0 | 17.0 | 7.0 | 0.0 |
| `more_itertools` | one python tool | 5.0 of 5 | 1.0 | 7.0 | 2.0 | 1.0 |
| `networkx` | one python tool | 13.0 of 14 | 9.0 | 14.0 | 3.0 | 0.0 |
| `jinja2` | one python tool | 3.0 of 3 | 1.0 | 6.0 | 4.0 | 0.0 |
| `werkzeug` | one python tool | 13.0 of 13 | 9.0 | 17.0 | 7.0 | 0.0 |
| `packaging` | one python tool | 10.0 of 10 | 8.0 | 11.0 | 2.0 | 0.0 |
| `rsa` | one python tool | 3.0 of 3 | 2.0 | 3.0 | 0.0 | 0.0 |

## By kind of answer

First run. A true-or-false question can be answered right by guessing half of the time.

| The answer is | Questions | No tools | One Python tool |
| --- | --- | --- | --- |
| true or false | 9 | 7 (78%) | 5 (56%) |
| another value | 53 | 25 (47%) | 34 (64%) |

## Question by question

First run. p is the exact two-sided sign test on the questions that only one of the two got right.

| A | B | Only A right | Only B right | p |
| --- | --- | --- | --- | --- |
| no tools | one python tool | 6 | 13 | 0.17 |
