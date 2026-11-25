# Spider dev with the SQL tool: `qwen3-4b-rec4`

20 of 20 databases run, 964 questions, one run. Right: 189 (20%). An answer is right when it gives the same rows as the gold query (out/downstream/spider/tasks.md). right: 189, answered with an error: 492, no answer (step limit or full context): 177, another wrong answer: 106; 12.4 tool calls per question.

| Database | Questions | Right | No answer | Tool calls |
| --- | --- | --- | --- | --- |
| `battle_death` | 16 | 0 (0%) | 1 | 76 |
| `car_1` | 78 | 10 (13%) | 4 | 480 |
| `concert_singer` | 45 | 12 (27%) | 10 | 618 |
| `course_teach` | 30 | 5 (17%) | 0 | 99 |
| `cre_Doc_Template_Mgt` | 84 | 22 (26%) | 11 | 701 |
| `dog_kennels` | 80 | 17 (21%) | 24 | 1427 |
| `employee_hire_evaluation` | 38 | 8 (21%) | 0 | 197 |
| `flight_2` | 76 | 13 (17%) | 27 | 1471 |
| `museum_visit` | 18 | 4 (22%) | 2 | 216 |
| `network_1` | 56 | 6 (11%) | 0 | 360 |
| `orchestra` | 40 | 7 (18%) | 3 | 366 |
| `pets_1` | 38 | 9 (24%) | 8 | 505 |
| `poker_player` | 40 | 8 (20%) | 16 | 774 |
| `real_estate_properties` | 4 | 1 (25%) | 0 | 13 |
| `singer` | 30 | 12 (40%) | 2 | 251 |
| `student_transcripts_tracking` | 78 | 10 (13%) | 24 | 1580 |
| `tvshow` | 62 | 6 (10%) | 3 | 435 |
| `voter_1` | 15 | 3 (20%) | 6 | 283 |
| `world_1` | 90 | 20 (22%) | 21 | 1336 |
| `wta_1` | 46 | 16 (35%) | 15 | 752 |
