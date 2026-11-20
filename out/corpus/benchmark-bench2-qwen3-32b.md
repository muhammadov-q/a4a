# Tools against no tools, on each library's own documentation questions (bench2)

A tool call that the model wrote as text is run as a call, and the Python tool's output is shown as text.

Model `qwen3-32b`. 7 repositories with every condition, 120 questions, 3 runs each. Right answers: no tools 70.0 (58%) (70, 70, 70); generated tools 63.7 (53%) (64, 63, 64); one python tool 81.0 (68%) (81, 81, 81); python tool + reference (elements used) 107.3 (89%) (108, 107, 107); python tool + reference (search) 101.7 (85%) (102, 101, 102).

A cell is the number of right answers: the mean of the runs, then each run in brackets.

| Package | Questions | Tools accepted | No tools | Generated tools | One Python tool | Python tool + reference (elements used) | Python tool + reference (search) |
| --- | --- | --- | --- | --- | --- | --- | --- |
| `dateutil` | 11 | 1 of 1 | 5.0 (5, 5, 5) | 5.0 (5, 5, 5) | 9.0 (9, 9, 9) | 10.0 (10, 10, 10) | 7.3 (7, 7, 8) |
| `mcp` | 15 | 0 of 54 | 12.0 (12, 12, 12) | none | none | none | none |
| `more_itertools` | 19 | 25 of 59 | 11.0 (11, 11, 11) | 10.0 (10, 10, 10) | 11.0 (11, 11, 11) | 18.0 (18, 18, 18) | 16.0 (16, 16, 16) |
| `networkx` | 20 | 3 of 45 | 6.0 (6, 6, 6) | 3.0 (3, 3, 3) | 16.0 (16, 16, 16) | 15.0 (15, 15, 15) | 15.3 (16, 15, 15) |
| `jinja2` | 9 | 11 of 58 | 7.0 (7, 7, 7) | 6.0 (6, 6, 6) | 3.0 (3, 3, 3) | 8.0 (8, 8, 8) | 9.0 (9, 9, 9) |
| `werkzeug` | 16 | 26 of 60 | 14.0 (14, 14, 14) | 11.0 (11, 11, 11) | 15.0 (15, 15, 15) | 15.0 (15, 15, 15) | 15.0 (15, 15, 15) |
| `packaging` | 28 | 41 of 60 | 19.0 (19, 19, 19) | 19.0 (19, 19, 19) | 15.0 (15, 15, 15) | 26.3 (27, 26, 26) | 24.0 (24, 24, 24) |
| `rsa` | 17 | 11 of 24 | 8.0 (8, 8, 8) | 9.7 (10, 9, 10) | 12.0 (12, 12, 12) | 15.0 (15, 15, 15) | 15.0 (15, 15, 15) |
| **7 repositories with every condition** | **120** | | **70.0 (58%) (70, 70, 70)** | **63.7 (53%) (64, 63, 64)** | **81.0 (68%) (81, 81, 81)** | **107.3 (89%) (108, 107, 107)** | **101.7 (85%) (102, 101, 102)** |

## How the tools were used

Means over the runs.

