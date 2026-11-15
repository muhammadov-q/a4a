# Tools against no tools, on each library's own documentation questions (bench2)

A tool call that the model wrote as text is run as a call, and the Python tool's output is shown as text.

Model `qwen3-32b`. 7 repositories with every condition, 120 questions, 3 runs each. Right answers: no tools 70.0 (58%) (70, 70, 70); generated tools 63.7 (53%) (64, 63, 64); one python tool 81.0 (68%) (81, 81, 81).

A cell is the number of right answers: the mean of the runs, then each run in brackets.

| Package | Questions | Tools accepted | No tools | Generated tools | One Python tool |
| --- | --- | --- | --- | --- | --- |
| `dateutil` | 11 | 1 of 1 | 5.0 (5, 5, 5) | 5.0 (5, 5, 5) | 9.0 (9, 9, 9) |
| `mcp` | 15 | 0 of 54 | 12.0 (12, 12, 12) | none | none |
| `more_itertools` | 19 | 25 of 59 | 11.0 (11, 11, 11) | 10.0 (10, 10, 10) | 11.0 (11, 11, 11) |
| `networkx` | 20 | 3 of 45 | 6.0 (6, 6, 6) | 3.0 (3, 3, 3) | 16.0 (16, 16, 16) |
| `jinja2` | 9 | 11 of 58 | 7.0 (7, 7, 7) | 6.0 (6, 6, 6) | 3.0 (3, 3, 3) |
| `werkzeug` | 16 | 26 of 60 | 14.0 (14, 14, 14) | 11.0 (11, 11, 11) | 15.0 (15, 15, 15) |
| `packaging` | 28 | 41 of 60 | 19.0 (19, 19, 19) | 19.0 (19, 19, 19) | 15.0 (15, 15, 15) |
| `rsa` | 17 | 11 of 24 | 8.0 (8, 8, 8) | 9.7 (10, 9, 10) | 12.0 (12, 12, 12) |
| **7 repositories with every condition** | **120** | | **70.0 (58%) (70, 70, 70)** | **63.7 (53%) (64, 63, 64)** | **81.0 (68%) (81, 81, 81)** |

## How the tools were used

Means over the runs.

| Package | Condition | Questions with a tool call | Right among those | Tool calls | Calls that gave an error | Calls written as text, and run |
| --- | --- | --- | --- | --- | --- | --- |
| `dateutil` | generated tools | 9.0 of 11 | 4.0 | 9.0 | 2.0 | 1.0 |
| `dateutil` | one python tool | 11.0 of 11 | 9.0 | 11.0 | 1.0 | 0.0 |
| `more_itertools` | generated tools | 14.0 of 19 | 7.0 | 20.0 | 4.0 | 0.0 |
| `more_itertools` | one python tool | 19.0 of 19 | 11.0 | 21.0 | 5.0 | 0.0 |
| `networkx` | generated tools | 13.0 of 20 | 2.0 | 91.7 | 66.3 | 0.3 |
| `networkx` | one python tool | 20.0 of 20 | 16.0 | 20.0 | 2.0 | 0.0 |
| `jinja2` | generated tools | 3.0 of 9 | 2.0 | 4.0 | 0.0 | 0.0 |
| `jinja2` | one python tool | 9.0 of 9 | 3.0 | 9.0 | 1.0 | 0.0 |
| `werkzeug` | generated tools | 10.0 of 16 | 6.0 | 13.0 | 1.0 | 2.0 |
| `werkzeug` | one python tool | 16.0 of 16 | 15.0 | 16.0 | 1.0 | 0.0 |
| `packaging` | generated tools | 24.0 of 28 | 18.0 | 39.0 | 10.7 | 0.0 |
| `packaging` | one python tool | 28.0 of 28 | 15.0 | 33.0 | 14.3 | 0.0 |
| `rsa` | generated tools | 12.0 of 17 | 5.7 | 21.3 | 1.0 | 4.3 |
| `rsa` | one python tool | 17.0 of 17 | 12.0 | 17.0 | 2.0 | 0.0 |

## By kind of answer

First run. A true-or-false question can be answered right by guessing half of the time.

| The answer is | Questions | No tools | Generated tools | One Python tool |
| --- | --- | --- | --- | --- |
| true or false | 44 | 33 (75%) | 29 (66%) | 26 (59%) |
| another value | 76 | 37 (49%) | 35 (46%) | 55 (72%) |

## Question by question

First run. p is the exact two-sided sign test on the questions that only one of the two got right.

| A | B | Only A right | Only B right | p |
| --- | --- | --- | --- | --- |
| no tools | generated tools | 18 | 12 | 0.36 |
| no tools | one python tool | 17 | 28 | 0.14 |
| generated tools | one python tool | 19 | 36 | 0.03 |
