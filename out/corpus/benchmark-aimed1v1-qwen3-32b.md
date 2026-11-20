# Tools against no tools, on the questions of out/corpus/tasks-aimed-v1/ (aimed1v1)

A tool call that the model wrote as text is run as a call, and the Python tool's output is shown as text.

Model `qwen3-32b`. 7 repositories with every condition, 42 questions, 1 run each. Right answers: no tools 19 (45%); one python tool 28 (67%).

A cell is the number of right answers: the mean of the runs, then each run in brackets.

| Package | Questions | Tools accepted | No tools | One Python tool |
| --- | --- | --- | --- | --- |
| `dateutil` | 8 | none | 6 | 5 |
| `more_itertools` | 5 | none | 2 | 3 |
| `networkx` | 13 | none | 4 | 8 |
| `jinja2` | 1 | none | 0 | 1 |
| `werkzeug` | 8 | none | 3 | 6 |
| `packaging` | 6 | none | 4 | 4 |
| `rsa` | 1 | none | 0 | 1 |
| **7 repositories with every condition** | **42** | | **19 (45%)** | **28 (67%)** |

## How the tools were used

Means over the runs.

| Package | Condition | Questions with a tool call | Right among those | Tool calls | Calls that gave an error | Calls written as text, and run |
| --- | --- | --- | --- | --- | --- | --- |
| `dateutil` | one python tool | 8.0 of 8 | 5.0 | 9.0 | 3.0 | 0.0 |
| `more_itertools` | one python tool | 5.0 of 5 | 3.0 | 13.0 | 8.0 | 0.0 |
| `networkx` | one python tool | 12.0 of 13 | 8.0 | 13.0 | 3.0 | 0.0 |
| `jinja2` | one python tool | 1.0 of 1 | 1.0 | 1.0 | 0.0 | 0.0 |
| `werkzeug` | one python tool | 8.0 of 8 | 6.0 | 13.0 | 6.0 | 0.0 |
| `packaging` | one python tool | 6.0 of 6 | 4.0 | 6.0 | 1.0 | 0.0 |
| `rsa` | one python tool | 1.0 of 1 | 1.0 | 1.0 | 0.0 | 0.0 |

## By kind of answer

First run. A true-or-false question can be answered right by guessing half of the time.

| The answer is | Questions | No tools | One Python tool |
| --- | --- | --- | --- |
| true or false | 5 | 5 (100%) | 3 (60%) |
| another value | 37 | 14 (38%) | 25 (68%) |

## Question by question

First run. p is the exact two-sided sign test on the questions that only one of the two got right.

| A | B | Only A right | Only B right | p |
| --- | --- | --- | --- | --- |
| no tools | one python tool | 4 | 13 | 0.049 |
