# Training data `rec17-f2`

Teachers: qwen3-32b, qwen3-8b. Runs: bench2, aimed1, db1, bench2rec17, aimed1rec17, db1rec17, the harness that repairs calls. Test sources: 30% of each kind, seed 1; fold 2 of 3, in which every source is tested once (fold 1 is that split).

| Source | Kind | Split | Runs used | Questions with an example | Examples | Questions to test on |
| --- | --- | --- | --- | --- | --- | --- |
| chinook | database | train | 3 | 39 | 145 |  |
| northwind | database | train | 3 | 39 | 166 |  |
| sakila | database | test | 0 | 0 | 0 | 39 tasks |
| dateutil__dateutil | repository | train | 10 | 21 | 137 |  |
| more-itertools__more-itertools | repository | test | 0 | 0 | 0 | 19 tasks, 5 tasks-aimed |
| networkx__networkx | repository | test | 0 | 0 | 0 | 20 tasks, 14 tasks-aimed |
| pallets__jinja | repository | train | 10 | 6 | 47 |  |
| pallets__werkzeug | repository | train | 10 | 24 | 211 |  |
| pypa__packaging | repository | test | 0 | 0 | 0 | 28 tasks, 10 tasks-aimed |
| sybrenstuvel__python-rsa | repository | train | 10 | 18 | 151 |  |

**857 examples** from 147 questions of 6 sources.
Left out: 184 runs with a wrong answer; 49 steps with a failed call; 7 runs that needed the reminder.
A step whose call failed stays in the history of the later steps of its run.
Examples that repeat an earlier one are counted once.
