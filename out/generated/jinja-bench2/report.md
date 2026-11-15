# repo2tools report: jinja-bench2

- Repo: https://github.com/pallets/jinja at `5ef70112a1ff19c05324ff889dd30405b1002044`
- Package: `jinja2`, 489 public callables
- Model: `qwen3-coder`, thinking off, temperature 0
- Sandbox: macOS sandbox-exec: no network, home folder unreadable, one scratch folder writable
- Time: 3.3 min. LLM tokens: 439,360 in 270 requests (propose 24,578, spec 239,397, code 175,385)

## Result

| | Tools |
| --- | --- |
| Picked by the LLM | 58 (dropped: 0, for unknown functions, duplicates or bad names) |
| Accepted | 11 |
| Accepted and confirmed against a direct library call | 7 |
| Passed all checks on the first try | 8 |
| Rejected after the repair rounds | 47 |

First try, by the first check that failed: spec: 31, static: 13, ok: 8, fastmcp: 4, differential: 1, loads: 1.

**Limit of these checks:** the same model wrote the tool and the direct call it is compared with, so they can share a misunderstanding of the library. The checks catch wrapper bugs (wrong field, wrong conversion, crashes), not a wrong idea of what the library does. A real score needs exercises with known answers.

## Accepted tools

| Tool | Wraps | Repairs | Samples: same / both error | Confirmed |
| --- | --- | --- | --- | --- |
| `create_environment` | `jinja2.Environment` | 1 | 0 / 0 | no: unstable |
| `create_template` | `jinja2.Template` | 0 | 0 / 0 | no: unstable |
| `render_template` | `jinja2.Template.render` | 0 | 5 / 0 | yes |
| `tokenize_template` | `jinja2.Environment.lex` | 1 | 5 / 0 | yes |
| `create_dict_loader` | `jinja2.DictLoader` | 0 | 0 / 0 | no: unstable |
| `create_overlay_environment` | `jinja2.Environment.overlay` | 0 | 0 / 0 | no: unstable |
| `clear_jinja_caches` | `jinja2.clear_caches` | 0 | 1 / 0 | yes |
| `iterate_tokens` | `jinja2.environment.Lexer.tokeniter` | 3 | 5 / 0 | yes |
| `join_markup` | `jinja2.runtime.markup_join` | 0 | 6 / 0 | yes |
| `join_strings` | `jinja2.runtime.str_join` | 0 | 6 / 0 | yes |
| `describe_token_expression` | `jinja2.lexer.describe_token_expr` | 0 | 6 / 0 | yes |

## Rejected tools

