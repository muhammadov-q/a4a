# Recovery examples `rec17`

The runs of `qwen3-1.7b` (run 1) are cut right after the first failed call; `qwen3-32b` goes on from there. Saved as the sets `<set>rec17`.

| Set | Source | Student's runs | With a failed call | Student right anyway | Teacher went on | Teacher right |
| --- | --- | --- | --- | --- | --- | --- |
| bench2 | dateutil__dateutil | 11 | 9 | 2 | 9 | 3 |
| bench2 | more-itertools__more-itertools | 19 | 12 | 4 | 12 | 5 |
| bench2 | networkx__networkx | 20 | 13 | 2 | 13 | 5 |
| bench2 | pallets__jinja | 9 | 7 | 2 | 7 | 2 |
| bench2 | pallets__werkzeug | 16 | 11 | 2 | 11 | 6 |
| bench2 | pypa__packaging | 28 | 24 | 6 | 24 | 6 |
| bench2 | sybrenstuvel__python-rsa | 17 | 6 | 1 | 6 | 1 |
| aimed1 | dateutil__dateutil | 14 | 9 | 5 | 9 | 4 |
| aimed1 | more-itertools__more-itertools | 5 | 4 | 1 | 4 | 2 |
| aimed1 | networkx__networkx | 14 | 8 | 3 | 8 | 3 |
| aimed1 | pallets__jinja | 3 | 3 | 0 | 3 | 0 |
| aimed1 | pallets__werkzeug | 13 | 10 | 2 | 10 | 2 |
| aimed1 | pypa__packaging | 10 | 8 | 2 | 8 | 1 |
| aimed1 | sybrenstuvel__python-rsa | 3 | 3 | 1 | 3 | 2 |
| db1 | chinook | 40 | 9 | 5 | 9 | 2 |
| db1 | northwind | 39 | 9 | 0 | 9 | 8 |
| db1 | sakila | 39 | 2 | 1 | 2 | 0 |
| **all** | | **300** | **147** | **39** | **147** | **52** |
