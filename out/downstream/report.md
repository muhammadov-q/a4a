# Public benchmarks: does training on the verified tasks help or hurt elsewhere?

Spider dev (questions on SQLite databases, with the SQL tool; `out/downstream/spider/tasks.md`) and HumanEval (plain Python, no tools, pass@1). One run each, temperature 0, thinking off. A trained student is compared with its untrained base on the same questions: "only base / only trained" counts the questions only one of the two gets right, with the exact sign test.

| Model | Spider dev | Only base / only trained | HumanEval | Only base / only trained |
| --- | --- | --- | --- | --- |
| `qwen3-1.7b` | 128 of 964 (13%) |  | 114 of 164 (70%) |  |
| `qwen3-1.7b-rec17` | 214 of 964 (22%) | 56 / 142, p = 8.4e-10 | 107 of 164 (65%) | 14 / 7, p = 0.19 |
| `qwen3-1.7b-rec17-f2` | 332 of 964 (34%) | 40 / 244, p = 7.1e-37 | 104 of 164 (63%) | 18 / 8, p = 0.076 |
| `qwen3-1.7b-rec17-f3` | 184 of 964 (19%) | 67 / 123, p = 5.9e-05 | 104 of 164 (63%) | 18 / 8, p = 0.076 |
| `qwen3-1.7b-sft1` | 278 of 964 (29%) | 44 / 194, p = 1.2e-23 | 109 of 164 (66%) | 16 / 11, p = 0.44 |
| `qwen3-1.7b-sft1-f2` | 203 of 964 (21%) | 56 / 131, p = 4.2e-08 | 99 of 164 (60%) | 24 / 9, p = 0.014 |
| `qwen3-1.7b-sft1-f3` | 223 of 964 (23%) | 52 / 147, p = 1.1e-11 | 105 of 164 (64%) | 17 / 8, p = 0.11 |
| `qwen3-4b` | 162 of 964 (17%) |  | 129 of 164 (79%) |  |
| `qwen3-4b-rec4` | 189 of 964 (20%) | 52 / 79, p = 0.023 | 125 of 164 (76%) | 11 / 7, p = 0.48 |
| `qwen3-4b-rec4-f2` | 236 of 964 (24%) | 48 / 122, p = 1.3e-08 | 133 of 164 (81%) | 6 / 10, p = 0.45 |
| `qwen3-4b-rec4-f3` | 252 of 964 (26%) | 45 / 135, p = 1.2e-11 | 129 of 164 (79%) | 8 / 8, p = 1 |
| `qwen3-4b-sft1` | 217 of 964 (23%) | 55 / 110, p = 2.2e-05 | 124 of 164 (76%) | 10 / 5, p = 0.3 |
| `qwen3-4b-sft1-f2` | 366 of 964 (38%) | 40 / 244, p = 7.1e-37 | 125 of 164 (76%) | 13 / 9, p = 0.52 |
| `qwen3-4b-sft1-f3` | 241 of 964 (25%) | 49 / 128, p = 2.5e-09 | 129 of 164 (79%) | 7 / 7, p = 1 |
| `qwen3-8b` | 413 of 964 (43%) |  | 138 of 164 (84%) |  |

Mean over the folds (each fold's student saw different training sources and none of these benchmarks):

| Base | Recipe | Folds | Spider dev | HumanEval |
| --- | --- | --- | --- | --- |
| `qwen3-1.7b` | rec17 | 3 | 25% (19% to 34%) | 64% (63% to 65%) |
| `qwen3-1.7b` | sft1 | 3 | 24% (21% to 29%) | 64% (60% to 66%) |
| `qwen3-4b` | rec4 | 3 | 23% (20% to 26%) | 79% (76% to 81%) |
| `qwen3-4b` | sft1 | 3 | 28% (23% to 38%) | 77% (76% to 79%) |

What became of the Spider questions:

| Model | Right | Answered with an error | No answer (step limit or full context) | Another wrong answer | Tool calls per question |
| --- | --- | --- | --- | --- | --- |
| `qwen3-1.7b-rec17-f2` | 332 | 0 | 302 | 330 | 14.5 |
| `qwen3-1.7b-rec17-f3` | 184 | 9 | 263 | 508 | 16.9 |
| `qwen3-1.7b-rec17` | 214 | 3 | 502 | 245 | 21.7 |
| `qwen3-1.7b-sft1-f2` | 203 | 18 | 185 | 558 | 13.0 |
| `qwen3-1.7b-sft1-f3` | 223 | 1 | 526 | 214 | 22.6 |
| `qwen3-1.7b-sft1` | 278 | 5 | 460 | 221 | 20.1 |
| `qwen3-1.7b` | 128 | 120 | 36 | 680 | 3.3 |
| `qwen3-4b-rec4-f2` | 236 | 497 | 103 | 128 | 8.5 |
| `qwen3-4b-rec4-f3` | 252 | 160 | 372 | 180 | 18.5 |
| `qwen3-4b-rec4` | 189 | 492 | 177 | 106 | 12.4 |
| `qwen3-4b-sft1-f2` | 366 | 99 | 241 | 258 | 13.1 |
| `qwen3-4b-sft1-f3` | 241 | 5 | 610 | 108 | 26.1 |
| `qwen3-4b-sft1` | 217 | 169 | 426 | 152 | 20.1 |
| `qwen3-4b` | 162 | 266 | 127 | 409 | 7.7 |
| `qwen3-8b` | 413 | 163 | 60 | 328 | 7.1 |
