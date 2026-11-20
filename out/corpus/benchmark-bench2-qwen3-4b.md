# Tools against no tools, on each library's own documentation questions (bench2)

A tool call that the model wrote as text is run as a call, and the Python tool's output is shown as text.

Model `qwen3-4b`. 7 repositories with every condition, 120 questions, 3 runs each. Right answers: no tools 48.7 (41%) (49, 48, 49); one python tool 65.3 (54%) (67, 67, 62).

A cell is the number of right answers: the mean of the runs, then each run in brackets.

| Package | Questions | Tools accepted | No tools | One Python tool |
| --- | --- | --- | --- | --- |
| `dateutil` | 11 | 1 of 1 | 2.0 (2, 2, 2) | 5.0 (5, 5, 5) |
| `mcp` | 15 | 0 of 54 | none | none |
| `more_itertools` | 19 | 25 of 59 | 7.7 (8, 7, 8) | 11.0 (11, 11, 11) |
| `networkx` | 20 | 3 of 45 | 4.0 (4, 4, 4) | 10.7 (12, 11, 9) |
| `jinja2` | 9 | 11 of 58 | 6.0 (6, 6, 6) | 1.7 (1, 3, 1) |
| `werkzeug` | 16 | 26 of 60 | 2.0 (2, 2, 2) | 14.0 (15, 14, 13) |
| `packaging` | 28 | 41 of 60 | 20.0 (20, 20, 20) | 12.0 (12, 12, 12) |
| `rsa` | 17 | 11 of 24 | 7.0 (7, 7, 7) | 11.0 (11, 11, 11) |
| **7 repositories with every condition** | **120** | | **48.7 (41%) (49, 48, 49)** | **65.3 (54%) (67, 67, 62)** |

## How the tools were used

Means over the runs.

| Package | Condition | Questions with a tool call | Right among those | Tool calls | Calls that gave an error | Calls written as text, and run |
| --- | --- | --- | --- | --- | --- | --- |
| `dateutil` | one python tool | 10.7 of 11 | 5.0 | 106.7 | 99.7 | 8.3 |
| `more_itertools` | one python tool | 19.0 of 19 | 11.0 | 98.3 | 83.7 | 16.0 |
| `networkx` | one python tool | 20.0 of 20 | 10.7 | 35.0 | 15.3 | 0.0 |
| `jinja2` | one python tool | 9.0 of 9 | 1.7 | 92.3 | 87.7 | 1.7 |
| `werkzeug` | one python tool | 16.0 of 16 | 14.0 | 27.0 | 12.0 | 7.0 |
| `packaging` | one python tool | 28.0 of 28 | 12.0 | 326.7 | 313.7 | 48.3 |
| `rsa` | one python tool | 17.0 of 17 | 11.0 | 69.0 | 57.0 | 0.7 |

## By kind of answer

First run. A true-or-false question can be answered right by guessing half of the time.

| The answer is | Questions | No tools | One Python tool |
| --- | --- | --- | --- |
| true or false | 44 | 31 (70%) | 19 (43%) |
| another value | 76 | 18 (24%) | 48 (63%) |

## Question by question

First run. p is the exact two-sided sign test on the questions that only one of the two got right.

| A | B | Only A right | Only B right | p |
| --- | --- | --- | --- | --- |
| no tools | one python tool | 18 | 36 | 0.02 |
