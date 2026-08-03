# TikTok Ads Manager — BiteBuddy install campaign ($20/day)

Written 2026-08-03 for the first paid test: four vertical VO videos driving installs of
the BiteBuddy iOS app. This is a setup runbook for Connor, who clicks every button
himself. Nothing in this repo touches the ad account, and nothing here is authorization
to spend — money stays a per-decision gate (`CLAUDE.md` → Approval gates).

App Store listing: https://apps.apple.com/us/app/bitebuddy-ai-calorie-scanner/id6787834752
App ID: `6787834752`

---

## 0. The correction that comes before everything

**Sales → App is the wrong branch for installs.** TikTok's Sales objective sells
*products* through a website, a TikTok Shop, or an app you already own on the device. Its
app side optimizes for in-app purchase / subscription events (AEO and value-based
optimization) against people who **already have BiteBuddy installed**. With effectively
zero users, that audience is approximately empty and the campaign will either fail to
deliver or burn budget finding the handful of installs that exist.

The objective that drives new installs is **App Promotion → App Install**.

Back out of Sales and re-pick the objective.

---

## 1. The blocker to resolve first: is the app measurable?

Both App Promotion and Sales → App require BiteBuddy to be **registered as an app asset**
inside TikTok Ads Manager, which requires one of:

- a **Mobile Measurement Partner** SDK in the app (AppsFlyer, Adjust, Branch, Singular,
  Tenjin, Kochava), or
- the **TikTok Business SDK** integrated directly.

Nothing in this repo indicates either is in the app. App code lives in `BiteBuddyMVP` and
was not visible from the session that wrote this doc. **Check that first** — search the
iOS project for `AppsFlyer`, `Adjust`, `Branch`, `Tenjin`, `TikTokBusinessSDK`.

### Path A — an MMP or the TikTok SDK is already in the shipped build
Use **App Promotion → App Install**. Best case: real install attribution, and TikTok can
actually optimize toward installs.

### Path B — no MMP (assume this until proven otherwise)
TikTok's own guidance for advertisers without an MMP is to run the **Traffic** objective
and measure clicks. Adding an MMP means an app code change plus an App Store release, so
it is a multi-week detour, not a today decision.

**At $20/day, Path B is the right call even if Path A is available.** See §3.

Run Path B now. If it produces signal worth scaling, adding an MMP becomes an easy yes,
and that is the moment to switch to App Promotion.

---

## 2. Structure: one campaign, one ad group, four ads

```
Campaign: BB-APP-2026-08 | Traffic (or App Promotion)   budget: No limit
└── Ad group: BB-AG1-US-iOS-broad                        budget: $20.00/day
    ├── Ad: BB-A1-darkhype-1
    ├── Ad: BB-A2-darkhype-2
    ├── Ad: BB-A3-food-has-a-witness
    └── Ad: BB-A4-every-other-tracker
```

**Never split $20 across multiple ad groups.** Each ad group learns independently; two
ad groups at $10 each is two campaigns that both fail to learn. Creative comparison
happens at the *ad* level inside one ad group, which is exactly what four videos want.

### The budget gotcha that will stop you
TikTok's minimum daily budget is **$50 at the campaign level** and **$20 at the ad group
level**. You cannot type $20 into the campaign budget field. So:

- Campaign budget → **No limit** (leave Campaign Budget Optimization **OFF**)
- Ad group daily budget → **$20.00**

The ad group is what caps your spend. That is the correct setup, not a workaround.

---

## 3. Why Traffic beats App Install at this budget

TikTok's install optimization needs roughly **50 conversions per ad group per week** to
exit the learning phase. Health-and-fitness iOS installs on TikTok run roughly $3–6 CPI,
so $20/day = $140/week = **~25–45 installs/week**. That sits at or below the threshold —
the ad group would spend the whole test semi-permanently in learning, and the numbers you
read at the end would be noise.

