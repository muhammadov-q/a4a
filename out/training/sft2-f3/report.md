# Training data `sft2-f3`

Teachers: qwen3-32b, qwen3-8b. Runs: bench2, aimed1, db1, the harness that repairs calls. Test sources: 30% of each kind, seed 1; fold 3 of 3, in which every source is tested once (fold 1 is that split).

| Source | Kind | Split | Runs used | Questions with an example | Examples | Questions to test on |
| --- | --- | --- | --- | --- | --- | --- |
| chinook | database | train | 2 | 39 | 146 |  |
| northwind | database | test | 0 | 0 | 0 | 39 tasks |
| sakila | database | train | 2 | 38 | 144 |  |
| dateutil__dateutil | repository | train | 8 | 20 | 129 |  |
| more-itertools__more-itertools | repository | train | 8 | 18 | 175 |  |
| networkx__networkx | repository | train | 8 | 28 | 244 |  |
| pallets__jinja | repository | test | 0 | 0 | 0 | 9 tasks, 3 tasks-aimed |
| pallets__werkzeug | repository | train | 8 | 24 | 214 |  |
| pypa__packaging | repository | train | 8 | 23 | 177 |  |
| sybrenstuvel__python-rsa | repository | test | 0 | 0 | 0 | 17 tasks, 3 tasks-aimed |

**1229 examples** from 190 questions of 7 sources.
Left out: 257 runs with a wrong answer; 24 runs that needed the reminder.
Examples that repeat an earlier one are counted once.
