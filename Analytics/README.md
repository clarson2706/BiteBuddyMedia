# Analytics — the loop's memory

*Recreated 2026-07-25 for the weekly loop. Rule #1, learned the hard way: **everything
here is committed.** The old system gitignored its rollups and its log stayed 0 bytes
for its entire life. If a number isn't in a file here, it doesn't exist.*

## Rule #2, learned 2026-07-25: platform exports outrank Upload-Post

Where a platform's own export and Upload-Post disagree, **the export wins**. The
first TikTok export we ingested put the daily view series a full day earlier than
Upload-Post reported it, and counted 9 likes in a window where Upload-Post's
lifetime total said 3. See `2026-07-25-tiktok-export-reconciliation.md`.

Upload-Post remains the scheduling layer and the per-post join key (`request_id`),
and it is still the only source of per-post rows. Its **account aggregates** are
now known to be date-shifted and under-counted. Any report citing an account-level
number should name its source.

## Two ways numbers get here

- **`weekly-loop` Phase 1** writes them as a *gate*: generation cannot start until this
  run's directives exist. That is about steering next week.
- **`media-report`** (skill) + `Analytics/report.py` answer "how are we doing" on demand,
  read-only, as often as you like. It appends to the same log, so asking the question
  more often makes the record better rather than noisier.

## Files

| File | Written by | When |
|---|---|---|
| `performance-log.jsonl` | weekly-loop Phase 1 | every Sunday run — append-only, never edited |
| `<ISO-week>-report.md` | weekly-loop Phase 1 | every Sunday run |
| `next-week-directives.json` | weekly-loop Phase 1 | every Sunday run — overwritten weekly (history lives in git) |
| `installs.jsonl` | **Connor, by hand** | optional, ~10 seconds/week — see below |
| `report.py` | the analysis engine both of the above call | per-post joins + cuts by series/persona/hook/recipe/CTA/platform/slot |
| `<date>-media-report.md` | media-report skill | any time it is run |
| `platform-exports/*.csv` | **Connor, by hand** | raw native exports, committed verbatim for provenance |
| `ingest_export.py` | normalises an export into the log | run whenever Connor drops one |

### Platform exports

Connor pulls these from TikTok Studio → Analytics → Overview (and equivalents
elsewhere) and drops the zip. Ingest, then commit both the raw CSV and the log:

```bash
python3 Analytics/ingest_export.py --tiktok <Overview.csv> --year 2026
```

Rows land in `performance-log.jsonl` as `post_id: ACCOUNT-DAILY`, `source:
tiktok-export`. Re-running is safe; already-logged dates are skipped. Metrics the
export does not report (saves, per-post breakdown) stay **null**, never zero.


## `performance-log.jsonl` — one snapshot per line

```json
{"post_id":"2026-W31-mon-1","week":"2026-W31","series":"S2","persona":"P3",
 "hook_family":"LIST","visual_recipe":"RANK-CARD","platform":"tiktok",
 "posted_at":"2026-07-27T13:00:00Z","captured_at":"2026-08-03T23:10:00Z",
 "views":0,"likes":0,"comments":0,"shares":0,"saves":0,"completion_rate":null,
 "link_clicks":null,"app_comments":0,"url":"https://..."}
```

- `app_comments` = hand-counted "what app is this?"-type comments (highest-intent
  signal we have).
- Null means the platform doesn't expose it — never fabricate.
- Posts are snapshotted on every run for their first 14 days (so most get two
  snapshots: T+~7d and T+~14d). Delta between snapshots = late tail.

## `next-week-directives.json`

```json
{"generated_at":"2026-08-03T23:15:00Z","week_analyzed":"2026-W31",
 "confidence":"none|low|medium|high",
 "lean_into":{"series":[],"hook_families":[],"personas":[],"topics":[],"slots":[]},
 "dial_back":{"series":[],"hook_families":[],"topics":[]},
 "recut_winners":[{"post_id":"","why":"","change_only":"cover"}],
 "experiments":["..."],
 "series_verdicts":{"S1":"hold|scale|iterate|kill","S2":"hold","S3":"hold"},
 "notes":"every entry above must trace to a number in this week's report"}
```

Generation (Phase 2) refuses to run unless `generated_at` matches the current run.

## `installs.jsonl` — Connor's 10-second job (optional but decisive)

One line per week from App Store Connect (App Store → Analytics → Metrics):

```json
{"week":"2026-W31","impressions":0,"product_page_views":0,"downloads":0}
```

Without it, the loop optimizes engagement proxies (saves, shares, link clicks,
app-comments). With it, the weekly report can say the only sentence that matters:
*"posts like X produce installs; posts like Y produce applause."*

## Report format (`<week>-report.md`)

Three sections, in order, each grounded in log lines: **What went well** (top posts +
why, on the metric ladder), **What didn't** (bottom posts + series slots
underperforming; content vs distribution separated), **What changes next week**
(3–7 directives, each citing a number). Then the tables: by series, hook family,
persona, visual recipe, time slot, platform.
