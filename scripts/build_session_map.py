#!/usr/bin/env python3
"""Build a teaching-ready session map without fabricating player strengths or mistakes."""
import argparse,json
from pathlib import Path

VALID_STATUS={'won','lost','escaped','injured_retreat','unresolved','unknown'}

def as_event(f,idx):
    fid=f.get('fight_id',f'fight_{idx:03d}')
    status=f.get('status',f.get('outcome','unresolved'))
    if status not in VALID_STATUS: status='unknown'
    evidence=[]
    for e in f.get('evidence',[]):
        kind=str(e.get('kind','frame')).lower()
        etype='audio' if 'audio' in kind or 'sound' in kind else 'hud' if any(x in kind for x in ('damage','kill','death')) else 'frame'
        evidence.append({'type':etype,'claim':f'Resolved evidence is recorded as {e.get("kind","frame")}; verify the exact frame or audio before teaching.'})
    if not evidence: evidence=[{'type':'frame','claim':'Boundary and outcome require direct source verification.'}]
    start=float(f.get('start',f.get('source_start',0)))
    end=float(f.get('end',f.get('source_end',start+0.1)))
    return {'fight_id':fid,'start':start,'end':end,'status':status,'outcome':f.get('outcome',status),'key_decisions':[{'decision_id':fid+'_decision_01','context_before':'Derive from the verified setup window; do not infer unseen information.','action_taken':'Describe the first controllable choice after direct source review.','consequence':'Describe the visible immediate effect and outcome.'}],'evidence':evidence,'unknowns':f.get('unknowns',['Enemy intent, off-screen teammates, and unseen geometry are not established.'])}

def make_priority(pid,rank,title,ids,why,alternative,drill_name,drill_condition):
    return {'priority_id':pid,'rank':rank,'title':title,'behavior_to_change':'Identify the earliest controllable decision from the cited fights; do not use the outcome alone as proof of error.','why_it_matters':why,'supporting_fights':ids,'observed_consequence':'The cited resolved events contain the relevant visible outcome or pressure; exact causal teaching requires source review.','alternative':alternative,'counterfactual':{'claim':'The alternative could preserve more options in the visible situation; it cannot guarantee a different outcome.','class':'inference','confidence':0.5,'unknowns':['Enemy aim, teammates, and unseen routes are unknown.']},'drill':{'name':drill_name,'success_condition':drill_condition}}

