# repo2tools report: itsdangerous-sample

- Repo: https://github.com/pallets/itsdangerous at `672971d66a2ef9f85151e53283113f33d642dabd`
- Package: `itsdangerous`, 38 public callables
- Model: `qwen3-coder`, thinking off, temperature 0
- Sandbox: macOS sandbox-exec: no network, home folder unreadable, one scratch folder writable
- Time: 0.8 min. LLM tokens: 91,091 in 57 requests (propose 2,921, spec 50,389, code 37,781)

## Result

| | Tools |
| --- | --- |
| Picked by the LLM | 15 (dropped: 0, for unknown functions, duplicates or bad names) |
| Accepted | 8 |
| Accepted and confirmed against a direct library call | 5 |
| Passed all checks on the first try | 5 |
| Rejected after the repair rounds | 7 |

First try, by the first check that failed: ok: 5, spec: 5, differential: 3, fastmcp: 1, loads: 1.

**Limit of these checks:** the same model wrote the tool and the direct call it is compared with, so they can share a misunderstanding of the library. The checks catch wrapper bugs (wrong field, wrong conversion, crashes), not a wrong idea of what the library does. A real score needs exercises with known answers.

## Accepted tools

| Tool | Wraps | Repairs | Samples: same / both error | Confirmed |
| --- | --- | --- | --- | --- |
| `create_serializer` | `itsdangerous.Serializer` | 2 | 0 / 0 | no: unstable |
| `serialize_and_sign` | `itsdangerous.Serializer.dumps` | 0 | 5 / 0 | yes |
| `deserialize_without_verification` | `itsdangerous.Serializer.loads_unsafe` | 0 | 4 / 0 | yes |
| `create_timed_serializer` | `itsdangerous.TimedSerializer` | 1 | 0 / 0 | no: unstable |
| `create_signer` | `itsdangerous.Signer` | 1 | 0 / 0 | no: unstable |
| `sign_data` | `itsdangerous.Signer.sign` | 0 | 5 / 0 | yes |
| `verify_signature_only` | `itsdangerous.Signer.verify_signature` | 0 | 5 / 0 | yes |
| `base64_encode_url_safe` | `itsdangerous.base64_encode` | 0 | 6 / 0 | yes |

## Rejected tools

| Tool | Wraps | Last failed check | Error |
| --- | --- | --- | --- |
| `verify_and_deserialize` | `itsdangerous.Serializer.loads` | spec | the direct call failed on every sample, so nothing can be compared. Errors: ["BadSignature: Signature b'SflKxwRJSMeKKF2QT4fwpMeJf36POk6yJV_adQssw5c' does not match"]. Use samples that are valid for the library. |
| `verify_and_deserialize_with_expiry` | `itsdangerous.TimedSerializer.loads` | spec | the reply must be a JSON object with parameters, direct_call and samples |
| `verify_and_extract` | `itsdangerous.Signer.unsign` | spec | the direct call failed on every sample, so nothing can be compared. Errors: ["BadSignature: Signature b'bar' does not match", "BadSignature: Signature b'data' does not match", "BadSignature: Signature b'signature' does n |
| `sign_with_timestamp` | `itsdangerous.TimestampSigner.sign` | end_to_end | over MCP it returned "special chars: !@#$%^&*().avmyDA.Ukvd9MtiI8fKKEfiYv_P_94v1D0", in the check "special chars: !@#$%^&*().avmx-w.7QfVbGXajS0uhDdQIwOilCusb1Y" |
| `verify_and_extract_with_timestamp` | `itsdangerous.TimestampSigner.unsign` | spec | the reply must be a JSON object with parameters, direct_call and samples |
| `base64_decode_url_safe` | `itsdangerous.base64_decode` | differential | Input {"string": "invalid_base64"}: the tool raised UnicodeDecodeError: 'utf-8' codec can't decode byte 0x8a in position 0: invalid start byte, but the direct library call returned "\ufffd{\u0696'\u007fm\ufffd\u001e\ufff |
| `convert_to_bytes` | `itsdangerous.want_bytes` | spec | the reply must be a JSON object with parameters, direct_call and samples |

## Use

```sh
uv run repo2tools run-model <exercises> --mode tools --base-url <url> --model <model> -- toolsets/generated/itsdangerous-sample/run_server.sh
```
