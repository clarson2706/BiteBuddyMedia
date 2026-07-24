---
name: carousel-week
description: >-
  Generate a full week of BiteBuddy social carousel content — 21 posts (3/day x
  7 days) with slide-by-slide copy, per-slide ChatGPT image prompts, captions,
  hashtags, sounds, post-folder scaffold, and a manifest.json — staged in the
  repo and pushed, ready for Connor to drop in ChatGPT images. Use this whenever
  the task is to stage, generate, produce, or refresh a week (or "next week") of
  BiteBuddy carousels / TikTok Photo Mode / Instagram slideshow posts, including
  when a Routine or schedule fires the weekly "Sunday staging" step. Trigger on
  "run carousel-week", "stage next week's posts", "generate the week's
  carousels", or any weekly BiteBuddy content-generation run. This is the Sunday
  content-generation half of AUTOMATION-WORKFLOW.md — it does NOT
  publish and NEVER generates images with AI (Connor supplies ChatGPT images).
---

# carousel-week — weekly BiteBuddy carousel generator

This skill performs the **Sunday-morning staging** step of
`AUTOMATION-WORKFLOW.md`: it produces a complete, ready-to-illustrate
week of carousel posts and pushes them to the repo. A Routine can fire it every
Sunday and get the same result hands-off.

**Scope boundaries (important):**
- **Copy + prompts + manifest only.** You do NOT publish anything and you do NOT
  generate images. Connor runs the prompts in ChatGPT and drops the PNGs in.
- One "post" = one carousel deck, cross-posted to all 4 platforms
  (Instagram, TikTok, Facebook, YouTube-as-slideshow-Short).

## Content model (the most important rule — read this before anything else)
The posts **educate first and sell last.** They should feel like genuinely useful
nutrition content, not an ad, until the very end.
- **Body slides (1 … N-1) teach.** Nutrition facts, real food photography, honest
  tips, the guess-the-number reveals, a relatable story. **No app UI in the body,
  and Buddy does not appear on every slide** — the content (the food, the fact, the
  number) carries each slide. Buddy is a small host on the cover and a reaction in
  the reveal formats, not a per-slide branding stamp.
- **The last slide of EVERY post is the one app moment** and it is always the same
  shape: the **Today-home hero UI inside a phone silhouette** + **"Download
  BiteBuddy — free on the App Store"** + a **call-to-action tied to that post's
  topic** (e.g. "Know the protein in any meal", "See your real number"). This is the
  only slide that shows the app.
- **Constant size:** every image is **1080 × 1350 px (4:5)**. State it in every prompt.
- Because app UI only appears on the final slide, the **only screenshot the whole
  week needs is the Today-home hero** (`02-today-home/01-today-home.png`), copied to
  the week's `assets/today-home-hero.png`. No per-post screenshot dependencies.

## Per-week deliverables (what "ready to go" means)
Each `Posts/<week>/` must contain, in addition to the 21 post folders:
- `README.md` — human overview + Connor's steps.
- `CHATGPT-GENERATION-GUIDE.md` — the **single self-contained file Connor hands to
  ChatGPT**. It states the global rules (constant size, one-post-at-a-time, reply
  `done` when finished), a **"Uploading to GitHub"** section, and **inlines all 21
  posts' slide prompts** so ChatGPT needs nothing else but the one uploaded screenshot.
- `assets/today-home-hero.png` — the one screenshot ChatGPT uploads (for the CTA slide).
- Each `<post-id>/prompts.md` is a **self-contained generation package**: it states
  the constant size, the **upload target path**, and the per-slide prompts.

## Handoff to the Sunday ChatGPT routine
A ChatGPT scheduled task runs later each Sunday (10am) to generate + commit the
images. It finds this week's batch via a stable pointer, so **every run must refresh
`Posts/current-week.json`** to the week just staged:
```json
{ "week": "<ISO-week>", "guide": "Posts/<week>/CHATGPT-GENERATION-GUIDE.md",
  "hero_asset": "Posts/<week>/assets/today-home-hero.png",
  "week_dir": "Posts/<week>", "posts": 21, "status": "staged",
  "updated_at": "<ts>" }
```
`scaffold_week.py` writes it automatically; if you build a week by hand, write it too.
The routine's prompt + setup live in `Posts/CHATGPT-ROUTINE.md` — keep them
in sync if the guide's contract changes. This staging skill must finish and push
**before** 10am so the routine has something to read.

## Delivery: ChatGPT commits the images to GitHub (no manual downloads)
The intended flow is that ChatGPT, given GitHub write access, **commits each finished
PNG straight into its post's `slides/` folder** — Connor doesn't download or drop files.
Bake this into every week's guide + each `prompts.md`:
- **Target:** `Posts/<week>/<post-id>/slides/NN.png` on branch `main` of
  `clarson2706/BiteBuddyMVP`, via the **GitHub Contents API**
  (`PUT /repos/{owner}/{repo}/contents/{path}` with base64 `content`; GET the existing
  `sha` first to overwrite). The guide includes a ready Python snippet.
