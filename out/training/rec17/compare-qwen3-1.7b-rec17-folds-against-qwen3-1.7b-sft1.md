# Before and after training, over 3 folds: two models for each fold

Every test source is scored with the model of its fold, whose training data did not include it.

| Fold | Training data | Examples | Before | Trained model | Test sources |
| --- | --- | --- | --- | --- | --- |
| 1 | `rec17` | 1067 | `qwen3-1.7b-sft1` | `qwen3-1.7b-rec17` | chinook, dateutil__dateutil, pallets__werkzeug |
| 2 | `rec17-f2` | 857 | `qwen3-1.7b-sft1-f2` | `qwen3-1.7b-rec17-f2` | more-itertools__more-itertools, networkx__networkx, pypa__packaging, sakila |
| 3 | `rec17-f3` | 1196 | `qwen3-1.7b-sft1-f3` | `qwen3-1.7b-rec17-f3` | northwind, pallets__jinja, sybrenstuvel__python-rsa |

A cell is the number of right answers: the mean of the runs, then each run in brackets. *Only* counts the questions that one model got right and the other did not, on the first run; p is the exact sign test on that split.

| Question set | Condition | Questions | before | trained | Only before | Only trained | p |
| --- | --- | --- | --- | --- | --- | --- | --- |
| Database questions | no tool | 118 | 1.0 (1%) (1, 1, 1) | 6.0 (5%) (6, 6, 6) | 0 | 5 | 0.062 |
| Database questions | SQL tool | 118 | 105.7 (90%) (106, 106, 105) | 104.7 (89%) (105, 104, 105) | 3 | 2 | 1 |
| Documentation questions | no tool | 120 | 49.0 (41%) (49, 49, 49) | 53.0 (44%) (53, 53, 53) | 7 | 11 | 0.48 |
| Documentation questions | Python tool | 120 | 49.3 (41%) (51, 49, 48) | 52.0 (43%) (51, 52, 53) | 10 | 10 | 1 |
| Aimed questions | no tool | 62 | 14.0 (23%) (14, 14, 14) | 17.0 (27%) (17, 17, 17) | 3 | 6 | 0.51 |
| Aimed questions | Python tool | 62 | 18.3 (30%) (18, 19, 18) | 27.7 (45%) (27, 27, 29) | 4 | 13 | 0.049 |

## How the student worked

Shares of all answers over the runs.

| Question set | Condition | Model | Called the tool | Calls per answer | The same call 3 times in a row | A call written as text | Needed the reminder | No answer |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| Database questions | no tool | before | 0% | 0 | 0% | 0% | 0% | 0% |
| Database questions | no tool | trained | 0% | 0 | 0% | 0% | 0% | 0% |
| Database questions | SQL tool | before | 98% | 3.54 | 6% | 2% | 2% | 8% |
| Database questions | SQL tool | trained | 100% | 4.76 | 10% | 0% | 2% | 9% |
| Documentation questions | no tool | before | 0% | 0 | 0% | 0% | 5% | 0% |
| Documentation questions | no tool | trained | 0% | 0 | 0% | 0% | 3% | 0% |
| Documentation questions | Python tool | before | 96% | 9.7 | 60% | 2% | 8% | 16% |
| Documentation questions | Python tool | trained | 98% | 12.39 | 59% | 0% | 6% | 16% |
| Aimed questions | no tool | before | 0% | 0 | 0% | 0% | 3% | 0% |
| Aimed questions | no tool | trained | 0% | 0 | 0% | 0% | 2% | 0% |
| Aimed questions | Python tool | before | 98% | 12.73 | 60% | 1% | 14% | 18% |
| Aimed questions | Python tool | trained | 97% | 13.34 | 47% | 0% | 5% | 19% |
