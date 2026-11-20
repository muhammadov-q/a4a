# Tools against no tools, on each library's own documentation questions (bench2)

A tool call that the model wrote as text is run as a call, and the Python tool's output is shown as text.

Model `qwen3-1.7b`. 2 repositories with every condition, 27 questions, 3 runs each. Right answers: no tools 4.0 (15%) (4, 4, 4); one python tool 7.3 (27%) (8, 7, 7).

A cell is the number of right answers: the mean of the runs, then each run in brackets.

| Package | Questions | Tools accepted | No tools | One Python tool |
| --- | --- | --- | --- | --- |
| `dateutil` | 11 | 1 of 1 | 1.0 (1, 1, 1) | 2.3 (3, 2, 2) |
| `mcp` | 15 | 0 of 54 | none | none |
| `more_itertools` | 19 | 25 of 59 | none | none |
| `networkx` | 20 | 3 of 45 | none | none |
| `jinja2` | 9 | 11 of 58 | none | none |
| `werkzeug` | 16 | 26 of 60 | 3.0 (3, 3, 3) | 5.0 (5, 5, 5) |
| `packaging` | 28 | 41 of 60 | none | none |
| `rsa` | 17 | 11 of 24 | none | none |
| **2 repositories with every condition** | **27** | | **4.0 (15%) (4, 4, 4)** | **7.3 (27%) (8, 7, 7)** |

## How the tools were used

Means over the runs.

| Package | Condition | Questions with a tool call | Right among those | Tool calls | Calls that gave an error | Calls written as text, and run |
| --- | --- | --- | --- | --- | --- | --- |
| `dateutil` | one python tool | 10.3 of 11 | 2.3 | 183.0 | 179.0 | 96.3 |
| `werkzeug` | one python tool | 16.0 of 16 | 5.0 | 147.7 | 143.3 | 72.7 |

## By kind of answer

First run. A true-or-false question can be answered right by guessing half of the time.

| The answer is | Questions | No tools | One Python tool |
| --- | --- | --- | --- |
| true or false | 2 | 2 (100%) | 0 (0%) |
| another value | 25 | 2 (8%) | 8 (32%) |

## Question by question

First run. p is the exact two-sided sign test on the questions that only one of the two got right.

| A | B | Only A right | Only B right | p |
| --- | --- | --- | --- | --- |
| no tools | one python tool | 3 | 7 | 0.34 |
