#!/usr/bin/env python3
"""Small persistent-worker shell for the staged gameplay coaching pipeline.

The worker intentionally does not invent a model provider or publish output. It
records run state and leaves the stage adapters explicit for deployment-specific
integration.
"""
import argparse, json, os, shutil, subprocess, sys
from datetime import datetime, timezone
from pathlib import Path

def now(): return datetime.now(timezone.utc).isoformat()
def write(p,data): p.parent.mkdir(parents=True,exist_ok=True); p.write_text(json.dumps(data,indent=2))

def main():
    ap=argparse.ArgumentParser()
    ap.add_argument('--source',required=True)
    ap.add_argument('--goal',required=True,help='JSON goal record or questionnaire answers')
    ap.add_argument('--run-id',required=True)
    ap.add_argument('--runs-root',default='/data/runs')
    ap.add_argument('--config',default='/app/configs/default.yaml')
    ap.add_argument('--stage',choices=['prepare','validate-only'],default='prepare')
    args=ap.parse_args()
    source=Path(args.source); goal=Path(args.goal); root=Path(args.runs_root)/args.run_id
    if not source.exists(): raise SystemExit(f'missing source: {source}')
    if not goal.exists(): raise SystemExit(f'missing goal: {goal}')
    root.mkdir(parents=True,exist_ok=True)
    state={'run_id':args.run_id,'status':'queued','created_at':now(),'source':str(source),'goal':str(goal),'config':args.config,'backend':'not_selected','artifacts':{}}
    write(root/'run_manifest.json',state)
    if args.stage=='validate-only':
        state['status']='validated_inputs'; state['completed_at']=now(); write(root/'run_manifest.json',state); print(json.dumps(state,indent=2)); return
    # Preparation is safe and deterministic. Model-specific stages are explicit next steps.
    state['status']='prepared'; state['prepared_at']=now(); state['artifacts']['source_manifest']=str(root/'source_manifest.json'); state['artifacts']['goal_record']=str(root/'goal_record.json')
    shutil.copy2(goal,root/'goal_record.json')
    cmd=[sys.executable,'/app/scripts/inspect_source.py',str(source)]
    try:
        r=subprocess.run(cmd,check=True,capture_output=True,text=True)
        (root/'source_manifest.json').write_text(r.stdout)
    except Exception as exc:
        state['status']='failed'; state['error']=f'source inspection failed: {exc}'; write(root/'run_manifest.json',state); raise
    state['status']='ready_for_analysis'; state['updated_at']=now(); write(root/'run_manifest.json',state); print(json.dumps(state,indent=2))
if __name__=='__main__': main()
