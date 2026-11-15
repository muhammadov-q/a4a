# Do the distinct tool candidates saturate?

97 repositories, embedding model `qwen3-embedding-4b`, 10 random orders of the repositories. A candidate joins a group if its similarity to the group's first member is at least the threshold.

Exponent: b in groups = a * candidates^b. 1 means no repetition; smaller means later repositories repeat earlier ones. Distinct inside: the sum of the groups each repository has on its own, so the gap to Candidates is repetition inside repositories and the gap to Groups is repetition between them. Seen before: of the distinct things a repository has, the share an earlier repository already had, for repositories added early (second tenth) and late (last tenth).

## All candidates

| Level | Threshold | Candidates | Distinct inside | Groups | Exponent | Seen before, early | Seen before, late | k=1 | k=5 | k=10 | k=20 | k=40 | k=60 | k=80 | k=97 |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| low | 0.80 | 17,362 | 9,346 | 8,930 | 0.976 | 2% | 11% | 103 | 431 | 841 | 1,717 | 3,947 | 5,420 | 7,178 | 8,930 |
| low | 0.85 | 17,362 | 11,324 | 11,073 | 0.983 | 1% | 6% | 119 | 522 | 1,035 | 2,102 | 4,840 | 6,635 | 8,859 | 11,073 |
| low | 0.90 | 17,362 | 13,392 | 13,248 | 0.986 | 0% | 2% | 139 | 612 | 1,237 | 2,506 | 5,761 | 7,872 | 10,579 | 13,248 |
| medium | 0.80 | 19,144 | 10,693 | 10,167 | 0.977 | 2% | 12% | 122 | 482 | 965 | 1,978 | 4,530 | 6,188 | 8,196 | 10,167 |
| medium | 0.85 | 19,144 | 12,936 | 12,606 | 0.985 | 1% | 6% | 142 | 582 | 1,183 | 2,413 | 5,552 | 7,577 | 10,114 | 12,606 |
| medium | 0.90 | 19,144 | 15,141 | 14,957 | 0.988 | 1% | 3% | 167 | 678 | 1,409 | 2,853 | 6,562 | 8,925 | 11,989 | 14,957 |
| high | 0.80 | 1,814 | 898 | 893 | 1.001 | 0% | 0% | 7 | 58 | 88 | 168 | 374 | 510 | 681 | 893 |
| high | 0.85 | 1,814 | 1,137 | 1,134 | 0.998 | 0% | 0% | 9 | 76 | 114 | 213 | 472 | 644 | 863 | 1,134 |
| high | 0.90 | 1,814 | 1,425 | 1,423 | 0.992 | 0% | 0% | 11 | 97 | 145 | 269 | 591 | 803 | 1,082 | 1,423 |

## Candidates the repository's own documentation uses

| Level | Threshold | Candidates | Distinct inside | Groups | Exponent | Seen before, early | Seen before, late | k=1 | k=5 | k=10 | k=20 | k=40 | k=60 | k=80 | k=97 |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| low | 0.80 | 2,150 | 1,268 | 1,246 | 0.981 | 0% | 3% | 13 | 64 | 111 | 244 | 536 | 788 | 1,004 | 1,246 |
| low | 0.85 | 2,150 | 1,492 | 1,480 | 0.991 | 0% | 1% | 14 | 77 | 130 | 290 | 630 | 926 | 1,186 | 1,480 |
| low | 0.90 | 2,150 | 1,748 | 1,744 | 0.994 | 0% | 0% | 15 | 95 | 152 | 344 | 738 | 1,078 | 1,385 | 1,744 |
| medium | 0.80 | 2,451 | 1,499 | 1,468 | 0.985 | 0% | 3% | 17 | 76 | 132 | 285 | 628 | 923 | 1,178 | 1,468 |
| medium | 0.85 | 2,451 | 1,748 | 1,731 | 0.992 | 0% | 1% | 19 | 91 | 155 | 336 | 734 | 1,079 | 1,383 | 1,731 |
| medium | 0.90 | 2,451 | 2,035 | 2,030 | 0.995 | 0% | 1% | 20 | 110 | 181 | 396 | 855 | 1,250 | 1,610 | 2,030 |
| high | 0.80 | 1,814 | 898 | 893 | 1.001 | 0% | 0% | 7 | 58 | 88 | 168 | 374 | 510 | 681 | 893 |
| high | 0.85 | 1,814 | 1,137 | 1,134 | 0.998 | 0% | 0% | 9 | 76 | 114 | 213 | 472 | 644 | 863 | 1,134 |
| high | 0.90 | 1,814 | 1,425 | 1,423 | 0.992 | 0% | 0% | 11 | 97 | 145 | 269 | 591 | 803 | 1,082 | 1,423 |
