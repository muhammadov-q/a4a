# Do the distinct tool candidates saturate?

97 repositories, embedding model `qwen3-embedding-4b`, 10 random orders of the repositories. A candidate joins a group if its similarity to the group's first member is at least the threshold.

Exponent: b in groups = a * candidates^b. 1 means no repetition; smaller means later repositories repeat earlier ones. Distinct inside: the sum of the groups each repository has on its own, so the gap to Candidates is repetition inside repositories and the gap to Groups is repetition between them. Seen before: of the distinct things a repository has, the share an earlier repository already had, for repositories added early (second tenth) and late (last tenth).

## All candidates

| Level | Threshold | Candidates | Distinct inside | Groups | Exponent | Seen before, early | Seen before, late | k=1 | k=5 | k=10 | k=20 | k=40 | k=60 | k=80 | k=97 |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| low | 0.80 | 17,362 | 9,346 | 8,930 | 0.976 | 2% | 11% | 103 | 431 | 841 | 1,717 | 3,947 | 5,420 | 7,178 | 8,930 |
| low | 0.85 | 17,362 | 11,324 | 11,073 | 0.983 | 1% | 6% | 119 | 522 | 1,035 | 2,102 | 4,840 | 6,635 | 8,859 | 11,073 |
| low | 0.90 | 17,362 | 13,392 | 13,248 | 0.986 | 0% | 2% | 139 | 612 | 1,237 | 2,506 | 5,761 | 7,872 | 10,579 | 13,248 |
| medium | 0.80 | 19,140 | 10,693 | 10,168 | 0.977 | 2% | 12% | 122 | 481 | 965 | 1,978 | 4,530 | 6,188 | 8,197 | 10,168 |
| medium | 0.85 | 19,140 | 12,938 | 12,606 | 0.985 | 1% | 6% | 143 | 583 | 1,184 | 2,413 | 5,553 | 7,576 | 10,115 | 12,606 |
| medium | 0.90 | 19,140 | 15,131 | 14,946 | 0.988 | 1% | 3% | 166 | 677 | 1,409 | 2,851 | 6,558 | 8,920 | 11,983 | 14,946 |
| high | 0.80 | 1,112 | 634 | 629 | 1.009 | 0% | 0% | 7 | 32 | 62 | 115 | 269 | 378 | 496 | 629 |
| high | 0.85 | 1,112 | 769 | 766 | 1.004 | 0% | 0% | 9 | 40 | 77 | 139 | 326 | 459 | 606 | 766 |
| high | 0.90 | 1,112 | 940 | 939 | 0.996 | 0% | 0% | 11 | 50 | 97 | 172 | 398 | 560 | 743 | 939 |

## Candidates the repository's own documentation uses

| Level | Threshold | Candidates | Distinct inside | Groups | Exponent | Seen before, early | Seen before, late | k=1 | k=5 | k=10 | k=20 | k=40 | k=60 | k=80 | k=97 |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| low | 0.80 | 1,611 | 1,108 | 1,086 | 0.978 | 0% | 3% | 13 | 48 | 95 | 212 | 472 | 707 | 892 | 1,086 |
| low | 0.85 | 1,611 | 1,248 | 1,236 | 0.991 | 0% | 1% | 14 | 54 | 105 | 241 | 533 | 803 | 1,016 | 1,236 |
| low | 0.90 | 1,611 | 1,387 | 1,382 | 0.995 | 0% | 0% | 15 | 59 | 116 | 271 | 594 | 896 | 1,133 | 1,382 |
| medium | 0.80 | 1,899 | 1,330 | 1,299 | 0.982 | 0% | 3% | 17 | 60 | 116 | 252 | 561 | 838 | 1,060 | 1,299 |
| medium | 0.85 | 1,899 | 1,500 | 1,483 | 0.991 | 0% | 1% | 19 | 67 | 130 | 287 | 635 | 954 | 1,210 | 1,483 |
| medium | 0.90 | 1,899 | 1,662 | 1,656 | 0.995 | 0% | 1% | 20 | 74 | 144 | 322 | 706 | 1,062 | 1,349 | 1,656 |
| high | 0.80 | 1,112 | 634 | 629 | 1.009 | 0% | 0% | 7 | 32 | 62 | 115 | 269 | 378 | 496 | 629 |
| high | 0.85 | 1,112 | 769 | 766 | 1.004 | 0% | 0% | 9 | 40 | 77 | 139 | 326 | 459 | 606 | 766 |
| high | 0.90 | 1,112 | 940 | 939 | 0.996 | 0% | 0% | 11 | 50 | 97 | 172 | 398 | 560 | 743 | 939 |
