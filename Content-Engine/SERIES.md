# Series — the recurring shows, and how we test them

*A series is a repeatable format a viewer recognizes in half a second and follows for.
Series are how an account becomes followable instead of a pile of one-offs, and they are
our cleanest A/B unit: same skeleton weekly, so performance differences mean something.*

*Rewritten 2026-08-01 against the first real numbers. The previous roster was chosen
from research priors before any data existed. It now has data, and the data says
something specific.*

---

## What the numbers changed

At 4,408 lifetime TikTok views the account has **59 likes, 0 comments, 0 shares, 0
profile views and 1 follower.** Reach works. Nothing downstream of reach works.

That is not a distribution problem and it is not a tone problem. It is a **utility
problem**: the roster was weighted toward posts that are *pleasant to read and finish*,
and light on posts that are *worth keeping*. Nobody saves an essay about why tracking
fails. People save a list of what to order.

So the roster shifts toward **reference content** — rankings, best-orders, cheat sheets
— which is also the format the research is most confident about (cheat sheets are the
most-saved carousel type, and saves are a heavy ranking input on both platforms). The
psychology series stays because its tone is genuinely differentiated, but it stops
carrying a third of the week.

**Every series, without exception, ends on the CTA slide**: the real Today dashboard in
a phone, "Download BiteBuddy, free on the App Store", the search line, and
"Follow @bitebuddyapp for more". The renderer enforces this; it is not per-post
discretion. See `render_slides.slide_cta()`.

---

## Active roster

### S2 — Ranked (the workhorse)
- **Recipe:** RANK-CARD · **Personas:** P3, P4, P2 · **Hooks:** LIST, ORDER, CHEAT
- **Format:** *"Every [item type] at [chain], ranked by [metric]."* One chain per
  episode, 6 to 8 ranked entries, then a CHEAT-GRID slide with the whole table on one
  screen, then the CTA.
- **The metric rotates and that rotation is the series' whole engine:**
  protein per 100 calories · protein per dollar · protein per gram of fat · sodium ·
  what actually fills you up per calorie. Same chain can run twice a quarter under a
  different metric without repeating itself.
- **Why this is slot one:** it is simultaneously the most-saved format in the research,
  the most useful thing we can give a stranger, endlessly serialisable, and the one
  where a "do [chain] next" comment is the obvious response. It is also the format
  Connor identified as working in the wild.
- **Hard rule:** every number is verified against the chain's own nutrition page during
  the run, and the source URL goes in the manifest. A number we cannot verify is not
  published. Never estimate a chain figure to fill a slot.
- **Comment CTA:** "which chain should I rank next?" A one-word answer, by design.

### S4 — The Best Order (new, promoted from the bench)
- **Recipe:** BUILD-STEP · **Personas:** P4, P3, P8 · **Hooks:** ORDER, CALLOUT, CHEAT
- **Format:** *"What to order at [chain] if you want [goal] — built one step at a
  time."* Entree, then side, then drink, then the swap that changes the most, with a
  running total ticking in the corner of every slide.
- **Why it earns its own slot next to S2:** S2 is a reference table, S4 is a decision.
  Same source data, different job, and the running total is a genuine retention device
  rather than a tease. Goals rotate: most protein per dollar, biggest meal under 600
  calories, most food for the money.
- **Guardrail:** the goal is always framed as a preference, never as a prescription.
  "If you want the most protein per dollar" is fine. "What you should eat" is not.

### S1 — Guess the Calories
- **Recipe:** QUIZ-CARD · **Personas:** P5, P4 · **Hooks:** GUESS, OUTCOME
- Appetizing real photo, "Guess the calories," reveal two slides later, and **the
  BiteBuddy scan screenshot is the reveal**. Receipts, not an ad.
- **Changed 2026-08-01:** the ask gets dumber. Zero comments came back from open,
  reflective questions across ~900 views. A number is the lowest-effort comment there
  is, so the cover says "comment your guess before you swipe" and the deck says nothing
  else interactive.
- **Known limitation:** our pinned comment cannot be posted to TikTok through the API,
  so the ask has to live *in the deck*, on slide 1 and slide 2, or it does not exist.

### S3 — Why Tracking Fails (reduced from 4 slots to 2)
- **Recipe:** STORY-BEAT / TYPE-CARD · **Persona:** P1 · **Hooks:** TRACKED,
  RIGHTWRONG, HABIT
- The kind, honest series about quitting and restarting: you are not overeating, you
  are under-counting; the day-4 collapse; the log-of-shame spiral. Always ends on the
  friction fix, never on guilt. The series only we can run credibly.
- **Why it is being reduced rather than kept or killed:** it produced the account's
  best individual reach and its worst downstream conversion. It is doing brand work,
  not acquisition work, and four slots a week was overpaying for that. Two slots keeps
  the tone in the feed without spending the week on it.

### DEMO — the scan flow itself (video track, not a carousel slot)
- **Recipe:** DEMO-VIDEO · **Personas:** P1, P4 · **Hooks:** OUTCOME, POV
- Real screen recordings, edited by `Content-Engine/build_demo.py`, scheduled by the
  **demo-drop** skill. Runs alongside the carousel series rather than consuming one of
  their slots.
- **Structural advantage worth knowing:** a video post can carry a sound through the
  API. A TikTok *photo* post cannot. Demos are therefore the only format in this system
  that gets the audio distribution lever at all, which is an argument for more of them,
  independent of how they perform on saves.

## The bench

- **S5 — Both the Same Calories** (P5; COMPARE-SPLIT; the @comparecalories lineage,
  inherently argument-starting and shareable, anti-moralizing by construction)
- **S6 — Scanned, Not Guessed** (P1/P4; RECEIPT; a real plate, the real scan result,
  what the eye got wrong. The closest thing to social proof we can produce ourselves,
  and the most direct install argument)
- **S7 — The Grocery Aisle** (P6/P2; PHOTO-FACT; label claims against the actual panel;
  strictly factual, never diagnostic)

## Weekly slot allocation (21 posts)

| Slot type | Count | Notes |
|---|---|---|
| S2 Ranked | 5 | the workhorse; different chain or metric each time |
| S4 The Best Order | 4 | complements S2 without repeating its data |
| S1 Guess the Calories | 4 | the comment engine |
| S3 Why Tracking Fails | 2 | tone, not acquisition |
| Winner re-cuts | 3 | only when directives name winners, else experiments |
| Experiments | 3 | new formats earning a bench spot |

Seven of the 21 fill the TikTok-only 13:00 flex slot, drawn from experiments first,
since that is the slot a demo video displaces.

## Testing protocol

1. **Minimum 2 weeks and 4 posts before any verdict.** Four data points is still noise.
   Earlier than that the report may say "early signal" and nothing stronger.
2. **Judged on the metric ladder, not views**: saves and shares first, then follows and
   profile visits, then comment intent ("what app is this?") counted by hand. A post
   with 40 views and one genuine question beats 400 silent views.
3. Verdicts: **scale** (+1 slot, max 6), **iterate** (keep slots, change one named weak
   element, one variable at a time), **kill** (slot goes to the top bench series).
4. The roster is always exactly 4 active carousel series plus the demo track.
5. Every series post carries its `series` id in the registry and manifest so the
   analytics tables aggregate automatically.

## The question this roster is built to answer

Not "which series gets the most views." Views are already fine.

**Which series makes a stranger tap the profile?** Until one does, nothing in this repo
can produce an install, and the weekly report should lead with that number every week.
