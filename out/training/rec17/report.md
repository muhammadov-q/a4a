# Training data `rec17`

Teachers: qwen3-32b, qwen3-8b. Runs: bench2, aimed1, db1, bench2rec17, aimed1rec17, db1rec17, the harness that repairs calls. Test sources: 30% of each kind, seed 1; fold 1 of 3, in which every source is tested once (fold 1 is that split).

| Source | Kind | Split | Runs used | Questions with an example | Examples | Questions to test on |
| --- | --- | --- | --- | --- | --- | --- |
| chinook | database | test | 0 | 0 | 0 | 40 tasks |
| northwind | database | train | 3 | 39 | 166 |  |
| sakila | database | train | 3 | 38 | 144 |  |
| dateutil__dateutil | repository | test | 0 | 0 | 0 | 11 tasks, 14 tasks-aimed |
| more-itertools__more-itertools | repository | train | 10 | 19 | 164 |  |
| networkx__networkx | repository | train | 10 | 29 | 236 |  |
| pallets__jinja | repository | train | 10 | 6 | 47 |  |
| pallets__werkzeug | repository | test | 0 | 0 | 0 | 16 tasks, 13 tasks-aimed |
| pypa__packaging | repository | train | 10 | 25 | 159 |  |
| sybrenstuvel__python-rsa | repository | train | 10 | 18 | 151 |  |

**1067 examples** from 174 questions of 7 sources.
Left out: 339 runs with a wrong answer; 101 steps with a failed call; 19 runs that needed the reminder.
A step whose call failed stays in the history of the later steps of its run.
Examples that repeat an earlier one are counted once.
