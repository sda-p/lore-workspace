#!/usr/bin/env python3
"""Persist partial review notes with record hashes; never approve a cohort."""
import json
from pathlib import Path
import lore

root = lore.ROOT
saved = 0
for path in sorted((root.parent / 'review-notes').glob('continuous-*-review-*.json')):
    state = json.loads(path.read_text(encoding='utf-8'))
    batch, reviewer = state['batch_id'], state['reviewer']
    final = root / f'reports/batches/{batch}/review-{reviewer}.json'
    if final.exists():
        continue
    assignment = lore.read(root / f'work/batches/{batch}/review-{reviewer}.json')
    ids = state['reviewed_source_ids']
    if len(ids) != len(set(ids)) or not set(ids) <= set(assignment['source_ids']):
        raise ValueError(f'Invalid partial review assignment: {path.name}')
    hashes = {}
    for sid in ids:
        if not (root / f'work/completed/{sid}.json').exists():
            raise ValueError(f'Partial review contains unreleased source: {sid}')
        record = lore.read(root / f'records/{sid}.json')
        hashes[sid] = lore.sha(json.dumps(record, sort_keys=True, ensure_ascii=False))
    if not ids:
        continue
    lore.write(root / f'work/review-progress/{path.name}', {
        'status': 'partial-not-approval',
        'checkpointed_at': lore.now(),
        'resume_policy': 'Reuse only after matching assigned IDs, release markers, retained source hashes and these record hashes. Re-review changed records. Final cohort reports remain required.',
        'review_state': state,
        'record_sha256': hashes,
    })
    saved += 1
print(f'Checkpointed {saved} partial review shards; no approval or ledger changes.')
