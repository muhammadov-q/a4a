# Memory or skill: `qwen3-32b` on tasks-v1 (db1v1) against the original questions (db1)

Only questions whose answer changed. "Old answer": on the changed question, the model gave the original answer, so it answered from memory. p is the exact two-sided sign test on the questions right only before or only after.

| Condition | Questions with a changed answer | Right before | Right after | Old answer | Right only before | Right only after | p |
| --- | --- | --- | --- | --- | --- | --- | --- |
| No tools | 82 | 30 (37%) | 1 (1%) | 30 (37%) | 30 | 1 | 3e-08 |
| One SQL tool | 82 | 76 (93%) | 75 (91%) | 0 (0%) | 1 | 0 | 1 |

For comparison, the questions whose answer did not change (the same question twice, so any difference is noise):

| Condition | Questions | Right before | Right after |
| --- | --- | --- | --- |
| No tools | 34 | 11 (32%) | 11 (32%) |
| One SQL tool | 34 | 33 (97%) | 33 (97%) |

## Per source

| Source | Condition | Changed | Right before | Right after | Old answer |
| --- | --- | --- | --- | --- | --- |
| `chinook` | No tools | 28 | 11 | 0 | 11 |
| `northwind` | No tools | 25 | 7 | 1 | 7 |
| `sakila` | No tools | 29 | 12 | 0 | 12 |
| `chinook` | One SQL tool | 28 | 23 | 23 | 0 |
| `northwind` | One SQL tool | 25 | 25 | 25 | 0 |
| `sakila` | One SQL tool | 29 | 28 | 27 | 0 |
