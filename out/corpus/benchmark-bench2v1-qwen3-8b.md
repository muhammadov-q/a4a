# Tools against no tools, on the questions of out/corpus/tasks-v1/ (bench2v1)

A tool call that the model wrote as text is run as a call, and the Python tool's output is shown as text.

Model `qwen3-8b`. 7 repositories with every condition, 80 questions, 1 run each. Right answers: no tools 42 (52%); one python tool 49 (61%).

A cell is the number of right answers: the mean of the runs, then each run in brackets.

| Package | Questions | Tools accepted | No tools | One Python tool |
| --- | --- | --- | --- | --- |
| `dateutil` | 5 | none | 1 | 3 |
| `fsspec` | 5 | none | none | none |
| `huggingface_hub` | 1 | none | none | none |
| `mcp` | 4 | none | none | none |
| `more_itertools` | 12 | none | 6 | 5 |
| `networkx` | 16 | none | 7 | 11 |
| `jinja2` | 3 | none | 2 | 2 |
| `werkzeug` | 9 | none | 4 | 9 |
| `pyasn1` | 1 | none | none | none |
| `distlib` | 3 | none | none | none |
| `packaging` | 23 | none | 15 | 10 |
| `attrs` | 1 | none | none | none |
| `jsonschema` | 1 | none | none | none |
| `pytz` | 1 | none | none | none |
| `rsa` | 12 | none | 7 | 9 |
| **7 repositories with every condition** | **80** | | **42 (52%)** | **49 (61%)** |

## How the tools were used

Means over the runs.

| Package | Condition | Questions with a tool call | Right among those | Tool calls | Calls that gave an error | Calls written as text, and run |
| --- | --- | --- | --- | --- | --- | --- |
| `dateutil` | one python tool | 5.0 of 5 | 3.0 | 7.0 | 3.0 | 0.0 |
| `more_itertools` | one python tool | 12.0 of 12 | 5.0 | 26.0 | 12.0 | 0.0 |
| `networkx` | one python tool | 16.0 of 16 | 11.0 | 63.0 | 47.0 | 28.0 |
| `jinja2` | one python tool | 3.0 of 3 | 2.0 | 26.0 | 24.0 | 4.0 |
| `werkzeug` | one python tool | 9.0 of 9 | 9.0 | 14.0 | 5.0 | 0.0 |
| `packaging` | one python tool | 23.0 of 23 | 10.0 | 195.0 | 187.0 | 50.0 |
| `rsa` | one python tool | 12.0 of 12 | 9.0 | 16.0 | 2.0 | 0.0 |

## By kind of answer

First run. A true-or-false question can be answered right by guessing half of the time.

| The answer is | Questions | No tools | One Python tool |
| --- | --- | --- | --- |
| true or false | 33 | 23 (70%) | 16 (48%) |
| another value | 47 | 19 (40%) | 33 (70%) |

## Question by question

First run. p is the exact two-sided sign test on the questions that only one of the two got right.

| A | B | Only A right | Only B right | p |
| --- | --- | --- | --- | --- |
| no tools | one python tool | 13 | 20 | 0.3 |
