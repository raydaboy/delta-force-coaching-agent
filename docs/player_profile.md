# Player Profile and Proficiency Calibration

The player profile is an optional onboarding object that persists learning context across recordings. It is not a performance verdict and it is never allowed to override current-recording evidence.

## What to ask

Ask about the current game and mode, prior games with transferable mechanics, roles or loadouts, time played, self-rated proficiency, rank or bracket if the player volunteers it, skill-specific confidence, desired improvements, preferred explanation depth, whether an enemy-perspective explanation is useful, and whether the profile may persist or be shared with external services.

The profile should be short enough to answer conversationally. A user may leave any item unknown. A nickname is sufficient for identity; no real name is required.

## How to use it

| Profile signal | Permitted adaptation | Prohibited inference |
| --- | --- | --- |
| Prior tactical shooter experience | Use familiar comparisons and reduce basic definitions | Do not assume the player knows this game’s map, economy, or operator abilities |
| Prior extraction-shooter experience | Explain loot risk, resets, and extraction routes at a deeper level | Do not assume the player values loot more than they stated for this match |
| New to the genre | Use simple language, short sentences, and one action per cue | Do not lower the evidence standard or treat uncertainty as incompetence |
| Self-rated advanced aim | Spend more time on positioning, timing, and decision quality | Do not excuse visible aim errors or assume mechanics are strong |
| Wants enemy perspective | Offer a panel labelled `ENEMY VIEW — INFERRED FROM VISIBLE GEOMETRY` | Do not draw unseen enemies or claim their intent |
| Wants detailed review | Use standard or deep reviews for high-leverage scenes | Do not fill runtime with generic narration or repeated cards |
| Simple language preference | Say “move behind the wall before healing” | Do not hide uncertainty behind jargon |

## Calibration rule

When profile and video disagree, state the difference as a hypothesis: “You describe yourself as comfortable with close fights, and this clip shows the close reaction was fast; the teachable issue here is the exit after the first damage.” Ask whether that framing feels accurate. Do not diagnose ability, personality, age, health, or motivation from game history or a recording.

## Privacy

Profile persistence is opt-in. External sharing is opt-in. Delete-after-run must be honored. Store only what is needed for coaching, keep profiles separate from raw recordings, and do not commit profiles containing personal information to a public repository. The example profile in this repository is intentionally blank.
