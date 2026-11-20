# Before and after training, over 3 folds: `qwen3-1.7b` and the model trained for each fold

Every test source is scored with the model of its fold, whose training data did not include it.

| Fold | Training data | Examples | Trained model | Test sources |
| --- | --- | --- | --- | --- |
| 1 | `rec17` | 1067 | `qwen3-1.7b-rec17` | chinook, dateutil__dateutil, pallets__werkzeug |
| 2 | `rec17-f2` | 857 | `qwen3-1.7b-rec17-f2` | more-itertools__more-itertools, networkx__networkx, pypa__packaging, sakila |
| 3 | `rec17-f3` | 1196 | `qwen3-1.7b-rec17-f3` | northwind, pallets__jinja, sybrenstuvel__python-rsa |

A cell is the number of right answers: the mean of the runs, then each run in brackets. *Only* counts the questions that one model got right and the other did not, on the first run; p is the exact sign test on that split.

| Question set | Condition | Questions | qwen3-1.7b | trained | Only qwen3-1.7b | Only trained | p |
| --- | --- | --- | --- | --- | --- | --- | --- |
| Database questions | no tool | 118 | 2.0 (2%) (2, 2, 2) | 6.0 (5%) (6, 6, 6) | 1 | 5 | 0.22 |
| Database questions | SQL tool | 118 | 52.0 (44%) (51, 50, 55) | 104.7 (89%) (105, 104, 105) | 4 | 58 | 2.6e-13 |
| Documentation questions | no tool | 120 | 32.7 (27%) (32, 33, 33) | 53.0 (44%) (53, 53, 53) | 5 | 26 | 0.00019 |
| Documentation questions | Python tool | 120 | 42.0 (35%) (44, 41, 41) | 52.0 (43%) (51, 52, 53) | 10 | 17 | 0.25 |
| Aimed questions | no tool | 62 | 11.0 (18%) (11, 11, 11) | 17.0 (27%) (17, 17, 17) | 1 | 7 | 0.07 |
| Aimed questions | Python tool | 62 | 20.7 (33%) (20, 21, 21) | 27.7 (45%) (27, 27, 29) | 7 | 14 | 0.19 |

## How the student worked

Shares of all answers over the runs.

| Question set | Condition | Model | Called the tool | Calls per answer | The same call 3 times in a row | A call written as text | Needed the reminder | No answer |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| Database questions | no tool | qwen3-1.7b | 0% | 0 | 0% | 0% | 29% | 0% |
| Database questions | no tool | trained | 0% | 0 | 0% | 0% | 0% | 0% |
| Database questions | SQL tool | qwen3-1.7b | 100% | 2.53 | 5% | 4% | 58% | 3% |
| Database questions | SQL tool | trained | 100% | 4.76 | 10% | 0% | 2% | 9% |
| Documentation questions | no tool | qwen3-1.7b | 0% | 0 | 0% | 0% | 11% | 0% |
| Documentation questions | no tool | trained | 0% | 0 | 0% | 0% | 3% | 0% |
| Documentation questions | Python tool | qwen3-1.7b | 98% | 10.83 | 52% | 35% | 48% | 19% |
| Documentation questions | Python tool | trained | 98% | 12.39 | 59% | 0% | 6% | 16% |
| Aimed questions | no tool | qwen3-1.7b | 0% | 0 | 0% | 0% | 8% | 0% |
| Aimed questions | no tool | trained | 0% | 0 | 0% | 0% | 2% | 0% |
| Aimed questions | Python tool | qwen3-1.7b | 100% | 7.68 | 51% | 27% | 50% | 8% |
| Aimed questions | Python tool | trained | 97% | 13.34 | 47% | 0% | 5% | 19% |
