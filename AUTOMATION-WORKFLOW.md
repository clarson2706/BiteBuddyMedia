# BiteBuddy — Auto-Posting Workflow (weekly operating rhythm)

The repeatable weekly system for producing and auto-publishing carousels across
**Instagram, TikTok, Facebook, and YouTube**. This is the source of truth for who
does what, when, and in what format.

Companion docs: `Research/CAROUSEL-MARKETING-PLAYBOOK.md` (strategy),
`Carousel-Ideas/` (the post templates), `UI-Library/` (screenshots + Buddy poses).

---

## Locked decisions

- **Posting engine: Upload-Post** — exposes a Claude **MCP connector** and posts
  to IG + TikTok + FB + YouTube via official APIs. Free tier = 10 uploads/mo
  (testing only); the real cadence (~360 uploads/mo) needs a paid plan (~$24/mo,
  unlimited posts / 5 accounts). Connor connects it in claude.ai connector
  settings + links the 4 accounts.
- **Images:** **Connor generates the slide images in ChatGPT** and drops them in
  the repo. **Claude does NOT generate images** (no Higgsfield / no AI image-gen).
- **Time slots (locked):** 8:00 AM / 12:30 PM / 7:00 PM, timezone
  **America/Chicago** (adjust in the manifest if needed).
- **YouTube (locked): Option A** — carousels become an ffmpeg slideshow Short.
- **Volume (locked): no trim** — 3 unique carousels/day, 21/week.
- **Copy, prompts, structure, manifest, scheduling, publishing:** Claude. The
  Sunday generation step is packaged as the **`carousel-week` skill** (see below)
  so a Routine can run it hands-off.

---

## Roles at a glance

| | **Connor** | **Claude** |
|---|---|---|
| Sunday AM | — | Generate all copy + ChatGPT image prompts + captions/hashtags/sounds; build the week's post folders + `manifest.json` |
| Sunday daytime | Generate images in ChatGPT, drop PNGs into each post's `slides/` folder; say "images are in" | — |
| Sunday night | — | Run the readiness check; flag/fix any gaps; arm the week's posting schedule |
| Mon–Sun | — | Auto-publish 3 posts/day to all 4 platforms at optimal times; log results |

---

## The weekly timeline

> **Sunday morning is a two-step pipeline: `carousel-optimize` → `carousel-week`.**
> `carousel-optimize` (`.claude/skills/carousel-optimize/`) runs FIRST — it pulls
> last weeks' performance, updates `Analytics/`, and writes the
> next-week directives. Then `carousel-week` (`.claude/skills/carousel-week/`)
> reads those directives and executes step ① end-to-end: scaffold → fill 21 posts
> → validate → commit/push → ping Connor. Neither publishes or generates images.
> (Both want the Upload-Post connector in the session for the analytics pull; a
> connector-bearing Sunday-AM Routine created from the claude.ai Routines UI gets
> the full loop, otherwise the optimize step analyzes existing history only.)
>
> **Publishing (steps ③–④) runs via the `carousel-publish` skill**
> (`.claude/skills/carousel-publish/`). A Sunday-night Routine fires it once
> images are in: readiness check → build each YouTube Short → schedule every
> READY post to all linked platforms via the Upload-Post MCP connector. It never
> writes copy and never generates images; with no accounts linked it stops in
> dry-run.

### ⓪ Sunday morning (first) — Claude learns from last week
Before generating, the **`carousel-publish`** analytics run + the
**`carousel-optimize`** skill pull performance for the posts already live (views,
likes, comments, shares, saves, swipe-through) via the Upload-Post analytics
tools, append them to `Analytics/performance-log.jsonl`, and write
`next-week-directives.{json,md}` — a ranked read of what's working by format /
hook / topic / cover / slot / platform / hashtag. Needs the Upload-Post connector
in the session; with none, it analyzes existing history (or, week 1, no-ops).

### ① Sunday morning — Claude generates & organizes (no images yet)
Claude reads the directives from step ⓪ and biases the week toward the winners
(extra slots to the top format/topic, re-cut the best posts, avoid the flops).
For the coming week Claude produces, per post:
- The **format** (rotating F1–F4 from `Carousel-Ideas/`) and a title.
- **Slide-by-slide copy** (the on-image text for each slide).
- **The ChatGPT image prompt for each slide** — so Connor just pastes prompts.
- **Caption, hashtags, pinned first comment, suggested TikTok sound.**
- A **post folder** with an empty `slides/` directory and a filled `manifest.json`.

Output committed to the repo and pushed. Claude pings Connor: "Week of \[date] is
staged — 21 posts, prompts inside each folder, ready for images."

### ② Sunday daytime — Connor adds images
Connor runs each slide's prompt in ChatGPT, exports the PNGs, and drops them into
that post's `slides/` folder named `01.png, 02.png, …` in swipe order. When done,
Connor tells Claude **"images are in."**

