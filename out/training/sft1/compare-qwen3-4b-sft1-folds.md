# Before and after training, over 3 folds: `qwen3-4b` and the model trained for each fold

Every test source is scored with the model of its fold, whose training data did not include it.

| Fold | Training data | Examples | Trained model | Test sources |
| --- | --- | --- | --- | --- |
| 1 | `sft1` | 997 | `qwen3-4b-sft1` | chinook, dateutil__dateutil, pallets__werkzeug |
| 2 | `sft1-f2` | 801 | `qwen3-4b-sft1-f2` | more-itertools__more-itertools, networkx__networkx, pypa__packaging, sakila |
| 3 | `sft1-f3` | 1122 | `qwen3-4b-sft1-f3` | northwind, pallets__jinja, sybrenstuvel__python-rsa |

A cell is the number of right answers: the mean of the runs, then each run in brackets. *Only* counts the questions that one model got right and the other did not, on the first run; p is the exact sign test on that split.

| Question set | Condition | Questions | qwen3-4b | trained | Only qwen3-4b | Only trained | p |
| --- | --- | --- | --- | --- | --- | --- | --- |
| Database questions | no tool | 118 | 16.3 (14%) (16, 16, 17) | 19.0 (16%) (19, 19, 19) | 1 | 4 | 0.38 |
| Database questions | SQL tool | 118 | 97.3 (82%) (97, 97, 98) | 114.0 (97%) (114, 114, 114) | 0 | 17 | 1.5e-05 |
| Documentation questions | no tool | 120 | 48.7 (41%) (49, 48, 49) | 49.7 (41%) (50, 50, 49) | 11 | 12 | 1 |
| Documentation questions | Python tool | 120 | 65.3 (54%) (67, 67, 62) | 61.7 (51%) (61, 63, 61) | 20 | 14 | 0.39 |
| Aimed questions | no tool | 62 | 23.0 (37%) (23, 23, 23) | 28.0 (45%) (28, 28, 28) | 2 | 7 | 0.18 |
| Aimed questions | Python tool | 62 | 32.3 (52%) (33, 33, 31) | 31.7 (51%) (31, 33, 31) | 7 | 5 | 0.77 |

## How the student worked

Shares of all answers over the runs.

| Question set | Condition | Model | Called the tool | Calls per answer | The same call 3 times in a row | A call written as text | Needed the reminder | No answer |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| Database questions | no tool | qwen3-4b | 0% | 0 | 0% | 0% | 0% | 0% |
| Database questions | no tool | trained | 0% | 0 | 0% | 0% | 0% | 0% |
| Database questions | SQL tool | qwen3-4b | 100% | 1.18 | 0% | 0% | 3% | 0% |
| Database questions | SQL tool | trained | 100% | 2.36 | 3% | 0% | 0% | 3% |
| Documentation questions | no tool | qwen3-4b | 0% | 0 | 0% | 0% | 0% | 0% |
| Documentation questions | no tool | trained | 0% | 0 | 0% | 0% | 1% | 0% |
| Documentation questions | Python tool | qwen3-4b | 100% | 6.29 | 19% | 9% | 23% | 9% |
| Documentation questions | Python tool | trained | 99% | 13.76 | 36% | 9% | 6% | 30% |
| Aimed questions | no tool | qwen3-4b | 0% | 0 | 0% | 0% | 0% | 0% |
| Aimed questions | no tool | trained | 0% | 0 | 0% | 0% | 6% | 0% |
| Aimed questions | Python tool | qwen3-4b | 98% | 5.35 | 14% | 4% | 33% | 7% |
| Aimed questions | Python tool | trained | 98% | 10.17 | 23% | 1% | 11% | 22% |
