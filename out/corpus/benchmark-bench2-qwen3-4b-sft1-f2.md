# Tools against no tools, on each library's own documentation questions (bench2)

A tool call that the model wrote as text is run as a call, and the Python tool's output is shown as text.

Model `qwen3-4b-sft1-f2`. 3 repositories with every condition, 67 questions, 3 runs each. Right answers: no tools 28.7 (43%) (29, 29, 28); one python tool 31.0 (46%) (30, 32, 31).

A cell is the number of right answers: the mean of the runs, then each run in brackets.

| Package | Questions | Tools accepted | No tools | One Python tool |
| --- | --- | --- | --- | --- |
| `dateutil` | 11 | 1 of 1 | none | none |
| `mcp` | 15 | 0 of 54 | none | none |
| `more_itertools` | 19 | 25 of 59 | 7.0 (7, 7, 7) | 9.3 (9, 9, 10) |
| `networkx` | 20 | 3 of 45 | 5.7 (6, 6, 5) | 13.7 (14, 14, 13) |
| `jinja2` | 9 | 11 of 58 | none | none |
| `werkzeug` | 16 | 26 of 60 | none | none |
| `packaging` | 28 | 41 of 60 | 16.0 (16, 16, 16) | 8.0 (7, 9, 8) |
| `rsa` | 17 | 11 of 24 | none | none |
| **3 repositories with every condition** | **67** | | **28.7 (43%) (29, 29, 28)** | **31.0 (46%) (30, 32, 31)** |

## How the tools were used

Means over the runs.

| Package | Condition | Questions with a tool call | Right among those | Tool calls | Calls that gave an error | Calls written as text, and run |
| --- | --- | --- | --- | --- | --- | --- |
| `more_itertools` | one python tool | 19.0 of 19 | 9.3 | 195.0 | 180.7 | 0.0 |
| `networkx` | one python tool | 20.0 of 20 | 13.7 | 116.0 | 98.3 | 0.3 |
| `packaging` | one python tool | 28.0 of 28 | 8.0 | 640.0 | 628.7 | 111.3 |

## By kind of answer

First run. A true-or-false question can be answered right by guessing half of the time.

| The answer is | Questions | No tools | One Python tool |
| --- | --- | --- | --- |
| true or false | 30 | 16 (53%) | 12 (40%) |
| another value | 37 | 13 (35%) | 18 (49%) |

## Question by question

First run. p is the exact two-sided sign test on the questions that only one of the two got right.

| A | B | Only A right | Only B right | p |
| --- | --- | --- | --- | --- |
| no tools | one python tool | 12 | 13 | 1 |
