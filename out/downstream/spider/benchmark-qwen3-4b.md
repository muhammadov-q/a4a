# Spider dev with the SQL tool: `qwen3-4b`

20 of 20 databases run, 964 questions, one run. Right: 162 (17%). An answer is right when it gives the same rows as the gold query (out/downstream/spider/tasks.md). right: 162, answered with an error: 266, no answer (step limit or full context): 127, another wrong answer: 409; 7.7 tool calls per question.

| Database | Questions | Right | No answer | Tool calls |
| --- | --- | --- | --- | --- |
| `battle_death` | 16 | 0 (0%) | 6 | 302 |
| `car_1` | 78 | 5 (6%) | 10 | 614 |
| `concert_singer` | 45 | 6 (13%) | 10 | 489 |
| `course_teach` | 30 | 6 (20%) | 1 | 123 |
| `cre_Doc_Template_Mgt` | 84 | 16 (19%) | 4 | 342 |
| `dog_kennels` | 80 | 12 (15%) | 8 | 543 |
| `employee_hire_evaluation` | 38 | 4 (11%) | 4 | 239 |
| `flight_2` | 76 | 25 (33%) | 20 | 955 |
| `museum_visit` | 18 | 1 (6%) | 2 | 126 |
| `network_1` | 56 | 5 (9%) | 5 | 323 |
| `orchestra` | 40 | 2 (5%) | 4 | 269 |
| `pets_1` | 38 | 4 (11%) | 3 | 213 |
| `poker_player` | 40 | 9 (22%) | 8 | 389 |
| `real_estate_properties` | 4 | 0 (0%) | 2 | 87 |
| `singer` | 30 | 13 (43%) | 1 | 98 |
| `student_transcripts_tracking` | 78 | 9 (12%) | 8 | 583 |
| `tvshow` | 62 | 4 (6%) | 4 | 299 |
| `voter_1` | 15 | 3 (20%) | 2 | 112 |
| `world_1` | 90 | 20 (22%) | 20 | 991 |
| `wta_1` | 46 | 18 (39%) | 5 | 303 |
