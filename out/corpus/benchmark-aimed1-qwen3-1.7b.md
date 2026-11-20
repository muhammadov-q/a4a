# Tools against no tools, on the questions of out/corpus/tasks-aimed/ (aimed1)

A tool call that the model wrote as text is run as a call, and the Python tool's output is shown as text.

Model `qwen3-1.7b`. 2 repositories with every condition, 27 questions, 3 runs each. Right answers: no tools 7.0 (26%) (7, 7, 7); one python tool 11.7 (43%) (11, 12, 12).

A cell is the number of right answers: the mean of the runs, then each run in brackets.

| Package | Questions | Tools accepted | No tools | One Python tool |
| --- | --- | --- | --- | --- |
| `dateutil` | 14 | none | 7.0 (7, 7, 7) | 8.7 (8, 9, 9) |
| `networkx` | 14 | none | none | none |
| `werkzeug` | 13 | none | 0.0 (0, 0, 0) | 3.0 (3, 3, 3) |
| `packaging` | 10 | none | none | none |
| **2 repositories with every condition** | **27** | | **7.0 (26%) (7, 7, 7)** | **11.7 (43%) (11, 12, 12)** |

## How the tools were used

Means over the runs.

| Package | Condition | Questions with a tool call | Right among those | Tool calls | Calls that gave an error | Calls written as text, and run |
| --- | --- | --- | --- | --- | --- | --- |
| `dateutil` | one python tool | 14.0 of 14 | 8.7 | 80.3 | 71.7 | 38.0 |
| `werkzeug` | one python tool | 13.0 of 13 | 3.0 | 141.3 | 136.3 | 35.3 |

## By kind of answer

First run. A true-or-false question can be answered right by guessing half of the time.

| The answer is | Questions | No tools | One Python tool |
| --- | --- | --- | --- |
| true or false | 7 | 4 (57%) | 1 (14%) |
| another value | 20 | 3 (15%) | 10 (50%) |

## Question by question

First run. p is the exact two-sided sign test on the questions that only one of the two got right.

| A | B | Only A right | Only B right | p |
| --- | --- | --- | --- | --- |
| no tools | one python tool | 4 | 8 | 0.39 |
