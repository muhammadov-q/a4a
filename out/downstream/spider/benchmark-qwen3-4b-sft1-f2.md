# Spider dev with the SQL tool: `qwen3-4b-sft1-f2`

20 of 20 databases run, 964 questions, one run. Right: 366 (38%). An answer is right when it gives the same rows as the gold query (out/downstream/spider/tasks.md). right: 366, answered with an error: 99, no answer (step limit or full context): 241, another wrong answer: 258; 13.1 tool calls per question.

| Database | Questions | Right | No answer | Tool calls |
| --- | --- | --- | --- | --- |
| `battle_death` | 16 | 8 (50%) | 1 | 120 |
| `car_1` | 78 | 22 (28%) | 24 | 936 |
| `concert_singer` | 45 | 23 (51%) | 12 | 623 |
| `course_teach` | 30 | 15 (50%) | 4 | 253 |
| `cre_Doc_Template_Mgt` | 84 | 32 (38%) | 18 | 1055 |
| `dog_kennels` | 80 | 28 (35%) | 29 | 1360 |
| `employee_hire_evaluation` | 38 | 19 (50%) | 5 | 361 |
| `flight_2` | 76 | 27 (36%) | 20 | 1111 |
| `museum_visit` | 18 | 6 (33%) | 7 | 322 |
| `network_1` | 56 | 21 (38%) | 10 | 595 |
| `orchestra` | 40 | 20 (50%) | 4 | 302 |
| `pets_1` | 38 | 10 (26%) | 6 | 523 |
| `poker_player` | 40 | 16 (40%) | 10 | 519 |
| `real_estate_properties` | 4 | 2 (50%) | 1 | 53 |
| `singer` | 30 | 14 (47%) | 7 | 335 |
| `student_transcripts_tracking` | 78 | 17 (22%) | 22 | 1246 |
| `tvshow` | 62 | 24 (39%) | 10 | 686 |
| `voter_1` | 15 | 8 (53%) | 3 | 171 |
| `world_1` | 90 | 34 (38%) | 27 | 1310 |
| `wta_1` | 46 | 20 (43%) | 21 | 728 |
