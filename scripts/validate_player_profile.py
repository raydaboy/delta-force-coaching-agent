#!/usr/bin/env python3
import argparse, json, sys
from pathlib import Path

def main():
    ap=argparse.ArgumentParser(description='Validate a player profile artifact.')
    ap.add_argument('profile',type=Path); args=ap.parse_args(); d=json.loads(args.profile.read_text())
    for key in ['profile_id','created_at','player','experience','teaching_preferences']:
        if key not in d: raise ValueError(f'missing {key}')
    exp=d['experience']; player=d['player']; prefs=d['teaching_preferences']
    if 'current_game' not in exp: raise ValueError('experience.current_game is required')
    if 'games_played' not in exp or not isinstance(exp['games_played'],list): raise ValueError('experience.games_played must be a list')
    if 'current_game_proficiency' not in exp or 'self_rating' not in exp['current_game_proficiency']: raise ValueError('current_game_proficiency.self_rating is required')
    if prefs.get('language_level') not in {'simple_game_language','intermediate','advanced'}: raise ValueError('invalid teaching_preferences.language_level')
    privacy=d.get('privacy',{})
    if privacy.get('share_with_external_services') is True and privacy.get('persist_profile') is False:
        note='external sharing requested for a non-persistent profile; require per-run confirmation'
    else: note='privacy flags are internally consistent'
    print(json.dumps({'valid':True,'profile_id':d['profile_id'],'current_game':exp['current_game'],'games_played':len(exp['games_played']),'privacy_note':note},indent=2))
if __name__=='__main__':
    try: main()
    except (OSError,ValueError,json.JSONDecodeError) as e: print('INVALID:',e,file=sys.stderr); raise SystemExit(1)
