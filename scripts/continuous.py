#!/usr/bin/env python3
"""Coordinate successive source-selection, extraction, and reviewed cohorts."""
import argparse
import copy
from collections import Counter
from pathlib import Path
import re
import sys
import time
sys.path.insert(0,str(Path(__file__).resolve().parent))
import lore

ROOT=lore.ROOT
EN=set('the and of to is what are we how from about with for in on not who our more life society questions message information extraterrestrial races contact pleiadian consciousness earth space english'.split())
ES=set('el la los las del que qué y por para con una un como cómo es son mensaje contacto extraterrestre pleyades sociedad nosotros'.split())

def language(title):
    words=set(re.findall(r"[a-záéíóúñ]+",title.lower()))
    if 'english' in words: return 'en'
    if 'español' in words or 'spanish' in words and not (words & EN): return 'es'
    a,b=len(words & EN),len(words & ES)
    return 'en' if a>=1 and a>b else 'es' if b>a else None

def select(batch,size,mode='en'):
    manifest=lore.read(ROOT/'sources/manifest.json')
    ledger=lore.read(ROOT/'work/ledger.json')
    available=[s for s in manifest['sources'] if s['id'] not in ledger['jobs'] and (mode=='remaining' or language(s['title'])==mode)]
    selected=available[:size]
    if not selected: raise ValueError(f'No unassigned records remain for selection mode {mode}.')
    path=ROOT/f'config/selections/{batch}.json'
    lore.write(path,[{'slug':s['url'].rsplit('/',1)[-1],'language':language(s['title']) or 'es'} for s in selected])
    ids=[s['id'] for s in selected]
    lore.write(ROOT/f'work/cohorts/{batch}.json',{'batch_id':batch,'source_ids':ids,'status':'selected','selected_at':lore.now(),'selection_method':f'{mode}: title-language heuristic; language verified during source reading'})
    print(f'Selected {len(ids)} new records for {batch}; {len(available)-len(ids)} other {mode} URLs remain.')

def ready(batch):
    cohort=lore.read(ROOT/f'work/cohorts/{batch}.json')
    manifest=lore.read(ROOT/'sources/manifest.json')
    sources={s['id']:s for s in manifest['sources']}
    ledger=lore.read(ROOT/'work/ledger.json')
    hashes={s['snapshot_sha256']:s['id'] for s in manifest['sources'] if s.get('snapshot_sha256') and ledger['jobs'].get(s['id'],{}).get('status')=='reviewed'}
    active=[]
    for sid in cohort['source_ids']:
        source=sources[sid]
        equivalent=hashes.get(source['snapshot_sha256'])
        if equivalent and equivalent!=sid:
            ledger['jobs'][sid].update(status='duplicate-exact',duplicate_of=equivalent,snapshot_sha256=source['snapshot_sha256'])
        else:
            hashes[source['snapshot_sha256']]=sid
            active.append(sid)
            ledger['jobs'][sid].update(status='running',attempts=ledger['jobs'][sid].get('attempts',0)+1,started_at=lore.now())
    for i in range(1,5):
        path=ROOT/f'work/batches/{batch}/worker-{i}.json'
        assignment=lore.read(path)
        assignment['source_ids']=[sid for sid in assignment['source_ids'] if sid in active]
        lore.write(path,assignment)
    # Review shards are stable independently of later cohort preparation.
    split=[[],[]]; totals=[0,0]
    for sid in sorted(active,key=lambda s:sources[s]['word_count'],reverse=True):
        i=min(range(2),key=lambda n:totals[n]); split[i].append(sid); totals[i]+=sources[sid]['word_count']
    for i,ids in enumerate(split,1): lore.write(ROOT/f'work/batches/{batch}/review-{i}.json',{'batch_id':batch,'reviewer':i,'source_ids':ids})
    cohort.update(status='running',active_source_ids=active,exact_duplicate_count=len(cohort['source_ids'])-len(active),source_word_count=sum(sources[s]['word_count'] for s in active))
    lore.write(ROOT/f'work/cohorts/{batch}.json',cohort)
    lore.write(ROOT/'work/ledger.json',ledger)
    print(f'{batch}: {len(active)} extraction jobs; {cohort["exact_duplicate_count"]} exact duplicates; {cohort["source_word_count"]} source words.')

