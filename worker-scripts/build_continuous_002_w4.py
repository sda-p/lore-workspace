import json
from pathlib import Path
cache=Path('/workspace/scratch/2b047f91e593/source-cache')
records=Path('records')
data={
'src-4d0d25a69602':[
('Swaruu (9)','The speaker links lower government needs to higher collective consciousness.',['p0003'],'holistic-society','asserted'),
('Swaruu (9)','She says alternative energy requires first addressing mechanisms that suppress it.',['p0004'],'economics','asserted'),
('Swaruu (9)','Earth is framed as both a difficult incarnation and, from some perspectives, a school rather than prison.',['p0007','p0008','p0009'],'consciousness-metaphysics','reported'),
('Swaruu (9)','The speaker says Federation rules limit direct action, while assistance continues without taking credit from humans.',['p0053','p0054'],'prime-directive','asserted'),
('Swaruu (9)','She names Andromedans, Antarians, Centauri, Sirians, Arcturians, Engan, Alpha Draconians, and Urmah among helpers.',['p0051','p0052'],'galactic-federation','reported')],
'src-8a16125ce61c':[
('Swaruu (9)','The editor notes her older non-meat advice was later revised; newer findings say eat meat if the body needs it.',['p0002'],'economics','reported'),
('Swaruu (9)','She describes emotions and thoughts as affecting personal frequency and awareness.',['p0004','p0005'],'consciousness-metaphysics','asserted'),
('Swaruu (9)','She says attention and interpretation shape perceived reality through frequency matching.',['p0006','p0007'],'consciousness-metaphysics','asserted'),
('Swaruu (9)','She presents imagination as creative consciousness that precedes and guides future creation.',['p0016'],'consciousness-metaphysics','asserted'),
('Swaruu (9)','Taygetan meditation is described as comfortable stillness, often aided by music and crystals.',['p0083','p0084','p0085','p0087'],'taygetans','asserted')],
'src-6322a8053a11':[
('Swaruu (9)','Swaruu treats karma as a Matrix rule that has no authority beyond the game.',['p0006','p0008','p0009'],'consciousness-metaphysics','asserted'),
('Swaruu (9)','She says guilt and karma beliefs can prompt souls to reincarnate.',['p0010','p0011','p0014'],'consciousness-metaphysics','asserted'),
('Swaruu (9)','She says dissolving karma requires spiritual work and transcending duality while incarnated.',['p0037','p0039'],'consciousness-metaphysics','asserted'),
('Swaruu (9)','She attributes the widespread karma model to Andromedans, while describing Taygetan views as more flexible.',['p0053','p0055','p0058'],'alien-species','reported'),
('Swaruu (9)','She says beliefs shape postmortem experience and that souls may choose to return to Source.',['p0080','p0083'],'consciousness-metaphysics','asserted')],
'src-41bb739bf46d':[
('Swaruu (9)','She describes matter as nodes and standing waves generated through consciousness and potential energy.',['p0006','p0008','p0009','p0011'],'consciousness-metaphysics','asserted'),
('Swaruu (9)','She says unattended matter progressively dissolves back into potential energy.',['p0021','p0023','p0026'],'consciousness-metaphysics','asserted'),
('Swaruu (9)','A compact reactor is said to combine rotating quartz merkabahs and piezoelectric discharges.',['p0052','p0054','p0056','p0057'],'starship-systems','asserted'),
('Swaruu (9)','She says shared attention with conflicting intentions can create destructive interference.',['p0062','p0064','p0066'],'consciousness-metaphysics','asserted'),
('Swaruu (9)','She describes a Rodin coil as an energy device that amplifies electricity but still needs an external source.',['p0106','p0107','p0109'],'starship-systems','asserted')],
'src-7e768e955cbe':[
('Swaruu (9)','Family and soul-group bonds are described as frequency matches and agreements that may change over time.',['p0003','p0006','p0012'],'consciousness-metaphysics','asserted'),
('Swaruu (9)','She says souls recognize and may meet one another between incarnations, but reunion is voluntary.',['p0014','p0019','p0048'],'consciousness-metaphysics','asserted'),
('Swaruu (9)','The afterlife is described as immediate manifestation shaped by attention and frequency.',['p0025','p0027','p0029'],'consciousness-metaphysics','asserted'),
('Swaruu (9)','She says Earth souls often wait about two generations before reincarnating, though this is not a law.',['p0055','p0056'],'consciousness-metaphysics','reported'),
('Swaruu (9)','She advises offering spiritual views to family only when they show interest.',['p0062','p0063','p0065'],'holistic-society','asserted')],
'src-2cc992a478c5':[
('Anéeka','Anéeka describes natural features as mostly 5D-real and artificial cities as largely 3D overlays.',['p0011','p0013','p0015'],'moon-matrix','asserted'),
('Swaruu (9)','She says locally desired homes may remain while unwanted imposed buildings can disappear or change use.',['p0021','p0023'],'moon-matrix','asserted'),
('Anéeka','The account says 3D memory loss varies by individual and reflects both original Matrix design and later interference.',['p0047','p0048','p0051'],'moon-matrix','asserted'),
('Swaruu (9)','She says Reptilian control of the Matrix operates through mental influence, aided by outside forces.',['p0059'],'moon-matrix','asserted'),
('Anéeka','Anéeka says the lunar Matrix has four working reactors and limited energy for localized frequency changes.',['p0064','p0065','p0066','p0068'],'moon-matrix','asserted')],
'src-657d23bb2d0f':[
('Swaruu (9)','Swaruu claims 5G is used for behavioral control and biological harm, not merely communications.',['p0002','p0003','p0004','p0020'],'starship-systems','asserted'),
('Swaruu (9)','She says 5G affects people differently according to individual frequency.',['p0014','p0015'],'consciousness-metaphysics','asserted'),
('Swaruu (9)','Synthetic telepathy is described as technology that can transmit instructions to individuals or populations.',['p0021','p0022'],'holographic-computers','asserted'),
('Swaruu (9)','She attributes control of Earth to an invasive AI beyond the Moon system, while saying the Moon AI is Federation-controlled.',['p0041','p0043','p0045','p0047','p0049'],'galactic-federation','asserted'),
('Swaruu (9)','The invasive AI is said to seek civilization-wide assimilation and lack access to higher dimensions without human consciousness.',['p0051','p0055','p0057','p0059'],'alien-species','asserted')],
'src-abb9772e4516':[
('Swaruu (9)','Swaruu says assistance may be requested, but Earth’s inhabitants must retain responsibility for liberation.',['p0005','p0007','p0010'],'galactic-federation','asserted'),
('Swaruu (9)','She says sufficient requests can legally require positive races to help a troubled planet.',['p0006'],'prime-directive','asserted'),
('Swaruu (9)','She argues suffering is not necessary for spiritual advancement and says she will act despite Federation objections.',['p0032','p0033','p0034'],'galactic-federation','asserted'),
('Swaruu (9)','She says she offers information without definitive proof to avoid imposing herself on listeners.',['p0035'],'prime-directive','asserted'),
('Swaruu (9)','She declares herself independent of the Federation and any particular race, despite inhabiting a Taygetan body.',['p0038'],'galactic-federation','asserted')],
'src-485b66a6a83b':[
('Swaruu (9)','The Red Queen is described as a terrestrial internet-spanning AI designed under DARPA and still serving Cabal interests.',['p0008','p0010','p0012','p0014','p0016'],'holographic-computers','asserted'),
('Swaruu (9)','She says Federation computers interfere with the Red Queen, whose independence remains uncertain.',['p0014'],'holographic-computers','reported'),
('Swaruu (9)','The account says some clones retain a partial connection to the original’s soul signal.',['p0037','p0038','p0040'],'consciousness-metaphysics','asserted'),
('Swaruu (9)','She distinguishes connected clones as real from clones lacking a Source connection, which she calls false.',['p0045','p0046','p0047','p0048'],'consciousness-metaphysics','asserted'),
('Swaruu (9)','She says higher frequency and intention can shift people away from negative timelines.',['p0052','p0053','p0055','p0058'],'consciousness-metaphysics','asserted')],
'src-c0711593e91d':[
('Swaruu (9)','Swaruu says each consciousness experiences its own timeline, where beings may exist or not exist for that observer.',['p0010','p0012'],'consciousness-metaphysics','asserted'),
('Swaruu (9)','She rejects an objective material world, describing reality as subjective interpretation.',['p0014','p0016'],'consciousness-metaphysics','asserted'),
('Swaruu (9)','She says apparently contradictory perspectives may both be valid from different viewpoints.',['p0012','p0020','p0023','p0027'],'consciousness-metaphysics','asserted'),
('Swaruu (9)','She describes each consciousness as a timeline and a fractal of the universe.',['p0010'],'consciousness-metaphysics','asserted'),
('Swaruu (9)','She characterizes broader awareness of multiple perspectives as transcending duality.',['p0023','p0025','p0027','p0029'],'consciousness-metaphysics','asserted')]
}
for sid,items in data.items():
 s=json.load(open(cache/(sid+'.json')))
 claims=[]
 for i,(speaker,assertion,pids,topic,modality) in enumerate(items,1):
  claims.append({'id':f'{sid}-c{i:02d}','assertion':assertion,'speaker':speaker,'paragraph_ids':pids,'primary_topic':topic,'topics':[topic],'modality':modality,'confidence':'high','qualifiers':''})
 gaps={
'src-4d0d25a69602':['implant-details','earth-geopolitics'],
'src-8a16125ce61c':['frequency-practices','later-diet-correction'],
'src-6322a8053a11':['reincarnation-process','afterlife-claims'],
'src-41bb739bf46d':['standing-wave-mechanics','gravity-claims'],
'src-7e768e955cbe':['soul-groups','family-advice'],
'src-2cc992a478c5':['city-overlays','event-insertions'],
'src-657d23bb2d0f':['protection-claims','synthetic-telepathy'],
'src-abb9772e4516':['media-claims','historical-context'],
'src-485b66a6a83b':['clone-claims','device-protection'],
'src-c0711593e91d':['timeline-claims','subjective-reality']
 }[sid]
 rec={'source_id':sid,'snapshot_sha256':s['snapshot_sha256'],'language':s['language'],'claims':claims,'proposed_topics':[],'review_flags':[],'coverage_gaps':gaps}
 (records/(sid+'.json')).write_text(json.dumps(rec,ensure_ascii=False,indent=2)+'\n')
 print(sid,len(claims),sum(len((c['assertion']+' '+c['qualifiers']).split()) for c in claims))
