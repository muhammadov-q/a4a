# Tools against no tools, on each library's own documentation questions (bench2)

A tool call that the model wrote as text is run as a call, and the Python tool's output is shown as text.

Model `qwen3-4b-rec4`. 2 repositories with every condition, 27 questions, 3 runs each. Right answers: no tools 14.0 (52%) (14, 14, 14); one python tool 14.7 (54%) (15, 15, 14).

A cell is the number of right answers: the mean of the runs, then each run in brackets.

| Package | Questions | Tools accepted | No tools | One Python tool |
| --- | --- | --- | --- | --- |
| `dateutil` | 11 | 1 of 1 | 3.0 (3, 3, 3) | 3.7 (4, 4, 3) |
| `mcp` | 15 | 0 of 54 | none | none |
| `more_itertools` | 19 | 25 of 59 | none | none |
| `networkx` | 20 | 3 of 45 | none | none |
| `jinja2` | 9 | 11 of 58 | none | none |
| `werkzeug` | 16 | 26 of 60 | 11.0 (11, 11, 11) | 11.0 (11, 11, 11) |
| `packaging` | 28 | 41 of 60 | none | none |
| `rsa` | 17 | 11 of 24 | none | none |
| **2 repositories with every condition** | **27** | | **14.0 (52%) (14, 14, 14)** | **14.7 (54%) (15, 15, 14)** |

## How the tools were used

Means over the runs.

| Package | Condition | Questions with a tool call | Right among those | Tool calls | Calls that gave an error | Calls written as text, and run |
| --- | --- | --- | --- | --- | --- | --- |
| `dateutil` | one python tool | 10.0 of 11 | 3.7 | 168.7 | 162.7 | 0.0 |
| `werkzeug` | one python tool | 16.0 of 16 | 11.0 | 201.0 | 190.0 | 4.0 |

## By kind of answer

First run. A true-or-false question can be answered right by guessing half of the time.

| The answer is | Questions | No tools | One Python tool |
| --- | --- | --- | --- |
| true or false | 2 | 2 (100%) | 2 (100%) |
| another value | 25 | 12 (48%) | 13 (52%) |

## Question by question

First run. p is the exact two-sided sign test on the questions that only one of the two got right.

| A | B | Only A right | Only B right | p |
| --- | --- | --- | --- | --- |
| no tools | one python tool | 4 | 5 | 1 |
