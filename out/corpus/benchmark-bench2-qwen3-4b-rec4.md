# Tools against no tools, on each library's own documentation questions (bench2)

A tool call that the model wrote as text is run as a call, and the Python tool's output is shown as text.

Model `qwen3-4b-rec4`. 2 repositories with every condition, 27 questions, 3 runs each. Right answers: no tools 14.0 (52%) (14, 14, 14); one python tool 14.7 (54%) (15, 15, 14); python tool + reference (elements used) 17.0 (63%) (17, 17, 17); python tool + reference (search) 17.7 (65%) (18, 18, 17).

A cell is the number of right answers: the mean of the runs, then each run in brackets.

| Package | Questions | Tools accepted | No tools | One Python tool | Python tool + reference (elements used) | Python tool + reference (search) |
| --- | --- | --- | --- | --- | --- | --- |
| `dateutil` | 11 | 1 of 1 | 3.0 (3, 3, 3) | 3.7 (4, 4, 3) | 4.0 (4, 4, 4) | 4.0 (4, 4, 4) |
| `mcp` | 15 | 0 of 54 | none | none | none | none |
| `more_itertools` | 19 | 25 of 59 | none | none | none | none |
| `networkx` | 20 | 3 of 45 | none | none | none | none |
| `jinja2` | 9 | 11 of 58 | none | none | none | none |
| `werkzeug` | 16 | 26 of 60 | 11.0 (11, 11, 11) | 11.0 (11, 11, 11) | 13.0 (13, 13, 13) | 13.7 (14, 14, 13) |
| `packaging` | 28 | 41 of 60 | none | none | none | none |
| `rsa` | 17 | 11 of 24 | none | none | none | none |
| **2 repositories with every condition** | **27** | | **14.0 (52%) (14, 14, 14)** | **14.7 (54%) (15, 15, 14)** | **17.0 (63%) (17, 17, 17)** | **17.7 (65%) (18, 18, 17)** |

## How the tools were used

Means over the runs.

| Package | Condition | Questions with a tool call | Right among those | Tool calls | Calls that gave an error | Calls written as text, and run |
| --- | --- | --- | --- | --- | --- | --- |
| `dateutil` | one python tool | 10.0 of 11 | 3.7 | 168.7 | 162.7 | 0.0 |
| `dateutil` | python tool + reference (elements used) | 10.0 of 11 | 4.0 | 156.0 | 149.3 | 0.0 |
| `dateutil` | python tool + reference (search) | 11.0 of 11 | 4.0 | 278.7 | 273.3 | 0.0 |
| `werkzeug` | one python tool | 16.0 of 16 | 11.0 | 201.0 | 190.0 | 4.0 |
| `werkzeug` | python tool + reference (elements used) | 16.0 of 16 | 13.0 | 114.7 | 101.7 | 1.3 |
| `werkzeug` | python tool + reference (search) | 16.0 of 16 | 13.7 | 69.3 | 54.7 | 0.0 |

## By kind of answer

First run. A true-or-false question can be answered right by guessing half of the time.

| The answer is | Questions | No tools | One Python tool | Python tool + reference (elements used) | Python tool + reference (search) |
| --- | --- | --- | --- | --- | --- |
| true or false | 2 | 2 (100%) | 2 (100%) | 2 (100%) | 2 (100%) |
| another value | 25 | 12 (48%) | 13 (52%) | 15 (60%) | 16 (64%) |

## Question by question

First run. p is the exact two-sided sign test on the questions that only one of the two got right.

| A | B | Only A right | Only B right | p |
| --- | --- | --- | --- | --- |
| no tools | one python tool | 4 | 5 | 1 |
| no tools | python tool + reference (elements used) | 3 | 6 | 0.51 |
| no tools | python tool + reference (search) | 2 | 6 | 0.29 |
| one python tool | python tool + reference (elements used) | 1 | 3 | 0.62 |
| one python tool | python tool + reference (search) | 2 | 5 | 0.45 |
| python tool + reference (elements used) | python tool + reference (search) | 1 | 2 | 1 |
