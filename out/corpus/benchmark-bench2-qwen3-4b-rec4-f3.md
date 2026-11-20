# Tools against no tools, on each library's own documentation questions (bench2)

A tool call that the model wrote as text is run as a call, and the Python tool's output is shown as text.

Model `qwen3-4b-rec4-f3`. 2 repositories with every condition, 26 questions, 3 runs each. Right answers: no tools 13.0 (50%) (13, 13, 13); one python tool 13.3 (51%) (13, 13, 14); python tool + reference (elements used) 23.7 (91%) (23, 24, 24); python tool + reference (search) 23.3 (90%) (23, 23, 24).

A cell is the number of right answers: the mean of the runs, then each run in brackets.

| Package | Questions | Tools accepted | No tools | One Python tool | Python tool + reference (elements used) | Python tool + reference (search) |
| --- | --- | --- | --- | --- | --- | --- |
| `dateutil` | 11 | 1 of 1 | none | none | none | none |
| `mcp` | 15 | 0 of 54 | none | none | none | none |
| `more_itertools` | 19 | 25 of 59 | none | none | none | none |
| `networkx` | 20 | 3 of 45 | none | none | none | none |
| `jinja2` | 9 | 11 of 58 | 7.0 (7, 7, 7) | 2.7 (3, 2, 3) | 9.0 (9, 9, 9) | 9.0 (9, 9, 9) |
| `werkzeug` | 16 | 26 of 60 | none | none | none | none |
| `packaging` | 28 | 41 of 60 | none | none | none | none |
| `rsa` | 17 | 11 of 24 | 6.0 (6, 6, 6) | 10.7 (10, 11, 11) | 14.7 (14, 15, 15) | 14.3 (14, 14, 15) |
| **2 repositories with every condition** | **26** | | **13.0 (50%) (13, 13, 13)** | **13.3 (51%) (13, 13, 14)** | **23.7 (91%) (23, 24, 24)** | **23.3 (90%) (23, 23, 24)** |

## How the tools were used

Means over the runs.

| Package | Condition | Questions with a tool call | Right among those | Tool calls | Calls that gave an error | Calls written as text, and run |
| --- | --- | --- | --- | --- | --- | --- |
| `jinja2` | one python tool | 9.0 of 9 | 2.7 | 103.0 | 96.3 | 0.0 |
| `jinja2` | python tool + reference (elements used) | 9.0 of 9 | 9.0 | 9.0 | 0.0 | 0.0 |
| `jinja2` | python tool + reference (search) | 9.0 of 9 | 9.0 | 9.0 | 0.0 | 0.0 |
| `rsa` | one python tool | 17.0 of 17 | 10.7 | 228.7 | 217.7 | 0.0 |
| `rsa` | python tool + reference (elements used) | 17.0 of 17 | 14.7 | 108.0 | 93.3 | 0.0 |
| `rsa` | python tool + reference (search) | 17.0 of 17 | 14.3 | 70.0 | 54.3 | 0.0 |

## By kind of answer

First run. A true-or-false question can be answered right by guessing half of the time.

| The answer is | Questions | No tools | One Python tool | Python tool + reference (elements used) | Python tool + reference (search) |
| --- | --- | --- | --- | --- | --- |
| true or false | 12 | 8 (67%) | 4 (33%) | 12 (100%) | 11 (92%) |
| another value | 14 | 5 (36%) | 9 (64%) | 11 (79%) | 12 (86%) |

## Question by question

First run. p is the exact two-sided sign test on the questions that only one of the two got right.

| A | B | Only A right | Only B right | p |
| --- | --- | --- | --- | --- |
| no tools | one python tool | 7 | 7 | 1 |
| no tools | python tool + reference (elements used) | 0 | 10 | 0.002 |
| no tools | python tool + reference (search) | 0 | 10 | 0.002 |
| one python tool | python tool + reference (elements used) | 2 | 12 | 0.013 |
| one python tool | python tool + reference (search) | 2 | 12 | 0.013 |
| python tool + reference (elements used) | python tool + reference (search) | 1 | 1 | 1 |
