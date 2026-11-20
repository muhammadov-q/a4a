# Tools against no tools, on each library's own documentation questions (bench2)

A tool call that the model wrote as text is run as a call, and the Python tool's output is shown as text.

Model `qwen3-4b-sft1-f2`. 3 repositories with every condition, 67 questions, 3 runs each. Right answers: no tools 28.7 (43%) (29, 29, 28); one python tool 31.0 (46%) (30, 32, 31); python tool + reference (elements used) 50.3 (75%) (51, 50, 50); python tool + reference (search) 51.3 (77%) (52, 52, 50).

A cell is the number of right answers: the mean of the runs, then each run in brackets.

| Package | Questions | Tools accepted | No tools | One Python tool | Python tool + reference (elements used) | Python tool + reference (search) |
| --- | --- | --- | --- | --- | --- | --- |
| `dateutil` | 11 | 1 of 1 | none | none | none | none |
| `mcp` | 15 | 0 of 54 | none | none | none | none |
| `more_itertools` | 19 | 25 of 59 | 7.0 (7, 7, 7) | 9.3 (9, 9, 10) | 15.0 (15, 15, 15) | 16.0 (16, 17, 15) |
| `networkx` | 20 | 3 of 45 | 5.7 (6, 6, 5) | 13.7 (14, 14, 13) | 13.3 (13, 13, 14) | 14.0 (14, 14, 14) |
| `jinja2` | 9 | 11 of 58 | none | none | none | none |
| `werkzeug` | 16 | 26 of 60 | none | none | none | none |
| `packaging` | 28 | 41 of 60 | 16.0 (16, 16, 16) | 8.0 (7, 9, 8) | 22.0 (23, 22, 21) | 21.3 (22, 21, 21) |
| `rsa` | 17 | 11 of 24 | none | none | none | none |
| **3 repositories with every condition** | **67** | | **28.7 (43%) (29, 29, 28)** | **31.0 (46%) (30, 32, 31)** | **50.3 (75%) (51, 50, 50)** | **51.3 (77%) (52, 52, 50)** |

## How the tools were used

Means over the runs.

| Package | Condition | Questions with a tool call | Right among those | Tool calls | Calls that gave an error | Calls written as text, and run |
| --- | --- | --- | --- | --- | --- | --- |
| `more_itertools` | one python tool | 19.0 of 19 | 9.3 | 195.0 | 180.7 | 0.0 |
| `more_itertools` | python tool + reference (elements used) | 19.0 of 19 | 15.0 | 48.0 | 30.0 | 0.0 |
| `more_itertools` | python tool + reference (search) | 19.0 of 19 | 16.0 | 48.7 | 18.7 | 0.0 |
| `networkx` | one python tool | 20.0 of 20 | 13.7 | 116.0 | 98.3 | 0.3 |
| `networkx` | python tool + reference (elements used) | 20.0 of 20 | 13.3 | 59.7 | 40.7 | 0.0 |
| `networkx` | python tool + reference (search) | 20.0 of 20 | 14.0 | 59.0 | 40.0 | 0.0 |
| `packaging` | one python tool | 28.0 of 28 | 8.0 | 640.0 | 628.7 | 111.3 |
| `packaging` | python tool + reference (elements used) | 28.0 of 28 | 22.0 | 187.3 | 163.3 | 14.0 |
| `packaging` | python tool + reference (search) | 28.0 of 28 | 21.3 | 141.7 | 118.0 | 0.7 |

## By kind of answer

First run. A true-or-false question can be answered right by guessing half of the time.

| The answer is | Questions | No tools | One Python tool | Python tool + reference (elements used) | Python tool + reference (search) |
| --- | --- | --- | --- | --- | --- |
| true or false | 30 | 16 (53%) | 12 (40%) | 23 (77%) | 24 (80%) |
| another value | 37 | 13 (35%) | 18 (49%) | 28 (76%) | 28 (76%) |

## Question by question

First run. p is the exact two-sided sign test on the questions that only one of the two got right.

| A | B | Only A right | Only B right | p |
| --- | --- | --- | --- | --- |
| no tools | one python tool | 12 | 13 | 1 |
| no tools | python tool + reference (elements used) | 3 | 25 | 2.7e-05 |
| no tools | python tool + reference (search) | 2 | 25 | 5.6e-06 |
| one python tool | python tool + reference (elements used) | 4 | 25 | 0.0001 |
| one python tool | python tool + reference (search) | 3 | 25 | 2.7e-05 |
| python tool + reference (elements used) | python tool + reference (search) | 5 | 6 | 1 |
