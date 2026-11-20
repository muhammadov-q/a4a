# Before and after training, over 3 folds: `qwen3-4b` and the model trained for each fold

Every test source is scored with the model of its fold, whose training data did not include it.

| Fold | Training data | Examples | Trained model | Test sources |
| --- | --- | --- | --- | --- |
| 1 | `rec4` | 1040 | `qwen3-4b-rec4` | chinook, dateutil__dateutil, pallets__werkzeug |
| 2 | `rec4-f2` | 823 | `qwen3-4b-rec4-f2` | more-itertools__more-itertools, networkx__networkx, pypa__packaging, sakila |
| 3 | `rec4-f3` | 1161 | `qwen3-4b-rec4-f3` | northwind, pallets__jinja, sybrenstuvel__python-rsa |

A cell is the number of right answers: the mean of the runs, then each run in brackets. *Only* counts the questions that one model got right and the other did not, on the first run; p is the exact sign test on that split.

| Question set | Condition | Questions | qwen3-4b | trained | Only qwen3-4b | Only trained | p |
| --- | --- | --- | --- | --- | --- | --- | --- |
| Database questions | no tool | 118 | 16.3 (14%) (16, 16, 17) | 19.7 (17%) (19, 20, 20) | 1 | 4 | 0.38 |
| Database questions | SQL tool | 118 | 97.3 (82%) (97, 97, 98) | 115.7 (98%) (115, 117, 115) | 0 | 18 | 7.6e-06 |
| Documentation questions | no tool | 120 | 48.7 (41%) (49, 48, 49) | 59.0 (49%) (59, 59, 59) | 5 | 15 | 0.041 |
| Documentation questions | Python tool | 120 | 65.3 (54%) (67, 67, 62) | 63.7 (53%) (64, 64, 63) | 19 | 16 | 0.74 |
| Aimed questions | no tool | 62 | 23.0 (37%) (23, 23, 23) | 29.7 (48%) (29, 30, 30) | 2 | 8 | 0.11 |
| Aimed questions | Python tool | 62 | 32.3 (52%) (33, 33, 31) | 32.7 (53%) (33, 32, 33) | 4 | 4 | 1 |

## How the student worked

Shares of all answers over the runs.

| Question set | Condition | Model | Called the tool | Calls per answer | The same call 3 times in a row | A call written as text | Needed the reminder | No answer |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| Database questions | no tool | qwen3-4b | 0% | 0 | 0% | 0% | 0% | 0% |
| Database questions | no tool | trained | 0% | 0 | 0% | 0% | 4% | 0% |
| Database questions | SQL tool | qwen3-4b | 100% | 1.18 | 0% | 0% | 3% | 0% |
| Database questions | SQL tool | trained | 100% | 1.36 | 2% | 0% | 0% | 1% |
| Documentation questions | no tool | qwen3-4b | 0% | 0 | 0% | 0% | 0% | 0% |
| Documentation questions | no tool | trained | 0% | 0 | 0% | 0% | 0% | 0% |
| Documentation questions | Python tool | qwen3-4b | 100% | 6.29 | 19% | 9% | 23% | 9% |
| Documentation questions | Python tool | trained | 98% | 8.38 | 31% | 1% | 2% | 16% |
| Aimed questions | no tool | qwen3-4b | 0% | 0 | 0% | 0% | 0% | 0% |
| Aimed questions | no tool | trained | 0% | 0 | 0% | 0% | 2% | 0% |
| Aimed questions | Python tool | qwen3-4b | 98% | 5.35 | 14% | 4% | 33% | 7% |
| Aimed questions | Python tool | trained | 98% | 7.02 | 19% | 2% | 4% | 11% |
