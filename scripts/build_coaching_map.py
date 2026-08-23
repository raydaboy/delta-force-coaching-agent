#!/usr/bin/env python3
"""Select a diverse, goal-relevant coaching set without treating raw combat count as value."""
import argparse,json
from pathlib import Path

def score(f):
    status=str(f.get('status',f.get('outcome',''))).lower(); text=json.dumps(f).lower(); value=0
    if status in {'lost','injured_retreat','escaped'}: value+=12
    if status=='won': value+=4
    if any(x in text for x in ('loot','extraction','forced','threat')): value+=8
    if any(x in text for x in ('cluster','squad','multiple','group')): value+=7
    if any(x in text for x in ('death','ambush','damage','retreat')): value+=5
    if any(x in text for x in ('optional','routine','ai')): value-=3
    return value

def label(f,prior_labels):
    text=json.dumps(f).lower()
    if f.get('status')=='won' and any(x in text for x in ('cluster','squad')): return 'model_success'
    if f.get('status') in {'lost','injured_retreat'} and prior_labels.get('loss'): return 'repeated_mistake'
    if any(x in text for x in ('loot','extraction')): return 'goal_tradeoff'
    if any(x in text for x in ('cluster','squad','multiple')): return 'different_version'
    return 'new_lesson'

def depth(f):
    text=json.dumps(f).lower(); status=f.get('status',f.get('outcome',''))
    if status in {'lost','injured_retreat','escaped'} or any(x in text for x in ('loot','extraction','cluster','squad','ambush')): return 'deep'
    return 'standard'

def main():
    ap=argparse.ArgumentParser(); ap.add_argument('--session',type=Path,required=True); ap.add_argument('--output',type=Path,required=True); ap.add_argument('--max-fights',type=int,default=15); args=ap.parse_args(); s=json.loads(args.session.read_text()); fights=s.get('fights',[])
    ranked=sorted(fights,key=lambda f:(-score(f),float(f.get('start',0)))); chosen=[]; categories=set(); prior={'loss':False}
    # First pass: maximize lesson diversity while preserving high-leverage events.
    for f in ranked:
        if len(chosen)>=max(1,args.max_fights): break
        t=json.dumps(f).lower(); cat='loss' if f.get('status') in {'lost','injured_retreat','escaped'} else 'cluster' if any(x in t for x in ('cluster','squad','multiple','group')) else 'goal' if any(x in t for x in ('loot','extraction','forced','threat')) else 'win' if f.get('status')=='won' else 'other'
        if cat in categories and cat in {'win','other'}: continue
        f=dict(f); f['selection_score']=score(f); f['novelty_label']=label(f,prior); f['review_depth']=depth(f); f['selection_reason']='goal relevance, outcome leverage, connected-cluster value, or distinct success'; chosen.append(f); categories.add(cat); prior['loss']=prior['loss'] or cat=='loss'
    # Second pass: fill remaining slots by score, but never duplicate exact fight IDs.
    for f in ranked:
        if len(chosen)>=max(1,args.max_fights): break
        if any(x.get('fight_id')==f.get('fight_id') for x in chosen): continue
        f=dict(f); f['selection_score']=score(f); f['novelty_label']=label(f,prior); f['review_depth']=depth(f); f['selection_reason']='highest remaining scored event'; chosen.append(f)
    chosen=sorted(chosen,key=lambda f:float(f.get('start',f.get('source_start',0))))
    omitted=[f.get('fight_id') for f in fights if not any(x.get('fight_id')==f.get('fight_id') for x in chosen)]
    out={'source':s.get('source',{}),'player_goal':s.get('session_goal',{}),'selected_fights':chosen,'selection_policy':{'max_fights':args.max_fights,'score':'loss/escape and goal-related risk first, then connected clusters, distinct wins, and remaining scored events','diversity_rule':'do not fill the set with routine isolated wins or same-category events when a stronger distinct lesson is available','review_start_rule':'outcome_time + 0.3 seconds when outcome_time is available'},'omitted_fights':omitted,'teaching_note':'Selection is not teaching. Every selected fight must pass teaching-engine lesson validation before narration.'}
    args.output.parent.mkdir(parents=True,exist_ok=True); args.output.write_text(json.dumps(out,indent=2)); print(json.dumps({'selected':len(chosen),'omitted':len(omitted),'categories':sorted(categories)},indent=2))
if __name__=='__main__': main()
