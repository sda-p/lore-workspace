import json
sid='src-2bf76cf1cd2e'
claims=[
('Earth–Temmer time slip is nearly five Earth days per Temmer day; Swaruu X says this gap widened from 4.5:1 in 2019 to about 4.7–4.8:1 by 2021.','p0004','temporal-skipping','reported','high','Figures are source-period claims.'),
('Swaruu X attributes planetary time perception to consciousness and collective thought, and says Earth’s collective consciousness was regressing.','p0009','consciousness-metaphysics','asserted','high',''),
('Swaruu X says Van Allen belts set Earth’s baseline existential frequency, while sufficiently elevated consciousness can transcend their limiting effect.','p0021','van-allen-belts','asserted','high','Her numerical frequency scale is explicitly illustrative.'),
('Swaruu X describes the brain as translating nonphysical experiences into physical memories; offworld memories may remain unprocessed in Earth bodies.','p0031','consciousness-metaphysics','asserted','high',''),
('Swaruu X says DNA encodes a body’s life plan, which she links to agreements made between lives.','p0042','dna-metaphysics','asserted','high','')]
record={'source_id':sid,'snapshot_sha256':'f16bfd94be141ce19c42c955681ca680c83a252a2b7b84c9c1e45fefc5ac7f08','language':'es','claims':[], 'proposed_topics':[], 'review_flags':['Van Allen belts both set a baseline and can be transcended; preserve distinction.'], 'coverage_gaps':['Schumann resonance','galactic waves','space-storm mechanics','astrological ages']}
for i,(a,p,t,m,c,q) in enumerate(claims,1): record['claims'].append({'id':f'{sid}-c{i:02d}','assertion':a,'speaker':'Swaruu X (Athena)','paragraph_ids':[p],'primary_topic':t,'topics':[t], 'modality':m,'confidence':c,'qualifiers':q})
with open(f'records/{sid}.json','w') as f: json.dump(record,f,ensure_ascii=False,indent=2); f.write('\n')
print(sum(len(c['assertion'].split())+len(c['qualifiers'].split()) for c in record['claims']))