Traffic optimizes for clicks, which arrive at 50–200/day at this budget. That is enough
volume to get a genuine read on **which of the four hooks people respond to**, which is
the actual question a first $600 answers. Install-cost optimization is a scaling problem,
and scaling comes after a winning hook exists.

---

## 4. Measurement, wired before the first dollar (non-negotiable — `CLAUDE.md` rule 1)

Without an MMP, TikTok will report clicks and stop there. Apple will report the rest, for
free, if the destination URL carries campaign parameters.

**Destination URL for every ad:**

```
https://apps.apple.com/us/app/bitebuddy-ai-calorie-scanner/id6787834752?pt=PROVIDER_ID&ct=tt_ads_aug26&mt=8
```

- `pt` — your App Store Connect provider ID (App Store Connect → **Users and Access**).
- `ct` — campaign token, max 40 chars, no leading/trailing space. **Use a different `ct`
  per ad** so Apple's numbers separate the four hooks:
  `tt_darkhype1`, `tt_darkhype2`, `tt_witness`, `tt_everyother`.
- `mt=8` — the App Store media type.

Read it in **App Store Connect → Analytics → Acquisition → Campaigns**. It reports
impressions, product page views, **first-time downloads**, and sales per token. Note
Apple's floor: a token shows nothing until it has produced first-time downloads from at
least **five** distinct users. At ~$20/day that can take a few days per token — expect
the first useful read around day 4–5, not day 1.

This gives the funnel end to end with no code change:

```
TikTok impressions → TikTok clicks → Apple product page views → Apple downloads
```

The drop between TikTok clicks and Apple product page views is the honest measure of how
many "clicks" were real intent. The drop between page views and downloads is a **listing
problem, not an ad problem** — if the ads send 400 page views and convert 12, the
screenshots and subtitle are the thing to fix, not the creative.

Record one line per week in `Analytics/installs.jsonl` (schema in `Analytics/README.md`),
plus a per-ad row in the results table at the bottom of this doc.

---

## 5. Campaign level — every setting

| Field | Value | Why |
|---|---|---|
| Objective | **Traffic** (Path B) or **App Promotion → App Install** (Path A) | §1 |
| Campaign name | `BB-APP-2026-08` | matches the ad naming convention below |
| Smart+ campaign | **OFF** | Smart+ hands targeting, bidding and creative mixing to TikTok's model. It needs volume this budget will not produce, and it hides which creative won |
| Split test (A/B) | **OFF** | four creatives in one ad group already answers the creative question; split test would fragment the $20 |
| Campaign budget optimization | **OFF** | with one ad group it does nothing, and it blocks the ad-group budget field |
| Campaign budget | **No limit** | see the budget gotcha in §2 |

---

## 6. Ad group level — every setting

### Destination / promotion type
- Path B: **Website** → paste the campaign link from §4.
- Path A: select the BiteBuddy app asset, download link auto-fills.

### Placements — do not leave on Automatic
| Placement | Set to | Why |
|---|---|---|
| TikTok | **ON** | the only placement that matters |
| TikTok Search / Search results | **ON** | search intent converts well, and BiteBuddy's whole CTA strategy is a search term (`Search 'BiteBuddy: Ai calorie scanner'`) |
| Pangle | **OFF** | third-party app inventory. Cheap clicks, near-zero intent. It will eat a $20/day budget and make the campaign look better than it is |
| Global App Bundle / News Feed App | **OFF** | same reason |

### Ad details toggles
| Setting | Value |
|---|---|
| User comment | **ON** — comments on ads are free objection-handling and social proof; the account already replies to people |
| Video download | OFF |
| Video sharing | ON |
| Automated Creative Optimization (ACO) / Smart Creative | **OFF** — ACO recombines assets and destroys the per-hook read this test exists to produce |

