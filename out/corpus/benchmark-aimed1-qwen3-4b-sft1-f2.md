# Tools against no tools, on the questions of out/corpus/tasks-aimed/ (aimed1)

A tool call that the model wrote as text is run as a call, and the Python tool's output is shown as text.

Model `qwen3-4b-sft1-f2`. 3 repositories with every condition, 29 questions, 3 runs each. Right answers: no tools 12.0 (41%) (12, 12, 12); one python tool 16.3 (56%) (16, 17, 16).

A cell is the number of right answers: the mean of the runs, then each run in brackets.

| Package | Questions | Tools accepted | No tools | One Python tool |
| --- | --- | --- | --- | --- |
| `dateutil` | 14 | none | none | none |
| `mcp` | 4 | none | none | none |
| `more_itertools` | 5 | none | 3.0 (3, 3, 3) | 3.0 (3, 3, 3) |
| `networkx` | 14 | none | 6.0 (6, 6, 6) | 7.3 (7, 8, 7) |
| `jinja2` | 3 | none | none | none |
| `werkzeug` | 13 | none | none | none |
| `packaging` | 10 | none | 3.0 (3, 3, 3) | 6.0 (6, 6, 6) |
| `rsa` | 3 | none | none | none |
| **3 repositories with every condition** | **29** | | **12.0 (41%) (12, 12, 12)** | **16.3 (56%) (16, 17, 16)** |

## How the tools were used

Means over the runs.

| Package | Condition | Questions with a tool call | Right among those | Tool calls | Calls that gave an error | Calls written as text, and run |
| --- | --- | --- | --- | --- | --- | --- |
| `more_itertools` | one python tool | 5.0 of 5 | 3.0 | 47.0 | 43.0 | 0.0 |
| `networkx` | one python tool | 13.0 of 14 | 7.3 | 118.0 | 107.3 | 0.7 |
| `packaging` | one python tool | 10.0 of 10 | 6.0 | 63.0 | 49.0 | 0.0 |

## By kind of answer

First run. A true-or-false question can be answered right by guessing half of the time.

| The answer is | Questions | No tools | One Python tool |
| --- | --- | --- | --- |
| true or false | 2 | 2 (100%) | 1 (50%) |
| another value | 27 | 10 (37%) | 15 (56%) |

## Question by question

First run. p is the exact two-sided sign test on the questions that only one of the two got right.

| A | B | Only A right | Only B right | p |
| --- | --- | --- | --- | --- |
| no tools | one python tool | 3 | 7 | 0.34 |
