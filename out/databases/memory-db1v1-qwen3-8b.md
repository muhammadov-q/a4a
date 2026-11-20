# Memory or skill: `qwen3-8b` on tasks-v1 (db1v1) against the original questions (db1)

Only questions whose answer changed. "Old answer": on the changed question, the model gave the original answer, so it answered from memory. p is the exact two-sided sign test on the questions right only before or only after.

| Condition | Questions with a changed answer | Right before | Right after | Old answer | Right only before | Right only after | p |
| --- | --- | --- | --- | --- | --- | --- | --- |
| No tools | 82 | 7 (9%) | 1 (1%) | 6 (7%) | 7 | 1 | 0.07 |
| One SQL tool | 82 | 72 (88%) | 73 (89%) | 0 (0%) | 2 | 3 | 1 |

For comparison, the questions whose answer did not change (the same question twice, so any difference is noise):

| Condition | Questions | Right before | Right after |
| --- | --- | --- | --- |
| No tools | 34 | 4 (12%) | 4 (12%) |
| One SQL tool | 34 | 32 (94%) | 31 (91%) |

## Per source

| Source | Condition | Changed | Right before | Right after | Old answer |
| --- | --- | --- | --- | --- | --- |
| `chinook` | No tools | 28 | 0 | 0 | 0 |
| `northwind` | No tools | 25 | 4 | 0 | 3 |
| `sakila` | No tools | 29 | 3 | 1 | 3 |
| `chinook` | One SQL tool | 28 | 25 | 26 | 0 |
| `northwind` | One SQL tool | 25 | 23 | 23 | 0 |
| `sakila` | One SQL tool | 29 | 24 | 24 | 0 |
