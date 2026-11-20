# Tools against no tools, on each library's own documentation questions (bench2)

A tool call that the model wrote as text is run as a call, and the Python tool's output is shown as text.

Model `qwen3-4b-rec4-f2`. 3 repositories with every condition, 67 questions, 3 runs each. Right answers: no tools 32.0 (48%) (32, 32, 32); one python tool 35.7 (53%) (36, 36, 35).

A cell is the number of right answers: the mean of the runs, then each run in brackets.

| Package | Questions | Tools accepted | No tools | One Python tool |
| --- | --- | --- | --- | --- |
| `dateutil` | 11 | 1 of 1 | none | none |
| `mcp` | 15 | 0 of 54 | none | none |
| `more_itertools` | 19 | 25 of 59 | 7.0 (7, 7, 7) | 9.0 (9, 9, 9) |
| `networkx` | 20 | 3 of 45 | 6.0 (6, 6, 6) | 14.0 (14, 14, 14) |
| `jinja2` | 9 | 11 of 58 | none | none |
| `werkzeug` | 16 | 26 of 60 | none | none |
| `packaging` | 28 | 41 of 60 | 19.0 (19, 19, 19) | 12.7 (13, 13, 12) |
| `rsa` | 17 | 11 of 24 | none | none |
| **3 repositories with every condition** | **67** | | **32.0 (48%) (32, 32, 32)** | **35.7 (53%) (36, 36, 35)** |

## How the tools were used

Means over the runs.

| Package | Condition | Questions with a tool call | Right among those | Tool calls | Calls that gave an error | Calls written as text, and run |
| --- | --- | --- | --- | --- | --- | --- |
| `more_itertools` | one python tool | 19.0 of 19 | 9.0 | 107.7 | 95.7 | 0.0 |
| `networkx` | one python tool | 20.0 of 20 | 14.0 | 71.0 | 53.0 | 0.0 |
| `packaging` | one python tool | 27.0 of 28 | 11.7 | 125.3 | 118.3 | 0.0 |

## By kind of answer

First run. A true-or-false question can be answered right by guessing half of the time.

| The answer is | Questions | No tools | One Python tool |
| --- | --- | --- | --- |
| true or false | 30 | 18 (60%) | 16 (53%) |
| another value | 37 | 14 (38%) | 20 (54%) |

## Question by question

First run. p is the exact two-sided sign test on the questions that only one of the two got right.

| A | B | Only A right | Only B right | p |
| --- | --- | --- | --- | --- |
| no tools | one python tool | 10 | 14 | 0.54 |
