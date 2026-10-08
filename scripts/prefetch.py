#!/usr/bin/env python3
"""Prefetch successive cohorts without changing extraction or review ownership."""
import argparse
import subprocess
import sys
import time
import lore

parser=argparse.ArgumentParser()
parser.add_argument('--start',type=int,required=True)
parser.add_argument('--stop',type=int,required=True)
parser.add_argument('--size',type=int,default=160)
parser.add_argument('--language',choices=('en','es','remaining'),default='en')
parser.add_argument('--after')
parser.add_argument('--cache',default='../source-cache')
args=parser.parse_args()

def run(*arguments):
    subprocess.run([sys.executable,*arguments],cwd=lore.ROOT,check=True)

if args.after:
    while not (lore.ROOT/f'work/batches/{args.after}/review-1.json').exists():
        time.sleep(2)
for number in range(args.start,args.stop+1):
    batch=f'continuous-{number:03}'
    if not (lore.ROOT/f'work/batches/{batch}/worker-1.json').exists():
        if not (lore.ROOT/f'config/selections/{batch}.json').exists():
            run('scripts/continuous.py','select','--batch',batch,'--size',str(args.size),'--language',args.language)
        run('scripts/lore.py','prepare','--selection',f'config/selections/{batch}.json','--batch',batch,'--cache',args.cache)
    if not (lore.ROOT/f'work/batches/{batch}/review-1.json').exists():
        run('scripts/continuous.py','ready','--batch',batch)
    print('PREFETCH_READY',batch,flush=True)
