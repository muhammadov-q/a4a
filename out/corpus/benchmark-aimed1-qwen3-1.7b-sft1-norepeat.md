# Tools against no tools, on the questions of out/corpus/tasks-aimed/ (aimed1, no repeated calls)

A tool call that the model wrote as text is run as a call, and the Python tool's output is shown as text. A call that is the same as an earlier call of the run is not run again; the model is told so.

Model `qwen3-1.7b-sft1`. 2 repositories with every condition, 27 questions, 3 runs each. Right answers: no tools 10.0 (37%) (10, 10, 10); one python tool 13.7 (51%) (13, 13, 15).

A cell is the number of right answers: the mean of the runs, then each run in brackets.

| Package | Questions | Tools accepted | No tools | One Python tool |
| --- | --- | --- | --- | --- |
| `dateutil` | 14 | none | 7.0 (7, 7, 7) | 7.0 (7, 6, 8) |
| `networkx` | 14 | none | none | none |
| `werkzeug` | 13 | none | 3.0 (3, 3, 3) | 6.7 (6, 7, 7) |
| `packaging` | 10 | none | none | none |
| **2 repositories with every condition** | **27** | | **10.0 (37%) (10, 10, 10)** | **13.7 (51%) (13, 13, 15)** |

## How the tools were used

Means over the runs.

| Package | Condition | Questions with a tool call | Right among those | Tool calls | Calls that gave an error | Calls written as text, and run |
| --- | --- | --- | --- | --- | --- | --- |
| `dateutil` | one python tool | 14.0 of 14 | 7.0 | 195.0 | 185.7 | 13.0 |
| `werkzeug` | one python tool | 12.3 of 13 | 6.7 | 164.7 | 159.0 | 9.7 |

## By kind of answer

First run. A true-or-false question can be answered right by guessing half of the time.

| The answer is | Questions | No tools | One Python tool |
| --- | --- | --- | --- |
| true or false | 7 | 4 (57%) | 3 (43%) |
| another value | 20 | 6 (30%) | 10 (50%) |

## Question by question

First run. p is the exact two-sided sign test on the questions that only one of the two got right.

| A | B | Only A right | Only B right | p |
| --- | --- | --- | --- | --- |
| no tools | one python tool | 5 | 8 | 0.58 |
