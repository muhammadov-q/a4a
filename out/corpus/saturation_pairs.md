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
  - [pypa__setuptools] WheelFile.close() -> None
  - [pypa__wheel] WheelFile.close() -> None
- **0.958**
  - [pyparsing__pyparsing] Or: symmetric difference of two of them (^)
  - [rthalley__dnspython] Set: symmetric difference of two of them (^)
- **1.0**
  - [fastapi__typer] Command.get_help_option_names(ctx: Context) -> list[str]: Returns the names for the help option.
  - [pallets__click] Command.get_help_option_names(ctx: Context) -> list[str]: Returns the names for the help option.
- **0.99**
  - [fastapi__typer] Command.invoke(ctx: Context) -> Any: Given a context, this invokes the attached callback (if it exists) in the right way.
  - [pallets__click] Command.invoke(ctx: Context) -> t.Any: Given a context, this invokes the attached callback (if it exists) in the right way.
- **1.0**
  - [aio-libs__aiobotocore] with_current_context(hook)
  - [boto__boto3] with_current_context(hook)
- **0.993**
  - [pallets__click] Command.get_params(ctx: Context) -> list[Parameter]
  - [fastapi__typer] Command.get_params(ctx: Context) -> list['Parameter']
- **1.0**
  - [pypa__wheel] WheelFile.writestr(zinfo_or_arcname: str | ZipInfo, data: SizedBuffer | str, compress_type: int | None) -> None
  - [pypa__setuptools] WheelFile.writestr(zinfo_or_arcname: str | ZipInfo, data: SizedBuffer | str, compress_type: int | None) -> None
- **1.0**
  - [pypa__wheel] WheelFile(file: StrPath, mode: Literal['r', 'w', 'x', 'a'], compression: int): build a WheelFile. A ZipFile derivative class that also reads SHA-256 hashes from .dist-info/RECORD and checks any read files against those.
  - [pypa__setuptools] WheelFile(file: StrPath, mode: Literal['r', 'w', 'x', 'a'], compression: int): build a WheelFile. A ZipFile derivative class that also reads SHA-256 hashes from .dist-info/RECORD and checks any read files against those.
- **0.988**
  - [pytest-dev__pytest-asyncio] pytest_configure(config: Config) -> None
  - [agronholm__anyio] pytest_configure(config: pytest.Config) -> None
- **1.0**
  - [fastapi__typer] getchar(echo: bool) -> str: Fetches a single character from the terminal and returns it.  This will always return a unicode character and under certain rare circumstances this might return more than one character.  The situations which more than one character is returned is when for whatever reason 
  - [pallets__click] getchar(echo: bool) -> str: Fetches a single character from the terminal and returns it.  This will always return a unicode character and under certain rare circumstances this might return more than one character.  The situations which more than one character is returned is when for whatever reason 

### Similarity 0.90 to 0.95

