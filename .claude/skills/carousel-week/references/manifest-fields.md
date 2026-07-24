# manifest-fields — the manifest.json + prompts.md contract

The `manifest.json` in each `Posts/<ISO-week>/` folder is the
machine-readable source of truth the **publishing** step reads. The
`scaffold_week.py` script writes the skeleton; this skill fills the creative
fields. Keep it valid JSON.

## Top level
| Field | Written by | Meaning |
|---|---|---|
| `week` | script | ISO week label, e.g. `2026-W30` |
| `timezone` | script | IANA tz for all `time_local` values (default `America/Chicago`) |
| `generated_at` | script | timestamp of the scaffold run |
| `posts` | script + skill | array of 21 post objects |

## Each post object
| Field | Written by | Notes |
|---|---|---|
| `id` | script | `<date>-slotN`, e.g. `2026-07-20-slot1` |
| `date` | script | `YYYY-MM-DD` |
| `time_local` | script | `08:00` / `12:30` / `19:00` |
| `format` | script | `F1-buddys-list` \| `F2-guess-the-calories` \| `F3-i-was-wrong` \| `F4-one-snap-demo` |
| `title` | **skill** | unique within the week; the post's angle |
| `slides_dir` | script | `<id>/slides` — where Connor drops `01.png…` |
| `slides_expected` | **skill** | number of slides you wrote (≥ 5, ≤ 9) |
| `caption` | **skill** | per the caption formula; within platform limits |
| `hashtags` | **skill** | 3–5, from the pools; always include `#bitebuddy` |
| `pinned_comment` | **skill** | one swipe-bait / reply-bait line |
| `tags` | **skill** | `{hook_type, topic, cover_style}` — the creative attributes the `carousel-optimize` loop correlates performance against. Reuse consistent values week to week. |
| `tiktok_sound` | script | leave `SET_AT_POST_TIME` |
| `platforms` | script | `["instagram","tiktok","facebook","youtube"]` |
| `cta` | script | App Store CTA line (edit only if needed) |
| `status` | script→publish | `draft` → `images-ready` → `verified` → `scheduled` → `posted` \| `failed` |
| `results` | publish | filled at publish time with each platform's post ID/URL |

The skill leaves `status: draft`. The publishing step advances it (to
`images-ready` once PNGs are present, `verified` after the Sunday-night check,
`scheduled`/`posted` as it fires).

## Week-level package files (in `Posts/<week>/`)
Besides the 21 post folders + `manifest.json`, each week ships:
- `README.md` — human overview + Connor's steps.
- `CHATGPT-GENERATION-GUIDE.md` — the self-contained file handed to ChatGPT: global
  rules (constant **1080×1350**, one post at a time, reply `done`), a **"Uploading to
  GitHub"** section (ChatGPT commits each PNG to `…/<post-id>/slides/NN.png` via the
  Contents API; token pasted at runtime, never committed), + **all 21 posts' slide
  prompts inlined**.
- `assets/today-home-hero.png` — the one screenshot ChatGPT uploads (CTA slide).

## prompts.md (one per post folder — a self-contained generation package)
Human-facing, for Connor / ChatGPT. A header block states the output contract, then
one `## Slide NN` section per slide with a paste-ready prompt (see `prompt-recipes.md`):
```
# Generation package — 2026-07-20-slot1 (F1-buddys-list)
# Post 1 of 21 — Week 2026-W30

**Upload target:** commit 01.png … 07.png into
Posts/2026-W30/2026-07-20-slot1/slides/ on branch main.
**Every image size:** exactly 1080 x 1350 pixels (4:5 vertical).
**App UI appears on the FINAL slide only** — uses the uploaded today-home-hero.png.

## Slide 01 — COVER
On-slide text: "…"
(full prompt — educational cover)

## Slide 07 — CTA — DOWNLOAD (only app slide)
On-slide text: "[topic CTA] · Download BiteBuddy — free on the App Store"
(full CTA prompt using today-home-hero.png)
```
The number of `## Slide` sections MUST equal `slides_expected`, the **last** section
is always the standard download CTA, and only that CTA section may reference app UI.
Slides are saved by Connor as `01.png, 02.png, …` matching these sections in order.

## Validation quick-checks
```bash
# valid JSON + 21 posts
python3 -c "import json;d=json.load(open('Posts/<week>/manifest.json'));\
assert len(d['posts'])==21; print('ok')"

# every post has the creative fields filled
python3 -c "import json;d=json.load(open('Posts/<week>/manifest.json'));\
bad=[p['id'] for p in d['posts'] if not(p['title'] and p['caption'] and 3<=len(p['hashtags'])<=5 and p['slides_expected']>=5)];\
print('incomplete:',bad or 'none')"
```
