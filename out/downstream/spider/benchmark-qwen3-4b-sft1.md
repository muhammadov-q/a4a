# Spider dev with the SQL tool: `qwen3-4b-sft1`

20 of 20 databases run, 964 questions, one run. Right: 217 (23%). An answer is right when it gives the same rows as the gold query (out/downstream/spider/tasks.md). right: 217, answered with an error: 169, no answer (step limit or full context): 426, another wrong answer: 152; 20.1 tool calls per question.

| Database | Questions | Right | No answer | Tool calls |
| --- | --- | --- | --- | --- |
| `battle_death` | 16 | 1 (6%) | 4 | 184 |
| `car_1` | 78 | 12 (15%) | 16 | 840 |
| `concert_singer` | 45 | 15 (33%) | 21 | 981 |
| `course_teach` | 30 | 5 (17%) | 7 | 360 |
| `cre_Doc_Template_Mgt` | 84 | 20 (24%) | 24 | 1233 |
| `dog_kennels` | 80 | 17 (21%) | 47 | 2025 |
| `employee_hire_evaluation` | 38 | 13 (34%) | 13 | 639 |
| `flight_2` | 76 | 11 (14%) | 49 | 2091 |
| `museum_visit` | 18 | 3 (17%) | 7 | 349 |
| `network_1` | 56 | 14 (25%) | 18 | 1009 |
| `orchestra` | 40 | 12 (30%) | 15 | 768 |
| `pets_1` | 38 | 12 (32%) | 20 | 874 |
| `poker_player` | 40 | 11 (28%) | 22 | 931 |
| `real_estate_properties` | 4 | 2 (50%) | 0 | 14 |
| `singer` | 30 | 13 (43%) | 11 | 461 |
| `student_transcripts_tracking` | 78 | 11 (14%) | 48 | 2024 |
| `tvshow` | 62 | 11 (18%) | 25 | 1172 |
| `voter_1` | 15 | 4 (27%) | 9 | 369 |
| `world_1` | 90 | 15 (17%) | 45 | 2007 |
| `wta_1` | 46 | 15 (33%) | 25 | 1046 |
