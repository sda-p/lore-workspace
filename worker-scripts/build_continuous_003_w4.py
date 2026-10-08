import json
from pathlib import Path
cache=Path('/workspace/scratch/2b047f91e593/source-cache')
records=Path('records')
data={
'src-919dc7641045':[
('Swaruu (9)','Taygetans classify them as primary species; humans are secondary, adaptable bodies.',['p0013','p0014','p0015','p0016'],'alien-species','asserted'),
('Swaruu (9)','She says human genetic change is shaped by consciousness and beliefs, not solely laboratory alteration.',['p0031','p0032','p0034'],'consciousness-metaphysics','asserted'),
('Swaruu (9)','She rejects the claim humans were assembled from 21 alien species, citing broad shared carbon-based genetics.',['p0041','p0042','p0044','p0045'],'alien-species','asserted'),
('Swaruu (9)','She describes starseeds as mental or conscious hybrids, usually without mixed extraterrestrial parentage.',['p0074','p0076','p0078'],'alien-species','asserted'),
('Swaruu (9)','She says dog lineages may revert over generations, depending on dominant traits and ongoing breeding.',['p0063','p0065','p0067','p0071','p0072'],'alien-species','asserted')],
'src-30ad5c1df3fd':[
('Swaruu','Time is described as consciousness sequencing perceived events, rather than an external process.',['p0005','p0008','p0018','p0019'],'consciousness-metaphysics','asserted'),
('Swaruu','Her navigation model assigns a frequency address to a place and uses progression factors to specify arrival time.',['p0053','p0058','p0075','p0082','p0087'],'stellar-navigation','asserted'),
('Swaruu','She describes past, present, and future as fixed snapshots that observers animate through attention.',['p0223','p0228','p0229','p0251','p0256'],'consciousness-metaphysics','asserted'),
('Swaruu','A personal timeline is defined as one consciousness’s event sequence; group timelines reflect shared perceptual agreements.',['p0314','p0315','p0325','p0329','p0332'],'consciousness-metaphysics','asserted'),
('Swaruu','She says feelings and emotions guide frequency-based choices among timelines.',['p0376','p0378','p0380','p0415','p0418'],'consciousness-metaphysics','asserted')],
'src-cf646873c491':[
('Swaruu (9)','She says mass contact lacks a viable channel because humans are unprepared and governments or media will not cooperate.',['p0003','p0007','p0008','p0009','p0011'],'galactic-federation','asserted'),
('Swaruu (9)','She portrays regressive visitors as opportunistic, while saying human and other-race dynamics jointly sustain the problem.',['p0012','p0015','p0018','p0019','p0021'],'alien-species','asserted'),
('Swaruu (9)','The First Contact project reportedly ended around November 2016 after its goal was met; command later shifted to Centauri.',['p0039'],'galactic-federation','reported'),
('Swaruu (9)','She says Taygetan presence near Earth had been reduced to one ship and two active communicators.',['p0040','p0041'],'taygetans','reported'),
('Swaruu (9)','Ascension is described as individual integration of understanding; galactic energy may promote, but does not determine, it.',['p0049','p0050','p0051','p0053'],'consciousness-metaphysics','asserted')],
'src-ffa5ee8fb668':[
('Dhor Káal’el','Dhor estimates his chronological age at about 10,000 years, while appearing roughly 21–25.',['p0017','p0018','p0019','p0022','p0023'],'taygetans','reported'),
('Dhor Káal’el','He says his work is preparing Earth’s population for withdrawal of the artificial 3D Matrix.',['p0091','p0092','p0093','p0094'],'moon-matrix','asserted'),
('Dhor Káal’el','He describes Taygeta as matriarchal, while men may take command roles as equals if they choose.',['p0118','p0123','p0132','p0133','p0135','p0136'],'holistic-society','asserted'),
('Dhor Káal’el','He rejects military takeover as counterproductive, while describing defensive coordination against regressive forces.',['p0160','p0161','p0163','p0166','p0167'],'galactic-federation','asserted'),
('Dhor Káal’el','He says about ten crew members speak human languages, limiting personal contact with thousands of people.',['p0259','p0260','p0261','p0265','p0266'],'taygetans','asserted')],
'src-b7bd29d43438':[
('Swaruu (9)','She lists three proposed sources of unexplained sky sounds; HAARP-like frequency use is described as widespread.',['p0003','p0004','p0005','p0006','p0007'],'earth-cabal','reported'),
('Swaruu (9)','She describes “Men in Black” as human law enforcement, covert human agents, and nonhuman intimidators.',['p0013','p0014','p0015'],'earth-cabal','asserted'),
('Swaruu (9)','She characterizes the UN as a Cabal vehicle for world government and says Taygetans briefly contacted it in the late 1950s.',['p0020','p0021'],'earth-cabal','asserted'),
('Anéeka','She says Taygetan air has about 78% oxygen and 20% nitrogen, the reverse of Earth’s proportions.',['p0022','p0023'],'taygetans','asserted'),
('Swaruu (9)','She says open contact should leave Earth’s liberation credit to its inhabitants, partly to avoid outside savior status.',['p0030','p0031'],'galactic-federation','asserted')],
'src-7454e687009f':[
('Swaruu','She says animal lifespans are difficult to compare because time is relative; a cat might exceed 1,000 years.',['p0019','p0020','p0025','p0026'],'consciousness-metaphysics','speculative'),
('Swaruu','Animal death is described as energetic fatigue or loss of purpose rather than bodily decay alone.',['p0030','p0035','p0036'],'consciousness-metaphysics','asserted'),
('Dhor Káal’el','He says animals may not share human “soul trap” concepts and that Ringo likely returned to Source.',['p0093','p0098','p0101','p0104','p0105'],'consciousness-metaphysics','reported'),
('Dhor Káal’el','He describes souls as nonlocal and suggests a frequency spectrometer could track a soul’s mirrors across incarnations.',['p0116','p0120','p0124','p0130','p0134'],'consciousness-metaphysics','speculative'),
('Dhor Káal’el','He says received love remains part of an animal’s soul, which experiences loved ones as present.',['p0139','p0140','p0156','p0157','p0160'],'consciousness-metaphysics','asserted')],
'src-6b41f329ba76':[
('Swaruu','She says electrogravitic coils need gravity-frequency sensing and modulation to avoid wasted output.',['p0034','p0036','p0037','p0038','p0039','p0040'],'starship-systems','asserted'),
('Swaruu','She identifies copper resistance and fixed frequency as major limits; nested tunable coils may help.',['p0064','p0068','p0072','p0073','p0076','p0079','p0080','p0082'],'starship-systems','asserted'),
('Swaruu','She says the proposed Rodin-coil setup consumes more energy than it produces and cannot provide zero-point power.',['p0087','p0088','p0096','p0097','p0098'],'starship-systems','asserted'),
('Swaruu','She describes counter-rotating magnetic pulse turbines as a starship-engine principle.',['p0211','p0212','p0213','p0218','p0219','p0220'],'starship-systems','asserted'),
('Swaruu','She says these engines require unavailable high-temperature alloys, ideally smelted in zero gravity.',['p0229','p0230','p0231','p0239','p0240','p0245'],'starship-systems','asserted')],
'src-dca3fe7e225f':[
('Swaruu','She frames the confinement and media cycle as fear-generating manipulation, and urges starseeds to maintain focus.',['p0008','p0009','p0010','p0011'],'earth-cabal','asserted'),
('Swaruu','She advises reducing media exposure and using meditation, hobbies, exercise, and hands-on activities.',['p0011','p0012','p0013','p0014'],'consciousness-metaphysics','asserted'),
('Swaruu','She says positive intention should be paired with practical action to change circumstances.',['p0018','p0019'],'consciousness-metaphysics','asserted'),
('Swaruu','She defines starseed identity as self-known, without requiring external confirmation.',['p0015','p0016'],'consciousness-metaphysics','asserted'),
('Swaruu','She tells starseeds to sustain a positive timeline through personal focus and action.',['p0015','p0021'],'consciousness-metaphysics','asserted')],
'src-d7282a4e99a9':[
('Swaruu of Erra','The described plasma turbine uses counter-rotating drums and frequency-controlled plasma flow.',['p0017','p0018','p0019','p0022','p0026','p0031'],'starship-systems','asserted'),
('Swaruu of Erra','Closing the engine circuit creates a high-energy toroid that sets the ship’s frequency.',['p0043','p0045','p0047','p0050','p0063','p0065'],'starship-systems','asserted'),
('Swaruu of Erra','Warp navigation matches the toroid frequency to a stellar frequency map instead of traversing distance.',['p0078','p0080','p0083','p0085','p0090','p0092'],'stellar-navigation','asserted'),
('Swaruu of Erra','She describes the jump as instantaneous through the ether, with perceived travel time arising inside the ship.',['p0093','p0094','p0096','p0112','p0122','p0124'],'stellar-navigation','asserted')],
'src-deac39f68d91':[
('Swaruu','She says integrating new information into the subconscious frees conscious attention for further learning.',['p0011','p0012','p0014','p0016','p0017','p0030','p0033'],'consciousness-metaphysics','asserted'),
('Swaruu','She contrasts integrated learning with information overload, which she associates with mental strain.',['p0025','p0026','p0027','p0028','p0030','p0032'],'consciousness-metaphysics','asserted'),
('Swaruu','She describes 5D-to-3D frequency mismatch as overloading an extraterrestrial’s nervous system.',['p0055','p0058','p0062','p0064','p0069'],'alien-species','asserted'),
('Swaruu','A toroidal belt device is said to technologically slow temporal frequency during 5D-to-3D immersion.',['p0071','p0072','p0073','p0077','p0078','p0080'],'starship-systems','asserted')]
}
gaps={
'src-919dc7641045':['species-taxonomy','hybridization','animal-genetics'],
'src-30ad5c1df3fd':['time-perception','timeline-navigation','frequency-choice'],
'src-cf646873c491':['contact-policy','fleet-deployment','planetary-mission'],
'src-ffa5ee8fb668':['pilot-profile','taygetan-gender-roles','contact-capacity'],
'src-b7bd29d43438':['sky-sound-causes','blockade','historical-records'],
'src-7454e687009f':['animal-incarnation','soul-mirrors','grief'],
'src-6b41f329ba76':['coil-materials','turbine-principles','zero-point-limits'],
'src-dca3fe7e225f':['dated-message-claims','starseed-advice'],
'src-d7282a4e99a9':['turbine-construction','ether-jump'],
'src-deac39f68d91':['frequency-dissonance','temporal-devices']}
for sid,items in data.items():
 s=json.load(open(cache/(sid+'.json'))); claims=[]
 for i,(speaker,assertion,pids,topic,modality) in enumerate(items,1):
  claims.append({'id':f'{sid}-c{i:02d}','assertion':assertion,'speaker':speaker,'paragraph_ids':pids,'primary_topic':topic,'topics':[topic],'modality':modality,'confidence':'high','qualifiers':''})
 rec={'source_id':sid,'snapshot_sha256':s['snapshot_sha256'],'language':s['language'],'claims':claims,'proposed_topics':[],'review_flags':[],'coverage_gaps':gaps[sid]}
 (records/(sid+'.json')).write_text(json.dumps(rec,ensure_ascii=False,indent=2)+'\n')
 print(sid,len(claims),sum(len((c['assertion']+' '+c['qualifiers']).split()) for c in claims))
