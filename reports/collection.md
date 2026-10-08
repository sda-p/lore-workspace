# Continuous collection progress

Updated: 2026-10-08T14:44:22+00:00

- Inventoried URLs: 2207
- Independently reviewed source records: 180
- Source-specific claims: 1024
- Exact duplicate URLs skipped: 0
- Unassigned URLs: 1987
- Assigned records still needing work: 40

Source-record counts include retained language/revision variants and are not counts of independent corroborating accounts. Each record is a compact core extraction, not exhaustive coverage. English-first selection uses title heuristics; other languages remain available for later comparisons.

| Cohort | Records selected | Status | Review corrections |
| --- | ---: | --- | ---: |
| continuous-002 | 40 | reviewed | 3 |
| continuous-003 | 40 | reviewed | 18 |
| continuous-004 | 40 | reviewed | 2 |
| continuous-005 | 40 | reviewed | 1 |
| continuous-006 | 40 | running | 0 |
| continuous-007 | 160 | selected | 0 |

## Resume

Select a new cohort with `continuous.py select --batch <id> --size 40`, prepare its selection with `lore.py prepare --selection config/selections/<id>.json --batch <id>`, then run `continuous.py ready --batch <id>`. Assign four extraction shards and two independent review shards. Integrate completed reviews, build the wiki, and checkpoint. Completed ledger jobs are retained across cohorts.

Review reports and integration errors are retained under `reports/batches/`. Failed downloads and records remain retryable; suspected translations are never skipped solely because their titles resemble another article.
