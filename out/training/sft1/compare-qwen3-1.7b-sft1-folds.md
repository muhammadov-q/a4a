# Before and after training, over 3 folds: `qwen3-1.7b` and the model trained for each fold

Every test source is scored with the model of its fold, whose training data did not include it.

| Fold | Training data | Examples | Trained model | Test sources |
| --- | --- | --- | --- | --- |
| 1 | `sft1` | 997 | `qwen3-1.7b-sft1` | chinook, dateutil__dateutil, pallets__werkzeug |
| 2 | `sft1-f2` | 801 | `qwen3-1.7b-sft1-f2` | more-itertools__more-itertools, networkx__networkx, pypa__packaging, sakila |
| 3 | `sft1-f3` | 1122 | `qwen3-1.7b-sft1-f3` | northwind, pallets__jinja, sybrenstuvel__python-rsa |

A cell is the number of right answers: the mean of the runs, then each run in brackets. *Only* counts the questions that one model got right and the other did not, on the first run; p is the exact sign test on that split.

| Question set | Condition | Questions | qwen3-1.7b | trained | Only qwen3-1.7b | Only trained | p |
| --- | --- | --- | --- | --- | --- | --- | --- |
| Database questions | no tool | 118 | 2.0 (2%) (2, 2, 2) | 1.0 (1%) (1, 1, 1) | 2 | 1 | 1 |
| Database questions | SQL tool | 118 | 52.0 (44%) (51, 50, 55) | 105.7 (90%) (106, 106, 105) | 2 | 57 | 6.1e-15 |
| Documentation questions | no tool | 120 | 32.7 (27%) (32, 33, 33) | 49.0 (41%) (49, 49, 49) | 2 | 19 | 0.00022 |
| Documentation questions | Python tool | 120 | 42.0 (35%) (44, 41, 41) | 49.3 (41%) (51, 49, 48) | 8 | 15 | 0.21 |
| Aimed questions | no tool | 62 | 11.0 (18%) (11, 11, 11) | 14.0 (23%) (14, 14, 14) | 3 | 6 | 0.51 |
| Aimed questions | Python tool | 62 | 20.7 (33%) (20, 21, 21) | 18.3 (30%) (18, 19, 18) | 11 | 9 | 0.82 |

## How the student worked

Shares of all answers over the runs.

| Question set | Condition | Model | Called the tool | Calls per answer | The same call 3 times in a row | A call written as text | Needed the reminder | No answer |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| Database questions | no tool | qwen3-1.7b | 0% | 0 | 0% | 0% | 29% | 0% |
| Database questions | no tool | trained | 0% | 0 | 0% | 0% | 0% | 0% |
| Database questions | SQL tool | qwen3-1.7b | 100% | 2.53 | 5% | 4% | 58% | 3% |
| Database questions | SQL tool | trained | 98% | 3.54 | 6% | 2% | 2% | 8% |
| Documentation questions | no tool | qwen3-1.7b | 0% | 0 | 0% | 0% | 11% | 0% |
| Documentation questions | no tool | trained | 0% | 0 | 0% | 0% | 5% | 0% |
| Documentation questions | Python tool | qwen3-1.7b | 98% | 10.83 | 52% | 35% | 48% | 19% |
| Documentation questions | Python tool | trained | 96% | 9.7 | 60% | 2% | 8% | 16% |
| Aimed questions | no tool | qwen3-1.7b | 0% | 0 | 0% | 0% | 8% | 0% |
| Aimed questions | no tool | trained | 0% | 0 | 0% | 0% | 3% | 0% |
| Aimed questions | Python tool | qwen3-1.7b | 100% | 7.68 | 51% | 27% | 50% | 8% |
| Aimed questions | Python tool | trained | 98% | 12.73 | 60% | 1% | 14% | 18% |
