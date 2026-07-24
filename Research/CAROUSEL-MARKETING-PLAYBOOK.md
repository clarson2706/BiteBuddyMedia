# Carousel / Slideshow Marketing Playbook — BiteBuddy

*Compiled July 2026. The static-image companion to
`Research/VIDEO-MARKETING-RESEARCH.md`. Where that doc covers 15s
video, this one covers **TikTok Photo Mode + Instagram carousels** — swipeable
static posts. This is the fastest, cheapest, highest-leverage channel we have.*

App Store: https://apps.apple.com/us/app/bitebuddy-ai-calorie-scanner/id6787834752

North star: **downloads.** Every carousel ends on the same door — the App Store.

---

## Why carousels are the #1 near-zero-cost channel for us

Carousels are winning the 2026 algorithm on both platforms, and they cost a
fraction of video to make (no filming, no editing, no voiceover — just images +
text in Canva). The data:

- **TikTok's own numbers:** carousels get **1.9× more likes, 2.9× more comments,
  and 2.6× more shares** than video posts. Photo Mode is currently getting
  **up to 5× the reach** of video for the same accounts.
- **Instagram:** carousels are the **highest-engagement format of any type** in
  2026 — ~**1.92% avg engagement vs 0.50% for Reels and 0.45% for static**. They
  pull **1.9× the reach of a single image** and up to **3× the engagement.**
- **The 5–7 slide sweet spot** generates **3.4× more saves and 2.1× more shares**
  than a static post.
- **Why it works mechanically:** the ranking signal is **swipe-through
  completion rate** — the carousel version of watch time. Every swipe is counted
  as dwell time, and the algorithm re-surfaces a swiped-through post to the same
  user's feed the next day (a second bite Reels don't get).

This is exactly Cal AI's cheat code. Their breakout format wasn't polished video
— it was **"images + bait text as a slideshow," near-zero production cost, that
consistently went viral** (see the video research doc). We are cloning that
format with one asset they don't have: **Buddy.**

---

## The format you saw (the "golf app" carousel), decoded

> *"an animated golfer talking about the top 7 things destroying your swing, and
> the last window is the app itself prompting download."*

That's a **mascot-narrated listicle carousel**, and it is the single most
repeatable, ownable format for us. Anatomy:

1. **A recurring animated character** carries every slide → instant brand
   recognition, and the character *is* the pattern-interrupt hook.
2. **A "mistake/danger" listicle** ("7 things destroying your X") → mistake-
   correction is one of the three top-performing hook types in health/fitness
   right now, because it makes the viewer anxious they're doing #4 wrong and they
   *must* keep swiping to find out.
3. **The last slide is the app** with a hard download CTA → by then the viewer
   trusts the character and wants the fix it's selling.

**We are unfairly well-positioned to run this.** BiteBuddy already ships a
purpose-built mascot with **14 consistent, effect-free poses** (see
`UI-Library/10-buddy-poses/` and `MASCOT_IMAGE_GEN_PROMPTS.md`). The
golf app had to commission an animator. We generate a pose in one prompt. **Buddy
is our golfer.**

---

## What's working right now — the evidence, by lever

### 1. The cover slide is 90% of the result
Audiences scroll **3–4 posts per second**; the cover has to win in the first
half-second. The winning cover formula (consistent across every source):

> **BOLD HEADLINE (5–8 words, biggest text on the slide)**
> **+ VISUAL PATTERN INTERRUPT (a face, high-contrast color, or a number)**
> **+ CURIOSITY GAP (a partial reveal, a surprising stat, or an open loop)**

For us the pattern-interrupt is free and unique: **Buddy's face** goes on the
cover of every post. High-contrast, expressive, un-ignorable.

### 2. The three hook types dominating health/fitness in 2026
From current top-performing fitness posts:

| Hook type | Why it works | Real example (views) | Our version |
|---|---|---|---|
| **Mistake correction** | Fear you're doing it wrong → must-swipe | single-arm lat pulldown fix — **2.4M** | "7 'healthy' foods wrecking your day" |
| **Constraint framing** | A tight, specific promise feels doable | "3 days only" split | "Track your food in 3 seconds, not 3 minutes" |
| **Identity shift** | Emotional, aspirational | "when her confidence came back" — **14.6M** | "the tracker you actually come back to" |

