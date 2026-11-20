# Tools against no tools, on the questions of out/corpus/tasks-aimed/ (aimed1)

A tool call that the model wrote as text is run as a call, and the Python tool's output is shown as text.

Model `qwen3-1.7b`. 7 repositories with every condition, 62 questions, 3 runs each. Right answers: no tools 11.0 (18%) (11, 11, 11); one python tool 20.7 (33%) (20, 21, 21); python tool + reference (elements used) 29.7 (48%) (31, 29, 29); python tool + reference (search) 20.3 (33%) (20, 22, 19).

A cell is the number of right answers: the mean of the runs, then each run in brackets.

| Package | Questions | Tools accepted | No tools | One Python tool | Python tool + reference (elements used) | Python tool + reference (search) |
| --- | --- | --- | --- | --- | --- | --- |
| `dateutil` | 14 | none | 7.0 (7, 7, 7) | 8.7 (8, 9, 9) | 9.7 (11, 9, 9) | 4.3 (5, 5, 3) |
| `mcp` | 4 | none | none | none | none | none |
| `more_itertools` | 5 | none | 0.0 (0, 0, 0) | 1.0 (1, 1, 1) | 3.0 (3, 3, 3) | 2.0 (2, 2, 2) |
| `networkx` | 14 | none | 2.0 (2, 2, 2) | 5.0 (5, 5, 5) | 7.0 (7, 7, 7) | 4.0 (4, 4, 4) |
| `jinja2` | 3 | none | 1.0 (1, 1, 1) | 0.0 (0, 0, 0) | 1.0 (1, 1, 1) | 1.0 (1, 1, 1) |
| `werkzeug` | 13 | none | 0.0 (0, 0, 0) | 3.0 (3, 3, 3) | 5.0 (5, 5, 5) | 4.0 (4, 4, 4) |
| `packaging` | 10 | none | 1.0 (1, 1, 1) | 2.0 (2, 2, 2) | 3.0 (3, 3, 3) | 4.7 (4, 5, 5) |
| `rsa` | 3 | none | 0.0 (0, 0, 0) | 1.0 (1, 1, 1) | 1.0 (1, 1, 1) | 0.3 (0, 1, 0) |
| **7 repositories with every condition** | **62** | | **11.0 (18%) (11, 11, 11)** | **20.7 (33%) (20, 21, 21)** | **29.7 (48%) (31, 29, 29)** | **20.3 (33%) (20, 22, 19)** |

## How the tools were used

Means over the runs.

| Package | Condition | Questions with a tool call | Right among those | Tool calls | Calls that gave an error | Calls written as text, and run |
| --- | --- | --- | --- | --- | --- | --- |
| `dateutil` | one python tool | 14.0 of 14 | 8.7 | 80.3 | 71.7 | 38.0 |
| `dateutil` | python tool + reference (elements used) | 14.0 of 14 | 9.7 | 104.7 | 94.3 | 40.3 |
| `dateutil` | python tool + reference (search) | 14.0 of 14 | 4.3 | 332.0 | 286.3 | 202.3 |
| `more_itertools` | one python tool | 5.0 of 5 | 1.0 | 23.0 | 20.0 | 2.0 |
| `more_itertools` | python tool + reference (elements used) | 5.0 of 5 | 3.0 | 9.0 | 4.0 | 0.0 |
| `more_itertools` | python tool + reference (search) | 5.0 of 5 | 2.0 | 13.7 | 9.0 | 0.7 |
| `networkx` | one python tool | 14.0 of 14 | 5.0 | 107.7 | 98.7 | 40.3 |
| `networkx` | python tool + reference (elements used) | 14.0 of 14 | 7.0 | 77.3 | 65.3 | 12.7 |
| `networkx` | python tool + reference (search) | 14.0 of 14 | 4.0 | 202.0 | 173.0 | 110.3 |
| `jinja2` | one python tool | 3.0 of 3 | 0.0 | 35.7 | 35.7 | 18.7 |
| `jinja2` | python tool + reference (elements used) | 3.0 of 3 | 1.0 | 16.0 | 15.0 | 0.0 |
| `jinja2` | python tool + reference (search) | 3.0 of 3 | 1.0 | 35.3 | 34.3 | 1.0 |
| `werkzeug` | one python tool | 13.0 of 13 | 3.0 | 141.3 | 136.3 | 35.3 |
| `werkzeug` | python tool + reference (elements used) | 13.0 of 13 | 5.0 | 104.0 | 92.0 | 74.0 |
| `werkzeug` | python tool + reference (search) | 13.0 of 13 | 4.0 | 76.0 | 39.0 | 33.7 |
| `packaging` | one python tool | 10.0 of 10 | 2.0 | 36.3 | 31.3 | 5.7 |
| `packaging` | python tool + reference (elements used) | 10.0 of 10 | 3.0 | 16.7 | 6.7 | 0.7 |
| `packaging` | python tool + reference (search) | 9.0 of 10 | 4.7 | 45.7 | 20.7 | 25.0 |
| `rsa` | one python tool | 3.0 of 3 | 1.0 | 52.0 | 52.0 | 0.0 |
| `rsa` | python tool + reference (elements used) | 3.0 of 3 | 1.0 | 42.0 | 40.0 | 0.0 |
| `rsa` | python tool + reference (search) | 3.0 of 3 | 0.3 | 82.0 | 80.0 | 1.0 |

## By kind of answer

First run. A true-or-false question can be answered right by guessing half of the time.

| The answer is | Questions | No tools | One Python tool | Python tool + reference (elements used) | Python tool + reference (search) |
| --- | --- | --- | --- | --- | --- |
| true or false | 9 | 6 (67%) | 1 (11%) | 6 (67%) | 3 (33%) |
| another value | 53 | 5 (9%) | 19 (36%) | 25 (47%) | 17 (32%) |

## Question by question

First run. p is the exact two-sided sign test on the questions that only one of the two got right.

| A | B | Only A right | Only B right | p |
| --- | --- | --- | --- | --- |
| no tools | one python tool | 8 | 17 | 0.11 |
| no tools | python tool + reference (elements used) | 3 | 23 | 8.8e-05 |
| no tools | python tool + reference (search) | 6 | 15 | 0.078 |
| one python tool | python tool + reference (elements used) | 5 | 16 | 0.027 |
| one python tool | python tool + reference (search) | 13 | 13 | 1 |
| python tool + reference (elements used) | python tool + reference (search) | 17 | 6 | 0.035 |