### Targeting
| Setting | Value | Why |
|---|---|---|
| Location | **United States** only | matches `PRIMARY_MARKET` and the App Store link's `/us/` storefront |
| Age | **18+**, recommend **18–44** | TikTok's weight-management ad policy prohibits targeting minors, and every persona in `Research/TARGET-USER-PROFILES.md` is adult. 18–44 covers P1, P2, P3, P5, P7, P8 |
| Gender | All | P3 and P5 pull opposite directions; let delivery sort it |
| Language | English | |
| Interests & behaviors | **leave empty** | at $20/day, layered interests starve delivery. TikTok's content graph finds food-tracking intent from the creative faster than a keyword list does |
| Custom / lookalike audiences | none | no seed data exists yet |
| **Device → Operating system** | **iOS only** | **the single most expensive mistake available here.** Default targeting serves Android users an ad for an iOS-only app. Set this or throw away roughly half the budget |
| Device → OS version | leave default, or iOS 15+ | |
| Device → Connection type / price | leave default | |
| Targeting expansion | **ON** | gives the model room to escape a too-narrow start |

### Budget & schedule
| Setting | Value |
|---|---|
| Budget | **Daily**, `$20.00` |
| Schedule | **Run continuously**, start tomorrow at 00:00 so day 1 is a full day |
| Dayparting | **All day** — splitting $20 across time blocks fragments delivery below the learning threshold |

### Bidding & optimization
| Setting | Path B (Traffic) | Path A (App Install) |
|---|---|---|
| Optimization goal | **Click** | **Install** |
| Bid strategy | **Maximum Delivery** (no bid cap) | **Maximum Delivery** |
| Billing event | CPC | oCPM |
| Attribution window | n/a | leave default (7-day click / 1-day view) |

Do not set a bid cap or cost cap on the first run. A cap on a cold ad group at $20/day
usually results in near-zero delivery, and then there is nothing to learn from.

---

## 7. Ad level — four ads, one per video

All four uploads are **1080×1920, H.264/AAC, 10.1–12.5s** — inside spec, no re-encode
needed. TikTok's minimum is 5s; these sit in the short band, which is fine for a hook
test but means every one of them lives or dies on the first 1.5 seconds.

| Ad name | Source file | Duration |
|---|---|---|
| `BB-A1-darkhype-1` | `Dark_hype_TT_VO.mp4` | 10.1s |
| `BB-A2-darkhype-2` | `Dark_Hype_2_TT_VO.mp4` | 11.2s |
| `BB-A3-food-has-a-witness` | `YOUR_FOOD_HAS_A_WITNESS_TT_VO.mp4` | 10.1s |
| `BB-A4-every-other-tracker` | `EVERY_OTHER_TRACKER_TT_VO.mp4` | 12.5s |

Keep the names literal. They are the join key between TikTok's report, the `ct` tokens in
App Store Connect, and this doc's results table.

### Per-ad settings
| Field | Value |
|---|---|
| Ad format | **Spark Ad** if the video is (or can be) a post on the BiteBuddy TikTok account; otherwise Non-Spark |
| Identity | the BiteBuddy TikTok account, not a generic "custom identity" |
| Display name / avatar | BiteBuddy + Buddy avatar from `Brand-Assets/buddy-poses/` |
| Ad text | ≤100 characters. **No em dashes** (house rule, `CLAUDE.md`) |
| Call to action | **Download** (or *Install Now* / *Get App*). Do not use Smart CTA — it varies the button and muddies the read |
| Destination | the per-ad `ct` campaign link from §4 |

### Spark vs non-Spark
Spark Ads run through the real account, so likes, comments, follows, and profile visits
accrue to BiteBuddy permanently, and the ad reads as a post rather than an ad — which
consistently outperforms for app installs. The cost: the video has to exist as a post.

The tension to be aware of: `CLAUDE.md` caps TikTok at **3 posts/day (08:00 / 13:00 /
19:00)**, and five simultaneous posts on 22 July 2026 is the suspected cause of the
current Instagram throttle. **Do not dump four videos onto the account at once to enable
Spark.** Either stagger them into the 13:00 flex slot across four days (the flex slot is
TikTok-only, and a video there *replaces* the carousel rather than adding a fourth post),
or run non-Spark for this test.

