import copy
import importlib.util
import json
from pathlib import Path
import tempfile
import unittest
from unittest.mock import patch

spec = importlib.util.spec_from_file_location('lore',Path(__file__).resolve().parents[1]/'scripts/lore.py')
lore = importlib.util.module_from_spec(spec)
spec.loader.exec_module(lore)

class IntegrityTests(unittest.TestCase):
    def setUp(self):
        self.snapshot={'source_id':'src-123456789abc','snapshot_sha256':'a'*64,'language':'en','paragraphs':[{'id':'p0001','text':'Title'},{'id':'p0002','text':'Speaker: Claim'}]}
        for passage in self.snapshot['paragraphs']: passage['sha256']=lore.sha(passage['text'])
        self.snapshot['snapshot_sha256']=lore.sha('\n'.join(p['text'] for p in self.snapshot['paragraphs']))
        self.snapshot['word_count']=sum(len(p['text'].split()) for p in self.snapshot['paragraphs'])
        self.record={'source_id':'src-123456789abc','snapshot_sha256':'a'*64,'language':'en','claims':[{'id':'src-123456789abc-c01','assertion':'Councils govern settlements.','speaker':'Speaker','paragraph_ids':['p0002'],'primary_topic':'politics','topics':['politics'],'modality':'asserted','confidence':'high','qualifiers':''}],'proposed_topics':[],'review_flags':[],'coverage_gaps':[]}
        self.record['snapshot_sha256']=self.snapshot['snapshot_sha256']

    def test_transcript_body_excludes_navigation_and_keeps_turns(self):
        html='<nav>Ignore navigation</nav><div class="transcript-content"><p>Title</p><p><b>Gosia:</b> Question?<br><br><b>Swaruu:</b> Answer &amp; qualifier.</p></div>'
        result=lore.parse_article(html)
        self.assertEqual([p['text'] for p in result['paragraphs']],['Title','Gosia: Question?','Swaruu: Answer & qualifier.'])

    def test_missing_body_fails_closed(self):
        with self.assertRaises(ValueError): lore.parse_article('<p>Navigation only</p>')

    def test_known_evidence_is_valid(self):
        self.assertEqual(lore.validate_record(self.record,self.snapshot,{'politics'})['claim_count'],1)

    def test_unknown_passage_rejected(self):
        self.record['claims'][0]['paragraph_ids']=['p9999']
        with self.assertRaises(ValueError): lore.validate_record(self.record,self.snapshot,{'politics'})

    def test_changed_snapshot_rejected(self):
        self.record['snapshot_sha256']='b'*64
        with self.assertRaises(ValueError): lore.validate_record(self.record,self.snapshot,{'politics'})

    def test_duplicate_claim_rejected(self):
        self.record['claims'].append(copy.deepcopy(self.record['claims'][0]))
        with self.assertRaises(ValueError): lore.validate_record(self.record,self.snapshot,{'politics'})

    def test_unregistered_topic_rejected(self):
        with self.assertRaises(ValueError): lore.validate_record(self.record,self.snapshot,{'other'})

    def test_changed_passage_without_new_hash_rejected(self):
        self.snapshot['paragraphs'][1]['text']='Speaker: Altered claim'
        with self.assertRaises(ValueError): lore.validate_record(self.record,self.snapshot,{'politics'})

    def test_rehashed_cache_with_old_manifest_hash_rejected(self):
        expected=self.snapshot['snapshot_sha256']
        self.snapshot['paragraphs'][1]['text']='Speaker: Altered claim'
        self.snapshot['paragraphs'][1]['sha256']=lore.sha('Speaker: Altered claim')
        self.snapshot['snapshot_sha256']=lore.sha('\n'.join(p['text'] for p in self.snapshot['paragraphs']))
        with self.assertRaises(ValueError): lore.validate_snapshot(self.snapshot,expected)

    def test_non_string_review_tag_rejected(self):
        self.record['review_flags']=[{}]
        with self.assertRaises(ValueError): lore.validate_record(self.record,self.snapshot,{'politics'})

    def test_zero_claim_sequence_rejected(self):
        self.record['claims'][0]['id']='src-123456789abc-c00'
        with self.assertRaises(ValueError): lore.validate_record(self.record,self.snapshot,{'politics'})

    def test_topic_path_traversal_rejected(self):
        self.record['proposed_topics']=[{'id':'../escape','name':'Unsafe','kind':'faction','aliases':[]}]
        with self.assertRaises(ValueError): lore.validate_record(self.record,self.snapshot,{'politics'})

    def test_topic_collision_rejected(self):
        self.record['proposed_topics']=[{'id':'politics','name':'Different','kind':'faction','aliases':[]}]
        with self.assertRaises(ValueError): lore.validate_record(self.record,self.snapshot,{'politics'})

    def test_previously_promoted_topic_can_be_revalidated(self):
        topic={'id':'politics','name':'Politics','kind':'institution','aliases':[]}
        self.record['proposed_topics']=[topic.copy()]
        self.assertEqual(lore.validate_record(self.record,self.snapshot,{'politics':topic})['claim_count'],1)

    def test_markdown_link_text_is_escaped(self):
        self.assertEqual(lore.md('[label](https://unexpected.example)'),r'\[label\](https://unexpected.example)')

    def test_unexpected_source_domain_rejected(self):
        with self.assertRaises(ValueError): lore.source_url('https://unexpected.example/transcripts/test')

    def test_inactive_ledger_jobs_are_retained(self):
        previous={'old-source':{'status':'reviewed','worker':1}}
        jobs=lore.retain_jobs(previous)
        jobs['new-source']={'status':'pending'}
        self.assertEqual(jobs['old-source']['status'],'reviewed')
        jobs['old-source']['worker']=2
        self.assertEqual(previous['old-source']['worker'],1)

    def test_changed_approved_record_cannot_rebuild_wiki(self):
        with tempfile.TemporaryDirectory() as directory:
            root=Path(directory)
            original=copy.deepcopy(self.record)
            digest=lore.sha(json.dumps(original,sort_keys=True,ensure_ascii=False))
            changed=copy.deepcopy(original)
            changed['claims'][0]['assertion']='A new claim added after approval.'
            fixtures={
                'sources/manifest.json':{'sources':[]},
                'config/topics.json':[],
                'work/ledger.json':{'jobs':{original['source_id']:{'status':'reviewed','record_sha256':digest}}},
                f"records/{original['source_id']}.json":changed,
            }
            for name,value in fixtures.items():
                path=root/name;path.parent.mkdir(parents=True,exist_ok=True);path.write_text(json.dumps(value))
            index=root/'wiki/index.md';index.parent.mkdir();index.write_text('Previous approved wiki')
            with patch.object(lore,'ROOT',root):
                with self.assertRaisesRegex(ValueError,'changed since approval'):
                    lore.build()
            self.assertEqual(index.read_text(),'Previous approved wiki')

if __name__=='__main__': unittest.main()
