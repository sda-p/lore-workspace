# Continuous collection progress

Updated: 2026-10-09T05:49:11+00:00

- Inventoried URLs: 2207
- Independently reviewed source records: 2207
- Source-specific claims: 9196
- Original source words in reviewed records: 5,274,594
- Original source words prepared for processing: 5,274,594
- Reviewed record languages: {'en': 908, 'es': 1299}
- Released records awaiting completed independent review/integration: 0
- Exact duplicate URLs skipped: 0
- Unassigned URLs: 0
- Assigned records still needing work: 0

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
| continuous-011 | 20 | 20 | 20 | reviewed | 7 |
| continuous-012 | 30 | 30 | 30 | reviewed | 5 |
| continuous-013 | 160 | 160 | 160 | reviewed | 24 |
| continuous-014 | 160 | 160 | 160 | reviewed | 12 |
| continuous-015 | 160 | 160 | 160 | reviewed | 10 |
| continuous-016 | 160 | 160 | 160 | reviewed | 22 |
| continuous-017 | 160 | 160 | 160 | reviewed | 32 |
| continuous-018 | 160 | 160 | 160 | reviewed | 29 |
| continuous-019 | 160 | 160 | 160 | reviewed | 41 |
| continuous-020 | 160 | 160 | 160 | reviewed | 26 |
| continuous-021 | 17 | 17 | 17 | reviewed | 2 |

## Resume

Resume existing queues from `work/ledger.json` and `work/handoffs.json`. Run `continuous.py shard-progress --batch <cohort> --worker <n>` for each extraction owner. Restore matching snapshots with `lore.py prepare --restore-only --selection config/selections/<cohort>.json --batch <cohort> --cache ../source-cache` before extraction or semantic review. Do not rerun `ready` for an already assigned cohort. Reuse partial review checkpoints only after checking assignments, release markers, source hashes, and record hashes. Integrate only after both complete independent review reports are present, then build the wiki and checkpoint.

Select a new cohort only when unassigned URLs remain: run `continuous.py select --batch <id> --size 40`, prepare its selection with `lore.py prepare --selection config/selections/<id>.json --batch <id>`, then run `continuous.py ready --batch <id>`. Assign four extraction shards and two independent review shards. Completed ledger jobs are retained across cohorts.

Review reports and integration errors are retained under `reports/batches/`. Failed downloads and records remain retryable; suspected translations are never skipped solely because their titles resemble another article.
