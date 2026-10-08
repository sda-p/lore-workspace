import json
from pathlib import Path
R=Path('/workspace/scratch/2b047f91e593/lore-workspace'); C=Path('/workspace/scratch/2b047f91e593/source-cache')
def add(sid, rows, flags=(), gaps=()):
 s=json.load(open(C/(sid+'.json')))
 claims=[dict(id=f'{sid}-c{i:02}',assertion=a,speaker=sp,paragraph_ids=ps,primary_topic=t,topics=ts,modality=m,confidence=c,qualifiers=q) for i,(a,sp,ps,t,ts,m,c,q) in enumerate(rows,1)]
 rec=dict(source_id=sid,snapshot_sha256=s['snapshot_sha256'],language=s['language'],claims=claims,proposed_topics=[],review_flags=list(flags),coverage_gaps=list(gaps))
 p=R/'records'/(sid+'.json'); p.write_text(json.dumps(rec,ensure_ascii=False,indent=2)+'\n')
add('src-06a1e5437c02',[
('Anéeka says parthenogenesis produced cloned Swaruu versions sharing synchronized consciousness.','Anéeka',['p0102','p0103','p0106'],'taygetans',['taygetans','consciousness-metaphysics'],'reported','high',''),
('Swaruu 2–9 repeatedly served as Sand Clock time-jump pilots altering Earth events.','Anéeka',['p0032','p0035','p0037'],'stellar-navigation',['stellar-navigation','taygetans'],'reported','high',''),
('Swaruu 9 stopped time-jumping after concluding changes affected only her own timeline.','Anéeka',['p0039'],'stellar-navigation',['stellar-navigation'],'reported','high',''),
('Anéeka says Swaruu 9 won independence from Federation space law and made Swaruu a species/legal name in 2018.','Anéeka',['p0072'],'galactic-federation',['galactic-federation','taygetans'],'reported','high',''),
('Anéeka and Yazhi describe Swaruu 9’s consciousness blending into Swaruu 12; Yazhi says she later dissolved the dead body.','Anéeka; Yazhi',['p0123','p0125','p0133','p0134','p0161'],'consciousness-metaphysics',['consciousness-metaphysics','taygetans'],'reported','medium','Their accounts distinguish mind assimilation from bodily disappearance.')
],['extraordinary_claims'],['biography_details','time_travel_methods'])
add('src-36a81d7c4f66',[
('Swaruu alleges Flavian rulers repurposed regional messianic beliefs to promote obedience to Rome.','Swaruu',['p0015','p0016','p0021'],'earth-cabal',['earth-cabal'],'reported','high',''),
('She says Titus and Vespasian built the savior narrative from confiscated regional documents.','Swaruu',['p0021'],'earth-cabal',['earth-cabal'],'reported','high',''),
('She presents Josephus and Roman networks as shaping Gospel accounts for Flavian purposes.','Swaruu',['p0033','p0034','p0045','p0048'],'earth-cabal',['earth-cabal'],'reported','medium',''),
('Swaruu says “Messiah” was a generic leader-title rather than unique to Jesus.','Swaruu',['p0025','p0026'],'terrestrial-science',['terrestrial-science'],'reported','high',''),
('She says her claimed stellar chronology conflicts with Earth accounts of crucifixion.','Swaruu',['p0117','p0118'],'terrestrial-science',['terrestrial-science'],'reported','high','She says her data places the punishment much later.')
],['extraordinary_history_claims','chronology_conflict'],['supporting_historical_evidence'])
add('src-476c3db82f6f',[
('Swaruu denies Jesus existed historically in this timeline and attributes the narrative to Flavian population control.','Swaruu',['p0002','p0003','p0005'],'earth-cabal',['earth-cabal'],'reported','high',''),
('She says Gospel accounts derive from Roman/Flavian sources and lack independent confirmation.','Swaruu',['p0008','p0010','p0012'],'terrestrial-science',['terrestrial-science','earth-cabal'],'reported','high',''),
('Swaruu distinguishes a collectively created Jesus concept from a historical person.','Swaruu',['p0043','p0050','p0079','p0087'],'consciousness-metaphysics',['consciousness-metaphysics'],'reported','high',''),
('She says ship systems respond to pilots’ beliefs, while Catholic cosmology obstructs supraluminal travel.','Swaruu',['p0054','p0058','p0062'],'starship-systems',['starship-systems','consciousness-metaphysics'],'reported','medium',''),
('Swaruu says religious institutions redirect spirituality toward external authority and social control.','Swaruu',['p0064','p0068','p0073'],'earth-cabal',['earth-cabal'],'reported','high','')
],['extraordinary_history_claims'],['institutional_history'])
add('src-19035581527f',[
('Swaruu depicts Cleopatra’s faction as cooperating with Rome and Arsinoe’s as resisting it.','Swaruu',['p0004','p0005','p0012'],'terrestrial-science',['terrestrial-science'],'reported','high',''),
('She says Arsinoe escaped Rome and advised Palestinian resistance as a guerrilla strategist.','Swaruu',['p0041','p0042','p0043'],'terrestrial-science',['terrestrial-science'],'reported','high',''),
('Swaruu says Cleopatra and Arsinoe both claimed Ishtar identity, dividing public allegiance.','Swaruu',['p0038'],'unicorn-symbolism',['unicorn-symbolism'],'reported','high',''),
('She identifies Mary Magdalene with Arsinoe and says Azazel relayed her teachings.','Swaruu',['p0071','p0073','p0082'],'terrestrial-science',['terrestrial-science'],'reported','high',''),
('Swaruu alleges Josephus’ scribes altered dates and recast Arsinoe as a prostitute to diminish resistance.','Swaruu',['p0077','p0088','p0089'],'earth-cabal',['earth-cabal','terrestrial-science'],'reported','high','')
],['extraordinary_history_claims'],['alternate_biography'])
add('src-9cfb205107c3',[
('Yazhi says awakening integrates all timelines of a person’s own experience, at least.','Yazhi',['p0064','p0066'],'consciousness-metaphysics',['consciousness-metaphysics'],'asserted','high',''),
('She frames freedom as a choice to help other selves or accept their suffering without attachment.','Yazhi',['p0025','p0068','p0075'],'consciousness-metaphysics',['consciousness-metaphysics'],'asserted','high',''),
('Yazhi says souls may incarnate into suffering for contrast and later seek integration.','Yazhi',['p0081'],'consciousness-metaphysics',['consciousness-metaphysics'],'asserted','high',''),
('She describes humanity as one being within a wider collective being.','Yazhi',['p0085'],'consciousness-metaphysics',['consciousness-metaphysics'],'asserted','high',''),
('Yazhi says service to others aligns with self-interest because others are also oneself.','Yazhi',['p0087','p0089'],'holistic-society',['holistic-society','consciousness-metaphysics'],'asserted','high','')
],[],['philosophical_discussion'])
add('src-792e153c2f4a',[
('Yazhi says crystal data can be encoded in molecular rearrangements or mapped frequency grids.','Yazhi',['p0023','p0024','p0026'],'holographic-computers',['holographic-computers'],'asserted','high',''),
('She says mapped crystals retain data while frequencies are imposed or as persistent oscillations.','Yazhi',['p0027'],'holographic-computers',['holographic-computers'],'asserted','high',''),
('Yazhi describes a contained miniature sun as a ship reactor, with induction and heat converted to electricity.','Yazhi',['p0054','p0064','p0065','p0069'],'energy-generation',['energy-generation','starship-systems'],'asserted','high',''),
('She says excess heat is a major starship hazard managed through thermoelectric cells, plates, and steam.','Yazhi',['p0069','p0083'],'starship-systems',['starship-systems','energy-generation'],'asserted','high',''),
('Yazhi says harmonic or gravity-control failures can shut down the reactor or disperse its crystal toroid.','Yazhi',['p0093','p0095','p0099'],'starship-systems',['starship-systems','energy-generation'],'asserted','high','')
],['extraordinary_technology_claims'],['human_technology_limits'])
add('src-412d2cb274cb',[
('Yazhi says Lemurian Evas freed Adamic people held by Atlantean controllers in Turkey.','Yazhi',['p0003','p0007','p0011'],'atlantis-lemuria',['atlantis-lemuria'],'asserted','high',''),
('She describes Lemuria as a holographic matriarchy aided mainly by Taygeta, with Solatian and Engan cooperation.','Yazhi',['p0009'],'holistic-society',['holistic-society','taygetans'],'asserted','high',''),
('Yazhi says the conflict escalated into a multi-century interstellar war between mostly Lyrian and Reptilian-backed sides.','Yazhi',['p0019','p0020'],'orion-wars',['orion-wars','atlantis-lemuria','alien-species'],'asserted','high',''),
('She attributes Tiamat’s destruction and Mars devastation to nuclear battles fought with spacecraft.','Yazhi',['p0024','p0026'],'tiamat',['tiamat','atlantis-lemuria'],'asserted','high',''),
('Yazhi says plasma weapons could destroy underground bases without nuclear radiation.','Yazhi',['p0028','p0029','p0030'],'starship-systems',['starship-systems'],'asserted','high','')
],['extraordinary_history_claims','translated_source'],['war_timeline'])
add('src-09e26ee299cd',[
('Yazhi says timelines intersect and influence one another, shaping a shared present.','Yazhi',['p0010','p0011','p0014'],'consciousness-metaphysics',['consciousness-metaphysics'],'asserted','high',''),
('She presents linear chronology as an explanatory arrangement rather than a fixed account.','Yazhi',['p0003','p0004','p0023'],'consciousness-metaphysics',['consciousness-metaphysics'],'asserted','high',''),
('Yazhi says contradictory event histories may converge into present reality.','Yazhi',['p0012','p0013'],'consciousness-metaphysics',['consciousness-metaphysics'],'asserted','high',''),
('She says there is no time independent of consciousness; attention creates experienced sequence.','Yazhi',['p0027'],'consciousness-metaphysics',['consciousness-metaphysics'],'asserted','high',''),
('Yazhi calls her own account an interpreted alternative, drawing partly on Federation and Taygetan data.','Yazhi',['p0002','p0015','p0028'],'consciousness-metaphysics',['consciousness-metaphysics'],'reported','high','')
],[],['history_methodology'])
add('src-ce9c92fd3b4e',[
('Anéeka says Venus remains under regressive control, while Mars is divided among Cabal, Maitre, and Ojalu’s Mantis.','Anéeka',['p0015','p0021'],'alien-species',['alien-species','earth-cabal'],'reported','high',''),
('She says Earth’s liberation would free Venus, described as an Earth Cabal colony.','Anéeka',['p0036','p0042'],'earth-cabal',['earth-cabal'],'reported','high',''),
('Anéeka describes Venus as a low-population water world with a stable, gentle climate.','Anéeka',['p0033'],'alien-species',['alien-species'],'reported','high',''),
('She says Federation forces classify Venus and Earth as regressive-controlled planets in this sector.','Anéeka',['p0025','p0026'],'galactic-federation',['galactic-federation','earth-cabal'],'reported','high',''),
('Anéeka says peaceful planets relying on high frequency as protection were easily invaded.','Anéeka',['p0044','p0045'],'galactic-federation',['galactic-federation'],'reported','high','')
],['extraordinary_claims','translated_source'],['planetary_roster'])
add('src-5a5946c015e8',[
('Yazhi says Taygetan toys use durable, non-toxic composite resin rather than plastic.','Yazhi',['p0003','p0005'],'taygetans',['taygetans','economics'],'reported','high',''),
('She says children often handcraft toys or design them for household replicators.','Yazhi',['p0005','p0006'],'taygetans',['taygetans','holographic-computers'],'reported','high',''),
('Yazhi says toy preferences reflect gender identities, without restrictions on who may play with them.','Yazhi',['p0007'],'taygetans',['taygetans','holistic-society'],'reported','high',''),
('Raguel describes a Taygetan board game requiring spatial planning, memory, and mostly telepathic exchange.','Raguel',['p0013','p0016'],'taygetans',['taygetans','consciousness-metaphysics'],'reported','high',''),
('Raguel says the crew plays Earth video games but prefers their less immersive quality.','Raguel',['p0020','p0021'],'taygetans',['taygetans'],'reported','high','')
],[],['recreation_details'])