def integrate(batch,cache):
    cohort=lore.read(ROOT/f'work/cohorts/{batch}.json')
    ledger=lore.read(ROOT/'work/ledger.json')
    sources={s['id']:s for s in lore.read(ROOT/'sources/manifest.json')['sources']}
    topics={t['id']:t for t in lore.read(ROOT/'config/topics.json')}
    approved=set(); errors=[]; corrections=0
    for i in range(1,3):
        report_path=ROOT/f'reports/batches/{batch}/review-{i}.json'
        if not report_path.exists(): errors.append({'reviewer':i,'error':'Review report missing'}); continue
        report=lore.read(report_path)
        if report.get('batch_id')!=batch or report.get('reviewer')!=i:
            raise ValueError('Review report identity does not match its assigned cohort/shard')
        assigned=set(lore.read(ROOT/f'work/batches/{batch}/review-{i}.json')['source_ids'])
        reviewed_ids=report.get('reviewed_source_ids',[])
        if not isinstance(reviewed_ids,list) or any(not isinstance(sid,str) for sid in reviewed_ids) or len(reviewed_ids)!=len(set(reviewed_ids)):
            raise ValueError('Review IDs must form a unique array; shared ledger unchanged')
        reviewed=set(reviewed_ids)
        if not reviewed<=assigned: raise ValueError('Review includes unassigned sources')
        blocked={item.get('source_id') for item in report.get('unresolved',[]) if item.get('severity') in ('high','medium')}
        approved.update(reviewed-blocked)
        corrections+=len(report.get('corrections',[]))
    active=set(cohort.get('active_source_ids',cohort['source_ids']))
    if errors or not active<=approved:
        raise ValueError('Independent review reports incomplete or blocked; shared ledger unchanged')
    for sid in cohort.get('active_source_ids',cohort['source_ids']):
        try:
            if sid not in approved: raise ValueError('Independent review incomplete or blocked')
            record=lore.read(ROOT/f'records/{sid}.json'); snapshot=lore.read(Path(cache)/f'{sid}.json')
            lore.validate_snapshot(snapshot,sources[sid]['snapshot_sha256'])
            # Canonical topic identity is stable; metadata variants are recorded for review.
            variants=[]
            for topic in record['proposed_topics']:
                if topic['id'] in topics and topic!=topics[topic['id']]:
                    variants.append({'proposed':copy.deepcopy(topic),'canonical':copy.deepcopy(topics[topic['id']])})
                    topic.update(topics[topic['id']])
            if variants:
                lore.write(ROOT/f'reports/topic-variants/{sid}.json',variants)
                lore.write(ROOT/f'records/{sid}.json',record)
            result=lore.validate_record(record,snapshot,topics)
            for topic in record['proposed_topics']: topics.setdefault(topic['id'],topic)
            ledger['jobs'][sid].update(status='reviewed',reviewed_at=lore.now(),snapshot_sha256=snapshot['snapshot_sha256'],record_sha256=lore.sha(__import__('json').dumps(record,sort_keys=True,ensure_ascii=False)),**result)
        except Exception as error:
            ledger['jobs'][sid]['status']='needs-correction'
            errors.append({'source_id':sid,'error':str(error)})
    lore.write(ROOT/'config/topics.json',list(topics.values()))
    ledger['updated_at']=lore.now(); lore.write(ROOT/'work/ledger.json',ledger)
    cohort.update(status='reviewed' if not errors else 'needs-correction',reviewed_at=lore.now(),review_corrections=corrections,integration_errors=errors)
    lore.write(ROOT/f'work/cohorts/{batch}.json',cohort)
    lore.write(ROOT/f'reports/batches/{batch}/integration.json',{'batch_id':batch,'reviewed_records':sum(ledger['jobs'][sid]['status']=='reviewed' for sid in cohort['source_ids']),'corrections':corrections,'errors':errors})
    print(f'{batch}: integrated {sum(ledger["jobs"][sid]["status"]=="reviewed" for sid in cohort["source_ids"])} reviewed records; {corrections} review corrections; {len(errors)} errors.')
    if errors: raise ValueError('Cohort integration requires correction')

