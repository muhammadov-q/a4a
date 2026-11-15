# Pairs of candidates from different repositories, by similarity

For choosing the threshold: read the pairs and mark from which similarity on two candidates are the same tool.

## low

### Similarity 0.95 to 1.00

- **1.0**
  - [boto__boto3] with_current_context(hook)
  - [aio-libs__aiobotocore] with_current_context(hook)
- **0.998**
  - [pallets__click] Command.shell_complete(ctx: Context, incomplete: str) -> list[CompletionItem]: Return a list of completions for the incomplete value. Looks at the names of options and chained multi-commands.
  - [fastapi__typer] Command.shell_complete(ctx: Context, incomplete: str) -> list['CompletionItem']: Return a list of completions for the incomplete value. Looks at the names of options and chained multi-commands.
- **1.0**
  - [encode__httpcore] HTTPConnection.close() -> None
  - [urllib3__urllib3] HTTPConnection.close() -> None
- **0.968**
  - [fastapi__typer] lenient_issubclass(cls: Any, class_or_tuple: AnyType | tuple[AnyType, ...]) -> bool
  - [fastapi__fastapi] lenient_issubclass(cls: Any, class_or_tuple: type[_T] | tuple[type[_T], ...] | None) -> TypeGuard[type[_T]]
- **0.95**
  - [pallets__click] Option.prompt_for_value(ctx: Context) -> t.Any: This is an alternative flow that can be activated in the full value processing if a value does not exist.  It will prompt the user until a valid value exists and then returns the processed value as result.
  - [fastapi__typer] TyperOption.prompt_for_value(ctx: _click.Context) -> Any: This is an alternative flow that can be activated in the full value processing if a value does not exist.  It will prompt the user until a valid value exists and then returns the processed value as result.
- **1.0**
  - [fastapi__typer] Command.get_usage(ctx: Context) -> str: Formats the usage line into a string and returns it.
  - [pallets__click] Command.get_usage(ctx: Context) -> str: Formats the usage line into a string and returns it.
- **1.0**
  - [kludex__starlette] websocket_session(func: Callable[[WebSocket], Awaitable[None]]) -> ASGIApp: Takes a coroutine `func(session)`, and returns an ASGI application.
  - [fastapi__fastapi] websocket_session(func: Callable[[WebSocket], Awaitable[None]]) -> ASGIApp: Takes a coroutine `func(session)`, and returns an ASGI application.
- **1.0**
  - [fastapi__typer] Command.format_usage(ctx: Context, formatter: HelpFormatter) -> None: Writes the usage line into the formatter.
  - [pallets__click] Command.format_usage(ctx: Context, formatter: HelpFormatter) -> None: Writes the usage line into the formatter.
- **1.0**
  - [fastapi__fastapi] Default(value: DefaultType) -> DefaultType: You shouldn't use this function directly.
  - [fastapi__typer] Default(value: DefaultType) -> DefaultType: You shouldn't use this function directly.
- **1.0**
  - [pallets__click] Command.get_short_help_str(limit: int) -> str: Gets short help for the command or makes it by shortening the long help string.
  - [fastapi__typer] Command.get_short_help_str(limit: int) -> str: Gets short help for the command or makes it by shortening the long help string.

### Similarity 0.90 to 0.95

- **0.921**
  - [pypa__packaging] canonicalize_name(name: str, validate: bool) -> NormalizedName: This function takes a valid Python package or extra name, and returns the normalized form of it.
  - [pypa__distlib] normalize_name(name): Normalize a python package name a la PEP 503
- **0.923**
  - [pypa__distlib] Progress.ETA()
  - [pallets__click] ProgressBar.eta() -> float
