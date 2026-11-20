# Tools against no tools, on the questions of out/corpus/tasks-aimed/ (aimed1)

A tool call that the model wrote as text is run as a call, and the Python tool's output is shown as text.

Model `qwen3-1.7b-rec17-f3`. 2 repositories with every condition, 6 questions, 3 runs each. Right answers: no tools 1.0 (17%) (1, 1, 1); one python tool 2.0 (33%) (2, 2, 2); python tool + reference (elements used) 3.0 (50%) (3, 3, 3); python tool + reference (search) 3.0 (50%) (3, 3, 3).

A cell is the number of right answers: the mean of the runs, then each run in brackets.

| Package | Questions | Tools accepted | No tools | One Python tool | Python tool + reference (elements used) | Python tool + reference (search) |
| --- | --- | --- | --- | --- | --- | --- |
| `dateutil` | 14 | none | none | none | none | none |
| `mcp` | 4 | none | none | none | none | none |
| `more_itertools` | 5 | none | none | none | none | none |
| `networkx` | 14 | none | none | none | none | none |
| `jinja2` | 3 | none | 1.0 (1, 1, 1) | 1.0 (1, 1, 1) | 1.0 (1, 1, 1) | 1.0 (1, 1, 1) |
| `werkzeug` | 13 | none | none | none | none | none |
| `packaging` | 10 | none | none | none | none | none |
| `rsa` | 3 | none | 0.0 (0, 0, 0) | 1.0 (1, 1, 1) | 2.0 (2, 2, 2) | 2.0 (2, 2, 2) |
| **2 repositories with every condition** | **6** | | **1.0 (17%) (1, 1, 1)** | **2.0 (33%) (2, 2, 2)** | **3.0 (50%) (3, 3, 3)** | **3.0 (50%) (3, 3, 3)** |

## How the tools were used

Means over the runs.

| Package | Condition | Questions with a tool call | Right among those | Tool calls | Calls that gave an error | Calls written as text, and run |
| --- | --- | --- | --- | --- | --- | --- |
| `jinja2` | one python tool | 2.0 of 3 | 1.0 | 38.0 | 38.0 | 0.0 |
| `jinja2` | python tool + reference (elements used) | 3.0 of 3 | 1.0 | 77.3 | 76.3 | 0.0 |
| `jinja2` | python tool + reference (search) | 3.0 of 3 | 1.0 | 40.0 | 39.3 | 0.0 |
| `rsa` | one python tool | 3.0 of 3 | 1.0 | 80.0 | 80.0 | 0.0 |
| `rsa` | python tool + reference (elements used) | 3.0 of 3 | 2.0 | 42.0 | 40.0 | 0.0 |
| `rsa` | python tool + reference (search) | 2.7 of 3 | 2.0 | 20.0 | 4.7 | 0.0 |

## By kind of answer

First run. A true-or-false question can be answered right by guessing half of the time.

| The answer is | Questions | No tools | One Python tool | Python tool + reference (elements used) | Python tool + reference (search) |
| --- | --- | --- | --- | --- | --- |
| true or false | 0 | none | none | none | none |
| another value | 6 | 1 (17%) | 2 (33%) | 3 (50%) | 3 (50%) |

## Question by question

First run. p is the exact two-sided sign test on the questions that only one of the two got right.

| A | B | Only A right | Only B right | p |
| --- | --- | --- | --- | --- |
| no tools | one python tool | 0 | 1 | 1 |
| no tools | python tool + reference (elements used) | 0 | 2 | 0.5 |
| no tools | python tool + reference (search) | 0 | 2 | 0.5 |
| one python tool | python tool + reference (elements used) | 0 | 1 | 1 |
| one python tool | python tool + reference (search) | 0 | 1 | 1 |
| python tool + reference (elements used) | python tool + reference (search) | 0 | 0 | 1 |
