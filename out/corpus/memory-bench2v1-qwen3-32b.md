# Memory or skill: `qwen3-32b` on tasks-v1 (bench2v1) against the original questions (bench2)

Only questions whose answer changed. "Old answer": on the changed question, the model gave the original answer, so it answered from memory. p is the exact two-sided sign test on the questions right only before or only after.

| Condition | Questions with a changed answer | Right before | Right after | Old answer | Right only before | Right only after | p |
| --- | --- | --- | --- | --- | --- | --- | --- |
| No tools | 41 | 21 (51%) | 19 (46%) | 3 (7%) | 6 | 4 | 0.75 |
| One Python tool | 41 | 29 (71%) | 25 (61%) | 2 (5%) | 5 | 1 | 0.22 |

For comparison, the questions whose answer did not change (the same question twice, so any difference is noise):

| Condition | Questions | Right before | Right after |
| --- | --- | --- | --- |
| No tools | 39 | 30 (77%) | 31 (79%) |
| One Python tool | 39 | 26 (67%) | 26 (67%) |

## Per source

| Source | Condition | Changed | Right before | Right after | Old answer |
| --- | --- | --- | --- | --- | --- |
| `dateutil__dateutil` | No tools | 5 | 2 | 2 | 0 |
| `more-itertools__more-itertools` | No tools | 9 | 5 | 4 | 0 |
| `networkx__networkx` | No tools | 11 | 4 | 4 | 1 |
| `pallets__jinja` | No tools | 0 | 0 | 0 | 0 |
| `pallets__werkzeug` | No tools | 3 | 3 | 3 | 0 |
| `pypa__packaging` | No tools | 6 | 4 | 4 | 1 |
| `sybrenstuvel__python-rsa` | No tools | 7 | 3 | 2 | 1 |
| `fsspec__filesystem_spec`, `huggingface__huggingface_hub`, `jaraco__zipp`, `jmespath__jmespath.py`, `modelcontextprotocol__python-sdk`, `oauthlib__oauthlib`, `psf__requests`, `pyasn1__pyasn1`, `pypa__distlib`, `python-attrs__attrs`, `python-jsonschema__jsonschema`, `python__importlib_metadata`, `python__typing_extensions`, `stub42__pytz` | No tools | no runs | | | |
| `dateutil__dateutil` | One Python tool | 5 | 4 | 4 | 0 |
| `more-itertools__more-itertools` | One Python tool | 9 | 4 | 2 | 0 |
| `networkx__networkx` | One Python tool | 11 | 8 | 6 | 1 |
| `pallets__jinja` | One Python tool | 0 | 0 | 0 | 0 |
| `pallets__werkzeug` | One Python tool | 3 | 3 | 3 | 0 |
| `pypa__packaging` | One Python tool | 6 | 4 | 4 | 1 |
| `sybrenstuvel__python-rsa` | One Python tool | 7 | 6 | 6 | 0 |
| `fsspec__filesystem_spec`, `huggingface__huggingface_hub`, `jaraco__zipp`, `jmespath__jmespath.py`, `modelcontextprotocol__python-sdk`, `oauthlib__oauthlib`, `psf__requests`, `pyasn1__pyasn1`, `pypa__distlib`, `python-attrs__attrs`, `python-jsonschema__jsonschema`, `python__importlib_metadata`, `python__typing_extensions`, `stub42__pytz` | One Python tool | no runs | | | |
