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
    ap.add_argument('--backend',choices=['auto','kinocut','hyperframes_ffmpeg','diffusionstudio','ffmpeg','dry-run'],default='auto')
    ap.add_argument('--source',type=Path)
    ap.add_argument('--clips-dir',type=Path)
    ap.add_argument('--audio-dir',type=Path)
    ap.add_argument('--dry-run',action='store_true')
    args=ap.parse_args(); w=args.workdir; w.mkdir(parents=True,exist_ok=True); args.output.parent.mkdir(parents=True,exist_ok=True)
    cmap_path=w/'contextual_coaching_map.json'
    if not cmap_path.exists(): raise ValueError(f'missing {cmap_path}')
    cmap=json.loads(cmap_path.read_text()); selected=cmap.get('selected_fights',[])
    if args.dry_run:
        backend='dry-run'
    elif args.backend in {'kinocut','hyperframes_ffmpeg','diffusionstudio'}:
        backend=args.backend
    else:  # auto
        backend='kinocut' if shutil.which('kino') else 'hyperframes_ffmpeg'
    scenes=[]
    for i,f in enumerate(selected,1):
        fid=f.get('fight_id',f'fight_{i:03d}')
        scenes.append({'scene_id':f'{fid}_source','kind':'source','source_start':f.get('source_start',f.get('start')),'source_end':f.get('source_end',f.get('end')),'must_precede':f'{fid}_review'})
        scenes.append({'scene_id':f'{fid}_review','kind':'review','review_start':f.get('review_start'),'question_first':True,'evidence_classes':['observed','inferred','unknown'],'source_fight_id':fid})
    manifest={'created_at':now(),'backend':backend,'workdir':str(w),'output':str(args.output),'scenes':scenes,'source':str(args.source or cmap.get('source',{}).get('path','')),'contract':{'action_before_review':True,'review_after_outcome':True,'no_vetoed_events':True}}
    (w/'scene_manifest.json').write_text(json.dumps(manifest,indent=2))
    if backend=='dry-run':
        print(json.dumps({'backend':backend,'scenes':len(scenes),'manifest':str(w/'scene_manifest.json')},indent=2)); return
    if backend=='ffmpeg':
        cmd=[sys.executable, str(Path(__file__).with_name('render_ffmpeg.py')), '--workdir', str(w), '--output', str(args.output)]
        if args.source: cmd += ['--source', str(args.source)]
        subprocess.run(cmd, check=True)
        return
    if backend=='diffusionstudio':
        proj=w/'render'/'diffusion_project'; proj.mkdir(parents=True,exist_ok=True)
        src=str(args.source or cmap.get('source',{}).get('path','')); fps=30
        def _fr(t): return int(round(float(t)*fps))
        fights=[{'id':f.get('fight_id','fight'),
                 'start':float(f.get('source_start',f.get('start',0))),
                 'end':float(f.get('source_end',f.get('end',0))),
                 'review_start':float(f.get('review_start',f.get('source_end',f.get('end',0)))),
                 'question':f.get('question') or 'What was the decision point here?',
                 'reveal':f.get('reveal') or f.get('outcome') or ''}
                for f in selected]
        scene_blocks=''.join(
            f"\n      <scene name={f['id']!r} width={{1920}} height={{1080}} fill=\"black\" active>"
            f"\n        <video src={src!r} start={{{_fr(f['start'])}}} end={{{_fr(f['end'])}}} width={{1920}} height={{1080}} />"
            f"\n        <text width={{1920}} height={{1080}} textAlign=\"center\" textBaseline=\"middle\" fontSize={{72}} color=\"#FFFFFF\" start={{{_fr(f['review_start'])}}} end={{{_fr(f['end'])}}}>"
            f"\n          {f['question']} — {f['reveal']}\n        </text>\n      </scene>" for f in fights)
        jsx=(f"import {{ For }} from \"solid-js\";\n"
             f"import {{ generate }} from \"@diffusionstudio/jsx\";\n\n"
             f"const SOURCE = {src!r};\nconst FPS = {fps};\n\n"
             f"const FIGHTS = {json.dumps(fights, indent=2)};\n\n"
             f"export default function Project() {{\n  return (\n    <stage camera={{[1,0,0,1,0,0]}}>{scene_blocks}\n    </stage>\n  );\n}}\n")
        (proj/'index.jsx').write_text(jsx)
        print(json.dumps({'backend':'diffusionstudio','project':str(proj/'index.jsx'),'fights':len(fights),'status':'jsx_project_ready_for_dapi'},indent=2)); return
    if backend=='kinocut':
        raise SystemExit('Kinocut was detected but automatic project-specific invocation is not configured; use the documented adapter and rerun with --backend hyperframes_ffmpeg after verification.')
    # The generic repository adapter intentionally stops after writing the contract manifest.
    # A deployment-specific HyperFrames/FFmpeg renderer should consume scene_manifest.json.
    print(json.dumps({'backend':backend,'scenes':len(scenes),'manifest':str(w/'scene_manifest.json'),'status':'manifest_ready_for_renderer'},indent=2))
if __name__=='__main__':
    try: main()
    except (OSError,ValueError,json.JSONDecodeError) as e: print('INVALID:',e,file=sys.stderr); raise SystemExit(1)
