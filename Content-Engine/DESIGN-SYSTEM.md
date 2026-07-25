# BiteBuddy Slide Design System

*The graphics layer of the content engine. `MASTER-PROMPT-V5.md` produces a CSV where
every post names a `Visual_Recipe`; this doc defines what each recipe looks like and the
two ways to render it: **Route A — Canva Bulk Create** (template + CSV merge) and
**Route B — Claude-designed slides** (Claude builds each deck via the Canva MCP tools or
direct 1080×1350 image generation). Same visual language either way, so the account
looks consistent no matter which route produced a given week.*

Approval gate (unchanged, from `CLAUDE.md`): anything published is Connor's call —
draft, show, then post. Both routes end at a review step, never at auto-publish.

---

## 1. Brand tokens

| Token | Value | Use |
|---|---|---|
| Cream | `#FFF8F1` | Default background of every slide |
| Peach | `#F4A261` | Accent shapes, highlights, secondary chips |
| Deep orange | `#E9843A` | Headlines, key numbers, CTA button |
| Sage | `#8FA27F` | "Good/better" indicators, secondary accents |
| Lavender | `#C9C4F2` | Buddy's color; quiz cards, playful accents |
| Charcoal | `#3A3A3A` (soft) | Body text, subtitles |

- **Typography:** one bold rounded sans for headlines (Canva: Quicksand Bold /
  Baloo 2 / Fredoka — pick ONE and lock it), a clean sans for body (Inter / Poppins
  Regular). Headline is always the biggest element on the slide. Minimum body size
  ~36pt at 1080×1350 — legible at feed size.
- **Canvas:** master ratio **4:5, 1080×1350 px**, PNG, under 8 MB. (TikTok accepts 4:5
  with light letterboxing; a 9:16 variant set is an optional later upgrade.)
- **Safe margins:** 90 px all sides; nothing critical in the bottom 180 px (platform UI
  overlays).
- **Buddy:** appears on the **cover and CTA slide only** (transparent-PNG poses from
  `Brand-Assets/buddy-poses/transparent/` — the 13 canonical app renders; never
  generate Buddy with an image model, that is what made him drift. The MASTER STYLE
  BLOCK in `Brand-Assets/MASCOT_IMAGE_GEN_PROMPTS.md` is only for a genuinely new
  pose, and match the existing framing). Body slides are
  content-forward. Buddy is small (lower third), a host — never filling the frame. No
  drawn effects; composite sparkles/confetti in the editor if ever needed.
- **App UI:** real screenshots only, from `UI-Library/` — the standard is the Today-home
  hero (`UI-Library/02-today-home/01-today-home.png`) in a simple phone silhouette, and
  the scan-result screen (`UI-Library/04-food-result/01-food-result.png`) when a post
  uses the scan as receipts. Never redraw, mock, or invent UI or numbers.

### Anti-slop rules (survival, not taste — see `Research/HOOK-INTELLIGENCE-2026.md` §Anti-patterns)

TikTok's July 2026 crackdown targets faceless AI-content health accounts — our exact
risk profile. Countermeasures, mandatory on both routes:

1. **Real food photography** on food slides (Canva stock / real photos), never AI-rendered
   food. AI renders of food are the fastest "slop" tell.
2. **Rotate at least 3 template variants** (§4) so consecutive posts don't share an
   identical layout. Vary background accent shapes, photo crops, and headline placement
   week to week.
3. Vary crops/captions **between platforms** (IG now penalizes identical cross-posted
   media).
4. The account must look human-operated: pinned comments, replies, occasional native
   content. (Ops item, but design supports it: leave room for personality in captions.)

---

## 2. Slide archetypes (the `Visual_Recipe` vocabulary)

Every post's `Visual_Recipe` in the CSV is one of these. Each defines the layout of the
body slides; covers and CTAs are shared across all recipes.

**Shared slide 1 — COVER:** cream background, headline (the hook) top 40%, dominant;
one visual pattern-interrupt: Buddy pose (small, lower third) OR the subject food photo
OR a huge number. Optional small "series chip" (peach pill, e.g. `PROTEIN PER $`).

