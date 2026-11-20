# Tools against no tools, on the questions of out/corpus/tasks-aimed/ (aimed1)

A tool call that the model wrote as text is run as a call, and the Python tool's output is shown as text.

Model `qwen3-4b-rec4-f3`. 2 repositories with every condition, 6 questions, 3 runs each. Right answers: no tools 2.0 (33%) (2, 2, 2); one python tool 2.0 (33%) (2, 2, 2); python tool + reference (elements used) 3.0 (50%) (3, 3, 3); python tool + reference (search) 2.3 (39%) (2, 3, 2).

A cell is the number of right answers: the mean of the runs, then each run in brackets.

| Package | Questions | Tools accepted | No tools | One Python tool | Python tool + reference (elements used) | Python tool + reference (search) |
| --- | --- | --- | --- | --- | --- | --- |
| `dateutil` | 14 | none | none | none | none | none |
| `mcp` | 4 | none | none | none | none | none |
| `more_itertools` | 5 | none | none | none | none | none |
| `networkx` | 14 | none | none | none | none | none |
| `jinja2` | 3 | none | 1.0 (1, 1, 1) | 1.0 (1, 1, 1) | 0.0 (0, 0, 0) | 1.0 (1, 1, 1) |
| `werkzeug` | 13 | none | none | none | none | none |
| `packaging` | 10 | none | none | none | none | none |
| `rsa` | 3 | none | 1.0 (1, 1, 1) | 1.0 (1, 1, 1) | 3.0 (3, 3, 3) | 1.3 (1, 2, 1) |
| **2 repositories with every condition** | **6** | | **2.0 (33%) (2, 2, 2)** | **2.0 (33%) (2, 2, 2)** | **3.0 (50%) (3, 3, 3)** | **2.3 (39%) (2, 3, 2)** |

## How the tools were used

Means over the runs.

| Package | Condition | Questions with a tool call | Right among those | Tool calls | Calls that gave an error | Calls written as text, and run |
| --- | --- | --- | --- | --- | --- | --- |
| `jinja2` | one python tool | 3.0 of 3 | 1.0 | 43.0 | 41.0 | 0.0 |
| `jinja2` | python tool + reference (elements used) | 3.0 of 3 | 0.0 | 91.0 | 91.0 | 0.0 |
| `jinja2` | python tool + reference (search) | 3.0 of 3 | 1.0 | 81.0 | 80.0 | 0.0 |
| `rsa` | one python tool | 3.0 of 3 | 1.0 | 50.0 | 49.0 | 0.0 |
| `rsa` | python tool + reference (elements used) | 3.0 of 3 | 3.0 | 3.0 | 0.0 | 0.0 |
| `rsa` | python tool + reference (search) | 3.0 of 3 | 1.3 | 46.3 | 45.0 | 0.0 |

## By kind of answer

First run. A true-or-false question can be answered right by guessing half of the time.

| The answer is | Questions | No tools | One Python tool | Python tool + reference (elements used) | Python tool + reference (search) |
| --- | --- | --- | --- | --- | --- |
| true or false | 0 | none | none | none | none |
| another value | 6 | 2 (33%) | 2 (33%) | 3 (50%) | 2 (33%) |

## Question by question

First run. p is the exact two-sided sign test on the questions that only one of the two got right.

| A | B | Only A right | Only B right | p |
| --- | --- | --- | --- | --- |
| no tools | one python tool | 1 | 1 | 1 |
| no tools | python tool + reference (elements used) | 1 | 2 | 1 |
| no tools | python tool + reference (search) | 2 | 2 | 1 |
| one python tool | python tool + reference (elements used) | 1 | 2 | 1 |
| one python tool | python tool + reference (search) | 1 | 1 | 1 |
| python tool + reference (elements used) | python tool + reference (search) | 2 | 1 | 1 |
