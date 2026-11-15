# repo2tools report: jmespath.py-sample

- Repo: https://github.com/jmespath/jmespath.py at `2812594e69d43098ef60f81f4efc404c071b0418`
- Package: `jmespath`, 60 public callables
- Model: `qwen3-coder`, thinking off, temperature 0
- Sandbox: macOS sandbox-exec: no network, home folder unreadable, one scratch folder writable
- Time: 1.0 min. LLM tokens: 94,963 in 93 requests (propose 3,003, spec 26,197, code 65,763)

## Result

| | Tools |
| --- | --- |
| Picked by the LLM | 31 (dropped: 1, for unknown functions, duplicates or bad names) |
| Accepted | 26 |
| Accepted and confirmed against a direct library call | 25 |
| Passed all checks on the first try | 18 |
| Rejected after the repair rounds | 5 |

First try, by the first check that failed: ok: 18, differential: 6, spec: 3, runs: 2, static: 1, syntax: 1.

**Limit of these checks:** the same model wrote the tool and the direct call it is compared with, so they can share a misunderstanding of the library. The checks catch wrapper bugs (wrong field, wrong conversion, crashes), not a wrong idea of what the library does. A real score needs exercises with known answers.

## Accepted tools

| Tool | Wraps | Repairs | Samples: same / both error | Confirmed |
| --- | --- | --- | --- | --- |
| `compile_jmespath_expression` | `jmespath.compile` | 0 | 3 / 2 | yes |
| `purge_jmespath_cache` | `jmespath.parser.Parser.purge` | 0 | 2 / 0 | yes |
| `tokenize_jmespath_expression` | `jmespath.lexer.Lexer.tokenize` | 0 | 6 / 0 | yes |
| `define_jmespath_function_signature` | `jmespath.functions.signature` | 3 | 0 / 0 | no: unstable |
| `set_incomplete_expression_error` | `jmespath.exceptions.IncompleteExpressionError.set_expression` | 3 | 4 / 0 | yes |
| `create_field_ast_node` | `jmespath.ast.field` | 0 | 5 / 0 | yes |
| `create_literal_ast_node` | `jmespath.ast.literal` | 3 | 6 / 0 | yes |
| `create_function_expression_ast_node` | `jmespath.ast.function_expression` | 0 | 5 / 0 | yes |
| `create_projection_ast_node` | `jmespath.ast.projection` | 0 | 4 / 0 | yes |
| `create_value_projection_ast_node` | `jmespath.ast.value_projection` | 0 | 5 / 0 | yes |
| `create_filter_projection_ast_node` | `jmespath.ast.filter_projection` | 0 | 4 / 0 | yes |
| `create_multi_select_list_ast_node` | `jmespath.ast.multi_select_list` | 0 | 5 / 0 | yes |
| `create_multi_select_dict_ast_node` | `jmespath.ast.multi_select_dict` | 1 | 4 / 0 | yes |
| `create_and_expression_ast_node` | `jmespath.ast.and_expression` | 0 | 5 / 0 | yes |
| `create_or_expression_ast_node` | `jmespath.ast.or_expression` | 0 | 5 / 0 | yes |
| `create_not_expression_ast_node` | `jmespath.ast.not_expression` | 0 | 5 / 0 | yes |
| `create_pipe_ast_node` | `jmespath.ast.pipe` | 0 | 4 / 0 | yes |
| `create_comparator_ast_node` | `jmespath.ast.comparator` | 0 | 5 / 0 | yes |
| `create_slice_ast_node` | `jmespath.ast.slice` | 1 | 5 / 0 | yes |
| `create_flatten_ast_node` | `jmespath.ast.flatten` | 0 | 4 / 0 | yes |
| `create_identity_ast_node` | `jmespath.ast.identity` | 0 | 2 / 0 | yes |
| `create_current_node_ast_node` | `jmespath.ast.current_node` | 2 | 2 / 0 | yes |
| `create_expression_reference_ast_node` | `jmespath.ast.expref` | 0 | 5 / 0 | yes |
| `create_subexpression_ast_node` | `jmespath.ast.subexpression` | 1 | 5 / 0 | yes |
| `create_index_expression_ast_node` | `jmespath.ast.index_expression` | 1 | 4 / 0 | yes |
| `create_key_value_pair_ast_node` | `jmespath.ast.key_val_pair` | 0 | 5 / 0 | yes |

## Rejected tools

| Tool | Wraps | Last failed check | Error |
| --- | --- | --- | --- |
| `search_with_jmespath` | `jmespath.search` | runs | Input {"data": {"age": 30, "name": "John"}, "expression": "name"}: the tool raised output is not JSON: John, but the direct library call returned "John" Input {"data": {"people": [{"name": "John"}, {"name": "Jane"}]}, "e |
| `parse_jmespath_expression` | `jmespath.parser.Parser.parse` | static | do not use __dict__ |
| `default_jmespath_visit` | `jmespath.visitor.TreeInterpreter.default_visit` | spec | the direct_call expression is wrong: AttributeError: 'dict' object has no attribute 'dict_cls' |
| `call_jmespath_function` | `jmespath.functions.Functions.call_function` | runs | Input {"function_name": "join", "resolved_args": [",", ["a", "b", "c"]]}: the tool raised output is not JSON: a,b,c, but the direct library call returned "a,b,c" |
| `create_index_ast_node` | `jmespath.ast.index` | static | do not use __name__ |

## Use

```sh
uv run repo2tools run-model <exercises> --mode tools --base-url <url> --model <model> -- toolsets/generated/jmespath.py-sample/run_server.sh
```