**Shared final slide — CTA (HARD REQUIREMENT, every carousel, no exceptions):** the last
slide **always shows the real Today dashboard inside a phone silhouette**, with Buddy
beside it, the post's topic CTA line above, and `Download BiteBuddy, free on the App
Store` beneath. The App Store search line appears only on APP-CTA rows, and the renderer
strips it from the headline when it is already in the CTA text so it never prints twice.

**Never a text-only "it's on the App Store" close.** People need to *see* the product to
want it: the dashboard, the rings, Buddy's reaction, the real numbers. A sentence about
an app is not a demo of one. This holds regardless of the post's CTA type, so a FOLLOW or
SAVE post still shows the phone; only the words above it change.

Implemented by `phone_mock()` in `Content-Engine/render_slides.py`, which crops
`UI-Library/02-today-home/01-today-home.png` to the dashboard hero so the rings and
numbers stay legible at feed size. Real screenshot only, never redrawn or mocked.

| Recipe | For | Body-slide layout |
|---|---|---|
| `RANK-CARD` | rankings, leaderboards | Big rank number (deep orange, top-left), food photo right 50%, item name + `Xg protein · Y cal` stat line bottom. Same grid every slide; the changing rank number creates the rhythm. |
| `PHOTO-FACT` | listicles, hidden-sugar, mistakes | Real food photo top ~60%, bold one-line fact below on cream, optional small peach chip with the key number. |
| `QUIZ-CARD` | guess-the-number, A-vs-B | Question slide: photo on lavender card + "Guess the calories" + A/B/C chips. Reveal slide: the same photo small, the answer HUGE in deep orange, one-line explanation. Final reveal slide may use the real scan screenshot as receipts. |
| `COMPARE-SPLIT` | same-calories, this-vs-that | Vertical 50/50 split, one food each side, shared stat banner across the middle ("BOTH 500 CALORIES"), difference line below. |
| `BUILD-STEP` | order builders, smart swaps | Numbered step chip, item photo left 40%, choice + why right, running total ticker bottom-right on every slide (the ticker is the retention device). |
| `CHEAT-GRID` | saveable reference sheets | 2×3 or 2×4 grid of mini-cards (item + number) on ONE dense slide near the end — the screenshot-me slide — with the preceding slides teasing 1–2 entries each. |
| `TYPE-CARD` | context/setup/verdict/science beats | Pure typography on cream, one idea, generous negative space, subtle accent shapes. Max ~20 words. |
| `STORY-BEAT` | then-I-tracked-it, POV, confession | Casual-feel: photo with slight tilt + tape corners, handwriting-accent sub-line under a bold headline. The "human" recipe — use for P1/P5 narrative posts. |

Rules of thumb: one idea per slide; the changing element (rank, step, reveal) should be
the visually loudest element; by slide 3 the viewer must have received real value (IG
re-serves carousels when viewers reach slide 3+).

---

## 3. Route A — Canva Bulk Create

The CSV from `MASTER-PROMPT-V5.md` is built to feed Canva's Bulk Create (Apps → Bulk
Create → upload CSV → connect fields to text placeholders → generate one design per
row).

**One-time setup (Connor or Claude-via-Canva-MCP):**
1. Build one **master template per recipe family** — minimum four to start:
   `RANK-CARD` (10 pages), `QUIZ-CARD` (10 pages), `PHOTO-FACT` (10 pages),
   `COMPARE-SPLIT`/`BUILD-STEP` as needed. Each template: page 1 = COVER, pages 2–9 =
   that recipe's body layout, page 10 = CTA.
2. Name text placeholders to match CSV columns: `S1_Hook`, `S2_Content` …
   `S10_CTA`. Bulk Create maps column → placeholder; one CSV run yields every post in
   that family.
3. Lock brand colors/fonts as Canva Brand Kit so drops stay on-palette.

**Per-batch flow:** filter the CSV by `Visual_Recipe` → run Bulk Create against the
matching template → swap in food photos per slide (Canva stock; this is the manual step
Bulk Create can't do from text) → export PNGs 1080×1350 → drop into the post folders /
hand to `carousel-publish`.

**Honest limitation:** Bulk Create fills *text*; photos still need a human pass
(~2–3 min/post with the template doing the layout). The 3-variant rotation = build a
second look per family in week 2, third in week 3.

---

## 4. Route B — Claude-designed slides

When Connor says "Claude, design this week": Claude takes the same CSV rows and builds
each deck directly —

1. **Via Canva MCP** (`generate-design-structured` / `edit-design` / brand templates):
   create each deck from the archetype spec above, then `export-design` at 1080×1350.
   Best fidelity to the template system; produces editable Canva designs Connor can
   tweak.
2. **Via direct image generation** (only if the Canva route is unavailable): generate
   per-slide images from the archetype specs — but the **real-food-photo and
   real-screenshot rules still apply**, which means composing text-on-photo layouts
   around sourced photography, not prompting an image model to invent food photos.

Either way Route B ends with: decks staged in the repo/Canva folder → Connor reviews →
only then does `carousel-publish` schedule anything.

**Choosing routes:** Bulk Create is cheapest per post once templates exist and keeps
Connor in the driver's seat; Claude-design is better for one-off formats, template
creation itself, and weeks when Connor has no Canva time. They are not exclusive — the
practical split is Canva for the high-volume recipe families, Claude for new-format
experiments and the templates themselves.

---

## 5. Export + platform spec (recap)

| Platform | Asset | Notes |
|---|---|---|
| Instagram | 4:5 PNGs, ≤10 slides | 1–2 posts/day MAX, spaced (see HOOK-INTELLIGENCE §cadence) |
| TikTok | same PNGs (letterboxed) or 9:16 set | Photo Mode, sound set at post time, ≤3/day |
| Facebook | same PNGs | multi-image page post |
| YouTube | slideshow Short via `build_youtube_short.py` | target 30–40s total, not 15s; keyworded-human title |

Vary caption + crop between platforms (duplicate-content penalty). Guardrails from
`AUTOMATION-WORKFLOW.md` apply to every rendered slide: no medical/outcome claims, no
Meal Advisor, real screenshots only, estimates framed as editable.
