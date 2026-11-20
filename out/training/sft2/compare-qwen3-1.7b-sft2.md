# Before and after training: `qwen3-1.7b-sft2` against `qwen3-1.7b`

Training data `sft2`: 1094 examples from the passed runs of qwen3-32b, qwen3-8b on 7 sources. The test sources gave no example: chinook, dateutil__dateutil, pallets__werkzeug.

A cell is the number of right answers: the mean of the runs, then each run in brackets. *Only* counts the questions that one model got right and the other did not, on the first run; p is the exact sign test on that split.

| Question set | Condition | Questions | qwen3-1.7b | qwen3-1.7b-sft2 | Only qwen3-1.7b | Only qwen3-1.7b-sft2 | p |
| --- | --- | --- | --- | --- | --- | --- | --- |
| Database questions | no tool | 40 | 2.0 (5%) (2, 2, 2) | 0.0 (0%) (0, 0, 0) | 2 | 0 | 0.5 |
| Database questions | SQL tool | 40 | 18.0 (45%) (18, 18, 18) | 33.0 (82%) (33, 33, 33) | 4 | 19 | 0.0026 |
| Documentation questions | no tool | 27 | 4.0 (15%) (4, 4, 4) | 9.0 (33%) (9, 9, 9) | 0 | 5 | 0.062 |
| Documentation questions | Python tool | 27 | 7.3 (27%) (8, 7, 7) | 10.0 (37%) (10, 10, 10) | 3 | 5 | 0.73 |
| Aimed questions | no tool | 27 | 7.0 (26%) (7, 7, 7) | 10.0 (37%) (10, 10, 10) | 1 | 4 | 0.38 |
| Aimed questions | Python tool | 27 | 11.7 (43%) (11, 12, 12) | 12.0 (44%) (11, 13, 12) | 5 | 5 | 1 |

## How the student worked

Shares of all answers over the runs.

| Question set | Condition | Model | Called the tool | Calls per answer | The same call 3 times in a row | A call written as text | Needed the reminder | No answer |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| Database questions | no tool | qwen3-1.7b | 0% | 0 | 0% | 0% | 54% | 0% |
| Database questions | no tool | qwen3-1.7b-sft2 | 0% | 0 | 0% | 0% | 0% | 0% |
| Database questions | SQL tool | qwen3-1.7b | 100% | 3.09 | 8% | 4% | 56% | 3% |
| Database questions | SQL tool | qwen3-1.7b-sft2 | 100% | 7.84 | 15% | 0% | 0% | 18% |
| Documentation questions | no tool | qwen3-1.7b | 0% | 0 | 0% | 0% | 7% | 0% |
| Documentation questions | no tool | qwen3-1.7b-sft2 | 0% | 0 | 0% | 0% | 4% | 0% |
| Documentation questions | Python tool | qwen3-1.7b | 98% | 12.25 | 59% | 38% | 48% | 24% |
| Documentation questions | Python tool | qwen3-1.7b-sft2 | 80% | 15.51 | 37% | 2% | 20% | 41% |
| Aimed questions | no tool | qwen3-1.7b | 0% | 0 | 0% | 0% | 4% | 0% |
| Aimed questions | no tool | qwen3-1.7b-sft2 | 0% | 0 | 0% | 0% | 0% | 0% |
| Aimed questions | Python tool | qwen3-1.7b | 100% | 8.21 | 46% | 25% | 38% | 12% |
| Aimed questions | Python tool | qwen3-1.7b-sft2 | 100% | 17.32 | 41% | 10% | 2% | 41% |
