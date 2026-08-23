#!/usr/bin/env python3
import argparse, json
from datetime import datetime, timezone
from pathlib import Path

def ask(prompt, default=''):
    value=input(prompt).strip(); return value or default

def split(value): return [x.strip() for x in value.split(',') if x.strip()]

def main():
    ap=argparse.ArgumentParser(description='Capture a persistent player profile for calibrated coaching.')
    ap.add_argument('--answers',type=Path,help='JSON answers file')
    ap.add_argument('--output',type=Path,required=True)
    ap.add_argument('--profile-id',default=None)
    args=ap.parse_args(); a=json.loads(args.answers.read_text()) if args.answers else {}
    if not a:
        a={'display_name':ask('Nickname (optional): '),'current_game':ask('Current game: '),'current_mode_or_role':ask('Mode or role: '),'games_played':[],'self_rating':ask('Current-game proficiency: ','unknown'),'hours_or_matches':ask('Hours or matches (optional): '),'rank_or_bracket':ask('Rank or bracket (optional): '),'goals_by_skill':split(ask('Skills to improve, comma separated: ')),'language_level':ask('Language level [simple_game_language/intermediate/advanced]: ','simple_game_language'),'wants_enemy_perspective':ask('Enemy perspective? [y/N]: ','n').lower()=='y','wants_question_first_review':ask('Question-first review? [Y/n]: ','y').lower()!='n','review_depth':ask('Review depth [concise/standard/detailed]: ','standard')}
    now=datetime.now(timezone.utc).isoformat(); games=a.get('games_played',[])
    if isinstance(games,str): games=[{'title':x,'familiarity':'unknown','roles_or_loadouts':[],'time_played':'','transferable_skills':[]} for x in split(games)]
    d={'profile_id':args.profile_id or 'profile_'+datetime.now(timezone.utc).strftime('%Y%m%dT%H%M%SZ'),'created_at':a.get('created_at',now),'updated_at':now,'player':{'display_name':a.get('display_name',''),'region_or_language':a.get('region_or_language',''),'platform':a.get('platform','')},'experience':{'current_game':a.get('current_game',''),'current_mode_or_role':a.get('current_mode_or_role',''),'games_played':games,'current_game_proficiency':{'self_rating':a.get('self_rating','unknown'),'self_rating_scale':a.get('self_rating_scale',''),'hours_or_matches':a.get('hours_or_matches',''),'confidence_by_skill':a.get('confidence_by_skill',{}),'rank_or_bracket':a.get('rank_or_bracket','')},'goals_by_skill':a.get('goals_by_skill',[])},'teaching_preferences':{'language_level':a.get('language_level','simple_game_language'),'preferred_examples':a.get('preferred_examples',[]),'wants_enemy_perspective':bool(a.get('wants_enemy_perspective',False)),'wants_question_first_review':bool(a.get('wants_question_first_review',True)),'review_depth':a.get('review_depth','standard')},'privacy':a.get('privacy',{'persist_profile':False,'share_with_external_services':False,'delete_after_run':False})}
    args.output.parent.mkdir(parents=True,exist_ok=True); args.output.write_text(json.dumps(d,indent=2)); print(json.dumps({'output':str(args.output),'profile_id':d['profile_id']},indent=2))
if __name__=='__main__': main()
