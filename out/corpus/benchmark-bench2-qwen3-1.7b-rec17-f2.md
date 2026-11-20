# Tools against no tools, on each library's own documentation questions (bench2)

A tool call that the model wrote as text is run as a call, and the Python tool's output is shown as text.

Model `qwen3-1.7b-rec17-f2`. 3 repositories with every condition, 67 questions, 3 runs each. Right answers: no tools 29.0 (43%) (29, 29, 29); one python tool 28.0 (42%) (27, 29, 28); python tool + reference (elements used) 40.7 (61%) (40, 41, 41); python tool + reference (search) 38.7 (58%) (39, 39, 38).

A cell is the number of right answers: the mean of the runs, then each run in brackets.

| Package | Questions | Tools accepted | No tools | One Python tool | Python tool + reference (elements used) | Python tool + reference (search) |
| --- | --- | --- | --- | --- | --- | --- |
| `dateutil` | 11 | 1 of 1 | none | none | none | none |
| `mcp` | 15 | 0 of 54 | none | none | none | none |
| `more_itertools` | 19 | 25 of 59 | 9.0 (9, 9, 9) | 10.7 (11, 11, 10) | 13.0 (13, 13, 13) | 12.0 (12, 12, 12) |
| `networkx` | 20 | 3 of 45 | 4.0 (4, 4, 4) | 6.0 (5, 6, 7) | 7.7 (7, 8, 8) | 10.3 (11, 10, 10) |
| `jinja2` | 9 | 11 of 58 | none | none | none | none |
| `werkzeug` | 16 | 26 of 60 | none | none | none | none |
| `packaging` | 28 | 41 of 60 | 16.0 (16, 16, 16) | 11.3 (11, 12, 11) | 20.0 (20, 20, 20) | 16.3 (16, 17, 16) |
| `rsa` | 17 | 11 of 24 | none | none | none | none |
| **3 repositories with every condition** | **67** | | **29.0 (43%) (29, 29, 29)** | **28.0 (42%) (27, 29, 28)** | **40.7 (61%) (40, 41, 41)** | **38.7 (58%) (39, 39, 38)** |

## How the tools were used

Means over the runs.

| Package | Condition | Questions with a tool call | Right among those | Tool calls | Calls that gave an error | Calls written as text, and run |
| --- | --- | --- | --- | --- | --- | --- |
| `more_itertools` | one python tool | 19.0 of 19 | 10.7 | 223.3 | 148.7 | 0.0 |
| `more_itertools` | python tool + reference (elements used) | 19.0 of 19 | 13.0 | 162.7 | 9.3 | 0.0 |
| `more_itertools` | python tool + reference (search) | 19.0 of 19 | 12.0 | 178.3 | 58.7 | 0.0 |
| `networkx` | one python tool | 20.0 of 20 | 6.0 | 132.3 | 123.7 | 0.0 |
| `networkx` | python tool + reference (elements used) | 20.0 of 20 | 7.7 | 109.3 | 98.3 | 0.0 |
| `networkx` | python tool + reference (search) | 20.0 of 20 | 10.3 | 120.7 | 83.0 | 0.0 |
| `packaging` | one python tool | 28.0 of 28 | 11.3 | 385.3 | 380.7 | 0.0 |
| `packaging` | python tool + reference (elements used) | 27.3 of 28 | 20.0 | 295.0 | 285.0 | 0.0 |
| `packaging` | python tool + reference (search) | 27.0 of 28 | 16.3 | 506.3 | 502.7 | 0.0 |

## By kind of answer

First run. A true-or-false question can be answered right by guessing half of the time.

| The answer is | Questions | No tools | One Python tool | Python tool + reference (elements used) | Python tool + reference (search) |
| --- | --- | --- | --- | --- | --- |
| true or false | 30 | 18 (60%) | 17 (57%) | 21 (70%) | 20 (67%) |
| another value | 37 | 11 (30%) | 10 (27%) | 19 (51%) | 19 (51%) |

## Question by question

First run. p is the exact two-sided sign test on the questions that only one of the two got right.

| A | B | Only A right | Only B right | p |
| --- | --- | --- | --- | --- |
| no tools | one python tool | 9 | 7 | 0.8 |
| no tools | python tool + reference (elements used) | 5 | 16 | 0.027 |
| no tools | python tool + reference (search) | 9 | 19 | 0.087 |
| one python tool | python tool + reference (elements used) | 2 | 15 | 0.0023 |
| one python tool | python tool + reference (search) | 3 | 15 | 0.0075 |
| python tool + reference (elements used) | python tool + reference (search) | 8 | 7 | 1 |
