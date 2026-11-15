# repo2tools report: dateutil-bench2

- Repo: https://github.com/dateutil/dateutil at `a78cbd81d5d03b5f126eb36edb92bca78972c804`
- Package: `dateutil`, 66 public callables
- Model: `qwen3-coder`, thinking off, temperature 0
- Sandbox: macOS sandbox-exec: no network, home folder unreadable, one scratch folder writable
- Time: 0.1 min. LLM tokens: 6,918 in 3 requests (propose 2,905, spec 1,943, code 2,070)

## Result

| | Tools |
| --- | --- |
| Picked by the LLM | 1 (dropped: 0, for unknown functions, duplicates or bad names) |
| Accepted | 1 |
| Accepted and confirmed against a direct library call | 1 |
| Passed all checks on the first try | 1 |
| Rejected after the repair rounds | 0 |

First try, by the first check that failed: ok: 1.

**Limit of these checks:** the same model wrote the tool and the direct call it is compared with, so they can share a misunderstanding of the library. The checks catch wrapper bugs (wrong field, wrong conversion, crashes), not a wrong idea of what the library does. A real score needs exercises with known answers.

## Accepted tools

| Tool | Wraps | Repairs | Samples: same / both error | Confirmed |
| --- | --- | --- | --- | --- |
| `parse_date_string` | `dateutil.parser.parse` | 0 | 4 / 1 | yes |

## Use

```sh
uv run repo2tools run-model <exercises> --mode tools --base-url <url> --model <model> -- toolsets/generated/dateutil-bench2/run_server.sh
```
