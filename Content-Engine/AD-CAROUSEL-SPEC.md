# TikTok Paid Carousel Ad — Template Spec

*Build brief for the `ad-carousel` recipe. Distinct from the organic weekly loop: these are
paid TikTok in-feed carousel ads for app installs, not account content. Written 2026-08-16.*

---

## 1. Goal

Five paid TikTok carousel ads driving App Store installs, all built from **one template** so
new ads are a swap of 7 background images and 7 strings. This spec covers the template and
carousel #1. Copy for carousels 2–5 comes after the template renders.

Campaign shape Connor is running: new campaign, one ad group, ~5 creatives, **$65/day**,
iOS 14 dedicated (SKAdNetwork) turned on — it was previously off, so clicks could not convert.

---

## 2. Ad-format facts that constrain the design

Verified against TikTok Ads Manager docs, 2026-08-16.

| Fact | Consequence |
|---|---|
| Carousel accepts 2–35 images; vertical spec is **720×1280**, JPG/PNG, **≤100KB suggested** per image | Build at 1080×1920, export JPEG ~q80, keep every file under 100KB |
| **One ad caption and one CTA button for the whole carousel** — not per slide | The caption is an extra creative slot; it must carry hook + CTA on its own |
| Viewer **swipes manually** (not auto-advancing like video) | Open-loop / swipe-forward mechanics genuinely matter |
| Engagement drops after ~7 cards | 7 slides is the ceiling. Value must land by slide 3 |
| iOS14 dedicated campaigns: SKAN 3.0 postbacks delayed up to 72h, SKAN 4.0 up to 4 days | Do not judge creative before day 4–5 |
| iOS14 dedicated quota: 15 campaigns × 5 ad groups per SKAN app | Plenty of headroom |

