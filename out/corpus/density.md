# Density and coverage of verified exercises

97 scanned repositories. 35 give at least one verified exercise. Lines of text were counted in 97 clones; nothing was run.

## By kind of source

| Kind of source | Lines | Examples | Verified | Yield | Verified per 1,000 lines | Repositories with one or more | Median per 1,000 lines in those |
| --- | --- | --- | --- | --- | --- | --- | --- |
| Documentation files | 629,194 | 1,026 | 375 | 37% | 0.60 | 17 | 4.00 |
| Docstrings | 206,099 | 1,997 | 1,170 | 59% | 5.68 | 27 | 5.11 |
| All, against lines of code | 1,248,695 | | 1,545 | | 1.24 | 35 | 1.47 |

Yield is verified exercises out of the examples that could become one. An example counts for the kind of source it was found in. Left out, because the examples were not run: `setuptools` (RuntimeError: the package has compiled code).

At most 400 examples of a repository are read. At that limit, so with numbers that are a lower bound: `huggingface-hub`, `networkx`.

## Where the exercises are

| Repositories | Count |
| --- | --- |
| with no example that could become an exercise | 38 |
| with examples, none verified | 23 |
| with at least one verified exercise | 35 |

Share of all verified exercises held by the repositories with the most: top 1: 22%, top 3: 54%, top 5: 74%, top 10: 90%.

## Coverage of the public API

| | Count | Share of the public API |
| --- | --- | --- |
| Functions, methods and properties | 17,362 | |
| used somewhere in the repository's documentation | 2,150 | 12.4% |
| used by at least one verified exercise | 519 | 3.0% |
| Classes | 2,539 | |
| built by at least one verified exercise | 45 | 1.8% |

Median coverage per repository: 0.0% over all scanned repositories, 2.0% over those with a verified exercise.

456 of 1,545 verified exercises use no function, method or property that the scan can name (they build a class, use an operator, or call something the scan cannot resolve).
In the median repository with exercises, 47% of the exercises use the single most used element.

## Does size explain the number of exercises?

Spearman rank correlation with the number of verified exercises, over the repositories whose lines were counted:

| Measure of size | Correlation |
| --- | --- |
| Lines of code | 0.27 |
| Lines of documentation files | 0.29 |
| Lines of docstrings | 0.40 |
| Public API elements | 0.26 |

## Per repository

