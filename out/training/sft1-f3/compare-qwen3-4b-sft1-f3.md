# Before and after training: `qwen3-4b-sft1-f3` against `qwen3-4b`

Training data `sft1-f3`: 1122 examples from the passed runs of qwen3-32b, qwen3-8b on 7 sources. The test sources gave no example: northwind, pallets__jinja, sybrenstuvel__python-rsa.

A cell is the number of right answers: the mean of the runs, then each run in brackets. *Only* counts the questions that one model got right and the other did not, on the first run; p is the exact sign test on that split.

| Question set | Condition | Questions | qwen3-4b | qwen3-4b-sft1-f3 | Only qwen3-4b | Only qwen3-4b-sft1-f3 | p |
| --- | --- | --- | --- | --- | --- | --- | --- |
| Database questions | no tool | 39 | 4.3 (11%) (4, 4, 5) | 5.0 (13%) (5, 5, 5) | 0 | 1 | 1 |
| Database questions | SQL tool | 39 | 34.3 (88%) (34, 34, 35) | 37.0 (95%) (37, 37, 37) | 0 | 3 | 0.25 |
| Documentation questions | no tool | 26 | 13.0 (50%) (13, 13, 13) | 11.0 (42%) (11, 11, 11) | 3 | 1 | 0.62 |
| Documentation questions | Python tool | 26 | 12.7 (49%) (12, 14, 12) | 15.3 (59%) (15, 16, 15) | 2 | 5 | 0.45 |
| Aimed questions | no tool | 6 | 2.0 (33%) (2, 2, 2) | 2.0 (33%) (2, 2, 2) | 0 | 0 | 1 |
| Aimed questions | Python tool | 6 | 1.3 (22%) (2, 1, 1) | 1.7 (28%) (1, 2, 2) | 2 | 1 | 1 |

## How the student worked

Shares of all answers over the runs.

| Question set | Condition | Model | Called the tool | Calls per answer | The same call 3 times in a row | A call written as text | Needed the reminder | No answer |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| Database questions | no tool | qwen3-4b | 0% | 0 | 0% | 0% | 0% | 0% |
| Database questions | no tool | qwen3-4b-sft1-f3 | 0% | 0 | 0% | 0% | 0% | 0% |
| Database questions | SQL tool | qwen3-4b | 100% | 1.03 | 0% | 0% | 3% | 0% |
| Database questions | SQL tool | qwen3-4b-sft1-f3 | 100% | 3 | 5% | 0% | 0% | 5% |
| Documentation questions | no tool | qwen3-4b | 0% | 0 | 0% | 0% | 0% | 0% |
| Documentation questions | no tool | qwen3-4b-sft1-f3 | 0% | 0 | 0% | 0% | 0% | 0% |
| Documentation questions | Python tool | qwen3-4b | 100% | 6.21 | 15% | 6% | 30% | 9% |
| Documentation questions | Python tool | qwen3-4b-sft1-f3 | 99% | 11.54 | 30% | 0% | 9% | 26% |
| Aimed questions | no tool | qwen3-4b | 0% | 0 | 0% | 0% | 0% | 0% |
| Aimed questions | no tool | qwen3-4b-sft1-f3 | 0% | 0 | 0% | 0% | 17% | 0% |
| Aimed questions | Python tool | qwen3-4b | 100% | 10.44 | 44% | 17% | 56% | 17% |
| Aimed questions | Python tool | qwen3-4b-sft1-f3 | 100% | 22.94 | 56% | 0% | 0% | 56% |
