# Growth report — 2026-07-29

*First run of the growth-report skill. Window: 30 days of social, 28 days of
revenue, 7 days of product usage. Sources and capture times in the appendix.
Snapshot: `2026-07-29-snapshot.json`. No prior snapshot, so no deltas yet.*

## 1. Scorecard

| Metric | Value | vs last report |
|---|---|---|
| MRR (gross) | $7 | first snapshot |
| Active subscriptions (paying = activated) | 1 (RC) / 2 (Supabase; see §6) | — |
| Active trials | 1 | — |
| New customers, 28d | 56 (~2/day) | — |
| App Store downloads/wk | **null — never recorded** | — |
| Signups, 7d | 7 | — |
| WAU | 5 (of 13 real users) | — |
| Views, 30d, all platforms | 1,139 | — |
| Engagement events, 30d | 8 (7 likes + 1 like; 0 comments, 0 shares, 0 saves) | — |
| Creators: tracked / DMs sent / deals / posts live | 20 / **0** / 0 / 0 | — |

## 2. The bottleneck

The engine's mechanical answer is the App Store data gap (§3), and it is real:
`installs.jsonl` has never been written, so the middle of the funnel is dark and
every install number in this report is a proxy. But the honest bottleneck this
week is **operational, not analytical: the operating system stalled on
2026-07-25.** The Sunday 7/27 full loop never ran (directives are still dated
7/25, there is no W31 post batch), and the daily creator-DM Routine has sent 0
of the 20 DMs written four days ago. The sprint's two highest-priority levers
are idle. Until the machine is actually running, channel-level optimization is
moot.

## 3. The funnel

| Stage | Count | → next | Source / freshness |
|---|---|---|---|
| Reach (views, 30d) | 1,139 | 0.70% | Upload-Post per-post rows, 2026-07-29 |
| Engagement (L+C+S+S) | 8 | — | same |
| Store page views (wk) | **null** | — | `installs.jsonl` missing — DARK |
| Downloads (wk) | **null** | — | same |
| Signups (7d) | 7 | — | Supabase, 2026-07-29, testers excluded |
| Active trials | 1 | — | RevenueCat, 2026-07-29 |
| **Paying = activated** | 1 | | RevenueCat, 2026-07-29 |

Windows differ per stage (30d / weekly / 7d / point-in-time); conversions are
directional. The engagement→signup line cannot be computed honestly: with the
store stage dark there is **no evidence any signup came from content** rather
than App Store browse. ~2 installs/day predates the new content system and has
not visibly moved since it started.

## 4. Channel by channel

**TikTok — distribution works, content doesn't convert attention. Can't tell on installs.**
4 posts with data: 462 / 305 / 286 / 0 views. Per-post reach is 5–10× the old
account average (~39), so the July-22 throttle is behind us. But 1,053 views
produced 7 likes (0.66%), **0 comments, 0 shares, 0 saves**, and the account
still has exactly 1 follower. The comment-earning premise of this batch
(RIGHTWRONG/COMMENT, POV hooks) has now had ~9 days and zero comments anywhere.
Note: the 7/26 POV post reads 0 views — the same post did 33 on YouTube, so
treat that row as a possible API miss, not proof of suppression.

**Instagram — dark.** Zero per-post rows and an empty account object from
Upload-Post. Whether the IG account is actually linked inside Upload-Post is
still unverified (flagged since 7/25). Two of our four organic channels are
producing no measurable anything.

**YouTube — partially recovered from the anomaly, still small.** Per-post rows
now register (53 and 33 views on the two S3 posts) where daily account views
read zero on 7/23–25 — consistent with the account-aggregate lag rather than a
channel strike, but not yet proven. 5 subscribers, 587 lifetime impressions.

**Facebook — dark.** Nulls throughout; link state unverified.

**App Store — the measurement hole.** Impressions, page views, downloads:
never recorded, not once. The sprint doc calls this paste "what separates
winning from applause." It takes ~10 seconds a week.

**Creator engine — written, not fired.** 20 personalized DMs written 7/25
(batch file exists), 0 sent, 0 replies, 0 deals, 0 posts. The daily 8 AM
Routine exists and is enabled but has produced nothing visible in 4 days.
Sprint lever #1 is not underperforming — it is unstarted.

## 5. Product & retention (usage, not activation)

13 real users (6 testers excluded via `excluded_from_analytics`). 7 signed up
in the last 7 days. 12/13 completed onboarding; 8/13 have ever completed a
first scan (62%). WAU 5. 16 scans and 8 food logs in the last 7 days —
roughly 3 scans per weekly-active user. Retention on the 28-day cohort: **D1
2/10, D7 1/5 (20% both, n tiny)**. Read: the bucket leaks at day 1 — most
installers touch it once and don't return the next day — but at n=10 this is
direction, not verdict. Worth watching, not yet worth redesigning onboarding
over.

## 6. Revenue

