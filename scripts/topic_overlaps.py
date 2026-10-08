#!/usr/bin/env python3
"""Refresh conservative shared-label navigation without merging topic identities."""
import re
import unicodedata
import lore

path = lore.ROOT / 'reports/topic-overlaps.json'
report = lore.read(path) if path.exists() else {}
previous = {(item['normalized_label'],tuple(sorted(item['topic_ids']))):item for item in report.get('collisions',[])}
labels = {}
for topic in lore.read(lore.ROOT / 'config/topics.json'):
    for label in [topic['id'],topic['name']] + topic['aliases']:
        key = re.sub('[^a-z0-9]','',unicodedata.normalize('NFKD',label).encode('ascii','ignore').decode().lower())
        if key:
            labels.setdefault(key,set()).add(topic['id'])
collisions = []
for label,ids in sorted(labels.items()):
    if len(ids) < 2:
        continue
    item = dict(previous.get((label,tuple(sorted(ids))),{}))
    item.update(normalized_label=label,topic_ids=sorted(ids))
    item.setdefault('status','overlap-awaiting-reconciliation')
    collisions.append(item)
report.update(checked_at=lore.now(),collisions=collisions)
report.setdefault('policy','Shared labels support navigation only; they do not establish identical entities or concepts.')
lore.write(path,report)
print(f'Refreshed {len(collisions)} shared-label entries; no identity merges or record changes.')
