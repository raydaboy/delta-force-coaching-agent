// Clone-ready session workbook and tactical playbook entry.
// The renderer writes a private workbook_data.json beside this template at build time.

#import "report-theme.typ": report-accent, report-theme

#let data = json("workbook_data.json")
#let cyan = rgb("14d9ec")
#let magenta = rgb("ed4aaf")
#let amber = rgb("f5b537")
#let ink = rgb("18202b")

#show: report-theme.with(
  title: data.at("title"),
  author: "Gameplay Coaching Agent",
  rhythm: "report",
  running-header: true,
)

#let evidence(label, items, color) = [
  #text(weight: "bold", fill: color)[#label] \
  #for item in items [• #item \
  ]
]

#let lesson-page(lesson) = [
  #pagebreak()
  #set text(size: 9pt)
  #set par(leading: 0.93em, spacing: 0.26em)
  #text(size: 17pt, weight: "bold", fill: report-accent)[#lesson.at("title")]
  #text(size: 8pt, fill: cyan, weight: "bold")[SOURCE: #lesson.at("source_window").at("start")s–#lesson.at("source_window").at("end")s  •  DECISION: #lesson.at("source_window").at("decision")s  •  OUTCOME: #lesson.at("source_window").at("outcome")s]
  #v(0.35em)
  #align(center)[#image(lesson.at("snapshot_path"), width: 78%)]
  #v(0.25em)
  #grid(
    columns: (1fr, 1fr),
    gutter: 0.7em,
    [#evidence("OBSERVED", lesson.at("observed"), cyan)],
    [#evidence("INFERRED", lesson.at("inferred"), magenta)],
  )
  #evidence("UNKNOWN", lesson.at("unknown"), amber)
  #v(0.25em)
  *Decision:* #lesson.at("decision_point") \
  *Better next option:* #lesson.at("alternative").at("action") \
  *Trade-off:* #lesson.at("alternative").at("tradeoff") \
  *Likely benefit:* #lesson.at("alternative").at("likely_benefit")
  #v(0.2em)
  #block(fill: luma(244), inset: 0.45em, radius: 4pt)[
    *Cue:* #text(fill: amber, weight: "bold")[#lesson.at("cue")]  |  *Trigger:* #lesson.at("drill").at("trigger") \
    *Action:* #lesson.at("drill").at("action") \
    *Measure:* #lesson.at("drill").at("success_condition") _(#lesson.at("drill").at("scope"))_
  ]
  #v(0.22em)
  #block(fill: luma(248), inset: 0.4em, radius: 4pt)[*Reflect:* #lesson.at("reflection_prompt") \
  _My answer:_ ........................................................................................................................]
]

// Cover
#page(margin: (top: 26%, x: 2.1cm), numbering: none, header: none)[
  #align(center)[
    #text(size: 26pt, weight: "bold", fill: report-accent)[#data.at("title")]
    #v(0.7em)
    #text(size: 14pt, fill: ink)[A tactical playbook and training workbook for the next session]
    #v(2.1em)
    #line(length: 42%, stroke: 0.6pt + cyan)
    #v(1.8em)
    #text(size: 11pt)[Primary match goal] \
    #text(size: 14pt, weight: "bold")[#data.at("player_goal")]
    #v(2em)
    #text(size: 10pt, fill: luma(95))[Evidence-first. Private source. Actionable next steps.]
  ]
]

#pagebreak()
= Match-at-a-glance
#data.at("session_summary").at("narrative")

== Strengths to keep
#for strength in data.at("strengths") [
  *#strength.at("title").* #strength.at("evidence") \
  _Why keep it:_ #strength.at("why_keep") \
]

== Priorities for the next run
#for priority in data.at("priorities") [
  *#priority.at("title").* #priority.at("pattern") \
  _Rule:_ #priority.at("rule") \
]

= How to use this workbook
Watch the source lesson once without pausing. Then use the evidence stack to separate what the frame proves from the coach's cautious interpretation. Write one answer to each reflection prompt before moving to the next lesson. Take only the three next-session rules into the next match.

#for lesson in data.at("lessons") [#lesson-page(lesson)]

#pagebreak()
= Next-session rules
#for rule in data.at("next_session_rules") [
  *#rule.at("trigger")* → #rule.at("action") \
]

== Practice plan
#for drill in data.at("practice_plan") [
  *#drill.at("name").* #drill.at("instruction") \
  _Measurement:_ #drill.at("measurement") \
]

#pagebreak()
= Evidence, limits, and provenance
This workbook is a training aid, not an all-seeing replay system. It keeps the source boundary visible so that useful coaching does not become invented certainty.

== Known limits
#for limit in data.at("evidence_limits") [• #limit \
]

== Snapshot index
#for lesson in data.at("lessons") [
  *#lesson.at("lesson_id"):* source #lesson.at("source_window").at("start")s–#lesson.at("source_window").at("end")s; decision at #lesson.at("source_window").at("decision")s; outcome at #lesson.at("source_window").at("outcome")s. \
]

== Final reminder
#text(fill: amber, weight: "bold")[The goal is not to replay the mistake perfectly. The goal is to recognise the trigger earlier next match.]
