# Recovery examples `rec4`

The runs of `qwen3-4b` (run 1) are cut right after the first failed call; `qwen3-32b` goes on from there. Saved as the sets `<set>rec4`.

| Set | Source | Student's runs | With a failed call | Student right anyway | Teacher went on | Teacher right |
| --- | --- | --- | --- | --- | --- | --- |
| bench2 | dateutil__dateutil | 11 | 7 | 2 | 7 | 1 |
| bench2 | more-itertools__more-itertools | 19 | 6 | 2 | 6 | 1 |
| bench2 | networkx__networkx | 20 | 10 | 6 | 10 | 5 |
| bench2 | pallets__jinja | 9 | 6 | 1 | 6 | 2 |
| bench2 | pallets__werkzeug | 16 | 2 | 2 | 2 | 1 |
| bench2 | pypa__packaging | 28 | 27 | 11 | 27 | 5 |
| bench2 | sybrenstuvel__python-rsa | 17 | 8 | 4 | 8 | 1 |
| aimed1 | dateutil__dateutil | 14 | 9 | 3 | 9 | 1 |
| aimed1 | more-itertools__more-itertools | 5 | 4 | 2 | 4 | 1 |
| aimed1 | networkx__networkx | 14 | 10 | 6 | 10 | 3 |
| aimed1 | pallets__jinja | 3 | 2 | 0 | 2 | 0 |
| aimed1 | pallets__werkzeug | 13 | 7 | 2 | 7 | 2 |
| aimed1 | pypa__packaging | 10 | 4 | 2 | 4 | 0 |
| aimed1 | sybrenstuvel__python-rsa | 3 | 3 | 2 | 3 | 2 |
| db1 | chinook | 40 | 6 | 1 | 6 | 0 |
| db1 | northwind | 39 | 1 | 0 | 1 | 1 |
| db1 | sakila | 39 | 0 | 0 | 0 | 0 |
| **all** | | **300** | **112** | **46** | **112** | **26** |
