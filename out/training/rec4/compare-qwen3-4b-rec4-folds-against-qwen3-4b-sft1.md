# Before and after training, over 3 folds: two models for each fold

Every test source is scored with the model of its fold, whose training data did not include it.

| Fold | Training data | Examples | Before | Trained model | Test sources |
| --- | --- | --- | --- | --- | --- |
| 1 | `rec4` | 1040 | `qwen3-4b-sft1` | `qwen3-4b-rec4` | chinook, dateutil__dateutil, pallets__werkzeug |
| 2 | `rec4-f2` | 823 | `qwen3-4b-sft1-f2` | `qwen3-4b-rec4-f2` | more-itertools__more-itertools, networkx__networkx, pypa__packaging, sakila |
| 3 | `rec4-f3` | 1161 | `qwen3-4b-sft1-f3` | `qwen3-4b-rec4-f3` | northwind, pallets__jinja, sybrenstuvel__python-rsa |

A cell is the number of right answers: the mean of the runs, then each run in brackets. *Only* counts the questions that one model got right and the other did not, on the first run; p is the exact sign test on that split.

| Question set | Condition | Questions | before | trained | Only before | Only trained | p |
| --- | --- | --- | --- | --- | --- | --- | --- |
| Database questions | no tool | 118 | 19.0 (16%) (19, 19, 19) | 19.7 (17%) (19, 20, 20) | 1 | 1 | 1 |
| Database questions | SQL tool | 118 | 114.0 (97%) (114, 114, 114) | 115.7 (98%) (115, 117, 115) | 1 | 2 | 1 |
| Documentation questions | no tool | 120 | 49.7 (41%) (50, 50, 49) | 59.0 (49%) (59, 59, 59) | 3 | 12 | 0.035 |
| Documentation questions | Python tool | 120 | 61.7 (51%) (61, 63, 61) | 63.7 (53%) (64, 64, 63) | 6 | 9 | 0.61 |
| Aimed questions | no tool | 62 | 28.0 (45%) (28, 28, 28) | 29.7 (48%) (29, 30, 30) | 1 | 2 | 1 |
| Aimed questions | Python tool | 62 | 31.7 (51%) (31, 33, 31) | 32.7 (53%) (33, 32, 33) | 3 | 5 | 0.73 |

## How the student worked

Shares of all answers over the runs.

| Question set | Condition | Model | Called the tool | Calls per answer | The same call 3 times in a row | A call written as text | Needed the reminder | No answer |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| Database questions | no tool | before | 0% | 0 | 0% | 0% | 0% | 0% |
| Database questions | no tool | trained | 0% | 0 | 0% | 0% | 4% | 0% |
| Database questions | SQL tool | before | 100% | 2.36 | 3% | 0% | 0% | 3% |
| Database questions | SQL tool | trained | 100% | 1.36 | 2% | 0% | 0% | 1% |
| Documentation questions | no tool | before | 0% | 0 | 0% | 0% | 1% | 0% |
| Documentation questions | no tool | trained | 0% | 0 | 0% | 0% | 0% | 0% |
| Documentation questions | Python tool | before | 99% | 13.76 | 36% | 9% | 6% | 30% |
| Documentation questions | Python tool | trained | 98% | 8.38 | 31% | 1% | 2% | 16% |
| Aimed questions | no tool | before | 0% | 0 | 0% | 0% | 6% | 0% |
| Aimed questions | no tool | trained | 0% | 0 | 0% | 0% | 2% | 0% |
| Aimed questions | Python tool | before | 98% | 10.17 | 23% | 1% | 11% | 22% |
| Aimed questions | Python tool | trained | 98% | 7.02 | 19% | 2% | 4% | 11% |
