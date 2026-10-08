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
sub.add_parser('list')
reader=sub.add_parser('read')
reader.add_argument('--path',required=True)
reader.add_argument('--offset',type=int,default=0)
reader.add_argument('--length',type=int,default=12000)
args=parser.parse_args()

if args.command=='list':
    result=subprocess.run(['git','ls-files','--cached','--others','--exclude-standard','-z'],cwd=ROOT,capture_output=True,check=True)
    files=[]
    for name in sorted(set(result.stdout.decode().split('\0'))- {''}):
        path=ROOT/name
        if not path.is_file(): continue
        if path.is_symlink(): raise ValueError('Refusing to publish symlinks')
        content=path.read_text(encoding='utf-8')
        target=SNAPSHOT/name
        target.parent.mkdir(parents=True,exist_ok=True)
        target.write_text(content,encoding='utf-8')
        files.append({'path':name,'characters':len(content)})
    parent=subprocess.run(['git','rev-parse','HEAD'],cwd=ROOT,capture_output=True,text=True,check=True).stdout.strip()
    tree=subprocess.run(['git','rev-parse','HEAD^{tree}'],cwd=ROOT,capture_output=True,text=True,check=True).stdout.strip()
    print(json.dumps({'parent_sha':parent,'base_tree_sha':tree,'files':files}))
else:
    path=(SNAPSHOT/args.path).resolve()
    if not path.is_relative_to(SNAPSHOT.resolve()): raise ValueError('Invalid snapshot path')
    if args.offset<0 or not 0<args.length<=12000: raise ValueError('Invalid chunk bounds')
    print(json.dumps(path.read_text(encoding='utf-8')[args.offset:args.offset+args.length],ensure_ascii=False))
