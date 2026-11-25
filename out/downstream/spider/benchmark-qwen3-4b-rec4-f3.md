# Spider dev with the SQL tool: `qwen3-4b-rec4-f3`

20 of 20 databases run, 964 questions, one run. Right: 252 (26%). An answer is right when it gives the same rows as the gold query (out/downstream/spider/tasks.md). right: 252, answered with an error: 160, no answer (step limit or full context): 372, another wrong answer: 180; 18.5 tool calls per question.

| Database | Questions | Right | No answer | Tool calls |
| --- | --- | --- | --- | --- |
| `battle_death` | 16 | 0 (0%) | 3 | 210 |
| `car_1` | 78 | 29 (37%) | 19 | 1030 |
| `concert_singer` | 45 | 20 (44%) | 10 | 513 |
| `course_teach` | 30 | 12 (40%) | 4 | 275 |
| `cre_Doc_Template_Mgt` | 84 | 22 (26%) | 22 | 1235 |
| `dog_kennels` | 80 | 14 (18%) | 47 | 2044 |
| `employee_hire_evaluation` | 38 | 12 (32%) | 12 | 609 |
| `flight_2` | 76 | 12 (16%) | 36 | 1736 |
| `museum_visit` | 18 | 1 (6%) | 8 | 408 |
| `network_1` | 56 | 19 (34%) | 17 | 894 |
| `orchestra` | 40 | 10 (25%) | 11 | 578 |
| `pets_1` | 38 | 9 (24%) | 17 | 826 |
| `poker_player` | 40 | 8 (20%) | 17 | 766 |
| `real_estate_properties` | 4 | 1 (25%) | 0 | 26 |
| `singer` | 30 | 13 (43%) | 12 | 509 |
| `student_transcripts_tracking` | 78 | 9 (12%) | 47 | 2070 |
| `tvshow` | 62 | 15 (24%) | 23 | 1181 |
| `voter_1` | 15 | 5 (33%) | 7 | 306 |
| `world_1` | 90 | 22 (24%) | 42 | 1858 |
| `wta_1` | 46 | 19 (41%) | 18 | 781 |
