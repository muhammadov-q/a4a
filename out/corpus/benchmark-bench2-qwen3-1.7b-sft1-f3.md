# Tools against no tools, on each library's own documentation questions (bench2)

A tool call that the model wrote as text is run as a call, and the Python tool's output is shown as text.

Model `qwen3-1.7b-sft1-f3`. 2 repositories with every condition, 26 questions, 3 runs each. Right answers: no tools 13.0 (50%) (13, 13, 13); one python tool 14.0 (54%) (14, 14, 14); python tool + reference (elements used) 19.0 (73%) (19, 19, 19); python tool + reference (search) 22.7 (87%) (23, 23, 22).

A cell is the number of right answers: the mean of the runs, then each run in brackets.

| Package | Questions | Tools accepted | No tools | One Python tool | Python tool + reference (elements used) | Python tool + reference (search) |
| --- | --- | --- | --- | --- | --- | --- |
| `dateutil` | 11 | 1 of 1 | none | none | none | none |
| `mcp` | 15 | 0 of 54 | none | none | none | none |
| `more_itertools` | 19 | 25 of 59 | none | none | none | none |
| `networkx` | 20 | 3 of 45 | none | none | none | none |
| `jinja2` | 9 | 11 of 58 | 5.0 (5, 5, 5) | 5.0 (5, 5, 5) | 5.0 (5, 5, 5) | 8.0 (8, 8, 8) |
| `werkzeug` | 16 | 26 of 60 | none | none | none | none |
| `packaging` | 28 | 41 of 60 | none | none | none | none |
| `rsa` | 17 | 11 of 24 | 8.0 (8, 8, 8) | 9.0 (9, 9, 9) | 14.0 (14, 14, 14) | 14.7 (15, 15, 14) |
| **2 repositories with every condition** | **26** | | **13.0 (50%) (13, 13, 13)** | **14.0 (54%) (14, 14, 14)** | **19.0 (73%) (19, 19, 19)** | **22.7 (87%) (23, 23, 22)** |

## How the tools were used

Means over the runs.

| Package | Condition | Questions with a tool call | Right among those | Tool calls | Calls that gave an error | Calls written as text, and run |
| --- | --- | --- | --- | --- | --- | --- |
| `jinja2` | one python tool | 9.0 of 9 | 5.0 | 94.3 | 90.3 | 0.7 |
| `jinja2` | python tool + reference (elements used) | 9.0 of 9 | 5.0 | 108.0 | 101.7 | 0.0 |
| `jinja2` | python tool + reference (search) | 9.0 of 9 | 8.0 | 11.0 | 2.0 | 0.0 |
| `rsa` | one python tool | 16.0 of 17 | 9.0 | 289.0 | 280.0 | 13.7 |
| `rsa` | python tool + reference (elements used) | 16.0 of 17 | 13.0 | 101.7 | 87.7 | 0.0 |
| `rsa` | python tool + reference (search) | 16.0 of 17 | 13.7 | 71.0 | 56.3 | 0.0 |

## By kind of answer

First run. A true-or-false question can be answered right by guessing half of the time.

| The answer is | Questions | No tools | One Python tool | Python tool + reference (elements used) | Python tool + reference (search) |
| --- | --- | --- | --- | --- | --- |
| true or false | 12 | 6 (50%) | 7 (58%) | 8 (67%) | 10 (83%) |
| another value | 14 | 7 (50%) | 7 (50%) | 11 (79%) | 13 (93%) |

## Question by question

First run. p is the exact two-sided sign test on the questions that only one of the two got right.

| A | B | Only A right | Only B right | p |
| --- | --- | --- | --- | --- |
| no tools | one python tool | 4 | 5 | 1 |
| no tools | python tool + reference (elements used) | 2 | 8 | 0.11 |
| no tools | python tool + reference (search) | 1 | 11 | 0.0063 |
| one python tool | python tool + reference (elements used) | 3 | 8 | 0.23 |
| one python tool | python tool + reference (search) | 1 | 10 | 0.012 |
| python tool + reference (elements used) | python tool + reference (search) | 1 | 5 | 0.22 |
