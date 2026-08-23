import json
from pathlib import Path

ROOT=Path(__file__).resolve().parents[1]

def test_blank_player_profile_shape():
    d=json.loads((ROOT/'examples/player_profile_blank.json').read_text())
    assert d['experience']['current_game_proficiency']['self_rating']=='unknown'
    assert d['teaching_preferences']['wants_question_first_review'] is True

def test_questionnaire_has_privacy_and_calibration_rules():
    d=json.loads((ROOT/'templates/player_profile_questionnaire.json').read_text())
    ids={q['id'] for q in d['questions']}
    assert {'games_played','current_game_proficiency','privacy'} <= ids
    assert any('current-video evidence' in rule for rule in d['calibration_rules'])

def test_episode_example_has_question_before_reveal():
    d=json.loads((ROOT/'examples/episode_script.json').read_text())
    kinds=[b['kind'] for b in d['beats']]
    assert kinds.index('question') < kinds.index('reveal')
    assert all(b.get('claim_class') for b in d['beats'])