### 3. Food/calorie content is a native, proven carousel niche
Calorie-count carousels (e.g. "the calories in every McDonald's item,"
food-comparison charts, "guess the calories") are an established, high-reach
format on food TikTok. This is the perfect Trojan horse: give genuinely useful
calorie info slide by slide, and the final slide reveals the app that does it
automatically. **Value first, product last.**

### 4. Volume + consistency beats polish (the Cal AI law)
Cal AI posted **multiple times daily, every day, across ~12 accounts**, re-cutting
one small content library, and messaged **hundreds** of micro-influencers (not
ten) at ~$5 CPM. More posts = more shots at virality. Carousels make this
sustainable because one can be produced in **~10 minutes** in Canva.

### 5. Distribution mechanics that move reach
- **9:16 vertical, 1080×1920** for TikTok Photo Mode; **4:5, 1080×1350** for
  Instagram (never square — 4:5 takes more feed height).
- **Trending audio still matters on a carousel.** TikTok Photo Mode lets you set
  a sound; picking a trending one is a free reach multiplier. Add one every time.
- **First comment = swipe bait.** Pin a comment that teases the last slide
  ("#5 is the one everyone gets wrong") to lift completion rate.
- **Caption = a literal search snippet.** Say the keyword ("AI calorie counter,"
  "calorie tracker app") in the caption and in on-slide text — carousels get
  indexed in TikTok/IG search and keep pulling installs for months.

---

## The BiteBuddy Carousel Engine (the repeatable system)

This is the core deliverable: a **fill-in-the-blank machine** so anyone can
produce an on-brand, on-strategy carousel in minutes. It has three reusable
parts — **Copy**, **Image**, **Distribution** — plus **four post formats** that
snap onto it.

### The universal skeleton (every carousel, every time)

```
Slide 1  — COVER / HOOK          Buddy face + 5–8 word headline + curiosity gap
Slide 2  — STAKES / SETUP        "here's why this matters" — one line, one Buddy pose
Slide 3–6 — VALUE (1 idea/slide)  the list / the reveals / the proof — Buddy reacts on each
Slide 7  — TURN                  "there's a faster way…" (bridge to the app)
Slide 8  — CTA / DOWNLOAD        the app screen + "BiteBuddy — free on the App Store 👇"
```

5–8 slides total. Never fewer than 5 (kills the save/share multiplier), rarely
more than 8 (completion rate drops). One idea per slide — if a slide needs a
second sentence to explain it, it's two slides.

### Part 1 — The COPY formula (per slide)

Fill these blanks. Keep every line under ~12 words; the reader is swiping fast.

- **Cover headline** = `[number or "the"] + [charged noun] + [mistake/promise]`
  → "7 foods sabotaging your calorie deficit" · "the tracker you actually reopen"
- **Value slide** = `[bold claim, ≤6 words]` on top + `[one-line why]` below +
  Buddy's one-word reaction as a caption ("yikes.", "better.", "this one.").
- **Turn slide** = `"Doing this by hand is why you quit. Buddy does it in one
  photo."`
- **CTA slide** = `"BiteBuddy — the AI calorie counter that's happy to see you."`
  + `"Free on the App Store 👇"` + the actual App Store name so it's searchable.

**Caption bank rule (hard guardrail):** pull the product line from
`Research/VIDEO-MARKETING-RESEARCH.md`'s approved language. **No
medical or outcome claims** — never "lose X lbs," "guaranteed," "melts fat," or
anything a dietitian would flag (see `Legal/MEDICAL_AND_NUTRITION_DISCLAIMER.md`).
We sell *the feeling of momentum and a buddy who's on your side*, not a result.
**Never show the Meal Advisor** (it ships as "Coming Soon" / disabled).

### Part 2 — The IMAGE formula (per slide)

