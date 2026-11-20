# Tools against no tools, on the questions of out/corpus/tasks-v1/ (bench2v1)

A tool call that the model wrote as text is run as a call, and the Python tool's output is shown as text.

Model `qwen3-32b`. 7 repositories with every condition, 80 questions, 1 run each. Right answers: no tools 50 (62%); one python tool 51 (64%).

A cell is the number of right answers: the mean of the runs, then each run in brackets.

| Package | Questions | Tools accepted | No tools | One Python tool |
| --- | --- | --- | --- | --- |
| `dateutil` | 5 | none | 2 | 4 |
| `fsspec` | 5 | none | none | none |
| `huggingface_hub` | 1 | none | none | none |
| `mcp` | 4 | none | none | none |
| `more_itertools` | 12 | none | 6 | 3 |
| `networkx` | 16 | none | 6 | 10 |
| `jinja2` | 3 | none | 3 | 2 |
| `werkzeug` | 9 | none | 9 | 9 |
| `pyasn1` | 1 | none | none | none |
| `distlib` | 3 | none | none | none |
| `packaging` | 23 | none | 17 | 13 |
| `attrs` | 1 | none | none | none |
| `jsonschema` | 1 | none | none | none |
| `pytz` | 1 | none | none | none |
| `rsa` | 12 | none | 7 | 10 |
| **7 repositories with every condition** | **80** | | **50 (62%)** | **51 (64%)** |

## How the tools were used

Means over the runs.

| Package | Condition | Questions with a tool call | Right among those | Tool calls | Calls that gave an error | Calls written as text, and run |
| --- | --- | --- | --- | --- | --- | --- |
| `dateutil` | one python tool | 5.0 of 5 | 4.0 | 5.0 | 0.0 | 0.0 |
| `more_itertools` | one python tool | 12.0 of 12 | 3.0 | 14.0 | 4.0 | 0.0 |
| `networkx` | one python tool | 16.0 of 16 | 10.0 | 17.0 | 3.0 | 0.0 |
| `jinja2` | one python tool | 3.0 of 3 | 2.0 | 3.0 | 0.0 | 0.0 |
| `werkzeug` | one python tool | 9.0 of 9 | 9.0 | 9.0 | 0.0 | 0.0 |
| `packaging` | one python tool | 23.0 of 23 | 13.0 | 34.0 | 17.0 | 0.0 |
| `rsa` | one python tool | 12.0 of 12 | 10.0 | 12.0 | 2.0 | 0.0 |

## By kind of answer

First run. A true-or-false question can be answered right by guessing half of the time.

| The answer is | Questions | No tools | One Python tool |
| --- | --- | --- | --- |
| true or false | 33 | 26 (79%) | 19 (58%) |
| another value | 47 | 24 (51%) | 32 (68%) |

## Question by question

First run. p is the exact two-sided sign test on the questions that only one of the two got right.

| A | B | Only A right | Only B right | p |
| --- | --- | --- | --- | --- |
| no tools | one python tool | 15 | 16 | 1 |