- **Auth:** the GitHub connector / a Custom GPT Action (*Contents: read & write*), or a
  fine-grained PAT Connor pastes at runtime. **Never write a token into the repo, a
  commit, or any generated file** — the guide must say so explicitly.
- **Fallback:** if write access isn't set up, ChatGPT returns one `<post-id>.zip` per
  post and Connor drops the files into each `slides/` folder himself.

## Read these first (the source material lives in the repo)
Before writing anything, load the strategy + templates so the copy is on-brand:
- `AUTOMATION-WORKFLOW.md` — the cadence, folder layout, manifest, guardrails.
- `Carousel-Ideas/01-buddys-list.md` … `04-one-snap-demo.md` — the four
  formats with full slide plans and fill-in-the-blanks. **Your copy comes from
  these.**
- `Research/CAROUSEL-MARKETING-PLAYBOOK.md` — the copy/hook rules.
- `MASCOT_IMAGE_GEN_PROMPTS.md` — the Buddy MASTER STYLE BLOCK + the 14 pose
  lines. Every Buddy image prompt you write is built from these.
- `UI-Library/README.md` — the real screenshot paths for app-proof
  slides (only reference screenshots that exist / are captured).

Then read this skill's own references:
- `references/prompt-recipes.md` — how to write each slide's ChatGPT prompt,
  the caption formula, and the rotating hashtag pools.
- `references/manifest-fields.md` — exact `manifest.json` + `prompts.md` spec.

## Procedure

### 0. Load the performance steer (if it exists)
Before writing anything, read `Analytics/next-week-directives.json`
(produced by the `carousel-optimize` skill, which runs just before this one on
Sunday morning). If present and not `no-data`, let it bias the week:
- give extra of the 21 slots to the top `lean_into.format` and `lean_into.topic`;
- prefer the winning `lean_into.hook_type` and `cover_style` in copy + prompts;
- **re-cut each `recut_winners` post** — same skeleton, a fresh cover slide, a new
  food/topic — as some of the week's posts (proven angle, new at-bat);
- steer away from the `dial_back` values; use `best_hashtags` in the rotation.
Respect `confidence`: on `low` (early weeks) treat it as a nudge, not a mandate,
and keep variety. Guardrails always outrank the steer. If the file is missing or
`no-data`, just run the base playbook below.

### 1. Scaffold the week (deterministic — use the script)
```bash
python3 .claude/skills/carousel-week/scripts/scaffold_week.py
```
Defaults to **next Monday** and `America/Chicago`. This creates
`Posts/<ISO-week>/` with 21 post folders (each has `slides/.gitkeep`
and a `prompts.md` stub) and a `manifest.json` skeleton where every post already
has its `id`, `date`, `time_local` (08:00 / 12:30 / 19:00), `format` (rotated so
no format repeats within a day), and `platforms`. You fill in the creative
fields. Pass `--week-start YYYY-MM-DD` to target a specific week, `--force` to
regenerate.

### 2. Fill every post (the actual work)
For each of the 21 posts, using its assigned `format` for variety (the four format
files in `Carousel-Ideas/` give the angle banks and slide rhythms — but
the **content model above overrides their old slide plans**: educate in the body,
app only on the final slide):

1. **Pick a distinct angle.** Never reuse a title within the week. Vary the
   food/topic across posts so the week feels fresh. **Bias toward high-intent
   topics:** people actively struggling to track (logging speed, quitting apps,
   deficit math, protein goals, eating-out tracking) are the ones who install AND
   pay — prefer those angles over generic food trivia when choosing between two
   ideas of equal strength. Trivia (F2) still earns reach; the point is the mix.
2. **Write the slide copy** — the on-image text for each slide:
   - **Cover:** the educational hook (Buddy as a small host is fine).
   - **Body (each slide one idea):** a nutrition fact + real food photo, a tip, a
     guess/reveal, or a story beat. No app UI. No per-slide Buddy branding.
   - **Final slide (always):** the standard CTA — Today-home hero in a phone
     silhouette + "Download BiteBuddy — free on the App Store" + a topic CTA line.
   Keep the skeleton 5–8 slides total, one idea per slide.
3. **Write `prompts.md`** as a self-contained generation package (see
   `references/prompt-recipes.md`): the package header (zip output name = `<id>.zip`,
   constant **1080×1350**, one PNG per slide), then one prompt per slide. Body
   prompts are food-photo / clean-type / guess-reveal recipes; the final prompt is
   the standard CTA recipe using the uploaded `today-home-hero.png`.
4. **Fill the manifest fields** for that post: `title`, `caption`, `hashtags`
   (3–5, rotated from the pools), `pinned_comment`, `slides_expected` (= number of
   slides), and `cta` (= the topic CTA line on the final slide). Leave
   `tiktok_sound` as `SET_AT_POST_TIME` and `status` as `draft`.
