# Tools against no tools, on each library's own documentation questions (bench2, strict harness)

Strict harness: a tool call that the model wrote as text was taken as its answer, and the Python tool's output was shown as a JSON string.

Model `qwen3-8b`. 7 repositories with every condition, 120 questions, 3 runs each. Right answers: no tools 54.0 (45%) (54, 54, 54); generated tools 35.0 (29%) (34, 35, 36); one python tool 63.3 (53%) (63, 63, 64).

A cell is the number of right answers: the mean of the runs, then each run in brackets.

| Package | Questions | Tools accepted | No tools | Generated tools | One Python tool |
| --- | --- | --- | --- | --- | --- |
| `dateutil` | 11 | 1 of 1 | 4.0 (4, 4, 4) | 3.0 (3, 3, 3) | 6.7 (6, 7, 7) |
| `mcp` | 15 | 0 of 54 | 10.0 (10, 10, 10) | none | none |
| `more_itertools` | 19 | 25 of 59 | 10.0 (10, 10, 10) | 9.0 (9, 9, 9) | 12.0 (12, 12, 12) |
| `networkx` | 20 | 3 of 45 | 6.0 (6, 6, 6) | 0.0 (0, 0, 0) | 10.7 (10, 11, 11) |
| `jinja2` | 9 | 11 of 58 | 6.0 (6, 6, 6) | 6.0 (6, 6, 6) | 4.3 (3, 5, 5) |
| `werkzeug` | 16 | 26 of 60 | 7.0 (7, 7, 7) | 4.7 (4, 5, 5) | 12.0 (12, 12, 12) |
| `packaging` | 28 | 41 of 60 | 14.0 (14, 14, 14) | 8.3 (8, 8, 9) | 8.7 (11, 7, 8) |
| `rsa` | 17 | 11 of 24 | 7.0 (7, 7, 7) | 4.0 (4, 4, 4) | 9.0 (9, 9, 9) |
| **7 repositories with every condition** | **120** | | **54.0 (45%) (54, 54, 54)** | **35.0 (29%) (34, 35, 36)** | **63.3 (53%) (63, 63, 64)** |

## How the tools were used

Means over the runs.

| Package | Condition | Questions with a tool call | Right among those | Tool calls | Calls that gave an error | Ended with a call written as text |
| --- | --- | --- | --- | --- | --- | --- |
| `dateutil` | generated tools | 9.0 of 11 | 1.0 | 16.3 | 2.0 | 3.0 |
| `dateutil` | one python tool | 10.0 of 11 | 6.7 | 33.3 | 24.3 | 0.7 |
| `more_itertools` | generated tools | 10.0 of 19 | 4.0 | 24.0 | 5.0 | 5.0 |
| `more_itertools` | one python tool | 19.0 of 19 | 12.0 | 33.3 | 16.0 | 0.7 |
| `networkx` | generated tools | 12.0 of 20 | 0.0 | 50.0 | 43.7 | 3.3 |
| `networkx` | one python tool | 20.0 of 20 | 10.7 | 26.7 | 8.7 | 3.7 |
| `jinja2` | generated tools | 3.0 of 9 | 2.0 | 6.3 | 0.7 | 1.0 |
| `jinja2` | one python tool | 9.0 of 9 | 4.3 | 19.0 | 13.0 | 3.3 |
| `werkzeug` | generated tools | 11.0 of 16 | 2.7 | 46.0 | 4.0 | 4.3 |
| `werkzeug` | one python tool | 16.0 of 16 | 12.0 | 19.3 | 3.3 | 1.0 |
| `packaging` | generated tools | 22.3 of 28 | 8.3 | 53.3 | 21.3 | 7.3 |
| `packaging` | one python tool | 28.0 of 28 | 8.7 | 136.7 | 127.3 | 6.3 |
| `rsa` | generated tools | 6.7 of 17 | 2.0 | 12.7 | 0.0 | 5.0 |
| `rsa` | one python tool | 16.0 of 17 | 9.0 | 26.7 | 8.7 | 0.0 |

## By kind of answer

First run. A true-or-false question can be answered right by guessing half of the time.

| The answer is | Questions | No tools | Generated tools | One Python tool |
| --- | --- | --- | --- | --- |
| true or false | 44 | 27 (61%) | 16 (36%) | 17 (39%) |
| another value | 76 | 27 (36%) | 18 (24%) | 46 (61%) |

## Question by question

First run. p is the exact two-sided sign test on the questions that only one of the two got right.

| A | B | Only A right | Only B right | p |
| --- | --- | --- | --- | --- |
| no tools | generated tools | 30 | 10 | 0.0022 |
| no tools | one python tool | 18 | 27 | 0.2327 |
| generated tools | one python tool | 8 | 37 | 0.0000 |
