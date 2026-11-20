# Before and after training: `qwen3-1.7b-sft1-f3` against `qwen3-1.7b`

Training data `sft1-f3`: 1122 examples from the passed runs of qwen3-32b, qwen3-8b on 7 sources. The test sources gave no example: northwind, pallets__jinja, sybrenstuvel__python-rsa.

A cell is the number of right answers: the mean of the runs, then each run in brackets. *Only* counts the questions that one model got right and the other did not, on the first run; p is the exact sign test on that split.

| Question set | Condition | Questions | qwen3-1.7b | qwen3-1.7b-sft1-f3 | Only qwen3-1.7b | Only qwen3-1.7b-sft1-f3 | p |
| --- | --- | --- | --- | --- | --- | --- | --- |
| Database questions | no tool | 39 | 0.0 (0%) (0, 0, 0) | 0.0 (0%) (0, 0, 0) | 0 | 0 | 1 |
| Database questions | SQL tool | 39 | 17.0 (44%) (15, 18, 18) | 33.0 (85%) (33, 33, 33) | 0 | 18 | 7.6e-06 |
| Documentation questions | no tool | 26 | 7.0 (27%) (7, 7, 7) | 13.0 (50%) (13, 13, 13) | 1 | 7 | 0.07 |
| Documentation questions | Python tool | 26 | 14.0 (54%) (14, 14, 14) | 14.0 (54%) (14, 14, 14) | 2 | 2 | 1 |
| Aimed questions | no tool | 6 | 1.0 (17%) (1, 1, 1) | 1.0 (17%) (1, 1, 1) | 1 | 1 | 1 |
| Aimed questions | Python tool | 6 | 1.0 (17%) (1, 1, 1) | 0.3 (6%) (0, 1, 0) | 1 | 0 | 1 |

## How the student worked

Shares of all answers over the runs.

| Question set | Condition | Model | Called the tool | Calls per answer | The same call 3 times in a row | A call written as text | Needed the reminder | No answer |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| Database questions | no tool | qwen3-1.7b | 0% | 0 | 0% | 0% | 13% | 0% |
| Database questions | no tool | qwen3-1.7b-sft1-f3 | 0% | 0 | 0% | 0% | 0% | 0% |
| Database questions | SQL tool | qwen3-1.7b | 100% | 3.32 | 6% | 5% | 58% | 5% |
| Database questions | SQL tool | qwen3-1.7b-sft1-f3 | 100% | 7 | 15% | 5% | 0% | 15% |
| Documentation questions | no tool | qwen3-1.7b | 0% | 0 | 0% | 0% | 0% | 0% |
| Documentation questions | no tool | qwen3-1.7b-sft1-f3 | 0% | 0 | 0% | 0% | 12% | 0% |
| Documentation questions | Python tool | qwen3-1.7b | 96% | 6.49 | 32% | 22% | 46% | 10% |
| Documentation questions | Python tool | qwen3-1.7b-sft1-f3 | 96% | 14.74 | 50% | 6% | 17% | 27% |
| Aimed questions | no tool | qwen3-1.7b | 0% | 0 | 0% | 0% | 0% | 0% |
| Aimed questions | no tool | qwen3-1.7b-sft1-f3 | 0% | 0 | 0% | 0% | 0% | 0% |
| Aimed questions | Python tool | qwen3-1.7b | 100% | 14.61 | 100% | 17% | 50% | 17% |
| Aimed questions | Python tool | qwen3-1.7b-sft1-f3 | 100% | 28.78 | 100% | 11% | 72% | 28% |
