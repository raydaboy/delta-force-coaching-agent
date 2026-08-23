#!/usr/bin/env python3
import argparse, json, sys
from pathlib import Path

VETO={'loot','death_crate','inventory_screen','peek','angle_clear','movement','rotation','recovery','visual_peak','generic_audio_peak','body_seen','death','death_screen','menu','extraction','hacking','safe_hacking'}

def read(p):
    if not p.exists(): raise ValueError(f'missing artifact: {p}')
    return json.loads(p.read_text())

def main():
    ap=argparse.ArgumentParser(description='Validate gameplay coaching handoff artifacts.')
    ap.add_argument('--workdir',type=Path,required=True)
    ap.add_argument('--require-render',action='store_true')
    args=ap.parse_args(); w=args.workdir
    goal=read(w/'goal_record.json')
    if not goal.get('player_stated_goal') and not goal.get('player_goal'): raise ValueError('goal record has no player goal')
    raw=read(w/'raw_candidate_inventory.json'); resolved=read(w/'resolved_event_map.json')
    events=resolved.get('events',[]); fights=resolved.get('fights',[])
    if not events: raise ValueError('resolved event map has no events')
    ids=set()
    for f in fights:
        fid=f.get('fight_id');
        if not fid or fid in ids: raise ValueError(f'duplicate/missing fight id: {fid}')
        ids.add(fid)
        if not float(f.get('start',0)) < float(f.get('end',0)): raise ValueError(f'bad fight bounds: {fid}')
        if f.get('status') not in {'won','lost','escaped','injured_retreat','unresolved','unknown'}: raise ValueError(f'bad status: {fid}')
    promoted_bad=[]
    for e in events:
        if e.get('resolved_label')=='fight' and (str(e.get('normalized_type','')) in VETO or set(e.get('evidence_channels',[])) & VETO): promoted_bad.append(e.get('event_id'))
    if promoted_bad: raise ValueError('vetoed candidates promoted as fights: '+','.join(map(str,promoted_bad)))
    coaching=w/'contextual_coaching_map.json'
    selected=[]
    if coaching.exists():
        selected=read(coaching).get('selected_fights',[])
        for f in selected:
            if f.get('fight_id') not in ids and not f.get('fight_id','').startswith('fight_'): raise ValueError(f'selected fight not in resolver: {f.get("fight_id")}')
            if 'review_start' in f and float(f['review_start']) < float(f.get('outcome_time',0)) + 0.3 - 1e-6: raise ValueError(f'review starts before outcome: {f.get("fight_id")}')
            if not float(f.get('source_start',0)) < float(f.get('source_end',0)): raise ValueError(f'bad selected bounds: {f.get("fight_id")}')
    if args.require_render:
        mp4s=list((w/'dist').glob('*.mp4')) if (w/'dist').exists() else []
        if not mp4s: raise ValueError('require-render requested but no MP4 found under workdir/dist')
        for name in ['final_qc_report.json','technical_qc.json','temporal_context_qc.json','coaching_usefulness_qc.json','session_memory_qc.json','audio_pacing_qc.json']:
            if not (w/'qc'/name).exists(): raise ValueError(f'missing QC receipt: {w/"qc"/name}')
    print(json.dumps({'valid':True,'raw_candidates':len(raw.get('events',[])),'resolved_fights':len(fights),'selected_fights':len(selected),'require_render':args.require_render},indent=2))
if __name__=='__main__':
    try: main()
    except (OSError,ValueError,json.JSONDecodeError) as exc:
        print('INVALID:',exc,file=sys.stderr); raise SystemExit(1)
