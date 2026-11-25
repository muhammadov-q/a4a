# Spider dev with the SQL tool: `qwen3-8b`

20 of 20 databases run, 964 questions, one run. Right: 413 (43%). An answer is right when it gives the same rows as the gold query (out/downstream/spider/tasks.md). right: 413, answered with an error: 163, no answer (step limit or full context): 60, another wrong answer: 328; 7.1 tool calls per question.

| Database | Questions | Right | No answer | Tool calls |
| --- | --- | --- | --- | --- |
| `battle_death` | 16 | 7 (44%) | 2 | 166 |
| `car_1` | 78 | 30 (38%) | 7 | 644 |
| `concert_singer` | 45 | 18 (40%) | 2 | 246 |
| `course_teach` | 30 | 15 (50%) | 1 | 179 |
| `cre_Doc_Template_Mgt` | 84 | 43 (51%) | 1 | 348 |
| `dog_kennels` | 80 | 22 (28%) | 6 | 635 |
| `employee_hire_evaluation` | 38 | 22 (58%) | 1 | 225 |
| `flight_2` | 76 | 41 (54%) | 8 | 653 |
| `museum_visit` | 18 | 6 (33%) | 0 | 127 |
| `network_1` | 56 | 21 (38%) | 4 | 428 |
| `orchestra` | 40 | 16 (40%) | 0 | 194 |
| `pets_1` | 38 | 17 (45%) | 7 | 558 |
| `poker_player` | 40 | 21 (52%) | 1 | 162 |
| `real_estate_properties` | 4 | 0 (0%) | 0 | 15 |
| `singer` | 30 | 19 (63%) | 4 | 321 |
| `student_transcripts_tracking` | 78 | 27 (35%) | 4 | 554 |
| `tvshow` | 62 | 22 (35%) | 1 | 370 |
| `voter_1` | 15 | 6 (40%) | 0 | 82 |
| `world_1` | 90 | 36 (40%) | 7 | 634 |
| `wta_1` | 46 | 24 (52%) | 4 | 277 |
