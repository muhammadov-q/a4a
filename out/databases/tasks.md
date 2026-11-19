# Exercises in plain words, from database queries

118 exercises from 3 databases. The answer of each is the verified result of a query made from a template; an LLM wrote only the request. Kept only if a second model, given the request and the schema, wrote a query that gives that answer in the sandbox.

| Database | Verified exercises | Chosen | Request written | Solvable from the request (kept) |
| --- | --- | --- | --- | --- |
| `chinook` | 128 | 40 | 40 | 40 |
| `northwind` | 165 | 40 | 40 | 39 |
| `sakila` | 163 | 40 | 40 | 39 |

## By template

| Template | What it asks | Chosen | Kept |
| --- | --- | --- | --- |
| rows | the number of rows of a table | 26 | 26 |
| distinct | the number of different values of a column | 26 | 26 |
| range | the smallest and the largest value of a column | 18 | 18 |
| filter | the number of rows with a column's most frequent value | 26 | 26 |
| most | along a foreign key, the parent row with the most child rows | 24 | 22 |
