# Tools against no tools, on the questions of out/corpus/tasks-aimed/ (aimed1)

A tool call that the model wrote as text is run as a call, and the Python tool's output is shown as text.

Model `qwen3-4b-rec4`. 2 repositories with every condition, 27 questions, 3 runs each. Right answers: no tools 14.3 (53%) (14, 15, 14); one python tool 15.0 (56%) (15, 15, 15).

A cell is the number of right answers: the mean of the runs, then each run in brackets.

| Package | Questions | Tools accepted | No tools | One Python tool |
| --- | --- | --- | --- | --- |
| `dateutil` | 14 | none | 9.0 (9, 9, 9) | 9.0 (9, 9, 9) |
| `mcp` | 4 | none | none | none |
| `more_itertools` | 5 | none | none | none |
| `networkx` | 14 | none | none | none |
| `jinja2` | 3 | none | none | none |
| `werkzeug` | 13 | none | 5.3 (5, 6, 5) | 6.0 (6, 6, 6) |
| `packaging` | 10 | none | none | none |
| `rsa` | 3 | none | none | none |
| **2 repositories with every condition** | **27** | | **14.3 (53%) (14, 15, 14)** | **15.0 (56%) (15, 15, 15)** |

## How the tools were used

Means over the runs.

| Package | Condition | Questions with a tool call | Right among those | Tool calls | Calls that gave an error | Calls written as text, and run |
| --- | --- | --- | --- | --- | --- | --- |
| `dateutil` | one python tool | 14.0 of 14 | 9.0 | 153.7 | 143.3 | 2.7 |
| `werkzeug` | one python tool | 13.0 of 13 | 6.0 | 103.0 | 93.0 | 0.0 |

## By kind of answer

First run. A true-or-false question can be answered right by guessing half of the time.

| The answer is | Questions | No tools | One Python tool |
| --- | --- | --- | --- |
| true or false | 7 | 4 (57%) | 3 (43%) |
| another value | 20 | 10 (50%) | 12 (60%) |

## Question by question

First run. p is the exact two-sided sign test on the questions that only one of the two got right.

| A | B | Only A right | Only B right | p |
| --- | --- | --- | --- | --- |
| no tools | one python tool | 4 | 5 | 1 |