### ③ Sunday night — Claude verifies the week is ready
Claude runs the **readiness check** (below) across every post. If anything's
missing (a post short on slides, a caption over the limit, a dimension off),
Claude lists exactly what's wrong and what Connor needs to fix. When all green,
Claude arms the posting schedule for Mon–Sun.

### ④ Mon–Sun — Claude auto-posts
3 posts/day, each cross-posted to all 4 platforms, at the optimal time slots.
Claude publishes via the MCP scheduler, then updates each post's `status` and
logs the platform post IDs.

---

## Posting cadence & optimal times

**3 posts/day, every day, cross-posted to all 4 platforms.** Default time slots
(local time — tuned from analytics after ~2 weeks). These map to meal times,
which is on-theme for a calorie app:

| Slot | Time (local) | Why |
|---|---|---|
| **Morning** | **8:00 AM** | breakfast / commute scroll — strong for food content |
| **Midday** | **12:30 PM** | lunch break peak |
| **Evening** | **7:00 PM** | highest overall scroll volume |

**Volume math:** 3 carousels/day × 7 = **21 carousels/week**, each to 4 platforms
= up to **84 publishes/week**. That's an aggressive image-gen load on Sunday.
**Efficiency lever (Cal AI model):** not all 21 must be wholly unique — a strong
post can be re-cut with a fresh cover slide and count as a new post. If the
Sunday image load is too heavy, we drop to ~12–15 unique/week + re-cuts.

---

## Platform matrix (important)

| Platform | Carousel auto-post | Notes |
|---|---|---|
| **Instagram** | ✅ | Image carousel (≤10). Needs a **Business/Creator** account linked to a **Facebook Page**. |
| **TikTok** | ✅ | Photo Mode carousel (2+ images) via Content Posting API. Sound set at post time. |
| **Facebook** | ✅ | Multi-image post to a Page. |
| **YouTube** | ⚠️ **No carousels** | YouTube has no carousel format. To hit "all 4," a carousel must become a **Short (slideshow video)**. See below. |

### YouTube handling (decision needed — see open items)
Two options to include YouTube without Higgsfield:
- **A) Slideshow Short:** Claude stitches the post's PNGs into a simple vertical
  slideshow `.mp4` (via `ffmpeg` — assembly, not AI generation) and posts it as a
  Short. Keeps all 4 platforms live. Automated by
  `.claude/skills/carousel-publish/scripts/build_youtube_short.py` (1080×1920,
  cream padding); if local ffmpeg is missing it emits the ffmpeg spec to run via
  Upload-Post's server-side `submit_ffmpeg_job`.
- **B) Drop YouTube from the carousel track** and reserve it for the separate
  15s **video** concepts (`Video-Ideas/`) later.

Default assumption until you say otherwise: **Option A** (ffmpeg slideshow Short).

---

## Repo structure & where to drop images

```
Posts/
  2026-W30/                      # ISO week folder
    manifest.json                # the week's machine-readable schedule (all posts)
    2026-07-20-slot1/
      slides/                    # ← Connor drops ChatGPT PNGs here: 01.png, 02.png, …
      prompts.md                 # Claude writes: one ChatGPT prompt per slide
    2026-07-20-slot2/
    2026-07-20-slot3/
    2026-07-21-slot1/
    …
```

- Slides are named **`01.png, 02.png, …`** in exact swipe order.
- One post folder = one carousel = the same deck cross-posted to all 4 platforms.

---

## `manifest.json` — the contract Claude publishes from

One array of post objects per week. Claude writes everything except the images.

```json
{
  "week": "2026-W30",
  "timezone": "America/Chicago",
  "posts": [
    {
      "id": "2026-07-20-slot1",
      "date": "2026-07-20",
      "time_local": "08:00",
      "format": "F1-buddys-list",
      "title": "7 'healthy' foods wrecking your calorie deficit",
      "slides_dir": "2026-07-20-slot1/slides",
      "slides_expected": 8,
      "caption": "4 'healthy' foods that blow your deficit … which one got you?",
      "hashtags": ["#caloriedeficit", "#caloriecounting", "#bitebuddy"],
      "pinned_comment": "the avocado toast one hurt to write 💀",
      "tiktok_sound": "SET_AT_POST_TIME",
      "platforms": ["instagram", "tiktok", "facebook", "youtube"],
      "cta": "link in bio — search BiteBuddy on the App Store",
      "status": "draft",
      "results": {}
    }
  ]
}
```

`status` lifecycle: `draft` → `images-ready` → `verified` → `scheduled` →
`posted` (or `failed`). `results` gets each platform's returned post ID/URL.

---

## Image export specs (for ChatGPT exports)

- **Universal master ratio: 4:5, `1080×1350`.** Works on IG, FB, and TikTok
  (TikTok accepts 4:5 with light letterboxing). One ratio keeps Sunday sane.
- Optional later: a **9:16 `1080×1920`** set for full-bleed TikTok if we want it.
- **PNG**, RGB, under ~8 MB each. **2–10 slides** per post (never 1 — kills the
  carousel reach multiplier). Keep text large and inside a safe margin.
