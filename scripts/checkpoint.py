#!/usr/bin/env python3
"""Read a bounded UTF-8 publication snapshot for authenticated GitHub tools.

No credentials are handled here. 'list' captures publishable files outside the
working tree so later bounded reads cannot race an edit. Raw source caches and
Git internals are excluded by Git's own tracked/untracked file enumeration.
"""
import argparse
import json
from pathlib import Path
import subprocess

ROOT=Path(__file__).resolve().parents[1]
SNAPSHOT=ROOT.parent/'publication-snapshot'

parser=argparse.ArgumentParser()
sub=parser.add_subparsers(dest='command',required=True)
lister=sub.add_parser('list')
lister.add_argument('--changed',action='store_true')
lister.add_argument('--summary',action='store_true')
lister.add_argument('--released-only',action='store_true',help='Exclude unreleased article drafts from the publication snapshot')
reader=sub.add_parser('read')
reader.add_argument('--path',required=True)
reader.add_argument('--offset',type=int,default=0)
reader.add_argument('--length',type=int,default=12000)
args=parser.parse_args()

if args.command=='list':
    ledger_path=ROOT/'work/ledger.json'
    jobs=json.loads(ledger_path.read_text(encoding='utf-8')).get('jobs',{}) if args.released_only and ledger_path.exists() else {}
    if args.changed:
        tracked=subprocess.run(['git','diff','--name-only','--diff-filter=ACMRT','HEAD','-z'],cwd=ROOT,capture_output=True,check=True)
        untracked=subprocess.run(['git','ls-files','--others','--exclude-standard','-z'],cwd=ROOT,capture_output=True,check=True)
        names=tracked.stdout+untracked.stdout
    else:
        names=subprocess.run(['git','ls-files','--cached','--others','--exclude-standard','-z'],cwd=ROOT,capture_output=True,check=True).stdout
    files=[]
    elements=[]
    deleted=[]
    if args.changed:
        result=subprocess.run(['git','diff','--name-only','--diff-filter=D','HEAD','-z'],cwd=ROOT,capture_output=True,check=True)
        deleted=sorted(set(result.stdout.decode().split('\0'))-{''})
        elements.extend({'path':name,'mode':'100644','type':'blob','sha':None} for name in deleted)
    for name in sorted(set(names.decode().split('\0'))- {''}):
        path=ROOT/name
        if not path.is_file() or name.endswith('.tmp'): continue
        if any(part.startswith('.tmp-') for part in Path(name).parts): continue
        if args.released_only and name.startswith('records/') and path.suffix=='.json':
            source_id=path.stem
            if jobs.get(source_id,{}).get('status')!='reviewed' and not (ROOT/f'work/completed/{source_id}.json').exists():
                continue
        if path.is_symlink(): raise ValueError('Refusing to publish symlinks')
        content=path.read_text(encoding='utf-8')
        target=SNAPSHOT/name
        target.parent.mkdir(parents=True,exist_ok=True)
        target.write_text(content,encoding='utf-8')
        files.append({'path':name,'characters':len(content)})
        elements.append({'path':name,'mode':'100644','type':'blob','content':content})
    parent=subprocess.run(['git','rev-parse','HEAD'],cwd=ROOT,capture_output=True,text=True,check=True).stdout.strip()
    tree=subprocess.run(['git','rev-parse','HEAD^{tree}'],cwd=ROOT,capture_output=True,text=True,check=True).stdout.strip()
    metadata={'parent_sha':parent,'base_tree_sha':tree,'files':files,'deleted':deleted}
    if args.summary:
        value=json.dumps(metadata)
        (SNAPSHOT/'.checkpoint-index.json').write_text(value,encoding='utf-8')
        bundle=json.dumps({'parent_sha':parent,'base_tree_sha':tree,'elements':elements})
        (SNAPSHOT/'.checkpoint-bundle.json').write_text(bundle,encoding='utf-8')
        print(json.dumps({'parent_sha':parent,'base_tree_sha':tree,'file_count':len(files),'index_characters':len(value),'bundle_characters':len(bundle),'total_characters':sum(f['characters'] for f in files)}))
    else:
        print(json.dumps(metadata))
else:
    path=(SNAPSHOT/args.path).resolve()
    if not path.is_relative_to(SNAPSHOT.resolve()): raise ValueError('Invalid snapshot path')
    if args.offset<0 or not 0<args.length<=12000: raise ValueError('Invalid chunk bounds')
    print(json.dumps(path.read_text(encoding='utf-8')[args.offset:args.offset+args.length],ensure_ascii=False))
