# Exercises from databases

3 of 3 databases. Drafts come from templates over the schema, without a model. A draft is verified if two sandboxed runs give the same plain value; there is no documented result to compare with.

| Database | Tables | Columns | Rows | Lines of schema | Drafts | Verified | Per 1,000 rows | Per line of schema | Tables and columns covered |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| `chinook` | 11 | 64 | 15,607 | 140 | 128 | 128 | 8.2 | 0.91 | 75 of 75 (100%) |
| `northwind` | 13 | 88 | 625,890 | 336 | 165 | 165 | 0.3 | 0.49 | 95 of 101 (94%) |
| `sakila` | 16 | 89 | 46,273 | 378 | 164 | 163 | 3.5 | 0.43 | 101 of 105 (96%) |

## By template

| Template | What it asks | Drafts | Verified |
| --- | --- | --- | --- |
| rows | the number of rows of a table | 37 | 37 |
| distinct | the number of different values of a column | 234 | 234 |
| range | the smallest and the largest value of a column | 18 | 18 |
| filter | the number of rows with a column's most frequent value | 124 | 124 |
| most | along a foreign key, the parent row with the most child rows | 44 | 43 |

What happened to the drafts: verified 456, error 1.

## Not covered

Tables and columns that no verified exercise uses (an empty table, or values that are not plain JSON):

- `northwind`: `CustomerCustomerDemo`, `CustomerCustomerDemo.CustomerID`, `CustomerCustomerDemo.CustomerTypeID`, `CustomerDemographics`, `CustomerDemographics.CustomerDesc`, `CustomerDemographics.CustomerTypeID`
- `sakila`: `film_text`, `film_text.description`, `film_text.film_id`, `film_text.title`
