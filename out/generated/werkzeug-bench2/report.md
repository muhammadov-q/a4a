# repo2tools report: werkzeug-bench2

- Repo: https://github.com/pallets/werkzeug at `0f43c6ebd426039e4b99ec22535c2c8a2ec2f69f`
- Package: `werkzeug`, 436 public callables
- Model: `qwen3-coder`, thinking off, temperature 0
- Sandbox: macOS sandbox-exec: no network, home folder unreadable, one scratch folder writable
- Time: 2.3 min. LLM tokens: 376,939 in 245 requests (propose 22,619, spec 148,171, code 206,149)

## Result

| | Tools |
| --- | --- |
| Picked by the LLM | 60 (dropped: 0, for unknown functions, duplicates or bad names) |
| Accepted | 26 |
| Accepted and confirmed against a direct library call | 25 |
| Passed all checks on the first try | 16 |
| Rejected after the repair rounds | 34 |

First try, by the first check that failed: spec: 18, ok: 16, differential: 14, static: 8, fastmcp: 4.

**Limit of these checks:** the same model wrote the tool and the direct call it is compared with, so they can share a misunderstanding of the library. The checks catch wrapper bugs (wrong field, wrong conversion, crashes), not a wrong idea of what the library does. A real score needs exercises with known answers.

## Accepted tools

| Tool | Wraps | Repairs | Samples: same / both error | Confirmed |
| --- | --- | --- | --- | --- |
| `create_client` | `werkzeug.Client` | 0 | 4 / 0 | yes |
| `create_response` | `werkzeug.Response` | 2 | 6 / 0 | yes |
| `response_text` | `werkzeug.Response.text` | 0 | 5 / 0 | yes |
| `create_headers` | `werkzeug.datastructures.Headers` | 2 | 5 / 0 | yes |
| `parse_accept_header` | `werkzeug.datastructures.Accept.from_header` | 1 | 6 / 0 | yes |
| `parse_authorization_header` | `werkzeug.datastructures.Authorization.from_header` | 0 | 5 / 0 | yes |
| `parse_www_authenticate` | `werkzeug.datastructures.WWWAuthenticate.from_header` | 0 | 6 / 0 | yes |
| `format_www_authenticate` | `werkzeug.datastructures.WWWAuthenticate.to_header` | 0 | 5 / 0 | yes |
| `parse_content_security_policy` | `werkzeug.datastructures.ContentSecurityPolicy.from_header` | 1 | 6 / 0 | yes |
| `parse_etag` | `werkzeug.datastructures.ETag.from_header` | 2 | 6 / 0 | yes |
| `format_etag` | `werkzeug.datastructures.ETag.to_header` | 1 | 5 / 0 | yes |
| `get_header_value` | `werkzeug.datastructures.Headers.get` | 2 | 5 / 0 | yes |
| `get_header_list` | `werkzeug.datastructures.Headers.getlist` | 3 | 5 / 0 | yes |
| `clear_headers` | `werkzeug.datastructures.Headers.clear` | 2 | 4 / 0 | yes |
| `parse_content_range` | `werkzeug.datastructures.ContentRange.from_header` | 0 | 6 / 0 | yes |
| `format_content_range` | `werkzeug.datastructures.ContentRange.to_header` | 0 | 6 / 0 | yes |
| `parse_options_header` | `werkzeug.formparser.parse_options_header` | 0 | 5 / 0 | yes |
| `unquote_header_value` | `werkzeug.http.unquote_header_value` | 0 | 6 / 0 | yes |
| `parse_dict_header` | `werkzeug.http.parse_dict_header` | 0 | 5 / 0 | yes |
| `bind_map` | `werkzeug.routing.Map.bind` | 0 | 0 / 1 | no: unstable, both_error |
| `check_password_hash` | `werkzeug.security.check_password_hash` | 0 | 5 / 0 | yes |
| `iri_to_uri` | `werkzeug.urls.iri_to_uri` | 0 | 5 / 0 | yes |
| `generate_debug_representation` | `werkzeug.debug.repr.DebugReprGenerator.repr` | 0 | 5 / 0 | yes |
| `parse_http_cookies` | `werkzeug.sansio.http.parse_cookie` | 2 | 5 / 0 | yes |
| `set_http_cookie` | `werkzeug.sansio.response.Response.set_cookie` | 1 | 5 / 0 | yes |
| `delete_http_cookie` | `werkzeug.sansio.response.Response.delete_cookie` | 0 | 6 / 0 | yes |

