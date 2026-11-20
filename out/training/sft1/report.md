# Training data `sft1`

Teachers: qwen3-32b, qwen3-8b. Runs: bench2, aimed1, db1, the harness that repairs calls. Test sources: 30% of each kind, seed 1.

| Source | Kind | Split | Runs used | Questions with an example | Examples | Questions to test on |
| --- | --- | --- | --- | --- | --- | --- |
| chinook | database | test | 0 | 0 | 0 | 40 tasks |
| northwind | database | train | 2 | 39 | 149 |  |
| sakila | database | train | 2 | 38 | 144 |  |
| dateutil__dateutil | repository | test | 0 | 0 | 0 | 11 tasks, 14 tasks-aimed |
| more-itertools__more-itertools | repository | train | 8 | 18 | 150 |  |
| networkx__networkx | repository | train | 8 | 28 | 220 |  |
| pallets__jinja | repository | train | 8 | 5 | 44 |  |
| pallets__werkzeug | repository | test | 0 | 0 | 0 | 16 tasks, 13 tasks-aimed |
| pypa__packaging | repository | train | 8 | 23 | 145 |  |
| sybrenstuvel__python-rsa | repository | train | 8 | 18 | 145 |  |

**997 examples** from 169 questions of 7 sources.
Left out: 275 runs with a wrong answer; 97 steps with a failed call; 19 runs that needed the reminder.
A step whose call failed stays in the history of the later steps of its run.
Examples that repeat an earlier one are counted once.
