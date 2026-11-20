# Tools against no tools, on the questions of out/corpus/tasks-aimed/ (aimed1)

A tool call that the model wrote as text is run as a call, and the Python tool's output is shown as text.

Model `qwen3-4b`. 7 repositories with every condition, 62 questions, 3 runs each. Right answers: no tools 23.0 (37%) (23, 23, 23); one python tool 32.3 (52%) (33, 33, 31); python tool + reference (elements used) 51.0 (82%) (50, 51, 52); python tool + reference (search) 42.0 (68%) (42, 43, 41).

A cell is the number of right answers: the mean of the runs, then each run in brackets.

| Package | Questions | Tools accepted | No tools | One Python tool | Python tool + reference (elements used) | Python tool + reference (search) |
| --- | --- | --- | --- | --- | --- | --- |
| `dateutil` | 14 | none | 8.0 (8, 8, 8) | 7.3 (7, 8, 7) | 13.0 (13, 13, 13) | 10.7 (10, 12, 10) |
| `mcp` | 4 | none | none | none | none | none |
| `more_itertools` | 5 | none | 2.0 (2, 2, 2) | 3.0 (3, 3, 3) | 3.0 (3, 3, 3) | 4.0 (4, 4, 4) |
| `networkx` | 14 | none | 5.0 (5, 5, 5) | 8.7 (9, 9, 8) | 11.0 (11, 11, 11) | 11.0 (11, 11, 11) |
| `jinja2` | 3 | none | 1.0 (1, 1, 1) | 0.0 (0, 0, 0) | 2.0 (2, 2, 2) | 1.0 (1, 1, 1) |
| `werkzeug` | 13 | none | 3.0 (3, 3, 3) | 6.0 (6, 6, 6) | 10.7 (10, 11, 11) | 7.0 (7, 7, 7) |
| `packaging` | 10 | none | 3.0 (3, 3, 3) | 6.0 (6, 6, 6) | 9.3 (9, 9, 10) | 7.3 (8, 7, 7) |
| `rsa` | 3 | none | 1.0 (1, 1, 1) | 1.3 (2, 1, 1) | 2.0 (2, 2, 2) | 1.0 (1, 1, 1) |
| **7 repositories with every condition** | **62** | | **23.0 (37%) (23, 23, 23)** | **32.3 (52%) (33, 33, 31)** | **51.0 (82%) (50, 51, 52)** | **42.0 (68%) (42, 43, 41)** |

## How the tools were used

Means over the runs.

| Package | Condition | Questions with a tool call | Right among those | Tool calls | Calls that gave an error | Calls written as text, and run |
| --- | --- | --- | --- | --- | --- | --- |
| `dateutil` | one python tool | 13.0 of 14 | 7.3 | 171.3 | 164.7 | 33.0 |
| `dateutil` | python tool + reference (elements used) | 14.0 of 14 | 13.0 | 62.7 | 49.7 | 0.0 |
| `dateutil` | python tool + reference (search) | 14.0 of 14 | 10.7 | 77.7 | 66.0 | 1.3 |
| `more_itertools` | one python tool | 5.0 of 5 | 3.0 | 23.7 | 20.3 | 2.3 |
| `more_itertools` | python tool + reference (elements used) | 5.0 of 5 | 3.0 | 5.0 | 0.0 | 0.0 |
| `more_itertools` | python tool + reference (search) | 5.0 of 5 | 4.0 | 5.0 | 0.0 | 0.0 |
| `networkx` | one python tool | 14.0 of 14 | 8.7 | 27.7 | 16.7 | 0.0 |
| `networkx` | python tool + reference (elements used) | 14.0 of 14 | 11.0 | 56.0 | 43.0 | 0.0 |
| `networkx` | python tool + reference (search) | 14.0 of 14 | 11.0 | 20.3 | 9.0 | 0.0 |
| `jinja2` | one python tool | 3.0 of 3 | 0.0 | 7.0 | 6.0 | 0.0 |
| `jinja2` | python tool + reference (elements used) | 3.0 of 3 | 2.0 | 11.7 | 9.7 | 0.0 |
| `jinja2` | python tool + reference (search) | 3.0 of 3 | 1.0 | 20.7 | 19.7 | 3.0 |
| `werkzeug` | one python tool | 13.0 of 13 | 6.0 | 34.3 | 25.3 | 0.0 |
| `werkzeug` | python tool + reference (elements used) | 13.0 of 13 | 10.7 | 52.0 | 40.0 | 0.0 |
| `werkzeug` | python tool + reference (search) | 13.0 of 13 | 7.0 | 101.0 | 91.0 | 2.3 |
| `packaging` | one python tool | 10.0 of 10 | 6.0 | 12.3 | 5.3 | 0.0 |
| `packaging` | python tool + reference (elements used) | 10.0 of 10 | 9.3 | 14.0 | 3.0 | 1.0 |
| `packaging` | python tool + reference (search) | 10.0 of 10 | 7.3 | 18.3 | 8.0 | 0.0 |
| `rsa` | one python tool | 3.0 of 3 | 1.3 | 55.7 | 54.7 | 19.7 |
| `rsa` | python tool + reference (elements used) | 3.0 of 3 | 2.0 | 40.7 | 38.7 | 0.0 |
| `rsa` | python tool + reference (search) | 3.0 of 3 | 1.0 | 75.7 | 74.7 | 42.7 |

## By kind of answer

First run. A true-or-false question can be answered right by guessing half of the time.

| The answer is | Questions | No tools | One Python tool | Python tool + reference (elements used) | Python tool + reference (search) |
| --- | --- | --- | --- | --- | --- |
| true or false | 9 | 6 (67%) | 3 (33%) | 8 (89%) | 7 (78%) |
| another value | 53 | 17 (32%) | 30 (57%) | 42 (79%) | 35 (66%) |

## Question by question

First run. p is the exact two-sided sign test on the questions that only one of the two got right.

| A | B | Only A right | Only B right | p |
| --- | --- | --- | --- | --- |
| no tools | one python tool | 8 | 18 | 0.076 |
| no tools | python tool + reference (elements used) | 3 | 30 | 1.4e-06 |
| no tools | python tool + reference (search) | 8 | 27 | 0.0019 |
| one python tool | python tool + reference (elements used) | 3 | 20 | 0.00049 |
| one python tool | python tool + reference (search) | 5 | 14 | 0.064 |
| python tool + reference (elements used) | python tool + reference (search) | 13 | 5 | 0.096 |
