# Tools against no tools, on the questions of out/corpus/tasks-aimed/ (aimed1)

A tool call that the model wrote as text is run as a call, and the Python tool's output is shown as text.

Model `qwen3-8b`. 7 repositories with every condition, 62 questions, 1 run each. Right answers: no tools 25 (40%); one python tool 38 (61%).

A cell is the number of right answers: the mean of the runs, then each run in brackets.

| Package | Questions | Tools accepted | No tools | One Python tool |
| --- | --- | --- | --- | --- |
| `dateutil` | 14 | none | 10 | 8 |
| `mcp` | 4 | none | none | none |
| `more_itertools` | 5 | none | 3 | 2 |
| `networkx` | 14 | none | 2 | 11 |
| `jinja2` | 3 | none | 1 | 1 |
| `werkzeug` | 13 | none | 5 | 7 |
| `packaging` | 10 | none | 3 | 6 |
| `rsa` | 3 | none | 1 | 3 |
| **7 repositories with every condition** | **62** | | **25 (40%)** | **38 (61%)** |

## How the tools were used

Means over the runs.

| Package | Condition | Questions with a tool call | Right among those | Tool calls | Calls that gave an error | Calls written as text, and run |
| --- | --- | --- | --- | --- | --- | --- |
| `dateutil` | one python tool | 14.0 of 14 | 8.0 | 40.0 | 30.0 | 5.0 |
| `more_itertools` | one python tool | 5.0 of 5 | 2.0 | 14.0 | 9.0 | 0.0 |
| `networkx` | one python tool | 14.0 of 14 | 11.0 | 39.0 | 27.0 | 0.0 |
| `jinja2` | one python tool | 3.0 of 3 | 1.0 | 9.0 | 7.0 | 0.0 |
| `werkzeug` | one python tool | 13.0 of 13 | 7.0 | 123.0 | 115.0 | 79.0 |
| `packaging` | one python tool | 10.0 of 10 | 6.0 | 20.0 | 11.0 | 0.0 |
| `rsa` | one python tool | 3.0 of 3 | 3.0 | 11.0 | 8.0 | 0.0 |

## By kind of answer

First run. A true-or-false question can be answered right by guessing half of the time.

| The answer is | Questions | No tools | One Python tool |
| --- | --- | --- | --- |
| true or false | 9 | 5 (56%) | 4 (44%) |
| another value | 53 | 20 (38%) | 34 (64%) |

## Question by question

First run. p is the exact two-sided sign test on the questions that only one of the two got right.

| A | B | Only A right | Only B right | p |
| --- | --- | --- | --- | --- |
| no tools | one python tool | 7 | 20 | 0.019 |
