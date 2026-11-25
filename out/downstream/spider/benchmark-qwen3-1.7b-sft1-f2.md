# Spider dev with the SQL tool: `qwen3-1.7b-sft1-f2`

20 of 20 databases run, 964 questions, one run. Right: 203 (21%). An answer is right when it gives the same rows as the gold query (out/downstream/spider/tasks.md). right: 203, answered with an error: 18, no answer (step limit or full context): 185, another wrong answer: 558; 13.0 tool calls per question.

| Database | Questions | Right | No answer | Tool calls |
| --- | --- | --- | --- | --- |
| `battle_death` | 16 | 2 (12%) | 5 | 277 |
| `car_1` | 78 | 10 (13%) | 17 | 1201 |
| `concert_singer` | 45 | 12 (27%) | 7 | 568 |
| `course_teach` | 30 | 4 (13%) | 4 | 333 |
| `cre_Doc_Template_Mgt` | 84 | 15 (18%) | 11 | 957 |
| `dog_kennels` | 80 | 9 (11%) | 17 | 1033 |
| `employee_hire_evaluation` | 38 | 5 (13%) | 9 | 525 |
| `flight_2` | 76 | 38 (50%) | 11 | 889 |
| `museum_visit` | 18 | 1 (6%) | 6 | 319 |
| `network_1` | 56 | 15 (27%) | 11 | 754 |
| `orchestra` | 40 | 14 (35%) | 6 | 418 |
| `pets_1` | 38 | 3 (8%) | 11 | 644 |
| `poker_player` | 40 | 8 (20%) | 6 | 437 |
| `real_estate_properties` | 4 | 1 (25%) | 1 | 50 |
| `singer` | 30 | 8 (27%) | 4 | 275 |
| `student_transcripts_tracking` | 78 | 15 (19%) | 18 | 1150 |
| `tvshow` | 62 | 11 (18%) | 18 | 1065 |
| `voter_1` | 15 | 1 (7%) | 0 | 73 |
| `world_1` | 90 | 18 (20%) | 15 | 1085 |
| `wta_1` | 46 | 13 (28%) | 8 | 520 |