| Tool | Wraps | Last failed check | Error |
| --- | --- | --- | --- |
| `load_template` | `jinja2.Environment.get_template` | static | do not use globals |
| `parse_template_string` | `jinja2.Environment.from_string` | static | do not use globals |
| `parse_template_source` | `jinja2.Environment.parse` | static | do not use __name__ |
| `compile_template` | `jinja2.Environment.compile` | differential | Input {"filename": "test.html", "name": "test_template", "raw": false, "source": "Hello {{ name }}!"}: the tool raised ValidationError: 2 validation errors for compile_templateOutput result.str Input should be a valid st |
| `list_available_templates` | `jinja2.Environment.list_templates` | spec | the direct_call expression is wrong: AttributeError: 'str' object has no attribute 'list_templates' |
| `create_filesystem_loader` | `jinja2.FileSystemLoader` | static | do not import sys |
| `select_template_from_list` | `jinja2.Environment.select_template` | differential | Input {"names": ["template1.html", "template2.html"], "parent": null}: the tool raised ValueError: None of the provided templates could be found: ['template1.html', 'template2.html'], but the direct library call returned |
| `get_or_select_template` | `jinja2.Environment.get_or_select_template` | static | do not use globals |
| `add_jinja_extension` | `jinja2.Environment.add_extension` | spec | the direct_call expression is wrong: AttributeError: 'str' object has no attribute 'add_extension' |
| `generate_python_source` | `jinja2.compiler.generate` | spec | the direct call failed on every sample, so nothing can be compared. Errors: ["TypeError: Can't compile non template nodes"]. Use samples that are valid for the library. |
| `get_template_lexer` | `jinja2.environment.get_lexer` | spec | the direct_call expression is wrong: AttributeError: 'dict' object has no attribute 'block_start_string' |
| `visit_template_node` | `jinja2.compiler.CodeGenerator.visit_Template` | spec | the direct_call expression is wrong: ModuleNotFoundError: No module named 'node' |
| `visit_output_node` | `jinja2.compiler.CodeGenerator.visit_Output` | spec | the direct_call expression is wrong: AttributeError: 'dict' object has no attribute 'require_output_check' |
| `visit_name_node` | `jinja2.compiler.CodeGenerator.visit_Name` | fastmcp | PydanticInvalidForJsonSchema: Cannot generate a JsonSchema for core_schema.IsInstanceSchema (<class 'jinja2.nodes.Name'>) For further information visit https://errors.pydantic.dev/2.14/u/invalid-for-json-schema |
| `visit_constant_node` | `jinja2.compiler.CodeGenerator.visit_Const` | spec | this parameter needs a snake_case name and a JSON type: {"name": "const_value", "type": "any", "description": "The constant value to generate Python code for", "required": true} |
| `visit_attribute_access` | `jinja2.compiler.CodeGenerator.visit_Getattr` | spec | the direct call failed on every sample, so nothing can be compared. Errors: ["TypeError: 'Getattr' takes 0 or 3 arguments"]. Use samples that are valid for the library. |
| `visit_function_call` | `jinja2.compiler.CodeGenerator.visit_Call` | spec | the direct call failed on every sample, so nothing can be compared. Errors: ['TypeError: CodeGenerator.visit_Call() takes 3 positional arguments but 4 were given']. Use samples that are valid for the library. |
| `visit_filter_expression` | `jinja2.compiler.CodeGenerator.visit_Filter` | spec | the direct_call expression is wrong: AttributeError: 'dict' object has no attribute 'eval_ctx' |
| `visit_test_expression` | `jinja2.compiler.CodeGenerator.visit_Test` | spec | the direct_call expression is wrong: AttributeError: 'dict' object has no attribute 'eval_ctx' |
| `visit_if_statement` | `jinja2.compiler.CodeGenerator.visit_If` | spec | the reply must be a JSON object with parameters, direct_call and samples |
| `visit_for_loop` | `jinja2.compiler.CodeGenerator.visit_For` | spec | the reply must be a JSON object with parameters, direct_call and samples |
| `visit_assignment` | `jinja2.compiler.CodeGenerator.visit_Assign` | spec | the reply must be a JSON object with parameters, direct_call and samples |
| `find_undeclared_variables` | `jinja2.compiler.find_undeclared` | spec | the direct_call expression is wrong: AttributeError: 'dict' object has no attribute 'iter_child_nodes' |
| `parse_template` | `jinja2.environment.Parser.parse` | spec | the direct_call expression is wrong: AttributeError: 'dict' object has no attribute '_tokenize' |
| `parse_expression` | `jinja2.environment.Parser.parse_expression` | static | do not use __name__ |
| `parse_statement` | `jinja2.environment.Parser.parse_statement` | spec | the direct_call expression is wrong: AttributeError: 'dict' object has no attribute '_tokenize' |
| `parse_statements` | `jinja2.environment.Parser.parse_statements` | static | do not use __import__ |
| `parse_assign_target` | `jinja2.environment.Parser.parse_assign_target` | spec | the direct call failed on every sample, so nothing can be compared. Errors: ["TemplateSyntaxError: expected token 'name', got 'begin of statement block'\n line 1", "TemplateSyntaxError: unexpected 'begin of statement blo |
| `parse_for_loop` | `jinja2.environment.Parser.parse_for` | spec | the direct_call expression is wrong: AttributeError: 'str' object has no attribute '_tokenize' |
| `parse_if_construct` | `jinja2.environment.Parser.parse_if` | spec | the direct_call expression is wrong: AttributeError: 'dict' object has no attribute '_tokenize' |
| `parse_set_statement` | `jinja2.environment.Parser.parse_set` | fastmcp | PydanticInvalidForJsonSchema: Cannot generate a JsonSchema for core_schema.IsInstanceSchema (<class 'jinja2.environment.Environment'>) For further information visit https://errors.pydantic.dev/2.14/u/invalid-for-json-sch |
| `parse_macro` | `jinja2.environment.Parser.parse_macro` | spec | the direct_call expression is wrong: AttributeError: 'dict' object has no attribute '_tokenize' |
| `parse_import` | `jinja2.environment.Parser.parse_import` | spec | the direct_call expression is wrong: AttributeError: 'dict' object has no attribute '_tokenize' |
| `parse_from_import` | `jinja2.environment.Parser.parse_from` | spec | the direct call failed on every sample, so nothing can be compared. Errors: ['TemplateSyntaxError: unexpected \'end of template\'\n File "another.j2", line 1', 'TemplateSyntaxError: unexpected \'end of template\'\n File  |
| `parse_include` | `jinja2.environment.Parser.parse_include` | spec | the direct_call expression is wrong: AttributeError: 'str' object has no attribute '_tokenize' |
| `parse_extends` | `jinja2.environment.Parser.parse_extends` | spec | the direct_call expression is wrong: AttributeError: 'dict' object has no attribute '_tokenize' |
| `parse_filter` | `jinja2.environment.Parser.parse_filter` | spec | the direct_call expression is wrong: AttributeError: 'dict' object has no attribute '_tokenize' |
| `parse_test` | `jinja2.environment.Parser.parse_test` | static | do not use __name__ |
| `format_string` | `jinja2.filters.do_format` | differential | Input {"args": ["World"], "format_string": "Hello, %s!", "kwargs": {}}: the direct library call raised TypeError: not all arguments converted during string formatting, but the tool returned "Hello, World!" Input {"args": |
| `filter_by_attribute` | `jinja2.filters.do_selectattr` | spec | the direct_call expression is wrong: ModuleNotFoundError: No module named 'type' |
| `reject_by_attribute` | `jinja2.filters.do_rejectattr` | spec | the direct_call expression is wrong: ModuleNotFoundError: No module named 'type' |
| `serialize_to_json` | `jinja2.filters.do_tojson` | spec | the direct_call expression is wrong: ModuleNotFoundError: No module named 'eval_ctx_mock' |
| `find_referenced_templates` | `jinja2.meta.find_referenced_templates` | spec | the direct_call expression is wrong: AttributeError: 'dict' object has no attribute 'find_all' |
| `find_node_by_type` | `jinja2.nodes.Node.find` | spec | direct_call must use every tool parameter; it does not use: node_type |
| `find_all_nodes_by_type` | `jinja2.nodes.Node.find_all` | static | do not use __import__ |
| `optimize_ast` | `jinja2.optimizer.optimize` | spec | the direct_call expression is wrong: AttributeError: 'dict' object has no attribute 'iter_fields' |
| `describe_token` | `jinja2.lexer.describe_token` | spec | the direct call failed on every sample, so nothing can be compared. Errors: ["TypeError: Token.__new__() missing 1 required positional argument: 'value'"]. Use samples that are valid for the library. |

## Use

```sh
uv run repo2tools run-model <exercises> --mode tools --base-url <url> --model <model> -- toolsets/generated/jinja-bench2/run_server.sh
```
