# Plan: the full marketing report skill (brainstorm, not built yet)

*Written 2026-07-29 at Connor's request; approved and **BUILT the same day**.
The living pieces are `.claude/skills/growth-report/SKILL.md`,
`Analytics/growth.py`, and `Reports/README.md` — they win over this document
wherever they differ. Kept as the design rationale. Per Connor: the skill runs
on Opus 5.*

## The question this report answers

`media-report` answers "how is the **content** doing." This skill answers a
bigger question:

> **What is the actual state of BiteBuddy as a business — across every channel —
> what trajectory is it on, and what is the single most important thing to fix?**

One run should leave Connor with a complete picture: awareness → App Store →
install → activation → trial → paid, with real numbers at every stage, trend
lines, honest projections for downloads and earnings, and a ranked list of where
to improve. Run it whenever, as often as wanted. Strictly read-only.

## Proposed name and placement

- **Skill name: `growth-report`** (working name; alternatives: `state-of-the-app`,
  `full-report`). It must not collide with `media-report`, which stays as the
  quick content-only read.
- **Reports live in a new top-level folder: `Reports/`**
  - `Reports/YYYY-MM-DD-growth-report.md` — the dated human report
  - `Reports/YYYY-MM-DD-snapshot.json` — every number from that run,
    machine-readable, so later runs can compute trends by diffing snapshots
    instead of re-deriving history
  - `Reports/README.md` — schema + how trajectory is computed
- Both files committed every run (`Analytics/` rule #1 applies here too: if a
  number isn't in a file, it doesn't exist).

## Data source inventory (verified live 2026-07-29)

The repo's rule: don't build around a connector that isn't connected. So each
source below was checked in-session before writing this plan.

| Source | Status | What it gives the report |
|---|---|---|
| **RevenueCat MCP** (project `proj624f423c` "BiteBuddy") | ✅ VERIFIED live | MRR, active subs, active trials, new customers, churn, charts/overview metrics. The sprint baseline ($7 MRR, 1 sub, ~2 installs/day) was pulled from here by hand; the skill pulls it automatically. This is the revenue layer's ground truth. |
| **Supabase MCP** (project `btgidcskbtozbwhavcmd` "BiteBuddy MVP", ACTIVE_HEALTHY) | ✅ VERIFIED live | Real product usage: signups/day, DAU/WAU, scans per user, activation rate, retention cohorts. Read-only SQL, **aggregates only — no per-user PII ever lands in a report**. This is the layer nothing else can see: what people do after installing. |
| **Upload-Post** (API key set 2026-07-25) | ✅ Live, with known defects | Per-post social metrics via `request_id` (reliable) and account aggregates (date-shifted a day, undercounts likes — see `2026-07-25-tiktok-export-reconciliation.md`). Already consumed by `Analytics/report.py`. |
| **Platform exports** (`Analytics/platform-exports/`) | ✅ When Connor drops them | Ground truth wherever they overlap Upload-Post. Export wins on conflict, always. |
| **App Store Connect** | ❌ NOT connected — hand-paste only | `Analytics/installs.jsonl` (impressions, product page views, downloads, weekly). This is the one hole in the funnel. See "Gaps" below. |
| **Outreach pipeline** (`Outreach/creators.jsonl`, `payouts.jsonl`, `batches/`) | ✅ In-repo | Creator engine status: DMs sent, replies, deals, live creator posts. Sprint lever #1 — the report is incomplete without it. |
| **Repo records** (`Posts/*/manifest.json`, `Content-Engine/registry.jsonl`, `Analytics/performance-log.jsonl`) | ✅ In-repo | What was actually published, when, with which series/persona/hook/recipe/CTA/slot metadata. The join layer. |

Not available and not to be faked: App Store keyword rankings, TikTok/IG
profile-visit counts where the API doesn't expose them, link-click attribution
beyond what Upload-Post reports. Nulls stay null, loudly.

## The spine: one funnel, every channel feeding it

Every number in the report hangs off this funnel. Each stage shows the count,
the conversion rate to the next stage, and the week-over-week delta:

