# The search reference for out/corpus/tasks-aimed/

Per question, a word search (BM25) over the library's API finds 8 elements; their signatures and the start of their documentation go under the question. Names used: the names of the elements of the verified answer that a reference can show (functions, methods, properties and classes; not operators). A name counts as found if the search found an element of that name: the scan cannot tell `G.degree` of a `Graph` from that of a `DiGraph`, so it lists both.

| Package | API elements | Questions | Names used | Found by the search | Questions with every used name found | Characters per reference |
| --- | --- | --- | --- | --- | --- | --- |
| `dateutil` | 80 | 14 | 25 | 16 (64%) | 6 of 14 | 2491 |
| `mcp` | 598 | 4 | 7 | 5 (71%) | 2 of 4 | 2172 |
| `more_itertools` | 182 | 5 | 7 | 6 (86%) | 4 of 5 | 3395 |
| `networkx` | 1217 | 14 | 44 | 15 (34%) | 2 of 14 | 3575 |
| `jinja2` | 560 | 3 | 9 | 3 (33%) | 0 of 3 | 1992 |
| `werkzeug` | 507 | 13 | 29 | 19 (66%) | 6 of 13 | 2459 |
| `packaging` | 116 | 10 | 16 | 11 (69%) | 5 of 10 | 3009 |
| `rsa` | 51 | 3 | 7 | 5 (71%) | 1 of 3 | 3212 |
| **all** | | **66** | **144** | **80 (56%)** | **26 of 66** | |
