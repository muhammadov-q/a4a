# Tools against no tools, on each library's own documentation questions (bench2)

A tool call that the model wrote as text is run as a call, and the Python tool's output is shown as text.

Model `qwen3-1.7b-rec17`. 2 repositories with every condition, 27 questions, 3 runs each. Right answers: no tools 12.0 (44%) (12, 12, 12); one python tool 9.0 (33%) (9, 9, 9); python tool + reference (elements used) 12.0 (44%) (12, 12, 12); python tool + reference (search) 9.3 (35%) (10, 9, 9).

A cell is the number of right answers: the mean of the runs, then each run in brackets.

| Package | Questions | Tools accepted | No tools | One Python tool | Python tool + reference (elements used) | Python tool + reference (search) |
| --- | --- | --- | --- | --- | --- | --- |
| `dateutil` | 11 | 1 of 1 | 4.0 (4, 4, 4) | 1.0 (1, 1, 1) | 2.0 (2, 2, 2) | 1.3 (2, 1, 1) |
| `mcp` | 15 | 0 of 54 | none | none | none | none |
| `more_itertools` | 19 | 25 of 59 | none | none | none | none |
| `networkx` | 20 | 3 of 45 | none | none | none | none |
| `jinja2` | 9 | 11 of 58 | none | none | none | none |
| `werkzeug` | 16 | 26 of 60 | 8.0 (8, 8, 8) | 8.0 (8, 8, 8) | 10.0 (10, 10, 10) | 8.0 (8, 8, 8) |
| `packaging` | 28 | 41 of 60 | none | none | none | none |
| `rsa` | 17 | 11 of 24 | none | none | none | none |
| **2 repositories with every condition** | **27** | | **12.0 (44%) (12, 12, 12)** | **9.0 (33%) (9, 9, 9)** | **12.0 (44%) (12, 12, 12)** | **9.3 (35%) (10, 9, 9)** |

## How the tools were used

Means over the runs.

| Package | Condition | Questions with a tool call | Right among those | Tool calls | Calls that gave an error | Calls written as text, and run |
| --- | --- | --- | --- | --- | --- | --- |
| `dateutil` | one python tool | 10.0 of 11 | 1.0 | 270.7 | 267.3 | 0.0 |
| `dateutil` | python tool + reference (elements used) | 9.7 of 11 | 2.0 | 195.0 | 190.0 | 0.0 |
| `dateutil` | python tool + reference (search) | 7.7 of 11 | 1.3 | 216.7 | 214.3 | 0.0 |
| `werkzeug` | one python tool | 16.0 of 16 | 8.0 | 296.3 | 287.3 | 0.0 |
| `werkzeug` | python tool + reference (elements used) | 16.0 of 16 | 10.0 | 211.0 | 200.0 | 0.0 |
| `werkzeug` | python tool + reference (search) | 16.0 of 16 | 8.0 | 253.7 | 243.7 | 0.0 |

## By kind of answer

First run. A true-or-false question can be answered right by guessing half of the time.

| The answer is | Questions | No tools | One Python tool | Python tool + reference (elements used) | Python tool + reference (search) |
| --- | --- | --- | --- | --- | --- |
| true or false | 2 | 2 (100%) | 2 (100%) | 2 (100%) | 2 (100%) |
| another value | 25 | 10 (40%) | 7 (28%) | 10 (40%) | 8 (32%) |

## Question by question

First run. p is the exact two-sided sign test on the questions that only one of the two got right.

| A | B | Only A right | Only B right | p |
| --- | --- | --- | --- | --- |
| no tools | one python tool | 5 | 2 | 0.45 |
| no tools | python tool + reference (elements used) | 5 | 5 | 1 |
| no tools | python tool + reference (search) | 4 | 2 | 0.69 |
| one python tool | python tool + reference (elements used) | 0 | 3 | 0.25 |
| one python tool | python tool + reference (search) | 1 | 2 | 1 |
| python tool + reference (elements used) | python tool + reference (search) | 3 | 1 | 0.62 |