Sources: [carousel specs](https://ads.tiktok.com/help/article/specifications-for-carousel-ads) ·
[about carousel ads](https://ads.tiktok.com/help/article/carousel-ads?lang=en) ·
[iOS 14.5+ campaign limits](https://ads.tiktok.com/help/article/in-product-experience-ios14?lang=en) ·
[iOS 14 bidding](https://ads.tiktok.com/help/article/bidding-optimization-considerations-ios14?lang=en)

**Media-buying note:** 5 creatives in one $65/day ad group is ~$13/day each — TikTok will
starve most of them before SKAN even reports. Recommend running 3 and holding 2 for round two.

---

## 3. The template — three layers

Layers 2 and 3 never move. Only layer 1 and the strings change between ads. This is what makes
it repeatable.

1. **ART** — full-bleed background image, one per slide. Same illustration style across all 7
   so the set reads as one story.
2. **SCRIM** — fixed cream gradient, top-down over the headline zone and bottom-up over the
   footer zone. This is the whole trick: it guarantees text legibility over *any* background
   dropped in, so art can be swapped without redesigning the layout.
3. **TEXT + FURNITURE** — fixed slots at fixed coordinates: `HEADLINE` (top, max 2 lines),
   `SUB` (1 line), `TICKER` (bottom-right), progress dots, and the phone-silhouette anchor on
   slide 7.

Safe margins 90px all sides. Nothing critical in the bottom 180px (TikTok UI overlays).

---

## 4. Slide roles

| # | File | Role | Note |
|---|---|---|---|
| 1 | `bg-01-hook` | **Hook** — specific contrarian claim or true number | Specific and visual only; generic myth-busting is burned in 2026 |
| 2 | `bg-02-proof` | **Proof / turn** — the receipt for slide 1 | Payoff starts here |
| 3 | `bg-03-value-a` | Value | Densest real value |
| 4 | `bg-04-value-b` | Value | |
| 5 | `bg-05-value-c` | Value / screenshot-me | |
| 6 | `bg-06-bridge` | **Bridge** — "tracking this by hand is why you quit" → product enters | Do not make slide 7 do the selling. This is where carousel ads usually fail |
| 7 | `bg-07-cta` | **CTA** — real Today dashboard in a phone silhouette + Buddy + App Store line | |

**Swipe device:** pick one per carousel and wire it as a fixed template slot — a running ticker
(bottom-right, changes each slide), a 5→1 countdown with #1 teased on the cover, or a
question-on-N / answer-on-N+1 delay. Progress dots always on, so viewers know there is more.

---

## 5. The backgrounds

Seven ChatGPT-generated illustrated backgrounds, already approved. Same recurring character
(late-20s, sage sweater, cream trousers) on slides 2–7; slide 1 is a hero food bowl, no character.
Warm flat vector, grain texture, brand palette.

**Source:** Google Drive folder `bitebuddy-ad-bg-01` (owner clarson2706@gmail.com).
**Destination:** `Content-Engine/ad-backgrounds/carousel-01/`

Six files already carry their final names. The seventh arrived as
`ChatGPT Image Aug 16, 2026, 03_33_20 PM.png` — that is the **corrected bg-02** (the first
version had the food wall intruding into the headline zone; the re-roll pushed it below the
halfway line). **Rename it to `bg-02-proof.png`** and confirm visually: top ~55% should be
empty cream, food wall in the lower half, character seen from behind.

### Required processing

- **Source images are 1024×1536 (2:3). Do NOT crop the sides to reach 9:16** — that clips the
  outer bowls in `bg-05` and the edge items in `bg-02`. Instead **extend the canvas vertically**
  with matched cream (~240px top, ~60px bottom) and scale to **1080×1920**. Nothing is lost and
  every slide gains headline room.
- **`bg-02-proof` needs extra bottom padding.** The character's feet land at ~95% of the frame
  and would collide with the progress dots and TikTok's own UI overlay.
- Palette drifted warm during generation — almost no deep orange `#E9843A` survived except the
  halo on slide 1, and lavender only appears incidentally. Not worth re-rolling; put the brand
  accents into the text/furniture layer where they read as intentional.

---

## 6. Brand tokens

| Token | Hex | Use |
|---|---|---|
| Cream | `#FFF8F1` | Background, scrim |
| Peach | `#F4A261` | Accent shapes, chips |
| Deep orange | `#E9843A` | Headlines, key numbers, CTA |
| Sage | `#8FA27F` | Secondary accents |
| Lavender | `#C9C4F2` | Buddy's color, playful accents |
| Charcoal | `#3A3A3A` | Body text |

Typography per `Content-Engine/DESIGN-SYSTEM.md`: one bold rounded sans for headlines, clean
sans for body. Headline is always the biggest element on the slide.

---

## 7. What to build

Extend `Content-Engine/render_slides.py` with an `ad-carousel` recipe. It already has what is
needed: brand constants, `fit_text()`, `load_pose()`, and `phone_mock()` which crops
`UI-Library/02-today-home/01-today-home.png` to the dashboard hero.

Changes required:

1. The existing renderer is hardcoded to `W, H = 1080, 1350`. The ad recipe needs **1080×1920** —
   parameterize rather than fork the file.
2. Add a background-plate loader: read from `ad-backgrounds/<set>/`, vertical-extend, scale.
3. Add the scrim compositor.
4. Add the ad slide renderer: scrim + headline + sub + ticker + progress dots.
5. Add the slide-7 CTA compositor: phone silhouette with the real Today screenshot, Buddy from
   `Brand-Assets/buddy-poses/transparent/`, CTA line, App Store line.
6. Export JPEG quality-stepped down until each file is **under 100KB**.
7. Drive it from one CSV/JSON row per carousel: background-set path + 7 headline strings +
   7 sub strings + ticker values + the single ad caption.

**Deliverable:** carousel #1 rendered end to end, all 7 JPEGs under 100KB, so the template can be
eyeballed before writing five sets of copy.

---

## 8. Hard guardrails

From `CLAUDE.md` in this repo and `BiteBuddyMVP/CLAUDE.md`. Non-negotiable.

- **Real screenshots only** for app UI, from `UI-Library/`. Never redraw, mock, or invent UI or
  numbers.
- **Buddy comes from the 13 canonical PNGs** in `Brand-Assets/buddy-poses/transparent/`. Never
  generate Buddy with an image model — that is what caused character drift before.
- **Never feature the Meal Advisor.** It ships disabled as a "Coming Soon" tile.
- **No medical or outcome claims.** No "lose X lbs", "guaranteed", "burns fat", no crash-diet or
  disordered-eating framing. Calorie facts are fine; health prescriptions are not.
- **App numbers are AI estimates the user reviews.** Keep that honest. Claim consistency, never
  scan precision.
- **No em dashes in any outbound copy** — captions included. House rule.
- The App Store CTA must use the canonical search term from
  `BiteBuddyMVP/APP_STORE_METADATA.md`. Do not paraphrase it.
- Illustrated food in this ad style is fine; AI-rendered *photorealistic* food is not — it is the
  fastest slop tell and a conversion risk.

## 9. Approval gates

Branch `claude/bitebuddy-carousel-ads-wep3if`, draft PR, never commit to `main`. The weekly
loop's no-per-post-approval authorization covers **organic carousels only** — it does not cover
paid ads. Anything that spends money is Connor's call, every time. Render and show; do not
upload to TikTok Ads Manager.
