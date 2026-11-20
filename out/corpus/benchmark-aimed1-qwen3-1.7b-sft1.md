# Tools against no tools, on the questions of out/corpus/tasks-aimed/ (aimed1)

A tool call that the model wrote as text is run as a call, and the Python tool's output is shown as text.

Model `qwen3-1.7b-sft1`. 2 repositories with every condition, 27 questions, 3 runs each. Right answers: no tools 10.0 (37%) (10, 10, 10); one python tool 9.7 (36%) (10, 9, 10); python tool + reference (elements used) 17.0 (63%) (17, 17, 17); python tool + reference (search) 14.0 (52%) (13, 14, 15).

A cell is the number of right answers: the mean of the runs, then each run in brackets.

| Package | Questions | Tools accepted | No tools | One Python tool | Python tool + reference (elements used) | Python tool + reference (search) |
| --- | --- | --- | --- | --- | --- | --- |
| `dateutil` | 14 | none | 7.0 (7, 7, 7) | 5.7 (6, 5, 6) | 8.0 (8, 8, 8) | 5.7 (5, 6, 6) |
| `mcp` | 4 | none | none | none | none | none |
| `more_itertools` | 5 | none | none | none | none | none |
| `networkx` | 14 | none | none | none | none | none |
| `jinja2` | 3 | none | none | none | none | none |
| `werkzeug` | 13 | none | 3.0 (3, 3, 3) | 4.0 (4, 4, 4) | 9.0 (9, 9, 9) | 8.3 (8, 8, 9) |
| `packaging` | 10 | none | none | none | none | none |
| `rsa` | 3 | none | none | none | none | none |
| **2 repositories with every condition** | **27** | | **10.0 (37%) (10, 10, 10)** | **9.7 (36%) (10, 9, 10)** | **17.0 (63%) (17, 17, 17)** | **14.0 (52%) (13, 14, 15)** |

## How the tools were used

Means over the runs.

| Package | Condition | Questions with a tool call | Right among those | Tool calls | Calls that gave an error | Calls written as text, and run |
| --- | --- | --- | --- | --- | --- | --- |
| `dateutil` | one python tool | 13.3 of 14 | 5.7 | 215.3 | 208.0 | 0.0 |
| `dateutil` | python tool + reference (elements used) | 14.0 of 14 | 8.0 | 256.0 | 248.0 | 0.0 |
| `dateutil` | python tool + reference (search) | 13.0 of 14 | 5.3 | 290.0 | 284.3 | 0.0 |
| `werkzeug` | one python tool | 13.0 of 13 | 4.0 | 253.0 | 247.0 | 0.0 |
| `werkzeug` | python tool + reference (elements used) | 13.0 of 13 | 9.0 | 109.7 | 99.7 | 0.0 |
| `werkzeug` | python tool + reference (search) | 13.0 of 13 | 8.3 | 120.7 | 110.3 | 0.0 |

## By kind of answer

First run. A true-or-false question can be answered right by guessing half of the time.

| The answer is | Questions | No tools | One Python tool | Python tool + reference (elements used) | Python tool + reference (search) |
| --- | --- | --- | --- | --- | --- |
| true or false | 7 | 4 (57%) | 2 (29%) | 5 (71%) | 3 (43%) |
| another value | 20 | 6 (30%) | 8 (40%) | 12 (60%) | 10 (50%) |

## Question by question

First run. p is the exact two-sided sign test on the questions that only one of the two got right.

| A | B | Only A right | Only B right | p |
| --- | --- | --- | --- | --- |
| no tools | one python tool | 7 | 7 | 1 |
| no tools | python tool + reference (elements used) | 3 | 10 | 0.092 |
| no tools | python tool + reference (search) | 3 | 6 | 0.51 |
| one python tool | python tool + reference (elements used) | 3 | 10 | 0.092 |
| one python tool | python tool + reference (search) | 4 | 7 | 0.55 |
| python tool + reference (elements used) | python tool + reference (search) | 5 | 1 | 0.22 |
