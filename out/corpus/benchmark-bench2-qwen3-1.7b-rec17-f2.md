# Tools against no tools, on each library's own documentation questions (bench2)

A tool call that the model wrote as text is run as a call, and the Python tool's output is shown as text.

Model `qwen3-1.7b-rec17-f2`. 3 repositories with every condition, 67 questions, 3 runs each. Right answers: no tools 29.0 (43%) (29, 29, 29); one python tool 28.0 (42%) (27, 29, 28).

A cell is the number of right answers: the mean of the runs, then each run in brackets.

| Package | Questions | Tools accepted | No tools | One Python tool |
| --- | --- | --- | --- | --- |
| `dateutil` | 11 | 1 of 1 | none | none |
| `mcp` | 15 | 0 of 54 | none | none |
| `more_itertools` | 19 | 25 of 59 | 9.0 (9, 9, 9) | 10.7 (11, 11, 10) |
| `networkx` | 20 | 3 of 45 | 4.0 (4, 4, 4) | 6.0 (5, 6, 7) |
| `jinja2` | 9 | 11 of 58 | none | none |
| `werkzeug` | 16 | 26 of 60 | none | none |
| `packaging` | 28 | 41 of 60 | 16.0 (16, 16, 16) | 11.3 (11, 12, 11) |
| `rsa` | 17 | 11 of 24 | none | none |
| **3 repositories with every condition** | **67** | | **29.0 (43%) (29, 29, 29)** | **28.0 (42%) (27, 29, 28)** |

## How the tools were used

Means over the runs.

| Package | Condition | Questions with a tool call | Right among those | Tool calls | Calls that gave an error | Calls written as text, and run |
| --- | --- | --- | --- | --- | --- | --- |
| `more_itertools` | one python tool | 19.0 of 19 | 10.7 | 223.3 | 148.7 | 0.0 |
| `networkx` | one python tool | 20.0 of 20 | 6.0 | 132.3 | 123.7 | 0.0 |
| `packaging` | one python tool | 28.0 of 28 | 11.3 | 385.3 | 380.7 | 0.0 |

## By kind of answer

First run. A true-or-false question can be answered right by guessing half of the time.

| The answer is | Questions | No tools | One Python tool |
| --- | --- | --- | --- |
| true or false | 30 | 18 (60%) | 17 (57%) |
| another value | 37 | 11 (30%) | 10 (27%) |

## Question by question

First run. p is the exact two-sided sign test on the questions that only one of the two got right.

| A | B | Only A right | Only B right | p |
| --- | --- | --- | --- | --- |
| no tools | one python tool | 9 | 7 | 0.8 |
