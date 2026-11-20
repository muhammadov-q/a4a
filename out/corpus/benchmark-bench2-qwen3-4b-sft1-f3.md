# Tools against no tools, on each library's own documentation questions (bench2)

A tool call that the model wrote as text is run as a call, and the Python tool's output is shown as text.

Model `qwen3-4b-sft1-f3`. 2 repositories with every condition, 26 questions, 3 runs each. Right answers: no tools 11.0 (42%) (11, 11, 11); one python tool 15.3 (59%) (15, 16, 15).

A cell is the number of right answers: the mean of the runs, then each run in brackets.

| Package | Questions | Tools accepted | No tools | One Python tool |
| --- | --- | --- | --- | --- |
| `dateutil` | 11 | 1 of 1 | none | none |
| `mcp` | 15 | 0 of 54 | none | none |
| `more_itertools` | 19 | 25 of 59 | none | none |
| `networkx` | 20 | 3 of 45 | none | none |
| `jinja2` | 9 | 11 of 58 | 5.0 (5, 5, 5) | 2.3 (2, 3, 2) |
| `werkzeug` | 16 | 26 of 60 | none | none |
| `packaging` | 28 | 41 of 60 | none | none |
| `rsa` | 17 | 11 of 24 | 6.0 (6, 6, 6) | 13.0 (13, 13, 13) |
| **2 repositories with every condition** | **26** | | **11.0 (42%) (11, 11, 11)** | **15.3 (59%) (15, 16, 15)** |

## How the tools were used

Means over the runs.

| Package | Condition | Questions with a tool call | Right among those | Tool calls | Calls that gave an error | Calls written as text, and run |
| --- | --- | --- | --- | --- | --- | --- |
| `jinja2` | one python tool | 8.7 of 9 | 2.0 | 155.0 | 150.0 | 0.0 |
| `rsa` | one python tool | 17.0 of 17 | 13.0 | 145.0 | 133.0 | 0.0 |

## By kind of answer

First run. A true-or-false question can be answered right by guessing half of the time.

| The answer is | Questions | No tools | One Python tool |
| --- | --- | --- | --- |
| true or false | 12 | 7 (58%) | 3 (25%) |
| another value | 14 | 4 (29%) | 12 (86%) |

## Question by question

First run. p is the exact two-sided sign test on the questions that only one of the two got right.

| A | B | Only A right | Only B right | p |
| --- | --- | --- | --- | --- |
| no tools | one python tool | 6 | 10 | 0.45 |
