# Reports/ — full-funnel growth reports

Written by the **growth-report** skill (`.claude/skills/growth-report/SKILL.md`),
the on-demand, read-only, whole-business read: social reach → App Store →
signup → trial → **paying** (activation, per Connor 2026-07-29: a real paid
subscription, monthly or annual, never manually granted premium/testers).
Design rationale: `MARKETING-REPORT-PLAN.md` at repo root.

Each run commits two files:

| File | What |
|---|---|
| `YYYY-MM-DD-growth-report.md` | The human report (10 sections, scorecard first) |
| `YYYY-MM-DD-snapshot.json` | Every number from the run, machine-readable |

Snapshots are the trend memory: `Analytics/growth.py` diffs the newest previous
snapshot for week-over-week deltas, so history is never re-derived and the
report gets better every run. Never edit an old snapshot.

## Snapshot schema (v1)

```json
{
  "schema": 1,
  "date": "YYYY-MM-DD",
  "generated_at": "ISO8601",
  "flags": ["warnings the report must repeat"],
  "sources": {"per input: where it came from, pulled_at, stale?"},
  "social":  {"window_days": 30, "posts_with_data": 0,
              "totals": {"views":0,"likes":0,"comments":0,"shares":0,"saves":0},
              "by_platform": {"tiktok": {"views":0,"...":0,"followers":null}}},
  "store":   {"week": "2026-W31", "impressions": null, "product_page_views": null,
              "downloads": null, "age_days": null, "stale": true},
  "product": {"users_total":0,"signups_7d":0,"signups_28d":0,"onboarded_total":0,
              "first_scan_users":0,"wau":0,"scans_7d":0,"logs_7d":0,
              "d1": {"cohort":0,"retained":0}, "d7": {"eligible":0,"retained":0},
              "excluded_testers":0},
  "revenue": {"mrr_gross":0,"revenue_28d":0,"active_subscriptions_rc":0,
              "active_trials_rc":0,"new_customers_28d":0,"active_users_28d":0,
              "paying_subs_supabase":0,"trial_subs_supabase":0,
              "arpu_gross":null,"apple_cut":0.15,"mrr_net_est":null},
  "outreach": {"creators_tracked":0,"by_status":{},"deals":0,"live_posts":0,
               "batches":0},
  "funnel":  {"stages":[{"name":"","count":null,"conv_to_next":null}],
              "bottleneck_hint":""},
  "deltas":  {"vs": "YYYY-MM-DD or null", "…scorecard keys…": "new-old"},
  "projections": {"horizon_days":[30,60,90], "scenarios": {
      "current":  {"assumptions":["arithmetic, spelled out"],
                   "confidence":"none|low|medium|high",
                   "subs":[[lo,mid,hi]], "mrr_gross":[[..]], "mrr_net":[[..]],
                   "downloads":[..]},
      "sprint":   {"…same…"},
      "breakout": {"…same…"}}}
}
```

Nulls mean "source didn't provide it." Nothing here is ever fabricated to fill
a hole; a null in the snapshot must surface as an honest gap in the report.

## Rules (inherited from `Analytics/` + `media-report`, plus this folder's own)

- Everything is committed. If a number isn't in a file, it doesn't exist.
- Platform exports outrank Upload-Post account aggregates; per-post rows win
  over both. Every headline number names its source.
- Paying/activation counts **exclude** promotional/manually granted
  entitlements (`store = PROMOTIONAL` in RevenueCat/Supabase,
  `user_entitlements.source in ('manual','promotion')`) and any profile with
  `excluded_from_analytics = true`.
- Projections are ranges with visible arithmetic and a confidence label, and
  they never feed the weekly loop's directives.
