#!/usr/bin/env python3
"""Resolve broad gameplay candidates into context-aware fight events.

The script is intentionally conservative: a candidate must show combat interaction
and a consequence. Weak visual triggers remain contact/non_fight events.
"""
import argparse
import json
from pathlib import Path

INTERACTION = {
    'shots_exchanged', 'weapon_fire_at_live_enemy', 'live_enemy_hit',
    'sustained_exchange'
}
CONSEQUENCE = {
    'damage_feedback', 'kill_feed_attributed', 'enemy_eliminated',
    'player_death', 'retreat_after_damage', 'heal_after_damage',
    'loss_of_contact_after_exchange'
}
HARD_VETO = {
    'loot', 'death_crate', 'inventory_screen', 'angle_clear', 'peek',
    'movement', 'rotation', 'recovery', 'visual_peak', 'generic_audio_peak',
    'body_seen', 'death', 'death_screen', 'menu', 'extraction', 'hacking', 'safe_hacking'
}
RESET_TYPES = {'loot', 'death_crate', 'inventory_screen', 'recovery', 'heal', 'relocation', 'objective_change', 'death', 'death_screen', 'menu', 'extraction'}
OUTCOME_TYPES = {'kill_feed_attributed', 'enemy_eliminated', 'player_death', 'retreat_after_damage', 'loss_of_contact_after_exchange'}


def strength(e):
    try:
        return float(e.get('strength', 0.0))
    except (TypeError, ValueError):
        return 0.0


def evidence_kinds(event):
    return {str(e.get('kind', '')).lower() for e in event.get('evidence', [])}


def has_strong(kinds, group):
    return any(k in kinds and any(str(k).lower() == x.lower() for x in group) for k in kinds)


def normalize_type(event):
    guess = str(event.get('type_guess', 'unknown')).lower().strip()
    if guess in {'death crate', 'death-crate', 'crate'}:
        return 'death_crate'
    if guess in {'angle clear', 'angle-clear', 'clear'}:
        return 'angle_clear'
    if guess in {'inventory', 'inventory screen'}:
        return 'inventory_screen'
    if guess in {'combat', 'engagement', 'fight'}:
        return 'combat'
    return guess or 'unknown'


def outcome_from(kinds):
    if 'player_death' in kinds:
        return 'lost'
    if 'kill_feed_attributed' in kinds or 'enemy_eliminated' in kinds:
        return 'won'
    if 'retreat_after_damage' in kinds or 'heal_after_damage' in kinds:
        return 'injured_retreat'
    if 'loss_of_contact_after_exchange' in kinds:
        return 'escaped'
    return 'unresolved'


