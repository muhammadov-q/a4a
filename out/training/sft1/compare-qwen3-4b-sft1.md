# Before and after training: `qwen3-4b-sft1` against `qwen3-4b`

Training data `sft1`: 997 examples from the passed runs of qwen3-32b, qwen3-8b on 7 sources. The test sources gave no example: chinook, dateutil__dateutil, pallets__werkzeug.

A cell is the number of right answers: the mean of the runs, then each run in brackets. *Only* counts the questions that one model got right and the other did not, on the first run; p is the exact sign test on that split.

| Question set | Condition | Questions | qwen3-4b | qwen3-4b-sft1 | Only qwen3-4b | Only qwen3-4b-sft1 | p |
| --- | --- | --- | --- | --- | --- | --- | --- |
| Database questions | no tool | 40 | 3.0 (8%) (3, 3, 3) | 2.0 (5%) (2, 2, 2) | 1 | 0 | 1 |
| Database questions | SQL tool | 40 | 31.0 (78%) (31, 31, 31) | 39.0 (98%) (39, 39, 39) | 0 | 8 | 0.0078 |
| Documentation questions | no tool | 27 | 4.0 (15%) (4, 4, 4) | 10.0 (37%) (10, 10, 10) | 0 | 6 | 0.031 |
| Documentation questions | Python tool | 27 | 19.0 (70%) (20, 19, 18) | 15.3 (57%) (16, 15, 15) | 4 | 0 | 0.12 |
| Aimed questions | no tool | 27 | 11.0 (41%) (11, 11, 11) | 14.0 (52%) (14, 14, 14) | 0 | 3 | 0.25 |
| Aimed questions | Python tool | 27 | 13.3 (49%) (13, 14, 13) | 13.7 (51%) (14, 14, 13) | 2 | 3 | 1 |

## How the student worked

Shares of all answers over the runs.

| Question set | Condition | Model | Called the tool | Calls per answer | The same call 3 times in a row | A call written as text | Needed the reminder | No answer |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| Database questions | no tool | qwen3-4b | 0% | 0 | 0% | 0% | 0% | 0% |
| Database questions | no tool | qwen3-4b-sft1 | 0% | 0 | 0% | 0% | 0% | 0% |
| Database questions | SQL tool | qwen3-4b | 100% | 1.52 | 1% | 1% | 7% | 1% |
| Database questions | SQL tool | qwen3-4b-sft1 | 100% | 2.1 | 2% | 0% | 0% | 2% |
| Documentation questions | no tool | qwen3-4b | 0% | 0 | 0% | 0% | 0% | 0% |
| Documentation questions | no tool | qwen3-4b-sft1 | 0% | 0 | 0% | 0% | 2% | 0% |
| Documentation questions | Python tool | qwen3-4b | 99% | 4.95 | 17% | 6% | 12% | 5% |
| Documentation questions | Python tool | qwen3-4b-sft1 | 96% | 14.81 | 35% | 0% | 0% | 38% |
| Aimed questions | no tool | qwen3-4b | 0% | 0 | 0% | 0% | 0% | 0% |
| Aimed questions | no tool | qwen3-4b-sft1 | 0% | 0 | 0% | 0% | 0% | 0% |
| Aimed questions | Python tool | qwen3-4b | 96% | 7.62 | 21% | 4% | 32% | 12% |
| Aimed questions | Python tool | qwen3-4b-sft1 | 100% | 9.81 | 24% | 0% | 7% | 21% |
