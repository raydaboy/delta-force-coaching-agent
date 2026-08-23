#!/usr/bin/env python3
import argparse, json, shutil, subprocess, sys
from datetime import datetime, timezone
from pathlib import Path

def now(): return datetime.now(timezone.utc).isoformat()
def run(cmd): return subprocess.run(cmd,check=True,text=True,capture_output=True)

def main():
    ap=argparse.ArgumentParser(description='Prepare or render an episode from a coaching map.')
    ap.add_argument('--workdir',type=Path,required=True)
    ap.add_argument('--output',type=Path,required=True)
    ap.add_argument('--backend',choices=['auto','kinocut','hyperframes_ffmpeg','dry-run'],default='auto')
    ap.add_argument('--source',type=Path)
    ap.add_argument('--clips-dir',type=Path)
    ap.add_argument('--audio-dir',type=Path)
    ap.add_argument('--dry-run',action='store_true')
    args=ap.parse_args(); w=args.workdir; w.mkdir(parents=True,exist_ok=True); args.output.parent.mkdir(parents=True,exist_ok=True)
    cmap_path=w/'contextual_coaching_map.json'
    if not cmap_path.exists(): raise ValueError(f'missing {cmap_path}')
    cmap=json.loads(cmap_path.read_text()); selected=cmap.get('selected_fights',[])
    backend='dry-run' if args.dry_run or args.backend=='dry-run' else None
    if backend is None and args.backend in {'auto','kinocut'} and shutil.which('kino'):
        backend='kinocut'
    if backend is None: backend='hyperframes_ffmpeg'
    scenes=[]
    for i,f in enumerate(selected,1):
        fid=f.get('fight_id',f'fight_{i:03d}')
        scenes.append({'scene_id':f'{fid}_source','kind':'source','source_start':f.get('source_start',f.get('start')),'source_end':f.get('source_end',f.get('end')),'must_precede':f'{fid}_review'})
        scenes.append({'scene_id':f'{fid}_review','kind':'review','review_start':f.get('review_start'),'question_first':True,'evidence_classes':['observed','inferred','unknown'],'source_fight_id':fid})
    manifest={'created_at':now(),'backend':backend,'workdir':str(w),'output':str(args.output),'scenes':scenes,'source':str(args.source or cmap.get('source',{}).get('path','')),'contract':{'action_before_review':True,'review_after_outcome':True,'no_vetoed_events':True}}
    (w/'scene_manifest.json').write_text(json.dumps(manifest,indent=2))
    if backend=='dry-run': print(json.dumps({'backend':backend,'scenes':len(scenes),'manifest':str(w/'scene_manifest.json')},indent=2)); return
    if backend=='kinocut':
        raise SystemExit('Kinocut was detected but automatic project-specific invocation is not configured; use the documented adapter and rerun with --backend hyperframes_ffmpeg after verification.')
    # The generic repository adapter intentionally stops after writing the contract manifest.
    # A deployment-specific HyperFrames/FFmpeg renderer should consume scene_manifest.json.
    print(json.dumps({'backend':backend,'scenes':len(scenes),'manifest':str(w/'scene_manifest.json'),'status':'manifest_ready_for_renderer'},indent=2))
if __name__=='__main__':
    try: main()
    except (OSError,ValueError,json.JSONDecodeError) as e: print('INVALID:',e,file=sys.stderr); raise SystemExit(1)