def resolve(events, cfg):
    events = sorted(events, key=lambda x: (float(x.get('start', 0)), float(x.get('end', 0))))
    state = {
        'active_episode_id': None, 'active_fight_id': None,
        'last_combat_signal_time': None, 'last_consequence_time': None,
        'last_reset_time': None, 'last_live_target_time': None,
        'continuity_key': None, 'phase': 'neutral', 'fight_index': 0,
    }
    resolved = []
    fights = []
    rejected = []

    def gap_from(prev_end, start):
        return None if prev_end is None else max(0.0, start - prev_end)

    for raw in events:
        event = dict(raw)
        start = float(event.get('start', 0.0)); end = float(event.get('end', start))
        kinds = evidence_kinds(event)
        guess = normalize_type(event)
        location = event.get('location_id') or state['continuity_key']
        gap = gap_from(state.get('_prev_end'), start)
        combat_kinds = kinds & INTERACTION
        consequence_kinds = kinds & CONSEQUENCE
        channels = sorted(combat_kinds | consequence_kinds)
        has_interaction = bool(combat_kinds) or ({'live_enemy', 'damage_feedback'} <= kinds)
        # A death or hit marker is a consequence, not proof of a fight by itself.
        has_prior_combat = state['last_combat_signal_time'] is not None and (start - state['last_combat_signal_time']) <= cfg['outcome_follow_gap_seconds']
        if not combat_kinds and not ({'live_enemy', 'damage_feedback'} <= kinds) and has_prior_combat and ({'player_death', 'kill_feed_attributed', 'enemy_eliminated'} & kinds):
            has_interaction = True
        has_consequence = bool(consequence_kinds)
        hard_veto = (guess in HARD_VETO or bool(kinds & HARD_VETO)) and guess not in {'combat', 'fight'}
        live_target = bool({'live_enemy', 'live_enemy_hit'} & kinds)
        reset = guess in RESET_TYPES or bool(kinds & RESET_TYPES)
        same_episode = (
            state['phase'] in {'contact', 'fight', 'aftermath'} and
            (gap is None or gap <= cfg['merge_gap_seconds'] or (state['last_combat_signal_time'] is not None and start - state['last_combat_signal_time'] <= cfg['outcome_follow_gap_seconds'])) and
            (not state['continuity_key'] or not location or state['continuity_key'] == location) and
            (state['last_reset_time'] is None or start - state['last_reset_time'] > cfg['reset_cooldown_seconds'])
        )

        event['normalized_type'] = guess
        event['evidence_channels'] = channels
        event['state_before'] = {k: v for k, v in state.items() if not k.startswith('_')}
        event['gap_from_previous_seconds'] = gap
        event['continuity_key'] = location

        if hard_veto:
            if state['phase'] in {'fight', 'aftermath'} and guess in {'loot', 'death_crate', 'inventory_screen', 'recovery', 'death', 'death_screen', 'menu', 'extraction'}:
                event['resolved_label'] = 'aftermath'
                event['reason'] = 'Non-fight recovery/loot/death/menu event attached to the active tactical episode; it cannot extend or create a fight.'
                if guess in {'death', 'death_screen'} and state['active_fight_id']:
                    prior = next((f for f in fights if f['fight_id'] == state['active_fight_id']), None)
                    if prior and 'player_death' in kinds:
                        prior['status'] = 'lost'; prior['outcome'] = 'lost'
                state['phase'] = 'recovery'
            else:
                event['resolved_label'] = guess if guess in HARD_VETO else 'non_fight'
                event['reason'] = 'Weak visual or UI trigger vetoed; no independent combat interaction plus consequence.'
            rejected.append(event)
            if reset:
                state['last_reset_time'] = end
                state['continuity_key'] = location
            state['_prev_end'] = end
            event['state_after'] = {k: v for k, v in state.items() if not k.startswith('_')}
            resolved.append(event)
            continue

        if live_target and not has_interaction:
            event['resolved_label'] = 'contact'
            event['reason'] = 'Live target is visible, but an exchange or consequence is not established.'
            state['phase'] = 'contact'; state['last_live_target_time'] = end
            state['continuity_key'] = location or state['continuity_key']
            rejected.append(event)
            state['_prev_end'] = end
            event['state_after'] = {k: v for k, v in state.items() if not k.startswith('_')}
            resolved.append(event)
            continue

        if has_interaction and has_consequence:
            if not same_episode or state['active_fight_id'] is None:
                state['fight_index'] += 1
                state['active_episode_id'] = f'episode_{state["fight_index"]:03d}'
                state['active_fight_id'] = f'fight_{state["fight_index"]:03d}'
                state['phase'] = 'fight'
            else:
                state['phase'] = 'fight'
            state['last_combat_signal_time'] = end
            state['last_consequence_time'] = end
            state['continuity_key'] = location or state['continuity_key']
            outcome = outcome_from(kinds)
            event['resolved_label'] = 'fight'
            event['reason'] = 'Combat interaction and consequence are both supported by independent evidence channels.'
            existing = next((f for f in fights if f['fight_id'] == state['active_fight_id']), None)
            if existing is None:
                existing = {
                    'fight_id': state['active_fight_id'],
                    'start': start, 'end': end, 'status': outcome,
                    'outcome': outcome, 'continuity_key': state['continuity_key'],
                    'supporting_event_ids': [event.get('event_id')],
                    'evidence_channels': channels, 'confidence': 'high' if len(channels) >= 3 else 'medium',
                    'unknowns': [], 'aftermath_event_ids': []
                }
                fights.append(existing)
            else:
                existing['end'] = max(existing['end'], end)
                existing['supporting_event_ids'].append(event.get('event_id'))
                existing['evidence_channels'] = sorted(set(existing['evidence_channels']) | set(channels))
                if outcome != 'unresolved':
                    existing['status'] = outcome; existing['outcome'] = outcome
                existing['confidence'] = 'high' if len(existing['evidence_channels']) >= 3 else existing['confidence']
            event['fight_id'] = state['active_fight_id']
            event['state_after'] = {k: v for k, v in state.items() if not k.startswith('_')}
            resolved.append(event)
            state['_prev_end'] = end
            continue

        if has_interaction:
            event['resolved_label'] = 'contact' if not has_consequence else 'information_limited'
            event['reason'] = 'Interaction is visible, but the required consequence is absent or ambiguous.'
        else:
            event['resolved_label'] = 'information_limited'
            event['reason'] = 'Evidence is insufficient to establish a combat interaction.'
        rejected.append(event)
        state['phase'] = 'contact' if has_interaction else state['phase']
        state['continuity_key'] = location or state['continuity_key']
        state['_prev_end'] = end
        event['state_after'] = {k: v for k, v in state.items() if not k.startswith('_')}
        resolved.append(event)

    # Mark recovery/loot after a fight as aftermath, not new fights.
    for event in resolved:
        if event.get('resolved_label') == 'aftermath':
            target = None
            for fight in reversed(fights):
                if fight['end'] <= float(event.get('start', 0)):
                    target = fight; break
            if target:
                target['aftermath_event_ids'].append(event.get('event_id'))

    for fight in fights:
        if fight['status'] == 'unresolved':
            fight['unknowns'].append('Winner and hidden enemy intent are not established.')
        fight['evidence'] = [{'kind': k, 'class': 'observed'} for k in fight.pop('evidence_channels')]
    return {'fights': fights, 'events': resolved, 'rejected_candidates': rejected, 'detector': cfg}


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('input', type=Path)
    ap.add_argument('-o', '--output', type=Path, required=True)
    ap.add_argument('--merge-gap-seconds', type=float, default=4.0)
    ap.add_argument('--reset-cooldown-seconds', type=float, default=3.0)
    args = ap.parse_args()
    data=json.loads(args.input.read_text())
    events=data.get('events', data if isinstance(data, list) else [])
    cfg={'version':'context-aware-fight-detector-v1','merge_gap_seconds':args.merge_gap_seconds,'outcome_follow_gap_seconds':8.0,'reset_cooldown_seconds':args.reset_cooldown_seconds,'policy':'interaction_plus_consequence','veto_types':sorted(HARD_VETO)}
    output=resolve(events,cfg)
    output['source']=data.get('source',{}) if isinstance(data,dict) else {}
    output['summary']={'candidate_events':len(events),'resolved_fights':len(output['fights']),'non_fight_or_rejected':sum(e.get('resolved_label')!='fight' for e in output['events'])}
    args.output.write_text(json.dumps(output,indent=2))
    print(json.dumps(output['summary'],indent=2))

if __name__ == '__main__':
    main()
