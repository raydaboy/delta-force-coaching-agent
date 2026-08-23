#!/usr/bin/env python3
import argparse, json
from pathlib import Path
from datetime import datetime, timezone

QUESTIONS = {
    'primary_goal': 'What is the primary goal? ',
    'secondary_goals': 'List secondary goals separated by commas: ',
    'engagement_policy': 'When should the coach treat a fight as necessary? ',
    'forced_fight_definition': 'What makes a fight forced? List conditions separated by commas: ',
    'unfavorable_fight_policy': 'When a forced fight becomes unfavorable, what should the coach prefer? ',
    'language_level': 'Preferred language level (simple_game_language/intermediate/advanced): '
}

def main():
    ap=argparse.ArgumentParser(description='Persist the player goal questionnaire.')
    ap.add_argument('--answers',type=Path,help='JSON file containing questionnaire answers')
    ap.add_argument('--source-path',required=True)
    ap.add_argument('--session-id',default=None)
    ap.add_argument('--output',type=Path,required=True)
    args=ap.parse_args()
    answers=json.loads(args.answers.read_text()) if args.answers else {}
    for key,prompt in QUESTIONS.items():
        if key not in answers:
            answers[key]=input(prompt).strip()
    def split(v):
        return [x.strip() for x in v.split(',') if x.strip()] if isinstance(v,str) else list(v)
    primary=answers['primary_goal']
    secondary=split(answers['secondary_goals'])
    forced=split(answers['forced_fight_definition'])
    policy=answers['engagement_policy']
    unfavorable=answers.get('unfavorable_fight_policy','take one safe exchange then retreat when damage or lost position threatens the goal')
    record={'session_id':args.session_id or datetime.now(timezone.utc).strftime('session_%Y%m%dT%H%M%SZ'),'source_path':str(args.source_path),'created_at':datetime.now(timezone.utc).isoformat(),'player_stated_goal':{'primary_goal':primary,'secondary_goals':secondary,'engagement_policy':policy,'forced_fight_definition':forced,'unfavorable_fight_default':unfavorable,'questionnaire_status':'captured'},'language_level':answers.get('language_level','simple_game_language')}
    args.output.parent.mkdir(parents=True,exist_ok=True); args.output.write_text(json.dumps(record,indent=2)); print(json.dumps({'output':str(args.output),'session_id':record['session_id']},indent=2))
if __name__=='__main__': main()
