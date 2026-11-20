# Tools against no tools, on each library's own documentation questions (bench2)

A tool call that the model wrote as text is run as a call, and the Python tool's output is shown as text.

Model `qwen3-1.7b`. 7 repositories with every condition, 120 questions, 3 runs each. Right answers: no tools 32.7 (27%) (32, 33, 33); one python tool 42.0 (35%) (44, 41, 41); python tool + reference (elements used) 39.0 (32%) (38, 40, 39); python tool + reference (search) 38.0 (32%) (38, 37, 39).

A cell is the number of right answers: the mean of the runs, then each run in brackets.

| Package | Questions | Tools accepted | No tools | One Python tool | Python tool + reference (elements used) | Python tool + reference (search) |
| --- | --- | --- | --- | --- | --- | --- |
| `dateutil` | 11 | 1 of 1 | 1.0 (1, 1, 1) | 2.3 (3, 2, 2) | 2.0 (2, 2, 2) | 0.0 (0, 0, 0) |
| `mcp` | 15 | 0 of 54 | none | none | none | none |
| `more_itertools` | 19 | 25 of 59 | 5.3 (5, 5, 6) | 7.3 (8, 7, 7) | 7.0 (7, 7, 7) | 5.7 (7, 5, 5) |
| `networkx` | 20 | 3 of 45 | 1.3 (1, 2, 1) | 6.7 (7, 6, 7) | 5.0 (5, 5, 5) | 7.0 (6, 7, 8) |
| `jinja2` | 9 | 11 of 58 | 5.0 (5, 5, 5) | 4.0 (4, 4, 4) | 1.3 (1, 2, 1) | 3.3 (3, 4, 3) |
| `werkzeug` | 16 | 26 of 60 | 3.0 (3, 3, 3) | 5.0 (5, 5, 5) | 5.3 (5, 5, 6) | 3.0 (2, 4, 3) |
| `packaging` | 28 | 41 of 60 | 15.0 (15, 15, 15) | 6.7 (7, 7, 6) | 7.3 (7, 8, 7) | 10.7 (12, 9, 11) |
| `rsa` | 17 | 11 of 24 | 2.0 (2, 2, 2) | 10.0 (10, 10, 10) | 11.0 (11, 11, 11) | 8.3 (8, 8, 9) |
| **7 repositories with every condition** | **120** | | **32.7 (27%) (32, 33, 33)** | **42.0 (35%) (44, 41, 41)** | **39.0 (32%) (38, 40, 39)** | **38.0 (32%) (38, 37, 39)** |

## How the tools were used

Means over the runs.

| Package | Condition | Questions with a tool call | Right among those | Tool calls | Calls that gave an error | Calls written as text, and run |
| --- | --- | --- | --- | --- | --- | --- |
| `dateutil` | one python tool | 10.3 of 11 | 2.3 | 183.0 | 179.0 | 96.3 |
| `dateutil` | python tool + reference (elements used) | 10.0 of 11 | 2.0 | 176.3 | 170.3 | 122.7 |
| `dateutil` | python tool + reference (search) | 8.3 of 11 | 0.0 | 253.3 | 213.0 | 185.7 |
| `more_itertools` | one python tool | 19.0 of 19 | 7.3 | 118.7 | 107.7 | 24.0 |
| `more_itertools` | python tool + reference (elements used) | 19.0 of 19 | 7.0 | 76.7 | 16.0 | 3.0 |
| `more_itertools` | python tool + reference (search) | 19.0 of 19 | 5.7 | 53.7 | 18.3 | 2.3 |
| `networkx` | one python tool | 19.7 of 20 | 6.7 | 318.0 | 302.7 | 127.7 |
| `networkx` | python tool + reference (elements used) | 18.7 of 20 | 5.0 | 265.7 | 213.0 | 168.0 |
| `networkx` | python tool + reference (search) | 20.0 of 20 | 7.0 | 216.0 | 199.7 | 147.7 |
| `jinja2` | one python tool | 9.0 of 9 | 4.0 | 57.7 | 51.7 | 2.7 |
| `jinja2` | python tool + reference (elements used) | 9.0 of 9 | 1.3 | 17.0 | 9.0 | 0.0 |
| `jinja2` | python tool + reference (search) | 9.0 of 9 | 3.3 | 35.3 | 27.7 | 0.0 |
| `werkzeug` | one python tool | 16.0 of 16 | 5.0 | 147.7 | 143.3 | 72.7 |
| `werkzeug` | python tool + reference (elements used) | 15.0 of 16 | 5.3 | 77.0 | 65.0 | 31.3 |
| `werkzeug` | python tool + reference (search) | 16.0 of 16 | 3.0 | 156.0 | 146.0 | 58.3 |
| `packaging` | one python tool | 27.7 of 28 | 6.7 | 363.7 | 348.0 | 156.3 |
| `packaging` | python tool + reference (elements used) | 27.3 of 28 | 7.3 | 397.3 | 354.7 | 150.7 |
| `packaging` | python tool + reference (search) | 25.3 of 28 | 10.7 | 319.7 | 301.7 | 147.3 |
| `rsa` | one python tool | 16.0 of 17 | 10.0 | 111.0 | 99.7 | 60.7 |
| `rsa` | python tool + reference (elements used) | 16.0 of 17 | 11.0 | 65.0 | 50.0 | 2.0 |
| `rsa` | python tool + reference (search) | 16.0 of 17 | 8.3 | 88.0 | 72.0 | 55.0 |

## By kind of answer

First run. A true-or-false question can be answered right by guessing half of the time.

| The answer is | Questions | No tools | One Python tool | Python tool + reference (elements used) | Python tool + reference (search) |
| --- | --- | --- | --- | --- | --- |
| true or false | 44 | 26 (59%) | 16 (36%) | 11 (25%) | 15 (34%) |
| another value | 76 | 6 (8%) | 28 (37%) | 27 (36%) | 23 (30%) |

## Question by question

First run. p is the exact two-sided sign test on the questions that only one of the two got right.

| A | B | Only A right | Only B right | p |
| --- | --- | --- | --- | --- |
| no tools | one python tool | 17 | 29 | 0.1 |
| no tools | python tool + reference (elements used) | 25 | 31 | 0.5 |
| no tools | python tool + reference (search) | 20 | 26 | 0.46 |
| one python tool | python tool + reference (elements used) | 21 | 15 | 0.41 |
| one python tool | python tool + reference (search) | 27 | 21 | 0.47 |
| python tool + reference (elements used) | python tool + reference (search) | 20 | 20 | 1 |
