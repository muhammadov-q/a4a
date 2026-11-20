# Tools against no tools, on each library's own documentation questions (bench2)

A tool call that the model wrote as text is run as a call, and the Python tool's output is shown as text.

Model `qwen3-8b`. 7 repositories with every condition, 120 questions, 3 runs each. Right answers: no tools 54.0 (45%) (54, 54, 54); generated tools 43.3 (36%) (44, 43, 43); one python tool 70.0 (58%) (70, 69, 71); python tool + reference (elements used) 89.3 (74%) (90, 89, 89); python tool + reference (search) 70.0 (58%) (71, 69, 70).

A cell is the number of right answers: the mean of the runs, then each run in brackets.

| Package | Questions | Tools accepted | No tools | Generated tools | One Python tool | Python tool + reference (elements used) | Python tool + reference (search) |
| --- | --- | --- | --- | --- | --- | --- | --- |
| `dateutil` | 11 | 1 of 1 | 4.0 (4, 4, 4) | 4.0 (4, 4, 4) | 6.7 (7, 6, 7) | 6.0 (6, 6, 6) | 3.0 (3, 3, 3) |
| `mcp` | 15 | 0 of 54 | 10.0 (10, 10, 10) | none | none | none | none |
| `more_itertools` | 19 | 25 of 59 | 10.0 (10, 10, 10) | 10.3 (10, 11, 10) | 13.0 (13, 13, 13) | 13.0 (13, 13, 13) | 11.0 (11, 11, 11) |
| `networkx` | 20 | 3 of 45 | 6.0 (6, 6, 6) | 0.0 (0, 0, 0) | 13.0 (13, 13, 13) | 15.3 (15, 16, 15) | 13.0 (13, 13, 13) |
| `jinja2` | 9 | 11 of 58 | 6.0 (6, 6, 6) | 6.0 (6, 6, 6) | 4.0 (3, 5, 4) | 4.0 (4, 4, 4) | 5.0 (5, 5, 5) |
| `werkzeug` | 16 | 26 of 60 | 7.0 (7, 7, 7) | 6.3 (7, 5, 7) | 14.0 (14, 14, 14) | 11.3 (12, 11, 11) | 10.3 (11, 10, 10) |
| `packaging` | 28 | 41 of 60 | 14.0 (14, 14, 14) | 9.7 (10, 10, 9) | 9.3 (10, 8, 10) | 25.7 (26, 25, 26) | 18.7 (19, 18, 19) |
| `rsa` | 17 | 11 of 24 | 7.0 (7, 7, 7) | 7.0 (7, 7, 7) | 10.0 (10, 10, 10) | 14.0 (14, 14, 14) | 9.0 (9, 9, 9) |
| **7 repositories with every condition** | **120** | | **54.0 (45%) (54, 54, 54)** | **43.3 (36%) (44, 43, 43)** | **70.0 (58%) (70, 69, 71)** | **89.3 (74%) (90, 89, 89)** | **70.0 (58%) (71, 69, 70)** |

## How the tools were used

Means over the runs.

