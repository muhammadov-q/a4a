# Tools against no tools, on the questions of out/corpus/tasks-aimed/ (aimed1)

A tool call that the model wrote as text is run as a call, and the Python tool's output is shown as text.

Model `qwen3-4b-sft1`. 2 repositories with every condition, 27 questions, 3 runs each. Right answers: no tools 14.0 (52%) (14, 14, 14); one python tool 13.7 (51%) (14, 14, 13); python tool + reference (elements used) 22.3 (83%) (23, 22, 22); python tool + reference (search) 18.7 (69%) (18, 18, 20).

A cell is the number of right answers: the mean of the runs, then each run in brackets.

| Package | Questions | Tools accepted | No tools | One Python tool | Python tool + reference (elements used) | Python tool + reference (search) |
| --- | --- | --- | --- | --- | --- | --- |
| `dateutil` | 14 | none | 9.0 (9, 9, 9) | 8.0 (8, 8, 8) | 13.0 (13, 13, 13) | 11.0 (10, 11, 12) |
| `mcp` | 4 | none | none | none | none | none |
| `more_itertools` | 5 | none | none | none | none | none |
| `networkx` | 14 | none | none | none | none | none |
| `jinja2` | 3 | none | none | none | none | none |
| `werkzeug` | 13 | none | 5.0 (5, 5, 5) | 5.7 (6, 6, 5) | 9.3 (10, 9, 9) | 7.7 (8, 7, 8) |
| `packaging` | 10 | none | none | none | none | none |
| `rsa` | 3 | none | none | none | none | none |
| **2 repositories with every condition** | **27** | | **14.0 (52%) (14, 14, 14)** | **13.7 (51%) (14, 14, 13)** | **22.3 (83%) (23, 22, 22)** | **18.7 (69%) (18, 18, 20)** |

## How the tools were used

Means over the runs.

| Package | Condition | Questions with a tool call | Right among those | Tool calls | Calls that gave an error | Calls written as text, and run |
| --- | --- | --- | --- | --- | --- | --- |
| `dateutil` | one python tool | 14.0 of 14 | 8.0 | 159.0 | 148.7 | 0.0 |
| `dateutil` | python tool + reference (elements used) | 14.0 of 14 | 13.0 | 55.0 | 42.0 | 0.0 |
| `dateutil` | python tool + reference (search) | 13.7 of 14 | 10.7 | 94.7 | 83.0 | 0.0 |
| `werkzeug` | one python tool | 13.0 of 13 | 5.7 | 106.0 | 96.7 | 0.0 |
| `werkzeug` | python tool + reference (elements used) | 13.0 of 13 | 9.3 | 117.7 | 107.3 | 0.0 |
| `werkzeug` | python tool + reference (search) | 13.0 of 13 | 7.7 | 94.0 | 82.3 | 0.0 |

## By kind of answer

First run. A true-or-false question can be answered right by guessing half of the time.

| The answer is | Questions | No tools | One Python tool | Python tool + reference (elements used) | Python tool + reference (search) |
| --- | --- | --- | --- | --- | --- |
| true or false | 7 | 4 (57%) | 2 (29%) | 6 (86%) | 5 (71%) |
| another value | 20 | 10 (50%) | 12 (60%) | 17 (85%) | 13 (65%) |

## Question by question

First run. p is the exact two-sided sign test on the questions that only one of the two got right.

| A | B | Only A right | Only B right | p |
| --- | --- | --- | --- | --- |
| no tools | one python tool | 5 | 5 | 1 |
| no tools | python tool + reference (elements used) | 2 | 11 | 0.022 |
| no tools | python tool + reference (search) | 4 | 8 | 0.39 |
| one python tool | python tool + reference (elements used) | 0 | 9 | 0.0039 |
| one python tool | python tool + reference (search) | 2 | 6 | 0.29 |
| python tool + reference (elements used) | python tool + reference (search) | 5 | 0 | 0.062 |