| Package | Lines of code | Doc lines | Docstring lines | Examples | Verified | From files | From docstrings | Per 1,000 lines of code | Questions | API | In docs | Covered | Coverage |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| `more-itertools` | 5,628 | 1,369 | 2,501 | 383 | 342 | 5 | 337 | 60.77 | 19 | 176 | 163 | 146 | 83.0% |
| `networkx` | 167,870 | 95,464 | 53,461 | 400 | 259 | 24 | 235 | 1.54 | 20 | 1180 | 779 | 175 | 14.8% |
| `packaging` | 11,316 | 4,275 | 2,030 | 311 | 231 | 91 | 140 | 20.41 | 28 | 99 | 71 | 54 | 54.5% |
| `python-dateutil` | 6,998 | 2,488 | 1,259 | 236 | 175 | 164 | 11 | 25.01 | 11 | 66 | 19 | 12 | 18.2% |
| `pip` | 132,808 | 13,643 | 13,187 | 251 | 144 | 0 | 144 | 1.08 | 0 | 1 | 0 | 0 | 0.0% |
| `importlib-metadata` | 2,016 | 1,047 | 733 | 89 | 71 | 0 | 71 | 35.22 | 4 | 54 | 8 | 8 | 14.8% |
| `rsa` | 2,241 | 787 | 604 | 56 | 45 | 1 | 44 | 20.08 | 17 | 44 | 16 | 11 | 25.0% |
| `werkzeug` | 19,082 | 5,578 | 4,503 | 70 | 44 | 30 | 14 | 2.31 | 16 | 436 | 43 | 14 | 3.2% |
| `pytz` | 2,262 | 541 | 391 | 128 | 36 | 17 | 19 | 15.92 | 2 | 34 | 25 | 3 | 8.8% |
| `zipp` | 539 | 375 | 202 | 39 | 36 | 0 | 36 | 66.79 | 3 | 31 | 11 | 10 | 32.3% |
| `mcp` | 24,148 | 73,098 | 4,701 | 24 | 24 | 0 | 24 | 0.99 | 15 | 513 | 56 | 7 | 1.4% |
| `jinja2` | 11,616 | 3,815 | 2,181 | 31 | 22 | 1 | 21 | 1.89 | 9 | 489 | 12 | 8 | 1.6% |
| `attrs` | 79 | 4,264 | 0 | 90 | 21 | 21 | 0 | 265.82 | 1 | 47 | 36 | 8 | 17.0% |
| `huggingface-hub` | 69,275 | 15,196 | 18,113 | 400 | 13 | 0 | 13 | 0.19 | 2 | 747 | 184 | 10 | 1.3% |
| `pyparsing` | 10,661 | 3,997 | 2,942 | 88 | 12 | 0 | 12 | 1.13 | 0 | 220 | 44 | 5 | 2.3% |
| `requests` | 5,186 | 3,960 | 979 | 43 | 9 | 0 | 9 | 1.74 | 4 | 165 | 28 | 4 | 2.4% |
| `tomlkit` | 5,230 | 750 | 332 | 22 | 9 | 3 | 6 | 1.72 | 0 | 183 | 36 | 27 | 14.8% |
| `fsspec` | 41,714 | 2,768 | 3,646 | 17 | 7 | 0 | 7 | 0.17 | 5 | 625 | 26 | 2 | 0.3% |
| `urllib3` | 10,262 | 3,574 | 1,598 | 12 | 5 | 0 | 5 | 0.49 | 0 | 239 | 17 | 2 | 0.8% |
| `wheel` | 2,168 | 949 | 144 | 5 | 5 | 0 | 5 | 2.31 | 0 | 27 | 0 | 0 | 0.0% |
| `pyjwt` | 2,712 | 1,891 | 317 | 6 | 4 | 4 | 0 | 1.47 | 0 | 81 | 2 | 0 | 0.0% |
| `trove-classifiers` | 929 | 73 | 0 | 5 | 4 | 4 | 0 | 4.31 | 0 | 0 | 0 | 0 | n/a |
| `distlib` | 9,268 | 5,290 | 979 | 32 | 3 | 3 | 0 | 0.32 | 3 | 286 | 32 | 1 | 0.3% |
| `docstring-parser` | 7,673 | 309 | 991 | 11 | 3 | 3 | 0 | 0.39 | 0 | 95 | 3 | 3 | 3.2% |
| `requests-toolbelt` | 2,797 | 1,226 | 1,011 | 7 | 3 | 0 | 3 | 1.07 | 0 | 74 | 13 | 0 | 0.0% |
| `typing-extensions` | 3,674 | 1,774 | 696 | 9 | 3 | 0 | 3 | 0.82 | 1 | 38 | 4 | 2 | 5.3% |
| `typing-inspection` | 1,000 | 404 | 166 | 21 | 3 | 0 | 3 | 3.00 | 0 | 7 | 4 | 3 | 42.9% |
| `fastapi` | 20,346 | 145,155 | 910 | 3 | 2 | 0 | 2 | 0.10 | 0 | 162 | 7 | 1 | 0.6% |
| `jmespath` | 1,422 | 259 | 28 | 2 | 2 | 2 | 0 | 1.41 | 2 | 60 | 3 | 1 | 1.7% |
| `pyasn1` | 8,852 | 4,934 | 2,064 | 15 | 2 | 0 | 2 | 0.23 | 1 | 177 | 0 | 0 | 0.0% |
| `pydantic` | 24,385 | 19,014 | 5,103 | 2 | 2 | 0 | 2 | 0.08 | 0 | 234 | 28 | 0 | 0.0% |
| `jsonschema` | 9,616 | 2,085 | 742 | 14 | 1 | 1 | 0 | 0.10 | 1 | 36 | 6 | 1 | 2.8% |
| `oauthlib` | 10,367 | 3,359 | 4,355 | 32 | 1 | 0 | 1 | 0.10 | 1 | 327 | 14 | 1 | 0.3% |
| `pytest` | 193 | 42,156 | 2 | 14 | 1 | 1 | 0 | 5.18 | 0 | 342 | 9 | 0 | 0.0% |
| `tqdm` | 4,025 | 2,646 | 773 | 3 | 1 | 0 | 1 | 0.25 | 0 | 109 | 17 | 0 | 0.0% |
| `aiobotocore` | 7,500 | 4,746 | 323 | 0 | 0 | 0 | 0 | 0.00 | n/a | 149 | 2 | 0 | 0.0% |
| `aiohappyeyeballs` | 476 | 410 | 86 | 0 | 0 | 0 | 0 | 0.00 | n/a | 4 | 0 | 0 | 0.0% |
| `aiosignal` | 43 | 649 | 6 | 0 | 0 | 0 | 0 | 0.00 | n/a | 1 | 0 | 0 | 0.0% |
| `alembic` | 24,225 | 485 | 3,761 | 1 | 0 | 0 | 0 | 0.00 | n/a | 510 | 1 | 0 | 0.0% |
| `annotated-doc` | 28 | 200 | 14 | 0 | 0 | 0 | 0 | 0.00 | n/a | 0 | 0 | 0 | n/a |
| `annotated-types` | 418 | 196 | 96 | 1 | 0 | 0 | 0 | 0.00 | n/a | 1 | 0 | 0 | 0.0% |
| `anyio` | 13,370 | 3,815 | 1,597 | 0 | 0 | 0 | 0 | 0.00 | n/a | 411 | 4 | 0 | 0.0% |
| `boto3` | 7,127 | 24,288 | 1,580 | 7 | 0 | 0 | 0 | 0.00 | n/a | 154 | 18 | 0 | 0.0% |
| `cachetools` | 1,274 | 1,539 | 81 | 12 | 0 | 0 | 0 | 0.00 | n/a | 35 | 2 | 0 | 0.0% |
| `certifi` | 93 | 30 | 3 | 1 | 0 | 0 | 0 | 0.00 | n/a | 3 | 1 | 0 | 0.0% |
| `click` | 10,398 | 6,744 | 2,364 | 1 | 0 | 0 | 0 | 0.00 | n/a | 240 | 18 | 0 | 0.0% |
| `cloudpickle` | 1,312 | 461 | 211 | 4 | 0 | 0 | 0 | 0.00 | n/a | 10 | 3 | 0 | 0.0% |
| `colorama` | 1,377 | 692 | 18 | 0 | 0 | 0 | 0 | 0.00 | n/a | 54 | 2 | 0 | 0.0% |
| `defusedxml` | 818 | 1,323 | 40 | 1 | 0 | 0 | 0 | 0.00 | n/a | 52 | 2 | 0 | 0.0% |
| `distro` | 1,269 | 692 | 448 | 3 | 0 | 0 | 0 | 0.00 | n/a | 40 | 3 | 0 | 0.0% |
| `dnspython` | 29,285 | 3,367 | 4,513 | 0 | 0 | 0 | 0 | 0.00 | n/a | 924 | 4 | 0 | 0.0% |
| `editables` | 151 | 487 | 0 | 0 | 0 | 0 | 0 | 0.00 | n/a | 16 | 3 | 0 | 0.0% |
| `exceptiongroup` | 996 | 259 | 10 | 0 | 0 | 0 | 0 | 0.00 | n/a | 11 | 2 | 0 | 0.0% |
| `filelock` | 11,196 | 5,176 | 780 | 0 | 0 | 0 | 0 | 0.00 | n/a | 82 | 30 | 0 | 0.0% |
| `h11` | 4,529 | 1,838 | 239 | 0 | 0 | 0 | 0 | 0.00 | n/a | 11 | 6 | 0 | 0.0% |
| `hatchling` | 12,834 | 5,684 | 574 | 0 | 0 | 0 | 0 | 0.00 | n/a | 605 | 0 | 0 | 0.0% |
| `httpcore` | 6,085 | 1,639 | 438 | 7 | 0 | 0 | 0 | 0.00 | n/a | 101 | 17 | 0 | 0.0% |
| `httpx` | 7,448 | 3,766 | 882 | 40 | 0 | 0 | 0 | 0.00 | n/a | 151 | 28 | 0 | 0.0% |
| `idna` | 20,191 | 931 | 249 | 5 | 0 | 0 | 0 | 0.00 | n/a | 29 | 2 | 0 | 0.0% |
| `iniconfig` | 376 | 45 | 40 | 7 | 0 | 0 | 0 | 0.00 | n/a | 4 | 2 | 0 | 0.0% |
| `isodate` | 1,184 | 203 | 245 | 0 | 0 | 0 | 0 | 0.00 | n/a | 26 | 0 | 0 | 0.0% |
| `itsdangerous` | 951 | 630 | 199 | 0 | 0 | 0 | 0 | 0.00 | n/a | 38 | 7 | 0 | 0.0% |
| `jsonschema-specifications` | 70 | 145 | 6 | 0 | 0 | 0 | 0 | 0.00 | n/a | 0 | 0 | 0 | n/a |
| `mako` | 7,024 | 154 | 823 | 1 | 0 | 0 | 0 | 0.00 | n/a | 191 | 0 | 0 | 0.0% |
| `markdown-it-py` | 6,082 | 9,202 | 482 | 1 | 0 | 0 | 0 | 0.00 | n/a | 193 | 8 | 0 | 0.0% |
| `mdurl` | 478 | 6 | 0 | 0 | 0 | 0 | 0 | 0.00 | n/a | 4 | 0 | 0 | 0.0% |
| `mypy-extensions` | 209 | 5 | 10 | 0 | 0 | 0 | 0 | 0.00 | n/a | 8 | 0 | 0 | 0.0% |
| `openai` | 192,425 | 8,846 | 27,767 | 0 | 0 | 0 | 0 | 0.00 | n/a | 2301 | 48 | 0 | 0.0% |
| `pathspec` | 4,710 | 1,705 | 940 | 0 | 0 | 0 | 0 | 0.00 | n/a | 46 | 5 | 0 | 0.0% |
| `platformdirs` | 3,175 | 3,321 | 696 | 14 | 0 | 0 | 0 | 0.00 | n/a | 237 | 13 | 0 | 0.0% |
| `pluggy` | 1,755 | 1,546 | 286 | 0 | 0 | 0 | 0 | 0.00 | n/a | 35 | 3 | 0 | 0.0% |
| `prompt-toolkit` | 34,386 | 3,935 | 4,301 | 0 | 0 | 0 | 0 | 0.00 | n/a | 964 | 35 | 0 | 0.0% |
| `pyasn1-modules` | 16,514 | 360 | 196 | 0 | 0 | 0 | 0 | 0.00 | n/a | 4 | 0 | 0 | 0.0% |
| `pycparser` | 5,882 | 287 | 317 | 0 | 0 | 0 | 0 | 0.00 | n/a | 131 | 2 | 0 | 0.0% |
| `pydantic-settings` | 5,956 | 2,778 | 599 | 0 | 0 | 0 | 0 | 0.00 | n/a | 56 | 15 | 0 | 0.0% |
| `pytest-asyncio` | 935 | 888 | 47 | 0 | 0 | 0 | 0 | 0.00 | n/a | 18 | 0 | 0 | 0.0% |
| `pytest-cov` | 815 | 1,117 | 42 | 0 | 0 | 0 | 0 | 0.00 | n/a | 38 | 0 | 0 | 0.0% |
| `python-dotenv` | 977 | 713 | 92 | 0 | 0 | 0 | 0 | 0.00 | n/a | 46 | 2 | 0 | 0.0% |
| `python-multipart` | 1,897 | 600 | 315 | 0 | 0 | 0 | 0 | 0.00 | n/a | 47 | 4 | 0 | 0.0% |
| `referencing` | 2,804 | 499 | 211 | 0 | 0 | 0 | 0 | 0.00 | n/a | 30 | 4 | 0 | 0.0% |
| `requests-oauthlib` | 1,174 | 1,315 | 315 | 13 | 0 | 0 | 0 | 0.00 | n/a | 30 | 9 | 0 | 0.0% |
| `rich` | 35,025 | 9,671 | 2,917 | 8 | 0 | 0 | 0 | 0.00 | n/a | 458 | 63 | 0 | 0.0% |
| `s3fs` | 7,456 | 835 | 552 | 10 | 0 | 0 | 0 | 0.00 | n/a | 33 | 6 | 0 | 0.0% |
| `s3transfer` | 7,579 | 733 | 1,411 | 0 | 0 | 0 | 0 | 0.00 | n/a | 268 | 0 | 0 | 0.0% |
| `setuptools` | 72,957 | 17,963 | 11,038 | n/a | 0 | 0 | 0 | 0.00 | n/a | 326 | 13 | 0 | 0.0% |
| `shellingham` | 360 | 194 | 18 | 1 | 0 | 0 | 0 | 0.00 | n/a | 6 | 1 | 0 | 0.0% |
| `six` | 813 | 628 | 49 | 0 | 0 | 0 | 0 | 0.00 | n/a | 31 | 3 | 0 | 0.0% |
| `sniffio` | 149 | 221 | 31 | 0 | 0 | 0 | 0 | 0.00 | n/a | 1 | 1 | 0 | 0.0% |
| `soupsieve` | 4,387 | 4,173 | 524 | 2 | 0 | 0 | 0 | 0.00 | n/a | 84 | 1 | 0 | 0.0% |
| `sse-starlette` | 623 | 660 | 115 | 0 | 0 | 0 | 0 | 0.00 | n/a | 8 | 0 | 0 | 0.0% |
| `starlette` | 5,890 | 4,361 | 164 | 6 | 0 | 0 | 0 | 0.00 | n/a | 257 | 29 | 0 | 0.0% |
| `tenacity` | 1,962 | 603 | 157 | 0 | 0 | 0 | 0 | 0.00 | n/a | 25 | 0 | 0 | 0.0% |
| `threadpoolctl` | 1,736 | 857 | 349 | 6 | 0 | 0 | 0 | 0.00 | n/a | 15 | 5 | 0 | 0.0% |
| `truststore` | 1,417 | 270 | 28 | 0 | 0 | 0 | 0 | 0.00 | n/a | 26 | 1 | 0 | 0.0% |
| `typer` | 11,361 | 7,699 | 728 | 0 | 0 | 0 | 0 | 0.00 | n/a | 128 | 5 | 0 | 0.0% |
| `tzdata` | 5 | 1,691 | 0 | 0 | 0 | 0 | 0 | 0.00 | n/a | 0 | 0 | 0 | n/a |
| `uvicorn` | 6,395 | 2,405 | 132 | 0 | 0 | 0 | 0 | 0.00 | n/a | 251 | 1 | 0 | 0.0% |
