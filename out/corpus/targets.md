# Examples written by a model, with and without a target

Model `qwen3-coder`, 40 requests per way and repository, 8 repositories with 3,003 public API elements together. The verified documentation exercises of these repositories use 427 of them (14%).

| Way | What the model is told | Requests | Drafts | Verified | Use the API | Different | API elements used | New (not used by documentation exercises) | Per request |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| free | Only the name of the library | 320 | 314 | 273 | 244 | 51 | 20 | 8 | 0.03 |
| listed | Also the names of the public API | 320 | 319 | 239 | 239 | 35 | 24 | 8 | 0.03 |
| target | One API element per request | 303 | 293 | 138 | 132 | 138 | 151 | 132 | 0.44 |

With a target, 118 of 138 verified examples use the element they were asked to use (86%); that is 39% of the requests.
All three ways together use 174 elements (6%); with the documentation exercises, 569 (19%).

What happened to the requests (no_code: the reply held no code that ends in a value; error: the code raised; not_repeatable: two runs differ; not_json: the value is an object):

| Way | verified | no_code | error | not_repeatable | not_json | timeout |
| --- | --- | --- | --- | --- | --- | --- |
| free | 273 | 6 | 40 | 0 | 1 | 0 |
| listed | 239 | 1 | 80 | 0 | 0 | 0 |
| target | 138 | 10 | 128 | 6 | 19 | 2 |

"Per request" is new elements for one request: what a request buys. "Different" counts examples whose code is not the same as another one of the same way.

## Per repository

| Package | API | Used by documentation exercises | free: verified | free: new | listed: verified | listed: new | target: verified | target: hits | target: new |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| `packaging` | 99 | 54 | 40 | 0 | 40 | 0 | 20 | 17 | 17 |
| `python-dateutil` | 66 | 12 | 40 | 0 | 40 | 0 | 25 | 22 | 22 |
| `jinja2` | 489 | 8 | 40 | 1 | 40 | 2 | 14 | 6 | 10 |
| `mcp` | 513 | 7 | 0 | 0 | 0 | 0 | 9 | 8 | 9 |
| `werkzeug` | 436 | 14 | 40 | 6 | 4 | 1 | 24 | 21 | 24 |
| `more-itertools` | 176 | 146 | 34 | 0 | 39 | 0 | 16 | 14 | 14 |
| `networkx` | 1180 | 175 | 40 | 1 | 37 | 5 | 22 | 22 | 27 |
| `rsa` | 44 | 11 | 39 | 0 | 39 | 0 | 8 | 8 | 9 |
