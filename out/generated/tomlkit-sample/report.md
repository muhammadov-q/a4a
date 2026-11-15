# repo2tools report: tomlkit-sample

- Repo: https://github.com/python-poetry/tomlkit at `7bf7284dbd622557d9909f8fee017a4cb169a139`
- Package: `tomlkit`, 183 public callables
- Model: `qwen3-coder`, thinking off, temperature 0
- Sandbox: macOS sandbox-exec: no network, home folder unreadable, one scratch folder writable
- Time: 1.8 min. LLM tokens: 276,532 in 242 requests (propose 7,702, spec 106,258, code 162,572)

## Result

| | Tools |
| --- | --- |
| Picked by the LLM | 59 (dropped: 0, for unknown functions, duplicates or bad names) |
| Accepted | 23 |
| Accepted and confirmed against a direct library call | 23 |
| Passed all checks on the first try | 15 |
| Rejected after the repair rounds | 36 |

First try, by the first check that failed: ok: 15, spec: 15, fastmcp: 9, loads: 9, differential: 7, static: 2, runs: 2.

**Limit of these checks:** the same model wrote the tool and the direct call it is compared with, so they can share a misunderstanding of the library. The checks catch wrapper bugs (wrong field, wrong conversion, crashes), not a wrong idea of what the library does. A real score needs exercises with known answers.

## Accepted tools

| Tool | Wraps | Repairs | Samples: same / both error | Confirmed |
| --- | --- | --- | --- | --- |
| `create_aot` | `tomlkit.api.AoT` | 0 | 5 / 0 | yes |
| `create_datetime` | `tomlkit.api.DateTime` | 1 | 4 / 1 | yes |
| `create_integer` | `tomlkit.api.Integer` | 0 | 5 / 0 | yes |
| `create_single_key` | `tomlkit.api.SingleKey` | 3 | 6 / 0 | yes |
| `create_trivia` | `tomlkit.api.Trivia` | 0 | 5 / 0 | yes |
| `create_whitespace` | `tomlkit.api.Whitespace` | 0 | 5 / 0 | yes |
| `make_aot` | `tomlkit.aot` | 0 | 4 / 0 | yes |
| `make_comment` | `tomlkit.comment` | 2 | 5 / 0 | yes |
| `make_date` | `tomlkit.date` | 0 | 3 / 2 | yes |
| `make_document` | `tomlkit.document` | 0 | 2 / 0 | yes |
| `dump_to_string` | `tomlkit.dumps` | 0 | 4 / 1 | yes |
| `make_float_item` | `tomlkit.float_` | 0 | 4 / 1 | yes |
| `make_key` | `tomlkit.key` | 1 | 5 / 0 | yes |
| `parse_string` | `tomlkit.loads` | 0 | 4 / 1 | yes |
| `make_newline` | `tomlkit.nl` | 0 | 2 / 0 | yes |
| `parse_toml` | `tomlkit.parse` | 0 | 4 / 1 | yes |
| `register_custom_encoder` | `tomlkit.register_encoder` | 3 | 4 / 0 | yes |
| `make_string_item` | `tomlkit.string` | 0 | 6 / 0 | yes |
| `make_table` | `tomlkit.table` | 1 | 5 / 0 | yes |
| `unregister_encoder` | `tomlkit.unregister_encoder` | 0 | 4 / 0 | yes |
| `make_whitespace_from_string` | `tomlkit.ws` | 1 | 5 / 0 | yes |
| `merge_toml_dicts` | `tomlkit.container.merge_dicts` | 0 | 5 / 0 | yes |
| `copy_table` | `tomlkit.items.AbstractTable.copy` | 2 | 4 / 0 | yes |

## Rejected tools

