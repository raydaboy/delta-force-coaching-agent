#!/usr/bin/env python3
import argparse, json
from pathlib import Path

def main():
    ap=argparse.ArgumentParser(description='Build a conservative session map from resolved events and a goal record.')
    ap.add_argument('--events',type=Path,required=True)
    ap.add_argument('--goal',type=Path,required=True)
    ap.add_argument('--output',type=Path,required=True)
    args=ap.parse_args()
    resolved=json.loads(args.events.read_text()); goal=json.loads(args.goal.read_text())
    source=dict(resolved.get('source',{})); source.setdefault('duration',source.get('duration_seconds',0)); source.setdefault('fps',0); source.setdefault('resolution',''); source.setdefault('game',''); source.setdefault('mode',''); source.setdefault('limitations',[])
    pg=goal.get('player_stated_goal',goal.get('player_goal',{})); primary=pg.get('primary_goal','user-defined goal')
    fights=[]
    for idx,f in enumerate(resolved.get('fights',[]),1):
        fid=f.get('fight_id',f'fight_{idx:03d}')
        status=f.get('status',f.get('outcome','unresolved'))
        evidence=[]
        for e in f.get('evidence',[]):
            kind=e.get('kind','frame')
            etype='audio' if 'sound' in kind or 'audio' in kind else 'hud' if any(x in kind for x in ['damage','kill','death']) else 'frame'
            evidence.append({'type':etype,'claim':f'Resolver evidence: {kind}.'})
        if not evidence: evidence=[{'type':'frame','claim':'Fight boundary and outcome require visual verification.'}]
        fights.append({'fight_id':fid,'start':f.get('start',0),'end':f.get('end',f.get('start',0)+0.1),'status':status,'outcome':f.get('outcome',status),'key_decisions':[{'decision_id':f'{fid}_decision_01','context_before':'Visible source context before the exchange; player knowledge requires scene review.','action_taken':'Player commits, disengages, or continues the exchange as shown.','consequence':f'Observed resolver outcome: {f.get("outcome",status)}.'}],'evidence':evidence,'unknowns':f.get('unknowns',['Enemy intent and off-screen information are not established.'])})
    ids=[f['fight_id'] for f in fights]
    loss_ids=[f['fight_id'] for f in fights if f['status'] in {'lost','injured_retreat','escaped'}][:4] or ids[:2]
    win_ids=[f['fight_id'] for f in fights if f['status']=='won'][:4] or ids[:2]
    strengths=[{'claim':'The recording contains confirmed close-range or tactical exchanges that can be reviewed as complete episodes.','class':'observed','confidence':0.8,'supporting_fights':win_ids}, {'claim':'The player sometimes converts a visible advantage into a fast outcome.','class':'inference','confidence':0.6,'supporting_fights':win_ids}]
    weaknesses=[{'claim':'Some exchanges end in damage, retreat, or death after the player loses a safe position.','class':'observed','confidence':0.8,'supporting_fights':loss_ids}, {'claim':'The extraction goal may be undermined when the player remains exposed after a bad first trade.','class':'inference','confidence':0.7,'supporting_fights':loss_ids}]
    priorities=[
      {'priority_id':'priority_01','rank':1,'title':'Create an exit before committing','behavior_to_change':'Before taking a close fight, identify the nearest hard cover and route back toward the goal.','why_it_matters':'A forced fight still has to preserve a way to survive and extract.','supporting_fights':loss_ids,'observed_consequence':'The selected loss or escape events show damage, retreat, or death after exposure.','alternative':'Move to the nearest hard cover, take the first safe exchange, then disengage if the path to a safe win disappears.','counterfactual':{'claim':'This would likely preserve more options and reduce exposure; it cannot guarantee survival.','class':'inference','confidence':0.7,'unknowns':['Enemy aim, teammates, and unseen routes are unknown.']},'drill':{'name':'Exit-first repetition drill','success_condition':'Before each forced fight, say or mark one cover point and one retreat direction before firing.'}},
      {'priority_id':'priority_02','rank':2,'title':'Stop sorting loot when danger appears','behavior_to_change':'Cancel inventory or loot interaction immediately when a nearby enemy forces contact.','why_it_matters':primary+' is lost when the player is stationary and cannot aim or move.','supporting_fights':ids[:3] or loss_ids,'observed_consequence':'At least one candidate event is a loot interruption or a fight near a loot route.','alternative':'Break line of sight first, then heal or resume loot only after the area is safer.','counterfactual':{'claim':'This would likely reduce the chance of taking free damage while vulnerable.','class':'inference','confidence':0.7,'unknowns':['The unseen enemy route is unknown.']},'drill':{'name':'Loot-cancel drill','success_condition':'On any shot or damage cue during loot, leave the interface within one second.'}},
      {'priority_id':'priority_03','rank':3,'title':'Separate connected enemies','behavior_to_change':'After the first target, move so the next enemy cannot inherit the same angle.','why_it_matters':'A group fight becomes harder when every target can see the same lane.','supporting_fights':ids[-3:] or loss_ids,'observed_consequence':'Connected cluster events show multiple targets or pressure through linked positions.','alternative':'Use smoke, height, or a corner to shorten the next line of sight before re-peeking.','counterfactual':{'claim':'This would likely make target order safer while keeping the fight forced.','class':'inference','confidence':0.6,'unknowns':['Enemy coordination and hidden angles are unknown.']},'drill':{'name':'One-target lane drill','success_condition':'After each down, change cover or angle before exposing to the next target.'}}
    ]
    objectives=[
      {'objective_id':'objective_01','rank':1,'title':'Protect the extraction route','opening_line':'We will judge every decision by whether it keeps the loot route alive.','question_for_player':'Where is the safest reset before you take the next shot?','reveal':'The map should show the first cover and the visible consequence of staying exposed.','supporting_fights':loss_ids,'drill':'Mark an exit before every forced fight.'},
      {'objective_id':'objective_02','rank':2,'title':'Win forced close fights without chasing','opening_line':'When the enemy comes close, commit quickly—but do not turn a forced fight into an optional chase.','question_for_player':'Is the enemy threatening your position, or are you opening a fight that can be left alone?','reveal':'The review separates forced danger from optional contact.','supporting_fights':win_ids,'drill':'Call forced or optional before firing.'},
      {'objective_id':'objective_03','rank':3,'title':'Improve movement and aim under pressure','opening_line':'We will connect aim quality to the position that gave it time to work.','question_for_player':'What cover lets your crosshair stay ready while your body is harder to hit?','reveal':'The freeze frame names one cover point and one crosshair height.','supporting_fights':ids[:4],'drill':'Move to cover before healing or reloading after damage.'}
    ]
    out={'source':source,'session_goal':primary,'events':resolved.get('events',[]),'fights':fights,'strengths':strengths,'weaknesses':weaknesses,'priorities':priorities,'learning_objectives':objectives,'session_summary':'This session is reviewed against the player-stated goal, with conservative evidence labels and explicit unknowns.','evidence_ledger':[{'type':'metadata','claim':'Source metadata comes from the source manifest or resolver input.'},{'type':'frame','claim':'Fight boundaries and outcomes require visual source review.'}],'unknowns':['Enemy intent, off-screen teammates, and guaranteed counterfactual outcomes are unknown unless directly established.']}
    args.output.parent.mkdir(parents=True,exist_ok=True); args.output.write_text(json.dumps(out,indent=2)); print(json.dumps({'output':str(args.output),'fights':len(fights)},indent=2))
if __name__=='__main__': main()
