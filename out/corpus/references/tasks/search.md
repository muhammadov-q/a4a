# The search reference for out/corpus/tasks/

Per question, a word search (BM25) over the library's API finds 8 elements; their signatures and the start of their documentation go under the question. Names used: the names of the elements of the verified answer that a reference can show (functions, methods, properties and classes; not operators). A name counts as found if the search found an element of that name: the scan cannot tell `G.degree` of a `Graph` from that of a `DiGraph`, so it lists both.

| Package | API elements | Questions | Names used | Found by the search | Questions with every used name found | Characters per reference |
| --- | --- | --- | --- | --- | --- | --- |
| `dateutil` | 80 | 11 | 23 | 12 (52%) | 2 of 11 | 2649 |
| `mcp` | 598 | 15 | 21 | 19 (90%) | 13 of 15 | 3290 |
| `more_itertools` | 182 | 19 | 25 | 21 (84%) | 15 of 19 | 3247 |
| `networkx` | 1217 | 20 | 64 | 33 (52%) | 2 of 20 | 3644 |
| `jinja2` | 560 | 9 | 14 | 9 (64%) | 5 of 9 | 2757 |
| `werkzeug` | 507 | 16 | 35 | 18 (51%) | 6 of 16 | 2505 |
| `packaging` | 116 | 28 | 64 | 27 (42%) | 6 of 28 | 3159 |
| `rsa` | 51 | 17 | 21 | 15 (71%) | 12 of 17 | 2690 |
| **all** | | **135** | **267** | **154 (58%)** | **61 of 135** | |