| Tool | Wraps | Last failed check | Error |
| --- | --- | --- | --- |
| `create_container` | `tomlkit.api.Container` | differential | Input {"parsed": false}: the tool returned {"parsed": false, "type": "container"}, but the direct library call returned {} Input {"parsed": true}: the tool returned {"parsed": true, "type": "container"}, but the direct l |
| `create_array` | `tomlkit.api.Array` | differential | Input {"multiline": false, "value": [1, 2, 3]}: the tool returned "[123]", but the direct library call returned [1, 2, 3] Input {"multiline": true, "value": ["a", "b", "c"]}: the tool returned "[\n \"a\",\n \"b\",\n \"c\ |
| `create_bool` | `tomlkit.api.Bool` | differential | Input {"value": true}: the tool returned true, but the direct library call returned "True" Input {"value": false}: the tool returned false, but the direct library call returned "False" Input {"value": 1}: the tool return |
| `create_comment` | `tomlkit.api.Comment` | loads | the check process died: File "/Users/qobiljonmuhammadov/Notes S2026/agentic-llms/code/repo2tools/src/repo2tools/synthesis/worker.py", line 297, in check "direct": canonical(to_json(direct["value"])) if "value" in direct  |
| `create_date` | `tomlkit.api.Date` | differential | Input {"day": 5, "month": 10, "year": 2023}: the tool returned "", but the direct library call returned "2023-10-05" Input {"day": 29, "month": 2, "year": 2000}: the tool returned "", but the direct library call returned |
| `create_float` | `tomlkit.api.Float` | differential | Input {"raw": "3.14", "value": 3.14}: the tool returned "3.14", but the direct library call returned 3.14 Input {"raw": "-2.5", "value": -2.5}: the tool returned "-2.5", but the direct library call returned -2.5 Input {" |
| `create_inline_table` | `tomlkit.api.InlineTable` | differential | Input {"new": false, "trivia": {"comment": "", "indent": " "}, "value": {"key1": "value1", "key2": "value2"}}: the tool returned "{key1 = \"value1\",key2 = \"value2\"}", but the direct library call returned {} Input {"ne |
| `create_key` | `tomlkit.api.Key` | spec | the direct call failed on every sample, so nothing can be compared. Errors: ['TypeError: Key() takes no arguments']. Use samples that are valid for the library. |
| `create_string` | `tomlkit.api.String` | spec | the direct_call expression is wrong: ModuleNotFoundError: No module named 'getattr' |
| `create_table` | `tomlkit.api.Table` | spec | the direct_call expression is wrong: AttributeError: 'dict' object has no attribute 'body' |
| `create_time` | `tomlkit.api.Time` | differential | Input {"hour": 0, "microsecond": 0, "minute": 0, "second": 0, "tzinfo": null}: the tool returned "00:00:00.000000", but the direct library call returned "00:00:00" Input {"hour": 15, "microsecond": 0, "minute": 30, "seco |
| `make_array` | `tomlkit.array` | runs | Input {"raw": "[]"}: the tool raised output is not JSON: , but the direct library call returned [] Input {"raw": "[\"a\", \"b\", \"c\"]"}: the tool raised output is not JSON: abc, but the direct library call returned ["a |
| `make_boolean` | `tomlkit.boolean` | differential | Input {"raw": "true"}: the tool returned true, but the direct library call returned "True" Input {"raw": "false"}: the tool returned false, but the direct library call returned "False" Input {"raw": "True"}: the tool ret |
| `make_datetime` | `tomlkit.datetime` | differential | Input {"raw": "2023-01-01T12:00:00Z"}: the tool returned "2023-01-01 12:00:00+00:00", but the direct library call returned "2023-01-01T12:00:00+00:00" Input {"raw": "2023-12-31T23:59:59.999999+05:00"}: the tool returned  |
| `dump_to_file` | `tomlkit.dump` | spec | the direct_call expression is wrong: AttributeError: 'str' object has no attribute 'write' |
| `make_inline_table` | `tomlkit.inline_table` | differential | Input {}: the tool returned "{}", but the direct library call returned {} Input {}: the tool returned "{}", but the direct library call returned {} Input {}: the tool returned "{}", but the direct library call returned { |
| `make_integer_item` | `tomlkit.integer` | static | line 18: no code at module level except imports, definitions and constants |
| `make_toml_item` | `tomlkit.item` | differential | Input {"value": [1, 2, 3]}: the tool returned "[1, 2, 3]", but the direct library call returned [1, 2, 3] Input {"value": {"a": 1, "b": 2}}: the tool returned "{'a': 1, 'b': 2}", but the direct library call returned {"a" |
| `parse_key_value` | `tomlkit.key_value` | differential | Input {"src": "foo = 1"}: the tool returned ["foo ", "1"], but the direct library call returned ["foo ", 1] Input {"src": "array = [1, 2, 3]"}: the tool returned ["array ", "[1, 2, 3]"], but the direct library call retur |
| `load_from_file` | `tomlkit.load` | spec | the direct_call expression is wrong: AttributeError: 'str' object has no attribute 'read' |
| `make_time` | `tomlkit.time` | differential | Input {"raw": "12:30:45"}: the tool raised ValueError: Invalid time string: '12:30:45', but the direct library call returned "12:30:45" Input {"raw": "23:59:59.999999"}: the tool raised ValueError: Invalid time string: ' |
| `parse_simple_value` | `tomlkit.value` | differential | Input {"raw": "true"}: the tool returned true, but the direct library call returned "True" |
| `decode_toml_string` | `tomlkit.container.decode` | differential | Input {"encodings": ["utf-8", "latin1", "ascii"], "string": "key = \"value\""}: the tool returned {"key": "value"}, but the direct library call returned "key = \"value\"" Input {"encodings": ["utf-8"], "string": "name =  |
| `item_to_string` | `tomlkit.container.Item.as_string` | spec | the direct_call expression is wrong: AttributeError: 'dict' object has no attribute 'as_string' |
| `unwrap_item` | `tomlkit.container.Item.unwrap` | spec | the direct_call expression is wrong: AttributeError: 'dict' object has no attribute 'unwrap' |
| `add_comment_to_item` | `tomlkit.container.Item.comment` | spec | the direct_call expression is wrong: AttributeError: 'str' object has no attribute 'comment' |
| `indent_item` | `tomlkit.container.Item.indent` | spec | the direct_call expression is wrong: AttributeError: 'dict' object has no attribute 'indent' |
| `is_boolean_item` | `tomlkit.container.Item.is_boolean` | spec | the direct_call expression is wrong: AttributeError: 'dict' object has no attribute 'is_boolean' |
| `is_table_item` | `tomlkit.container.Item.is_table` | spec | the direct_call expression is wrong: AttributeError: 'dict' object has no attribute 'is_table' |
| `is_inline_table_item` | `tomlkit.container.Item.is_inline_table` | spec | the direct_call expression is wrong: AttributeError: 'dict' object has no attribute 'is_inline_table' |
| `is_aot_item` | `tomlkit.container.Item.is_aot` | spec | the direct_call expression is wrong: AttributeError: 'dict' object has no attribute 'is_aot' |
| `append_to_table` | `tomlkit.items.AbstractTable.append` | spec | the direct call failed on every sample, so nothing can be compared. Errors: ["UnexpectedCharError: Unexpected character: '\\x00' at line 1 col 0", 'UnexpectedEofError: Unexpected end of file at line 1 col 0']. Use sample |
| `add_to_table` | `tomlkit.items.AbstractTable.add` | spec | the direct_call expression is wrong: AttributeError: 'str' object has no attribute 'add' |
| `remove_from_table` | `tomlkit.items.AbstractTable.remove` | spec | the direct_call expression is wrong: AttributeError: 'dict' object has no attribute 'remove' |
| `get_table_item` | `tomlkit.items.AbstractTable.item` | spec | the direct_call expression is wrong: AttributeError: 'dict' object has no attribute 'item' |
| `set_default_in_table` | `tomlkit.items.AbstractTable.setdefault` | spec | this parameter needs a snake_case name and a JSON type: {"name": "default_value", "type": "any", "description": "The default value to set if the key does not exist", "required": true} |

## Use

```sh
uv run repo2tools run-model <exercises> --mode tools --base-url <url> --model <model> -- toolsets/generated/tomlkit-sample/run_server.sh
```
