# Tools against no tools, on each library's own documentation questions (bench2)

A tool call that the model wrote as text is run as a call, and the Python tool's output is shown as text.

Model `qwen3-4b-sft1`. 2 repositories with every condition, 27 questions, 3 runs each. Right answers: no tools 10.0 (37%) (10, 10, 10); one python tool 15.3 (57%) (16, 15, 15); python tool + reference (elements used) 16.3 (60%) (16, 17, 16); python tool + reference (search) 15.7 (58%) (16, 16, 15).

A cell is the number of right answers: the mean of the runs, then each run in brackets.

| Package | Questions | Tools accepted | No tools | One Python tool | Python tool + reference (elements used) | Python tool + reference (search) |
| --- | --- | --- | --- | --- | --- | --- |
| `dateutil` | 11 | 1 of 1 | 3.0 (3, 3, 3) | 4.0 (4, 4, 4) | 5.3 (5, 6, 5) | 3.0 (3, 3, 3) |
| `mcp` | 15 | 0 of 54 | none | none | none | none |
| `more_itertools` | 19 | 25 of 59 | none | none | none | none |
| `networkx` | 20 | 3 of 45 | none | none | none | none |
| `jinja2` | 9 | 11 of 58 | none | none | none | none |
| `werkzeug` | 16 | 26 of 60 | 7.0 (7, 7, 7) | 11.3 (12, 11, 11) | 11.0 (11, 11, 11) | 12.7 (13, 13, 12) |
| `packaging` | 28 | 41 of 60 | none | none | none | none |
| `rsa` | 17 | 11 of 24 | none | none | none | none |
| **2 repositories with every condition** | **27** | | **10.0 (37%) (10, 10, 10)** | **15.3 (57%) (16, 15, 15)** | **16.3 (60%) (16, 17, 16)** | **15.7 (58%) (16, 16, 15)** |

## How the tools were used

Means over the runs.

| Package | Condition | Questions with a tool call | Right among those | Tool calls | Calls that gave an error | Calls written as text, and run |
| --- | --- | --- | --- | --- | --- | --- |
| `dateutil` | one python tool | 10.0 of 11 | 4.0 | 209.0 | 204.0 | 0.0 |
| `dateutil` | python tool + reference (elements used) | 10.0 of 11 | 5.3 | 135.7 | 102.0 | 0.0 |
| `dateutil` | python tool + reference (search) | 10.3 of 11 | 3.0 | 271.3 | 267.7 | 0.0 |
| `werkzeug` | one python tool | 16.0 of 16 | 11.3 | 191.0 | 179.3 | 0.0 |
| `werkzeug` | python tool + reference (elements used) | 16.0 of 16 | 11.0 | 173.0 | 161.0 | 0.0 |
| `werkzeug` | python tool + reference (search) | 16.0 of 16 | 12.7 | 71.3 | 56.7 | 0.0 |

## By kind of answer

First run. A true-or-false question can be answered right by guessing half of the time.

| The answer is | Questions | No tools | One Python tool | Python tool + reference (elements used) | Python tool + reference (search) |
| --- | --- | --- | --- | --- | --- |
| true or false | 2 | 2 (100%) | 2 (100%) | 2 (100%) | 2 (100%) |
| another value | 25 | 8 (32%) | 14 (56%) | 14 (56%) | 14 (56%) |

## Question by question

First run. p is the exact two-sided sign test on the questions that only one of the two got right.

| A | B | Only A right | Only B right | p |
| --- | --- | --- | --- | --- |
| no tools | one python tool | 3 | 9 | 0.15 |
| no tools | python tool + reference (elements used) | 3 | 9 | 0.15 |
| no tools | python tool + reference (search) | 2 | 8 | 0.11 |
| one python tool | python tool + reference (elements used) | 3 | 3 | 1 |
| one python tool | python tool + reference (search) | 2 | 2 | 1 |
| python tool + reference (elements used) | python tool + reference (search) | 2 | 2 | 1 |
