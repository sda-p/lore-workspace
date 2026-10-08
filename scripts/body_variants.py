#!/usr/bin/env python3
"""Identify identical article bodies without treating distinct source URLs as corroboration."""
import argparse
from collections import defaultdict
from itertools import combinations
from pathlib import Path
import re
import unicodedata
import lore


def title_key(text):
    return ''.join(re.findall(r'\w+', unicodedata.normalize('NFKC', text).casefold()))


def body_text(snapshot, title):
    passages = snapshot['paragraphs']
    # Never discard an actual first content paragraph in place of a title.
    if title_key(passages[0]['text']) != title_key(title):
        return None
    return ' '.join(' '.join(p['text'] for p in passages[1:]).split())


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--cache', default='../source-cache')
    args = parser.parse_args()
    cache = Path(args.cache).resolve()
    with lore.coordinator_lock():
        manifest = lore.read(lore.ROOT / 'sources/manifest.json')
        groups = defaultdict(list)
        checked = 0
        for source in manifest['sources']:
            path = cache / (source['id'] + '.json')
            if not path.exists():
                continue
            snapshot = lore.read(path)
            lore.validate_snapshot(snapshot, source['snapshot_sha256'])
            if snapshot['source_id'] != source['id'] or snapshot['url'] != source['url']:
                raise ValueError('Source identity mismatch')
            checked += 1
            text = body_text(snapshot, source['title'])
            if text:
                groups[lore.sha(text)].append(source)
        matches = []
        matched_groups = [members for members in groups.values() if len(members) > 1]
        for members in matched_groups:
            digest = lore.sha(body_text(lore.read(cache / (members[0]['id'] + '.json')), members[0]['title']))
            group_id = 'body-' + digest[:12]
            for source in members:
                source['body_equivalence_group'] = group_id
            for a, b in combinations(sorted(members, key=lambda s: s['id']), 2):
                matches.append({'source_ids': [a['id'], b['id']], 'body_equivalence_group': group_id,
                    'comparison': 'Complete body after verified article title is identical after whitespace normalization; punctuation and wording retained.',
                    'distinct_title_metadata': [a['title'], b['title']]})
        lore.write(lore.ROOT / 'sources/manifest.json', manifest)
        lore.write(lore.ROOT / 'reports/body-equivalence.json', {
            'checked_at': lore.now(), 'prepared_snapshots_scanned': checked,
            'method': 'Complete body comparison after verifying the first passage matches the index title; whitespace normalization only.',
            'policy': 'Source metadata and snapshot hashes stay distinct. No job assignments or extraction counts are changed.',
            'body_equivalence_groups': len(matched_groups),
            'grouped_source_records': sum(len(m) for m in matched_groups),
            'confirmed_body_matches': matches})
        print(f'{checked} snapshots checked; {len(matched_groups)} identical-body groups; {sum(len(m) for m in matched_groups)} retained source records.')


if __name__ == '__main__':
    main()
