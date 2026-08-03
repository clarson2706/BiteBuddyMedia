# Apple Ads — Search results campaign structure

*Drafted 2026-08-03. **Not authorized. Not live.** `SPRINT-AUG25.md` lever 4 says
"$0 until earned," and the approval gates in `CLAUDE.md` make anything that spends
money Connor's call every time. This document is the draft half of draft-show-act.
Nothing here goes into Apple Ads Manager until Connor says go.*

Placement: **Search results only.** Today tab, Search tab and Product pages are
deliberately excluded — reasoning in "Why only search results" at the bottom.

---

## Read this before the tables

At the install→pay rate currently on record (~2%, from `SPRINT-AUG25.md`: 1 subscriber
/ 50 new customers), **this does not pay for itself.** The math:

| | |
|---|---|
| Health & Fitness tap→install | ~48% |
| Median search-results CPT | ~$0.92 (overall avg ~$1.40) |
| Implied CPI | **$2.50–4.00** |
| × install→pay at 2% | **$125–200 per subscriber** |
| Net revenue per sub/month | $6.79 ($7.99 less 15% Small Business commission) |
| Months of retention to break even | **18–29** |

So the campaign below is scoped as a **learning budget, not a growth channel**. What it
buys is the answer to "which query converts," at keyword granularity, faster than the
creator engine will produce one — which is exactly the *"proven install channel"* the
sprint's committed target asks for. Treat MRR from it as noise.

**The number that would change this:** at a $2.50 CPI and 6-month retention
($40.74 net LTV), paid breaks even at **~6% install→pay**. At today's 2%, it breaks
even only if CPI stays under **$0.81**. Fixing paywall/trial conversion is worth more
than any bid adjustment in this file.

Caveat on the 2%: n=1 subscriber. It could truly be 4%. It still doesn't pencil.

---

## Shared settings (apply to all three campaigns)

| Setting | Value | Why |
|---|---|---|
| Placement | Search results | the only placement in this doc |
| Countries/regions | **United States only** | pricing is USD, listing is US, keeps CPI comparable to benchmarks |
| Devices | **iPhone only** | screenshots are 6.9"/6.5"; iPad is not a target persona |
| Customer type | **New users only** | never pay to re-acquire someone who already has the app |
| Age | 18+ | app enforces 16+ contractually; personas core at 25–34 |
| Gender | All | persona skew is real but too small to exclude on |
| Ad scheduling | All day, all week | Monday-weighting is a phase-2 lever, see below |
| Creative | **Default product page** | no Custom Product Pages exist yet |
| CPA goal field | **Leave blank** | Apple's optimizer needs volume this budget won't give it |
| Search Match | **OFF everywhere** | at $15/day, automatic matching sprays budget across untracked queries |

Total daily budget: **$15/day** (~$450/month).

---

## Campaign A — Brand Defense

**Daily budget: $3/day** · Ad group `brand-exact` · Default max CPT bid **$0.50**

This one is insurance, not acquisition. Every carousel CTA in the content engine is
`Search 'BiteBuddy: Ai calorie scanner'` (canonical, per `BiteBuddyMVP/APP_STORE_METADATA.md`).
The organic engine manufactures brand searches by design. If any competitor's ad sits
above the organic result on those queries, content spend leaks. Nobody else bids on
"bitebuddy," so expected CPT lands far under the $0.50 ceiling.

Keywords — **exact match**, all at default bid:

```
bitebuddy
bite buddy
bitebuddy app
bitebuddy calorie
bitebuddy ai calorie scanner
bite buddy calorie scanner
```

Negative keywords: none.

---

## Campaign B — Competitor: Cal AI

**Daily budget: $6/day** · Ad group `calai-exact` · Default max CPT bid **$1.75**

This is the actual experiment. Cal AI proved the photo-scan market (15M+ downloads,
~$30M in 2025) and **Apple removed it from the App Store in April 2026** — a
high-volume query whose destination no longer exists. The ASO keyword field already
targets it via the `cal`+`ai` cross-combination; this buys the ad slot above it.

Keywords — **exact match**:

```
cal ai
calai
cal ai app
cal ai scanner
cal ai calorie counter
calai calorie counter
```

Negative keywords — **exact**:

```
bitebuddy
bite buddy
```

Honest risk: every other scanner app can see the same gap. If CPT comes back at $3+,
the arbitrage is already priced in and this campaign is the first to pause.

---

## Campaign C — Category: photo-scan intent

**Daily budget: $6/day** · Ad group `photo-scan-exact` · Default max CPT bid **$1.40**

One cluster, not six tests — these are phrasing variants of a single intent. Small
budgets cannot reach significance across many clusters, so concentration is the point.

Keywords — **exact match**:

```
ai calorie counter
ai calorie scanner
calorie scanner
photo calorie counter
scan food calories
calorie counter by photo
```

Negative keywords — **exact** (stops cannibalizing A and B, and keeps attribution clean):

