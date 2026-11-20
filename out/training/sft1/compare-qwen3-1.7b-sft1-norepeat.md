# Before and after training: `qwen3-1.7b-sft1` against `qwen3-1.7b`

Training data `sft1`: 997 examples from the passed runs of qwen3-32b, qwen3-8b on 7 sources. The test sources gave no example: chinook, dateutil__dateutil, pallets__werkzeug.

Tool runs with `--no-repeat`: a call that is the same as an earlier call of the run is not run again; the model is told so.

A cell is the number of right answers: the mean of the runs, then each run in brackets. *Only* counts the questions that one model got right and the other did not, on the first run; p is the exact sign test on that split.

| Question set | Condition | Questions | qwen3-1.7b | qwen3-1.7b-sft1 | Only qwen3-1.7b | Only qwen3-1.7b-sft1 | p |
| --- | --- | --- | --- | --- | --- | --- | --- |
| Database questions | no tool | 40 | 2.0 (5%) (2, 2, 2) | 1.0 (2%) (1, 1, 1) | 2 | 1 | 1 |
| Database questions | SQL tool | 40 | 20.0 (50%) (20, 20, 20) | 34.3 (86%) (34, 35, 34) | 3 | 17 | 0.0026 |
| Documentation questions | no tool | 27 | 4.0 (15%) (4, 4, 4) | 9.0 (33%) (9, 9, 9) | 0 | 5 | 0.062 |
| Documentation questions | Python tool | 27 | 7.7 (28%) (8, 7, 8) | 9.0 (33%) (10, 9, 8) | 1 | 3 | 0.62 |
| Aimed questions | no tool | 27 | 7.0 (26%) (7, 7, 7) | 10.0 (37%) (10, 10, 10) | 1 | 4 | 0.38 |
| Aimed questions | Python tool | 27 | 9.3 (35%) (10, 9, 9) | 13.7 (51%) (13, 13, 15) | 4 | 7 | 0.55 |

## How the student worked

Shares of all answers over the runs.

| Question set | Condition | Model | Called the tool | Calls per answer | The same call 3 times in a row | A call written as text | Needed the reminder | No answer |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| Database questions | no tool | qwen3-1.7b | 0% | 0 | 0% | 0% | 54% | 0% |
| Database questions | no tool | qwen3-1.7b-sft1 | 0% | 0 | 0% | 0% | 0% | 0% |
| Database questions | SQL tool | qwen3-1.7b | 100% | 2.52 | 8% | 2% | 59% | 2% |
| Database questions | SQL tool | qwen3-1.7b-sft1 | 100% | 4.43 | 8% | 4% | 6% | 8% |
| Documentation questions | no tool | qwen3-1.7b | 0% | 0 | 0% | 0% | 7% | 0% |
| Documentation questions | no tool | qwen3-1.7b-sft1 | 0% | 0 | 0% | 0% | 0% | 0% |
| Documentation questions | Python tool | qwen3-1.7b | 96% | 9.25 | 52% | 24% | 56% | 15% |
| Documentation questions | Python tool | qwen3-1.7b-sft1 | 88% | 15.48 | 44% | 6% | 26% | 41% |
| Aimed questions | no tool | qwen3-1.7b | 0% | 0 | 0% | 0% | 4% | 0% |
| Aimed questions | no tool | qwen3-1.7b-sft1 | 0% | 0 | 0% | 0% | 4% | 0% |
| Aimed questions | Python tool | qwen3-1.7b | 100% | 7.19 | 46% | 22% | 54% | 9% |
| Aimed questions | Python tool | qwen3-1.7b-sft1 | 98% | 13.32 | 49% | 10% | 24% | 26% |