def main():
    ap=argparse.ArgumentParser(); ap.add_argument('--events',type=Path,required=True); ap.add_argument('--goal',type=Path,required=True); ap.add_argument('--profile',type=Path); ap.add_argument('--output',type=Path,required=True); args=ap.parse_args()
    resolved=json.loads(args.events.read_text()); goal=json.loads(args.goal.read_text()); profile=json.loads(args.profile.read_text()) if args.profile and args.profile.exists() else None
    source=dict(resolved.get('source',{})); source.setdefault('path',source.get('input',source.get('format',{}).get('filename',''))); duration_value=source.get('duration',source.get('duration_seconds',source.get('format',{}).get('duration',0))); source['duration']=float(duration_value or 0); source.setdefault('fps',0); source.setdefault('resolution',''); source.setdefault('game',''); source.setdefault('mode',''); source.setdefault('limitations',[])
    pg=goal.get('player_stated_goal',goal.get('player_goal',{})); primary=pg.get('primary_goal',pg.get('primary','user-defined goal')) if isinstance(pg,dict) else str(pg)
    fights=[as_event(f,i) for i,f in enumerate(resolved.get('fights',[]),1)]
    ids=[f['fight_id'] for f in fights]; losses=[f['fight_id'] for f in fights if f['status'] in {'lost','injured_retreat','escaped'}]; wins=[f['fight_id'] for f in fights if f['status']=='won']; clusters=[f['fight_id'] for f in fights if any(x in json.dumps(f).lower() for x in ('cluster','squad','multiple','group'))]
    evidence=[{'type':'metadata','claim':'Source metadata comes from the inspected manifest or resolver input.'}]
    for f in fights: evidence.extend({'type':e['type'],'claim':f['fight_id']+': '+e['claim']} for e in f['evidence'])
    strengths=[]
    if wins: strengths.append({'claim':f'{len(wins)} resolved fight(s) have a recorded win outcome; inspect the controllable advantage in each before calling it a strength.','class':'observed','confidence':0.9,'supporting_fights':wins})
    else: strengths.append({'claim':'No resolved win outcome was available in this input; do not invent a strength.','class':'unknown','confidence':0.9,'supporting_fights':[]})
    weaknesses=[]
    if losses: weaknesses.append({'claim':f'{len(losses)} resolved fight(s) have a loss, escape, or injured-retreat outcome; inspect the turning point rather than blaming the result.','class':'observed','confidence':0.9,'supporting_fights':losses})
    if clusters: weaknesses.append({'claim':f'{len(clusters)} resolved event(s) may contain connected pressure; verify whether each is one tactical cluster before splitting lessons.','class':'observed','confidence':0.7,'supporting_fights':clusters})
    if not weaknesses: weaknesses.append({'claim':'No resolved loss or retreat was available in this input; do not invent a weakness.','class':'unknown','confidence':0.9,'supporting_fights':[]})
    priorities=[]
    if losses: priorities.append(make_priority('priority_01',1,'Find the first lost option before the outcome',losses,'The goal is better decisions, not outcome blame.','Use the earliest verified reset, cover, range, or disengagement option and state its trade-off.','Exit-first review drill','In three relevant fights, call the first safe reset before taking the next exposure.'))
    if clusters and len(priorities)<3: priorities.append(make_priority('priority_02',len(priorities)+1,'Separate connected targets before teaching individual kills',clusters,'Group pressure is easier to understand as one episode when contact is continuous.','Use the visible choke, height, smoke, or angle that reduces how many targets can act at once.','One-target lane drill','After each down, change the angle before exposing to the next target.'))
    if len(priorities)<3: priorities.append(make_priority('priority_03',len(priorities)+1,'Protect the stated goal while solving forced danger',ids[:min(6,len(ids))],'Every lesson must test whether the choice protected the stated objective: '+str(primary)+'.','Compare the fight choice with the safest goal-preserving option visible in the frame.','Forced-or-optional call drill','Label each contact forced or optional before committing.'))
    objectives=[]
    for p in priorities[:3]: objectives.append({'objective_id':p['priority_id'].replace('priority','objective'),'rank':p['rank'],'title':p['title'],'opening_line':'We will use the cited source moments, not generic advice, to answer this.','question_for_player':'What is the earliest controllable choice visible before the outcome?','reveal':'Teaching-engine must identify observed facts, cautious inference, unknowns, trade-off, and measurable cue.','supporting_fights':p['supporting_fights'],'drill':p['drill']['name']})
    out={'source':source,'session_goal':primary,'goal_record_ref':str(args.goal),'player_profile_ref':str(args.profile) if args.profile else None,'events':resolved.get('events',[]),'fights':fights,'strengths':strengths,'weaknesses':weaknesses,'priorities':priorities,'learning_objectives':objectives,'teaching_engine_required':True,'teaching_instructions':['Do not copy priority wording into a final lesson without source review.','Use teaching-engine to fill local decision, what_helped, what_hurt, alternative, trade-off, cue, drill, and novelty.','Reject any alternative that could be pasted into another fight unchanged.'],'session_summary':'This map records resolved evidence and review priorities without pretending that generic templates are player-specific findings.','evidence_ledger':evidence,'unknowns':['Enemy intent, off-screen teammates, and guaranteed counterfactual outcomes are unknown unless directly established.']}
    args.output.parent.mkdir(parents=True,exist_ok=True); args.output.write_text(json.dumps(out,indent=2)); print(json.dumps({'output':str(args.output),'fights':len(fights),'priorities':len(priorities),'profile_loaded':bool(profile)},indent=2))
if __name__=='__main__': main()
