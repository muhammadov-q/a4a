# Tools against no tools, on each library's own documentation questions (bench2)

A tool call that the model wrote as text is run as a call, and the Python tool's output is shown as text.

Model `qwen3-1.7b-sft1-f2`. 3 repositories with every condition, 67 questions, 3 runs each. Right answers: no tools 27.0 (40%) (27, 27, 27); one python tool 25.3 (38%) (27, 25, 24); python tool + reference (elements used) 40.7 (61%) (41, 42, 39); python tool + reference (search) 38.0 (57%) (37, 37, 40).

A cell is the number of right answers: the mean of the runs, then each run in brackets.

| Package | Questions | Tools accepted | No tools | One Python tool | Python tool + reference (elements used) | Python tool + reference (search) |
| --- | --- | --- | --- | --- | --- | --- |
| `dateutil` | 11 | 1 of 1 | none | none | none | none |
| `mcp` | 15 | 0 of 54 | none | none | none | none |
| `more_itertools` | 19 | 25 of 59 | 8.0 (8, 8, 8) | 9.3 (10, 9, 9) | 16.0 (16, 16, 16) | 13.0 (13, 13, 13) |
| `networkx` | 20 | 3 of 45 | 4.0 (4, 4, 4) | 5.0 (5, 5, 5) | 9.7 (10, 10, 9) | 10.0 (9, 10, 11) |
| `jinja2` | 9 | 11 of 58 | none | none | none | none |
| `werkzeug` | 16 | 26 of 60 | none | none | none | none |
| `packaging` | 28 | 41 of 60 | 15.0 (15, 15, 15) | 11.0 (12, 11, 10) | 15.0 (15, 16, 14) | 15.0 (15, 14, 16) |
| `rsa` | 17 | 11 of 24 | none | none | none | none |
| **3 repositories with every condition** | **67** | | **27.0 (40%) (27, 27, 27)** | **25.3 (38%) (27, 25, 24)** | **40.7 (61%) (41, 42, 39)** | **38.0 (57%) (37, 37, 40)** |

## How the tools were used

Means over the runs.

| Package | Condition | Questions with a tool call | Right among those | Tool calls | Calls that gave an error | Calls written as text, and run |
| --- | --- | --- | --- | --- | --- | --- |
| `more_itertools` | one python tool | 18.7 of 19 | 9.3 | 79.0 | 69.7 | 1.3 |
| `more_itertools` | python tool + reference (elements used) | 19.0 of 19 | 16.0 | 19.0 | 0.0 | 0.0 |
| `more_itertools` | python tool + reference (search) | 19.0 of 19 | 13.0 | 40.3 | 23.7 | 0.0 |
| `networkx` | one python tool | 20.0 of 20 | 5.0 | 71.7 | 68.7 | 0.0 |
| `networkx` | python tool + reference (elements used) | 20.0 of 20 | 9.7 | 73.0 | 60.3 | 7.0 |
| `networkx` | python tool + reference (search) | 19.3 of 20 | 10.0 | 55.3 | 40.0 | 8.7 |
| `packaging` | one python tool | 27.7 of 28 | 11.0 | 139.0 | 133.0 | 0.0 |
| `packaging` | python tool + reference (elements used) | 27.0 of 28 | 15.0 | 197.0 | 188.3 | 0.7 |
| `packaging` | python tool + reference (search) | 27.0 of 28 | 15.0 | 134.0 | 121.0 | 0.0 |

## By kind of answer

First run. A true-or-false question can be answered right by guessing half of the time.

| The answer is | Questions | No tools | One Python tool | Python tool + reference (elements used) | Python tool + reference (search) |
| --- | --- | --- | --- | --- | --- |
| true or false | 30 | 19 (63%) | 14 (47%) | 17 (57%) | 18 (60%) |
| another value | 37 | 8 (22%) | 13 (35%) | 24 (65%) | 19 (51%) |

## Question by question

First run. p is the exact two-sided sign test on the questions that only one of the two got right.

| A | B | Only A right | Only B right | p |
| --- | --- | --- | --- | --- |
| no tools | one python tool | 11 | 11 | 1 |
| no tools | python tool + reference (elements used) | 7 | 21 | 0.013 |
| no tools | python tool + reference (search) | 9 | 19 | 0.087 |
| one python tool | python tool + reference (elements used) | 2 | 16 | 0.0013 |
| one python tool | python tool + reference (search) | 6 | 16 | 0.052 |
| python tool + reference (elements used) | python tool + reference (search) | 9 | 5 | 0.42 |
