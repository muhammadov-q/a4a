# Generated tools against no tools, on each library's own documentation questions (bench2)

Model `qwen3-8b`. 7 repositories with both runs, 120 questions: 54 right without tools (45%), 34 right with the generated tools (28%). One run each.

| Package | Questions | Tools picked | Tools accepted | Right without tools | Right with tools | Called a tool | Right when it called | Tool errors |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| `dateutil` | 11 | 1 | 1 | 4 | 3 | 9 | 1 | 2 |
| `mcp` | 15 | 54 | 0 | 10 | none | none | none | none |
| `more_itertools` | 19 | 59 | 25 | 10 | 9 | 10 | 4 | 5 |
| `networkx` | 20 | 45 | 3 | 6 | 0 | 12 | 0 | 44 |
| `jinja2` | 9 | 58 | 11 | 6 | 6 | 3 | 2 | 0 |
| `werkzeug` | 16 | 60 | 26 | 7 | 4 | 11 | 2 | 4 |
| `packaging` | 28 | 60 | 41 | 14 | 8 | 22 | 8 | 23 |
| `rsa` | 17 | 24 | 11 | 7 | 4 | 6 | 2 | 0 |
