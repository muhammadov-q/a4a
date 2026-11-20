# Tools against no tools, on the questions of out/corpus/tasks-aimed/ (aimed1)

A tool call that the model wrote as text is run as a call, and the Python tool's output is shown as text.

Model `qwen3-1.7b-rec17`. 2 repositories with every condition, 27 questions, 3 runs each. Right answers: no tools 12.0 (44%) (12, 12, 12); one python tool 12.3 (46%) (12, 12, 13); python tool + reference (elements used) 13.7 (51%) (13, 14, 14); python tool + reference (search) 10.3 (38%) (10, 11, 10).

A cell is the number of right answers: the mean of the runs, then each run in brackets.

| Package | Questions | Tools accepted | No tools | One Python tool | Python tool + reference (elements used) | Python tool + reference (search) |
| --- | --- | --- | --- | --- | --- | --- |
| `dateutil` | 14 | none | 9.0 (9, 9, 9) | 7.3 (7, 7, 8) | 6.3 (6, 7, 6) | 3.3 (3, 4, 3) |
| `mcp` | 4 | none | none | none | none | none |
| `more_itertools` | 5 | none | none | none | none | none |
| `networkx` | 14 | none | none | none | none | none |
| `jinja2` | 3 | none | none | none | none | none |
| `werkzeug` | 13 | none | 3.0 (3, 3, 3) | 5.0 (5, 5, 5) | 7.3 (7, 7, 8) | 7.0 (7, 7, 7) |
| `packaging` | 10 | none | none | none | none | none |
| `rsa` | 3 | none | none | none | none | none |
| **2 repositories with every condition** | **27** | | **12.0 (44%) (12, 12, 12)** | **12.3 (46%) (12, 12, 13)** | **13.7 (51%) (13, 14, 14)** | **10.3 (38%) (10, 11, 10)** |

## How the tools were used

Means over the runs.

| Package | Condition | Questions with a tool call | Right among those | Tool calls | Calls that gave an error | Calls written as text, and run |
| --- | --- | --- | --- | --- | --- | --- |
| `dateutil` | one python tool | 14.0 of 14 | 7.3 | 199.3 | 190.0 | 0.0 |
| `dateutil` | python tool + reference (elements used) | 14.0 of 14 | 6.3 | 280.3 | 273.3 | 0.0 |
| `dateutil` | python tool + reference (search) | 14.0 of 14 | 3.3 | 378.7 | 375.0 | 0.0 |
| `werkzeug` | one python tool | 13.0 of 13 | 5.0 | 260.0 | 253.0 | 0.0 |
| `werkzeug` | python tool + reference (elements used) | 13.0 of 13 | 7.3 | 157.0 | 147.7 | 0.0 |
| `werkzeug` | python tool + reference (search) | 13.0 of 13 | 7.0 | 148.3 | 138.7 | 0.0 |

## By kind of answer

First run. A true-or-false question can be answered right by guessing half of the time.

| The answer is | Questions | No tools | One Python tool | Python tool + reference (elements used) | Python tool + reference (search) |
| --- | --- | --- | --- | --- | --- |
| true or false | 7 | 5 (71%) | 3 (43%) | 3 (43%) | 2 (29%) |
| another value | 20 | 7 (35%) | 9 (45%) | 10 (50%) | 8 (40%) |

## Question by question

First run. p is the exact two-sided sign test on the questions that only one of the two got right.

| A | B | Only A right | Only B right | p |
| --- | --- | --- | --- | --- |
| no tools | one python tool | 6 | 6 | 1 |
| no tools | python tool + reference (elements used) | 6 | 7 | 1 |
| no tools | python tool + reference (search) | 7 | 5 | 0.77 |
| one python tool | python tool + reference (elements used) | 3 | 4 | 1 |
| one python tool | python tool + reference (search) | 6 | 4 | 0.75 |
| python tool + reference (elements used) | python tool + reference (search) | 4 | 1 | 0.38 |
