#!/usr/bin/env python3
"""Run the repository pipeline against a real recording without committing the media."""
from __future__ import annotations
import argparse,json,shutil,subprocess,sys
from pathlib import Path

def run(cmd):
    print('+',' '.join(map(str,cmd)))
    subprocess.run([str(x) for x in cmd],check=True)

def main():
    ap=argparse.ArgumentParser(description='Run a real-recording end-to-end simulation.'); ap.add_argument('--source',type=Path,required=True); ap.add_argument('--goal',type=Path,required=True); ap.add_argument('--profile',type=Path,required=True); ap.add_argument('--candidates',type=Path,required=True); ap.add_argument('--verified-coaching-map',type=Path,help='Optional analyst-enriched map with complete boundaries and goal relations.'); ap.add_argument('--workdir',type=Path,required=True); ap.add_argument('--repo',type=Path,default=Path(__file__).resolve().parents[1]); ap.add_argument('--render-backend',choices=['dry-run','auto'],default='dry-run'); args=ap.parse_args()
    for p in (args.source,args.goal,args.profile,args.candidates):
        if not p.exists(): raise SystemExit(f'missing input: {p}')
    w=args.workdir; a=w/'artifacts'; w.mkdir(parents=True,exist_ok=True); a.mkdir(exist_ok=True); (w/'input').mkdir(exist_ok=True); (w/'render').mkdir(exist_ok=True); (w/'qc').mkdir(exist_ok=True)
    source_link=w/'input'/'source.mp4';
    if source_link.exists() or source_link.is_symlink(): source_link.unlink()
    source_link.symlink_to(args.source.resolve())
    shutil.copy2(args.goal,a/'goal_record.json'); shutil.copy2(args.profile,a/'player_profile.json'); shutil.copy2(args.candidates,a/'candidate_events.json')
    repo=args.repo
    run([sys.executable,repo/'scripts/inspect_source.py',source_link,'--json-out',a/'source_manifest.json'])
    run([sys.executable,repo/'scripts/build_candidate_inventory.py','--source',a/'source_manifest.json','--goal',a/'goal_record.json','--candidates',a/'candidate_events.json','--output',a/'raw_candidate_inventory.json'])
    run([sys.executable,repo/'scripts/resolve_candidates.py',a/'raw_candidate_inventory.json','--output',a/'resolved_event_map.json'])
    run([sys.executable,repo/'scripts/build_session_map.py','--events',a/'resolved_event_map.json','--goal',a/'goal_record.json','--profile',a/'player_profile.json','--output',a/'session_map.json'])
    if args.verified_coaching_map:
        shutil.copy2(args.verified_coaching_map,a/'contextual_coaching_map.json'); coaching_backend='analyst-enriched handoff supplied'
    else:
        run([sys.executable,repo/'scripts/build_coaching_map.py','--session',a/'session_map.json','--output',a/'contextual_coaching_map.json','--max-fights','15']); coaching_backend='deterministic selector; analyst enrichment still required before teaching'
    # The teaching contract intentionally fails closed when no analyst-enriched decision times exist.
    run([sys.executable,repo/'scripts/build_teaching_ledger.py','--map',a/'contextual_coaching_map.json','--output',a/'teaching_lessons.json'])
    run([sys.executable,repo/'scripts/validate_session_map.py',a/'session_map.json'])
    run([sys.executable,repo/'scripts/validate_teaching.py',a/'teaching_lessons.json'])
    shutil.copy2(a/'contextual_coaching_map.json',w/'contextual_coaching_map.json')
    run([sys.executable,repo/'scripts/render_episode.py','--workdir',w,'--source',source_link,'--output',w/'render'/'scene_manifest.json','--backend',args.render_backend,'--dry-run'])
    shutil.copy2(w/'scene_manifest.json',w/'render'/'scene_manifest.json')
    report={'source':str(args.source.resolve()),'workdir':str(w.resolve()),'stages':{'source_inspection':'passed','candidate_normalization':'passed','context_resolution':'passed','session_map':'passed','coaching_map':coaching_backend,'teaching_ledger':'passed','render_handoff':'dry-run manifest only','media_render':'not performed by generic adapter','human_watch_qc':'not performed by generic adapter'},'truthfulness_note':'This simulation uses the real recording and real evidence artifacts. The repository does not claim that a multimodal analyzer, speech renderer, or human viewer ran unless their output is supplied.'}
    (w/'simulation_report.json').write_text(json.dumps(report,indent=2)); print(json.dumps(report,indent=2))
if __name__=='__main__':
    try: main()
    except subprocess.CalledProcessError as e: raise SystemExit(e.returncode)
