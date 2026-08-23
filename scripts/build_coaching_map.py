#!/usr/bin/env python3
import argparse, json
from pathlib import Path

def main():
    ap=argparse.ArgumentParser(description='Select goal-relevant complete engagements for a focused coaching edit.')
    ap.add_argument('--session',type=Path,required=True)
    ap.add_argument('--output',type=Path,required=True)
    ap.add_argument('--max-fights',type=int,default=15)
    args=ap.parse_args(); s=json.loads(args.session.read_text())
    fights=s.get('fights',[])
    def score(f):
        status=f.get('status',f.get('outcome',''))
        text=(json.dumps(f)).lower()
        value=0
        if status in {'lost','injured_retreat','escaped'}: value+=8
        if 'cluster' in text or 'squad' in text or 'sustained' in text: value+=5
        if 'loot' in text or 'extraction' in text or 'retreat' in text: value+=5
        if status=='won': value+=2
        return value
    ranked=sorted(fights,key=lambda f:(-score(f),float(f.get('start',0))))[:max(1,args.max_fights)]
    chosen=sorted(ranked,key=lambda f:float(f.get('start',0)))
    out={'source':s.get('source',{}),'player_goal':s.get('session_goal',{}),'selected_fights':chosen,'selection_policy':{'max_fights':args.max_fights,'score':'loss/escape and goal-related risk first, then clusters and distinct wins','review_start_rule':'outcome_time + 0.3 seconds when outcome_time is available'},'omitted_fights':[f.get('fight_id') for f in fights if f not in chosen]}
    args.output.parent.mkdir(parents=True,exist_ok=True); args.output.write_text(json.dumps(out,indent=2)); print(json.dumps({'selected':len(chosen),'omitted':len(out['omitted_fights'])},indent=2))
if __name__=='__main__': main()
