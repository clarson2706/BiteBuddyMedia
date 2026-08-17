# BiteBuddy Design System

*The single reference for what BiteBuddy is, who it serves, what it does, and how it looks and
sounds. Covers both the iOS product and the social content built from it.*

## Provenance, read this first

This document has two kinds of statements and they are not equally reliable.

**Verified** means read directly off the 19 real app screenshots in `UI-Library/` during this
writing pass. Anything about screens, features, pricing, targets, XP values, or on-screen copy is
verified and cited to a file.

**Carried** means reconstructed from `CLAUDE.md`, `Content-Engine/DESIGN-SYSTEM.md` and
`Research/TARGET-USER-PROFILES.md`, which were deleted from this repo on 2026-08-17. The content
is faithful but the source files no longer exist here to check against. Recover the originals with
`git checkout e9b8b9e -- CLAUDE.md` if you want to diff.

Where the two disagree, the screenshots win. There is one significant disagreement, in
[Typography](#typography).

---

## 1. What BiteBuddy is

An AI calorie and macro tracking iOS app. Photograph your food, get calories and macros, review
and edit, save. A mascot named Buddy reacts to what you log.

The product's whole argument is that **tracking fails on friction, not on willpower**. Every
feature is downstream of that.

### The four positions, never stated as slogans

1. Photo scanning removes the tedium that makes people quit tracking.
2. BiteBuddy is kind. No shame, no red-number guilt, no diet-culture pressure.
3. Estimates are editable and honest. Consistency beats false precision.
4. No billing tricks.

*(Carried.)*

### App Store search line, used verbatim

```
Search 'BiteBuddy: Ai calorie scanner'
```

---

## 2. Goals

**Product goal.** Get a user to log on more days than they otherwise would, by making a single log
take seconds and by never punishing a gap.

**Business goal.** Convert engaged free users to Pro at the moment scan volume becomes the
constraint, not by walling off core value.

**Content goal.** Qualified installs, not vanity reach. A viewer should arrive already
understanding that the app answers "what was actually in that."

**The anti-goal.** BiteBuddy is not competing on accuracy. See
[the anti-persona](#the-anti-persona).

---

## 3. Who it is for

Eight personas. Every piece of content names exactly one. *(Carried.)*

| ID | Persona | Core situation |
|---|---|---|
| **P1** | Restarter, 28-50 | Has quit MyFitnessPal or Lose It before. Quit because logging took too long and one missed day collapsed the attempt. |
| **P2** | Small-appetite protein seeker, skews 40-64 | Appetite is suppressed. Must hit 80-100g protein in small meals. Never name or assume medications. |
| **P3** | Bulker, male 16-27 | New to lifting. Protein grams are the goal, calories secondary. |
| **P4** | Zero-friction professional, 27-45 | Eats out constantly, analytical, time-starved. Tests claims. |
| **P5** | Glow-up tracker, female 18-30 | Aesthetic goals, IG/TikTok native. **Highest sensitivity segment** for compulsive tracking. |
| **P6** | Wake-up call, 45-65 | Doctor mentioned A1c, cholesterol or BP and asked for a food diary. |
| **P7** | Reclaimer, postpartum 25-40 | Zero hands, zero time, may be breastfeeding and need more food, not less. |
| **P8** | Dining-hall, college 18-22 | Unlabeled buffet food, broke. P5's sensitivity rules apply in full. |

### The anti-persona

The gram-weighing data purist. Never write accuracy bait ("99% accurate", "exact calories from a
photo"). Frame the scan as fast, consistent and editable:

> close enough, every meal, beats perfect twice a week

---

## 4. Use cases

The jobs the product actually gets hired for, in rough order of frequency:

1. **Log a meal I did not cook** — restaurant plate, takeout container, dining-hall tray. No
   barcode, no recipe, no label. This is the core case and the reason photo scan exists.
2. **Check a packaged item before buying** — label or barcode scan in the aisle.
3. **Answer "how much have I had today"** — glance at Today, no interaction.
4. **Hit a protein floor in a small appetite** — P2 and P7 checking whether a meal clears 30g.
5. **Reality-check a habit** — the drink or snack that turns out to be a meal.
6. **Re-enter after a lapse** — return on day 9 without the app implying failure.
7. **See a week honestly** — the weekly report, including which days were missing.

---

## 5. Feature inventory

All verified from `UI-Library/` unless marked.

### Navigation

Four tabs, persistent bottom bar: **Today · Scan · Log · Progress**. Active tab is deep orange with
a filled pill; inactive is charcoal outline.

### Onboarding and plan setup
`01-onboarding-auth/`

- Stepped flow with a deep-orange progress bar.
- **Your daily plan** — targets card with icon per row: Calories `2210 kcal`, Protein `180 g`,
  Carbs `224 g`, Fat `66 g`, Fiber `31 g`.
- **Projected goal date** with pace: `November 6, 2026 · About 1.3 lb per week`.
- **Why these numbers** — resting-energy estimate from age, sex, height, current weight; activity
  level estimating maintenance; a statement that the requested pace fits within plan guardrails.
- Legal acceptance screen.

This screen is the clearest expression of position 4. The app shows its arithmetic.

### Today
`02-today-home/`

- Wordmark, date, greeting by name, streak flame chip.
- **Buddy's Reaction** — the signature component. Buddy pose centered between two vertical meters:
  **Energy** (Dip ↔ Lift) and **Comfort** (Load ↔ Ease). Below, a state label
  (`Getting hungry`), a plain-language explanation, and a `Why Buddy feels this way ↗` disclosure.
- Insight card, icon plus one finding, e.g. *"Logged calories are below today's range."*
- **Today's logged nutrition** — large calorie figure, remaining figure, concentric progress rings,
  per-macro bars with `used / target` and a shortfall note.
- **XP & Levels** sheet and **Your streak** sheet.

### Scan and capture
`03-scan-capture/`

Four capture methods: **photo, label, barcode, voice**. Screens: scan home, camera viewfinder with
mode variants, photo preview, analyzing state.

### Food result
`04-food-result/`

- Title `Review Food`, an `AI Estimate` chip, save/bookmark.
- Food name, and a confidence line: `Food match: high confidence`.
- Buddy reacting to the meal, over the caption `ILLUSTRATIVE · MODELS THIS MEAL BY ITSELF`.
- Calories large, then three macro chips: Protein (green), Carbs (orange), Fat (green).
- Meal segmented control: Breakfast / Lunch / Dinner / Snack.
- **How much did you eat?** portion control, defaulting `All · 100%`.
- Persistent disclaimer: *"AI estimates can be inaccurate. Review and edit before saving."*
- Actions: `Edit`, re-estimate, and a primary `Review & Log · 580 cal`.

Three separate honesty affordances on one screen — confidence, illustrative label, disclaimer.
That is deliberate and should not be trimmed.

### Log and weekly report
`07-reports/`

- Log tab with Day / Week / Month.
- Weekly report with date-range stepper.
- **Buddy's Weekly Read** — eyebrow, serif headline, and an explicit methodology sentence:
  *"You logged on 7 of 7 days; averages use only those logged days."*
- Findings list with check and target icons, including shortfalls stated plainly.
- **Week at a glance** — days logged, entries logged, avg kcal.
- **Daily energy** bar chart against a target line.

### Progress
`06-progress-weight/`

Current weight, goal weight, delta chip (`5.7 lb down in 3 months`), weight-over-time chart with
1W / 1M / 3M / 6M / 1Y / All ranges and a dashed goal line, stat tiles (streak days, level, meals
logged), recent weigh-ins, `Log weight`.

### Gamification
`02-today-home/04-xp-levels.png`

- Level, total XP, progress bar, XP to next level.
- **Learn BiteBuddy** one-time rewards: set up your goals, try your first scan, make it yours (edit
  an estimated food), log your first food.
- **Keep earning**: log a food `+20 XP` per unique entry; meet the core daily targets `+75 XP`
  (calories, macros, fiber, sodium, complete added-sugar data); streak milestones `25-500 XP` at
  3, 7, 14, 30, 60 and 100 days.

Note that *editing an estimate* is a rewarded action. The product teaches correction, not
compliance.

### Pro and pricing
`09-paywall-pro/`

| | Free | Pro |
|---|---|---|
| Scans | 10 per week | 100 per day |
| Capture | — | photo, label, barcode, voice |
| Results | — | personalized to goal and targets |

**Annual $49.99** (marked *Best value*) · **Monthly $7.99**. Headline: *"More room to learn what
works."* Primary action `Continue with Pro`.

The paywall sells volume and convenience, not access to the core loop.

### Not shipped

**Meal Advisor** ships disabled as "Coming Soon." Never feature it in content. *(Carried.)*

---

## 6. Brand foundations

### Color

Canonical tokens *(carried)*:

| Token | Hex | Role |
|---|---|---|
| Cream | `#FFF8F1` | Default background, everywhere |
| Peach | `#F4A261` | Accent shapes, chips, secondary highlights |
| Deep orange | `#E9843A` | Headlines, key numbers, primary CTA |
| Sage | `#8FA27F` | Good/better indicators, secondary accents |
| Lavender | `#C9C4F2` | Buddy's colour; quiz cards, playful accents |
| Charcoal | `#3A3A3A` | Body text, subtitles |

The shipped app uses three shades that are **not** in the token list and should be reconciled:

- A **deeper rust** for primary buttons and the active tab, noticeably darker than Deep orange.
  Compare `Review & Log` and `Log weight` against the paywall's `Continue with Pro`.
- A **forest green**, darker than Sage, for progress rings, check badges and positive figures.
  Sage appears as the lighter fill behind it.
- A **near-black**, darker than Charcoal, for display numerals and headlines.

Semantic usage that is consistent across screens: green reads *on track / complete*, orange reads
*action / attention*, lavender is reserved for Buddy and playful surfaces. **No red anywhere.** The
absence of red is a deliberate expression of position 2 and should be treated as a rule.

### Typography

**This is the one place the app and the social system disagree, and it needs a decision.**

The **app** pairs a high-contrast **serif** for display type — headlines, calorie figures, level
numbers, the wordmark — with a clean **sans** for body, labels and controls. The serif is doing the
brand work.

The **social system** *(carried)* specifies the opposite: one bold **rounded sans** for headlines
(Quicksand Bold / Baloo 2 / Fredoka, pick one and lock it) with Inter or Poppins for body. The
deleted `Brand-Assets/fonts/` held Baloo 2 and Inter, confirming that is what slides used.

So a viewer who sees a carousel and then opens the App Store sees two different brands. My
recommendation is to **move social to the app's serif-plus-sans pairing**, because the app is the
thing being sold and its typography is the more distinctive of the two. That is a decision for you,
not a change I have made.

Open item: the app's serif is not yet identified by name. Someone with the Xcode project should
read it out of the font stack rather than guessing from a screenshot.

Sizing floor for social: **minimum body ~36pt at 1080×1350**, legible at feed size.

### Shape, depth, layout

- **Cards** — generously rounded rectangles on cream, very soft shadow, near-flat. Corner radius is
  large and consistent; nothing is sharp.
- **Chips and pills** — fully rounded. Used for status (streak), category (macros), segmented
  controls, and tier badges.
- **Icons** — simple line-and-fill glyphs, one per data row, tinted to the semantic colour of that
  row. Never decorative-only.
- **Density** — low. One idea per card, generous padding, plenty of cream.
- **Numbers are the hero.** On every data screen the figure is the largest element and the label is
  small beneath it.

---

## 7. Buddy

The mascot, and the only character in the system.

### Canonical design *(carried)*

A cute chubby round fuzzy monster. Soft lavender/periwinkle fur with subsurface scattering. Two
small smooth beige curved horns. Large round glossy black eyes with white highlights. Small mouth
with two tiny lower fangs. Oversized cream knit hoodie with drawstrings and a front pocket. Short
stubby legs, small rounded paws. Soft studio lighting from upper left.

### The 13 canonical poses

`Brand-Assets/buddy-poses/`, in `source/` and `transparent/` (RGBA cutout):

`idle` · `happy` · `thinking` · `warning_check` · `protein_powerup` · `fiber_shield` ·
`balanced_glow` · `heavy_meal` · `sugar_lightning` · `sugar_crash` · `sodium_fog` ·
`goal_celebration` · `level_up`

### Hard rules

1. **Never generate Buddy with an image model.** That is what made him drift. Composite the
   existing transparent PNGs. New poses only from the master style block, matching existing framing.
2. **Effects are not in the art.** No lightning, fog, shields, sparkles or auras drawn into the
   character. The app adds motion and effects in code; social composites them in the editor.
3. **Buddy is a host, not the subject.** Small, lower third, never filling the frame.
4. **Buddy is not a category signal.** To a stranger scrolling, he reads "cute app," not
   "nutrition." He earns his place on the CTA slide, not the cover.

### The reaction model

Buddy expresses two axes, both visible on Today: **Energy** (Dip ↔ Lift) and **Comfort**
(Load ↔ Ease). A pose plus a state label plus one sentence of plain explanation, always with a
disclosure to the reasoning. Buddy never judges the food. He reports a state and explains it.

---

## 8. Voice

Confident, neutral, kind.

**Always**

- Hedged causality for science: *can, may, often, for some people, in this serving*.
- Numbers with context. A figure alone is not an insight.
- Methodology stated when it affects the reading (*"averages use only those logged days"*).
- Plain language over clinical language.

**Never**

- Food shaming, body shaming, or moral labels: *good, bad, clean, cheat, guilt-free*.
- Fear language or diagnostic language.
- Implying more protein equals healthier, fewer calories equals better, one meal causes weight
  gain, or one food fixes anything.
- **Em dashes.** Use a comma, colon, semicolon or hyphen. This applies to every outbound surface:
  slides, captions, DMs, briefs.

---

## 9. Guardrails

Non-negotiable, on every surface. *(Carried.)*

1. **No medical or outcome claims.** No "lose X lbs." Calorie and macro facts yes, health
   prescriptions no.
2. **Never feature the Meal Advisor.** It ships disabled.
3. **No precision claims.** See [the anti-persona](#the-anti-persona).
4. **Real screenshots only.** Never redraw, mock, or invent app UI or in-app numbers.
5. **Real food photography** on food-hero slides. AI-rendered food is the fastest slop tell, and it
   is worse when a real number sits next to it.
6. **Food-positive always**, and absolutely for P5 and P8.
7. **Approval gate.** Anything that spends money, changes App Store copy, contacts real people, or
   publishes outside the normal loop is Connor's call.

---

## 10. Social content system

*(Carried, with the current template's numbers.)*

### Canvas

- **1080×1350, 4:5**, PNG under 8 MB.
- Safe margins **90 px** all sides.
- Nothing critical in the **bottom 180 px** — platform UI overlays it.

### Deck shape

Seven slides: **cover, five body slides, CTA.** The five body slides must form a narrative arc with
a turn in it, not five disconnected facts.

### Slide archetypes

`RANK-CARD` rankings · `PHOTO-FACT` listicles and hidden numbers · `QUIZ-CARD` guess and A-vs-B ·
`COMPARE-SPLIT` same-calorie matchups · `BUILD-STEP` order builders with a running total ·
`CHEAT-GRID` the saveable dense reference slide · `TYPE-CARD` pure-typography beats ·
`STORY-BEAT` narrative and confession posts.

### The CTA slide

Always shows the **real Today dashboard** in a phone silhouette with Buddy beside it, the post's CTA
line above, and the App Store line beneath. Never a text-only "it's on the App Store" close. People
need to see the product to want it.

### Cover principle

The cover image should state the **promise**, not the subject. A plate of food reads *food account*.
A plate of food with a number on it reads *BiteBuddy*. **The number is the category signal.**

### Anti-slop

1. Real food photography on food slides, never AI-rendered food.
2. Rotate at least three template variants so consecutive posts do not share a layout.
3. Vary crop and caption between platforms; identical cross-posted media is penalised.
4. The account must look human-operated: pinned comments, replies, occasional native content.

### Platform ceilings

| Platform | Asset | Cadence |
|---|---|---|
| TikTok | same PNGs, letterboxed, or a 9:16 set | ≤3/day, spaced |
| Instagram | 4:5 PNGs, ≤10 slides | ≤2/day, spaced 5h+ |
| Facebook | same PNGs | mirrors Instagram |
| YouTube | slideshow Short, 30-40s | 1-2/day |

### Illustrated scenes

`Brand-Assets/scene-backgrounds/` holds a recurring illustrated character across one day: morning,
list, store, label, cooking, plate, plus a defocused CTA background. Masters are 1080×1920; the 4:5
production crops use vertical offset 285. `character-reference-sheet.png` reproduces her in a later
batch.

Scope: illustration is for **narrative rows** where the subject is a person. Ranking, cheat-sheet
and comparison decks keep **real food photography**, because a stylised illustration next to a hard
number reads as a lie.

---

## 11. Open questions

Things this document cannot resolve and someone should decide:

1. **Serif or rounded sans for social.** See [Typography](#typography). Blocking a consistent brand.
2. **Name the app's serif.** Requires the Xcode font stack.
3. **Reconcile the palette.** Add the rust, forest green and near-black to the token table with
   real hex values pulled from the app, or correct the app to the existing tokens.
4. **No Canva Brand Kit exists.** Nothing enforces palette or type on new designs.
5. **Two empty UI sections** — `05-log-diary/` and `08-profile-settings/` have no screenshots, so
   the diary and settings surfaces are undocumented here.
