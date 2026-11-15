# repo2tools report: idna-sample

- Repo: https://github.com/kjd/idna at `d357725082245ff90f5cf8800a3fc297b1f2319a`
- Package: `idna`, 29 public callables
- Model: `qwen3-coder`, thinking off, temperature 0
- Sandbox: macOS sandbox-exec: no network, home folder unreadable, one scratch folder writable
- Time: 0.5 min. LLM tokens: 86,928 in 60 requests (propose 2,125, spec 43,226, code 41,577)

## Result

| | Tools |
| --- | --- |
| Picked by the LLM | 20 (dropped: 0, for unknown functions, duplicates or bad names) |
| Accepted | 16 |
| Accepted and confirmed against a direct library call | 15 |
| Passed all checks on the first try | 11 |
| Rejected after the repair rounds | 4 |

First try, by the first check that failed: ok: 11, spec: 5, differential: 4.

**Limit of these checks:** the same model wrote the tool and the direct call it is compared with, so they can share a misunderstanding of the library. The checks catch wrapper bugs (wrong field, wrong conversion, crashes), not a wrong idea of what the library does. A real score needs exercises with known answers.

## Accepted tools

| Tool | Wraps | Repairs | Samples: same / both error | Confirmed |
| --- | --- | --- | --- | --- |
| `encode_domain_name` | `idna.encode` | 0 | 4 / 1 | yes |
| `decode_domain_name` | `idna.decode` | 0 | 5 / 1 | yes |
| `convert_to_a_label` | `idna.alabel` | 0 | 3 / 2 | yes |
| `convert_to_u_label` | `idna.ulabel` | 1 | 2 / 4 | yes |
| `check_bidi_rule` | `idna.check_bidi` | 0 | 5 / 0 | yes |
| `check_hyphen_usage` | `idna.check_hyphen_ok` | 0 | 3 / 3 | yes |
| `check_initial_combiner` | `idna.check_initial_combiner` | 0 | 4 / 1 | yes |
| `check_nfc_normalization` | `idna.check_nfc` | 0 | 4 / 1 | yes |
| `apply_uts46_mapping` | `idna.uts46_remap` | 0 | 3 / 2 | yes |
| `validate_contextj_rule` | `idna.valid_contextj` | 0 | 5 / 0 | yes |
| `validate_contexto_rule` | `idna.valid_contexto` | 0 | 6 / 0 | yes |
| `create_idna_codec` | `idna.codec.Codec` | 3 | 6 / 0 | yes |
| `create_incremental_encoder` | `idna.codec.IncrementalEncoder` | 3 | 3 / 2 | yes |
| `create_incremental_decoder` | `idna.codec.IncrementalDecoder` | 1 | 0 / 0 | no: unstable |
| `compat_to_ascii` | `idna.compat.ToASCII` | 0 | 4 / 1 | yes |
| `compat_to_unicode` | `idna.compat.ToUnicode` | 3 | 4 / 1 | yes |

## Rejected tools

| Tool | Wraps | Last failed check | Error |
| --- | --- | --- | --- |
| `validate_idna_label` | `idna.check_label` | spec | the reply must be a JSON object with parameters, direct_call and samples |
| `validate_label_length` | `idna.valid_label_length` | spec | the reply must be a JSON object with parameters, direct_call and samples |
| `validate_domain_length` | `idna.valid_string_length` | spec | the reply must be a JSON object with parameters, direct_call and samples |
| `check_integer_in_ranges` | `idna.intranges_contain` | spec | direct_call may not use GeneratorExp: only calls, attributes, names, constants and simple conditions |

## Use

```sh
uv run repo2tools run-model <exercises> --mode tools --base-url <url> --model <model> -- toolsets/generated/idna-sample/run_server.sh
```
