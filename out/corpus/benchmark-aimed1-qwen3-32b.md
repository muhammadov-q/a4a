# Tools against no tools, on the questions of out/corpus/tasks-aimed/ (aimed1)

A tool call that the model wrote as text is run as a call, and the Python tool's output is shown as text.

Model `qwen3-32b`. 7 repositories with every condition, 62 questions, 1 run each. Right answers: no tools 32 (52%); one python tool 39 (63%); python tool + reference (elements used) 52 (84%); python tool + reference (search) 49 (79%).

A cell is the number of right answers: the mean of the runs, then each run in brackets.

| Package | Questions | Tools accepted | No tools | One Python tool | Python tool + reference (elements used) | Python tool + reference (search) |
| --- | --- | --- | --- | --- | --- | --- |
| `dateutil` | 14 | none | 11 | 9.7 (9, 10, 10) | 13.0 (13, 13, 13) | 11.7 (12, 12, 11) |
| `mcp` | 4 | none | none | none | none | none |
| `more_itertools` | 5 | none | 2 | 1.3 (1, 1, 2) | 4.0 (4, 4, 4) | 4.0 (4, 4, 4) |
| `networkx` | 14 | none | 5 | 9.0 (9, 9, 9) | 11.3 (11, 12, 11) | 12.0 (12, 12, 12) |
| `jinja2` | 3 | none | 1 | 1.0 (1, 1, 1) | 2.0 (2, 2, 2) | 2.0 (2, 2, 2) |
| `werkzeug` | 13 | none | 7 | 9.0 (9, 9, 9) | 9.7 (9, 10, 10) | 7.0 (7, 7, 7) |
| `packaging` | 10 | none | 5 | 8.0 (8, 8, 8) | 10.0 (10, 10, 10) | 10.0 (10, 10, 10) |
| `rsa` | 3 | none | 1 | 2.0 (2, 2, 2) | 3.0 (3, 3, 3) | 2.0 (2, 2, 2) |
| **7 repositories with every condition** | **62** | | **32 (52%)** | **39 (63%)** | **52 (84%)** | **49 (79%)** |

## How the tools were used

Means over the runs.

| Package | Condition | Questions with a tool call | Right among those | Tool calls | Calls that gave an error | Calls written as text, and run |
| --- | --- | --- | --- | --- | --- | --- |
| `dateutil` | one python tool | 14.0 of 14 | 9.7 | 17.7 | 7.7 | 0.7 |
| `dateutil` | python tool + reference (elements used) | 14.0 of 14 | 13.0 | 14.0 | 1.0 | 0.0 |
| `dateutil` | python tool + reference (search) | 14.0 of 14 | 11.7 | 14.7 | 2.7 | 0.0 |
| `more_itertools` | one python tool | 5.0 of 5 | 1.3 | 6.7 | 1.7 | 1.0 |
| `more_itertools` | python tool + reference (elements used) | 5.0 of 5 | 4.0 | 5.0 | 0.0 | 0.0 |
| `more_itertools` | python tool + reference (search) | 5.0 of 5 | 4.0 | 6.0 | 1.0 | 1.0 |
| `networkx` | one python tool | 13.0 of 14 | 9.0 | 14.0 | 3.0 | 0.0 |
| `networkx` | python tool + reference (elements used) | 13.0 of 14 | 11.3 | 14.0 | 1.7 | 1.0 |
| `networkx` | python tool + reference (search) | 13.0 of 14 | 12.0 | 13.0 | 1.0 | 0.0 |
| `jinja2` | one python tool | 3.0 of 3 | 1.0 | 7.3 | 6.0 | 0.0 |
| `jinja2` | python tool + reference (elements used) | 3.0 of 3 | 2.0 | 3.0 | 1.0 | 0.0 |
| `jinja2` | python tool + reference (search) | 3.0 of 3 | 2.0 | 3.0 | 1.0 | 0.0 |
| `werkzeug` | one python tool | 13.0 of 13 | 9.0 | 19.7 | 9.7 | 0.0 |
| `werkzeug` | python tool + reference (elements used) | 13.0 of 13 | 9.7 | 13.0 | 2.0 | 0.0 |
| `werkzeug` | python tool + reference (search) | 13.0 of 13 | 7.0 | 14.0 | 2.0 | 1.0 |
| `packaging` | one python tool | 10.0 of 10 | 8.0 | 11.3 | 2.3 | 0.0 |
| `packaging` | python tool + reference (elements used) | 10.0 of 10 | 10.0 | 10.0 | 0.0 | 0.0 |
| `packaging` | python tool + reference (search) | 10.0 of 10 | 10.0 | 10.0 | 0.0 | 0.0 |
| `rsa` | one python tool | 3.0 of 3 | 2.0 | 3.0 | 0.0 | 0.0 |
| `rsa` | python tool + reference (elements used) | 3.0 of 3 | 3.0 | 3.0 | 0.0 | 0.0 |
| `rsa` | python tool + reference (search) | 3.0 of 3 | 2.0 | 3.0 | 1.0 | 0.0 |

## By kind of answer

First run. A true-or-false question can be answered right by guessing half of the time.

| The answer is | Questions | No tools | One Python tool | Python tool + reference (elements used) | Python tool + reference (search) |
| --- | --- | --- | --- | --- | --- |
| true or false | 9 | 7 (78%) | 5 (56%) | 8 (89%) | 7 (78%) |
| another value | 53 | 25 (47%) | 34 (64%) | 44 (83%) | 42 (79%) |

## Question by question

First run. p is the exact two-sided sign test on the questions that only one of the two got right.

| A | B | Only A right | Only B right | p |
| --- | --- | --- | --- | --- |
| no tools | one python tool | 6 | 13 | 0.17 |
| no tools | python tool + reference (elements used) | 5 | 25 | 0.00032 |
| no tools | python tool + reference (search) | 5 | 22 | 0.0015 |
| one python tool | python tool + reference (elements used) | 4 | 17 | 0.0072 |
| one python tool | python tool + reference (search) | 5 | 15 | 0.041 |
| python tool + reference (elements used) | python tool + reference (search) | 7 | 4 | 0.55 |
