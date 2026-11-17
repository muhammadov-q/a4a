# Examples written by a model, with and without a target

Model `qwen3-coder`, 40 requests per way and repository, and for the aimed ways one request for every open element, 4 repositories with 385 public API elements together. The verified documentation exercises of these repositories use 223 of them (58%).

| Way | What the model is told | Requests | Drafts | Verified | Use the API | Different | API elements used | New (not used by documentation exercises) | Per request |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| free | Only the name of the library | 160 | 154 | 151 | 122 | 24 | 6 | 0 | 0.00 |
| listed | Also the names of the public API | 160 | 160 | 158 | 157 | 24 | 9 | 0 | 0.00 |
| named | One API element per request, by name | 162 | 160 | 59 | 57 | 57 | 56 | 50 | 0.31 |
| target | The same element, with its signature and documentation | 162 | 157 | 78 | 74 | 78 | 75 | 68 | 0.42 |

Way `named`: 50 of 162 requests give a verified example that uses the element it was asked to use (31%).
Way `target`: 66 of 162 requests give a verified example that uses the element it was asked to use (41%).

The two aimed ways ask for the same 162 elements. Reached both ways: 40. Only with the signature and documentation: 26. Only by name: 10. Neither: 86. Exact two-sided sign test on the elements reached one way only: p = 0.011.
All ways together use 92 elements (24%); with the documentation exercises, 300 (78%).

What happened to the requests (no_code: the reply held no code that ends in a value; error: the code raised; not_repeatable: two runs differ; not_json: the value is an object):

| Way | verified | no_code | error | not_repeatable | not_json | timeout |
| --- | --- | --- | --- | --- | --- | --- |
| free | 151 | 6 | 0 | 1 | 2 | 0 |
| listed | 158 | 0 | 2 | 0 | 0 | 0 |
| named | 59 | 2 | 73 | 8 | 20 | 0 |
| target | 78 | 5 | 60 | 8 | 11 | 0 |

"Per request" is new elements for one request: what a request buys. "Different" counts examples whose code is not the same as another one of the same way.

## Per repository

| Package | API | Used by documentation exercises | Open | Asked for | free: new | listed: new | named: hits | named: new | target: hits | target: new | Used at the end |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| `packaging` | 99 | 54 | 45 | 45 | 0 | 0 | 11 | 11 | 17 | 17 | 72 (73%) |
| `python-dateutil` | 66 | 12 | 54 | 54 | 0 | 0 | 22 | 22 | 29 | 29 | 44 (67%) |
| `more-itertools` | 176 | 146 | 30 | 30 | 0 | 0 | 13 | 13 | 14 | 14 | 163 (93%) |
| `rsa` | 44 | 11 | 33 | 33 | 0 | 0 | 4 | 4 | 6 | 8 | 21 (48%) |
