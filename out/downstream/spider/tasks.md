# Spider's dev questions, with answers from the gold query

964 of 1034 questions kept, on 20 databases. A question is kept when its gold query, run twice in the sandbox, gives the same plain rows, at most 20 of them. A model answers with a value; it is right when the value gives the same rows as the gold query (in order if the query orders them at the top level, columns in any order). This is close to Spider's execution match, not its official metric.

| Not kept | Questions |
| --- | --- |
| more than 20 rows | 38 |
| the result is too long for the worker | 30 |
| text that is not UTF-8 | 2 |

| Rows in the answer | Questions |
| --- | --- |
| 0 | 49 |
| 1 | 531 |
| 2 to 5 | 201 |
| 6 to 20 | 183 |

| Database | Questions | Kept | Ordered |
| --- | --- | --- | --- |
| `battle_death` | 16 | 16 | 2 |
| `car_1` | 92 | 78 | 16 |
| `concert_singer` | 45 | 45 | 10 |
| `course_teach` | 30 | 30 | 8 |
| `cre_Doc_Template_Mgt` | 84 | 84 | 12 |
| `dog_kennels` | 82 | 80 | 12 |
| `employee_hire_evaluation` | 38 | 38 | 12 |
| `flight_2` | 80 | 76 | 12 |
| `museum_visit` | 18 | 18 | 6 |
| `network_1` | 56 | 56 | 6 |
| `orchestra` | 40 | 40 | 14 |
| `pets_1` | 42 | 38 | 4 |
| `poker_player` | 40 | 40 | 16 |
| `real_estate_properties` | 4 | 4 | 0 |
| `singer` | 30 | 30 | 6 |
| `student_transcripts_tracking` | 78 | 78 | 30 |
| `tvshow` | 62 | 62 | 14 |
| `voter_1` | 15 | 15 | 3 |
| `world_1` | 120 | 90 | 26 |
| `wta_1` | 62 | 46 | 18 |

Spider is under CC BY-SA 4.0 (https://yale-lily.github.io/spider), and so are the files in this folder.
