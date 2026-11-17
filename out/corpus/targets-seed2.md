# Examples written by a model, with and without a target

Model `qwen3-coder`, 40 requests per way and repository, 8 repositories with 3,003 public API elements together. The verified documentation exercises of these repositories use 427 of them (14%).

| Way | What the model is told | Requests | Drafts | Verified | Use the API | Different | API elements used | New (not used by documentation exercises) | Per request |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| free | Only the name of the library | 320 | 317 | 276 | 247 | 45 | 19 | 7 | 0.02 |
| listed | Also the names of the public API | 320 | 320 | 235 | 234 | 34 | 20 | 7 | 0.02 |
| named | One API element per request, by name | 303 | 298 | 107 | 102 | 107 | 107 | 95 | 0.31 |
| target | The same element, with its signature and documentation | 303 | 292 | 122 | 119 | 122 | 138 | 122 | 0.40 |

Way `named`: 86 of 303 requests give a verified example that uses the element it was asked to use (28%).
Way `target`: 107 of 303 requests give a verified example that uses the element it was asked to use (35%).

The two aimed ways ask for the same 303 elements. Reached both ways: 66. Only with the signature and documentation: 41. Only by name: 20. Neither: 176. Exact two-sided sign test on the elements reached one way only: p = 0.0099.
All ways together use 181 elements (6%); with the documentation exercises, 579 (19%).

What happened to the requests (no_code: the reply held no code that ends in a value; error: the code raised; not_repeatable: two runs differ; not_json: the value is an object):

| Way | verified | no_code | error | not_repeatable | not_json | timeout |
| --- | --- | --- | --- | --- | --- | --- |
| free | 276 | 3 | 41 | 0 | 0 | 0 |
| listed | 235 | 0 | 85 | 0 | 0 | 0 |
| named | 107 | 5 | 156 | 9 | 26 | 0 |
| target | 122 | 11 | 136 | 12 | 22 | 0 |

"Per request" is new elements for one request: what a request buys. "Different" counts examples whose code is not the same as another one of the same way.

## Per repository

| Package | API | Used by documentation exercises | Open | Asked for | free: new | listed: new | named: hits | named: new | target: hits | target: new | Used at the end |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| `packaging` | 99 | 54 | 45 | 40 | 0 | 0 | 11 | 11 | 15 | 15 | 70 (71%) |
| `python-dateutil` | 66 | 12 | 54 | 40 | 0 | 0 | 17 | 17 | 21 | 21 | 36 (55%) |
| `jinja2` | 489 | 8 | 481 | 40 | 1 | 2 | 4 | 7 | 7 | 13 | 22 (4%) |
| `mcp` | 513 | 7 | 506 | 40 | 0 | 0 | 3 | 3 | 8 | 8 | 17 (3%) |
| `werkzeug` | 436 | 14 | 422 | 40 | 5 | 0 | 18 | 22 | 18 | 21 | 46 (11%) |
| `more-itertools` | 176 | 146 | 30 | 30 | 0 | 0 | 14 | 14 | 14 | 14 | 164 (93%) |
| `networkx` | 1180 | 175 | 1005 | 40 | 1 | 5 | 16 | 18 | 19 | 23 | 205 (17%) |
| `rsa` | 44 | 11 | 33 | 33 | 0 | 0 | 3 | 3 | 5 | 7 | 19 (43%) |
