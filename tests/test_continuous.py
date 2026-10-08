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

if __name__=='__main__':
    unittest.main()
