# Tools against no tools, on the questions of out/corpus/tasks-aimed/ (aimed1)

A tool call that the model wrote as text is run as a call, and the Python tool's output is shown as text.

Model `qwen3-1.7b-sft2`. 2 repositories with every condition, 27 questions, 3 runs each. Right answers: no tools 10.0 (37%) (10, 10, 10); one python tool 12.0 (44%) (11, 13, 12).

A cell is the number of right answers: the mean of the runs, then each run in brackets.

| Package | Questions | Tools accepted | No tools | One Python tool |
| --- | --- | --- | --- | --- |
| `dateutil` | 14 | none | 7.0 (7, 7, 7) | 7.7 (7, 9, 7) |
| `networkx` | 14 | none | none | none |
| `werkzeug` | 13 | none | 3.0 (3, 3, 3) | 4.3 (4, 4, 5) |
| `packaging` | 10 | none | none | none |
| **2 repositories with every condition** | **27** | | **10.0 (37%) (10, 10, 10)** | **12.0 (44%) (11, 13, 12)** |

## How the tools were used

Means over the runs.

| Package | Condition | Questions with a tool call | Right among those | Tool calls | Calls that gave an error | Calls written as text, and run |
| --- | --- | --- | --- | --- | --- | --- |
| `dateutil` | one python tool | 14.0 of 14 | 7.7 | 188.7 | 179.7 | 2.0 |
| `werkzeug` | one python tool | 13.0 of 13 | 4.3 | 279.0 | 272.7 | 9.3 |

## By kind of answer

First run. A true-or-false question can be answered right by guessing half of the time.

| The answer is | Questions | No tools | One Python tool |
| --- | --- | --- | --- |
| true or false | 7 | 5 (71%) | 2 (29%) |
| another value | 20 | 5 (25%) | 9 (45%) |

## Question by question

First run. p is the exact two-sided sign test on the questions that only one of the two got right.

| A | B | Only A right | Only B right | p |
| --- | --- | --- | --- | --- |
| no tools | one python tool | 6 | 7 | 1 |
