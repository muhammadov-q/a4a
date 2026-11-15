# Tools against no tools, on each library's own documentation questions (bench2)

A tool call that the model wrote as text is run as a call, and the Python tool's output is shown as text.

Model `qwen3-8b`. 7 repositories with every condition, 120 questions, 3 runs each. Right answers: no tools 54.0 (45%) (54, 54, 54); generated tools 43.3 (36%) (44, 43, 43); one python tool 70.0 (58%) (70, 69, 71).

A cell is the number of right answers: the mean of the runs, then each run in brackets.

| Package | Questions | Tools accepted | No tools | Generated tools | One Python tool |
| --- | --- | --- | --- | --- | --- |
| `dateutil` | 11 | 1 of 1 | 4.0 (4, 4, 4) | 4.0 (4, 4, 4) | 6.7 (7, 6, 7) |
| `mcp` | 15 | 0 of 54 | 10.0 (10, 10, 10) | none | none |
| `more_itertools` | 19 | 25 of 59 | 10.0 (10, 10, 10) | 10.3 (10, 11, 10) | 13.0 (13, 13, 13) |
| `networkx` | 20 | 3 of 45 | 6.0 (6, 6, 6) | 0.0 (0, 0, 0) | 13.0 (13, 13, 13) |
| `jinja2` | 9 | 11 of 58 | 6.0 (6, 6, 6) | 6.0 (6, 6, 6) | 4.0 (3, 5, 4) |
| `werkzeug` | 16 | 26 of 60 | 7.0 (7, 7, 7) | 6.3 (7, 5, 7) | 14.0 (14, 14, 14) |
| `packaging` | 28 | 41 of 60 | 14.0 (14, 14, 14) | 9.7 (10, 10, 9) | 9.3 (10, 8, 10) |
| `rsa` | 17 | 11 of 24 | 7.0 (7, 7, 7) | 7.0 (7, 7, 7) | 10.0 (10, 10, 10) |
| **7 repositories with every condition** | **120** | | **54.0 (45%) (54, 54, 54)** | **43.3 (36%) (44, 43, 43)** | **70.0 (58%) (70, 69, 71)** |

## How the tools were used

Means over the runs.

| Package | Condition | Questions with a tool call | Right among those | Tool calls | Calls that gave an error | Calls written as text, and run |
| --- | --- | --- | --- | --- | --- | --- |
| `dateutil` | generated tools | 9.0 of 11 | 2.0 | 28.0 | 2.0 | 9.0 |
| `dateutil` | one python tool | 10.0 of 11 | 6.7 | 32.0 | 23.0 | 0.7 |
| `more_itertools` | generated tools | 10.3 of 19 | 5.3 | 128.3 | 7.0 | 104.0 |
| `more_itertools` | one python tool | 19.0 of 19 | 13.0 | 35.0 | 17.0 | 0.0 |
| `networkx` | generated tools | 11.7 of 20 | 0.0 | 167.0 | 161.3 | 106.3 |
| `networkx` | one python tool | 20.0 of 20 | 13.0 | 82.3 | 23.0 | 43.3 |
| `jinja2` | generated tools | 3.0 of 9 | 2.0 | 44.0 | 1.0 | 37.0 |
| `jinja2` | one python tool | 9.0 of 9 | 4.0 | 67.3 | 58.3 | 20.3 |
| `werkzeug` | generated tools | 11.0 of 16 | 4.3 | 88.7 | 6.0 | 42.3 |
| `werkzeug` | one python tool | 16.0 of 16 | 14.0 | 34.0 | 6.0 | 12.0 |
| `packaging` | generated tools | 24.0 of 28 | 9.7 | 120.0 | 40.7 | 62.7 |
| `packaging` | one python tool | 28.0 of 28 | 9.3 | 232.7 | 221.7 | 50.7 |
| `rsa` | generated tools | 10.0 of 17 | 5.0 | 30.7 | 0.0 | 15.7 |
| `rsa` | one python tool | 16.0 of 17 | 10.0 | 27.3 | 9.3 | 0.0 |

## By kind of answer

First run. A true-or-false question can be answered right by guessing half of the time.

| The answer is | Questions | No tools | Generated tools | One Python tool |
| --- | --- | --- | --- | --- |
| true or false | 44 | 27 (61%) | 18 (41%) | 19 (43%) |
| another value | 76 | 27 (36%) | 26 (34%) | 51 (67%) |

## Question by question

First run. p is the exact two-sided sign test on the questions that only one of the two got right.

| A | B | Only A right | Only B right | p |
| --- | --- | --- | --- | --- |
| no tools | generated tools | 25 | 15 | 0.15 |
| no tools | one python tool | 14 | 30 | 0.023 |
| generated tools | one python tool | 12 | 38 | 0.00031 |
