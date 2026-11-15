# Exercises from documentation examples

97 repositories. 2,989 examples in their documentation show a value; 1,523 of them are verified: run twice in the library's own environment and sandbox, a plain JSON value both times, and the value the documentation shows. 35 repositories have at least one.

| What happened to an example | Number |
| --- | --- |
| verified | 1,523 |
| the code raised an error (also: needs earlier context, the network or a file) | 922 |
| the result is an object, not a plain value | 321 |
| the result is not what the documentation shows | 161 |
| took longer than 5 s | 37 |
| two runs gave different results | 25 |

| Package | Examples that show a value | Verified | Error | Object | Differs | Not scanned or run because |
| --- | --- | --- | --- | --- | --- | --- |
| `more-itertools` | 383 | 342 | 1 | 6 | 34 |  |
| `networkx` | 400 | 259 | 63 | 71 | 7 |  |
| `packaging` | 302 | 222 | 32 | 48 | 0 |  |
| `python-dateutil` | 236 | 175 | 12 | 12 | 37 |  |
| `pip` | 252 | 145 | 79 | 26 | 2 |  |
| `importlib-metadata` | 89 | 71 | 2 | 11 | 5 |  |
| `werkzeug` | 70 | 45 | 14 | 9 | 2 |  |
| `rsa` | 56 | 45 | 0 | 11 | 0 |  |
| `zipp` | 37 | 34 | 0 | 3 | 0 |  |
| `mcp` | 24 | 24 | 0 | 0 | 0 |  |
| `pytz` | 103 | 23 | 78 | 2 | 0 |  |
| `jinja2` | 31 | 22 | 8 | 1 | 0 |  |
| `attrs` | 90 | 21 | 17 | 40 | 12 |  |
| `huggingface-hub` | 400 | 13 | 347 | 15 | 25 |  |
| `pyparsing` | 89 | 12 | 40 | 34 | 3 |  |
| `requests` | 43 | 9 | 30 | 4 | 0 |  |
| `tomlkit` | 22 | 9 | 1 | 10 | 2 |  |
| `fsspec` | 17 | 7 | 5 | 3 | 2 |  |
| `urllib3` | 12 | 5 | 6 | 0 | 1 |  |
| `wheel` | 5 | 5 | 0 | 0 | 0 |  |
| `pyjwt` | 6 | 4 | 2 | 0 | 0 |  |
| `trove-classifiers` | 5 | 4 | 0 | 0 | 1 |  |
| `typing-extensions` | 9 | 3 | 5 | 0 | 1 |  |
| `typing-inspection` | 21 | 3 | 9 | 6 | 3 |  |
| `docstring-parser` | 11 | 3 | 2 | 1 | 5 |  |
| `distlib` | 32 | 3 | 21 | 1 | 7 |  |
| `requests-toolbelt` | 7 | 3 | 3 | 0 | 1 |  |
| `pydantic` | 2 | 2 | 0 | 0 | 0 |  |
| `jmespath` | 2 | 2 | 0 | 0 | 0 |  |
| `fastapi` | 3 | 2 | 0 | 1 | 0 |  |
| `pyasn1` | 15 | 2 | 13 | 0 | 0 |  |
| `pytest` | 14 | 1 | 12 | 0 | 1 |  |
| `jsonschema` | 14 | 1 | 13 | 0 | 0 |  |
| `tqdm` | 3 | 1 | 2 | 0 | 0 |  |
| `oauthlib` | 32 | 1 | 15 | 1 | 15 |  |
| `boto3` | 7 | 0 | 7 | 0 | 0 |  |
| `certifi` | 1 | 0 | 0 | 0 | 1 |  |
| `idna` | 5 | 0 | 3 | 1 | 1 |  |
| `pluggy` | 0 | 0 | 0 | 0 | 0 |  |
| `pycparser` | 0 | 0 | 0 | 0 | 0 |  |
| `six` | 0 | 0 | 0 | 0 | 0 |  |
| `setuptools` | 0 | 0 | 0 | 0 | 0 | RuntimeError: the package has compiled code |
| `click` | 1 | 0 | 1 | 0 | 0 |  |
| `anyio` | 0 | 0 | 0 | 0 | 0 |  |
| `annotated-types` | 1 | 0 | 0 | 1 | 0 |  |
| `iniconfig` | 7 | 0 | 7 | 0 | 0 |  |
| `h11` | 0 | 0 | 0 | 0 | 0 |  |
| `httpx` | 40 | 0 | 39 | 1 | 0 |  |
| `httpcore` | 7 | 0 | 7 | 0 | 0 |  |
| `s3transfer` | 0 | 0 | 0 | 0 | 0 |  |
| `python-dotenv` | 0 | 0 | 0 | 0 | 0 |  |
| `aiobotocore` | 0 | 0 | 0 | 0 | 0 |  |
| `starlette` | 6 | 0 | 6 | 0 | 0 |  |
| `platformdirs` | 14 | 0 | 13 | 0 | 1 |  |
| `uvicorn` | 0 | 0 | 0 | 0 | 0 |  |
| `pathspec` | 0 | 0 | 0 | 0 | 0 |  |
| `filelock` | 0 | 0 | 0 | 0 | 0 |  |
| `tzdata` | 0 | 0 | 0 | 0 | 0 |  |
| `referencing` | 0 | 0 | 0 | 0 | 0 |  |
| `jsonschema-specifications` | 0 | 0 | 0 | 0 | 0 |  |
| `markdown-it-py` | 1 | 0 | 1 | 0 | 0 |  |
| `rich` | 8 | 0 | 3 | 0 | 5 |  |
| `mdurl` | 0 | 0 | 0 | 0 | 0 |  |
| `annotated-doc` | 0 | 0 | 0 | 0 | 0 |  |
| `aiosignal` | 0 | 0 | 0 | 0 | 0 |  |
| `aiohappyeyeballs` | 0 | 0 | 0 | 0 | 0 |  |
| `sniffio` | 0 | 0 | 0 | 0 | 0 |  |
| `pydantic-settings` | 0 | 0 | 0 | 0 | 0 |  |
| `python-multipart` | 0 | 0 | 0 | 0 | 0 |  |
| `tenacity` | 0 | 0 | 0 | 0 | 0 |  |
| `pyasn1-modules` | 0 | 0 | 0 | 0 | 0 |  |
| `hatchling` | 0 | 0 | 0 | 0 | 0 |  |
| `truststore` | 0 | 0 | 0 | 0 | 0 |  |
| `openai` | 0 | 0 | 0 | 0 | 0 |  |
| `soupsieve` | 2 | 0 | 2 | 0 | 0 |  |
| `distro` | 3 | 0 | 0 | 0 | 3 |  |
| `shellingham` | 1 | 0 | 1 | 0 | 0 |  |
| `sse-starlette` | 0 | 0 | 0 | 0 | 0 |  |
| `s3fs` | 10 | 0 | 10 | 0 | 0 |  |
| `mypy-extensions` | 0 | 0 | 0 | 0 | 0 |  |
| `typer` | 0 | 0 | 0 | 0 | 0 |  |
| `colorama` | 0 | 0 | 0 | 0 | 0 |  |
| `dnspython` | 0 | 0 | 0 | 0 | 0 |  |
| `requests-oauthlib` | 13 | 0 | 12 | 0 | 1 |  |
| `pytest-asyncio` | 0 | 0 | 0 | 0 | 0 |  |
| `cachetools` | 12 | 0 | 12 | 0 | 0 |  |
| `editables` | 0 | 0 | 0 | 0 | 0 |  |
| `defusedxml` | 1 | 0 | 1 | 0 | 0 |  |
| `pytest-cov` | 0 | 0 | 0 | 0 | 0 |  |
| `exceptiongroup` | 0 | 0 | 0 | 0 | 0 |  |
| `itsdangerous` | 0 | 0 | 0 | 0 | 0 |  |
| `mako` | 1 | 0 | 0 | 1 | 0 |  |
| `alembic` | 1 | 0 | 1 | 0 | 0 |  |
| `prompt-toolkit` | 0 | 0 | 0 | 0 | 0 |  |
| `cloudpickle` | 4 | 0 | 1 | 1 | 2 |  |
| `threadpoolctl` | 6 | 0 | 0 | 0 | 6 |  |
| `isodate` | 0 | 0 | 0 | 0 | 0 |  |