| Package | Condition | Questions with a tool call | Right among those | Tool calls | Calls that gave an error | Calls written as text, and run |
| --- | --- | --- | --- | --- | --- | --- |
| `dateutil` | generated tools | 9.0 of 11 | 4.0 | 9.0 | 2.0 | 1.0 |
| `dateutil` | one python tool | 11.0 of 11 | 9.0 | 11.0 | 1.0 | 0.0 |
| `dateutil` | python tool + reference (elements used) | 11.0 of 11 | 10.0 | 11.0 | 0.0 | 0.0 |
| `dateutil` | python tool + reference (search) | 11.0 of 11 | 7.3 | 12.7 | 3.7 | 0.0 |
| `more_itertools` | generated tools | 14.0 of 19 | 7.0 | 20.0 | 4.0 | 0.0 |
| `more_itertools` | one python tool | 19.0 of 19 | 11.0 | 21.0 | 5.0 | 0.0 |
| `more_itertools` | python tool + reference (elements used) | 19.0 of 19 | 18.0 | 19.0 | 0.0 | 0.0 |
| `more_itertools` | python tool + reference (search) | 19.0 of 19 | 16.0 | 19.0 | 1.0 | 0.0 |
| `networkx` | generated tools | 13.0 of 20 | 2.0 | 91.7 | 66.3 | 0.3 |
| `networkx` | one python tool | 20.0 of 20 | 16.0 | 20.0 | 2.0 | 0.0 |
| `networkx` | python tool + reference (elements used) | 20.0 of 20 | 15.0 | 21.0 | 2.0 | 0.0 |
| `networkx` | python tool + reference (search) | 20.0 of 20 | 15.3 | 22.0 | 3.0 | 1.0 |
| `jinja2` | generated tools | 3.0 of 9 | 2.0 | 4.0 | 0.0 | 0.0 |
| `jinja2` | one python tool | 9.0 of 9 | 3.0 | 9.0 | 1.0 | 0.0 |
| `jinja2` | python tool + reference (elements used) | 5.0 of 9 | 4.0 | 5.0 | 1.0 | 0.0 |
| `jinja2` | python tool + reference (search) | 8.0 of 9 | 8.0 | 8.0 | 0.0 | 0.0 |
| `werkzeug` | generated tools | 10.0 of 16 | 6.0 | 13.0 | 1.0 | 2.0 |
| `werkzeug` | one python tool | 16.0 of 16 | 15.0 | 16.0 | 1.0 | 0.0 |
| `werkzeug` | python tool + reference (elements used) | 16.0 of 16 | 15.0 | 16.0 | 0.0 | 0.0 |
| `werkzeug` | python tool + reference (search) | 16.0 of 16 | 15.0 | 17.0 | 2.0 | 0.0 |
| `packaging` | generated tools | 24.0 of 28 | 18.0 | 39.0 | 10.7 | 0.0 |
| `packaging` | one python tool | 28.0 of 28 | 15.0 | 33.0 | 14.3 | 0.0 |
| `packaging` | python tool + reference (elements used) | 28.0 of 28 | 26.3 | 30.0 | 2.7 | 0.0 |
| `packaging` | python tool + reference (search) | 28.0 of 28 | 24.0 | 33.0 | 6.0 | 1.0 |
| `rsa` | generated tools | 12.0 of 17 | 5.7 | 21.3 | 1.0 | 4.3 |
| `rsa` | one python tool | 17.0 of 17 | 12.0 | 17.0 | 2.0 | 0.0 |
| `rsa` | python tool + reference (elements used) | 17.0 of 17 | 15.0 | 17.0 | 0.0 | 0.0 |
| `rsa` | python tool + reference (search) | 17.0 of 17 | 15.0 | 17.0 | 1.0 | 0.0 |

## By kind of answer

First run. A true-or-false question can be answered right by guessing half of the time.

| The answer is | Questions | No tools | Generated tools | One Python tool | Python tool + reference (elements used) | Python tool + reference (search) |
| --- | --- | --- | --- | --- | --- | --- |
| true or false | 44 | 33 (75%) | 29 (66%) | 26 (59%) | 41 (93%) | 40 (91%) |
| another value | 76 | 37 (49%) | 35 (46%) | 55 (72%) | 67 (88%) | 62 (82%) |

## Question by question

First run. p is the exact two-sided sign test on the questions that only one of the two got right.

| A | B | Only A right | Only B right | p |
| --- | --- | --- | --- | --- |
| no tools | generated tools | 18 | 12 | 0.36 |
| no tools | one python tool | 17 | 28 | 0.14 |
| no tools | python tool + reference (elements used) | 1 | 39 | 7.5e-11 |
| no tools | python tool + reference (search) | 5 | 37 | 4.4e-07 |
| generated tools | one python tool | 19 | 36 | 0.03 |
| generated tools | python tool + reference (elements used) | 2 | 46 | 8.4e-12 |
| generated tools | python tool + reference (search) | 5 | 43 | 1.4e-08 |
| one python tool | python tool + reference (elements used) | 2 | 29 | 4.6e-07 |
| one python tool | python tool + reference (search) | 6 | 27 | 0.00032 |
| python tool + reference (elements used) | python tool + reference (search) | 11 | 5 | 0.21 |