MRR **$7 gross / ~$5.95 net** (15% Apple Small Business cut). 1 active paying
subscription per RevenueCat; the Supabase mirror shows 2 production
non-promotional paying rows — likely `app_user_id` aliasing (anonymous +
identified IDs for the same person) or a lapsed row; RevenueCat is
authoritative for the count, but worth a one-time look. 1 active trial —
the nearest revenue event in the pipeline; it converts or expires within days.
2 promotional subs (testers) correctly excluded everywhere. Observed
install→pay: 1/56 = **1.8%**, 90% interval **0.4%–7.6%** — wide because n is
small, and the sprint's 2% assumption sits inside it.

## 7. Trajectory & projections (30/60/90 days)

From `growth.py`; confidence **low** on all three. Shared assumptions:
installs/day is a **proxy** (RevenueCat new customers ÷ 28 = 2.0/day; no App
Store data), pay rate 1.8% [0.4%–7.6%], ARPU $7.00 gross, **churn assumed
zero** (the assumption most likely to break), creator revenue share not
modelled (no attributed creator installs exist).

| Scenario | +30d | +60d | +90d |
|---|---|---|---|
| **Current trajectory** (flat 2 installs/day) | ~60 dl, MRR net $7–33 | ~120 dl, $9–60 | ~180 dl, $10–87 |
| **Sprint lands** (10/day from Aug 5, 2% pay — plan numbers) | ~244 dl, ~$35 | ~544 dl, ~$71 | ~844 dl, ~$106 |
| **Breakout** (wk 1 ×5.5 = account's own best-post multiple, then 2× base) | ~169 dl, $10–82 | ~289 dl, $13–136 | ~409 dl, $16–191 |

The blunt reading: **on the current trajectory, the Aug-25 $250 committed
target is out of reach ($7 MRR today, mid-estimate ~$14 gross by Aug 28), and
even the sprint plan landing perfectly gets MRR to ~$41 gross by then, not
$250.** The sprint's checkpoint math always depended on the creator engine
producing compounding installs, and that engine hasn't started. The gap is not
a content problem; it is a throughput problem.

## 8. Sprint checkpoint (W31, due Jul 27)

| Target | Actual | Verdict |
|---|---|---|
| 100 DMs sent | 0 sent (20 written) | ❌ |
| 3+ deals | 0 | ❌ |
| 1+ creator post live | 0 | ❌ |
| Any comments at all | 0 across all platforms | ❌ |
| First tracked-link installs | none (no tracking live) | ❌ |
| MRR $25 | $7 | ❌ |

One checkpoint missed, not two — the two-in-a-row rule hasn't tripped yet. But
W32 (due Aug 3: installs/day > 10, $75) is five days out and mathematically
requires the DM engine firing this week. Per the sprint's own rule, the broken
lever is named: **lever 1 (creator engine) and lever 3 (iteration speed — the
loop itself) both stalled on 2026-07-25.**

## 9. Where to improve — ranked

1. **Restart the machine** (attacks: everything). Run the weekly loop (W31 is
   4 days late), and get the 20 written DMs actually sent per the daily
   Routine. Diagnose why both Routines produced nothing since 7/25. Every
   other recommendation is downstream of this.
2. **Record the App Store numbers** (attacks: store stage, projections).
   One `installs.jsonl` line turns the funnel's dark middle into data and
   replaces the installs proxy in every projection. 10 seconds.
3. **Change the comment ask** (attacks: engagement). The 7/25 media report
   pre-committed: if a full batch still showed zero comments, drop open-ended
   reflective questions for one-word / A-or-B asks. That condition has now
   been met — ~1,139 views, 0 comments. Execute the change in the next batch.
4. **Verify IG and Facebook inside Upload-Post** (attacks: reach). Two of four
   channels report nothing; either they're not linked (fix in Upload-Post
   dashboard) or they're posting into the void unmeasured.
5. **Watch the live trial** (attacks: paying). One trial converts or expires
   within days; it is the single nearest MRR movement and worth a check in the
   next report.

**What we don't know yet:** whether any install has ever come from our content
(no attribution, store stage dark); IG/FB link state; whether YouTube's
zero-view days were lag or a strike; churn (nobody has churned from a real sub
yet); why the 7/26 TikTok POV post reads 0 views.

## 10. Data appendix

| Number | Source | Captured |
|---|---|---|
| MRR, subs, trials, new customers, active users | RevenueCat MCP `get-overview-metrics`, project proj624f423c | 2026-07-29 ~16:10Z |
| Paying/trial production rows, signups, WAU, scans, retention | Supabase MCP aggregate SQL, project btgidcskbtozbwhavcmd, `excluded_from_analytics` filtered | 2026-07-29 ~16:20Z |
| Per-post social metrics | Upload-Post per-post API via `report.py --days 30` (per-post rows, the reliable path) | 2026-07-29 ~16:25Z |
| Account aggregates (TikTok impressions 2,052; YT 587) | Upload-Post account API — known date-shift/undercount; exports outrank it | same |
| App Store impressions / page views / downloads | `Analytics/installs.jsonl` | **never recorded** |
| Creator pipeline | `Outreach/creators.jsonl`, `payouts.jsonl`, `batches/` | repo state 2026-07-29 |
| Projections | `Analytics/growth.py` on the above; arithmetic in §7 assumptions | 2026-07-29 |
