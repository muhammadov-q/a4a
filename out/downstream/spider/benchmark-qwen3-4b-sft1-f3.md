# Spider dev with the SQL tool: `qwen3-4b-sft1-f3`

20 of 20 databases run, 964 questions, one run. Right: 241 (25%). An answer is right when it gives the same rows as the gold query (out/downstream/spider/tasks.md). right: 241, answered with an error: 5, no answer (step limit or full context): 610, another wrong answer: 108; 26.1 tool calls per question.

| Database | Questions | Right | No answer | Tool calls |
| --- | --- | --- | --- | --- |
| `battle_death` | 16 | 1 (6%) | 12 | 510 |
| `car_1` | 78 | 28 (36%) | 33 | 1292 |
| `concert_singer` | 45 | 20 (44%) | 23 | 973 |
| `course_teach` | 30 | 11 (37%) | 13 | 562 |
| `cre_Doc_Template_Mgt` | 84 | 16 (19%) | 58 | 2379 |
| `dog_kennels` | 80 | 19 (24%) | 55 | 2268 |
| `employee_hire_evaluation` | 38 | 10 (26%) | 27 | 1120 |
| `flight_2` | 76 | 12 (16%) | 55 | 2283 |
| `museum_visit` | 18 | 3 (17%) | 14 | 573 |
| `network_1` | 56 | 12 (21%) | 38 | 1605 |
| `orchestra` | 40 | 15 (38%) | 23 | 954 |
| `pets_1` | 38 | 9 (24%) | 27 | 1112 |
| `poker_player` | 40 | 10 (25%) | 24 | 999 |
| `real_estate_properties` | 4 | 0 (0%) | 3 | 127 |
| `singer` | 30 | 12 (40%) | 13 | 539 |
| `student_transcripts_tracking` | 78 | 11 (14%) | 62 | 2486 |
| `tvshow` | 62 | 14 (23%) | 41 | 1703 |
| `voter_1` | 15 | 4 (27%) | 8 | 335 |
| `world_1` | 90 | 16 (18%) | 55 | 2243 |
| `wta_1` | 46 | 18 (39%) | 26 | 1075 |
