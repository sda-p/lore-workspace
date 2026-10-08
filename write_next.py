import json
sid='src-a18d1af875eb';sha='bc2e13f8cb6eaf6d9f68d5f918adbe3c3e9017fe28b0f228f166dd6ee6439944'
claims=[
('Swaruu 9 says Tiamat’s destruction shifted planetary orbits; Saturn captured debris that formed its rings.',['p0007','p0010','p0014','p0015'],'tiamat','asserted','high',''),
('She says Saturn’s moons host colonies and relay stations for many species; the region passed from Sauroid to Federation-aligned control.',['p0026','p0036','p0050','p0052'],'saturn-bases','asserted','medium',''),
('Saturn’s rings are mined for essential metals, especially gold, and support passing-ship resupply.',['p0037','p0038'],'economics','asserted','high',''),
('Swaruu 9 says a destroyed 5-km Sauroid cube once served as a Saturn-region base; Saturn itself is not inherently evil.',['p0054','p0059','p0061'],'saturn-bases','asserted','medium',''),
('She says natural portals occur on every celestial body; artificial portals can strand users if exit control is lost.',['p0100','p0101','p0103','p0106'],'natural-portals','asserted','high','')]
d={'source_id':sid,'snapshot_sha256':sha,'language':'es','claims':[],'proposed_topics':[],'review_flags':['Regional Sauroid control is distinct from Saturn itself; source dates its end to 2012.'],'coverage_gaps':['Titan and Enceladus development','gas-giant life','Saturn symbolism']}
for i,(a,ps,t,m,c,q) in enumerate(claims,1):d['claims'].append({'id':f'{sid}-c{i:02d}','assertion':a,'speaker':'Swaruu (9)','paragraph_ids':ps,'primary_topic':t,'topics':[t],'modality':m,'confidence':c,'qualifiers':q})
json.dump(d,open(f'records/{sid}.json','w'),ensure_ascii=False,indent=2);open(f'records/{sid}.json','a').write('\n')
print('words',sum(len(c['assertion'].split())+len(c['qualifiers'].split()) for c in d['claims']))
