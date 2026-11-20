# Tools against no tools, on each library's own documentation questions (bench2, no repeated calls)

A tool call that the model wrote as text is run as a call, and the Python tool's output is shown as text. A call that is the same as an earlier call of the run is not run again; the model is told so.

Model `qwen3-1.7b`. 2 repositories with every condition, 27 questions, 3 runs each. Right answers: no tools 4.0 (15%) (4, 4, 4); one python tool 7.7 (28%) (8, 7, 8).

A cell is the number of right answers: the mean of the runs, then each run in brackets.

| Package | Questions | Tools accepted | No tools | One Python tool |
| --- | --- | --- | --- | --- |
| `dateutil` | 11 | 1 of 1 | 1.0 (1, 1, 1) | 2.7 (3, 3, 2) |
| `mcp` | 15 | 0 of 54 | none | none |
| `more_itertools` | 19 | 25 of 59 | 5.3 (5, 5, 6) | none |
| `networkx` | 20 | 3 of 45 | 1.3 (1, 2, 1) | none |
| `jinja2` | 9 | 11 of 58 | 5.0 (5, 5, 5) | none |
| `werkzeug` | 16 | 26 of 60 | 3.0 (3, 3, 3) | 5.0 (5, 4, 6) |
| `packaging` | 28 | 41 of 60 | 15.0 (15, 15, 15) | none |
| `rsa` | 17 | 11 of 24 | 2.0 (2, 2, 2) | none |
| **2 repositories with every condition** | **27** | | **4.0 (15%) (4, 4, 4)** | **7.7 (28%) (8, 7, 8)** |

## How the tools were used

Means over the runs.

| Package | Condition | Questions with a tool call | Right among those | Tool calls | Calls that gave an error | Calls written as text, and run |
| --- | --- | --- | --- | --- | --- | --- |
| `dateutil` | one python tool | 10.0 of 11 | 2.7 | 159.7 | 155.7 | 47.7 |
| `werkzeug` | one python tool | 16.0 of 16 | 5.0 | 90.0 | 85.3 | 10.0 |

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
