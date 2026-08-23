#!/usr/bin/env python3
import argparse, json, subprocess, sys
from pathlib import Path

def main():
    ap=argparse.ArgumentParser(description='Normalize an external candidate list into the repository inventory contract.')
    ap.add_argument('--source',type=Path,required=True,help='Source manifest JSON')
    ap.add_argument('--goal',type=Path,required=True,help='Goal record JSON')
    ap.add_argument('--candidates',type=Path,required=True,help='JSON list or object with events from a multimodal analyzer/manual pass')
    ap.add_argument('--output',type=Path,required=True)
    args=ap.parse_args(); source=json.loads(args.source.read_text()); goal=json.loads(args.goal.read_text()); raw=json.loads(args.candidates.read_text())
    events=raw.get('events',raw) if isinstance(raw,(list,dict)) else []
    if not isinstance(events,list): raise ValueError('candidates must be a list or an object with an events list')
    normalized=[]
    for i,e in enumerate(events,1):
        e=dict(e); e.setdefault('event_id',f'candidate_{i:04d}'); e.setdefault('start',0); e.setdefault('end',e['start']); e.setdefault('type_guess','unknown'); e.setdefault('summary',''); e.setdefault('evidence',[])
        if float(e['end']) < float(e['start']): raise ValueError(f'candidate {e["event_id"]} ends before it starts')
        normalized.append(e)
    out={'source':source,'player_goal':goal.get('player_stated_goal',goal.get('player_goal',{})),'events':sorted(normalized,key=lambda x:(float(x['start']),float(x['end']))),'ledger_notes':{'raw_candidates_are_not_fights':True,'resolver':'scripts/resolve_candidates.py'}}
    args.output.parent.mkdir(parents=True,exist_ok=True); args.output.write_text(json.dumps(out,indent=2)); print(json.dumps({'output':str(args.output),'events':len(normalized)},indent=2))
if __name__=='__main__':
    try: main()
    except (OSError,ValueError,json.JSONDecodeError) as e: print('INVALID:',e,file=sys.stderr); raise SystemExit(1)
