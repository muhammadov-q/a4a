# Spider dev with the SQL tool: `qwen3-1.7b-rec17-f2`

20 of 20 databases run, 964 questions, one run. Right: 332 (34%). An answer is right when it gives the same rows as the gold query (out/downstream/spider/tasks.md). right: 332, answered with an error: 0, no answer (step limit or full context): 302, another wrong answer: 330; 14.5 tool calls per question.

| Database | Questions | Right | No answer | Tool calls |
| --- | --- | --- | --- | --- |
| `battle_death` | 16 | 6 (38%) | 10 | 420 |
| `car_1` | 78 | 24 (31%) | 26 | 1266 |
| `concert_singer` | 45 | 12 (27%) | 17 | 764 |
| `course_teach` | 30 | 12 (40%) | 8 | 386 |
| `cre_Doc_Template_Mgt` | 84 | 34 (40%) | 18 | 895 |
| `dog_kennels` | 80 | 17 (21%) | 36 | 1382 |
| `employee_hire_evaluation` | 38 | 12 (32%) | 14 | 630 |
| `flight_2` | 76 | 41 (54%) | 14 | 795 |
| `museum_visit` | 18 | 6 (33%) | 2 | 132 |
| `network_1` | 56 | 22 (39%) | 16 | 764 |
| `orchestra` | 40 | 19 (48%) | 7 | 360 |
| `pets_1` | 38 | 13 (34%) | 10 | 506 |
| `poker_player` | 40 | 13 (32%) | 18 | 826 |
| `real_estate_properties` | 4 | 2 (50%) | 2 | 86 |
| `singer` | 30 | 9 (30%) | 8 | 354 |
| `student_transcripts_tracking` | 78 | 17 (22%) | 40 | 1637 |
| `tvshow` | 62 | 24 (39%) | 11 | 709 |
| `voter_1` | 15 | 4 (27%) | 5 | 277 |
| `world_1` | 90 | 28 (31%) | 21 | 1019 |
| `wta_1` | 46 | 17 (37%) | 19 | 768 |
