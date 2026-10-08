import json
from pathlib import Path
import shutil
import subprocess
import sys
import tempfile
import unittest

ROOT = Path(__file__).resolve().parents[1]

class ReviewGateTests(unittest.TestCase):
    def test_missing_review_report_preserves_existing_ledger_and_topics(self):
        with tempfile.TemporaryDirectory() as directory:
            root=Path(directory)
            (root/'scripts').mkdir()
            (root/'.git').mkdir()
            for name in ('lore.py','continuous.py'):
                shutil.copyfile(ROOT/'scripts'/name,root/'scripts'/name)
            sid='src-123456789abc'
            fixtures={
                'work/cohorts/test-batch.json':{'source_ids':[sid],'active_source_ids':[sid]},
                'work/ledger.json':{'jobs':{sid:{'status':'running'}}},
                'sources/manifest.json':{'sources':[]},
                'config/topics.json':[],
            }
            before={}
            for name,value in fixtures.items():
                path=root/name;path.parent.mkdir(parents=True,exist_ok=True)
                path.write_text(json.dumps(value))
                before[name]=path.read_bytes()
            result=subprocess.run([sys.executable,'scripts/continuous.py','integrate','--batch','test-batch'],cwd=root,capture_output=True,text=True)
            self.assertNotEqual(result.returncode,0)
            self.assertIn('shared ledger unchanged',result.stderr)
            for name,content in before.items():
                self.assertEqual((root/name).read_bytes(),content)
            self.assertFalse((root/'reports/batches/test-batch/integration.json').exists())

    def test_topic_variant_retains_original_metadata_after_normalization(self):
        import hashlib
        sha=lambda text:hashlib.sha256(text.encode()).hexdigest()
        with tempfile.TemporaryDirectory() as directory:
            root=Path(directory);(root/'scripts').mkdir();(root/'.git').mkdir()
            for name in ('lore.py','continuous.py'):
                shutil.copyfile(ROOT/'scripts'/name,root/'scripts'/name)
            sid='src-123456789abc';text='Speaker: Councils govern the territory.'
            digest=sha(text)
            canonical={'id':'politics','name':'Politics','kind':'institution','aliases':[]}
            proposed={'id':'politics','name':'Political councils','kind':'institution','aliases':['Council']}
            snapshot={'source_id':sid,'language':'en','snapshot_sha256':digest,'word_count':len(text.split()),'paragraphs':[{'id':'p0001','text':text,'sha256':digest}]}
            record={'source_id':sid,'language':'en','snapshot_sha256':digest,'claims':[{'id':sid+'-c01','assertion':'Councils govern the territory.','speaker':'Speaker','paragraph_ids':['p0001'],'primary_topic':'politics','topics':['politics'],'modality':'asserted','confidence':'high','qualifiers':''}],'proposed_topics':[proposed],'review_flags':[],'coverage_gaps':[]}
            fixtures={
                'work/cohorts/test-batch.json':{'batch_id':'test-batch','source_ids':[sid],'active_source_ids':[sid]},
                'work/ledger.json':{'jobs':{sid:{'status':'running'}}},
                'sources/manifest.json':{'sources':[{'id':sid,'snapshot_sha256':digest}]},
                'config/topics.json':[canonical],
                'records/'+sid+'.json':record,
                'cache/'+sid+'.json':snapshot,
            }
            for i,ids in ((1,[sid]),(2,[])):
                fixtures[f'work/batches/test-batch/review-{i}.json']={'source_ids':ids}
                fixtures[f'reports/batches/test-batch/review-{i}.json']={'batch_id':'test-batch','reviewer':i,'reviewed_source_ids':ids,'corrections':[],'unresolved':[]}
            for name,value in fixtures.items():
                path=root/name;path.parent.mkdir(parents=True,exist_ok=True);path.write_text(json.dumps(value))
            result=subprocess.run([sys.executable,'scripts/continuous.py','integrate','--batch','test-batch','--cache','cache'],cwd=root,capture_output=True,text=True)
            self.assertEqual(result.returncode,0,result.stderr)
            variant=json.loads((root/f'reports/topic-variants/{sid}.json').read_text())[0]
            self.assertEqual(variant['proposed'],proposed)
            self.assertEqual(variant['canonical'],canonical)
            self.assertEqual(json.loads((root/f'records/{sid}.json').read_text())['proposed_topics'],[canonical])
            self.assertEqual(json.loads((root/'work/ledger.json').read_text())['jobs'][sid]['status'],'reviewed')

    def test_duplicate_review_ids_rejected_before_ledger_changes(self):
        with tempfile.TemporaryDirectory() as directory:
            root=Path(directory);(root/'scripts').mkdir();(root/'.git').mkdir()
            for name in ('lore.py','continuous.py'):
                shutil.copyfile(ROOT/'scripts'/name,root/'scripts'/name)
            sid='src-123456789abc'
            fixtures={
                'work/cohorts/test-batch.json':{'source_ids':[sid],'active_source_ids':[sid]},
                'work/ledger.json':{'jobs':{sid:{'status':'running'}}},
                'sources/manifest.json':{'sources':[]},'config/topics.json':[],
                'work/batches/test-batch/review-1.json':{'source_ids':[sid]},
                'reports/batches/test-batch/review-1.json':{'batch_id':'test-batch','reviewer':1,'reviewed_source_ids':[sid,sid],'corrections':[],'unresolved':[]},
            }
            for name,value in fixtures.items():
                path=root/name;path.parent.mkdir(parents=True,exist_ok=True);path.write_text(json.dumps(value))
            before=(root/'work/ledger.json').read_bytes()
            result=subprocess.run([sys.executable,'scripts/continuous.py','integrate','--batch','test-batch'],cwd=root,capture_output=True,text=True)
            self.assertNotEqual(result.returncode,0)
            self.assertIn('unique array',result.stderr)
            self.assertEqual((root/'work/ledger.json').read_bytes(),before)

if __name__=='__main__':
    unittest.main()