```
bitebuddy
bite buddy
cal ai
calai
```

Negative keywords — **broad** (intent filters):

```
free
android
apk
recipe
workout
gym
water
sleep
```

`free` is the debatable one. It blocks real volume ("free calorie counter"), but at a
2% install→pay rate free-seekers are the worst possible traffic. Negating it is the
right call while the economics are underwater; revisit if conversion improves.

---

## Bidding notes

Apple runs a second-price auction — the bid is a ceiling, not the price paid. Expect
realized CPT below these numbers, especially on Campaign A.

Since **March 2026 Apple serves multiple ad slots per search query** (iOS 26.2+, all
markets). This favors a small advertiser: winning position 2 or 3 is meaningfully
cheaper than contesting position 1, and for these keyword volumes position is worth
less than presence. Do not raise bids chasing slot 1.

---

## Measurement (Rule #1: if a number isn't in a file here, it doesn't exist)

New file: **`Analytics/ads.jsonl`**, append-only, one line per keyword per week, pulled
by hand from Apple Ads → Reports. Same 10-second weekly discipline as `installs.jsonl`.

```json
{"week":"2026-W32","source":"apple-ads","campaign":"calai","ad_group":"calai-exact",
 "keyword":"cal ai","match":"exact","impressions":0,"taps":0,"ttr":null,
 "installs":0,"spend_usd":0.00,"cpt_usd":null,"cpi_usd":null,
 "captured_at":"2026-08-09T23:10:00Z"}
```

Null where Apple doesn't report it. Never zero, never fabricated — same rule as
`performance-log.jsonl`.

This is the whole reason to run the campaign, so it is not optional. A week where the
ads run and no line is written is the exact failure the repo already made once.

---

## Decision gates

| Trigger | Check | Action |
|---|---|---|
| $100 cumulative spend | Any keyword with CPI < $3? | If none → pause Campaign C |
| $100 cumulative spend | Campaign B CPT > $3? | Pause B — the arbitrage is priced in |
| $300 cumulative spend | Blended CPI > $3 **and** install→pay still < 5% | **Stop all paid.** Budget returns to the creator engine |
| Any time | Campaign A CPT < $0.75 | Keep A running regardless of the above — it's channel insurance, not acquisition |

The deliverable at $300 is a sentence: *"query X converts at $Y CPI."* If that sentence
can't be written, the answer is that paid isn't the channel yet, and that is a
legitimate result rather than a failure.

---

## Why only search results

- **Search results** is the only placement with keyword-level *intent* and keyword-level
  *attribution*. Every tap teaches which words convert — and that feeds the ASO keyword
  field and caption keywords for free.
- **Product pages** ("You Might Also Like" on other apps' pages) is the genuine second
  choice and a strong persona fit: P1 Serial Restarter is defined in
  `Research/TARGET-USER-PROFILES.md` as *"has already used MyFitnessPal / Lose It / Noom
  and quit. A switcher, not a first-timer"* — literally someone browsing alternatives.
  Held back only because splitting a $15/day budget across two placements produces two
  underpowered tests instead of one readable one. This is phase 2 if search results works.
- **Search tab** shows before the user types, so there is no intent to match, and it is
  a single premium slot contested by every well-funded advertiser on the store.
- **Today tab** is the most expensive placement, is pure brand awareness, and requires a
  Custom Product Page that doesn't exist. This is a funded-launch buy, not a $7-MRR buy.

## Phase 2 levers (do not touch until the gates above have been run)

1. **Product pages placement**, targeted at MyFitnessPal / Lose It / Noom / MacroFactor
   product pages. Best remaining persona fit.
2. **Monday dayparting.** P1's download trigger is documented as *"Monday. January 1. A
   post-holiday photo."* Weighting Monday morning is a real lever once there's baseline
   data to weight against.
3. **A discovery campaign with Search Match ON**, tiny budget, purely to harvest keyword
   ideas — only once there's budget headroom that isn't stealing from a live test.
4. **Custom Product Pages** per keyword cluster (a GLP-1/protein-first CPP would serve
   P2, which `TARGET-USER-PROFILES.md` notes nobody in this space owns yet). Requires
   App Store Connect work first.

## Sources

Benchmarks are directional, not targets; category medians hide large spread.

- [Ad Placement Options — Apple Ads Help](https://ads.apple.com/app-store/help/ad-placements/0081-ad-placement-options)
- [Apple expands App Store search ads to multiple slots, March 2026](https://almcorp.com/blog/apple-app-store-multiple-search-ad-slots-march-2026/)
- [Apple Ads benchmarks 2026: CPT, CPI, CR & TTR by category — AppTweak](https://www.apptweak.com/en/aso-blog/apple-ads-benchmarks)
- [Apple Ads benchmarks 2026 — Adapty](https://adapty.io/blog/apple-ads-benchmarks-2026/)
- [Apple Search Ads benchmarks 2026 — Sparrow Apps](https://sparrowapps.io/articles/apple-ads-benchmarks/)
