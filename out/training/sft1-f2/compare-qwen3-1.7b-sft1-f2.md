# Before and after training: `qwen3-1.7b-sft1-f2` against `qwen3-1.7b`

Training data `sft1-f2`: 801 examples from the passed runs of qwen3-32b, qwen3-8b on 6 sources. The test sources gave no example: more-itertools__more-itertools, networkx__networkx, pypa__packaging, sakila.

A cell is the number of right answers: the mean of the runs, then each run in brackets. *Only* counts the questions that one model got right and the other did not, on the first run; p is the exact sign test on that split.

| Question set | Condition | Questions | qwen3-1.7b | qwen3-1.7b-sft1-f2 | Only qwen3-1.7b | Only qwen3-1.7b-sft1-f2 | p |
| --- | --- | --- | --- | --- | --- | --- | --- |
| Documentation questions | no tool | 67 | 21.7 (32%) (21, 22, 22) | 27.0 (40%) (27, 27, 27) | 1 | 7 | 0.07 |
| Documentation questions | Python tool | 67 | 20.7 (31%) (22, 20, 20) | 25.3 (38%) (27, 25, 24) | 4 | 9 | 0.27 |
| Aimed questions | no tool | 29 | 3.0 (10%) (3, 3, 3) | 3.0 (10%) (3, 3, 3) | 1 | 1 | 1 |
| Aimed questions | Python tool | 29 | 8.0 (28%) (8, 8, 8) | 8.3 (29%) (8, 9, 8) | 5 | 5 | 1 |
| Database questions | no tool | 39 | 0.0 (0%) (0, 0, 0) | 0.0 (0%) (0, 0, 0) | 0 | 0 | 1 |
| Database questions | SQL tool | 39 | 17.0 (44%) (18, 14, 19) | 38.0 (97%) (38, 38, 38) | 0 | 20 | 1.9e-06 |

## How the student worked

Shares of all answers over the runs.

| Question set | Condition | Model | Called the tool | Calls per answer | The same call 3 times in a row | A call written as text | Needed the reminder | No answer |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| Documentation questions | no tool | qwen3-1.7b | 0% | 0 | 0% | 0% | 17% | 0% |
| Documentation questions | no tool | qwen3-1.7b-sft1-f2 | 0% | 0 | 0% | 0% | 4% | 0% |
| Documentation questions | Python tool | qwen3-1.7b | 99% | 11.95 | 57% | 39% | 49% | 21% |
| Documentation questions | Python tool | qwen3-1.7b-sft1-f2 | 99% | 4.32 | 70% | 1% | 1% | 0% |
| Aimed questions | no tool | qwen3-1.7b | 0% | 0 | 0% | 0% | 14% | 0% |
| Aimed questions | no tool | qwen3-1.7b-sft1-f2 | 0% | 0 | 0% | 0% | 3% | 0% |
| Aimed questions | Python tool | qwen3-1.7b | 100% | 5.76 | 46% | 31% | 61% | 2% |
| Aimed questions | Python tool | qwen3-1.7b-sft1-f2 | 98% | 5.11 | 63% | 0% | 2% | 0% |
| Database questions | no tool | qwen3-1.7b | 0% | 0 | 0% | 0% | 20% | 0% |
| Database questions | no tool | qwen3-1.7b-sft1-f2 | 0% | 0 | 0% | 0% | 0% | 0% |
| Database questions | SQL tool | qwen3-1.7b | 99% | 1.16 | 2% | 2% | 60% | 1% |
| Database questions | SQL tool | qwen3-1.7b-sft1-f2 | 100% | 1.42 | 2% | 0% | 1% | 0% |
