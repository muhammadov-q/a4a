# Examples written by a model, with and without a target

Model `qwen3-coder`, 40 requests per way and repository, 8 repositories with 3,003 public API elements together. The verified documentation exercises of these repositories use 427 of them (14%).

| Way | What the model is told | Requests | Drafts | Verified | Use the API | Different | API elements used | New (not used by documentation exercises) | Per request |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| free | Only the name of the library | 320 | 315 | 274 | 245 | 50 | 19 | 8 | 0.03 |
| listed | Also the names of the public API | 320 | 319 | 240 | 240 | 40 | 27 | 8 | 0.03 |
| named | One API element per request, by name | 303 | 296 | 104 | 101 | 102 | 108 | 94 | 0.31 |
| target | The same element, with its signature and documentation | 303 | 295 | 141 | 136 | 141 | 155 | 136 | 0.45 |

Way `named`: 84 of 303 requests give a verified example that uses the element it was asked to use (28%).
Way `target`: 122 of 303 requests give a verified example that uses the element it was asked to use (40%).

The two aimed ways ask for the same 303 elements. Reached both ways: 62. Only with the signature and documentation: 60. Only by name: 22. Neither: 159. Exact two-sided sign test on the elements reached one way only: p = 3.2e-05.
All ways together use 205 elements (7%); with the documentation exercises, 598 (20%).

What happened to the requests (no_code: the reply held no code that ends in a value; error: the code raised; not_repeatable: two runs differ; not_json: the value is an object):

| Way | verified | no_code | error | not_repeatable | not_json | timeout |
| --- | --- | --- | --- | --- | --- | --- |
| free | 274 | 5 | 40 | 0 | 1 | 0 |
| listed | 240 | 1 | 79 | 0 | 0 | 0 |
| named | 104 | 7 | 156 | 9 | 27 | 0 |
| target | 141 | 8 | 126 | 7 | 21 | 0 |

"Per request" is new elements for one request: what a request buys. "Different" counts examples whose code is not the same as another one of the same way.

## Per repository

| Package | API | Used by documentation exercises | Open | Asked for | free: new | listed: new | named: hits | named: new | target: hits | target: new | Used at the end |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| `packaging` | 99 | 54 | 45 | 40 | 0 | 0 | 12 | 12 | 17 | 17 | 73 (74%) |
| `python-dateutil` | 66 | 12 | 54 | 40 | 0 | 0 | 14 | 14 | 22 | 22 | 37 (56%) |
| `jinja2` | 489 | 8 | 481 | 40 | 1 | 2 | 4 | 7 | 7 | 11 | 21 (4%) |
| `mcp` | 513 | 7 | 506 | 40 | 0 | 0 | 3 | 3 | 10 | 11 | 20 (4%) |
| `werkzeug` | 436 | 14 | 422 | 40 | 6 | 1 | 18 | 23 | 23 | 26 | 52 (12%) |
| `more-itertools` | 176 | 146 | 30 | 30 | 0 | 0 | 14 | 14 | 17 | 17 | 166 (94%) |
| `networkx` | 1180 | 175 | 1005 | 40 | 1 | 5 | 16 | 18 | 19 | 23 | 208 (18%) |
| `rsa` | 44 | 11 | 33 | 33 | 0 | 0 | 3 | 3 | 7 | 9 | 21 (48%) |
