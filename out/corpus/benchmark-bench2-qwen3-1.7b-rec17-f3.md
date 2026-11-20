# Tools against no tools, on each library's own documentation questions (bench2)

A tool call that the model wrote as text is run as a call, and the Python tool's output is shown as text.

Model `qwen3-1.7b-rec17-f3`. 2 repositories with every condition, 26 questions, 3 runs each. Right answers: no tools 12.0 (46%) (12, 12, 12); one python tool 15.0 (58%) (15, 14, 16).

A cell is the number of right answers: the mean of the runs, then each run in brackets.

| Package | Questions | Tools accepted | No tools | One Python tool |
| --- | --- | --- | --- | --- |
| `dateutil` | 11 | 1 of 1 | none | none |
| `mcp` | 15 | 0 of 54 | none | none |
| `more_itertools` | 19 | 25 of 59 | none | none |
| `networkx` | 20 | 3 of 45 | none | none |
| `jinja2` | 9 | 11 of 58 | 4.0 (4, 4, 4) | 2.7 (2, 2, 4) |
| `werkzeug` | 16 | 26 of 60 | none | none |
| `packaging` | 28 | 41 of 60 | none | none |
| `rsa` | 17 | 11 of 24 | 8.0 (8, 8, 8) | 12.3 (13, 12, 12) |
| **2 repositories with every condition** | **26** | | **12.0 (46%) (12, 12, 12)** | **15.0 (58%) (15, 14, 16)** |

## How the tools were used

Means over the runs.

| Package | Condition | Questions with a tool call | Right among those | Tool calls | Calls that gave an error | Calls written as text, and run |
| --- | --- | --- | --- | --- | --- | --- |
| `jinja2` | one python tool | 8.0 of 9 | 2.7 | 72.7 | 69.3 | 0.0 |
| `rsa` | one python tool | 16.0 of 17 | 12.3 | 106.3 | 97.3 | 0.0 |

## By kind of answer

First run. A true-or-false question can be answered right by guessing half of the time.

| The answer is | Questions | No tools | One Python tool |
| --- | --- | --- | --- |
| true or false | 12 | 5 (42%) | 5 (42%) |
| another value | 14 | 7 (50%) | 10 (71%) |

## Question by question

First run. p is the exact two-sided sign test on the questions that only one of the two got right.

| A | B | Only A right | Only B right | p |
| --- | --- | --- | --- | --- |
| no tools | one python tool | 2 | 5 | 0.45 |