def progress():
    ledger=lore.read(ROOT/'work/ledger.json'); manifest=lore.read(ROOT/'sources/manifest.json')
    counts=Counter(j['status'] for j in ledger['jobs'].values())
    reviewed=[sid for sid,j in ledger['jobs'].items() if j['status']=='reviewed']
    claims=sum(ledger['jobs'][sid].get('claim_count',0) for sid in reviewed)
    by_source={source['id']:source for source in manifest['sources']}
    languages=Counter(by_source[sid].get('language','unknown') for sid in reviewed)
    reviewed_words=sum(by_source[sid].get('word_count',0) for sid in reviewed)
    prepared_words=sum(source.get('word_count',0) for source in manifest['sources'])
    released_pending=sum(job['status']!='reviewed' and (ROOT/f'work/completed/{sid}.json').exists() for sid,job in ledger['jobs'].items())
    cohorts=[lore.read(p) for p in sorted((ROOT/'work/cohorts').glob('*.json'))] if (ROOT/'work/cohorts').exists() else []
    lines=['# Continuous collection progress','',f'Updated: {lore.now()}','',f'- Inventoried URLs: {manifest["record_count"]}',f'- Independently reviewed source records: {len(reviewed)}',f'- Source-specific claims: {claims}',f'- Original source words in reviewed records: {reviewed_words:,}',f'- Original source words prepared for processing: {prepared_words:,}',f'- Reviewed record languages: {dict(languages)}',f'- Released records awaiting completed independent review/integration: {released_pending}',f'- Exact duplicate URLs skipped: {counts["duplicate-exact"]}',f'- Unassigned URLs: {manifest["record_count"]-len(ledger["jobs"])}',f'- Assigned records still needing work: {len(ledger["jobs"])-len(reviewed)-counts["duplicate-exact"]}','','Source-record counts include retained language/revision variants and are not counts of independent corroborating accounts. Each record is a compact core extraction, not exhaustive coverage. English-first selection uses title heuristics plus coordinator review of ambiguous titles. Later cohorts process Spanish and remaining records; extracts are written in English, with original source language retained.','','| Cohort | Records selected | Records released | Records reviewed | Status | Review corrections |','| --- | ---: | ---: | ---: | --- | ---: |']
    for c in cohorts:
        released=sum((ROOT/f'work/completed/{sid}.json').exists() for sid in c['source_ids'])
        approved=sum(ledger['jobs'].get(sid,{}).get('status')=='reviewed' for sid in c['source_ids'])
        lines.append(f'| {c["batch_id"]} | {len(c["source_ids"])} | {released} | {approved} | {c["status"]} | {c.get("review_corrections",0)} |')
    lines += ['','## Resume','', 'Select a new cohort with `continuous.py select --batch <id> --size 40`, prepare its selection with `lore.py prepare --selection config/selections/<id>.json --batch <id>`, then run `continuous.py ready --batch <id>`. Assign four extraction shards and two independent review shards. Integrate completed reviews, build the wiki, and checkpoint. Completed ledger jobs are retained across cohorts.','','Review reports and integration errors are retained under `reports/batches/`. Failed downloads and records remain retryable; suspected translations are never skipped solely because their titles resemble another article.','']
    (ROOT/'reports/collection.md').write_text('\n'.join(lines),encoding='utf-8')
    print(dict(counts),'claims:',claims,'unassigned:',manifest['record_count']-len(ledger['jobs']))

def extracted(sid,cache):
    if not re.fullmatch(r'src-[a-f0-9]{12}',sid): raise ValueError('Invalid source ID')
    record=lore.read(ROOT/f'records/{sid}.json')
    snapshot=lore.read(Path(cache)/f'{sid}.json')
    topics={t['id']:t for t in lore.read(ROOT/'config/topics.json')}
    result=lore.validate_record(record,snapshot,topics)
    lore.write(ROOT/f'work/completed/{sid}.json',{'source_id':sid,'completed_at':lore.now(),'record_sha256':lore.sha(__import__('json').dumps(record,sort_keys=True,ensure_ascii=False)),**result})
    print(sid,'ready for independent review')

def wait_ready(batch,reviewer,excluded):
    assigned=lore.read(ROOT/f'work/batches/{batch}/review-{reviewer}.json')['source_ids']
    todo=[sid for sid in assigned if sid not in excluded]
    end=time.monotonic()+45
    while True:
        ready=[sid for sid in todo if (ROOT/f'work/completed/{sid}.json').exists() and (ROOT/f'records/{sid}.json').exists()]
        if ready or not todo or time.monotonic()>=end:
            print(__import__('json').dumps({'ready_source_ids':ready,'waiting_count':len(todo)-len(ready),'all_done':not todo,'observed_at':lore.now(),'record_directory':str(ROOT/'records'),'completion_directory':str(ROOT/'work/completed')})); return
        time.sleep(1)

parser=argparse.ArgumentParser(); sub=parser.add_subparsers(dest='command',required=True)
s=sub.add_parser('select'); s.add_argument('--batch',required=True); s.add_argument('--size',type=int,default=40); s.add_argument('--language',choices=('en','es','remaining'),default='en')
r=sub.add_parser('ready'); r.add_argument('--batch',required=True)
i=sub.add_parser('integrate'); i.add_argument('--batch',required=True); i.add_argument('--cache',default='../source-cache')
sub.add_parser('progress')
e=sub.add_parser('extracted'); e.add_argument('--source',required=True); e.add_argument('--cache',default='../source-cache')
w=sub.add_parser('wait-ready'); w.add_argument('--batch',required=True); w.add_argument('--reviewer',type=int,required=True); w.add_argument('--exclude',default='')
args=parser.parse_args()
if args.command in ('extracted','wait-ready'):
    if args.command=='extracted': extracted(args.source,args.cache)
    else: wait_ready(args.batch,args.reviewer,set(filter(None,args.exclude.split(','))))
else:
    with lore.coordinator_lock():
        if args.command=='select': select(args.batch,args.size,args.language)
        elif args.command=='ready': ready(args.batch)
        elif args.command=='integrate': integrate(args.batch,args.cache)
        else: progress()
