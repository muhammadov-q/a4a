# Spider dev with the SQL tool: `qwen3-1.7b-sft1-f3`

20 of 20 databases run, 964 questions, one run. Right: 223 (23%). An answer is right when it gives the same rows as the gold query (out/downstream/spider/tasks.md). right: 223, answered with an error: 1, no answer (step limit or full context): 526, another wrong answer: 214; 22.6 tool calls per question.

| Database | Questions | Right | No answer | Tool calls |
| --- | --- | --- | --- | --- |
| `battle_death` | 16 | 2 (12%) | 11 | 454 |
| `car_1` | 78 | 7 (9%) | 48 | 2039 |
| `concert_singer` | 45 | 14 (31%) | 18 | 798 |
| `course_teach` | 30 | 12 (40%) | 10 | 454 |
| `cre_Doc_Template_Mgt` | 84 | 25 (30%) | 48 | 1995 |
| `dog_kennels` | 80 | 16 (20%) | 43 | 1572 |
| `employee_hire_evaluation` | 38 | 9 (24%) | 18 | 780 |
| `flight_2` | 76 | 15 (20%) | 48 | 2008 |
| `museum_visit` | 18 | 6 (33%) | 11 | 461 |
| `network_1` | 56 | 16 (29%) | 33 | 1396 |
| `orchestra` | 40 | 15 (38%) | 19 | 816 |
| `pets_1` | 38 | 6 (16%) | 28 | 1156 |
| `poker_player` | 40 | 10 (25%) | 21 | 893 |
| `real_estate_properties` | 4 | 1 (25%) | 2 | 86 |
| `singer` | 30 | 14 (47%) | 8 | 350 |
| `student_transcripts_tracking` | 78 | 10 (13%) | 50 | 2104 |
| `tvshow` | 62 | 17 (27%) | 29 | 1283 |
| `voter_1` | 15 | 3 (20%) | 9 | 391 |
| `world_1` | 90 | 11 (12%) | 49 | 1904 |
| `wta_1` | 46 | 14 (30%) | 23 | 839 |
