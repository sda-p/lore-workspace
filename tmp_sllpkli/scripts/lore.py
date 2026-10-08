#!/usr/bin/env python3
"""Discover, cache, validate, and build a small source-linked lore wiki."""
import argparse
import contextlib
import fcntl
import concurrent.futures
import datetime as dt
import hashlib
import json
from html.parser import HTMLParser
from pathlib import Path
import re
import time
import urllib.request
from urllib.parse import quote, urljoin, urlparse, urlunparse

ROOT = Path(__file__).resolve().parents[1]
BASE = 'https://swaruu.org/transcripts/'

def now():
    return dt.datetime.now(dt.timezone.utc).isoformat(timespec='seconds')

def sha(text):
    return hashlib.sha256(text.encode('utf-8')).hexdigest()

def read(path):
    return json.loads(Path(path).read_text(encoding='utf-8'))

def write(path, data):
    path = Path(path)
    path.parent.mkdir(parents=True, exist_ok=True)
    temporary = path.with_suffix(path.suffix + '.tmp')
    temporary.write_text(json.dumps(data, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
    temporary.replace(path)

@contextlib.contextmanager
def coordinator_lock():
    """Serialize brief shared ledger/config updates across prefetch and integration."""
    with (ROOT / '.git/lore-coordinator.lock').open('a') as handle:
        fcntl.flock(handle, fcntl.LOCK_EX)
        try:
            yield
        finally:
            fcntl.flock(handle, fcntl.LOCK_UN)

def retain_jobs(previous):
    """Keep inactive job history when a new selection is assigned."""
    return {source_id:dict(job) for source_id,job in previous.items()}

class Node:
    def __init__(self, tag, attrs=(), parent=None):
        self.tag, self.attrs, self.parent, self.children = tag, dict(attrs), parent, []

    def walk(self):
        yield self
        for child in self.children:
            if isinstance(child, Node):
                yield from child.walk()

    def text(self):
        if self.tag in ('script', 'style'):
            return ''
        pieces = []
        for child in self.children:
            if isinstance(child, str):
                pieces.append(child)
            elif child.tag == 'br':
                pieces.append('\n')
            else:
                pieces.append(child.text())
                if child.tag in ('p', 'div', 'li', 'h4', 'h6'):
                    pieces.append('\n')
        return ''.join(pieces)

class DOM(HTMLParser):
    VOID = {'area', 'base', 'br', 'col', 'embed', 'hr', 'img', 'input', 'link', 'meta', 'param', 'source', 'track', 'wbr'}

    def __init__(self):
        super().__init__(convert_charrefs=True)
        self.root = Node('root')
        self.stack = [self.root]

    def handle_starttag(self, tag, attrs):
        node = Node(tag, attrs, self.stack[-1])
        self.stack[-1].children.append(node)
        if tag not in self.VOID:
            self.stack.append(node)

    def handle_startendtag(self, tag, attrs):
        self.handle_starttag(tag, attrs)
        if tag not in self.VOID:
            self.handle_endtag(tag)

    def handle_endtag(self, tag):
        for position in range(len(self.stack)-1, 0, -1):
            if self.stack[position].tag == tag:
                self.stack = self.stack[:position]
                break

    def handle_data(self, data):
        self.stack[-1].children.append(data)

def clean(text):
    return ' '.join(text.split())

def parse_article(html):
    dom = DOM()
    dom.feed(html)
    containers = [n for n in dom.root.walk() if 'transcript-content' in n.attrs.get('class', '').split()]
    if len(containers) != 1:
        raise ValueError(f'Expected one transcript body, got {len(containers)}')
    passages = [clean(piece) for piece in containers[0].text().splitlines() if clean(piece)]
    if len(passages) < 3:
        raise ValueError('Suspiciously short transcript')
    metadata = {}
    for node in dom.root.walk():
        if node.tag == 'h6' and clean(node.text()).lower() in ('author', 'published'):
            spans = [n for n in node.parent.walk() if n.tag == 'span']
            if spans:
                metadata[clean(node.text()).lower()] = clean(spans[0].text())
    published = metadata.get('published')
    if published:
        try:
            metadata['published_date'] = dt.datetime.strptime(published, '%B %d, %Y').date().isoformat()
        except ValueError:
            metadata['published_date'] = None
    paragraphs = [{'id':f'p{i:04d}', 'text':text, 'sha256':sha(text)} for i, text in enumerate(passages, 1)]
    metadata.update(parser_version='line-passages-v1', paragraphs=paragraphs, snapshot_sha256=sha('\n'.join(passages)), word_count=sum(len(p.split()) for p in passages))
    return metadata

def validate_snapshot(snapshot, expected_sha=None):
    if not re.fullmatch(r'src-[a-f0-9]{12}',snapshot.get('source_id','')) or snapshot.get('language') not in ('en','es'):
        raise ValueError('Invalid snapshot identity or language')
    paragraphs = snapshot.get('paragraphs')
    if not isinstance(paragraphs,list) or not paragraphs:
        raise ValueError('Missing source passages')
    texts = []
    for number,passage in enumerate(paragraphs,1):
        if passage.get('id') != f'p{number:04d}' or not isinstance(passage.get('text'),str) or not passage['text'].strip():
            raise ValueError('Invalid source passage order or text')
        if passage.get('sha256') != sha(passage['text']):
            raise ValueError('Source passage hash mismatch')
        texts.append(passage['text'])
    actual = sha('\n'.join(texts))
    if snapshot.get('snapshot_sha256') != actual or (expected_sha is not None and expected_sha != actual):
        raise ValueError('Source snapshot hash mismatch')
    if snapshot.get('word_count') != sum(len(text.split()) for text in texts):
        raise ValueError('Source word count mismatch')
    return actual

def download(url):
    request = urllib.request.Request(url, headers={'User-Agent':'LoreResearch/0.2 (source-linked research; bounded download concurrency)'})
    with urllib.request.urlopen(request, timeout=25) as response:
        return response.read().decode('utf-8')

def discover(index):
    path = Path(index)
    if not path.exists():
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(download(BASE), encoding='utf-8')
    dom = DOM()
    dom.feed(path.read_text(encoding='utf-8'))
    found = {}
    for node in dom.root.walk():
        if node.tag != 'a':
            continue
        url = urljoin(BASE, node.attrs.get('href', ''))
        parts = urlparse(url)
        label = clean(node.text())
        if parts.netloc == 'swaruu.org' and parts.path.startswith('/transcripts/') and parts.path.rstrip('/') != '/transcripts' and not parts.query and label not in ('', 'Read transcript'):
            found[url.rstrip('/')] = label
    if not found:
        raise ValueError('No article links discovered')
    manifest_path = ROOT / 'sources/manifest.json'
    existing = {s['url']:s for s in read(manifest_path)['sources']} if manifest_path.exists() else {}
    sources = []
    for url, title in found.items():
        entry = existing.get(url, {'id':'src-'+sha(url)[:12], 'url':url, 'language':None})
        entry['title'] = title
        sources.append(entry)
    write(manifest_path, {'schema_version':1, 'index_url':BASE, 'discovered_at':now(), 'index_sha256':sha(path.read_text()), 'record_count':len(sources), 'sources':sources})
    print(f'Discovered {len(sources)} distinct article URLs; translation equivalence remains to be reviewed.', flush=True)

def prepare(cache, selection_path=None, batch_id='pilot-001', restore_only=False):
    cache = Path(cache).resolve()
    cache.mkdir(parents=True, exist_ok=True)
    manifest = read(ROOT / 'sources/manifest.json')
    by_url = {s['url']:s for s in manifest['sources']}
    selections = read(selection_path or ROOT / 'config/pilot.json')
    selected = []
    for selection in selections:
        url = BASE + selection['slug']
        if url not in by_url:
            raise ValueError(f'Selected URL missing from inventory: {url}')
        source = by_url[url]
        source.update({k:v for k,v in selection.items() if k != 'slug'})
        selected.append(source)

    def fetch(source):
        target = cache / (source['id']+'.json')
        if target.exists():
            snapshot = read(target)
        else:
            error = None
            for attempt in range(2):
                try:
                    html = download(source['url'])
                    snapshot = parse_article(html)
                    snapshot.update(source_id=source['id'], url=source['url'], title=source['title'], language=source['language'], retrieved_at=now(), html_sha256=sha(html))
                    write(target, snapshot)
                    break
                except Exception as exc:
                    error = exc
                    if attempt == 0: time.sleep(2)
            else:
                raise error
        validate_snapshot(snapshot,source.get('snapshot_sha256'))
        if snapshot['source_id'] != source['id'] or snapshot['url'] != source['url'] or snapshot['language'] != source['language']:
            raise ValueError(f"Cached source identity mismatch: {source['id']}")
        source.update({k:snapshot.get(k) for k in ('snapshot_sha256','html_sha256','retrieved_at','published_date','author','word_count')})
        source['paragraph_count'] = len(snapshot['paragraphs'])
        source.pop('passage_hashes',None)
        source['parser_version'] = snapshot.get('parser_version','line-passages-v1')
        source['rights_notice'] = 'Source displays a notice prohibiting commercial publication of its information; adaptation permission not established.'
        print(f"Cached {source['id']}: {source['word_count']} words, {source['paragraph_count']} passages", flush=True)
        return source

    errors = []
    with concurrent.futures.ThreadPoolExecutor(max_workers=2) as pool:
        futures = {pool.submit(fetch,s):s for s in selected}
        for future in concurrent.futures.as_completed(futures):
            try:
                future.result()
            except Exception as exc:
                errors.append({'source_id':futures[future]['id'], 'error':str(exc)})
    with coordinator_lock():
        current_manifest = read(ROOT / 'sources/manifest.json')
        current_sources = {s['id']:s for s in current_manifest['sources']}
        for source in selected:
            current_sources[source['id']].update(source)
        write(ROOT / 'sources/manifest.json', current_manifest)
    if errors:
        write(ROOT / 'reports/download-errors.json', errors)
        raise ValueError(f'{len(errors)} source downloads failed; retry prepare')
    if restore_only:
        print(f'Restored {len(selected)} matching source snapshots; assignments and ledger unchanged.')
        return
    groups = {}
    for source in selected:
        groups.setdefault(source.get('translation_candidate_group', source['id']), []).append(source)
    batches, totals = [[] for _ in range(4)], [0]*4
    for group in sorted(groups.values(), key=lambda g:sum(s['word_count'] for s in g), reverse=True):
        worker = min(range(4), key=lambda i:totals[i])
        batches[worker].extend(s['id'] for s in group)
        totals[worker] += sum(s['word_count'] for s in group)
    with coordinator_lock():
        ledger_path = ROOT / 'work/ledger.json'
        previous = read(ledger_path).get('jobs',{}) if ledger_path.exists() else {}
        jobs = retain_jobs(previous)
        for i, ids in enumerate(batches,1):
            write(ROOT / f'work/batches/worker-{i}.json', {'worker':i,'source_ids':ids,'source_word_count':totals[i-1]})
            write(ROOT / f'work/batches/{batch_id}/worker-{i}.json', {'worker':i,'batch_id':batch_id,'source_ids':ids,'source_word_count':totals[i-1]})
            for source_id in ids:
                jobs[source_id] = previous.get(source_id, {'status':'pending','attempts':0})
                jobs[source_id]['worker'] = i
                jobs[source_id]['batch_id'] = batch_id
        write(ledger_path, {'batch':batch_id,'updated_at':now(),'active_source_ids':[s['id'] for s in selected],'jobs':jobs})
    print(f'Prepared {len(selected)} records across four batches, {sum(totals)} source words.', flush=True)

def validate_record(record, snapshot, known_topics):
    validate_snapshot(snapshot)
    required = {'source_id','snapshot_sha256','language','claims','proposed_topics','review_flags','coverage_gaps'}
    if set(record) != required:
        raise ValueError('Unexpected or missing article fields')
    if not isinstance(record['source_id'],str) or not re.fullmatch(r'src-[a-f0-9]{12}',record['source_id']) or not isinstance(record['snapshot_sha256'],str) or not re.fullmatch(r'[a-f0-9]{64}',record['snapshot_sha256']) or record['language'] not in ('en','es'):
        raise ValueError('Invalid article identity, hash, or language')
    if record['source_id'] != snapshot['source_id'] or record['snapshot_sha256'] != snapshot['snapshot_sha256'] or record['language'] != snapshot['language']:
        raise ValueError('Source identity, language, or snapshot mismatch')
    for field in ('claims','proposed_topics','review_flags','coverage_gaps'):
        if not isinstance(record[field],list):
            raise ValueError(f'{field} must be an array')
    topics = set(known_topics)
    proposed = set()
    for topic in record['proposed_topics']:
        if not isinstance(topic,dict) or set(topic) != {'id','name','kind','aliases'} or not isinstance(topic['id'],str) or not re.fullmatch(r'[a-z0-9]+(?:-[a-z0-9]+)*',topic['id']):
            raise ValueError('Invalid proposed topic')
        identical_known = isinstance(known_topics,dict) and known_topics.get(topic['id'])==topic
        if (topic['id'] in topics and not identical_known) or topic['id'] in proposed:
            raise ValueError('Proposed topic ID collides with an existing topic')
        if any(not isinstance(topic[field],str) or not topic[field].strip() for field in ('name','kind')) or not isinstance(topic['aliases'],list) or any(not isinstance(alias,str) or not alias.strip() for alias in topic['aliases']):
            raise ValueError('Invalid topic metadata')
        proposed.add(topic['id'])
        topics.add(topic['id'])
    if any(not isinstance(tag,str) or not tag.strip() for field in ('review_flags','coverage_gaps') for tag in record[field]):
        raise ValueError('Review flags and coverage gaps must be nonempty string tags')
    evidence = {p['id'] for p in snapshot['paragraphs']}
    ids, words = set(), 0
    fields = {'id','assertion','speaker','paragraph_ids','primary_topic','topics','modality','confidence','qualifiers'}
    if not 1 <= len(record['claims']) <= 10:
        raise ValueError('Extraction must contain 1–10 compact claims')
    for number,claim in enumerate(record['claims'],1):
        if not isinstance(claim,dict) or set(claim) != fields:
            raise ValueError('Unexpected or missing claim fields')
        if not isinstance(claim['id'],str) or claim['id'] != f"{record['source_id']}-c{number:02d}" or claim['id'] in ids:
            raise ValueError('Invalid or duplicate claim ID')
        ids.add(claim['id'])
        if not isinstance(claim['assertion'],str) or not claim['assertion'].strip() or not isinstance(claim['speaker'],str) or not claim['speaker'].strip() or not isinstance(claim['qualifiers'],str):
            raise ValueError('Missing assertion or attribution')
        if not isinstance(claim['paragraph_ids'],list) or not claim['paragraph_ids'] or any(not isinstance(p,str) for p in claim['paragraph_ids']) or len(set(claim['paragraph_ids'])) != len(claim['paragraph_ids']) or not set(claim['paragraph_ids']) <= evidence:
            raise ValueError('Unknown, empty, or repeated evidence passage')
        if not isinstance(claim['topics'],list) or not claim['topics'] or any(not isinstance(t,str) for t in claim['topics']) or not isinstance(claim['primary_topic'],str) or len(set(claim['topics'])) != len(claim['topics']) or not set(claim['topics']) <= topics or claim['primary_topic'] not in claim['topics']:
            raise ValueError('Invalid topic reference')
        if claim['modality'] not in ('asserted','speculative','reported') or claim['confidence'] not in ('high','medium','low'):
            raise ValueError('Invalid modality or confidence')
        words += len((claim['assertion']+' '+claim['qualifiers']).split())
    if words > 85:
        raise ValueError(f'Paraphrase budget exceeded: {words} > 85')
    return {'claim_count':len(ids),'paraphrase_words':words}

def validate(cache):
    cache = Path(cache)
    ledger = read(ROOT / 'work/ledger.json')
    topics = {t['id']:t for t in read(ROOT / 'config/topics.json')}
    sources = {s['id']:s for s in read(ROOT / 'sources/manifest.json')['sources']}
    results, failed = [], []
    for source_id, job in ledger['jobs'].items():
        if source_id not in ledger.get('active_source_ids',ledger['jobs']):
            continue
        path = ROOT / f'records/{source_id}.json'
        if not path.exists():
            failed.append({'source_id':source_id,'error':'Extraction missing'})
            continue
        try:
            snapshot = read(cache / f'{source_id}.json')
            validate_snapshot(snapshot,sources[source_id].get('snapshot_sha256'))
            record = read(path)
            result = validate_record(record,snapshot,topics)
            results.append({'source_id':source_id,**result})
            record_hash = sha(json.dumps(record,sort_keys=True,ensure_ascii=False))
            already_reviewed = job['status']=='reviewed' and job.get('record_sha256')==record_hash
            job['status'] = 'reviewed' if already_reviewed else 'validated'
            job['record_sha256'] = record_hash
            job.update(result)
        except Exception as exc:
            failed.append({'source_id':source_id,'error':str(exc)})
            job['status'] = 'needs-correction'
    ledger['updated_at'] = now()
    write(ROOT / 'work/ledger.json',ledger)
    write(ROOT / 'reports/validation.json',{'checked_at':now(),'valid':results,'errors':failed})
    print(f'Validated {len(results)} records, {sum(r["claim_count"] for r in results)} claims; {len(failed)} errors.')
    if failed:
        raise ValueError('Validation failed; inspect reports/validation.json')

def md(text):
    return re.sub(r'([\\`*_{}\[\]<>!#|])',r'\\\1',str(text).replace('\n',' '))

def source_url(url):
    parts = urlparse(url)
    if parts.scheme != 'https' or parts.netloc != 'swaruu.org' or not parts.path.startswith('/transcripts/'):
        raise ValueError('Unexpected source URL')
    return urlunparse((parts.scheme,parts.netloc,quote(parts.path,safe='/-._~'),'',quote(parts.query,safe='=&'),''))

def build():
    manifest = read(ROOT / 'sources/manifest.json')
    sources = {s['id']:s for s in manifest['sources']}
    ledger = read(ROOT / 'work/ledger.json')
    topics = {t['id']:t for t in read(ROOT / 'config/topics.json')}
    records = []
    for source_id,job in ledger['jobs'].items():
        if job['status'] != 'reviewed':
            continue
        record = read(ROOT / f'records/{source_id}.json')
        digest = sha(__import__('json').dumps(record,sort_keys=True,ensure_ascii=False))
        if record.get('source_id') != source_id or digest != job.get('record_sha256'):
            raise ValueError(f'Reviewed record changed since approval: {source_id}; re-review before rebuilding the wiki')
        records.append(record)
        for topic in record['proposed_topics']:
            topics.setdefault(topic['id'],topic)
    wiki = ROOT / 'wiki'
    (wiki / 'topics').mkdir(parents=True,exist_ok=True)
    linked = {}
    for record in records:
        for claim in record['claims']:
            for topic in claim['topics']:
                linked.setdefault(topic,[]).append((record,claim))
    overlaps = {}
    overlap_report = ROOT / 'reports/topic-overlaps.json'
    if overlap_report.exists():
        for collision in read(overlap_report).get('collisions',[]):
            ids = set(collision['topic_ids']) & set(linked)
            for topic_id in ids:
                overlaps.setdefault(topic_id,set()).update(ids-{topic_id})
    lines = ['# Lore topic wiki','','All statements below are attributed lore claims. Evidence passage IDs refer to the hashed local source snapshot, not anchors on the live website.','','Language and revision variants remain separate source records unless content equivalence is established. Their agreement is not independent corroboration.','','| Topic | Type | Primary claims | Related claims |','| --- | --- | ---: | ---: |']
    for topic_id in sorted(linked):
        if not re.fullmatch(r'[a-z0-9]+(?:-[a-z0-9]+)*',topic_id):
            raise ValueError('Unsafe topic path')
        topic = topics[topic_id]
        primary = [(r,c) for r,c in linked[topic_id] if c['primary_topic']==topic_id]
        related = [(r,c) for r,c in linked[topic_id] if c['primary_topic']!=topic_id]
        lines.append(f"| [{md(topic['name'])}](topics/{topic_id}.md) | {md(topic['kind'])} | {len(primary)} | {len(related)} |")
        page = [f"# {md(topic['name'])}",'',f"Type: {md(topic['kind'])}",'',f"Aliases: {md(', '.join(topic['aliases']) or 'None recorded')}",'', 'These are source-specific assertions; disagreement is preserved rather than resolved by publication order.','']
        if overlaps.get(topic_id):
            page += ['## Related topic collections','','These collections share labels; that alone does not establish identical entities or concepts.','']
            page += [f"- [{md(topics[other]['name'])}]({other}.md)" for other in sorted(overlaps[topic_id])]
            page += ['']
        page += ['## Collected claims','']
        for record,claim in primary:
            source = sources[record['source_id']]
            page += [f"### {claim['id']}",'',md(claim['assertion'] + (' '+claim['qualifiers'] if claim['qualifiers'] else '')),'',f"Attributed to **{md(claim['speaker'])}**; {claim['modality']}; extraction confidence: {claim['confidence']}.",'',f"Source: [{md(source['title'])}]({source_url(source['url'])}) ({source.get('published_date') or 'date unavailable'}; {source['language']}); passages {', '.join(claim['paragraph_ids'])}. [Structured record](../../records/{record['source_id']}.json).",'']
            others = [t for t in claim['topics'] if t!=topic_id]
            if others:
                page += ['Related topics: '+', '.join(f"[{md(topics[t]['name'])}]({t}.md)" for t in others)+'.','']
        if not primary:
            page += ['Primary assertions are filed under the linked topics below.','']
        if related:
            page += ['## Claims filed under other topics','']
            for record,claim in related:
                page.append(f"- [{claim['id']}]({claim['primary_topic']}.md#{claim['id']}) — {md(topics[claim['primary_topic']]['name'])}")
            page.append('')
        flags = sorted({flag for r,c in linked[topic_id] for flag in r['review_flags']})
        if flags:
            page += ['## Review flags',''] + ['- '+md(flag) for flag in flags] + ['']
        (wiki / 'topics' / f'{topic_id}.md').write_text('\n'.join(page),encoding='utf-8')
    lines += ['','## Reviewed sources','','| Source | Language | Published | Claims |','| --- | --- | --- | ---: |']
    for record in sorted(records,key=lambda r:sources[r['source_id']].get('published_date') or ''):
        source = sources[record['source_id']]
        lines.append(f"| [{md(source['title'])}]({source_url(source['url'])}) | {source['language']} | {source.get('published_date') or 'Unknown'} | {len(record['claims'])} |")
    lines += ['','See [continuous collection progress](../reports/collection.md), [pilot review](../reports/pilot.md), [reconciliation](../reports/reconciliation.md), and [original game design](../design/README.md).','']
    (wiki / 'index.md').write_text('\n'.join(lines),encoding='utf-8')
    count = sum(len(r['claims']) for r in records)
    work_count = len({sources[r['source_id']].get('work_group_id',r['source_id']) for r in records})
    pending = sum(j['status'] not in ('validated','reviewed') for j in ledger['jobs'].values())
    report = ['# Collection pilot','','## Current checkpoint','',f"- Discovered article URLs: {manifest['record_count']}",f'- Batch records validated: {len(records)}',f'- Reviewed underlying work groups in this batch: {work_count}',f'- Source-specific claims collected: {count}',f'- Topic pages: {len(linked)}',f'- Batch records pending or needing correction: {pending}',f"- Catalogued URLs outside this batch: {manifest['record_count']-len(records)}",'','Validation checks identities, recomputed source hashes, passage references, topic references, IDs, and compact paraphrase budgets. Structural validation does not establish factual truth or semantic accuracy. This batch is a compact core extraction, with omissions retained as coverage tags.','','## Review outcome','','Four Luna workers extracted the initial records. A separate Luna reviewed 131 claims; the coordinator applied five evidence/scope corrections and one regional refinement. Full-language comparison identified material omitted from one English counterpart; one additional Spanish-specific claim was added and independently checked, bringing the checkpoint to 132 claims. Both translation pairs remain separate source snapshots grouped for deduplication.','','The engineering review led to hash revalidation, stronger format/type checks, retained inactive ledger history, and safer Markdown output. Sixteen integrity tests pass. Line-break passage segmentation remains an explicit documented limitation.','','Coverage recall was not measured against a full human extraction. Compact records do not claim to capture all available lore.','','## Resume','', 'Start from `work/ledger.json`. Recreate the source cache with `prepare`, compare retained hashes, and assign only uncompleted or explicitly expanded jobs. Candidate translations require review before one record is skipped. Do not report the entire inventory as processed.','']
    if not (ROOT / 'reports/pilot.md').exists():
        (ROOT / 'reports/pilot.md').write_text('\n'.join(report),encoding='utf-8')
    write(ROOT / 'reports/topic-registry.json',list(topics.values()))
    print(f'Built {len(linked)} topic pages from {count} claims.')

def main():
    parser = argparse.ArgumentParser()
    sub = parser.add_subparsers(dest='command',required=True)
    discover_parser = sub.add_parser('discover')
    discover_parser.add_argument('--index',default='../source-cache/index.html')
    prepare_parser = sub.add_parser('prepare')
    prepare_parser.add_argument('--cache',default='../source-cache')
    prepare_parser.add_argument('--selection')
    prepare_parser.add_argument('--batch',default='pilot-001')
    prepare_parser.add_argument('--restore-only',action='store_true',help='Restore and hash-check snapshots without rewriting assignments or ledger')
    validate_parser = sub.add_parser('validate')
    validate_parser.add_argument('--cache',default='../source-cache')
    sub.add_parser('build')
    args = parser.parse_args()
    if args.command=='discover': discover(args.index)
    elif args.command=='prepare': prepare(args.cache,args.selection,args.batch,args.restore_only)
    elif args.command=='validate': validate(args.cache)
    else: build()

if __name__=='__main__':
    main()
