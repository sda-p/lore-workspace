# Continuous collection progress

Updated: 2026-10-08T16:26:59+00:00

- Inventoried URLs: 2207
- Independently reviewed source records: 860
- Source-specific claims: 4444
- Original source words in reviewed records: 2,104,200
- Original source words prepared for processing: 5,274,594
- Reviewed record languages: {'en': 858, 'es': 2}
- Released records awaiting completed independent review/integration: 100
- Exact duplicate URLs skipped: 0
- Unassigned URLs: 0
- Assigned records still needing work: 1347

Source-record counts include retained language/revision variants and are not counts of independent corroborating accounts. Each record is a compact core extraction, not exhaustive coverage. English-first selection uses title heuristics plus coordinator review of ambiguous titles. Later cohorts process Spanish and remaining records; extracts are written in English, with original source language retained.

| Cohort | Records selected | Records released | Records reviewed | Status | Review corrections |
| --- | ---: | ---: | ---: | --- | ---: |
| continuous-002 | 40 | 40 | 40 | reviewed | 3 |
| continuous-003 | 40 | 40 | 40 | reviewed | 18 |
| continuous-004 | 40 | 40 | 40 | reviewed | 2 |
| continuous-005 | 40 | 40 | 40 | reviewed | 1 |
| continuous-006 | 40 | 40 | 40 | reviewed | 7 |
| continuous-007 | 160 | 160 | 160 | reviewed | 35 |
| continuous-008 | 160 | 160 | 160 | reviewed | 34 |
| continuous-009 | 160 | 160 | 160 | reviewed | 33 |
| continuous-010 | 160 | 160 | 160 | reviewed | 24 |
| continuous-011 | 20 | 16 | 0 | running | 0 |
| continuous-012 | 30 | 23 | 0 | running | 0 |
| continuous-013 | 160 | 56 | 0 | running | 0 |
| continuous-014 | 160 | 5 | 0 | running | 0 |
| continuous-015 | 160 | 0 | 0 | running | 0 |
| continuous-016 | 160 | 0 | 0 | running | 0 |
| continuous-017 | 160 | 0 | 0 | running | 0 |
| continuous-018 | 160 | 0 | 0 | running | 0 |
| continuous-019 | 160 | 0 | 0 | running | 0 |
| continuous-020 | 160 | 0 | 0 | running | 0 |
| continuous-021 | 17 | 0 | 0 | running | 0 |

## Resume

Select a new cohort with `continuous.py select --batch <id> --size 40`, prepare its selection with `lore.py prepare --selection config/selections/<id>.json --batch <id>`, then run `continuous.py ready --batch <id>`. Assign four extraction shards and two independent review shards. Integrate completed reviews, build the wiki, and checkpoint. Completed ledger jobs are retained across cohorts.

Review reports and integration errors are retained under `reports/batches/`. Failed downloads and records remain retryable; suspected translations are never skipped solely because their titles resemble another article.
