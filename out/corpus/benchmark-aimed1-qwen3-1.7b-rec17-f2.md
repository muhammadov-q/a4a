# Tools against no tools, on the questions of out/corpus/tasks-aimed/ (aimed1)

A tool call that the model wrote as text is run as a call, and the Python tool's output is shown as text.

Model `qwen3-1.7b-rec17-f2`. 3 repositories with every condition, 29 questions, 3 runs each. Right answers: no tools 4.0 (14%) (4, 4, 4); one python tool 13.3 (46%) (13, 13, 14).

A cell is the number of right answers: the mean of the runs, then each run in brackets.

| Package | Questions | Tools accepted | No tools | One Python tool |
| --- | --- | --- | --- | --- |
| `dateutil` | 14 | none | none | none |
| `mcp` | 4 | none | none | none |
| `more_itertools` | 5 | none | 0.0 (0, 0, 0) | 2.0 (2, 2, 2) |
| `networkx` | 14 | none | 4.0 (4, 4, 4) | 6.3 (6, 6, 7) |
| `jinja2` | 3 | none | none | none |
| `werkzeug` | 13 | none | none | none |
| `packaging` | 10 | none | 0.0 (0, 0, 0) | 5.0 (5, 5, 5) |
| `rsa` | 3 | none | none | none |
| **3 repositories with every condition** | **29** | | **4.0 (14%) (4, 4, 4)** | **13.3 (46%) (13, 13, 14)** |

## How the tools were used

Means over the runs.

| Package | Condition | Questions with a tool call | Right among those | Tool calls | Calls that gave an error | Calls written as text, and run |
| --- | --- | --- | --- | --- | --- | --- |
| `more_itertools` | one python tool | 5.0 of 5 | 2.0 | 62.3 | 61.3 | 0.0 |
| `networkx` | one python tool | 13.3 of 14 | 6.3 | 90.7 | 83.7 | 0.0 |
| `packaging` | one python tool | 9.7 of 10 | 5.0 | 97.0 | 92.3 | 0.0 |

## By kind of answer

First run. A true-or-false question can be answered right by guessing half of the time.

| The answer is | Questions | No tools | One Python tool |
| --- | --- | --- | --- |
| true or false | 2 | 1 (50%) | 1 (50%) |
| another value | 27 | 3 (11%) | 12 (44%) |

## Question by question

First run. p is the exact two-sided sign test on the questions that only one of the two got right.

| A | B | Only A right | Only B right | p |
| --- | --- | --- | --- | --- |
| no tools | one python tool | 1 | 10 | 0.012 |
