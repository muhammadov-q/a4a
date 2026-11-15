# repo2tools report: python-rsa-bench2

- Repo: https://github.com/sybrenstuvel/python-rsa at `42b0e14ffbeeb9d99d1037e6440a2cc61780e4ea`
- Package: `rsa`, 44 public callables
- Model: `qwen3-coder`, thinking off, temperature 0
- Sandbox: macOS sandbox-exec: no network, home folder unreadable, one scratch folder writable
- Time: 1.6 min. LLM tokens: 126,940 in 88 requests (propose 2,911, spec 65,920, code 58,109)

## Result

| | Tools |
| --- | --- |
| Picked by the LLM | 24 (dropped: 0, for unknown functions, duplicates or bad names) |
| Accepted | 11 |
| Accepted and confirmed against a direct library call | 8 |
| Passed all checks on the first try | 11 |
| Rejected after the repair rounds | 13 |

First try, by the first check that failed: ok: 11, spec: 8, differential: 2, fastmcp: 1, loads: 1, static: 1.

**Limit of these checks:** the same model wrote the tool and the direct call it is compared with, so they can share a misunderstanding of the library. The checks catch wrapper bugs (wrong field, wrong conversion, crashes), not a wrong idea of what the library does. A real score needs exercises with known answers.

## Accepted tools

| Tool | Wraps | Repairs | Samples: same / both error | Confirmed |
| --- | --- | --- | --- | --- |
| `blinded_decrypt` | `rsa.PrivateKey.blinded_decrypt` | 0 | 2 / 2 | yes |
| `get_integer_bit_size` | `rsa.common.bit_size` | 0 | 6 / 0 | yes |
| `get_integer_byte_size` | `rsa.common.byte_size` | 0 | 6 / 0 | yes |
| `extended_euclidean_algorithm` | `rsa.common.extended_gcd` | 0 | 5 / 0 | yes |
| `modular_inverse` | `rsa.common.inverse` | 0 | 4 / 1 | yes |
| `encrypt_integer` | `rsa.core.encrypt_int` | 0 | 4 / 1 | yes |
| `decrypt_integer` | `rsa.core.decrypt_int` | 0 | 5 / 0 | yes |
| `generate_prime_number` | `rsa.prime.getprime` | 0 | 0 / 2 | no: unstable, both_error |
| `check_coprime` | `rsa.prime.are_relatively_prime` | 0 | 5 / 0 | yes |
| `read_random_integer` | `rsa.randnum.read_random_int` | 0 | 1 / 1 | no: unstable, both_error |
| `read_random_odd_integer` | `rsa.randnum.read_random_odd_int` | 0 | 0 / 1 | no: unstable, both_error |

## Rejected tools

| Tool | Wraps | Last failed check | Error |
| --- | --- | --- | --- |
| `generate_rsa_keys` | `rsa.newkeys` | end_to_end | returned a value over MCP, but raised in the check |
| `encrypt_message` | `rsa.encrypt` | spec | the reply must be a JSON object with parameters, direct_call and samples |
| `decrypt_message` | `rsa.decrypt` | spec | the direct_call expression is wrong: AttributeError: 'str' object has no attribute 'n' |
| `sign_message` | `rsa.sign` | spec | the direct call failed on every sample, so nothing can be compared. Errors: ['AssertionError: ']. Use samples that are valid for the library. |
| `verify_signature` | `rsa.verify` | spec | the direct call failed on every sample, so nothing can be compared. Errors: ['VerificationError: Verification failed']. Use samples that are valid for the library. |
| `load_public_key_pem` | `rsa.PublicKey.load_pkcs1_openssl_pem` | spec | the direct_call expression is wrong: ModuleNotFoundError: No module named 'pyasn1' |
| `load_public_key_der` | `rsa.PublicKey.load_pkcs1_openssl_der` | spec | the direct_call expression is wrong: ModuleNotFoundError: No module named 'pyasn1' |
| `find_signature_hash_method` | `rsa.find_signature_hash` | spec | the direct_call expression is wrong: AttributeError: 'dict' object has no attribute 'n' |
| `compute_message_hash` | `rsa.compute_hash` | spec | the direct_call expression is wrong: ModuleNotFoundError: No module named 'isinstance' |
| `sign_precomputed_hash` | `rsa.sign_hash` | spec | the direct call failed on every sample, so nothing can be compared. Errors: ["TypeError: PrivateKey.__init__() missing 3 required positional arguments: 'd', 'p', and 'q'", 'ValueError: non-hexadecimal number found in fro |
| `read_random_bits` | `rsa.randnum.read_random_bits` | differential | Input {"nbits": 8}: the tool raised PydanticSerializationError: Error serializing to JSON: invalid utf-8 sequence of 1 bytes from index 0, but the direct library call returned "F" Input {"nbits": 16}: the tool raised Pyd |
| `convert_bytes_to_integer` | `rsa.transform.bytes2int` | spec | the reply must be a JSON object with parameters, direct_call and samples |
| `convert_integer_to_bytes` | `rsa.transform.int2bytes` | differential | Input {"fill_size": 1, "number": 255}: the tool raised PydanticSerializationError: Error serializing to JSON: invalid utf-8 sequence of 1 bytes from index 0, but the direct library call returned "\ufffd" |

## Use

```sh
uv run repo2tools run-model <exercises> --mode tools --base-url <url> --model <model> -- toolsets/generated/python-rsa-bench2/run_server.sh
```
