# Spider dev with the SQL tool: `qwen3-1.7b`

20 of 20 databases run, 964 questions, one run. Right: 128 (13%). An answer is right when it gives the same rows as the gold query (out/downstream/spider/tasks.md). right: 128, answered with an error: 120, no answer (step limit or full context): 36, another wrong answer: 680; 3.3 tool calls per question.

| Database | Questions | Right | No answer | Tool calls |
| --- | --- | --- | --- | --- |
| `battle_death` | 16 | 1 (6%) | 1 | 80 |
| `car_1` | 78 | 1 (1%) | 3 | 185 |
| `concert_singer` | 45 | 8 (18%) | 1 | 145 |
| `course_teach` | 30 | 3 (10%) | 0 | 42 |
| `cre_Doc_Template_Mgt` | 84 | 19 (23%) | 2 | 199 |
| `dog_kennels` | 80 | 10 (12%) | 2 | 260 |
| `employee_hire_evaluation` | 38 | 2 (5%) | 1 | 147 |
| `flight_2` | 76 | 13 (17%) | 1 | 134 |
| `museum_visit` | 18 | 1 (6%) | 0 | 27 |
| `network_1` | 56 | 8 (14%) | 3 | 289 |
| `orchestra` | 40 | 8 (20%) | 1 | 109 |
| `pets_1` | 38 | 4 (11%) | 3 | 170 |
| `poker_player` | 40 | 7 (18%) | 3 | 205 |
| `real_estate_properties` | 4 | 0 (0%) | 0 | 4 |
| `singer` | 30 | 10 (33%) | 0 | 105 |
| `student_transcripts_tracking` | 78 | 10 (13%) | 4 | 406 |
| `tvshow` | 62 | 3 (5%) | 0 | 102 |
| `voter_1` | 15 | 2 (13%) | 1 | 59 |
| `world_1` | 90 | 4 (4%) | 8 | 453 |
| `wta_1` | 46 | 14 (30%) | 2 | 89 |
