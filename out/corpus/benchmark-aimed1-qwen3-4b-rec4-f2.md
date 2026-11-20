# Tools against no tools, on the questions of out/corpus/tasks-aimed/ (aimed1)

A tool call that the model wrote as text is run as a call, and the Python tool's output is shown as text.

Model `qwen3-4b-rec4-f2`. 3 repositories with every condition, 29 questions, 3 runs each. Right answers: no tools 13.3 (46%) (13, 13, 14); one python tool 15.7 (54%) (16, 15, 16); python tool + reference (elements used) 27.3 (94%) (28, 27, 27); python tool + reference (search) 27.0 (93%) (27, 27, 27).

A cell is the number of right answers: the mean of the runs, then each run in brackets.

| Package | Questions | Tools accepted | No tools | One Python tool | Python tool + reference (elements used) | Python tool + reference (search) |
| --- | --- | --- | --- | --- | --- | --- |
| `dateutil` | 14 | none | none | none | none | none |
| `mcp` | 4 | none | none | none | none | none |
| `more_itertools` | 5 | none | 3.0 (3, 3, 3) | 2.0 (2, 2, 2) | 4.0 (4, 4, 4) | 4.0 (4, 4, 4) |
| `networkx` | 14 | none | 7.3 (7, 7, 8) | 8.0 (8, 8, 8) | 13.3 (14, 13, 13) | 14.0 (14, 14, 14) |
| `jinja2` | 3 | none | none | none | none | none |
| `werkzeug` | 13 | none | none | none | none | none |
| `packaging` | 10 | none | 3.0 (3, 3, 3) | 5.7 (6, 5, 6) | 10.0 (10, 10, 10) | 9.0 (9, 9, 9) |
| `rsa` | 3 | none | none | none | none | none |
| **3 repositories with every condition** | **29** | | **13.3 (46%) (13, 13, 14)** | **15.7 (54%) (16, 15, 16)** | **27.3 (94%) (28, 27, 27)** | **27.0 (93%) (27, 27, 27)** |

## How the tools were used

Means over the runs.

| Package | Condition | Questions with a tool call | Right among those | Tool calls | Calls that gave an error | Calls written as text, and run |
| --- | --- | --- | --- | --- | --- | --- |
| `more_itertools` | one python tool | 5.0 of 5 | 2.0 | 19.0 | 15.0 | 0.0 |
| `more_itertools` | python tool + reference (elements used) | 5.0 of 5 | 4.0 | 5.0 | 0.0 | 0.0 |
| `more_itertools` | python tool + reference (search) | 5.0 of 5 | 4.0 | 5.0 | 0.0 | 0.0 |
| `networkx` | one python tool | 12.7 of 14 | 7.0 | 43.3 | 34.0 | 0.0 |
| `networkx` | python tool + reference (elements used) | 14.0 of 14 | 13.3 | 49.7 | 36.7 | 0.0 |
| `networkx` | python tool + reference (search) | 14.0 of 14 | 14.0 | 19.0 | 5.0 | 0.0 |
| `packaging` | one python tool | 10.0 of 10 | 5.7 | 23.3 | 15.3 | 0.0 |
| `packaging` | python tool + reference (elements used) | 10.0 of 10 | 10.0 | 10.0 | 0.0 | 0.0 |
| `packaging` | python tool + reference (search) | 10.0 of 10 | 9.0 | 10.7 | 0.7 | 0.0 |

## By kind of answer

First run. A true-or-false question can be answered right by guessing half of the time.

| The answer is | Questions | No tools | One Python tool | Python tool + reference (elements used) | Python tool + reference (search) |
| --- | --- | --- | --- | --- | --- |
| true or false | 2 | 2 (100%) | 1 (50%) | 2 (100%) | 2 (100%) |
| another value | 27 | 11 (41%) | 15 (56%) | 26 (96%) | 25 (93%) |

## Question by question

First run. p is the exact two-sided sign test on the questions that only one of the two got right.

| A | B | Only A right | Only B right | p |
| --- | --- | --- | --- | --- |
| no tools | one python tool | 4 | 7 | 0.55 |
| no tools | python tool + reference (elements used) | 1 | 16 | 0.00027 |
| no tools | python tool + reference (search) | 1 | 15 | 0.00052 |
| one python tool | python tool + reference (elements used) | 0 | 12 | 0.00049 |
| one python tool | python tool + reference (search) | 0 | 11 | 0.00098 |
| python tool + reference (elements used) | python tool + reference (search) | 1 | 0 | 1 |