## Rejected tools

| Tool | Wraps | Last failed check | Error |
| --- | --- | --- | --- |
| `client_open` | `werkzeug.Client.open` | spec | the direct call failed on every sample, so nothing can be compared. Errors: ["TypeError: 'str' object is not callable"]. Use samples that are valid for the library. |
| `client_get` | `werkzeug.Client.get` | spec | the direct call failed on every sample, so nothing can be compared. Errors: ["TypeError: 'str' object is not callable"]. Use samples that are valid for the library. |
| `client_post` | `werkzeug.Client.post` | spec | the direct call failed on every sample, so nothing can be compared. Errors: ["TypeError: 'str' object is not callable"]. Use samples that are valid for the library. |
| `client_put` | `werkzeug.Client.put` | spec | the direct call failed on every sample, so nothing can be compared. Errors: ["TypeError: 'str' object is not callable"]. Use samples that are valid for the library. |
| `client_delete` | `werkzeug.Client.delete` | spec | the direct call failed on every sample, so nothing can be compared. Errors: ["TypeError: 'str' object is not callable"]. Use samples that are valid for the library. |
| `create_request` | `werkzeug.Request.from_values` | differential | Input {"data": {}, "headers": {}, "method": "GET", "path": "/api/users"}: the tool returned {"data": null, "headers": {"Host": "localhost"}, "method": "GET", "path": "/api/users"}, but the direct library call returned "< |
| `request_form_data` | `werkzeug.Request.form` | spec | the reply must be a JSON object with parameters, direct_call and samples |
| `request_files` | `werkzeug.Request.files` | spec | the reply must be a JSON object with parameters, direct_call and samples |
| `request_json` | `werkzeug.Request.json` | spec | the reply must be a JSON object with parameters, direct_call and samples |
| `response_data` | `werkzeug.Response.data` | spec | the reply must be a JSON object with parameters, direct_call and samples |
| `response_json` | `werkzeug.Response.json` | runs | Input {"response": "null", "status": 200}: the tool raised output is not JSON: , but the direct library call returned null |
| `create_multidict` | `werkzeug.datastructures.MultiDict` | differential | Input {"mapping": [["a", "b"], ["a", "c"]]}: the tool returned {"a": ["b", "c"]}, but the direct library call returned {"a": "b"} Input {"mapping": {"x": "y", "z": ["p", "q"]}}: the tool returned {"x": ["y"], "z": ["p",  |
| `format_content_security_policy` | `werkzeug.datastructures.ContentSecurityPolicy.to_header` | differential | Input {"policy": {"default-src": "'self'", "script-src": "'self' https://example.com", "style-src": "'self' 'unsafe-inline'"}}: the direct library call raised TypeError: CallbackDict.__init__() got an unexpected keyword  |
| `parse_etag_set` | `werkzeug.datastructures.ETagSet.from_header` | differential | Input {"value": "\"tag1\", \"tag2\""}: the tool returned {"star_tag": false, "strong": [], "weak": []}, but the direct library call returned "\"tag1\", \"tag2\"" Input {"value": "*"}: the tool returned {"star_tag": false |
| `format_etag_set` | `werkzeug.datastructures.ETagSet.to_header` | end_to_end | over MCP it returned "W/\"wtag2\", W/\"wtag1\"", in the check "W/\"wtag1\", W/\"wtag2\"" |
| `set_header_value` | `werkzeug.datastructures.Headers.set` | spec | the direct_call expression is wrong: AttributeError: 'dict' object has no attribute 'set' |
| `set_header_list` | `werkzeug.datastructures.Headers.setlist` | spec | the direct_call expression is wrong: AttributeError: 'dict' object has no attribute 'setlist' |
| `add_header_value` | `werkzeug.datastructures.Headers.add` | spec | the direct_call expression is wrong: AttributeError: 'str' object has no attribute 'add' |
| `remove_header` | `werkzeug.datastructures.Headers.remove` | differential | Input {"headers": {"Authorization": "Bearer token123", "Content-Type": "application/json"}, "key": "Authorization"}: the tool raised ValueError: headers must have a remove method, but the direct library call returned nul |
| `parse_range` | `werkzeug.datastructures.Range.from_header` | differential | Input {"value": "bytes=0-100"}: the tool returned {"ranges": [{"end": 101, "start": 0}], "units": "bytes"}, but the direct library call returned "bytes=0-100" Input {"value": "bytes=0-100,101-200"}: the tool returned {"r |
| `abort_http_exception` | `werkzeug.exceptions.abort` | spec | the direct call failed on every sample, so nothing can be compared. Errors: ['Forbidden: 403 Forbidden: Insufficient permissions for the requested resource.', 'Gone: 410 Gone: The requested resource no longer exists.', ' |
| `quote_header_value` | `werkzeug.http.quote_header_value` | runs | Input {"value": "text/plain"}: the tool raised RecursionError: maximum recursion depth exceeded, but the direct library call returned "\"text/plain\"" Input {"value": "text with spaces"}: the tool raised RecursionError:  |
| `dump_options_header` | `werkzeug.http.dump_options_header` | runs | Input {"header": "text/html", "options": {"charset": "UTF-8"}}: the tool raised RecursionError: maximum recursion depth exceeded, but the direct library call returned "text/html; charset=UTF-8" Input {"header": "applicat |
| `parse_list_header` | `werkzeug.http.parse_list_header` | differential | Input {"value": "token, \"quoted value\""}: the tool raised ValueError: Failed to parse list header: Failed to parse list header: Failed to parse list header: Failed to parse list header: Failed to parse list header: Fai |
| `parse_date` | `werkzeug.http.parse_date` | differential | Input {"value": "Mon, 01 Jan 2023 12:00:00 GMT"}: the tool returned "2023-01-01T12:00:00Z", but the direct library call returned "2023-01-01T12:00:00+00:00" Input {"value": "Wed, 03 Jan 2023 09:15:00"}: the tool returned |
| `format_http_date` | `werkzeug.http.http_date` | differential | Input {"timestamp": "2023-10-15T14:30:00"}: the direct library call raised TypeError: 'str' object cannot be interpreted as an integer, but the tool returned "Sun, 15 Oct 2023 14:30:00 GMT" Input {"timestamp": "2023-10-1 |
| `dump_cookie` | `werkzeug.http.dump_cookie` | differential | Input {"key": "session_id", "value": "abc123"}: the tool raised ValueError: Failed to encode cookie: Failed to encode cookie: Failed to encode cookie: Failed to encode cookie: Failed to encode cookie: Failed to encode co |
| `build_url` | `werkzeug.routing.MapAdapter.build` | spec | the direct call failed on every sample, so nothing can be compared. Errors: ["BuildError: Could not build url for endpoint 'api.resource' with values ['format', 'resource_id'].", "BuildError: Could not build url for endp |
| `match_url` | `werkzeug.routing.MapAdapter.match` | spec | the direct_call expression is wrong: AttributeError: 'str' object has no attribute 'match' |
| `generate_password_hash` | `werkzeug.security.generate_password_hash` | runs | Input {"password": "mySecretPassword123"}: the tool raised RecursionError: maximum recursion depth exceeded, but the direct library call returned "scrypt:32768:8:1$nhGMdSn7mf0FhGe36ZAF8A$9018aeb05cbb3dd87ea2f6255fb017e89 |
| `secure_filename` | `werkzeug.utils.secure_filename` | differential | Input {"filename": "CON.txt"}: the tool returned "_CON.txt", but the direct library call returned "CON.txt" |
| `redirect_response` | `werkzeug.utils.redirect` | differential | Input {"location": ""}: the tool raised ValidationError: 2 validation errors for DictModel location.str Input should be a valid string [type=string_type, input_value=None, input_type=NoneType] For further information vis |
| `parse_url_query_parameters` | `werkzeug.routing.map.SansIORequest.args` | spec | the direct call failed on every sample, so nothing can be compared. Errors: ["TypeError: 'ImmutableMultiDict' object is not callable"]. Use samples that are valid for the library. |
| `check_if_response_is_json` | `werkzeug.sansio.response.Response.is_json` | spec | the direct call failed on every sample, so nothing can be compared. Errors: ["TypeError: 'bool' object is not callable"]. Use samples that are valid for the library. |

## Use

```sh
uv run repo2tools run-model <exercises> --mode tools --base-url <url> --model <model> -- toolsets/generated/werkzeug-bench2/run_server.sh
```
