# Training data `rec17-f3`

Teachers: qwen3-32b, qwen3-8b. Runs: bench2, aimed1, db1, bench2rec17, aimed1rec17, db1rec17, the harness that repairs calls. Test sources: 30% of each kind, seed 1; fold 3 of 3, in which every source is tested once (fold 1 is that split).

| Source | Kind | Split | Runs used | Questions with an example | Examples | Questions to test on |
| --- | --- | --- | --- | --- | --- | --- |
| chinook | database | train | 3 | 39 | 145 |  |
| northwind | database | test | 0 | 0 | 0 | 39 tasks |
| sakila | database | train | 3 | 38 | 144 |  |
| dateutil__dateutil | repository | train | 10 | 21 | 137 |  |
| more-itertools__more-itertools | repository | train | 10 | 19 | 164 |  |
| networkx__networkx | repository | train | 10 | 29 | 236 |  |
| pallets__jinja | repository | test | 0 | 0 | 0 | 9 tasks, 3 tasks-aimed |
| pallets__werkzeug | repository | train | 10 | 24 | 211 |  |
| pypa__packaging | repository | train | 10 | 25 | 159 |  |
| sybrenstuvel__python-rsa | repository | test | 0 | 0 | 0 | 17 tasks, 3 tasks-aimed |

**1196 examples** from 195 questions of 7 sources.
Left out: 337 runs with a wrong answer; 114 steps with a failed call; 24 runs that needed the reminder.
A step whose call failed stays in the history of the later steps of its run.
Examples that repeat an earlier one are counted once.
