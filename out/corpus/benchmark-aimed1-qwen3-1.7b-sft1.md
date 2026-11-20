# Tools against no tools, on the questions of out/corpus/tasks-aimed/ (aimed1)

A tool call that the model wrote as text is run as a call, and the Python tool's output is shown as text.

Model `qwen3-1.7b-sft1`. 2 repositories with every condition, 27 questions, 3 runs each. Right answers: no tools 10.0 (37%) (10, 10, 10); one python tool 9.7 (36%) (10, 9, 10).

A cell is the number of right answers: the mean of the runs, then each run in brackets.

| Package | Questions | Tools accepted | No tools | One Python tool |
| --- | --- | --- | --- | --- |
| `dateutil` | 14 | none | 7.0 (7, 7, 7) | 5.7 (6, 5, 6) |
| `networkx` | 14 | none | none | none |
| `werkzeug` | 13 | none | 3.0 (3, 3, 3) | 4.0 (4, 4, 4) |
| `packaging` | 10 | none | none | none |
| **2 repositories with every condition** | **27** | | **10.0 (37%) (10, 10, 10)** | **9.7 (36%) (10, 9, 10)** |

## How the tools were used

Means over the runs.

| Package | Condition | Questions with a tool call | Right among those | Tool calls | Calls that gave an error | Calls written as text, and run |
| --- | --- | --- | --- | --- | --- | --- |
| `dateutil` | one python tool | 13.3 of 14 | 5.7 | 215.3 | 208.0 | 0.0 |
| `werkzeug` | one python tool | 13.0 of 13 | 4.0 | 253.0 | 247.0 | 0.0 |

## By kind of answer

First run. A true-or-false question can be answered right by guessing half of the time.

| The answer is | Questions | No tools | One Python tool |
| --- | --- | --- | --- |
| true or false | 7 | 4 (57%) | 2 (29%) |
| another value | 20 | 6 (30%) | 8 (40%) |

## Question by question

First run. p is the exact two-sided sign test on the questions that only one of the two got right.

| A | B | Only A right | Only B right | p |
| --- | --- | --- | --- | --- |
| no tools | one python tool | 7 | 7 | 1 |
