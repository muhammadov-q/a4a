# Before and after training: `qwen3-4b-sft1-f2` against `qwen3-4b`

Training data `sft1-f2`: 801 examples from the passed runs of qwen3-32b, qwen3-8b on 6 sources. The test sources gave no example: more-itertools__more-itertools, networkx__networkx, pypa__packaging, sakila.

A cell is the number of right answers: the mean of the runs, then each run in brackets. *Only* counts the questions that one model got right and the other did not, on the first run; p is the exact sign test on that split.

| Question set | Condition | Questions | qwen3-4b | qwen3-4b-sft1-f2 | Only qwen3-4b | Only qwen3-4b-sft1-f2 | p |
| --- | --- | --- | --- | --- | --- | --- | --- |
| Documentation questions | no tool | 67 | 31.7 (47%) (32, 31, 32) | 28.7 (43%) (29, 29, 28) | 8 | 5 | 0.58 |
| Documentation questions | Python tool | 67 | 33.7 (50%) (35, 34, 32) | 31.0 (46%) (30, 32, 31) | 14 | 9 | 0.4 |
| Aimed questions | no tool | 29 | 10.0 (34%) (10, 10, 10) | 12.0 (41%) (12, 12, 12) | 2 | 4 | 0.69 |
| Aimed questions | Python tool | 29 | 17.7 (61%) (18, 18, 17) | 16.3 (56%) (16, 17, 16) | 3 | 1 | 0.62 |
| Database questions | no tool | 39 | 9.0 (23%) (9, 9, 9) | 12.0 (31%) (12, 12, 12) | 0 | 3 | 0.25 |
| Database questions | SQL tool | 39 | 32.0 (82%) (32, 32, 32) | 38.0 (97%) (38, 38, 38) | 0 | 6 | 0.031 |

## How the student worked

Shares of all answers over the runs.

| Question set | Condition | Model | Called the tool | Calls per answer | The same call 3 times in a row | A call written as text | Needed the reminder | No answer |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| Documentation questions | no tool | qwen3-4b | 0% | 0 | 0% | 0% | 0% | 0% |
| Documentation questions | no tool | qwen3-4b-sft1-f2 | 0% | 0 | 0% | 0% | 0% | 0% |
| Documentation questions | Python tool | qwen3-4b | 100% | 6.87 | 22% | 10% | 25% | 10% |
| Documentation questions | Python tool | qwen3-4b-sft1-f2 | 100% | 14.19 | 39% | 15% | 8% | 28% |
| Aimed questions | no tool | qwen3-4b | 0% | 0 | 0% | 0% | 0% | 0% |
| Aimed questions | no tool | qwen3-4b-sft1-f2 | 0% | 0 | 0% | 0% | 10% | 0% |
| Aimed questions | Python tool | qwen3-4b | 100% | 2.2 | 2% | 1% | 30% | 0% |
| Aimed questions | Python tool | qwen3-4b-sft1-f2 | 97% | 7.86 | 15% | 2% | 17% | 15% |
| Database questions | no tool | qwen3-4b | 0% | 0 | 0% | 0% | 0% | 0% |
| Database questions | no tool | qwen3-4b-sft1-f2 | 0% | 0 | 0% | 0% | 0% | 0% |
| Database questions | SQL tool | qwen3-4b | 100% | 1 | 0% | 0% | 0% | 0% |
| Database questions | SQL tool | qwen3-4b-sft1-f2 | 100% | 2 | 3% | 0% | 0% | 3% |
