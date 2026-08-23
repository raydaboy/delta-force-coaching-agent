import json
import subprocess
from pathlib import Path

fixture = Path('/home/ubuntu/context_detector_regression_fixture.json')
out = Path('/home/ubuntu/context_detector_regression_output.json')
script = Path('/home/ubuntu/skills/context-aware-fight-detector/scripts/resolve_event_candidates.py')
subprocess.run(['python3', str(script), str(fixture), '-o', str(out)], check=True)
data = json.loads(out.read_text())
by_id = {e['event_id']: e for e in data['events']}
assert len(data['fights']) == 3, data['summary']
for event_id in ['false_peek_01','false_death_crate_01','false_angle_clear_01','false_loot_02','false_visual_peak_03','false_body_03','false_movement_04']:
    assert by_id[event_id]['resolved_label'] != 'fight', (event_id, by_id[event_id])
for event_id in ['real_fight_01','real_fight_02','real_fight_03']:
    assert by_id[event_id]['resolved_label'] == 'fight', (event_id, by_id[event_id])
assert data['fights'][0]['outcome'] == 'won'
assert data['fights'][1]['outcome'] == 'injured_retreat'
assert data['fights'][2]['outcome'] == 'lost'
print('context detector regression: PASS')
