# Spider dev with the SQL tool: `qwen3-1.7b-rec17`

20 of 20 databases run, 964 questions, one run. Right: 214 (22%). An answer is right when it gives the same rows as the gold query (out/downstream/spider/tasks.md). right: 214, answered with an error: 3, no answer (step limit or full context): 502, another wrong answer: 245; 21.7 tool calls per question.

| Database | Questions | Right | No answer | Tool calls |
| --- | --- | --- | --- | --- |
| `battle_death` | 16 | 2 (12%) | 12 | 494 |
| `car_1` | 78 | 23 (29%) | 27 | 1231 |
| `concert_singer` | 45 | 6 (13%) | 26 | 1075 |
| `course_teach` | 30 | 6 (20%) | 17 | 716 |
| `cre_Doc_Template_Mgt` | 84 | 23 (27%) | 37 | 1592 |
| `dog_kennels` | 80 | 18 (22%) | 40 | 1570 |
| `employee_hire_evaluation` | 38 | 5 (13%) | 26 | 1072 |
| `flight_2` | 76 | 27 (36%) | 34 | 1488 |
| `museum_visit` | 18 | 4 (22%) | 10 | 427 |
| `network_1` | 56 | 12 (21%) | 35 | 1472 |
| `orchestra` | 40 | 8 (20%) | 19 | 809 |
| `pets_1` | 38 | 9 (24%) | 20 | 861 |
| `poker_player` | 40 | 8 (20%) | 21 | 880 |
| `real_estate_properties` | 4 | 0 (0%) | 2 | 82 |
| `singer` | 30 | 11 (37%) | 8 | 366 |
| `student_transcripts_tracking` | 78 | 13 (17%) | 42 | 1780 |
| `tvshow` | 62 | 17 (27%) | 29 | 1270 |
| `voter_1` | 15 | 3 (20%) | 10 | 412 |
| `world_1` | 90 | 5 (6%) | 61 | 2415 |
| `wta_1` | 46 | 14 (30%) | 26 | 951 |