| Package | Condition | Questions with a tool call | Right among those | Tool calls | Calls that gave an error | Calls written as text, and run |
| --- | --- | --- | --- | --- | --- | --- |
| `dateutil` | generated tools | 9.0 of 11 | 2.0 | 28.0 | 2.0 | 9.0 |
| `dateutil` | one python tool | 10.0 of 11 | 6.7 | 32.0 | 23.0 | 0.7 |
| `dateutil` | python tool + reference (elements used) | 10.0 of 11 | 6.0 | 52.0 | 44.0 | 0.0 |
| `dateutil` | python tool + reference (search) | 9.3 of 11 | 3.0 | 52.3 | 44.3 | 0.7 |
| `more_itertools` | generated tools | 10.3 of 19 | 5.3 | 128.3 | 7.0 | 104.0 |
| `more_itertools` | one python tool | 19.0 of 19 | 13.0 | 35.0 | 17.0 | 0.0 |
| `more_itertools` | python tool + reference (elements used) | 19.0 of 19 | 13.0 | 22.0 | 4.0 | 0.0 |
| `more_itertools` | python tool + reference (search) | 19.0 of 19 | 11.0 | 103.7 | 76.0 | 12.3 |
| `networkx` | generated tools | 11.7 of 20 | 0.0 | 167.0 | 161.3 | 106.3 |
| `networkx` | one python tool | 20.0 of 20 | 13.0 | 82.3 | 23.0 | 43.3 |
| `networkx` | python tool + reference (elements used) | 19.7 of 20 | 15.3 | 32.7 | 2.3 | 11.0 |
| `networkx` | python tool + reference (search) | 19.3 of 20 | 12.3 | 64.3 | 2.0 | 43.0 |
| `jinja2` | generated tools | 3.0 of 9 | 2.0 | 44.0 | 1.0 | 37.0 |
| `jinja2` | one python tool | 9.0 of 9 | 4.0 | 67.3 | 58.3 | 20.3 |
| `jinja2` | python tool + reference (elements used) | 9.0 of 9 | 4.0 | 9.0 | 0.0 | 0.0 |
| `jinja2` | python tool + reference (search) | 9.0 of 9 | 5.0 | 14.0 | 0.0 | 5.0 |
| `werkzeug` | generated tools | 11.0 of 16 | 4.3 | 88.7 | 6.0 | 42.3 |
| `werkzeug` | one python tool | 16.0 of 16 | 14.0 | 34.0 | 6.0 | 12.0 |
| `werkzeug` | python tool + reference (elements used) | 16.0 of 16 | 11.3 | 57.0 | 1.0 | 40.0 |
| `werkzeug` | python tool + reference (search) | 16.0 of 16 | 10.3 | 54.0 | 0.0 | 38.0 |
| `packaging` | generated tools | 24.0 of 28 | 9.7 | 120.0 | 40.7 | 62.7 |
| `packaging` | one python tool | 28.0 of 28 | 9.3 | 232.7 | 221.7 | 50.7 |
| `packaging` | python tool + reference (elements used) | 28.0 of 28 | 25.7 | 52.0 | 22.7 | 2.0 |
| `packaging` | python tool + reference (search) | 28.0 of 28 | 18.7 | 48.0 | 14.3 | 8.7 |
| `rsa` | generated tools | 10.0 of 17 | 5.0 | 30.7 | 0.0 | 15.7 |
| `rsa` | one python tool | 16.0 of 17 | 10.0 | 27.3 | 9.3 | 0.0 |
| `rsa` | python tool + reference (elements used) | 17.0 of 17 | 14.0 | 59.0 | 41.0 | 3.0 |
| `rsa` | python tool + reference (search) | 17.0 of 17 | 9.0 | 19.0 | 1.0 | 3.0 |

## By kind of answer

First run. A true-or-false question can be answered right by guessing half of the time.

| The answer is | Questions | No tools | Generated tools | One Python tool | Python tool + reference (elements used) | Python tool + reference (search) |
| --- | --- | --- | --- | --- | --- | --- |
| true or false | 44 | 27 (61%) | 18 (41%) | 19 (43%) | 31 (70%) | 24 (55%) |
| another value | 76 | 27 (36%) | 26 (34%) | 51 (67%) | 59 (78%) | 47 (62%) |

## Question by question

First run. p is the exact two-sided sign test on the questions that only one of the two got right.

| A | B | Only A right | Only B right | p |
| --- | --- | --- | --- | --- |
| no tools | generated tools | 25 | 15 | 0.15 |
| no tools | one python tool | 14 | 30 | 0.023 |
| no tools | python tool + reference (elements used) | 11 | 47 | 2e-06 |
| no tools | python tool + reference (search) | 15 | 32 | 0.019 |
| generated tools | one python tool | 12 | 38 | 0.00031 |
| generated tools | python tool + reference (elements used) | 9 | 55 | 3.5e-09 |
| generated tools | python tool + reference (search) | 12 | 39 | 0.0002 |
| one python tool | python tool + reference (elements used) | 11 | 31 | 0.0029 |
| one python tool | python tool + reference (search) | 19 | 20 | 1 |
| python tool + reference (elements used) | python tool + reference (search) | 25 | 6 | 0.00088 |
