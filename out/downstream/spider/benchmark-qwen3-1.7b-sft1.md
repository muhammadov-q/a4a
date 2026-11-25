# Spider dev with the SQL tool: `qwen3-1.7b-sft1`

20 of 20 databases run, 964 questions, one run. Right: 278 (29%). An answer is right when it gives the same rows as the gold query (out/downstream/spider/tasks.md). right: 278, answered with an error: 5, no answer (step limit or full context): 460, another wrong answer: 221; 20.1 tool calls per question.

| Database | Questions | Right | No answer | Tool calls |
| --- | --- | --- | --- | --- |
| `battle_death` | 16 | 5 (31%) | 9 | 383 |
| `car_1` | 78 | 22 (28%) | 33 | 1455 |
| `concert_singer` | 45 | 15 (33%) | 22 | 938 |
| `course_teach` | 30 | 12 (40%) | 8 | 386 |
| `cre_Doc_Template_Mgt` | 84 | 28 (33%) | 39 | 1654 |
| `dog_kennels` | 80 | 16 (20%) | 39 | 1598 |
| `employee_hire_evaluation` | 38 | 15 (39%) | 17 | 754 |
| `flight_2` | 76 | 33 (43%) | 31 | 1386 |
| `museum_visit` | 18 | 6 (33%) | 9 | 389 |
| `network_1` | 56 | 16 (29%) | 33 | 1392 |
| `orchestra` | 40 | 15 (38%) | 16 | 707 |
| `pets_1` | 38 | 9 (24%) | 24 | 1007 |
| `poker_player` | 40 | 9 (22%) | 20 | 857 |
| `real_estate_properties` | 4 | 1 (25%) | 1 | 57 |
| `singer` | 30 | 12 (40%) | 10 | 435 |
| `student_transcripts_tracking` | 78 | 15 (19%) | 49 | 1805 |
| `tvshow` | 62 | 17 (27%) | 22 | 1009 |
| `voter_1` | 15 | 3 (20%) | 9 | 378 |
| `world_1` | 90 | 18 (20%) | 43 | 1776 |
| `wta_1` | 46 | 11 (24%) | 26 | 1030 |
