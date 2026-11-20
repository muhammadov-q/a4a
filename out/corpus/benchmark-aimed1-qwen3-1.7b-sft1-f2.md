# Tools against no tools, on the questions of out/corpus/tasks-aimed/ (aimed1)

A tool call that the model wrote as text is run as a call, and the Python tool's output is shown as text.

Model `qwen3-1.7b-sft1-f2`. 3 repositories with every condition, 29 questions, 3 runs each. Right answers: no tools 3.0 (10%) (3, 3, 3); one python tool 8.3 (29%) (8, 9, 8); python tool + reference (elements used) 16.7 (57%) (16, 17, 17); python tool + reference (search) 16.7 (57%) (17, 17, 16).

A cell is the number of right answers: the mean of the runs, then each run in brackets.

| Package | Questions | Tools accepted | No tools | One Python tool | Python tool + reference (elements used) | Python tool + reference (search) |
| --- | --- | --- | --- | --- | --- | --- |
| `dateutil` | 14 | none | none | none | none | none |
| `mcp` | 4 | none | none | none | none | none |
| `more_itertools` | 5 | none | 0.0 (0, 0, 0) | 1.3 (1, 2, 1) | 2.0 (2, 2, 2) | 3.0 (3, 3, 3) |
| `networkx` | 14 | none | 2.0 (2, 2, 2) | 6.0 (6, 6, 6) | 9.7 (9, 10, 10) | 8.7 (9, 9, 8) |
| `jinja2` | 3 | none | none | none | none | none |
| `werkzeug` | 13 | none | none | none | none | none |
| `packaging` | 10 | none | 1.0 (1, 1, 1) | 1.0 (1, 1, 1) | 5.0 (5, 5, 5) | 5.0 (5, 5, 5) |
| `rsa` | 3 | none | none | none | none | none |
| **3 repositories with every condition** | **29** | | **3.0 (10%) (3, 3, 3)** | **8.3 (29%) (8, 9, 8)** | **16.7 (57%) (16, 17, 17)** | **16.7 (57%) (17, 17, 16)** |

## How the tools were used

Means over the runs.

| Package | Condition | Questions with a tool call | Right among those | Tool calls | Calls that gave an error | Calls written as text, and run |
| --- | --- | --- | --- | --- | --- | --- |
| `more_itertools` | one python tool | 5.0 of 5 | 1.3 | 30.0 | 28.7 | 0.0 |
| `more_itertools` | python tool + reference (elements used) | 5.0 of 5 | 2.0 | 21.0 | 18.0 | 0.0 |
| `more_itertools` | python tool + reference (search) | 5.0 of 5 | 3.0 | 22.3 | 18.3 | 0.0 |
| `networkx` | one python tool | 13.7 of 14 | 5.7 | 51.7 | 45.0 | 0.0 |
| `networkx` | python tool + reference (elements used) | 14.0 of 14 | 9.7 | 26.0 | 14.0 | 0.0 |
| `networkx` | python tool + reference (search) | 14.0 of 14 | 8.7 | 37.7 | 26.3 | 0.0 |
| `packaging` | one python tool | 9.7 of 10 | 1.0 | 66.7 | 65.0 | 0.0 |
| `packaging` | python tool + reference (elements used) | 10.0 of 10 | 5.0 | 44.0 | 31.0 | 0.0 |
| `packaging` | python tool + reference (search) | 10.0 of 10 | 5.0 | 44.0 | 37.7 | 0.0 |

## By kind of answer

First run. A true-or-false question can be answered right by guessing half of the time.

| The answer is | Questions | No tools | One Python tool | Python tool + reference (elements used) | Python tool + reference (search) |
| --- | --- | --- | --- | --- | --- |
| true or false | 2 | 1 (50%) | 0 (0%) | 2 (100%) | 2 (100%) |
| another value | 27 | 2 (7%) | 8 (30%) | 14 (52%) | 15 (56%) |

## Question by question

First run. p is the exact two-sided sign test on the questions that only one of the two got right.

| A | B | Only A right | Only B right | p |
| --- | --- | --- | --- | --- |
| no tools | one python tool | 3 | 8 | 0.23 |
| no tools | python tool + reference (elements used) | 1 | 14 | 0.00098 |
| no tools | python tool + reference (search) | 2 | 16 | 0.0013 |
| one python tool | python tool + reference (elements used) | 3 | 11 | 0.057 |
| one python tool | python tool + reference (search) | 3 | 12 | 0.035 |
| python tool + reference (elements used) | python tool + reference (search) | 2 | 3 | 1 |
