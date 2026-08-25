# Standard Tactical Playbook Format

## Status

This is the **required Markdown format** for future player-facing tactical playbooks in this repository. Use it after the evidence map and lesson ledger are approved. It is a concise quick-reference companion to the deeper Session Workbook & Tactical Playbook PDF.

The standard is intentionally operational. It should tell the player what goal matters, which good habits to preserve, what decisions to change, and which rule to execute under pressure. It must not become a transcript, a generic tips list, or a claim about information the recording does not establish.

## Privacy and evidence rules

Do not commit recordings, extracted snapshots, private paths, private URLs, narration, or generated PDFs. A committed playbook may contain user-approved teaching text, source-window references when suitable, and sanitized evidence descriptions.

Use the evidence vocabulary faithfully:

| Label | Allowed content |
| --- | --- |
| **OBSERVED** | A directly visible or audible action, warning, outcome, resource state, or HUD element. |
| **INFERRED** | A cautious tactical interpretation supported by the visible moment. |
| **UNKNOWN** | Enemy intent, unseen teammates, hidden geometry, scan source, or an unshown result. |

Never convert a useful inference into a fact. Do not promise that the recommended alternative would have guaranteed a win, survival, loot, or extraction.

## Required document structure

Every standard playbook uses the following headings in this order.

```markdown
# <Game / Mode>: Tactical Playbook & Session Guide

## Match Objective
<Ranked goal, forced-fight definition, and improvement focus.>

## Match Overview

### Key Strengths
<Two to three repeatable behaviors worth keeping.>

### Primary Adjustments
<No more than three cross-session priorities.>

## Tactical Decision Breakdown

### Scenario 1: <Short decision name>
**Trigger:** <Visible or player-defined trigger.>

**What happened:** <OBSERVED first; inference and uncertainty where needed.>

**Corrective action:** <Local, source-supported alternative.>

**Execution rule:** `<Trigger> → <Action 1> → <Action 2> → <Outcome focus>`

## Core Rules & Practice Plan

### Core Operating Rules
<Three short trigger-action rules.>

### Execution Drills
<One measurable drill per core rule.>

## Evidence Limits
<The unresolved information and scope limitations that matter to the player.>
```

## Content constraints

| Section | Required standard |
| --- | --- |
| **Match objective** | Preserve the player’s ranking of loot, survival, forced fights, mechanics, and objectives. Define a forced fight from that goal rather than from gunfire alone. |
| **Key strengths** | Name a visible behavior, why it helped, and when to repeat it. A lost fight can still contain a strength. |
| **Primary adjustments** | Limit to three patterns. Each must be a controllable decision, not a label such as “bad aim.” |
| **Scenarios** | Use only moments with a useful trigger and decision. Do not manufacture scenarios from menus, generic travel, or unresolved contacts. |
| **Corrective action** | Name a local visible action where the source supports it. Reject reusable filler such as “use cover” on its own. |
| **Execution rule** | Use short pressure-ready verbs and a clear order. The rule should be easy to say during a match. |
| **Drill** | Include a trigger, action, measurement, and scope such as the next three forced fights or next extraction-focused run. |
| **Evidence limits** | Keep unknown scan source, enemy count, intent, hidden geometry, and outcomes visibly unresolved. |

## Scenario-writing pattern

The standard scenario is written in four layers. The first sentence should be plain player language. The explanation can then add advanced depth without burying the action.

| Layer | Purpose | Example shape |
| --- | --- | --- |
| **Trigger** | Tells the player when the rule applies. | “Position Exposed warning or scan alert.” |
| **What happened** | States the visible choice and consequence; separates inference and unknown. | “The warning appears before continued direct travel. The scan source is unknown.” |
| **Corrective action** | Gives one local alternative and its trade-off. | “Break to the visible wall edge before returning fire; this costs tempo but preserves a reset route.” |
| **Execution rule** | Compresses the lesson into a usable sequence. | “Scan → cover → identify lane → engage.” |

## Relationship to the PDF workbook

The Markdown playbook is the player’s fast operational reference. The optional PDF workbook is the deeper study version, with selected annotated snapshots, reflection prompts, drills, and provenance. They must share the same approved evidence and lesson ledger; neither document may introduce an unsupported claim the other does not contain.

## Quality gate before publishing

Before committing a playbook, verify that it:

1. States the player goal and forced-fight policy.
2. Contains no more than three primary adjustments.
3. Separates OBSERVED, INFERRED, and UNKNOWN where a scenario involves uncertainty.
4. Uses local alternatives with explicit trade-offs rather than generic cover language.
5. Provides a short execution rule and measurable drill for each core adjustment.
6. Contains no private media, source paths, secret values, or unapproved personal data.
