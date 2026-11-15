# repo2tools report: python-sdk-bench2

- Repo: https://github.com/modelcontextprotocol/python-sdk at `77001c96f9507be0f4d009b83210a384a5e08bda`
- Package: `mcp`, 513 public callables
- Model: `qwen3-coder`, thinking off, temperature 0
- Sandbox: macOS sandbox-exec: no network, home folder unreadable, one scratch folder writable
- Time: 2.5 min. LLM tokens: 480,856 in 274 requests (propose 28,375, spec 65,449, code 387,032)

## Result

| | Tools |
| --- | --- |
| Picked by the LLM | 54 (dropped: 0, for unknown functions, duplicates or bad names) |
| Accepted | 0 |
| Accepted and confirmed against a direct library call | 0 |
| Passed all checks on the first try | 0 |
| Rejected after the repair rounds | 54 |

First try, by the first check that failed: loads: 40, static: 9, spec: 5.

**Limit of these checks:** the same model wrote the tool and the direct call it is compared with, so they can share a misunderstanding of the library. The checks catch wrapper bugs (wrong field, wrong conversion, crashes), not a wrong idea of what the library does. A real score needs exercises with known answers.

## Accepted tools

| Tool | Wraps | Repairs | Samples: same / both error | Confirmed |
| --- | --- | --- | --- | --- |

## Rejected tools

