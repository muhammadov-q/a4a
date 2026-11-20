# Tools against no tools, on the questions of out/corpus/tasks-aimed/ (aimed1)

A tool call that the model wrote as text is run as a call, and the Python tool's output is shown as text.

Model `qwen3-8b`. 7 repositories with every condition, 62 questions, 1 run each. Right answers: no tools 25 (40%); one python tool 38 (61%); python tool + reference (elements used) 50 (81%); python tool + reference (search) 43 (69%).

A cell is the number of right answers: the mean of the runs, then each run in brackets.

| Package | Questions | Tools accepted | No tools | One Python tool | Python tool + reference (elements used) | Python tool + reference (search) |
| --- | --- | --- | --- | --- | --- | --- |
| `dateutil` | 14 | none | 10 | 8.0 (8, 8, 8) | 11.0 (11, 11, 11) | 9.7 (9, 10, 10) |
| `mcp` | 4 | none | none | none | none | none |
| `more_itertools` | 5 | none | 3 | 2.0 (2, 2, 2) | 4.0 (4, 4, 4) | 4.0 (4, 4, 4) |
| `networkx` | 14 | none | 2 | 10.3 (11, 10, 10) | 14.0 (14, 14, 14) | 13.0 (13, 13, 13) |
| `jinja2` | 3 | none | 1 | 1.0 (1, 1, 1) | 1.0 (1, 1, 1) | 0.7 (0, 1, 1) |
| `werkzeug` | 13 | none | 5 | 6.3 (7, 6, 6) | 8.3 (8, 8, 9) | 8.3 (9, 8, 8) |
| `packaging` | 10 | none | 3 | 4.7 (6, 4, 4) | 9.0 (9, 9, 9) | 7.3 (7, 8, 7) |
| `rsa` | 3 | none | 1 | 3.0 (3, 3, 3) | 3.0 (3, 3, 3) | 1.0 (1, 1, 1) |
| **7 repositories with every condition** | **62** | | **25 (40%)** | **38 (61%)** | **50 (81%)** | **43 (69%)** |

## How the tools were used

Means over the runs.

| Package | Condition | Questions with a tool call | Right among those | Tool calls | Calls that gave an error | Calls written as text, and run |
| --- | --- | --- | --- | --- | --- | --- |
| `dateutil` | one python tool | 14.0 of 14 | 8.0 | 60.0 | 50.0 | 21.0 |
| `dateutil` | python tool + reference (elements used) | 14.0 of 14 | 11.0 | 55.0 | 42.0 | 0.0 |
| `dateutil` | python tool + reference (search) | 14.0 of 14 | 9.7 | 111.0 | 96.3 | 3.0 |
| `more_itertools` | one python tool | 5.0 of 5 | 2.0 | 13.3 | 8.3 | 0.0 |
| `more_itertools` | python tool + reference (elements used) | 5.0 of 5 | 4.0 | 8.0 | 4.0 | 0.0 |
| `more_itertools` | python tool + reference (search) | 5.0 of 5 | 4.0 | 5.3 | 0.3 | 0.0 |
| `networkx` | one python tool | 14.0 of 14 | 10.3 | 39.7 | 28.3 | 0.0 |
| `networkx` | python tool + reference (elements used) | 14.0 of 14 | 14.0 | 17.0 | 3.0 | 0.0 |
| `networkx` | python tool + reference (search) | 14.0 of 14 | 13.0 | 17.0 | 2.0 | 1.0 |
| `jinja2` | one python tool | 3.0 of 3 | 1.0 | 9.7 | 7.7 | 2.0 |
| `jinja2` | python tool + reference (elements used) | 2.0 of 3 | 1.0 | 41.0 | 40.0 | 0.0 |
| `jinja2` | python tool + reference (search) | 3.0 of 3 | 0.7 | 74.7 | 48.7 | 24.7 |
| `werkzeug` | one python tool | 13.0 of 13 | 6.3 | 99.0 | 91.0 | 64.7 |
| `werkzeug` | python tool + reference (elements used) | 13.0 of 13 | 8.3 | 18.3 | 6.0 | 3.3 |
| `werkzeug` | python tool + reference (search) | 13.0 of 13 | 8.3 | 51.0 | 16.0 | 23.0 |
| `packaging` | one python tool | 10.0 of 10 | 4.7 | 22.0 | 13.7 | 0.0 |
| `packaging` | python tool + reference (elements used) | 10.0 of 10 | 9.0 | 10.0 | 0.0 | 0.0 |
| `packaging` | python tool + reference (search) | 10.0 of 10 | 7.3 | 45.0 | 2.0 | 33.0 |
| `rsa` | one python tool | 3.0 of 3 | 3.0 | 11.0 | 8.0 | 0.0 |
| `rsa` | python tool + reference (elements used) | 3.0 of 3 | 3.0 | 3.0 | 0.0 | 0.0 |
| `rsa` | python tool + reference (search) | 3.0 of 3 | 1.0 | 24.0 | 23.0 | 14.0 |

## By kind of answer

First run. A true-or-false question can be answered right by guessing half of the time.

| The answer is | Questions | No tools | One Python tool | Python tool + reference (elements used) | Python tool + reference (search) |
| --- | --- | --- | --- | --- | --- |
| true or false | 9 | 5 (56%) | 4 (44%) | 6 (67%) | 4 (44%) |
| another value | 53 | 20 (38%) | 34 (64%) | 44 (83%) | 39 (74%) |

## Question by question

First run. p is the exact two-sided sign test on the questions that only one of the two got right.

| A | B | Only A right | Only B right | p |
| --- | --- | --- | --- | --- |
| no tools | one python tool | 7 | 20 | 0.019 |
| no tools | python tool + reference (elements used) | 6 | 31 | 4.1e-05 |
| no tools | python tool + reference (search) | 8 | 26 | 0.0029 |
| one python tool | python tool + reference (elements used) | 3 | 15 | 0.0075 |
| one python tool | python tool + reference (search) | 10 | 15 | 0.42 |
| python tool + reference (elements used) | python tool + reference (search) | 11 | 4 | 0.12 |