5. **Tag the post** — fill the `tags` object so the optimize loop can learn:
   `hook_type` (e.g. `educational-listicle` / `guess-the-number` /
   `confession-awareness` / `nutrition-literacy`), `topic` (the subject, e.g.
   `hidden-calories`), and `cover_style`. Reuse consistent tag values week to week.

Then build the **week-level package files**:
- Copy `UI-Library/02-today-home/01-today-home.png` →
  `Posts/<week>/assets/today-home-hero.png`.
- Write `Posts/<week>/README.md` (human overview + steps).
- Write `Posts/<week>/CHATGPT-GENERATION-GUIDE.md` — global rules, the
  **"Uploading to GitHub"** section (target paths + Contents-API snippet + token
  security note), **all 21 posts' prompts inlined**, one-post-at-a-time, reply
  `done` at the end.

Work through all 21. This is long but mechanical — a small generator script that
emits `prompts.md` + the guide + README from one data table keeps it consistent.

### 3. Validate before committing
Run a self-check across the week:
- 21 posts present; every post has `title`, `caption`, 3–5 `hashtags`,
  `slides_expected ≥ 5`, `cta`, and a `prompts.md` with that many slide prompts.
- No duplicate titles; ≤ one of each format per day.
- **Number-promise integrity:** any numbered title ("7 foods…") has exactly that
  many FACT slides in its `prompts.md`. No exceptions — see
  `references/prompt-recipes.md` → "Number-promise integrity".
- **Every caption contains one search keyword phrase** (AI calorie counter /
  calorie tracker app / calorie scanner app / food tracker app), woven naturally.
- **Every CTA prompt uses the exact search line** `Search 'BiteBuddy: Ai calorie
  scanner'` (per the App Store search term in BiteBuddyMVP `APP_STORE_METADATA.md`).
- **Every post's LAST slide is the standard download CTA** (Today-home hero +
  "Download BiteBuddy — free on the App Store" + topic CTA).
- **No body slide references app UI** (`grep -L today-home-hero` aside, the only
  `UI-Library` / screenshot mention should be the single CTA slide).
- Week has `README.md`, `CHATGPT-GENERATION-GUIDE.md` (21 inlined posts), and
  `assets/today-home-hero.png`.
- **Guardrails** (see below) hold on every caption and slide line.
- `manifest.json` is valid JSON. Quick check:
  ```bash
  python3 -c "import json,sys;d=json.load(open(sys.argv[1]));print(len(d['posts']),'posts OK')" Posts/<week>/manifest.json
  ```

### 4. Commit, push, notify
- Commit the week's folder to the marketing branch and push (retry with backoff
  on network errors).
- Post a short summary for Connor: week label, 21 titles grouped by day, and his
  one job — "give ChatGPT GitHub write access, upload `assets/today-home-hero.png`,
  paste `CHATGPT-GENERATION-GUIDE.md`, say 'generate and upload week <week>'. ChatGPT
  commits each post's `01.png…` into its `slides/` folder and replies 'done'; skim the
  commits, then say 'images are in'."

Do **not** attempt to publish and do **not** create images.

## Brand palette (put on every slide background/framing)
cream `#FFF8F1`, peach `#F4A261`, deep orange `#E9843A`, sage `#8FA27F`,
lavender `#C9C4F2` (Buddy's own color). Buddy hosts the cover and the CTA slide;
the body slides are content-forward (food/type), not Buddy-branded.

## Guardrails (non-negotiable — bake into every post)
- **No medical/outcome claims** — never "lose X lbs," "guaranteed," "burns fat,"
  or crash-diet / disordered-eating framing. Calorie *facts* are fine; health
  *prescriptions* are not. See `Legal/MEDICAL_AND_NUTRITION_DISCLAIMER.md`.
- **Never feature the Meal Advisor** — it ships as "Coming Soon" / disabled.
- **Real screenshot only, on the CTA slide** — the final slide places the real
  `today-home-hero.png` in a phone silhouette; ChatGPT must not redraw or invent
  UI. Body slides show no app UI at all, so there are no other screenshot
  dependencies to capture.
- **App numbers are AI estimates the user reviews** — keep that honesty visible
  ("editable," "see the reasoning") anywhere a result/number is implied.
- **Buddy stays consistent** — always the MASTER STYLE BLOCK + a named pose from
  the 14-pose set; no AI-drawn effects (glow/sparkles/confetti are composited
  later in Canva). Buddy hosts the cover + CTA and reacts in reveals; he is not on
  every body slide.

## What this skill does NOT do
Publishing, scheduling the actual posts, the Sunday-night readiness check across
delivered images, and the YouTube ffmpeg Short assembly are the *publishing*
half of the workflow — separate from this generation step.
