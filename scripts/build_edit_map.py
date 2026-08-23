#!/usr/bin/env python3
import argparse,json
from pathlib import Path

def main():
    ap=argparse.ArgumentParser(description='Export a pure-gameplay edit map from a contextual coaching map.')
    ap.add_argument('--map',dest='map_path',type=Path,required=True)
    ap.add_argument('--output',type=Path,required=True)
    ap.add_argument('--source-file',default=None)
    args=ap.parse_args(); m=json.loads(args.map_path.read_text())
    clips=[]
    for f in sorted(m.get('selected_fights',[]),key=lambda x:float(x.get('source_start',0))):
        clips.append({'label':f.get('fight_id','fight'),'kind':'combat','source_start':f.get('source_start'),'source_end':f.get('source_end'),'keep_complete':True,'outcome':f.get('outcome'),'goal_relation':f.get('goal_relation'),'lesson_category':f.get('lesson_category')})
    exclusions=m.get('omissions',m.get('selection_policy',{}).get('excluded_ranges',[]))
    out={'source_file':args.source_file or m.get('source',{}).get('path',''),'target_duration_seconds':sum(max(0,float(c['source_end'])-float(c['source_start'])) for c in clips),'clips':clips,'excluded_ranges':exclusions,'selection_policy':m.get('selection_policy',{})}
    args.output.parent.mkdir(parents=True,exist_ok=True); args.output.write_text(json.dumps(out,indent=2)); print(json.dumps({'output':str(args.output),'clips':len(clips),'target_duration_seconds':out['target_duration_seconds']},indent=2))
if __name__=='__main__': main()
