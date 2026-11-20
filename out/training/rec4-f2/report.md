# Training data `rec4-f2`

Teachers: qwen3-32b, qwen3-8b. Runs: bench2, aimed1, db1, bench2rec4, aimed1rec4, db1rec4, the harness that repairs calls. Test sources: 30% of each kind, seed 1; fold 2 of 3, in which every source is tested once (fold 1 is that split).

| Source | Kind | Split | Runs used | Questions with an example | Examples | Questions to test on |
| --- | --- | --- | --- | --- | --- | --- |
| chinook | database | train | 3 | 39 | 141 |  |
| northwind | database | train | 3 | 39 | 152 |  |
| sakila | database | test | 0 | 0 | 0 | 39 tasks |
| dateutil__dateutil | repository | train | 10 | 21 | 128 |  |
| more-itertools__more-itertools | repository | test | 0 | 0 | 0 | 19 tasks, 5 tasks-aimed |
| networkx__networkx | repository | test | 0 | 0 | 0 | 20 tasks, 14 tasks-aimed |
| pallets__jinja | repository | train | 10 | 5 | 48 |  |
| pallets__werkzeug | repository | train | 10 | 25 | 203 |  |
| pypa__packaging | repository | test | 0 | 0 | 0 | 28 tasks, 10 tasks-aimed |
| sybrenstuvel__python-rsa | repository | train | 10 | 18 | 151 |  |

**823 examples** from 147 questions of 6 sources.
Left out: 178 runs with a wrong answer; 53 steps with a failed call; 7 runs that needed the reminder.
A step whose call failed stays in the history of the later steps of its run.
Examples that repeat an earlier one are counted once.
