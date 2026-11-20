# Tools against no tools, on each library's own documentation questions (bench2)

A tool call that the model wrote as text is run as a call, and the Python tool's output is shown as text.

Model `qwen3-4b`. 7 repositories with every condition, 120 questions, 3 runs each. Right answers: no tools 48.7 (41%) (49, 48, 49); one python tool 65.3 (54%) (67, 67, 62); python tool + reference (elements used) 89.3 (74%) (89, 89, 90); python tool + reference (search) 81.0 (68%) (81, 81, 81).

A cell is the number of right answers: the mean of the runs, then each run in brackets.

| Package | Questions | Tools accepted | No tools | One Python tool | Python tool + reference (elements used) | Python tool + reference (search) |
| --- | --- | --- | --- | --- | --- | --- |
| `dateutil` | 11 | 1 of 1 | 2.0 (2, 2, 2) | 5.0 (5, 5, 5) | 4.3 (4, 4, 5) | 3.0 (3, 3, 3) |
| `mcp` | 15 | 0 of 54 | none | none | none | none |
| `more_itertools` | 19 | 25 of 59 | 7.7 (8, 7, 8) | 11.0 (11, 11, 11) | 16.3 (16, 17, 16) | 12.7 (14, 12, 12) |
| `networkx` | 20 | 3 of 45 | 4.0 (4, 4, 4) | 10.7 (12, 11, 9) | 12.0 (12, 12, 12) | 10.0 (9, 11, 10) |
| `jinja2` | 9 | 11 of 58 | 6.0 (6, 6, 6) | 1.7 (1, 3, 1) | 9.0 (9, 9, 9) | 9.0 (9, 9, 9) |
| `werkzeug` | 16 | 26 of 60 | 2.0 (2, 2, 2) | 14.0 (15, 14, 13) | 11.7 (12, 11, 12) | 10.0 (10, 10, 10) |
| `packaging` | 28 | 41 of 60 | 20.0 (20, 20, 20) | 12.0 (12, 12, 12) | 23.0 (23, 23, 23) | 22.3 (22, 22, 23) |
| `rsa` | 17 | 11 of 24 | 7.0 (7, 7, 7) | 11.0 (11, 11, 11) | 13.0 (13, 13, 13) | 14.0 (14, 14, 14) |
| **7 repositories with every condition** | **120** | | **48.7 (41%) (49, 48, 49)** | **65.3 (54%) (67, 67, 62)** | **89.3 (74%) (89, 89, 90)** | **81.0 (68%) (81, 81, 81)** |

## How the tools were used

Means over the runs.

| Package | Condition | Questions with a tool call | Right among those | Tool calls | Calls that gave an error | Calls written as text, and run |
| --- | --- | --- | --- | --- | --- | --- |
| `dateutil` | one python tool | 10.7 of 11 | 5.0 | 106.7 | 99.7 | 8.3 |
| `dateutil` | python tool + reference (elements used) | 10.7 of 11 | 4.3 | 104.0 | 96.3 | 11.3 |
| `dateutil` | python tool + reference (search) | 11.0 of 11 | 3.0 | 209.3 | 205.3 | 17.7 |
| `more_itertools` | one python tool | 19.0 of 19 | 11.0 | 98.3 | 83.7 | 16.0 |
| `more_itertools` | python tool + reference (elements used) | 19.0 of 19 | 16.3 | 29.3 | 11.3 | 4.3 |
| `more_itertools` | python tool + reference (search) | 19.0 of 19 | 12.7 | 51.0 | 19.3 | 4.3 |
| `networkx` | one python tool | 20.0 of 20 | 10.7 | 35.0 | 15.3 | 0.0 |
| `networkx` | python tool + reference (elements used) | 20.0 of 20 | 12.0 | 59.0 | 40.0 | 0.0 |
| `networkx` | python tool + reference (search) | 20.0 of 20 | 10.0 | 45.3 | 26.3 | 0.0 |
| `jinja2` | one python tool | 9.0 of 9 | 1.7 | 92.3 | 87.7 | 1.7 |
| `jinja2` | python tool + reference (elements used) | 9.0 of 9 | 9.0 | 9.0 | 0.0 | 0.0 |
| `jinja2` | python tool + reference (search) | 9.0 of 9 | 9.0 | 9.0 | 0.0 | 0.0 |
| `werkzeug` | one python tool | 16.0 of 16 | 14.0 | 27.0 | 12.0 | 7.0 |
| `werkzeug` | python tool + reference (elements used) | 16.0 of 16 | 11.7 | 80.7 | 67.0 | 20.7 |
| `werkzeug` | python tool + reference (search) | 16.0 of 16 | 10.0 | 62.3 | 47.7 | 0.0 |
| `packaging` | one python tool | 28.0 of 28 | 12.0 | 326.7 | 313.7 | 48.3 |
| `packaging` | python tool + reference (elements used) | 28.0 of 28 | 23.0 | 151.3 | 127.3 | 2.0 |
| `packaging` | python tool + reference (search) | 28.0 of 28 | 22.3 | 113.7 | 89.3 | 28.0 |
| `rsa` | one python tool | 17.0 of 17 | 11.0 | 69.0 | 57.0 | 0.7 |
| `rsa` | python tool + reference (elements used) | 17.0 of 17 | 13.0 | 56.0 | 41.7 | 0.0 |
| `rsa` | python tool + reference (search) | 17.0 of 17 | 14.0 | 57.7 | 41.7 | 0.0 |

## By kind of answer

First run. A true-or-false question can be answered right by guessing half of the time.

| The answer is | Questions | No tools | One Python tool | Python tool + reference (elements used) | Python tool + reference (search) |
| --- | --- | --- | --- | --- | --- |
| true or false | 44 | 31 (70%) | 19 (43%) | 37 (84%) | 38 (86%) |
| another value | 76 | 18 (24%) | 48 (63%) | 52 (68%) | 43 (57%) |

## Question by question

First run. p is the exact two-sided sign test on the questions that only one of the two got right.

| A | B | Only A right | Only B right | p |
| --- | --- | --- | --- | --- |
| no tools | one python tool | 18 | 36 | 0.02 |
| no tools | python tool + reference (elements used) | 6 | 46 | 1e-08 |
| no tools | python tool + reference (search) | 7 | 39 | 1.8e-06 |
| one python tool | python tool + reference (elements used) | 11 | 33 | 0.0013 |
| one python tool | python tool + reference (search) | 17 | 31 | 0.059 |
| python tool + reference (elements used) | python tool + reference (search) | 16 | 8 | 0.15 |
