# Series — the recurring shows, and how we test them

*A series is a repeatable format a viewer can recognize in half a second and follow
for. Series are how an account becomes followable instead of a pile of one-offs — and
they're our cleanest A/B unit: same skeleton weekly, so performance differences mean
something. Three series are **active** at any time; each gets 4 slots/week (12 of the
week's 21 posts). The remaining 9 are 3 winner re-cuts and 6 experiments.*

## Active roster (launch)

### S1 — Guess the Calories
- **Recipe:** QUIZ-CARD · **Personas:** P5, P4 · **Hooks:** GUESS, OUTCOME
- Cover = appetizing photo + "Guess the calories. Almost everyone goes low." Reveal 2
  slides later; **the BiteBuddy scan screenshot is the reveal** (receipts, not ads).
  Pinned comment: "drop your guess before you swipe."
- Why first: the research's single best-fit format — outcome-showcase hook + comment
  farm + swipe completion + organic product demo in one post.

### S2 — Protein Per Dollar
- **Recipe:** RANK-CARD · **Personas:** P3, P4 · **Hooks:** LIST, CHEAT, ORDER
- One chain per episode, items ranked by verified protein-per-dollar; save-bait cheat
  sheet near the end. Comment CTA: "name the next chain."
- Why: established 2026 vocabulary, proven demand, endless episodes, strongest
  save+follow mechanics.

### S3 — Why Tracking Fails
- **Recipe:** STORY-BEAT / TYPE-CARD · **Persona:** P1 · **Hooks:** TRACKED,
  RIGHTWRONG, HABIT
- The kind, honest series about quitting and restarting: "you're not overeating,
  you're under-counting," day-4 collapse, the log-of-shame spiral — always ending on
  the friction fix, never on guilt. This is the series only we can run credibly;
  Cal AI's tone can't go here.

### DEMO — the scan flow itself (video track, not a carousel slot)
- **Recipe:** DEMO-VIDEO · **Personas:** P1, P4 · **Hooks:** OUTCOME, POV
- Real screen recordings of dashboard to scan to result to log, edited by
  `Content-Engine/build_demo.py` and scheduled by the **demo-drop** skill.
- Runs *alongside* the three carousel series rather than occupying one of their
  slots, so it does not consume the 2-posts-per-day carousel budget.
- Why it is worth its own track: every carousel argues the app helps, a demo shows
  it. This is the format Cal AI built on. If DEMO starts beating the carousel
  series on saves, follows or app-intent comments, that finding outranks anything
  else in the weekly report.

## The bench (next up when a slot opens)

- **S4 — Small Meals, Big Protein** (P2; BUILD-STEP; the uncrowded GLP-1-era angle —
  situation-framed, never medication-framed)
- **S5 — Macro Matchup** (P5; COMPARE-SPLIT; "both 500 calories" side-by-sides)
- **S6 — Reality Check** (P4/P6; PHOTO-FACT; menu/label claims vs verified numbers)

## Testing protocol (the weekly report enforces this)

1. **Minimum 2 weeks × 2 posts before any verdict.** Four data points is still noise —
   verdicts before that are banned; the report may only note "early signal."
2. **Judged on the metric ladder**, not views: save-rate and follow/profile activity
   first, comment intent ("what app is this?") counted by hand from comments.
3. Verdicts: **scale** (+1 weekly slot, max 3), **iterate** (keep slots, change the
   named weak element — hook wording, cover style, chain choice — one variable at a
   time), **kill** (slot goes to the top bench series; killed series logged in the
   report with the numbers that killed it).
4. Roster is always exactly 3 active. Experiments (the 6 weekly one-off slots) are
   where new series ideas earn a bench spot. Experiments fill the TikTok-only 13:00
   flex slot first, so an experiment is the thing a demo video displaces — which is
   correct, since it is the least-committed content of the week.
5. Every series post carries its `series` id in the registry + manifest, so the
   analytics tables aggregate automatically.