Every slide is one of three visual types. All use the **brand palette**: cream
background `#FFF8F1`, peach `#F4A261`, deep orange `#E9843A`, sage `#8FA27F`,
lavender `#C9C4F2` (Buddy's own color).

1. **Buddy slide** — a transparent-PNG pose from
   `UI-Library/10-buddy-poses/` on a solid cream/lavender card, big
   bold headline above or beside it. This is every cover + every reaction beat.
2. **App-proof slide** — a real screenshot from `UI-Library/` inside a
   phone frame, with a small Buddy pose peeking over the bezel pointing at the
   number. Used for the demo/proof and the final CTA.
3. **Info slide** — a food photo or a big number on a color card (for calorie-
   reveal formats), Buddy reacting in the corner.

**Reusable image-gen prompt (for any NEW Buddy pose you need):** take the MASTER
STYLE BLOCK from `MASCOT_IMAGE_GEN_PROMPTS.md` verbatim, append the pose line,
and keep framing identical so Buddy is consistent across every post. Do **not**
let the model draw effects (glows/sparkles/confetti) — add those in Canva. For
90% of carousels you won't generate anything new; the 14 existing poses cover it.

**Canva build:** one master template with the 8-slide skeleton, brand colors,
and a locked text style. To make a new carousel you duplicate it, drop in the
Buddy poses + screenshots, and swap the copy. ~10 minutes each once the template
exists. This is what makes 2–4 posts/day realistic for one person.

### Part 3 — The DISTRIBUTION formula (per post)

Same wrapper on every carousel:

- **Caption:** hook restated + keyword ("AI calorie counter / calorie tracker
  app") + a question to farm comments ("which one surprised you?"). 1–2 lines.
- **Hashtags:** 3–5 only. Mix one big (#caloriedeficit #weightlosstok), one
  mid (#caloriecounting #foodtracker), one niche/brand (#bitebuddy). Rotate.
- **Sound:** add a trending TikTok audio every time (free reach). On IG, a
  trending audio on the carousel does the same.
- **Pinned first comment:** tease the payoff slide to lift swipe-through.
- **Link:** App Store link in bio; final slide says "link in bio / search
  BiteBuddy on the App Store."

---

## The four post formats (snap onto the skeleton)

Rotate these so the account never looks repetitive. Each has a dedicated,
ready-to-produce template in `Carousel-Ideas/`.

| # | Format | Hook type | Best for | Template |
|---|---|---|---|---|
| **F1** | **Buddy's List** (the golf-app clone) | Mistake correction | The workhorse. Ownable, series-able. | `01-buddys-list.md` |
| **F2** | **Guess the Calories** | Curiosity / reveal | Native food-TikTok reach; huge saves | `02-guess-the-calories.md` |
| **F3** | **"I was wrong about calorie apps"** | Confession / identity | Overcomes skepticism → installs | `03-i-was-wrong.md` |
| **F4** | **One Snap, Every Macro** (screenshot demo) | Constraint / speed | Purest product proof; paid-ad ready | `04-one-snap-demo.md` |

**F1 is the hero** — it is exactly the golf-app format, it's the most ownable
(Buddy narrates), and it spins into an endless series (a new "7 things" every
week). Lead with F1 + F2.

---

## Posting schedule (aggressive, growth-max)

Goal: as many quality posts as sustainable, because volume is the Cal AI lesson.
Two tiers depending on how much you can commit.

### Tier 1 — Solo founder, sustainable (start here, week 1)
**3 carousels/day** — 1 TikTok + 1 Instagram + 1 cross-post to the other, staggered.

| Slot | Time (local) | Platform | Format that day |
|---|---|---|---|
| Morning | 8–9 AM | TikTok | rotate F1→F2→F3→F4 |
| Midday | 12–1 PM | Instagram | same carousel, re-sized 4:5 |
| Evening | 6–8 PM | TikTok (2nd acct) | a *different* format's post |

Batch-produce **a week at a time** (one Canva session, ~2 hrs → 15–21 posts),
then schedule. Rotate the 4 formats so no format repeats two days running.

### Tier 2 — Scale mode (once a format is proven, week 3+)
The Cal AI multi-account model. **6–12 posts/day across 3–5 handles**, each
handle a slightly different angle (one "food facts," one "Buddy character," one
"honest app reviews"). Re-cut the *same* small library — a winning carousel gets
reposted on every account with a fresh cover. Accounts that post 2–4×/day see
**~2.5× the follower growth** of once-daily accounts.

### The weekly rhythm
- **Mon–Fri:** full cadence (best reach days).
- **Sat/Sun:** lighter — repost the week's top performer to a second account.
- **Every Friday:** look at which cover/hook got the most swipe-throughs and
  saves; make **5–10 new cover variations of that winner** for next week (swap
  only slide 1). This is the whole optimization loop — you're A/B testing hooks,
  not rebuilding posts.

### First 30 days, concretely
- **Week 1:** ship the 4 templates below, 3 posts/day, learn what lands.
- **Week 2:** double down on the top format; start DMing micro-influencers
  (health/food/college niches) — message **50+**, not 5, offer free Pro + a
  small flat fee for a native "apps I use" carousel or Photo Mode post.
- **Week 3–4:** spin up 2 more accounts, go to 6+ posts/day on proven formats.
  When organic plateaus, put spend behind the single best-performing carousel as
  a **Spark Ad** (amplify the organic post, don't make a new "ad").

---

## Guardrails (repeat of the non-negotiables)

- **No medical/outcome claims.** No "lose X lbs," "guaranteed," "burns fat,"
  crash-diet framing, or anything targeting disordered eating. Calorie facts are
  fine; prescriptions are not. (`Legal/MEDICAL_AND_NUTRITION_DISCLAIMER.md`.)
- **Estimates are informational** — if a screenshot shows a number, it's an AI
  estimate the user reviews before saving. Keep that honesty; it builds trust.
- **Never feature the Meal Advisor** — it's "Coming Soon" and disabled.
- **Real screenshots only** for app-proof slides, pulled from
  `UI-Library/`. No mocked-up numbers.
- **Buddy stays consistent** — always the 14-pose set / MASTER STYLE BLOCK, same
  framing, no drawn effects (composite effects in Canva).

---

## Success metrics to watch (per post)
- **Swipe-through completion rate** (primary — the ranking signal).
- **Saves + shares** (carousels' superpower; saves signal high install intent).
- **Profile visits → App Store taps** (the actual funnel to a download).
- **Comments asking "what app is this?"** — the Cal AI tell that a post is
  converting; answer every one with the name + "free on the App Store."

---

## Sources
- [ReelBase — TikTok Photo Mode Algorithm: 5× Reach in 2026](https://reelbase.io/blog/tiktok-photo-mode-algorithm-explained)
- [AttentionClaw — TikTok Slideshow Strategy for Apps](https://www.attentionclaw.com/blog/tiktok-slideshow-strategy-for-apps)
- [Socialinsider — How to Use TikTok Carousels for Storytelling](https://www.socialinsider.io/blog/tiktok-carousel/)
- [TrueFuture Media — Instagram Carousel Strategy 2026](https://www.truefuturemedia.com/articles/instagram-carousel-strategy-2026)
- [Resont — Best Hooks for Instagram Carousels](https://resont.com/blog/top-instagram-carousel-hooks/)
- [Marketing Agent — Instagram Carousel Strategy 2026: Algorithm Demands Swipes](https://marketingagent.blog/2026/01/03/mastering-instagram-carousel-strategy-in-2026-the-algorithm-demands-swipes-not-just-scrolls/)
- [Krumzi — 15 Instagram Carousel Ideas (Templates) 2026](https://www.krumzi.com/blog/15-instagram-carousel-ideas-that-actually-drive-engagement-in-2026)
- [Draper — TikTok Fitness Hooks 2026](https://draper.chat/blog/tiktok-fitness-hooks-2026)
- [Stormy AI — Cal AI TikTok Marketing Playbook 2026](https://stormy.ai/blog/cal-ai-tiktok-marketing-playbook-2026)
- [PostWaffle — 10 TikTok Carousel Tips](https://www.postwaffle.com/blog/tiktok-carousel-tips-for-beginners)
- [SociallyIn — How Often to Post on TikTok in 2026](https://sociallyin.com/resources/how-often-should-you-post-on-tiktok/)
- [JoinBrands — How Often to Post on TikTok in 2026 (Data-Backed)](https://joinbrands.com/blog/how-often-to-post-on-tiktok/)