```
  Reach          views across TikTok / IG / YT / FB + creator posts
    ↓ engagement rate
  Engagement     likes, comments, saves, shares, app-comments (metric ladder order)
    ↓ intent rate
  Intent         link clicks, "what app is this?" comments, profile visits
    ↓                                    ┌─ App Store impressions
  Store funnel   installs.jsonl ────────┼─ product page views
    ↓ page conversion                    └─ downloads
  Signup         Supabase: account created, first scan completed (usage, not activation)
    ↓ trial start rate
  Trial          RevenueCat: active trials, trial→paid conversion
    ↓
  Activated      = PAYING user, monthly or annual (Connor's definition, 2026-07-29).
                 Excludes manually granted premium (testers) — RevenueCat marks
                 those as promotional entitlements, so filter store == "promotional"
                 out of every subscriber count. MRR, subscribers, churn live here.
```

**The report's most important output is naming the current bottleneck stage in
one sentence.** Today the whole funnel below "Reach" is nearly empty, so the
answer is obvious; the report earns its keep when that stops being true and the
bottleneck starts moving (e.g. "reach is fine now, store page conversion is the
leak: 400 page views → 6 downloads").

## Report structure (the dated markdown)

1. **Scorecard.** One table, ~10 north-star numbers with WoW delta and trend
   arrow: MRR, subscribers, active trials, downloads/wk, installs/day trend,
   total reach, engagement events, followers by platform, creator posts live,
   DMs sent. Readable on a phone in 20 seconds.
2. **The bottleneck.** One paragraph. Which funnel stage is the constraint,
   evidenced by the stage conversion numbers, and what that implies.
3. **The funnel.** The diagram above with real numbers and stage conversions,
   plus data-freshness flag per stage (see honesty rules).
4. **Channel by channel.** TikTok, Instagram, YouTube, Facebook, App Store,
   creator engine. For each: reach trend, engagement quality on the metric
   ladder, best/worst post with the attribute that plausibly explains it
   (reusing `report.py --json` cuts — this skill does NOT reimplement the social
   layer, it consumes it), a verdict (working / not working / can't tell yet +
   why), and a data-quality note (e.g. YouTube's zero-views anomaly, Facebook
   unlinked). "Can't tell yet" is a legitimate verdict and often the honest one.
5. **Product & retention** (Supabase). Signups, first-scan completion rate,
   D1/D7 retention, scans/user. These are *usage* metrics — activation itself
   is defined as paying (see funnel) — but they answer whether marketing is
   pouring water into a leaky bucket, which nothing else in the repo can.
6. **Revenue** (RevenueCat). MRR, ARR run rate, subs, trial funnel, churn,
   observed install→pay rate, and estimated net earnings (after Apple's cut and
   the 30% creator first-payment share where applicable).
7. **Trajectory & projections.** See methodology below. Downloads and MRR at
   +30/60/90 days under three scenarios, with the arithmetic shown.
8. **Sprint checkpoint** (while `SPRINT-AUG25.md` is live). The checkpoint table
   with actual vs target, and — per the sprint rule — if two checkpoints in a
   row are missed, which lever is broken. This section retires with the sprint.
9. **Where to improve.** Ranked, 3–5 moves, each traceable to a number in this
   report, each tagged with which funnel stage it attacks. Plus an explicit
   **"what we don't know yet"** list (missing data, samples too small) so
   absence of evidence never silently reads as evidence.
10. **Data appendix.** Every headline number's source, capture time, and
    freshness. Upload-Post aggregate vs export vs per-post provenance named.

## Projection methodology (the part that can go wrong)

The ask: estimated earnings, downloads, growth trajectory from current
engagement. The risk: with today's sample sizes this becomes confident-sounding
fiction. So the projections are rule-bound:

- **Three scenarios, always.**
  - *Current trajectory*: trailing 14-day installs/day and observed
    install→trial→paid rates, extended linearly. No optimism.
  - *Sprint plan*: the `SPRINT-AUG25.md` checkpoint assumptions (creator posts
    landing, 10+ installs/day by W32, ~2% install→pay held).
  - *Breakout*: one post or creator hits; parameterized by the account's own
    best observed reach multiple, not an invented viral number.
- **Show the arithmetic in the report.** "38 downloads/wk × 2.0% pay rate ×
  $7.99 × 0.85 Apple net = ..." — every projection reproducible from the
  snapshot JSON.
- **Ranges, not points, when n is small.** Under ~50 downloads or ~5 paying
  subs in the window, conversion rates get a wide band (e.g. binomial-style
  uncertainty), and the report says "somewhere between $X and $Y" and means it.
- **Estimated earnings = net**: minus Apple's 15% (Small Business Program),
  minus 30% creator share on attributed first payments, noting trial-expiry lag
  (a trial started this week is revenue in ~3 days or never).
- **Every projection carries a confidence label** (`none/low/medium/high`,
  same vocabulary as `next-week-directives.json`) and the single assumption
  most likely to break it.
- **Projections never feed the weekly loop's directives.** Steering stays with
  `weekly-loop` Phase 1 on observed numbers only. This report is a telescope,
  not a steering wheel.

## Mechanics and guardrails

- **Read-only, hard rule.** The skill never publishes, schedules, edits,
  DMs, or changes RevenueCat/Supabase state. RevenueCat MCP includes write
  tools (pricing, offerings, paywalls); the skill text must explicitly forbid
  them. Supabase access is `SELECT` aggregates only.
- **No PII.** No emails, user IDs, or per-customer rows in any report. Counts
  and rates only.
- **Layered, not duplicated.** The social layer comes from
  `Analytics/report.py --json` (and appends to `performance-log.jsonl` exactly
  as media-report does — asking more often makes the record better). This skill
  adds the store, product, revenue, outreach, and projection layers on top.
  `media-report` survives as the quick content read; `growth-report` is the
  full business read. Likely refactor: a small `Analytics/growth.py` that
  gathers the new layers and emits the snapshot JSON.
- **Trend = snapshot diffs.** Each run's `snapshot.json` is append-only
  history; trajectory charts/tables come from reading prior snapshots, so the
  report gets better every time it runs and never re-guesses the past.
- **Inherits every honesty rule in `media-report`** (own engagement is not
  engagement; small samples are anecdote; distinguish weak content from weak
  distribution; report zeros loudly; never fabricate a cause; name every
  number's source) plus the projection rules above.
- **Freshness gates.** If `installs.jsonl` is older than 7 days the store
  stage renders as STALE with the date, and projections that depend on it say
  so. Same for any platform export.
- **Runs on demand only** — no Routine for now. If it earns a schedule later,
  monthly (1st of month) alongside the existing Sunday loop is the natural
  slot, but that's a separate decision for Connor.

## Gaps and open questions for Connor

1. **App Store Connect stays manual — DECIDED 2026-07-29: option (b).** The
   skill begins each run by checking `installs.jsonl` freshness; if stale it
   prompts Connor for the three numbers (impressions, product page views,
   downloads — ~10 seconds), writes the line, and proceeds with a complete
   funnel. If Connor declines or is unavailable, the store stage renders STALE
   and the run continues.
2. **Activation definition — DECIDED 2026-07-29: activation = paying user**,
   monthly or annual, NOT counting manually granted premium (Connor's
   testers). Implementation: count only RevenueCat subscriptions with a real
   store purchase; exclude promotional/granted entitlements from every
   subscriber, conversion, and activation number. First-scan and retention
   stay in the report as usage metrics, not activation.
3. **Attribution honesty.** We mostly cannot prove which post produced which
   install (no per-post tracking links today). The report will correlate
   ("installs rose the week X ran") and label it correlation. If Connor wants
   real attribution, tracked links / creator promo codes are a separate
   project worth its own decision.
4. **Name and folder** — `growth-report` + `Reports/` unless Connor prefers
   otherwise.
5. **Apple cut** — plan assumes 15% Small Business Program. Confirm.

## Build plan (when approved — NOT yet)

1. `Reports/README.md` + snapshot JSON schema.
2. `Analytics/growth.py`: RevenueCat pull, Supabase aggregate queries,
   installs/outreach/registry readers, funnel math, scenario projections,
   snapshot writer. Each source degrades gracefully to "unavailable," never to
   fake numbers.
3. `.claude/skills/growth-report/SKILL.md`: procedure, report template, the
   guardrails above, honesty rules.
4. First run, sanity-check every number against its source by hand (the
   reconciliation habit that caught the TikTok export drift), commit report +
   snapshot.
5. Update `CLAUDE.md`'s current-state section to point at the new skill.
