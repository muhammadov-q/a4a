# Memory or skill: `qwen3-32b` on tasks-aimed-v1 (aimed1v1) against the original questions (aimed1)

Only questions whose answer changed. "Old answer": on the changed question, the model gave the original answer, so it answered from memory. p is the exact two-sided sign test on the questions right only before or only after.

| Condition | Questions with a changed answer | Right before | Right after | Old answer | Right only before | Right only after | p |
| --- | --- | --- | --- | --- | --- | --- | --- |
| No tools | 28 | 13 (46%) | 11 (39%) | 2 (7%) | 2 | 0 | 0.5 |
| One Python tool | 28 | 18 (64%) | 19 (68%) | 1 (4%) | 2 | 3 | 1 |

For comparison, the questions whose answer did not change (the same question twice, so any difference is noise):

| Condition | Questions | Right before | Right after |
| --- | --- | --- | --- |
| No tools | 14 | 7 (50%) | 8 (57%) |
| One Python tool | 14 | 9 (64%) | 9 (64%) |

## Per source

| Source | Condition | Changed | Right before | Right after | Old answer |
| --- | --- | --- | --- | --- | --- |
| `dateutil__dateutil` | No tools | 4 | 3 | 2 | 1 |
| `more-itertools__more-itertools` | No tools | 4 | 1 | 1 | 0 |
| `networkx__networkx` | No tools | 7 | 3 | 3 | 1 |
| `pallets__jinja` | No tools | 1 | 1 | 0 | 0 |
| `pallets__werkzeug` | No tools | 6 | 2 | 2 | 0 |
| `pypa__packaging` | No tools | 5 | 3 | 3 | 0 |
| `sybrenstuvel__python-rsa` | No tools | 1 | 0 | 0 | 0 |
| `modelcontextprotocol__python-sdk` | No tools | no runs | | | |
| `dateutil__dateutil` | One Python tool | 4 | 4 | 3 | 1 |
| `more-itertools__more-itertools` | One Python tool | 4 | 1 | 3 | 0 |
| `networkx__networkx` | One Python tool | 7 | 4 | 4 | 0 |
| `pallets__jinja` | One Python tool | 1 | 1 | 1 | 0 |
| `pallets__werkzeug` | One Python tool | 6 | 4 | 4 | 0 |
| `pypa__packaging` | One Python tool | 5 | 4 | 3 | 0 |
| `sybrenstuvel__python-rsa` | One Python tool | 1 | 0 | 1 | 0 |
| `modelcontextprotocol__python-sdk` | One Python tool | no runs | | | |
