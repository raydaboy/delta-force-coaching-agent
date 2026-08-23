#!/usr/bin/env python3
"""Validate evidence-backed teaching lessons or a lesson list."""
import argparse,json,sys
from pathlib import Path
GENERIC_PHRASES=[
 'use the nearest hard cover, shorten the enemy view, and keep a route toward extraction',
 'tie your movement and aim to the next safe piece of cover',
 'use cover and reset',
]
REQUIRED={'lesson_id','source_fight_id','lesson_type','novelty_label','decision_point','observed','inferred','unknown','what_helped','what_hurt','realistic_alternative','next_game_cue','drill'}

def validate(data):
    lessons=data.get('lessons') if isinstance(data,dict) and 'lessons' in data else [data]
    errors=[]; warnings=[]; seen={}
    if not isinstance(lessons,list) or not lessons: return ['lessons must be a non-empty list'],[]
    for i,l in enumerate(lessons):
        p=f'lessons[{i}]'
        if not isinstance(l,dict): errors.append(p+' must be an object'); continue
        missing=REQUIRED-set(l)
        if missing: errors.append(p+' missing '+','.join(sorted(missing))); continue
        for key in ('observed','inferred','unknown'):
            if not isinstance(l[key],list): errors.append(f'{p}.{key} must be a list')
        dp=l['decision_point']
        if not isinstance(dp,dict) or not isinstance(dp.get('source_time'),(int,float)) or not dp.get('description') or not isinstance(dp.get('evidence_refs'),list) or not dp['evidence_refs']:
            errors.append(p+'.decision_point needs source_time, description, and evidence_refs')
        alt=l['realistic_alternative']
        if not isinstance(alt,dict) or not all(alt.get(k) for k in ('action','tradeoff','likely_benefit')) or not isinstance(alt.get('unknowns'),list): errors.append(p+'.realistic_alternative is incomplete')
        drill=l['drill']
        if not isinstance(drill,dict) or not all(drill.get(k) for k in ('name','trigger','action','success_condition','scope')): errors.append(p+'.drill needs name, trigger, action, success_condition, scope')
        blob=json.dumps(l).lower()
        for phrase in GENERIC_PHRASES:
            if phrase in blob: errors.append(p+' contains rejected generic teaching phrase')
        if l['novelty_label'] not in {'new_lesson','progression','repeated_mistake','different_version','model_success','no_review'}: errors.append(p+'.novelty_label unsupported')
        if l['novelty_label'] in {'progression','repeated_mistake','different_version'} and not l.get('progression_note'): warnings.append(p+' should include progression_note for a non-new lesson')
        cue=l['next_game_cue'].strip().lower(); seen.setdefault(cue,[]).append(l['lesson_id'])
        for forbidden in ('guaranteed','definitely win','would have won','enemy intended'):
            if forbidden in blob: errors.append(p+' uses unsupported certainty: '+forbidden)
    for cue,ids in seen.items():
        if len(ids)>1: errors.append('duplicate next_game_cue across '+','.join(ids))
    return errors,warnings

def main():
    ap=argparse.ArgumentParser(); ap.add_argument('input',type=Path); args=ap.parse_args()
    try: data=json.loads(args.input.read_text()); errors,warnings=validate(data)
    except Exception as e: print(json.dumps({'valid':False,'errors':[str(e)],'warnings':[]})); return 1
    print(json.dumps({'valid':not errors,'errors':errors,'warnings':warnings},indent=2)); return 1 if errors else 0
if __name__=='__main__': raise SystemExit(main())
