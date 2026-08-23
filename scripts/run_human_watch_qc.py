#!/usr/bin/env python3
import argparse, json, sys
from datetime import datetime, timezone
from pathlib import Path

def main():
    ap=argparse.ArgumentParser(description='Create human-watch QC review contracts for a rendered MP4.')
    ap.add_argument('--video',type=Path,required=True)
    ap.add_argument('--map',type=Path,required=True)
    ap.add_argument('--output',type=Path,required=True)
    ap.add_argument('--results',type=Path,help='Optional JSON file containing completed role results')
    args=ap.parse_args()
    if not args.video.exists(): raise ValueError(f'missing video: {args.video}')
    if not args.map.exists(): raise ValueError(f'missing coaching map: {args.map}')
    args.output.mkdir(parents=True,exist_ok=True)
    roles=['temporal_context','coaching_usefulness','session_memory','audio_pacing']
    supplied=json.loads(args.results.read_text()) if args.results else {}
    for role in roles:
        result=supplied.get(role,{'status':'pending_human_review','blocking_findings':[],'major_findings':[],'minor_findings':[],'timestamps':[],'corrections':[],'reviewed_video':str(args.video)})
        result.update({'role':role,'video':str(args.video),'created_at':datetime.now(timezone.utc).isoformat(),'must_review_rendered_mp4':True})
        (args.output/(role+'_qc.json')).write_text(json.dumps(result,indent=2))
    summary={'status':'pending_human_review' if not args.results else 'submitted_for_adjudication','video':str(args.video),'roles':roles,'release_gate':'block on any blocker or major; do not average findings'}
    (args.output/'final_qc_report.json').write_text(json.dumps(summary,indent=2)); print(json.dumps(summary,indent=2))
if __name__=='__main__':
    try: main()
    except (OSError,ValueError,json.JSONDecodeError) as e: print('INVALID:',e,file=sys.stderr); raise SystemExit(1)