| Tool | Wraps | Last failed check | Error |
| --- | --- | --- | --- |
| `create_client` | `mcp.Client` | loads | ModuleNotFoundError: No module named 'mcp_types' |
| `initialize_client_session` | `mcp.ClientSession.initialize` | loads | the check process died: Traceback (most recent call last): File "/Users/qobiljonmuhammadov/Notes S2026/agentic-llms/code/repo2tools/src/repo2tools/synthesis/worker.py", line 353, in <module> main() File "/Users/qobiljonm |
| `discover_server_capabilities` | `mcp.ClientSession.discover` | loads | the check process died: Traceback (most recent call last): File "/Users/qobiljonmuhammadov/Notes S2026/agentic-llms/code/repo2tools/src/repo2tools/synthesis/worker.py", line 353, in <module> main() File "/Users/qobiljonm |
| `list_available_tools` | `mcp.ClientSession.list_tools` | loads | the check process died: Traceback (most recent call last): File "/Users/qobiljonmuhammadov/Notes S2026/agentic-llms/code/repo2tools/src/repo2tools/synthesis/worker.py", line 353, in <module> main() File "/Users/qobiljonm |
| `execute_tool` | `mcp.ClientSession.call_tool` | static | do not use __dict__ |
| `list_available_resources` | `mcp.ClientSession.list_resources` | loads | the check process died: Traceback (most recent call last): File "/Users/qobiljonmuhammadov/Notes S2026/agentic-llms/code/repo2tools/src/repo2tools/synthesis/worker.py", line 353, in <module> main() File "/Users/qobiljonm |
| `read_resource_content` | `mcp.ClientSession.read_resource` | loads | ModuleNotFoundError: No module named 'mcp_types' |
| `list_available_prompts` | `mcp.ClientSession.list_prompts` | loads | the check process died: Traceback (most recent call last): File "/Users/qobiljonmuhammadov/Notes S2026/agentic-llms/code/repo2tools/src/repo2tools/synthesis/worker.py", line 353, in <module> main() File "/Users/qobiljonm |
| `retrieve_prompt` | `mcp.ClientSession.get_prompt` | loads | the check process died: Traceback (most recent call last): File "/Users/qobiljonmuhammadov/Notes S2026/agentic-llms/code/repo2tools/src/repo2tools/synthesis/worker.py", line 353, in <module> main() File "/Users/qobiljonm |
| `get_completions` | `mcp.ClientSession.complete` | loads | the check process died: Traceback (most recent call last): File "/Users/qobiljonmuhammadov/Notes S2026/agentic-llms/code/repo2tools/src/repo2tools/synthesis/worker.py", line 353, in <module> main() File "/Users/qobiljonm |
| `send_ping_request` | `mcp.ClientSession.send_ping` | loads | the check process died: Traceback (most recent call last): File "/Users/qobiljonmuhammadov/Notes S2026/agentic-llms/code/repo2tools/src/repo2tools/synthesis/worker.py", line 353, in <module> main() File "/Users/qobiljonm |
| `set_server_logging_level` | `mcp.ClientSession.set_logging_level` | loads | the check process died: Traceback (most recent call last): File "/Users/qobiljonmuhammadov/Notes S2026/agentic-llms/code/repo2tools/src/repo2tools/synthesis/worker.py", line 353, in <module> main() File "/Users/qobiljonm |
| `connect_to_mcp_server` | `mcp.ClientSessionGroup.connect_to_server` | static | line 5: no code at module level except imports, definitions and constants |
| `execute_tool_across_servers` | `mcp.ClientSessionGroup.call_tool` | loads | the check process died: Traceback (most recent call last): File "/Users/qobiljonmuhammadov/Notes S2026/agentic-llms/code/repo2tools/src/repo2tools/synthesis/worker.py", line 353, in <module> main() File "/Users/qobiljonm |
| `convert_jsonrpc_error` | `mcp.MCPError.from_jsonrpc_error` | loads | the check process died: Traceback (most recent call last): File "/Users/qobiljonmuhammadov/Notes S2026/agentic-llms/code/repo2tools/src/repo2tools/synthesis/worker.py", line 353, in <module> main() File "/Users/qobiljonm |
| `send_server_request` | `mcp.ServerSession.send_request` | loads | the check process died: Traceback (most recent call last): File "/Users/qobiljonmuhammadov/Notes S2026/agentic-llms/code/repo2tools/src/repo2tools/synthesis/worker.py", line 353, in <module> main() File "/Users/qobiljonm |
| `send_server_notification` | `mcp.ServerSession.send_notification` | loads | the check process died: Traceback (most recent call last): File "/Users/qobiljonmuhammadov/Notes S2026/agentic-llms/code/repo2tools/src/repo2tools/synthesis/worker.py", line 353, in <module> main() File "/Users/qobiljonm |
| `create_chat_message` | `mcp.ServerSession.create_message` | loads | the check process died: Traceback (most recent call last): File "/Users/qobiljonmuhammadov/Notes S2026/agentic-llms/code/repo2tools/src/repo2tools/synthesis/worker.py", line 353, in <module> main() File "/Users/qobiljonm |
| `list_root_directories` | `mcp.ServerSession.list_roots` | static | do not use __import__ |
| `request_user_input` | `mcp.ServerSession.elicit` | loads | the check process died: Traceback (most recent call last): File "/Users/qobiljonmuhammadov/Notes S2026/agentic-llms/code/repo2tools/src/repo2tools/synthesis/worker.py", line 353, in <module> main() File "/Users/qobiljonm |
| `ping_server` | `mcp.ServerSession.send_ping` | loads | the check process died: Traceback (most recent call last): File "/Users/qobiljonmuhammadov/Notes S2026/agentic-llms/code/repo2tools/src/repo2tools/synthesis/worker.py", line 353, in <module> main() File "/Users/qobiljonm |
| `report_task_progress` | `mcp.ServerSession.report_progress` | loads | the check process died: Traceback (most recent call last): File "/Users/qobiljonmuhammadov/Notes S2026/agentic-llms/code/repo2tools/src/repo2tools/synthesis/worker.py", line 353, in <module> main() File "/Users/qobiljonm |
| `start_mcp_server` | `mcp.server.MCPServer.run` | loads | the check process died: Traceback (most recent call last): File "/Users/qobiljonmuhammadov/Notes S2026/agentic-llms/code/repo2tools/src/repo2tools/synthesis/worker.py", line 353, in <module> main() File "/Users/qobiljonm |
| `register_new_tool` | `mcp.server.MCPServer.add_tool` | loads | the check process died: Traceback (most recent call last): File "/Users/qobiljonmuhammadov/Notes S2026/agentic-llms/code/repo2tools/src/repo2tools/synthesis/worker.py", line 353, in <module> main() File "/Users/qobiljonm |
| `unregister_tool` | `mcp.server.MCPServer.remove_tool` | loads | the check process died: Traceback (most recent call last): File "/Users/qobiljonmuhammadov/Notes S2026/agentic-llms/code/repo2tools/src/repo2tools/synthesis/worker.py", line 353, in <module> main() File "/Users/qobiljonm |
| `stream_within_origin` | `mcp.client.streamable_http.stream_within_origin` | static | line 5: no code at module level except imports, definitions and constants |
| `listen_subscriptions` | `mcp.client.subscriptions.listen` | loads | the check process died: Traceback (most recent call last): File "/Users/qobiljonmuhammadov/Notes S2026/agentic-llms/code/repo2tools/src/repo2tools/synthesis/worker.py", line 353, in <module> main() File "/Users/qobiljonm |
| `elicit_information` | `mcp.server.apps.Context.elicit` | loads | the check process died: Traceback (most recent call last): File "/Users/qobiljonmuhammadov/Notes S2026/agentic-llms/code/repo2tools/src/repo2tools/synthesis/worker.py", line 353, in <module> main() File "/Users/qobiljonm |
| `elicit_url` | `mcp.server.apps.Context.elicit_url` | loads | the check process died: Traceback (most recent call last): File "/Users/qobiljonmuhammadov/Notes S2026/agentic-llms/code/repo2tools/src/repo2tools/synthesis/worker.py", line 353, in <module> main() File "/Users/qobiljonm |
| `read_resource` | `mcp.server.apps.Context.read_resource` | loads | the check process died: Traceback (most recent call last): File "/Users/qobiljonmuhammadov/Notes S2026/agentic-llms/code/repo2tools/src/repo2tools/synthesis/worker.py", line 353, in <module> main() File "/Users/qobiljonm |
| `notify_tools_changed` | `mcp.server.apps.Context.notify_tools_changed` | loads | the check process died: Traceback (most recent call last): File "/Users/qobiljonmuhammadov/Notes S2026/agentic-llms/code/repo2tools/src/repo2tools/synthesis/worker.py", line 353, in <module> main() File "/Users/qobiljonm |
| `notify_prompts_changed` | `mcp.server.apps.Context.notify_prompts_changed` | loads | the check process died: Traceback (most recent call last): File "/Users/qobiljonmuhammadov/Notes S2026/agentic-llms/code/repo2tools/src/repo2tools/synthesis/worker.py", line 353, in <module> main() File "/Users/qobiljonm |
| `notify_resources_changed` | `mcp.server.apps.Context.notify_resources_changed` | loads | the check process died: Traceback (most recent call last): File "/Users/qobiljonmuhammadov/Notes S2026/agentic-llms/code/repo2tools/src/repo2tools/synthesis/worker.py", line 353, in <module> main() File "/Users/qobiljonm |
| `notify_resource_updated` | `mcp.server.apps.Context.notify_resource_updated` | loads | the check process died: Traceback (most recent call last): File "/Users/qobiljonmuhammadov/Notes S2026/agentic-llms/code/repo2tools/src/repo2tools/synthesis/worker.py", line 353, in <module> main() File "/Users/qobiljonm |
| `send_notification` | `mcp.server.connection.Connection.notify` | static | do not use __name__ |
| `log_message` | `mcp.server.context.Context.log` | loads | the check process died: Traceback (most recent call last): File "/Users/qobiljonmuhammadov/Notes S2026/agentic-llms/code/repo2tools/src/repo2tools/synthesis/worker.py", line 353, in <module> main() File "/Users/qobiljonm |
| `elicit_validated_input` | `mcp.server.elicitation.elicit_with_validation` | loads | the check process died: Traceback (most recent call last): File "/Users/qobiljonmuhammadov/Notes S2026/agentic-llms/code/repo2tools/src/repo2tools/synthesis/worker.py", line 353, in <module> main() File "/Users/qobiljonm |
| `elicit_url_mode` | `mcp.server.elicitation.elicit_url` | loads | the check process died: Traceback (most recent call last): File "/Users/qobiljonmuhammadov/Notes S2026/agentic-llms/code/repo2tools/src/repo2tools/synthesis/worker.py", line 353, in <module> main() File "/Users/qobiljonm |
| `require_client_extension` | `mcp.server.mcpserver.require_client_extension` | loads | ModuleNotFoundError: No module named 'mcp_types' |
| `classify_inbound_request` | `mcp.shared.inbound.classify_inbound_request` | loads | ModuleNotFoundError: No module named 'mcp_types' |
| `validate_mcp_param_headers` | `mcp.shared.inbound.validate_mcp_param_headers` | loads | the check process died: Traceback (most recent call last): File "/Users/qobiljonmuhammadov/Notes S2026/agentic-llms/code/repo2tools/src/repo2tools/synthesis/worker.py", line 353, in <module> main() File "/Users/qobiljonm |
| `validate_tool_name` | `mcp.shared.tool_name_validation.validate_tool_name` | static | line 6: no code at module level except imports, definitions and constants |
| `validate_and_warn_tool_name` | `mcp.shared.tool_name_validation.validate_and_warn_tool_name` | loads | the check process died: Traceback (most recent call last): File "/Users/qobiljonmuhammadov/Notes S2026/agentic-llms/code/repo2tools/src/repo2tools/synthesis/worker.py", line 353, in <module> main() File "/Users/qobiljonm |
| `add_tool` | `mcp.server.mcpserver.server.ToolManager.add_tool` | loads | ModuleNotFoundError: No module named 'mcp_types' |
| `call_tool` | `mcp.server.mcpserver.server.ToolManager.call_tool` | loads | the check process died: Traceback (most recent call last): File "/Users/qobiljonmuhammadov/Notes S2026/agentic-llms/code/repo2tools/src/repo2tools/synthesis/worker.py", line 353, in <module> main() File "/Users/qobiljonm |
| `add_resource` | `mcp.server.mcpserver.resources.ResourceManager.add_resource` | loads | the check process died: Traceback (most recent call last): File "/Users/qobiljonmuhammadov/Notes S2026/agentic-llms/code/repo2tools/src/repo2tools/synthesis/worker.py", line 353, in <module> main() File "/Users/qobiljonm |
| `get_resource` | `mcp.server.mcpserver.resources.ResourceManager.get_resource` | loads | the check process died: Traceback (most recent call last): File "/Users/qobiljonmuhammadov/Notes S2026/agentic-llms/code/repo2tools/src/repo2tools/synthesis/worker.py", line 353, in <module> main() File "/Users/qobiljonm |
| `add_prompt` | `mcp.server.mcpserver.prompts.PromptManager.add_prompt` | loads | the check process died: Traceback (most recent call last): File "/Users/qobiljonmuhammadov/Notes S2026/agentic-llms/code/repo2tools/src/repo2tools/synthesis/worker.py", line 353, in <module> main() File "/Users/qobiljonm |
| `render_prompt` | `mcp.server.mcpserver.prompts.PromptManager.render_prompt` | loads | the check process died: Traceback (most recent call last): File "/Users/qobiljonmuhammadov/Notes S2026/agentic-llms/code/repo2tools/src/repo2tools/synthesis/worker.py", line 353, in <module> main() File "/Users/qobiljonm |
| `list_tools` | `mcp.server.mcpserver.server.ToolManager.list_tools` | loads | the check process died: Traceback (most recent call last): File "/Users/qobiljonmuhammadov/Notes S2026/agentic-llms/code/repo2tools/src/repo2tools/synthesis/worker.py", line 353, in <module> main() File "/Users/qobiljonm |
| `list_resources` | `mcp.server.mcpserver.resources.ResourceManager.list_resources` | loads | the check process died: Traceback (most recent call last): File "/Users/qobiljonmuhammadov/Notes S2026/agentic-llms/code/repo2tools/src/repo2tools/synthesis/worker.py", line 353, in <module> main() File "/Users/qobiljonm |
| `list_prompts` | `mcp.server.mcpserver.prompts.PromptManager.list_prompts` | loads | the check process died: Traceback (most recent call last): File "/Users/qobiljonmuhammadov/Notes S2026/agentic-llms/code/repo2tools/src/repo2tools/synthesis/worker.py", line 353, in <module> main() File "/Users/qobiljonm |
| `handler_exception_to_error_data` | `mcp.shared.jsonrpc_dispatcher.handler_exception_to_error_data` | static | do not use __name__ |
| `configure_logging` | `mcp.server.mcpserver.server.configure_logging` | loads | the check process died: Traceback (most recent call last): File "/Users/qobiljonmuhammadov/Notes S2026/agentic-llms/code/repo2tools/src/repo2tools/synthesis/worker.py", line 353, in <module> main() File "/Users/qobiljonm |

## Use

```sh
uv run repo2tools run-model <exercises> --mode tools --base-url <url> --model <model> -- toolsets/generated/python-sdk-bench2/run_server.sh
```
