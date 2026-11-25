# Spider dev with the SQL tool: `qwen3-1.7b-rec17-f3`

20 of 20 databases run, 964 questions, one run. Right: 184 (19%). An answer is right when it gives the same rows as the gold query (out/downstream/spider/tasks.md). right: 184, answered with an error: 9, no answer (step limit or full context): 263, another wrong answer: 508; 16.9 tool calls per question.

| Database | Questions | Right | No answer | Tool calls |
| --- | --- | --- | --- | --- |
| `battle_death` | 16 | 1 (6%) | 6 | 361 |
| `car_1` | 78 | 14 (18%) | 25 | 1392 |
| `concert_singer` | 45 | 13 (29%) | 18 | 874 |
| `course_teach` | 30 | 10 (33%) | 4 | 315 |
| `cre_Doc_Template_Mgt` | 84 | 21 (25%) | 15 | 1211 |
| `dog_kennels` | 80 | 12 (15%) | 34 | 1750 |
| `employee_hire_evaluation` | 38 | 2 (5%) | 6 | 530 |
| `flight_2` | 76 | 21 (28%) | 26 | 1477 |
| `museum_visit` | 18 | 2 (11%) | 4 | 294 |
| `network_1` | 56 | 8 (14%) | 7 | 775 |
| `orchestra` | 40 | 9 (22%) | 13 | 732 |
| `pets_1` | 38 | 4 (11%) | 10 | 676 |
| `poker_player` | 40 | 8 (20%) | 17 | 878 |
| `real_estate_properties` | 4 | 2 (50%) | 0 | 42 |
| `singer` | 30 | 12 (40%) | 0 | 135 |
| `student_transcripts_tracking` | 78 | 12 (15%) | 21 | 1353 |
| `tvshow` | 62 | 6 (10%) | 11 | 943 |
| `voter_1` | 15 | 2 (13%) | 3 | 202 |
| `world_1` | 90 | 11 (12%) | 30 | 1632 |
| `wta_1` | 46 | 14 (30%) | 13 | 689 |
