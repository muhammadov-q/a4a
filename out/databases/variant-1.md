# Database variants (seed 1, each row kept with probability 0.7)

The same questions on a copy of each database with part of its rows removed. A question whose answer changed can tell memory from skill: a model that answers from memory gives the old answer.

| Database | Rows before | Rows after | Questions | Answer changed | Answer the same | No answer on the variant |
| --- | --- | --- | --- | --- | --- | --- |
| `chinook` | 15,607 | 10,923 | 40 | 28 | 11 | 1 |
| `northwind` | 625,890 | 438,150 | 39 | 25 | 14 | 0 |
| `sakila` | 46,273 | 32,211 | 39 | 29 | 9 | 1 |

Together: 82 questions with a changed answer, 34 with the same answer.

## By template

| Template | Questions | Answer changed |
| --- | --- | --- |
| rows | 26 | 24 |
| distinct | 26 | 18 |
| filter | 26 | 20 |
| range | 18 | 1 |
| most | 20 | 19 |
