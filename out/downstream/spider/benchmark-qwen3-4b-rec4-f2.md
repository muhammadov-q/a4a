# Spider dev with the SQL tool: `qwen3-4b-rec4-f2`

20 of 20 databases run, 964 questions, one run. Right: 236 (24%). An answer is right when it gives the same rows as the gold query (out/downstream/spider/tasks.md). right: 236, answered with an error: 497, no answer (step limit or full context): 103, another wrong answer: 128; 8.5 tool calls per question.

| Database | Questions | Right | No answer | Tool calls |
| --- | --- | --- | --- | --- |
| `battle_death` | 16 | 2 (12%) | 1 | 114 |
| `car_1` | 78 | 23 (29%) | 3 | 437 |
| `concert_singer` | 45 | 17 (38%) | 2 | 254 |
| `course_teach` | 30 | 15 (50%) | 0 | 91 |
| `cre_Doc_Template_Mgt` | 84 | 24 (29%) | 4 | 467 |
| `dog_kennels` | 80 | 15 (19%) | 10 | 741 |
| `employee_hire_evaluation` | 38 | 14 (37%) | 0 | 162 |
| `flight_2` | 76 | 12 (16%) | 21 | 1173 |
| `museum_visit` | 18 | 2 (11%) | 1 | 140 |
| `network_1` | 56 | 7 (12%) | 0 | 220 |
| `orchestra` | 40 | 13 (32%) | 1 | 196 |
| `pets_1` | 38 | 7 (18%) | 6 | 413 |
| `poker_player` | 40 | 8 (20%) | 14 | 699 |
| `real_estate_properties` | 4 | 1 (25%) | 0 | 14 |
| `singer` | 30 | 12 (40%) | 1 | 115 |
| `student_transcripts_tracking` | 78 | 9 (12%) | 13 | 906 |
| `tvshow` | 62 | 15 (24%) | 1 | 312 |
| `voter_1` | 15 | 3 (20%) | 5 | 242 |
| `world_1` | 90 | 18 (20%) | 12 | 977 |
| `wta_1` | 46 | 19 (41%) | 8 | 509 |