- **0.927**
  - [huggingface__huggingface_hub] InferenceClient.image_to_video(image: ContentT, model: str | None, prompt: str | None, negative_prompt: str | None, num_frames: float | None, num_inference_steps: int | None, guidance_scale: float | None, seed: int | None, target_size: ImageToVideoTargetSize | None, kwargs) -> bytes: Generate a vide
  - [openai__openai-python] AsyncVideos.create(prompt: str, input_reference: video_create_params.InputReference | Omit, model: VideoModelParam | Omit, seconds: VideoSeconds | Omit, size: VideoSize | Omit, extra_headers: Headers | None, extra_query: Query | None, extra_body: Body | None, timeout: float | httpx2.Timeout | None |
- **0.938**
  - [pyparsing__pyparsing] And: add two of them (+)
  - [rthalley__dnspython] Name: add two of them (+)
- **0.934**
  - [pallets__jinja] do_filesizeformat(value: str | float | int, binary: bool) -> str: Format the value like a 'human-readable' file size (i.e. 13 kB, 4.1 MB, 102 Bytes, etc).  Per default decimal prefixes are used (Mega, Giga, etc.), if the second parameter is set to `True` the binary prefixes are used (Mebi, Gibi).
  - [huggingface__huggingface_hub] format_size(size: int | float, human_readable: bool) -> str: Format a size in bytes.
- **0.934**
  - [dateutil__dateutil] tzfile.tzname(dt)
  - [stub42__pytz] USTimeZone.tzname(dt)
- **0.923**
  - [rthalley__dnspython] Message: compare two of them (smaller, equal, greater)
  - [textualize__rich] Text: compare two of them (smaller, equal, greater)
- **0.915**
  - [openai__openai-python] AsyncCompletions.messages() -> AsyncMessages: Given a list of messages comprising a conversation, the model will return a response.
  - [huggingface__huggingface_hub] InferenceClient.chat_completion(messages: list[dict | ChatCompletionInputMessage], model: str | None, stream: bool, frequency_penalty: float | None, logit_bias: list[float] | None, logprobs: bool | None, max_tokens: int | None, n: int | None, presence_penalty: float | None, response_format: ChatComp
- **0.913**
  - [pallets__werkzeug] MultiDict.poplist(key: K) -> list[V]: Pop the list for a key from the dict.  If the key is not in the dict an empty list is returned.
  - [kludex__starlette] MultiDict.poplist(key: Any) -> list[Any]
- **0.925**
  - [stub42__pytz] LocalTimezone.dst(dt)
  - [dateutil__dateutil] tzlocal.dst(dt)
- **0.906**
  - [kludex__starlette] MultiDict.setdefault(key: Any, default: Any) -> Any
  - [pallets__werkzeug] MultiDict.setdefault(key: K) -> None
- **0.9**
  - [openai__openai-python] AudioWithStreamingResponse.speech() -> SpeechWithStreamingResponse: Turn audio into text or text into audio.
  - [huggingface__huggingface_hub] InferenceClient.text_to_speech(text: str, model: str | None, do_sample: bool | None, early_stopping: Union[bool, 'TextToSpeechEarlyStoppingEnum'] | None, epsilon_cutoff: float | None, eta_cutoff: float | None, max_length: int | None, max_new_tokens: int | None, min_length: int | None, min_new_tokens

### Similarity 0.85 to 0.90

- **0.857**
  - [fastapi__fastapi] APIRoute.handle(scope: Scope, receive: Receive, send: Send) -> None
  - [kludex__starlette] Route.handle(scope: Scope, receive: Receive, send: Send) -> None
- **0.854**
  - [encode__httpcore] AsyncMockBackend.sleep(seconds: float) -> None
  - [agronholm__anyio] AsyncBackend.sleep(delay: float) -> None: Pause the current task for the specified duration.
- **0.893**
  - [huggingface__huggingface_hub] HfFileSystemStreamFile.seek(loc: int, whence: int)
  - [fsspec__filesystem_spec] AsyncStreamFile.seek(loc, whence)
- **0.86**
  - [kludex__starlette] Headers.keys() -> list[str]
  - [encode__httpx] Headers.keys() -> typing.KeysView[str]
- **0.852**
  - [openai__openai-python] AsyncStreamedBinaryAPIResponse.stream_to_file(file: str | os.PathLike[str], chunk_size: int | None) -> None: Streams the output to the given file.
  - [requests__toolbelt] stream_response_to_file(response, path, chunksize): Stream a response body to the specified file.
- **0.853**
  - [rthalley__dnspython] Parser(): build a Parser
  - [jmespath__jmespath.py] Parser(lookahead): build a Parser
- **0.855**
  - [pydantic__pydantic] ByteSize.to(unit: str) -> float: Converts a byte size to another unit, including both byte and bit units.
  - [pallets__jinja] do_filesizeformat(value: str | float | int, binary: bool) -> str: Format the value like a 'human-readable' file size (i.e. 13 kB, 4.1 MB, 102 Bytes, etc).  Per default decimal prefixes are used (Mega, Giga, etc.), if the second parameter is set to `True` the binary prefixes are used (Mebi, Gibi).
- **0.878**
  - [psf__requests] RequestsCookieJar.get(name: str, default: str | None, domain: str | None, path: str | None) -> str | None: Dict-like get() that also supports optional domain and path args in order to resolve naming collisions from using one cookie jar over multiple domains.
  - [encode__httpx] Cookies.get(name: str, default: str | None, domain: str | None, path: str | None) -> str | None: Get a cookie by name. May optionally include domain and path in order to specify exactly which cookie to retrieve.
- **0.862**
  - [kludex__starlette] HTTPConnection: read its properties: app, url, base_url, headers, query_params, path_params, cookies, client, session, auth, user, state
  - [urllib3__urllib3] HTTPConnection: read its properties: host, is_closed, is_connected, has_connected_to_proxy, proxy_is_forwarding, proxy_is_tunneling
- **0.872**
  - [psf__requests] options(url: _t.UriType, kwargs: Unpack[_t.RequestKwargs]) -> Response: Sends an OPTIONS request.
  - [encode__httpx] options(url: URL | str, params: QueryParamTypes | None, headers: HeaderTypes | None, cookies: CookieTypes | None, auth: AuthTypes | None, proxy: ProxyTypes | None, follow_redirects: bool, verify: ssl.SSLContext | str | bool, timeout: TimeoutTypes, trust_env: bool) -> Response: Sends an `OPTIONS` req

### Similarity 0.80 to 0.85

- **0.816**
  - [openai__openai-python] AsyncOrganization.audit_logs() -> AsyncAuditLogs: List user actions and configuration changes within this organization.
  - [huggingface__huggingface_hub] HfApi.get_organization_overview(organization: str, token: bool | str | None) -> Organization: Get an overview of an organization on the Hub.
- **0.805**
  - [tox-dev__filelock] SoftReadWriteLock.get_lock(lock_file: str | os.PathLike[str], timeout: float, blocking: bool) -> SoftReadWriteLock: Return the singleton :class:`SoftReadWriteLock` for *lock_file*.
  - [huggingface__huggingface_hub] WeakFileLock(lock_file: str | Path, timeout: float | None) -> Generator[BaseFileLock, None, None]: A filelock with some custom logic.
- **0.821**
  - [openai__openai-python] Agents.create(model: str, compaction: Optional[agent_create_params.Compaction] | Omit, experimental: agent_create_params.Experimental | Omit, instructions: Optional[str] | Omit, metadata: Optional[Dict[str, str]] | Omit, multi_agent: Optional[MultiAgentConfigParam] | Omit, name: Optional[str] | Omit
  - [huggingface__huggingface_hub] Agent(model: Optional[str], servers: Iterable[ServerConfig], provider: Optional[PROVIDER_OR_POLICY_T], base_url: Optional[str], api_key: Optional[str], prompt: Optional[str]): build a Agent. Implementation of a Simple Agent, which is a simple while loop built right on top of an [`MCPClient`].
- **0.8**
  - [prompt-toolkit__python-prompt-toolkit] Buffer.open_in_editor(validate_and_handle: bool) -> asyncio.Task[None]: Open code in editor.
  - [sqlalchemy__alembic] open_in_editor(filename: str, environ: dict[str, str] | None) -> None: Opens the given file in a text editor. If the environment variable ``EDITOR`` is set, this is taken as preference.
- **0.816**
  - [kludex__starlette] Starlette.add_exception_handler(exc_class_or_status_code: int | type[Exception], handler: ExceptionHandler) -> None
  - [fastapi__fastapi] FastAPI.exception_handler(exc_class_or_status_code: Annotated[int | type[Exception], Doc('\n                The Exception class this would handle, or a status code.\n                ')]) -> Callable[[DecoratedCallable], DecoratedCallable]: Add an exception handler to the app.
- **0.843**
  - [sqlalchemy__mako] LoopContext.cycle(values): Cycle through values as the loop progresses.
  - [pallets__jinja] LoopContext.cycle(args: V) -> V: Return a value from the given args, cycling through based on the current :attr:`index0`.
- **0.818**
  - [encode__httpx] ASGITransport.handle_async_request(request: Request) -> Response
  - [encode__httpcore] AsyncHTTPConnection.handle_async_request(request: Request) -> Response
- **0.846**
  - [rthalley__dnspython] PublicRSA(): build a PublicRSA
  - [sybrenstuvel__python-rsa] PublicKey(): build a PublicKey. Represents a public RSA key.
- **0.847**
  - [kludex__uvicorn] is_dir(path: Path) -> bool
  - [fsspec__filesystem_spec] DirFileSystem.isdir(path)
- **0.823**
  - [textualize__rich] NullFile.seekable() -> bool
  - [fsspec__filesystem_spec] AbstractBufferedFile.seekable(): Whether is seekable (only in read mode)

### Similarity 0.75 to 0.80

- **0.784**
  - [pypa__packaging] normalize_pre(letter: str) -> str: Normalize the pre-release segment of a version string.
  - [pypa__distlib] normalize_name(name): Normalize a python package name a la PEP 503
- **0.795**
  - [huggingface__huggingface_hub] SandboxPool.close() -> None: Release the pool. Idempotent.
  - [encode__httpcore] ConnectionPool.close() -> None
- **0.788**
  - [pyasn1__pyasn1] NamedTypes(namedTypes, kwargs): build a NamedTypes. Create a collection of named fields for a constructed ASN.1 type.
  - [python__typing_extensions] NamedTuple(typename, fields, kwargs): Typed version of namedtuple.
- **0.775**
  - [tqdm__tqdm] DiscordIO.delete(): Deletes internal `message_id`.
  - [openai__openai-python] AsyncMessages.delete(message_id: str, thread_id: str, extra_headers: Headers | None, extra_query: Query | None, extra_body: Body | None, timeout: float | httpx2.Timeout | None | NotGiven) -> MessageDeleted: Deletes a message.
- **0.799**
  - [openai__openai-python] Conversations.create(items: Optional[Iterable[ResponseInputItemParam]] | Omit, metadata: Optional[Metadata] | Omit, extra_headers: Headers | None, extra_query: Query | None, extra_body: Body | None, timeout: float | httpx2.Timeout | None | NotGiven) -> Conversation: Create a conversation.
  - [huggingface__huggingface_hub] InferenceClient.chat_completion(messages: list[dict | ChatCompletionInputMessage], model: str | None, stream: bool, frequency_penalty: float | None, logit_bias: list[float] | None, logprobs: bool | None, max_tokens: int | None, n: int | None, presence_penalty: float | None, response_format: ChatComp
- **0.769**
  - [modelcontextprotocol__python-sdk] StreamableHTTPServerTransport.connect() -> AsyncGenerator[tuple[ReadStream[SessionMessage | Exception], WriteStream[SessionMessage]], None]: Context manager that provides read and write streams for a connection.
  - [rthalley__dnspython] AsyncQuicConnection.make_stream() -> Any
- **0.796**
  - [pallets__werkzeug] MultiDict.values() -> cabc.Iterable[V]: Returns an iterator of the first value on every key's value list.
  - [kludex__starlette] ImmutableMultiDict.values() -> ValuesView[_CovariantValueType]
- **0.771**
  - [pydantic__pydantic] GenerateJsonSchema.get_default_value(schema: core_schema.WithDefaultSchema) -> Any: Get the default value to be used when generating a JSON Schema for a core schema with a default.
  - [modelcontextprotocol__python-sdk] UntitledJsonSchema(): build a UntitledJsonSchema. A JSON schema generator that leaves out the titles pydantic derives from field names.
- **0.754**
  - [psf__requests] PreparedRequest.prepare(method: str | None, url: _t.UriType | None, headers: Mapping[str, str | bytes] | None, files: _t.FilesType, data: _t.DataType, params: _t.ParamsType, auth: _t.AuthType, cookies: RequestsCookieJar | CookieJar | dict[str, str] | None, hooks: _t.HooksInputType | None, json: _t.J
  - [requests__toolbelt] BaseUrlSession.prepare_request(request, args, kwargs): Prepare the request after generating the complete URL.
- **0.798**
  - [aio-libs__aiobotocore] AioRefreshableCredentials: compare two of them (smaller, equal, greater)
  - [modelcontextprotocol__python-sdk] OAuthToken: compare two of them (smaller, equal, greater)

### Similarity 0.70 to 0.75

- **0.73**
  - [boto__s3transfer] InterruptReader.close()
  - [pallets__werkzeug] InputStream.close() -> None
- **0.745**
  - [kludex__starlette] MultiPartParser.on_header_end() -> None
  - [kludex__uvicorn] HttpToolsProtocol.on_headers_complete() -> None
- **0.75**
  - [prompt-toolkit__python-prompt-toolkit] is_dumb_terminal(term: str | None) -> bool: True if this terminal type is considered "dumb".
  - [pallets__werkzeug] HTMLStringO.isatty() -> bool
- **0.749**
  - [pallets__click] HelpFormatter.section(name: str) -> cabc.Generator[None]: Helpful context manager that writes a paragraph, a heading, and the indents.
  - [textualize__rich] Table.add_section() -> None: Add a new section (draw a line after current row).
- **0.725**
  - [textualize__rich] Console.save_html(path: str | PathLike[str], theme: TerminalTheme | None, clear: bool, code_format: str, inline_styles: bool) -> None: Generate HTML from console contents and write to a file (requires record=True argument in constructor).
  - [prompt-toolkit__python-prompt-toolkit] HTML(value: str): build a HTML. HTML formatted text. Take something HTML-like, for use as a formatted string.
- **0.719**
  - [huggingface__huggingface_hub] HfApi.verify_repo_checksums(repo_id: str, repo_type: str | None, revision: str | None, local_dir: str | Path | None, cache_dir: str | Path | None, token: str | bool | None) -> FolderVerification: Verify local files for a repo against Hub checksums.
  - [sybrenstuvel__python-rsa] VerifyOperation.perform_operation(indata: bytes, pub_key: rsa.key.AbstractKey, cli_args: Indexable) -> None: Verifies files.
- **0.733**
  - [prompt-toolkit__python-prompt-toolkit] HighlightSelectionProcessor(): build a HighlightSelectionProcessor. Processor that highlights the selection in the document.
  - [textualize__rich] Highlighter(): build a Highlighter. Abstract base class for highlighters.
- **0.711**
  - [requests__toolbelt] urlencode(query, args, kwargs): Handle nested form-data queries and serialize them appropriately.
  - [pallets__jinja] do_urlencode(value: str | t.Mapping[str, t.Any] | t.Iterable[tuple[str, t.Any]]) -> str: Quote data for use in a URL path or query using UTF-8.
- **0.722**
  - [urllib3__urllib3] HTTPConnectionPool: test whether it contains a value
  - [pallets__werkzeug] MultiDict: test whether it contains a value
- **0.702**
  - [pypa__setuptools] alias.finalize_options() -> None
  - [pypa__wheel] bdist_wheel.finalize_options()

### Similarity 0.60 to 0.70

- **0.606**
  - [kludex__uvicorn] resolve_reload_patterns(patterns_list: list[str], directories_list: list[str]) -> tuple[list[str], list[Path]]
  - [pypa__setuptools] glob_relative(patterns: Iterable[str], root_dir: StrPath | None) -> list[str]: Expand the list of glob patterns, but preserving relative paths.
- **0.684**
  - [pallets__jinja] htmlsafe_json_dumps(obj: t.Any, dumps: t.Callable[..., str] | None, kwargs: t.Any) -> markupsafe.Markup: Serialize an object to a string of JSON with :func:`json.dumps`, then replace HTML-unsafe characters with Unicode escapes and mark the result safe with :class:`~markupsafe.Markup`.
  - [textualize__rich] JSON(json: str, indent: None | int | str, highlight: bool, skip_keys: bool, ensure_ascii: bool, check_circular: bool, allow_nan: bool, default: Callable[[Any], Any] | None, sort_keys: bool): build a JSON. A renderable which pretty prints JSON.
- **0.696**
  - [huggingface__huggingface_hub] app_callback(version: Annotated[bool | None, Option('-v', '--version', callback=_version_callback, is_eager=True, hidden=True)], skills: Annotated[bool, Option('--skills', callback=_skills_callback, is_eager=True, help='Print the `hf-cli` SKILL.md to stdout (alias for `hf skills preview`).')], insta
  - [fastapi__typer] callback(ctx: typer.Context, path_or_module: str, app: str, func: str, version: bool) -> None: Run Typer scripts with completion, without having to create a package.
- **0.651**
  - [networkx__networkx] is_planar(G): Returns True if and only if `G` is planar.
  - [sybrenstuvel__python-rsa] are_relatively_prime(a: int, b: int) -> bool: Returns True if a and b are relatively prime, and False if they are not.
- **0.65**
  - [rthalley__dnspython] NSEC3(rdclass, rdtype, algorithm, flags, iterations, salt, next, windows): build a NSEC3. NSEC3 record
  - [pallets__itsdangerous] Signer.get_signature(value: str | bytes) -> bytes: Returns the signature for the given value.
- **0.655**
  - [networkx__networkx] estrada_index(G): Returns the Estrada index of a the graph G.
  - [more-itertools__more-itertools] subfactorial(n): Number of permutations of *n* elements with no fixed points.
- **0.607**
  - [prompt-toolkit__python-prompt-toolkit] UIControl.create_content(width: int, height: int) -> UIContent: Generate the content for this user control.
  - [openai__openai-python] Content(): build a Content
- **0.673**
  - [modelcontextprotocol__python-sdk] Prompt.render(arguments: dict[str, Any] | None, context: Context[LifespanContextT, RequestT]) -> list[Message] | InputRequiredResult: Render the prompt with arguments.
  - [sqlalchemy__mako] Template.render_context(context, args, kwargs): Render this :class:`.Template` with the given context.
- **0.632**
  - [rthalley__dnspython] Node.is_immutable() -> bool
  - [networkx__networkx] is_frozen(G): Returns True if graph is frozen.
- **0.685**
  - [executablebooks__markdown-it-py] Ruler.getRules(chainName: str) -> list[RuleFuncTv]: Return array of active functions (rules) for given chain name. It analyzes rules configuration, compiles caches if not exists and returns result.
  - [pallets__jinja] compile_rules(environment: 'Environment') -> list[tuple[str, str]]: Compiles all the rules from the environment into a list of rules.

## high

### Similarity 0.95 to 1.00


### Similarity 0.90 to 0.95

- **0.929**
  - [psf__requests] Example that uses delete, head, options, put: r = requests.put('https://httpbin.org/put', data={'key': 'value'}) r = requests.delete('https://httpbin.org/delete') r = requests.head('https://httpbin.org/get') r = requests.options('https://httpbin.org/get')
  - [encode__httpx] Example that uses delete, head, options, put: r = httpx.put('https://httpbin.org/put', data={'key': 'value'}) r = httpx.delete('https://httpbin.org/delete') r = httpx.head('https://httpbin.org/get') r = httpx.options('https://httpbin.org/get')
- **0.929**
  - [encode__httpx] Example that uses delete, head, options, put: r = httpx.put('https://httpbin.org/put', data={'key': 'value'}) r = httpx.delete('https://httpbin.org/delete') r = httpx.head('https://httpbin.org/get') r = httpx.options('https://httpbin.org/get')
  - [psf__requests] Example that uses delete, head, options, put: r = requests.put('https://httpbin.org/put', data={'key': 'value'}) r = requests.delete('https://httpbin.org/delete') r = requests.head('https://httpbin.org/get') r = requests.options('https://httpbin.org/get')
- **0.901**
  - [psf__requests] Example that uses Response.raise_for_status, get: bad_r = requests.get('https://httpbin.org/status/404') bad_r.status_code bad_r.raise_for_status()
  - [encode__httpx] Example that uses Response.raise_for_status, get: not_found = httpx.get('https://httpbin.org/status/404') not_found.status_code not_found.raise_for_status()
- **0.901**
  - [encode__httpx] Example that uses Response.raise_for_status, get: not_found = httpx.get('https://httpbin.org/status/404') not_found.status_code not_found.raise_for_status()
  - [psf__requests] Example that uses Response.raise_for_status, get: bad_r = requests.get('https://httpbin.org/status/404') bad_r.status_code bad_r.raise_for_status()

### Similarity 0.85 to 0.90

- **0.859**
  - [encode__httpx] Example that uses Response.raise_for_status, Response.request, Response.url, get: response = httpx.get("https://www.example.com/") try:     response.raise_for_status() except httpx.HTTPStatusError as exc:     print(f"Error response {exc.response.status_code} while requesting {exc.request.url!r}.")
  - [psf__requests] Example that uses Response.raise_for_status, get: bad_r = requests.get('https://httpbin.org/status/404') bad_r.status_code bad_r.raise_for_status()
- **0.867**
  - [encode__httpx] Example that uses Response.text, post: files = {'upload-file': (None, 'text content', 'text/plain')} r = httpx.post("https://httpbin.org/post", files=files) print(r.text)
  - [psf__requests] Example that uses Response.text, Session.post: url = 'https://httpbin.org/post' multiple_files = [ r = requests.post(url, files=multiple_files) r.text
- **0.867**
  - [psf__requests] Example that uses Response.text, Session.post: url = 'https://httpbin.org/post' multiple_files = [ r = requests.post(url, files=multiple_files) r.text
  - [encode__httpx] Example that uses Response.text, post: files = {'upload-file': (None, 'text content', 'text/plain')} r = httpx.post("https://httpbin.org/post", files=files) print(r.text)

### Similarity 0.80 to 0.85

- **0.823**
  - [urllib3__urllib3] Example that uses BaseHTTPResponse.json, request: import urllib3 resp = urllib3.request("GET", "https://httpbin.org/anything")  print(resp.status)  # 200 print(resp.headers) # HTTPHeaderDict(...) print(resp.json())  # {"headers": {"Accept": "*/*", ...}, ...}
  - [psf__requests] Example that uses Response.json, Response.text, get: import requests r = requests.get('https://httpbin.org/basic-auth/user/pass', auth=('user', 'pass')) r.status_code r.headers['content-type'] r.encoding r.text r.json()
- **0.809**
  - [psf__requests] Example that uses Response.json, get: import requests r = requests.get('https://api.github.com/events') r.json()   # This *call* raises an exception if JSON decoding fails
  - [encode__httpx] Example that uses Response.json, get: r = httpx.get('https://api.github.com/events') r.json()
- **0.82**
  - [dateutil__dateutil] Example that uses tzname, tzname, tzname, tzname, tzname, tzoffset(): from datetime import * from dateutil.tz import * datetime.now(tzoffset("BRST", -10800)) datetime.now(tzoffset("BRST", -10800)).tzname() datetime.now(tzoffset("BRST", -10800)).astimezone(UTC)
  - [stub42__pytz] Example that uses FixedOffset(), FixedOffset.dst, FixedOffset.utcoffset: one = FixedOffset(-330) one str(one.utcoffset(datetime.datetime.now())) str(one.dst(datetime.datetime.now())) two = FixedOffset(1380) two str(two.utcoffset(datetime.datetime.now())) str(two.dst(datetime.datetime.now()))
- **0.831**
  - [encode__httpx] Example that uses Response.text, get: import httpx r = httpx.get('https://www.example.org/') r r.status_code r.headers['content-type'] r.text
  - [psf__requests] Example that uses Response.json, Response.text, get: import requests r = requests.get('https://httpbin.org/basic-auth/user/pass', auth=('user', 'pass')) r.status_code r.headers['content-type'] r.encoding r.text r.json()
- **0.815**
  - [encode__httpx] Example that uses Cookies(), Cookies.set, Response.json, get: cookies = httpx.Cookies() cookies.set('cookie_on_domain', 'hello, there!', domain='httpbin.org') cookies.set('cookie_off_domain', 'nope.', domain='example.org') r = httpx.get('http://httpbin.org/cookies', cookies=cookies) r.json()
  - [psf__requests] Example that uses RequestsCookieJar(), Response.text, RequestsCookieJar.set, get: jar = requests.cookies.RequestsCookieJar() jar.set('tasty_cookie', 'yum', domain='httpbin.org', path='/cookies') jar.set('gross_cookie', 'blech', domain='httpbin.org', path='/elsewhere') url = 'https://httpbin.org/cook
- **0.811**
  - [pallets__werkzeug] Example that uses Client(), Response(), Client.get, Request.application, Response.text, Response.status_code: from werkzeug import Request, Response, Client  @Request.application def app(request: Request) -> Response:     return Response("Hello, World!")  c = Client(app) r = c.get("/") assert r.stat
  - [encode__httpx] Example that uses Client(), WSGITransport(), Client.get, Response.text: from flask import Flask import httpx   app = Flask(__name__)  @app.route("/") def hello():     return "Hello World!"  transport = httpx.WSGITransport(app=app) with httpx.Client(transport=transport, base_url="http://testserver") 
- **0.811**
  - [encode__httpx] Example that uses Client(), WSGITransport(), Client.get, Response.text: from flask import Flask import httpx   app = Flask(__name__)  @app.route("/") def hello():     return "Hello World!"  transport = httpx.WSGITransport(app=app) with httpx.Client(transport=transport, base_url="http://testserver") 
  - [pallets__werkzeug] Example that uses Client(), Response(), Client.get, Request.application, Response.text, Response.status_code: from werkzeug import Request, Response, Client  @Request.application def app(request: Request) -> Response:     return Response("Hello, World!")  c = Client(app) r = c.get("/") assert r.stat
- **0.82**
  - [stub42__pytz] Example that uses FixedOffset(), FixedOffset.dst, FixedOffset.utcoffset: one = FixedOffset(-330) one str(one.utcoffset(datetime.datetime.now())) str(one.dst(datetime.datetime.now())) two = FixedOffset(1380) two str(two.utcoffset(datetime.datetime.now())) str(two.dst(datetime.datetime.now()))
  - [dateutil__dateutil] Example that uses tzname, tzname, tzname, tzname, tzname, tzoffset(): from datetime import * from dateutil.tz import * datetime.now(tzoffset("BRST", -10800)) datetime.now(tzoffset("BRST", -10800)).tzname() datetime.now(tzoffset("BRST", -10800)).astimezone(UTC)
- **0.815**
  - [psf__requests] Example that uses RequestsCookieJar(), Response.text, RequestsCookieJar.set, get: jar = requests.cookies.RequestsCookieJar() jar.set('tasty_cookie', 'yum', domain='httpbin.org', path='/cookies') jar.set('gross_cookie', 'blech', domain='httpbin.org', path='/elsewhere') url = 'https://httpbin.org/cook
  - [encode__httpx] Example that uses Cookies(), Cookies.set, Response.json, get: cookies = httpx.Cookies() cookies.set('cookie_on_domain', 'hello, there!', domain='httpbin.org') cookies.set('cookie_off_domain', 'nope.', domain='example.org') r = httpx.get('http://httpbin.org/cookies', cookies=cookies) r.json()
- **0.812**
  - [encode__httpcore] Example that uses Response.iter_stream, stream: import httpcore  with httpcore.stream('GET', 'https://example.com') as response:     for chunk in response.iter_stream():         print(f"Downloaded: {chunk}")
  - [urllib3__urllib3] Example that uses BaseHTTPResponse.release_conn, BaseHTTPResponse.stream, request: import urllib3  resp = urllib3.request(     "GET",     "https://httpbin.org/bytes/1024",     preload_content=False )  for chunk in resp.stream(32):     print(chunk)     # b"\x9e\xa97'\x8e\x1eT ....  resp.release_conn(

### Similarity 0.75 to 0.80

- **0.791**
  - [dateutil__dateutil] Example that uses tzname, tzname, tzname, tzname, tzname, tzutc(): from datetime import * from dateutil.tz import * datetime.now() datetime.now(tzutc()) datetime.now(tzutc()).tzname()
  - [stub42__pytz] Example that uses FixedOffset.tzname, LocalTimezone.tzname, USTimeZone.tzname, UTC.tzname, timezone, DstTzInfo.tzname, StaticTzInfo.tzname: from pytz import timezone tz = timezone('America/St_Johns') normal = datetime(2009, 9, 1) tz.tzname(normal) tz.tzname(normal, is_dst=False) tz.tzname(normal, is
- **0.762**
  - [oauthlib__oauthlib] Example that uses LegacyApplicationClient(), LegacyApplicationClient.prepare_request_body: from oauthlib.oauth2 import LegacyApplicationClient client = LegacyApplicationClient('your_id') client.prepare_request_body(username='foo', password='bar', scope=['hello', 'world'])
  - [requests__requests-oauthlib] Example that uses OAuth2Session(), OAuth2Session.fetch_token: from oauthlib.oauth2 import BackendApplicationClient from requests_oauthlib import OAuth2Session from requests.auth import HTTPBasicAuth auth = HTTPBasicAuth(client_id, client_secret) client = BackendApplicationClient(client_id=client_id)
- **0.757**
  - [pallets__werkzeug] Example that uses Response.status, Response.status_code: response.status response.status = '404 Not Found' response.status_code response.status_code = 400 response.status
  - [psf__requests] Example that uses Response.raise_for_status, get: bad_r = requests.get('https://httpbin.org/status/404') bad_r.status_code bad_r.raise_for_status()
- **0.785**
  - [huggingface__huggingface_hub] Example that uses AsyncInferenceClient(), AsyncInferenceClient.chat_completion: from huggingface_hub import AsyncInferenceClient messages = [{"role": "user", "content": "What is the capital of France?"}] client = AsyncInferenceClient("meta-llama/Meta-Llama-3-8B-Instruct") await client.chat_completio
  - [openai__openai-python] Example that uses AsyncOpenAI(), AsyncOpenAI.chat, OpenAI.chat, bedrock: from openai import AsyncOpenAI  client = AsyncOpenAI(provider=bedrock(endpoint="runtime", region="us-west-2", api_key=None)) completion = await client.chat.completions.create(     model="us.openai.gpt-5.6-sol",     messages=[{"
- **0.781**
  - [encode__httpx] Example that uses Response.json, Response.raise_for_status, get: r = httpx.get('...').raise_for_status() data = httpx.get('...').raise_for_status().json()
  - [psf__requests] Example that uses Response.raise_for_status, get: bad_r = requests.get('https://httpbin.org/status/404') bad_r.status_code bad_r.raise_for_status()
- **0.785**
  - [openai__openai-python] Example that uses AsyncOpenAI(), AsyncOpenAI.chat, OpenAI.chat, bedrock: from openai import AsyncOpenAI  client = AsyncOpenAI(provider=bedrock(endpoint="runtime", region="us-west-2", api_key=None)) completion = await client.chat.completions.create(     model="us.openai.gpt-5.6-sol",     messages=[{"
  - [huggingface__huggingface_hub] Example that uses AsyncInferenceClient(), AsyncInferenceClient.chat_completion: from huggingface_hub import AsyncInferenceClient messages = [{"role": "user", "content": "What is the capital of France?"}] client = AsyncInferenceClient("meta-llama/Meta-Llama-3-8B-Instruct") await client.chat_completio
- **0.767**
  - [requests__requests-oauthlib] Example that uses OAuth2Session(), OAuth2Session.authorization_url, OAuth2Session.token_from_fragment: import requests from requests_oauthlib import OAuth2Session from oauthlib.oauth2 import MobileApplicationClient client_id = "<your client ID here>" scope = ["activity", "heartrate", "location", "nu
  - [oauthlib__oauthlib] Example that uses MobileApplicationClient(), MobileApplicationClient.prepare_request_uri: from oauthlib.oauth2 import MobileApplicationClient client = MobileApplicationClient('your_id') client.prepare_request_uri('https://example.com') client.prepare_request_uri('https://example.com', redirect_uri='
- **0.768**
  - [textualize__rich] Example that uses Progress(), Progress.get_default_columns: progress = Progress(     SpinnerColumn(),     *Progress.get_default_columns(),     TimeElapsedColumn(), )
  - [prompt-toolkit__python-prompt-toolkit] Example that uses Bar(), Label(), Percentage(), Progress(), Text(), TimeLeft(): from prompt_toolkit.shortcuts.progress_bar.formatters import *  default_formatting = [     Label(),     Text(' '),     Percentage(),     Text(' '),     Bar(),     Text(' '),     Progress(),     Text(' '),     Text('eta [
- **0.787**
  - [textualize__rich] Example that uses Progress(), Progress.add_task, Progress.finished, Progress.update: import time  from rich.progress import Progress  with Progress() as progress:      task1 = progress.add_task("[red]Downloading...", total=1000)     task2 = progress.add_task("[green]Processing...", total=1000)     t
  - [tqdm__tqdm] Example that uses tqdm(), update: with tqdm(total=100) as pbar:     for i in range(10):         sleep(0.1)         pbar.update(10)
- **0.762**
  - [fsspec__s3fs] Example that uses S3FileSystem(), S3FileSystem.set_session: s3 = S3FileSystem(profile="<profile name>")  # doctest: +SKIP await s3.set_session()  # doctest: +SKIP s3.connect(refresh=True)  # doctest: +SKIP
  - [boto__boto3] Example that uses Session(), Session.client: import boto3  session = boto3.Session(profile_name='my-sso-profile') s3_client = session.client('s3')

### Similarity 0.70 to 0.75

- **0.718**
  - [stub42__pytz] Example that uses UTC.localize, UTC.normalize, timezone, DstTzInfo.localize, DstTzInfo.normalize, StaticTzInfo.localize, StaticTzInfo.normalize: la = timezone('America/Los_Angeles') dt = la.localize(datetime(2011, 5, 7, 1, 2, 3)) fmt = '%Y-%m-%d %H:%M:%S %Z (%z)' gmt.normalize(dt).strftime(fmt)
  - [dateutil__dateutil] Example that uses tzname, tzname, tzname, tzname, tzname, tzutc(): from datetime import * from dateutil.tz import * datetime.now() datetime.now(tzutc()) datetime.now(tzutc()).tzname()
- **0.72**
  - [openai__openai-python] Example that uses AsyncOpenAI(), OpenAI(), DefaultAsyncHttpx2Client, DefaultHttpx2Client: import httpx2 from openai import OpenAI, AsyncOpenAI, DefaultHttpx2Client, DefaultAsyncHttpx2Client  proxy_client = OpenAI(http_client=DefaultHttpx2Client(proxy="http://proxy.example.com:8080"))  transport_clie
  - [encode__httpx] Example that uses AsyncClient(), AsyncHTTPTransport(): import httpx transport = httpx.AsyncHTTPTransport(retries=1) async with httpx.AsyncClient(transport=transport) as client:     ...
- **0.735**
  - [stub42__pytz] Example that uses FixedOffset.dst, LocalTimezone.dst, USTimeZone.dst, UTC.dst, timezone, DstTzInfo.dst, StaticTzInfo.dst: from pytz import timezone tz = timezone('America/St_Johns') normal = datetime(2009, 9, 1) str(tz.dst(normal)) str(tz.dst(normal, is_dst=False)) str(tz.dst(normal, is_dst=True)) a
  - [dateutil__dateutil] Example that uses resolve_imaginary, gettz: from dateutil import tz from datetime import datetime NYC = tz.gettz('America/New_York') print(tz.resolve_imaginary(datetime(2017, 3, 12, 2, 30, tzinfo=NYC))) KIR = tz.gettz('Pacific/Kiritimati') print(tz.resolve_imaginary(datetime(1995, 1, 1, 12, 30, tzin
- **0.736**
  - [pydantic__pydantic] Example that uses TypeAdapter(), Field, TypeAdapter.validate_python: from typing import Annotated  from pydantic import Field, TypeAdapter, ValidationError  PositiveInt = Annotated[int, Field(gt=0)]  # (1)!  ta = TypeAdapter(PositiveInt)  print(ta.validate_python(1)) #> 1  try:     ta.validate_pytho
  - [python-attrs__attrs] Example that uses field, gt: @define class C:     x = field(validator=attrs.validators.gt(42)) C(43) C(42)
- **0.737**
  - [stub42__pytz] Example that uses UTC.normalize, timezone, DstTzInfo.normalize, StaticTzInfo.normalize: from datetime import datetime, timedelta utc = timezone('UTC') eastern = timezone('US/Eastern') eastern.zone timezone(unicode('US/Eastern')) is eastern utc_dt = datetime(2002, 10, 27, 6, 0, 0, tzinfo=utc) loc_dt 
  - [dateutil__dateutil] Example that uses tzname, tzname, tzname, tzname, tzname, tzoffset(): from datetime import * from dateutil.tz import * datetime.now(tzoffset("BRST", -10800)) datetime.now(tzoffset("BRST", -10800)).tzname() datetime.now(tzoffset("BRST", -10800)).astimezone(UTC)
- **0.75**
  - [pallets__werkzeug] Example that uses Response(), Request.application: from werkzeug import Request, Response from werkzeug.exceptions import NotFound  @Request.application def app(request: Request) -> Response:     if request.path != "/":         raise NotFound()      return Response("Hello, World!")
  - [kludex__starlette] Example that uses Request(), Response(), Request.method: from starlette.requests import Request from starlette.responses import Response   async def app(scope, receive, send):     assert scope['type'] == 'http'     request = Request(scope, receive)     content = '%s %s' % (request.method, request.ur
- **0.75**
  - [kludex__starlette] Example that uses Request(), Response(), Request.method: from starlette.requests import Request from starlette.responses import Response   async def app(scope, receive, send):     assert scope['type'] == 'http'     request = Request(scope, receive)     content = '%s %s' % (request.method, request.ur
  - [pallets__werkzeug] Example that uses Response(), Request.application: from werkzeug import Request, Response from werkzeug.exceptions import NotFound  @Request.application def app(request: Request) -> Response:     if request.path != "/":         raise NotFound()      return Response("Hello, World!")
- **0.71**
  - [huggingface__huggingface_hub] Example that uses InferenceClient(), InferenceClient.chat_completion: from huggingface_hub import InferenceClient messages = [{"role": "user", "content": "What is the capital of France?"}] client = InferenceClient("meta-llama/Meta-Llama-3-8B-Instruct") client.chat_completion(messages, max_tokens=100
  - [openai__openai-python] Example that uses OpenAI(), OpenAI.chat, bedrock: from openai import OpenAI from openai.providers import bedrock  client = OpenAI(     provider=bedrock(         endpoint="runtime",         region="us-west-2",         api_key=None,     ) )  completion = client.chat.completions.create(     model="us.o
- **0.706**
  - [encode__httpx] Example that uses AsyncClient.get, Client.get, Cookies.get, Headers.get, QueryParams.get: client = httpx.Client() response = client.get('https://example.org')
  - [psf__requests] Example that uses Session(), Session.get: s = requests.Session()    # formerly, session took parameters s.auth = auth s.headers.update(headers) r = s.get('https://httpbin.org/headers')
- **0.715**
  - [openai__openai-python] Example that uses AsyncOpenAI.chat, OpenAI.chat: import openai  try:     completion = await client.chat.completions.create(         messages=[{"role": "user", "content": "Say this is a test"}], model="gpt-5.5"     ) except openai.APIStatusError as exc:     print(exc.request_id)  # req_123     raise 
  - [huggingface__huggingface_hub] Example that uses AsyncInferenceClient(), AsyncInferenceClient.chat_completion: from huggingface_hub import AsyncInferenceClient messages = [{"role": "user", "content": "What is the capital of France?"}] client = AsyncInferenceClient("meta-llama/Meta-Llama-3-8B-Instruct") await client.chat_completio

### Similarity 0.60 to 0.70

- **0.617**
  - [boto__boto3] Example that uses CollectionManager.all, ResourceCollection.all: bucket = s3.Bucket('boto3') for obj in bucket.objects.all():     print(obj.key)
  - [fsspec__s3fs] Example that uses S3FileSystem(), S3AsyncStreamedFile.read: s3 = S3FileSystem(anon=False)  # doctest: +SKIP s3.ls('my-bucket/')  # doctest: +SKIP with s3.open('my-bucket/my-file.txt', mode='rb') as f:  # doctest: +SKIP     print(f.read())  # doctest: +SKIP
- **0.61**
  - [modelcontextprotocol__python-sdk] Example that uses ClientSession.call_tool, MCPError.code, MCPServer.call_tool: from mcp.shared.exceptions import MCPError from mcp.types import REQUEST_TIMEOUT  # -32001  try:     result = await client.call_tool("slow_tool", {}) except MCPError as e:     if e.code == REQUEST_TIMEOUT:         ...  # 
  - [openai__openai-python] Example that uses AsyncOpenAI.beta, OpenAI.beta, AssistantEventHandler.until_done: def report_tool_error(failure):     logger.error(         "Tool %s failed during %s (call %s)",         failure.tool_name,         failure.stage,         failure.call_id,     )   with client.beta.agents.sessions.strea
- **0.677**
  - [dateutil__dateutil] Example that uses get, keys, tzical(): from dateutil.tz import *; from datetime import * tz = tzical('samples/EST5EDT.ics') tz.keys() est = tz.get('US-Eastern') est datetime.now(est) est == tz.get()
  - [stub42__pytz] Example that uses FixedOffset.dst, LocalTimezone.dst, USTimeZone.dst, UTC.dst, timezone, DstTzInfo.dst, StaticTzInfo.dst: from pytz import timezone tz = timezone('America/St_Johns') normal = datetime(2009, 9, 1) str(tz.dst(normal)) str(tz.dst(normal, is_dst=False)) str(tz.dst(normal, is_dst=True)) a
- **0.697**
  - [textualize__rich] Example that uses Console(), Console.log, Console.status: from time import sleep from rich.console import Console  console = Console() tasks = [f"task {n}" for n in range(1, 11)]  with console.status("[bold green]Working on tasks...") as status:     while tasks:         task = tasks.pop(0)         s
  - [pallets__click] Example that uses echo, progressbar: import time  with click.progressbar([1, 2, 3]) as bar:     for x in bar:         click.echo(f"sleep({x})...")         time.sleep(x)
- **0.631**
  - [huggingface__huggingface_hub] Example that uses AsyncInferenceClient(), AsyncInferenceClient.image_to_image, RepoCard.save, ExtensionManifest.save: from huggingface_hub import AsyncInferenceClient client = AsyncInferenceClient() image = await client.image_to_image("cat.jpg", prompt="turn the cat into a tiger") image.save("tiger.
  - [openai__openai-python] Example that uses AsyncOpenAI(), bedrock: client = AsyncOpenAI(     provider=bedrock(         endpoint="runtime",         region="us-west-2",         token_provider=refresh_bedrock_token,     ) )
- **0.672**
  - [huggingface__huggingface_hub] Example that uses AsyncInferenceClient(), AsyncInferenceClient.text_classification: from huggingface_hub import AsyncInferenceClient client = AsyncInferenceClient() await client.text_classification("I like you")
  - [openai__openai-python] Example that uses AsyncOpenAI(), AsyncOpenAI.chat, OpenAI.chat, bedrock: from openai import AsyncOpenAI  client = AsyncOpenAI(provider=bedrock(endpoint="runtime", region="us-west-2", api_key=None)) completion = await client.chat.completions.create(     model="us.openai.gpt-5.6-sol",     messages=[{"
- **0.622**
  - [textualize__rich] Example that uses Console(), Console.log: from rich.console import Console console = Console()  test_data = [     {"jsonrpc": "2.0", "method": "sum", "params": [None, 1, 2, 4, False, True], "id": "1",},     {"jsonrpc": "2.0", "method": "notify_hello", "params": [7]},     {"jsonrpc": "2.0", "method":
  - [modelcontextprotocol__python-sdk] Example that uses Context.info, Context.log: # Before await ctx.info("Connection failed", extra={"host": "localhost", "port": 5432})  # extra= type-checked but raised TypeError at runtime in v1 await ctx.log(level="info", message="hello")  # After await ctx.info({"message": "Connection failed", "hos
- **0.671**
  - [huggingface__huggingface_hub] Example that uses AsyncInferenceClient(), AsyncInferenceClient.fill_mask: from huggingface_hub import AsyncInferenceClient client = AsyncInferenceClient() await client.fill_mask("The goal of life is <mask>.")
  - [openai__openai-python] Example that uses AsyncOpenAI(), bedrock: client = AsyncOpenAI(     provider=bedrock(         endpoint="runtime",         region="us-west-2",         token_provider=refresh_bedrock_token,     ) )
- **0.641**
  - [textualize__rich] Example that uses Console(), Console.print: from rich.console import Console from rich.markdown import Markdown  console = Console() with open("README.md") as readme:     markdown = Markdown(readme.read()) console.print(markdown)
  - [prompt-toolkit__python-prompt-toolkit] Example that uses HTML(), print_formatted_text: from prompt_toolkit import print_formatted_text, HTML  print_formatted_text(HTML('<b>This is bold</b>')) print_formatted_text(HTML('<i>This is italic</i>')) print_formatted_text(HTML('<u>This is underlined</u>'))
- **0.689**
  - [pallets__werkzeug] Example that uses Response(), Response.data: from werkzeug.wrappers import Response response = Response("Hello World!") response.headers['content-type'] response.data response.headers['content-length'] = len(response.data)
  - [urllib3__urllib3] Example that uses BaseHTTPResponse.data, request: import urllib3 resp = urllib3.request("GET", "http://httpbin.org/robots.txt") resp.status resp.data