### Before you upload: check the creative against the guardrails
The ad review queue and `CLAUDE.md` want the same things. Confirm for each video:
- No weight-loss outcome claims, no "lose X lbs", no before/after framing, no
  crash-diet or disordered-eating implication. TikTok's weight-management policy is
  enforced tightly and a rejection can flag the ad account, not just the ad.
- No Meal Advisor anywhere (it ships disabled).
- Any app UI on screen is a real screenshot, not a mock.
- "Dark hype" framing reads as intensity, not shame. Shame-adjacent copy fails both the
  brand guardrail and TikTok review.

First-time ads clear review in roughly 24 hours. Submit the day before you want spend to
start.

---

## 8. What to expect, and the decision rules

At $20/day in the US, iOS-only, expect roughly **$0.40–$1.20 CPC**, so ~17–50 clicks/day,
and single-digit daily installs. Two things follow:

- **Do not touch anything for the first 3 days.** Every edit to a live ad group restarts
  learning. This is the hardest rule to keep and the most expensive one to break.
- **Judge on 7 days, not 3.** Under ~2,000 impressions per ad, differences between the
  four are noise.

### Day 3 — one check, no edits
Confirm delivery is happening at all: spend near $20/day, impressions accumulating,
placements showing TikTok rather than Pangle. If spend is under ~$5/day, the ad group is
starved — the usual cause is a leftover bid cap or over-narrow targeting.

### Day 7 — the first real decision
Rank the four ads on **click-through rate** first and **cost per App Store product page
view** second (Apple's number, not TikTok's).

- Pause any ad below **0.5% CTR**. It is not a hook.
- Keep the top 2. Let the winner take the freed budget.
- If the whole ad group is under 0.5% CTR, the problem is the creative concept, not the
  settings. Go back to `Research/HOOK-INTELLIGENCE-2026.md` and cut new openers.
- If CTR is healthy but Apple shows few product page views, the clicks are accidental —
  usually a Pangle placement that got left on.
- If page views are healthy but downloads are not, **the ads worked and the listing did
  not.** That is an ASO job, not an ads job.

### Day 14 — scale or stop
Scaling rule: raise the daily budget by no more than **20–30% every 2–3 days**. Larger
jumps reset learning. If after $280 there is no hook clearing 0.5% CTR and no measurable
lift in App Store page views, stop and put the money into the creator engine
(`Outreach/DM-PLAYBOOK.md`), which costs $0 upfront.

---

## 9. Results log — fill this in

| Date | Ad | Spend | Impr | Clicks | CTR | CPC | ASC page views | ASC downloads |
|---|---|---|---|---|---|---|---|---|
| | `BB-A1-darkhype-1` | | | | | | | |
| | `BB-A2-darkhype-2` | | | | | | | |
| | `BB-A3-food-has-a-witness` | | | | | | | |
| | `BB-A4-every-other-tracker` | | | | | | | |

Weekly App Store Connect totals go in `Analytics/installs.jsonl` as usual. The paid
numbers must stay separable from organic there, otherwise the weekly loop will credit
paid installs to carousels.

---

## Sources

- [About the App Promotion Objective](https://ads.tiktok.com/help/article/what-is-app-promotion-objective)
- [Supported ad group settings for App Promotion](https://ads.tiktok.com/help/article/new-app-promotion-advertising-objective)
- [About the Sales advertising objective](https://ads.tiktok.com/help/article/sales-advertising-objective-tiktok?lang=en)
- [About Mobile Measurement Partner Tracking](https://ads.tiktok.com/help/article/mobile-measurement-partner-mmp-tracking?lang=en)
- [About iOS 14.5+ dedicated campaign limits](https://ads.tiktok.com/help/article/in-product-experience-ios14?lang=en)
- [Apple — Campaign links, App Store Connect Analytics](https://developer.apple.com/help/app-store-connect-analytics/acquisition/campaign-links/)
- [TikTok minimum daily budget benchmarks 2026](https://www.stackmatix.com/blog/tiktok-ads-minimum-daily-budget-2026)