- Brand palette: cream `#FFF8F1`, peach `#F4A261`, deep orange `#E9843A`, sage
  `#8FA27F`, lavender `#C9C4F2` (Buddy's color). Buddy on every cover.

---

## Sunday-night readiness check (Claude runs this)

> Automated: `python3 .claude/skills/carousel-publish/scripts/readiness_check.py`
> classifies every post READY / BLOCKED / WAITING and enforces the list below.
> `--write` advances each post's `status`. It's step 1 of the `carousel-publish`
> skill.

Per post, Claude verifies:
- [ ] `slides/` has **≥ `slides_expected`** PNGs, named `01.png…` in order.
- [ ] Every image is the right ratio/format and under size limit.
- [ ] Caption within each platform's limit; hashtags present (3–5).
- [ ] `platforms`, `date`, `time_local` set; slot doesn't collide.
- [ ] Pinned comment + (for TikTok) a sound plan present.
- [ ] Guardrails: no medical/outcome claims, no Meal Advisor, real screenshots
      only on app-proof slides.

Result: a green/red list back to Connor. All green → schedule armed for the week.

---

## Failure handling
- **Images missing Sunday night:** Claude lists exactly which posts/slots are
  short and holds those; the rest still ship.
- **A publish fails at post time:** retry with backoff; if it still fails, mark
  `status: failed`, log the error, and notify Connor — don't silently drop it.
- **A platform account disconnects:** skip that platform for the slot, post the
  others, flag the reconnect needed.

---

## Activation prerequisites (must be done before any post goes live)

1. **Connect Upload-Post** as a connector in **claude.ai connector settings**
   (Connor — Claude can't run the OAuth flow from this session).
2. **Link the 4 accounts** inside Upload-Post: IG (Business/Creator + FB Page),
   TikTok, Facebook Page, YouTube channel. Upgrade past the free tier before the
   real cadence starts (free = 10 uploads/mo).
3. ~~Confirm timezone~~ ✅ America/Chicago.
4. ~~Confirm YouTube handling~~ ✅ Option A (ffmpeg slideshow Short).

Until 1–2 are done, Claude can fully stage content but **cannot publish** — the
pipeline runs in dry-run (everything staged + verified, nothing sent live).

---

## Conversion levers (downloads → paying users)

The north star is **downloads**, but the business metric is **trial starts /
subscriptions** (RevenueCat). These levers point the same content at money:

1. **Clickable links wherever the platform allows.** IG captions can't link
   ("link in bio" only — keep the App Store link in the IG bio at all times).
   **YouTube descriptions and Facebook captions CAN** — every publish appends
   `⬇️ Download BiteBuddy free: https://apps.apple.com/us/app/bitebuddy-ai-calorie-scanner/id6787834752`
   there (see `carousel-publish` → `upload-post-mapping.md`).
2. **Search keywords in every caption.** TikTok/IG index carousels in search;
   each caption carries one natural phrase (AI calorie counter / calorie tracker
   app / calorie scanner app / food tracker app). Compounds for months.
3. **The exact App Store search line** on every CTA slide:
   `Search 'BiteBuddy: Ai calorie scanner'` (the App Store search term in BiteBuddyMVP `APP_STORE_METADATA.md`).
4. **Comment-reply SOP (daily, 5 min).** Reply to every "what app is this?"
   with the app name + "free on the App Store" — this is the highest-intent
   moment in the entire funnel (the Cal AI tell). Reply to the first ~10
   comments on each post within the hour to feed the algorithm.
5. **Number-promise integrity.** A "7 foods" cover delivers 7 items — broken
   promises tank swipe-through completion (the ranking signal) and trust. If a
   legacy deck under-delivers, the pinned comment bridges it as comment bait
   ("we only fit 4 — guess the other 3 👇").
6. **High-intent topic bias.** People struggling to *track* (logging speed,
   app-quitting, protein goals, eating out) install AND pay; generic food trivia
   earns reach but converts worse. Weight the week toward tracking-pain topics;
   keep F2 trivia as the reach engine.
7. **Winner escalation.** Every Friday: take the top post by saves+shares, cut
   5–10 new covers of it for next week. When one clearly outperforms, put small
   spend behind the *organic* post as a TikTok Spark Ad — amplify, don't remake.
8. **Weekly reality check.** Lay App Store installs + RevenueCat trial starts
   over the engagement leaderboard. If a "winner" gets reach but no installs,
   it's not a winner — optimize to installs, not applause.

---

## Guardrails (unchanged, apply to every post)
No medical/outcome claims ("lose X lbs," "guaranteed"); estimates are
informational and user-reviewed; **never feature the Meal Advisor** (Coming
Soon); real screenshots only; Buddy visually consistent (the 14-pose set). See
`Legal/MEDICAL_AND_NUTRITION_DISCLAIMER.md`.