- **0.911**
  - [huggingface__huggingface_hub] InferenceClient.text_to_speech(text: str, model: str | None, do_sample: bool | None, early_stopping: Union[bool, 'TextToSpeechEarlyStoppingEnum'] | None, epsilon_cutoff: float | None, eta_cutoff: float | None, max_length: int | None, max_new_tokens: int | None, min_length: int | None, min_new_tokens
  - [openai__openai-python] Audio.speech() -> Speech: Turn audio into text or text into audio.
- **0.923**
  - [agronholm__anyio] Process.kill() -> None: Kills the process.
  - [kludex__uvicorn] Process.kill() -> None
- **0.938**
  - [encode__httpcore] AsyncHTTPConnection.is_closed() -> bool
  - [urllib3__urllib3] HTTPConnection.is_closed() -> bool
- **0.927**
  - [boto__boto3] download_file(self, Bucket, Key, Filename, ExtraArgs, Callback, Config): Download an S3 object to a file.
  - [boto__s3transfer] S3Transfer.download_file(bucket, key, filename, extra_args, callback): Download an S3 object to a file.
- **0.921**
  - [pallets__click] ProgressBar.pct() -> float
  - [prompt-toolkit__python-prompt-toolkit] ProgressBar.percentage() -> int
- **0.932**
  - [dateutil__dateutil] tzlocal.utcoffset(dt)
  - [stub42__pytz] LocalTimezone.utcoffset(dt)
- **0.906**
  - [textualize__rich] Control.bell() -> 'Control': Ring the 'bell'.
  - [prompt-toolkit__python-prompt-toolkit] Output.bell() -> None: Sound bell.
- **0.902**
  - [pyparsing__pyparsing] LRUMemo.clear()
  - [tkem__cachetools] LRUCache.clear()

### Similarity 0.85 to 0.90

- **0.868**
  - [openai__openai-python] Stream.close() -> None: Close the response and release the connection.
  - [encode__httpx] Response.close() -> None: Close the response and release the connection. Automatically called if the response body is read to completion.
- **0.856**
  - [agronholm__anyio] free_tcp_port(free_tcp_port_factory: Callable[[], int]) -> int
  - [pytest-dev__pytest-asyncio] unused_tcp_port_factory() -> Callable[[], int]: A factory function, producing different unused TCP ports.
- **0.877**
  - [pallets__werkzeug] LocalStack.push(obj: T) -> list[T]: Add a new item to the top of the stack.
  - [textualize__rich] Stack.push(item: T) -> None: Push an item on to the stack (append in stack nomenclature).
- **0.858**
  - [agronholm__anyio] UnreliableObjectSendStream.send(item: T_contra) -> None: Send an item to the peer(s).
  - [modelcontextprotocol__python-sdk] ContextSendStream.send(item: T) -> None
- **0.898**
  - [boto__boto3] object_download_file(self, Filename, ExtraArgs, Callback, Config): Download an S3 object to a file.
  - [boto__s3transfer] S3Transfer.download_file(bucket, key, filename, extra_args, callback): Download an S3 object to a file.
- **0.883**
  - [psf__requests] extract_cookies_to_jar(jar: CookieJar, request: PreparedRequest, response: Any) -> None: Extract the cookies from the response into a CookieJar.
  - [encode__httpx] Cookies.extract_cookies(response: Response) -> None: Loads any cookies based on the response `Set-Cookie` headers.
- **0.883**
  - [pydantic__pydantic-settings] _get_alias_names(field_name: str, field_info: FieldInfo, alias_path_args: dict[str, int | None] | None, case_sensitive: bool, populate_by_name: bool, validate_by_alias: bool) -> tuple[tuple[str, ...], bool]: Get alias names for a field, handling alias paths and case sensitivity.
  - [pydantic__pydantic] AliasGenerator.generate_aliases(field_name: str) -> tuple[str | None, str | AliasPath | AliasChoices | None, str | None]: Generate `alias`, `validation_alias`, and `serialization_alias` for a field.
- **0.871**
  - [encode__httpcore] ConnectionInterface.is_closed() -> bool: Return `True` if the connection has been closed.
  - [urllib3__urllib3] HTTPConnection.is_closed() -> bool
- **0.86**
  - [pypa__setuptools] newer(source: str | bytes | os.PathLike[str] | os.PathLike[bytes], target: str | bytes | os.PathLike[str] | os.PathLike[bytes]) -> bool: Is source modified more recently than target.
  - [pypa__distlib] FileOperator.newer(source, target): Tell if the target is newer than the source.
- **0.883**
  - [openai__openai-python] AsyncWebhooks.create(event_types: List[Literal['batch.completed', 'batch.failed', 'batch.expired', 'batch.cancelled', 'response.completed', 'response.failed', 'response.cancelled', 'response.incomplete', 'eval.run.succeeded', 'eval.run.failed', 'eval.run.canceled', 'fine_tuning.job.succeeded', 'fine
  - [huggingface__huggingface_hub] webhooks_create(watch: Annotated[list[str], Option('--watch', help="Item to watch, in 'type:name' format (e.g. 'model:bert-base-uncased'). Repeatable.")], url: Annotated[str | None, Option(help='URL to send webhook payloads to. Mutually exclusive with --job-id.')], job_id: Annotated[str | None, Opti

### Similarity 0.80 to 0.85

- **0.814**
  - [textualize__rich] Style.test(text: str | None) -> None: Write text with style directly to terminal.
  - [fastapi__typer] style(text: Any, fg: int | tuple[int, int, int] | str | None, bg: int | tuple[int, int, int] | str | None, bold: bool | None, dim: bool | None, underline: bool | None, overline: bool | None, italic: bool | None, blink: bool | None, reverse: bool | None, strikethrough: bool | None, reset: bool) -> st
- **0.819**
  - [agronholm__anyio] SpooledTemporaryFile.tell() -> int
  - [boto__s3transfer] DeferredOpenFile.tell()
- **0.828**
  - [encode__httpx] Client.delete(url: URL | str, params: QueryParamTypes | None, headers: HeaderTypes | None, cookies: CookieTypes | None, auth: AuthTypes | UseClientDefault, follow_redirects: bool | UseClientDefault, timeout: TimeoutTypes | UseClientDefault, extensions: RequestExtensions | None) -> Response: Send a `
  - [psf__requests] delete(url: _t.UriType, kwargs: Unpack[_t.RequestKwargs]) -> Response: Sends a DELETE request.
- **0.817**
  - [fsspec__filesystem_spec] AbstractFileSystem.delete(path, recursive, maxdepth): Alias of `AbstractFileSystem.rm`.
  - [huggingface__huggingface_hub] HfFileSystem.rm(path: str, recursive: bool, maxdepth: int | None, revision: str | None, kwargs) -> None: Delete files from a repository.
- **0.832**
  - [urllib3__urllib3] HTTPResponse.closed() -> bool
  - [encode__httpcore] HTTP11Connection.is_closed() -> bool
- **0.816**
  - [openai__openai-python] AsyncBetaWithStreamingResponse.assistants() -> AsyncAssistantsWithStreamingResponse: Build Assistants that can call models and use tools.
  - [huggingface__huggingface_hub] InferenceClient.chat_completion(messages: list[dict | ChatCompletionInputMessage], model: str | None, stream: bool, frequency_penalty: float | None, logit_bias: list[float] | None, logprobs: bool | None, max_tokens: int | None, n: int | None, presence_penalty: float | None, response_format: ChatComp
- **0.848**
  - [modelcontextprotocol__python-sdk] OAuthAuthorizationServerProvider.revoke_token(token: AccessTokenT | RefreshTokenT) -> None: Revokes an access or refresh token.
  - [oauthlib__oauthlib] RevocationEndpoint.create_revocation_response(uri, http_method, body, headers): Revoke supplied access or refresh token.
- **0.83**
  - [rthalley__dnspython] Tokenizer.unget(token: Token) -> None: Unget a token.
  - [pallets__jinja] TokenStream.push(token: Token) -> None: Push a token back to the stream.
- **0.841**
  - [pallets__werkzeug] parse_cookie(cookie: str | None, kwargs: t.Any) -> ds.ImmutableMultiDict[str, str]: Parse cookies from a ``Cookie`` header as an :class:`.ImmutableMultiDict`.
  - [kludex__starlette] cookie_parser(cookie_string: str) -> dict[str, str]: This function parses a ``Cookie`` HTTP header into a dict of key/value pairs.
- **0.839**
  - [textualize__rich] Text.wrap(console: 'Console', width: int, justify: 'JustifyMethod | None', overflow: 'OverflowMethod | None', tab_size: int, no_wrap: bool | None) -> Lines: Word wrap the text.
  - [pallets__jinja] do_wordwrap(environment: 'Environment', s: str, width: int, break_long_words: bool, wrapstring: str | None, break_on_hyphens: bool) -> str: Wrap a string to the given width. Existing newlines are treated as paragraphs to be wrapped separately.

### Similarity 0.75 to 0.80

- **0.784**
  - [networkx__networkx] discrete_sequence(n, distribution, cdistribution, seed): Return sample sequence of length n from a given discrete distribution or discrete cumulative distribution.
  - [more-itertools__more-itertools] random_combination_with_replacement(iterable, r): Return a random *r* length subsequence of elements in *iterable*, allowing individual elements to be repeated.
- **0.768**
  - [urllib3__urllib3] EmscriptenRequest.set_header(name: str, value: str) -> None
  - [psf__requests] MockRequest.add_unredirected_header(name: str, value: str) -> None
- **0.766**
  - [huggingface__huggingface_hub] HfApi.create_scheduled_job(image: str, command: list[str], schedule: str, suspend: bool | None, concurrency: bool | None, env: dict[str, Any] | None, secrets: dict[str, Any] | None, flavor: JobHardware | str | None, timeout: int | float | str | None, attempts: int | None, name: str | None, labels: d
  - [openai__openai-python] AsyncJobs.checkpoints() -> AsyncCheckpoints: Manage fine-tuning jobs to tailor a model to your specific training data.
- **0.788**
  - [tox-dev__filelock] AsyncSoftReadWriteLock.lock_file() -> str: The path to the lock file passed to the constructor.
  - [huggingface__huggingface_hub] WeakFileLock(lock_file: str | Path, timeout: float | None) -> Generator[BaseFileLock, None, None]: A filelock with some custom logic.
- **0.755**
  - [pallets__jinja] RootVisitor.visit_For(node: nodes.For, for_branch: str, kwargs: t.Any) -> None
  - [eliben__pycparser] CGenerator.visit_For(n: c_ast.For) -> str
- **0.795**
  - [huggingface__huggingface_hub] SandboxPool.close() -> None: Release the pool. Idempotent.
  - [encode__httpcore] ConnectionPool.close() -> None
- **0.767**
  - [tox-dev__platformdirs] PlatformDirsABC.user_templates_path() -> Path: Templates path tied to the user.
  - [sqlalchemy__alembic] Config.get_template_directory() -> str: Return the directory where Alembic setup templates are found.
- **0.778**
  - [urllib3__urllib3] HTTP2Connection.connect() -> None
  - [pypa__distlib] HTTPSConnection.connect()
- **0.782**
  - [pydantic__typing-inspection] is_namedtuple(obj: Any) -> bool: Return whether the argument is a named tuple type.
  - [python__typing_extensions] NamedTuple(typename, fields, kwargs): Typed version of namedtuple.
- **0.757**
  - [fsspec__filesystem_spec] MemoryFile.close()
  - [boto__s3transfer] DeferredOpenFile.close()

### Similarity 0.70 to 0.75

- **0.734**
  - [sqlalchemy__alembic] path_relative_to(path: Path, other: Path, walk_up: bool) -> Path
  - [agronholm__anyio] Path.is_relative_to(other: str | PathLike[str]) -> bool
- **0.733**
  - [kludex__starlette] SchemaGenerator.get_schema(routes: list[BaseRoute]) -> dict[str, Any]
  - [fastapi__fastapi] FastAPI.openapi() -> dict[str, Any]: Generate the OpenAPI schema of the application. This is called by FastAPI internally.
- **0.739**
  - [pypa__setuptools] safer_version(version: str) -> str
  - [huggingface__huggingface_hub] safe_revision(revision: str) -> str
- **0.701**
  - [openai__openai-python] DataRetention.retrieve(project_id: str, extra_headers: Headers | None, extra_query: Query | None, extra_body: Body | None, timeout: float | httpx2.Timeout | None | NotGiven) -> ProjectDataRetention: Retrieves project data retention controls.
  - [pypa__hatch] metadata(app: Application, field: str | None): Display project metadata.
- **0.75**
  - [prompt-toolkit__python-prompt-toolkit] Output.disable_autowrap() -> None: Disable auto line wrapping.
  - [textualize__rich] Text.wrap(console: 'Console', width: int, justify: 'JustifyMethod | None', overflow: 'OverflowMethod | None', tab_size: int, no_wrap: bool | None) -> Lines: Word wrap the text.
- **0.701**
  - [openai__openai-python] Turns.retrieve(turn_id: str, session_id: str, extra_headers: Headers | None, extra_query: Query | None, extra_body: Body | None, timeout: float | httpx2.Timeout | None | NotGiven) -> Turn: Retrieves a turn's current status, timestamps, usage, and error.
  - [huggingface__huggingface_hub] HfApi.resume_scheduled_job(scheduled_job_id: str, namespace: str | None, token: bool | str | None) -> None: Resume (unpause) a scheduled compute Job on Hugging Face infrastructure.
- **0.71**
  - [urllib3__urllib3] resolve_ssl_version(candidate: None | int | str) -> int: like resolve_cert_reqs
  - [sethmlarson__truststore] SSLContext.minimum_version() -> ssl.TLSVersion
- **0.705**
  - [rthalley__dnspython] Name.to_digestable(origin: 'Name | None') -> bytes: Convert name to a format suitable for digesting in hashes.
  - [pypa__wheel] safe_name(name: str) -> str: Convert an arbitrary string to a standard distribution name Any runs of non-alphanumeric/. characters are replaced with a single '-'.
- **0.707**
  - [tox-dev__platformdirs] platformdirs_isolated(tmp_path: Path) -> Iterator[Path]: Redirect every platformdirs directory under ``tmp_path`` with :func:`~platformdirs.testing.isolated_dirs`.
  - [pytest-dev__pytest] Testdir.tmpdir() -> LEGACY_PATH: Temporary directory where tests are executed.
- **0.707**
  - [pytest-dev__pytest] ExceptionInfo.typename() -> str: The type name of the exception.
  - [sqlalchemy__mako] RichTraceback.errorname()

### Similarity 0.60 to 0.70

- **0.672**
  - [huggingface__huggingface_hub] XetUploadProgressReporter.format_desc(name: str, indent: bool) -> str: if name is longer than width characters, prints ... at the start and then the last width-3 characters of the name, otherwise the whole name right justified into description_width characters.  Also adds some padding.
  - [tqdm__tqdm] tqdm.set_description(desc, refresh): Set/modify description of the progress bar.
- **0.691**
  - [kludex__uvicorn] HttpToolsProtocol.timeout_keep_alive_handler() -> None: Called on a keep-alive connection if no new data is received after a short delay.
  - [encode__httpcore] HTTPConnection.is_idle() -> bool
- **0.625**
  - [pallets__werkzeug] LanguageAccept.best_match(within: cabc.Iterable[str]) -> str | None
  - [facelessuser__soupsieve] CSSMatch.resolve_lang(el: bs4.Tag, visited: list[int]) -> str: Resolve the language of an element, which is an empty string if it is unknown.
- **0.691**
  - [rthalley__dnspython] from_text(text: str) -> Rcode: Convert text into an rcode.
  - [textualize__rich] Text.from_ansi(text: str, style: str | Style, justify: 'JustifyMethod | None', overflow: 'OverflowMethod | None', no_wrap: bool | None, end: str, tab_size: int | None) -> 'Text': Create a Text object from a string containing ANSI escape codes.
- **0.626**
  - [networkx__networkx] get_edge_attributes(G, name, default): Get edge attributes from graph
  - [executablebooks__markdown-it-py] SyntaxTreeNode.attrGet(name: str) -> str | int | float | None: Get the value of attribute `name`, or null if it does not exist.
- **0.639**
  - [modelcontextprotocol__python-sdk] ResourceTemplate.matches(uri: str) -> dict[str, str | list[str]] | None: Check if a URI matches this template and extract parameters.
  - [sqlalchemy__mako] TemplateLookup.adjust_uri(uri, relativeto): Adjust the given ``uri`` based on the given relative URI.
- **0.676**
  - [pallets__click] Parameter.get_default(ctx: Context, call: t.Literal[True]) -> t.Any | None
  - [fastapi__fastapi] Default(value: DefaultType) -> DefaultType: You shouldn't use this function directly.
- **0.625**
  - [openai__openai-python] Files.create(container_id: str, file: FileTypes | Omit, file_id: str | Omit, extra_headers: Headers | None, extra_query: Query | None, extra_body: Body | None, timeout: float | httpx2.Timeout | None | NotGiven) -> FileCreateResponse: Create a Container File
  - [huggingface__huggingface_hub] HfApi.upload_file(path_or_fileobj: str | Path | bytes | BinaryIO, path_in_repo: str, repo_id: str, token: str | bool | None, repo_type: str | None, revision: str | None, commit_message: str | None, commit_description: str | None, create_pr: bool | None, parent_commit: str | None, run_as_future: bool
- **0.614**
  - [prompt-toolkit__python-prompt-toolkit] Container.is_modal() -> bool: When this container is modal, key bindings from parent containers are not taken into account if a user control in this container is focused.
  - [textualize__rich] Control.show_cursor(show: bool) -> 'Control': Show or hide the cursor.
- **0.619**
  - [networkx__networkx] Graph.to_directed_class(): Returns the class to use for empty directed copies.
  - [prompt-toolkit__python-prompt-toolkit] vi_digraph_mode() -> bool

## medium

### Similarity 0.95 to 1.00

- **1.0**
  - [pallets__click] Command.get_usage(ctx: Context) -> str: Formats the usage line into a string and returns it.
  - [fastapi__typer] Command.get_usage(ctx: Context) -> str: Formats the usage line into a string and returns it.
- **1.0**
  - [fastapi__typer] getchar(echo: bool) -> str: Fetches a single character from the terminal and returns it.  This will always return a unicode character and under certain rare circumstances this might return more than one character.  The situations which more than one character is returned is when for whatever reason 
  - [pallets__click] getchar(echo: bool) -> str: Fetches a single character from the terminal and returns it.  This will always return a unicode character and under certain rare circumstances this might return more than one character.  The situations which more than one character is returned is when for whatever reason 
- **1.0**
  - [aio-libs__aiobotocore] with_current_context(hook)
  - [boto__boto3] with_current_context(hook)
- **0.99**
  - [fastapi__typer] Command.invoke(ctx: Context) -> Any: Given a context, this invokes the attached callback (if it exists) in the right way.
  - [pallets__click] Command.invoke(ctx: Context) -> t.Any: Given a context, this invokes the attached callback (if it exists) in the right way.
- **1.0**
  - [pypa__wheel] WheelFile.writestr(zinfo_or_arcname: str | ZipInfo, data: SizedBuffer | str, compress_type: int | None) -> None
  - [pypa__setuptools] WheelFile.writestr(zinfo_or_arcname: str | ZipInfo, data: SizedBuffer | str, compress_type: int | None) -> None
- **1.0**
  - [pallets__werkzeug] Headers: unite two of them (|)
  - [kludex__starlette] Headers: unite two of them (|)
- **0.975**
  - [textualize__rich] ProgressBar: read its properties: percentage_completed
  - [prompt-toolkit__python-prompt-toolkit] ProgressBar: read its properties: percentage
- **1.0**
  - [boto__s3transfer] S3Transfer.upload_file(filename, bucket, key, callback, extra_args): Upload a file to an S3 object.
  - [boto__boto3] S3Transfer.upload_file(filename, bucket, key, callback, extra_args): Upload a file to an S3 object.
- **1.0**
  - [fastapi__typer] Command.get_help_option_names(ctx: Context) -> list[str]: Returns the names for the help option.
  - [pallets__click] Command.get_help_option_names(ctx: Context) -> list[str]: Returns the names for the help option.
- **1.0**
  - [pypa__hatch] main() -> None
  - [encode__httpx] main() -> None

### Similarity 0.90 to 0.95

- **0.917**
  - [modelcontextprotocol__python-sdk] ContextReceiveStream.aclose() -> None
  - [agronholm__anyio] TextReceiveStream.aclose() -> None
- **0.906**
  - [kludex__starlette] MultiDict.setdefault(key: Any, default: Any) -> Any
  - [pallets__werkzeug] MultiDict.setdefault(key: K) -> None
- **0.923**
  - [requests__toolbelt] get_unicode_from_response(response): Return the requested content back in unicode.
  - [psf__requests] get_unicode_from_response(r: Response) -> str | bytes | None: Returns the requested content back in unicode.
- **0.921**
  - [kludex__uvicorn] Process.kill() -> None
  - [agronholm__anyio] Process.kill() -> None: Kills the process.
- **0.92**
  - [sqlalchemy__mako] LoopContext: read its properties: reverse_index, first, last, even, odd
  - [pallets__jinja] LoopContext: read its properties: length, depth, index, revindex0, revindex, first, last, previtem, nextitem
- **0.949**
  - [pyasn1__pyasn1] Tag: add two of them (+)
  - [pyparsing__pyparsing] Keyword: add two of them (+)
- **0.9**
  - [requests__toolbelt] MultipartEncoder(fields, boundary, encoding): build a MultipartEncoder. The ``MultipartEncoder`` object is a generic interface to the engine that will create a ``multipart/form-data`` body for you.
  - [pallets__werkzeug] MultipartEncoder(boundary: bytes): build a MultipartEncoder. Used by the test client to create a multipart body. This is not secure and must only be used during testing, never in applications.
- **0.915**
  - [openai__openai-python] Speech(): build a Speech. Turn audio into text or text into audio.
  - [huggingface__huggingface_hub] InferenceClient.text_to_speech(text: str, model: str | None, do_sample: bool | None, early_stopping: Union[bool, 'TextToSpeechEarlyStoppingEnum'] | None, epsilon_cutoff: float | None, eta_cutoff: float | None, max_length: int | None, max_new_tokens: int | None, min_length: int | None, min_new_tokens
- **0.905**
  - [fsspec__filesystem_spec] AbstractFileSystem.find(path, maxdepth, withdirs, detail, kwargs): List all files below path.
  - [huggingface__huggingface_hub] HfFileSystem.find(path: str, maxdepth: int | None, withdirs: bool, detail: bool, refresh: bool, revision: str | None, kwargs) -> list[str] | dict[str, dict[str, Any]]: List all files below path.
- **0.912**
  - [modelcontextprotocol__python-sdk] UntitledJsonSchema.field_title_should_be_set(schema: Any) -> bool
  - [pydantic__pydantic] GenerateJsonSchema.field_title_should_be_set(schema: CoreSchemaOrField) -> bool: Returns true if a field with the given schema should have a title set based on the field name.

### Similarity 0.85 to 0.90

- **0.855**
  - [rthalley__dnspython] IDNACodec(): build a IDNACodec. Abstract base class for IDNA encoder/decoders.
  - [kjd__idna] Codec(): build a Codec. Stateless IDNA 2008 codec.
- **0.875**
  - [textualize__rich] ConsoleOptions: compare two of them (smaller, equal, greater)
  - [rthalley__dnspython] Option: compare two of them (smaller, equal, greater)
- **0.865**
  - [textualize__rich] Console.set_alt_screen(enable: bool) -> bool: Enables alternative screen mode.
  - [prompt-toolkit__python-prompt-toolkit] Output.enter_alternate_screen() -> None: Go to the alternate screen buffer. (For full screen applications).
- **0.893**
  - [pallets__click] Context.get_usage() -> str: Helper method to get formatted usage string for the current context and command.
  - [fastapi__typer] Command.get_usage(ctx: Context) -> str: Formats the usage line into a string and returns it.
- **0.861**
  - [kludex__starlette] Headers.keys() -> list[str]
  - [encode__httpx] Headers.keys() -> typing.KeysView[str]
- **0.887**
  - [dateutil__dateutil] isoparser.parse_tzstr(tzstr, zero_as_utc): Parse a valid ISO time zone string.
  - [gweis__isodate] parse_tzinfo(tzstring: str) -> Union[tzinfo, None]: Parses ISO 8601 time zone designators to tzinfo objects.
- **0.869**
  - [requests__toolbelt] MultipartDecoder(content, content_type, encoding): build a MultipartDecoder. The ``MultipartDecoder`` object parses the multipart payload of a bytestring into a tuple of ``Response``-like ``BodyPart`` objects.
  - [pallets__werkzeug] MultipartDecoder(boundary: bytes, max_form_memory_size: int | None, max_parts: int | None): build a MultipartDecoder. Decodes a multipart message as bytes into Python events.
- **0.876**
  - [pydantic__pydantic] GenerateJsonSchema.json_schema(schema: core_schema.JsonSchema) -> JsonSchemaValue: Generates a JSON schema that matches a schema that defines a JSON object.
  - [modelcontextprotocol__python-sdk] UntitledJsonSchema(): build a UntitledJsonSchema. A JSON schema generator that leaves out the titles pydantic derives from field names.
- **0.855**
  - [kjd__idna] Codec(): build a Codec. Stateless IDNA 2008 codec.
  - [rthalley__dnspython] IDNACodec(): build a IDNACodec. Abstract base class for IDNA encoder/decoders.
- **0.877**
  - [openai__openai-python] AsyncAudioWithRawResponse.speech() -> AsyncSpeechWithRawResponse: Turn audio into text or text into audio.
  - [huggingface__huggingface_hub] AsyncInferenceClient.automatic_speech_recognition(audio: ContentT, model: str | None, extra_body: dict | None) -> AutomaticSpeechRecognitionOutput: Perform automatic speech recognition (ASR or audio-to-text) on the given audio content.

### Similarity 0.80 to 0.85

- **0.847**
  - [kludex__uvicorn] is_dir(path: Path) -> bool
  - [fsspec__filesystem_spec] DirFileSystem.isdir(path)
- **0.825**
  - [pyparsing__pyparsing] WordStart: unite two of them (|)
  - [pypa__packaging] Marker: unite two of them (|)
- **0.817**
  - [python__importlib_metadata] PackagePath.read_binary() -> bytes
  - [agronholm__anyio] Path.read_bytes() -> bytes
- **0.828**
  - [fsspec__filesystem_spec] AsyncStreamFile.close()
  - [agronholm__anyio] AsyncFile.aclose() -> None
- **0.814**
  - [fsspec__filesystem_spec] GithubFileSystem: read its properties: kw, tags, branches, refs
  - [huggingface__huggingface_hub] HfApi.list_repo_tree(repo_id: str, path_in_repo: str | None, recursive: bool, expand: bool, revision: str | None, repo_type: str | None, token: str | bool | None) -> Iterable[RepoFile | RepoFolder]: List a repo tree's files and folders and get information about them.
- **0.811**
  - [pydantic__pydantic] BaseValidateHandlerProtocol.on_error(error: ValidationError) -> None: Callback to be notified of validation errors.
  - [textualize__rich] PromptBase.on_validate_error(value: str, error: InvalidResponse) -> None: Called to handle validation error.
- **0.8**
  - [urllib3__urllib3] wait_for_read(sock: socket.socket, timeout: float | None) -> bool: Waits for reading to be available on a given socket. Returns True if the socket is readable, or False if the timeout expired.
  - [agronholm__anyio] wait_socket_readable(sock: socket.socket) -> Awaitable[None]: .. deprecated:: 4.7.0    Use :func:`wait_readable` instead.
- **0.814**
  - [pallets__jinja] fake_traceback(exc_value: BaseException, tb: TracebackType | None, filename: str, lineno: int) -> TracebackType: Produce a new traceback object that looks like it came from the template source instead of the compiled code. The filename, line number, and location name will point to the template, and 
  - [textualize__rich] Traceback.from_exception(exc_type: type[Any], exc_value: BaseException, traceback: TracebackType | None, width: int | None, code_width: int | None, extra_lines: int, theme: str | None, word_wrap: bool, show_locals: bool, locals_max_length: int, locals_max_string: int, locals_max_depth: int | None, l
- **0.838**
  - [fsspec__filesystem_spec] AbstractFileSystem.rmdir(path): Remove a directory, if empty
  - [agronholm__anyio] Path.rmdir() -> None
- **0.801**
  - [pytest-dev__pytest-asyncio] pytest_report_header(config: Config) -> list[str]: Add asyncio config to pytest header.
  - [pytest-dev__pytest] TerminalReporter.pytest_report_header(config: Config) -> list[str]

### Similarity 0.75 to 0.80

- **0.791**
  - [sybrenstuvel__python-rsa] PrivateKey(n: int, e: int, d: int, p: int, q: int, rs: typing.Optional[typing.List[int]]): build a PrivateKey. Represents a private RSA key.
  - [rthalley__dnspython] CryptographyPrivateKey(key: Any): build a CryptographyPrivateKey
- **0.76**
  - [textualize__rich] Syntax.from_path(path: str, encoding: str, lexer: Lexer | str | None, theme: str | SyntaxTheme, dedent: bool, line_numbers: bool, line_range: tuple[int, int] | None, start_line: int, highlight_lines: set[int] | None, code_width: int | None, tab_size: int, word_wrap: bool, background_color: str | Non
  - [prompt-toolkit__python-prompt-toolkit] PygmentsLexer.from_filename(filename: str, sync_from_start: FilterOrBool) -> Lexer: Create a `Lexer` from a filename.
- **0.777**
  - [pydantic__pydantic] EncoderProtocol.get_json_format() -> str: Get the JSON format for the encoded data.
  - [textualize__rich] JSON.from_data(data: Any, indent: None | int | str, highlight: bool, skip_keys: bool, ensure_ascii: bool, check_circular: bool, allow_nan: bool, default: Callable[[Any], Any] | None, sort_keys: bool) -> 'JSON': Encodes a JSON object from arbitrary data.
- **0.751**
  - [pytest-dev__pytest] Collector(): build a Collector. Base class of all collectors.
  - [pypa__hatch] EnvironmentCollectorInterface(root, config): build a EnvironmentCollectorInterface. Example usage:
- **0.787**
  - [textualize__rich] NullFile.writelines(__lines: Iterable[str]) -> None
  - [agronholm__anyio] AsyncFile.writelines(lines: Iterable[ReadableBuffer] | Iterable[str]) -> None
- **0.773**
  - [oauthlib__oauthlib] Client.prepare_request_body(args, kwargs): Abstract method used to create request bodies.
  - [psf__requests] PreparedRequest.prepare_body(data: _t.DataType, files: _t.FilesType, json: _t.JsonType) -> None: Prepares the given HTTP body data.
- **0.755**
  - [openai__openai-python] AsyncResponses.compact(model: Union[Literal['gpt-6-astra', 'gpt-6.1-sol', 'gpt-6.1-terra', 'gpt-6-sol', 'gpt-6-luna', 'gpt-5.6-sol', 'gpt-5.6-terra', 'gpt-5.6-luna', 'gpt-5.5', 'gpt-5.5-2026-04-23', 'gpt-5.4', 'gpt-5.4-mini', 'gpt-5.4-nano', 'gpt-5.4-mini-2026-03-17', 'gpt-5.4-nano-2026-03-17', 'gpt
  - [huggingface__huggingface_hub] InferenceClient.chat_completion(messages: list[dict | ChatCompletionInputMessage], model: str | None, stream: bool, frequency_penalty: float | None, logit_bias: list[float] | None, logprobs: bool | None, max_tokens: int | None, n: int | None, presence_penalty: float | None, response_format: ChatComp
- **0.769**
  - [prompt-toolkit__python-prompt-toolkit] DummyInput: read its properties: closed
  - [fsspec__filesystem_spec] LocalFileOpener: read its properties: closed
- **0.769**
  - [tartley__colorama] GetConsoleScreenBufferInfo(stream_id)
  - [prompt-toolkit__python-prompt-toolkit] Win32Output.get_win32_screen_buffer_info() -> CONSOLE_SCREEN_BUFFER_INFO: Return Screen buffer info.
- **0.771**
  - [fsspec__filesystem_spec] AbstractFileSystem.cp(path1, path2, kwargs): Alias of `AbstractFileSystem.copy`.
  - [huggingface__huggingface_hub] HfFileSystem.cp_file(path1: str, path2: str, revision: str | None, kwargs) -> None: Copy a file within or between repositories, or into a bucket.

### Similarity 0.70 to 0.75

- **0.724**
  - [prompt-toolkit__python-prompt-toolkit] FuzzyCompleter.get_completions(document: Document, complete_event: CompleteEvent) -> Iterable[Completion]
  - [pallets__click] ShellComplete.get_completions(args: list[str], incomplete: str) -> list[CompletionItem[str]]: Determine the context and last complete command or parameter from the complete args. Call that object's ``shell_complete`` method to get the completions for the incomplete value.
- **0.704**
  - [pallets__werkzeug] MapAdapter.allowed_methods(path_info: str | None) -> t.Iterable[str]: Returns the valid methods that match for a given path.
  - [openai__openai-python] Models(): build a Models. List and describe the various models available in the API.
- **0.72**
  - [openai__openai-python] AsyncEvals.retrieve(eval_id: str, extra_headers: Headers | None, extra_query: Query | None, extra_body: Body | None, timeout: float | httpx2.Timeout | None | NotGiven) -> EvalRetrieveResponse: Get an evaluation by ID.
  - [huggingface__huggingface_hub] metadata_eval_result(model_pretty_name: str, task_pretty_name: str, task_id: str, metrics_pretty_name: str, metrics_id: str, metrics_value: Any, dataset_pretty_name: str, dataset_id: str, metrics_config: str | None, metrics_verified: bool, dataset_config: str | None, dataset_split: str | None, datas
- **0.724**
  - [agronholm__anyio] as_completed(awaitables: Awaitable[R]) -> AsyncGenerator[MemoryObjectReceiveStream[TaskHandle[R]]]: Run awaitable objects concurrently in a task group, returning an iterator which can be used to get finished task handles in the order they complete.
  - [tqdm__tqdm] tqdm_asyncio.as_completed(fs, loop, timeout, total, tqdm_kwargs): Wrapper for `asyncio.as_completed`.
- **0.724**
  - [modelcontextprotocol__python-sdk] ResponseCacheStore.set(key: CacheKey, entry: CacheEntry) -> None
  - [rthalley__dnspython] LRUCache.put(key: CacheKey, value: Answer) -> None: Associate key and value in the cache.
- **0.72**
  - [openai__openai-python] AsyncVideos.poll(video_id: str, poll_interval_ms: int | Omit) -> Video: Wait for the vector store file to finish processing.
  - [huggingface__huggingface_hub] jobs_wait(job_ids: Annotated[list[str], Argument(help="Job IDs to wait for (or 'namespace/job_id').")], timeout: Annotated[str | None, Option(help='Max time to wait: int with s (seconds, default), m (minutes), h (hours) or d (days).')], namespace: NamespaceOpt, token: TokenOpt) -> None: Wait for one
- **0.715**
  - [openai__openai-python] RealtimeWithRawResponse.client_secrets() -> ClientSecretsWithRawResponse
  - [oauthlib__oauthlib] RequestValidator.get_client_secret(client_key, request): Retrieves the client secret associated with the client key.
- **0.702**
  - [rthalley__dnspython] TrioQuicStream(connection, stream_id): build a TrioQuicStream
  - [modelcontextprotocol__python-sdk] StreamableHTTPServerTransport.connect() -> AsyncGenerator[tuple[ReadStream[SessionMessage | Exception], WriteStream[SessionMessage]], None]: Context manager that provides read and write streams for a connection.
- **0.71**
  - [tiran__defusedxml] iterparse(args, kwargs)
  - [boto__s3transfer] StreamReaderProgress.read(args, kwargs)
- **0.701**
  - [fsspec__filesystem_spec] DirCache(use_listings_cache, listings_expiry_time, max_paths, kwargs): build a DirCache. Caching of directory listings, in a structure like::
  - [pytest-dev__pytest] Cache(cachedir: Path, config: Config, _ispytest: bool): build a Cache. Instance of the `cache` fixture.

### Similarity 0.60 to 0.70

- **0.64**
  - [openai__openai-python] AsyncBrowserToolset(driver: AsyncBrowserDriver, members: Sequence[str] | None, additional_members: Sequence[str] | None, confirm_reads: Sequence[str] | None, confirm: Callable[[BrowserConfirmContext], Awaitable[bool]] | Callable[[BrowserConfirmContext | BrowserReadConfirmContext], Awaitable[bool]] |
  - [modelcontextprotocol__python-sdk] Apps.tools() -> Sequence[ToolBinding]: The bound tools.
- **0.602**
  - [networkx__networkx] TimeRespectingDiGraphMatcher.test_two(pred_dates, succ_dates): Edges from a dual Gx_node in the mapping should be ordered in a time-respecting manner.
  - [dateutil__dateutil] within_delta(dt1, dt2, delta): Useful for comparing two datetimes that may have a negligible difference to be considered equal.
- **0.639**
  - [fastapi__fastapi] get_request_handler(dependant: Dependant, body_field: ModelField | None, status_code: int | None, response_class: type[Response] | DefaultPlaceholder, response_field: ModelField | None, response_model_include: IncEx | None, response_model_exclude: IncEx | None, response_model_by_alias: bool, respons
  - [modelcontextprotocol__python-sdk] Server.get_request_handler(method: str) -> HandlerEntry[LifespanResultT] | None: Return the registered entry for a request method, or `None`.
- **0.66**
  - [rthalley__dnspython] PrivateDSA.generate(key_size: int) -> Self
  - [sybrenstuvel__python-rsa] newkeys(nbits: int, accurate: bool, poolsize: int, exponent: int, nprimes: int) -> typing.Tuple[PublicKey, PrivateKey]: Generates public and private keys, and returns them as (pub, priv).
- **0.696**
  - [kludex__uvicorn] WebSocketProtocol.connection_made(transport: asyncio.Transport) -> None
  - [kludex__starlette] WebSocketEndpoint.on_connect(websocket: WebSocket) -> None: Override to handle an incoming websocket connection
- **0.687**
  - [jpadilla__pyjwt] HMACAlgorithm.prepare_key(key: str | bytes) -> bytes
  - [pallets__itsdangerous] HMACAlgorithm.get_signature(key: bytes, value: bytes) -> bytes
- **0.636**
  - [rthalley__dnspython] ImmutableNode.is_immutable() -> bool
  - [networkx__networkx] is_frozen(G): Returns True if graph is frozen.
- **0.669**
  - [huggingface__huggingface_hub] read_tree_cache(tree_cache_folder: str, commit_hash: str) -> dict[str, TreeCacheEntry] | None: Return the cached tree listing for a commit hash, or `None` if not cached, invalid, or unreadable.
  - [fsspec__filesystem_spec] CachingFileSystem.load_cache(): Read set of stored blocks from file
- **0.62**
  - [jmespath__jmespath.py] IncompleteExpressionError(): build a IncompleteExpressionError
  - [python-poetry__tomlkit] Parser.parse_error(exception: type[ParseError], args: Any, kwargs: Any) -> ParseError: Creates a generic "parse error" at the current position.
- **0.633**
  - [networkx__networkx] topological_sort(G): Returns a generator of nodes in topologically sorted order.
  - [more-itertools__more-itertools] derangements(iterable, r): Yield successive derangements of the elements in *iterable*.

## high

### Similarity 0.95 to 1.00


### Similarity 0.90 to 0.95

- **0.929**
  - [encode__httpx] Example that uses delete, head, options, put: r = httpx.put('https://httpbin.org/put', data={'key': 'value'}) r = httpx.delete('https://httpbin.org/delete') r = httpx.head('https://httpbin.org/get') r = httpx.options('https://httpbin.org/get')
  - [psf__requests] Example that uses delete, head, options, put: r = requests.put('https://httpbin.org/put', data={'key': 'value'}) r = requests.delete('https://httpbin.org/delete') r = requests.head('https://httpbin.org/get') r = requests.options('https://httpbin.org/get')
- **0.929**
  - [psf__requests] Example that uses delete, head, options, put: r = requests.put('https://httpbin.org/put', data={'key': 'value'}) r = requests.delete('https://httpbin.org/delete') r = requests.head('https://httpbin.org/get') r = requests.options('https://httpbin.org/get')
  - [encode__httpx] Example that uses delete, head, options, put: r = httpx.put('https://httpbin.org/put', data={'key': 'value'}) r = httpx.delete('https://httpbin.org/delete') r = httpx.head('https://httpbin.org/get') r = httpx.options('https://httpbin.org/get')

### Similarity 0.85 to 0.90

- **0.866**
  - [psf__requests] Example that uses Response.text, Session.post: url = 'https://httpbin.org/post' multiple_files = [ r = requests.post(url, files=multiple_files) r.text
  - [encode__httpx] Example that uses Response.text, post: files = {'upload-file': (None, 'text content', 'text/plain')} r = httpx.post("https://httpbin.org/post", files=files) print(r.text)
- **0.86**
  - [encode__httpx] Example that uses Response.raise_for_status, Response.request, Response.url, get: response = httpx.get("https://www.example.com/") try:     response.raise_for_status() except httpx.HTTPStatusError as exc:     print(f"Error response {exc.response.status_code} while requesting {exc.request.url!r}.")
  - [psf__requests] Example that uses Response.raise_for_status, get: bad_r = requests.get('https://httpbin.org/status/404') bad_r.status_code bad_r.raise_for_status()
- **0.9**
  - [psf__requests] Example that uses Response.raise_for_status, get: bad_r = requests.get('https://httpbin.org/status/404') bad_r.status_code bad_r.raise_for_status()
  - [encode__httpx] Example that uses Response.raise_for_status, get: not_found = httpx.get('https://httpbin.org/status/404') not_found.status_code not_found.raise_for_status()
- **0.9**
  - [encode__httpx] Example that uses Response.raise_for_status, get: not_found = httpx.get('https://httpbin.org/status/404') not_found.status_code not_found.raise_for_status()
  - [psf__requests] Example that uses Response.raise_for_status, get: bad_r = requests.get('https://httpbin.org/status/404') bad_r.status_code bad_r.raise_for_status()
- **0.866**
  - [encode__httpx] Example that uses Response.text, post: files = {'upload-file': (None, 'text content', 'text/plain')} r = httpx.post("https://httpbin.org/post", files=files) print(r.text)
  - [psf__requests] Example that uses Response.text, Session.post: url = 'https://httpbin.org/post' multiple_files = [ r = requests.post(url, files=multiple_files) r.text

### Similarity 0.80 to 0.85

- **0.811**
  - [urllib3__urllib3] Example that uses BaseHTTPResponse.release_conn, BaseHTTPResponse.stream, request: import urllib3  resp = urllib3.request(     "GET",     "https://httpbin.org/bytes/1024",     preload_content=False )  for chunk in resp.stream(32):     print(chunk)     # b"\x9e\xa97'\x8e\x1eT ....  resp.release_conn(
  - [encode__httpcore] Example that uses Response.iter_stream, stream: import httpcore  with httpcore.stream('GET', 'https://example.com') as response:     for chunk in response.iter_stream():         print(f"Downloaded: {chunk}")
- **0.812**
  - [pallets__werkzeug] Example that uses Client(), Response(), Client.get, Request.application, Response.text, Response.status_code: from werkzeug import Request, Response, Client  @Request.application def app(request: Request) -> Response:     return Response("Hello, World!")  c = Client(app) r = c.get("/") assert r.stat
  - [encode__httpx] Example that uses Client(), WSGITransport(), Client.get, Response.text: from flask import Flask import httpx   app = Flask(__name__)  @app.route("/") def hello():     return "Hello World!"  transport = httpx.WSGITransport(app=app) with httpx.Client(transport=transport, base_url="http://testserver") 
- **0.831**
  - [psf__requests] Example that uses Response.json, Response.text, get: import requests r = requests.get('https://httpbin.org/basic-auth/user/pass', auth=('user', 'pass')) r.status_code r.headers['content-type'] r.encoding r.text r.json()
  - [encode__httpx] Example that uses Response.text, get: import httpx r = httpx.get('https://www.example.org/') r r.status_code r.headers['content-type'] r.text
- **0.811**
  - [encode__httpcore] Example that uses Response.iter_stream, stream: import httpcore  with httpcore.stream('GET', 'https://example.com') as response:     for chunk in response.iter_stream():         print(f"Downloaded: {chunk}")
  - [urllib3__urllib3] Example that uses BaseHTTPResponse.release_conn, BaseHTTPResponse.stream, request: import urllib3  resp = urllib3.request(     "GET",     "https://httpbin.org/bytes/1024",     preload_content=False )  for chunk in resp.stream(32):     print(chunk)     # b"\x9e\xa97'\x8e\x1eT ....  resp.release_conn(
- **0.822**
  - [urllib3__urllib3] Example that uses BaseHTTPResponse.json, request: import urllib3 resp = urllib3.request("GET", "https://httpbin.org/anything")  print(resp.status)  # 200 print(resp.headers) # HTTPHeaderDict(...) print(resp.json())  # {"headers": {"Accept": "*/*", ...}, ...}
  - [psf__requests] Example that uses Response.json, Response.text, get: import requests r = requests.get('https://httpbin.org/basic-auth/user/pass', auth=('user', 'pass')) r.status_code r.headers['content-type'] r.encoding r.text r.json()
- **0.836**
  - [encode__httpcore] Example that uses Response.content, request: import httpcore  response = httpcore.request("GET", "https://www.example.com/")  print(response) # <Response [200]> print(response.status) # 200 print(response.headers) # [(b'Accept-Ranges', b'bytes'), (b'Age', b'557328'), (b'Cache-Control', b'max-age=604
  - [psf__requests] Example that uses Response.content, get: import requests r = requests.get('https://www.python.org') r.status_code b'Python is a programming language' in r.content
- **0.815**
  - [encode__httpx] Example that uses Cookies(), Cookies.set, Response.json, get: cookies = httpx.Cookies() cookies.set('cookie_on_domain', 'hello, there!', domain='httpbin.org') cookies.set('cookie_off_domain', 'nope.', domain='example.org') r = httpx.get('http://httpbin.org/cookies', cookies=cookies) r.json()
  - [psf__requests] Example that uses RequestsCookieJar(), Response.text, RequestsCookieJar.set, get: jar = requests.cookies.RequestsCookieJar() jar.set('tasty_cookie', 'yum', domain='httpbin.org', path='/cookies') jar.set('gross_cookie', 'blech', domain='httpbin.org', path='/elsewhere') url = 'https://httpbin.org/cook
- **0.812**
  - [encode__httpx] Example that uses Client(), WSGITransport(), Client.get, Response.text: from flask import Flask import httpx   app = Flask(__name__)  @app.route("/") def hello():     return "Hello World!"  transport = httpx.WSGITransport(app=app) with httpx.Client(transport=transport, base_url="http://testserver") 
  - [pallets__werkzeug] Example that uses Client(), Response(), Client.get, Request.application, Response.text, Response.status_code: from werkzeug import Request, Response, Client  @Request.application def app(request: Request) -> Response:     return Response("Hello, World!")  c = Client(app) r = c.get("/") assert r.stat
- **0.809**
  - [encode__httpx] Example that uses Response.json, get: r = httpx.get('https://api.github.com/events') r.json()
  - [psf__requests] Example that uses Response.json, get: import requests r = requests.get('https://api.github.com/events') r.json()   # This *call* raises an exception if JSON decoding fails
- **0.823**
  - [psf__requests] Example that uses Response.text, post: payload = {'key1': 'value1', 'key2': 'value2'} r = requests.post('https://httpbin.org/post', data=payload) print(r.text)
  - [encode__httpx] Example that uses Response.text, post: files = {'upload-file': (None, 'text content', 'text/plain')} r = httpx.post("https://httpbin.org/post", files=files) print(r.text)

### Similarity 0.75 to 0.80

- **0.789**
  - [pypa__packaging] Example that uses Version <, Version <=, Version ==, Version >, Version >=, Version(): v1 = Version("1.0a5") v2 = Version("1.0") v1 v2 v1 < v2 v1 == v2 v1 > v2 v1 >= v2 v1 <= v2
  - [pypa__distlib] Example that uses LegacyVersion ==, LegacyVersion(), NormalizedVersion ==, NormalizedVersion(), SemanticVersion ==, SemanticVersion(): from distlib.version import SemanticVersion, LegacyVersion nv = NormalizedVersion('1.0.0') lv = LegacyVersion('1.0.0') sv = SemanticVersion('1.0.0') lv == sv nv == s
- **0.769**
  - [python-hyper__h11] Example that uses Connection(), Connection.send: import ssl, socket import h11  ctx = ssl.create_default_context() sock = ctx.wrap_socket(socket.create_connection(("httpbin.org", 443)),                        server_hostname="httpbin.org")  conn = h11.Connection(our_role=h11.CLIENT) request = h11.Re
  - [encode__httpcore] Example that uses SyncBackend(), NetworkStream.read, NetworkStream.start_tls, NetworkStream.write, SyncBackend.connect_tcp, default_ssl_context: import httpcore  # Create an SSL context using 'certifi' for the certificates. ssl_context = httpcore.default_ssl_context()  # A basic HTTP/1.1 request as 
- **0.767**
  - [oauthlib__oauthlib] Example that uses MobileApplicationClient(), MobileApplicationClient.prepare_request_uri: from oauthlib.oauth2 import MobileApplicationClient client = MobileApplicationClient('your_id') client.prepare_request_uri('https://example.com') client.prepare_request_uri('https://example.com', redirect_uri='
  - [requests__requests-oauthlib] Example that uses OAuth2Session(), OAuth2Session.authorization_url, OAuth2Session.token_from_fragment: import requests from requests_oauthlib import OAuth2Session from oauthlib.oauth2 import MobileApplicationClient client_id = "<your client ID here>" scope = ["activity", "heartrate", "location", "nu
- **0.752**
  - [encode__httpx] Example that uses ASGITransport(), AsyncClient(), Client.get, Response.text: transport = httpx.ASGITransport(app=app)  async with httpx.AsyncClient(transport=transport, base_url="http://testserver") as client:     r = await client.get("/")     assert r.status_code == 200     assert r.text == "Hello 
  - [pallets__werkzeug] Example that uses Client(), Response(), Client.get, Request.application, Response.text, Response.status_code: from werkzeug import Request, Response, Client  @Request.application def app(request: Request) -> Response:     return Response("Hello, World!")  c = Client(app) r = c.get("/") assert r.stat
- **0.758**
  - [huggingface__huggingface_hub] Example that uses AsyncInferenceClient(), RepoCard.content: from huggingface_hub import AsyncInferenceClient client = AsyncInferenceClient("meta-llama/Meta-Llama-3-70B-Instruct") messages = [ response_format = { response = await client.chat_completion( response.choices[0].message.content
  - [openai__openai-python] Example that uses AsyncOpenAI(), AsyncOpenAI.chat, OpenAI.chat, bedrock: from openai import AsyncOpenAI  client = AsyncOpenAI(provider=bedrock(endpoint="runtime", region="us-west-2", api_key=None)) completion = await client.chat.completions.create(     model="us.openai.gpt-5.6-sol",     messages=[{"
- **0.768**
  - [psf__requests] Example that uses Request(), Session(), Session.prepare_request, Session.send: from requests import Request, Session  s = Session() req = Request('GET',  url, data=data, headers=headers)  prepped = s.prepare_request(req)  # do something with prepped.body prepped.body = 'Seriously, send exactly these
  - [requests__toolbelt] Example that uses HostHeaderSSLAdapter.send, BaseUrlSession.prepare_request, BaseUrlSession.request: from requests import Request from requests_toolbelt import sessions s = sessions.BaseUrlSession( request = Request(method='GET', url='sub-resource/') prepared_request = s.prepare_request(request) r =
- **0.756**
  - [urllib3__urllib3] Example that uses HTTPResponse.release_conn, HTTPConnection.getresponse: # Set by the HTTPConnectionPool before returning to the caller. resp = conn.getresponse() resp._pool = pool  # This will call resp._pool._put_conn(resp.connection) # Connection can get auto-released by exhausting. resp.release_
  - [encode__httpcore] Example that uses ConnectionPool(), ConnectionPool.close: http = httpcore.ConnectionPool() try:     ... finally:     http.close()
- **0.757**
  - [pallets__werkzeug] Example that uses Response.status, Response.status_code: response.status response.status = '404 Not Found' response.status_code response.status_code = 400 response.status
  - [psf__requests] Example that uses Response.raise_for_status, get: bad_r = requests.get('https://httpbin.org/status/404') bad_r.status_code bad_r.raise_for_status()
- **0.791**
  - [stub42__pytz] Example that uses FixedOffset.tzname, LocalTimezone.tzname, USTimeZone.tzname, UTC.tzname, timezone, DstTzInfo.tzname, StaticTzInfo.tzname: from pytz import timezone tz = timezone('America/St_Johns') normal = datetime(2009, 9, 1) tz.tzname(normal) tz.tzname(normal, is_dst=False) tz.tzname(normal, is
  - [dateutil__dateutil] Example that uses tzname, tzname, tzname, tzname, tzname, tzutc(): from datetime import * from dateutil.tz import * datetime.now() datetime.now(tzutc()) datetime.now(tzutc()).tzname()
- **0.763**
  - [psf__requests] Example that uses Request(), Session(), Request.prepare, Session.send: from requests import Request, Session  s = Session()  req = Request('POST', url, data=data, headers=headers) prepped = req.prepare()  # do something with prepped.body prepped.body = 'No, I want exactly this as the body.'  # do so
  - [requests__toolbelt] Example that uses HostHeaderSSLAdapter.send, BaseUrlSession.prepare_request, BaseUrlSession.request: from requests import Request from requests_toolbelt import sessions s = sessions.BaseUrlSession( request = Request(method='GET', url='sub-resource/') prepared_request = s.prepare_request(request) r =

### Similarity 0.70 to 0.75

- **0.732**
  - [huggingface__huggingface_hub] Example that uses AsyncInferenceClient(), AsyncInferenceClient.question_answering: from huggingface_hub import AsyncInferenceClient client = AsyncInferenceClient() await client.question_answering(question="What's my name?", context="My name is Clara and I live in Berkeley.")
  - [openai__openai-python] Example that uses AsyncOpenAI(), AsyncOpenAI.chat, OpenAI.chat, bedrock: from openai import AsyncOpenAI  client = AsyncOpenAI(provider=bedrock(endpoint="runtime", region="us-west-2", api_key=None)) completion = await client.chat.completions.create(     model="us.openai.gpt-5.6-sol",     messages=[{"
- **0.747**
  - [dateutil__dateutil] Example that uses parse, default_tzinfo, tzoffset(): from dateutil.tz import tzoffset from dateutil.parser import parse from dateutil.utils import default_tzinfo dflt_tz = tzoffset("EST", -18000) print(default_tzinfo(parse('2014-01-01 12:30 UTC'), dflt_tz)) print(default_tzinfo(parse('2014-01-01 12:
  - [stub42__pytz] Example that uses FixedOffset.utcoffset, LocalTimezone.utcoffset, USTimeZone.utcoffset, UTC.utcoffset, timezone, DstTzInfo.utcoffset, StaticTzInfo.utcoffset: from pytz import timezone tz = timezone('America/St_Johns') ambiguous = datetime(2009, 10, 31, 23, 30) str(tz.utcoffset(ambiguous, is_dst=Fals
- **0.701**
  - [encode__httpx] Example that uses ASGITransport(), AsyncClient(): # Instantiate a client that makes ASGI requests with a client IP of "1.2.3.4", # on port 123. transport = httpx.ASGITransport(app=app, client=("1.2.3.4", 123)) async with httpx.AsyncClient(transport=transport, base_url="http://testserver") as client:
  - [openai__openai-python] Example that uses AsyncOpenAI(), OpenAI(), DefaultAsyncHttpx2Client, DefaultHttpx2Client: import httpx2 from openai import OpenAI, AsyncOpenAI, DefaultHttpx2Client, DefaultAsyncHttpx2Client  proxy_client = OpenAI(http_client=DefaultHttpx2Client(proxy="http://proxy.example.com:8080"))  transport_clie
- **0.727**
  - [requests__requests-oauthlib] Example that uses OAuth2Session(), OAuth2Session.authorization_url, OAuth2Session.fetch_token: # Credentials you get from registering a new application client_id = '<the id you get from github>' client_secret = '<the secret you get from github>' # OAuth endpoints given in the GitHub API documentatio
  - [oauthlib__oauthlib] Example that uses WebApplicationClient(), WebApplicationClient.prepare_request_uri: from oauthlib.oauth2 import WebApplicationClient client = WebApplicationClient('your_id') client.prepare_request_uri('https://example.com') client.prepare_request_uri('https://example.com', redirect_uri='https://a.b/
- **0.736**
  - [python-attrs__attrs] Example that uses field, gt: @define class C:     x = field(validator=attrs.validators.gt(42)) C(43) C(42)
  - [pydantic__pydantic] Example that uses TypeAdapter(), Field, TypeAdapter.validate_python: from typing import Annotated  from pydantic import Field, TypeAdapter, ValidationError  PositiveInt = Annotated[int, Field(gt=0)]  # (1)!  ta = TypeAdapter(PositiveInt)  print(ta.validate_python(1)) #> 1  try:     ta.validate_pytho
- **0.711**
  - [openai__openai-python] Example that uses OpenAI(), AsyncOpenAI.responses, OpenAI.responses: from openai import OpenAI  client = OpenAI()  stream = client.responses.create(     model="gpt-5.5",     input="Write a one-sentence bedtime story about a unicorn.",     stream=True, )  for event in stream:     print(event)
  - [huggingface__huggingface_hub] Example that uses AsyncInferenceClient(), AsyncInferenceClient.text_to_image, InferenceClient.text_to_image: from huggingface_hub import AsyncInferenceClient client = AsyncInferenceClient() image = await client.text_to_image("An astronaut riding a horse on the moon.") image.save("astronaut.png") asy
- **0.718**
  - [huggingface__huggingface_hub] Example that uses AsyncInferenceClient(), AsyncInferenceClient.token_classification: from huggingface_hub import AsyncInferenceClient client = AsyncInferenceClient() await client.token_classification("My name is Sarah Jessica Parker but you can call me Jessica")
  - [openai__openai-python] Example that uses AsyncOpenAI(), bedrock: client = AsyncOpenAI(     provider=bedrock(         endpoint="runtime",         region="us-west-2",         token_provider=refresh_bedrock_token,     ) )
- **0.739**
  - [huggingface__huggingface_hub] Example that uses AsyncInferenceClient(), AsyncInferenceClient.health_check: from huggingface_hub import AsyncInferenceClient client = AsyncInferenceClient("https://jzgu0buei5.us-east-1.aws.endpoints.huggingface.cloud") await client.health_check()
  - [openai__openai-python] Example that uses AsyncOpenAI(), bedrock: client = AsyncOpenAI(     provider=bedrock(         endpoint="runtime",         region="us-west-2",         token_provider=refresh_bedrock_token,     ) )
- **0.725**
  - [prompt-toolkit__python-prompt-toolkit] Example that uses PromptSession(), PromptSession.prompt_async, patch_stdout: from prompt_toolkit import PromptSession from prompt_toolkit.patch_stdout import patch_stdout  async def my_coroutine():     session = PromptSession()     while True:         with patch_stdout():             result = await 
  - [modelcontextprotocol__python-sdk] Example that uses ClientSession(), ClientSession.get_prompt, ClientSession.initialize, ClientSession.list_prompts, stdio_client: import asyncio from mcp.client.session import ClientSession from mcp.client.stdio import StdioServerParameters, stdio_client   async def main():     async with stdio_clien
- **0.723**
  - [stub42__pytz] Example that uses UTC.localize, timezone, DstTzInfo.localize, StaticTzInfo.localize: from pytz import timezone fmt = '%Y-%m-%d %H:%M:%S %Z (%z)' amdam = timezone('Europe/Amsterdam') dt  = datetime(2004, 10, 31, 2, 0, 0) loc_dt1 = amdam.localize(dt, is_dst=True) loc_dt2 = amdam.localize(dt, is_dst=Fa
  - [dateutil__dateutil] Example that uses tzname, tzname, tzname, tzname, tzname, tzutc(): from datetime import * from dateutil.tz import * datetime.now() datetime.now(tzutc()) datetime.now(tzutc()).tzname()

### Similarity 0.60 to 0.70

- **0.686**
  - [huggingface__huggingface_hub] Example that uses AsyncInferenceClient(), AsyncInferenceClient.summarization: from huggingface_hub import AsyncInferenceClient client = AsyncInferenceClient() await client.summarization("The Eiffel tower...")
  - [openai__openai-python] Example that uses AsyncOpenAI.beta, AsyncOpenAI.vector_stores, AsyncOpenAI.videos, OpenAI.beta, OpenAI.vector_stores, OpenAI.videos: client.beta.threads.create_and_run_poll(...) client.beta.threads.runs.create_and_poll(...) client.beta.threads.runs.submit_tool_outputs_and_poll(...) client.vector_sto
- **0.626**
  - [openai__openai-python] Example that uses OpenAI(), k8s_service_account_token_provider: from openai import OpenAI from openai.auth import k8s_service_account_token_provider  client = OpenAI(     workload_identity={         "identity_provider_id": "idp-123",         "service_account_id": "sa-456",         "provider": k8s_se
  - [huggingface__huggingface_hub] Example that uses InferenceClient(), InferenceClient.chat_completion: from huggingface_hub import InferenceClient messages = [{"role": "user", "content": "What is the capital of France?"}] client = InferenceClient("meta-llama/Meta-Llama-3-8B-Instruct") client.chat_completion(messages, max_tokens=100
- **0.697**
  - [openai__openai-python] Example that uses OpenAI(), AsyncOpenAI.chat, AsyncOpenAI.completions, OpenAI.chat, OpenAI.completions: from openai import OpenAI  # Configure the default for all requests: client = OpenAI(     # default is 2     max_retries=0, )  # Or, configure per-request: client.with_options(max_retries=5).chat.
  - [huggingface__huggingface_hub] Example that uses AsyncInferenceClient(), AsyncInferenceClient.chat_completion: from huggingface_hub import AsyncInferenceClient messages = [{"role": "user", "content": "What is the capital of France?"}] client = AsyncInferenceClient("meta-llama/Meta-Llama-3-8B-Instruct") await client.chat_completio
- **0.69**
  - [requests__requests-oauthlib] Example that uses OAuth1Session(), OAuth1Session.fetch_request_token: request_token_url = 'https://api.twitter.com/oauth/request_token' # Using OAuth1Session oauth = OAuth1Session(client_key, client_secret=client_secret) fetch_response = oauth.fetch_request_token(request_token_url) resource_owner_ke
  - [oauthlib__oauthlib] Example that uses Client(), Client.sign: # OAuth 1 Clients raise a value error for the example below from oauthlib.oauth1 import Client client = Client('client-id') headers = {'Content-Type': 'application/x-www-form-urlencoded'} body = 'hello world' client.sign('https://foo.bar', headers=headers, bo
- **0.672**
  - [huggingface__huggingface_hub] Example that uses InferenceClient(), RepoCard.content: from huggingface_hub import InferenceClient client = InferenceClient("meta-llama/Meta-Llama-3-70B-Instruct") messages = [ response_format = { response = client.chat_completion( response.choices[0].message.content
  - [openai__openai-python] Example that uses OpenAI(), OpenAI.responses, vertex: from openai import OpenAI from openai.providers import vertex  client = OpenAI(provider=vertex(project="my-google-project", location="us-east5")) response = client.responses.create(model="your-enabled-model", input="Hello", store=False) print(res
- **0.633**
  - [openai__openai-python] Example that uses AsyncTranscriptGrouper(), AsyncTranscriptGrouper.push, TranscriptGrouper.push: from openai.lib.live import AsyncTranscriptGrouper  async with AsyncTranscriptGrouper() as transcript:     transcript.on("segment.updated", render_segment)     transcript.on("segment.closed", finalize_se
  - [huggingface__huggingface_hub] Example that uses AsyncInferenceClient(), AsyncInferenceClient.automatic_speech_recognition: from huggingface_hub import AsyncInferenceClient client = AsyncInferenceClient() await client.automatic_speech_recognition("hello_world.flac").text
- **0.691**
  - [pallets__werkzeug] Example that uses Response(), Response.data: from werkzeug.wrappers import Response response = Response("Hello World!") response.headers['content-type'] response.data response.headers['content-length'] = len(response.data)
  - [urllib3__urllib3] Example that uses BaseHTTPResponse.data, request: import urllib3 resp = urllib3.request("GET", "http://httpbin.org/robots.txt") resp.status resp.data
- **0.65**
  - [openai__openai-python] Example that uses AsyncOpenAI(), AsyncOpenAI.fine_tuning, OpenAI.fine_tuning: import asyncio from openai import AsyncOpenAI  client = AsyncOpenAI()   async def main() -> None:     all_jobs = []     # Iterate through items across all pages, issuing requests as needed.     async for job in client.fine
  - [huggingface__huggingface_hub] Example that uses AsyncInferenceClient(), AsyncInferenceClient.get_endpoint_info: from huggingface_hub import AsyncInferenceClient client = AsyncInferenceClient("meta-llama/Meta-Llama-3-70B-Instruct") await client.get_endpoint_info()
- **0.634**
  - [kludex__starlette] Example that uses Starlette(), Starlette.add_middleware: from starlette.applications import Starlette from starlette.middleware.base import BaseHTTPMiddleware   class CustomMiddleware(BaseHTTPMiddleware):     async def dispatch(self, request, call_next):         response = await call_next(request)  
  - [fastapi__fastapi] Example that uses FastAPI(), FastAPI.get, Header: from typing import Annotated  from fastapi import FastAPI, Header from pydantic import BaseModel  app = FastAPI()   class CommonHeaders(BaseModel):     host: str     save_data: bool     if_modified_since: str | None = None     traceparent: str | None
- **0.667**
  - [openai__openai-python] Example that uses OpenAI(), AsyncOpenAI.chat, AsyncOpenAI.with_raw_response, OpenAI.chat, OpenAI.with_raw_response: from openai import OpenAI  client = OpenAI() response = client.chat.completions.with_raw_response.create(     messages=[         {             "role": "user",             "content": "S
  - [huggingface__huggingface_hub] Example that uses AsyncInferenceClient(), AsyncInferenceClient.chat_completion: from huggingface_hub import AsyncInferenceClient messages = [{"role": "user", "content": "What is the capital of France?"}] client = AsyncInferenceClient("meta-llama/Meta-Llama-3-8B-Instruct") await client.chat_completio
