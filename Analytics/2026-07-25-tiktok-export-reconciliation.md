# TikTok export vs Upload-Post — reconciliation, 2026-07-25

*First native platform export ingested. Source: TikTok Studio → Analytics →
Overview, range 18 to 24 July, dropped by Connor. Raw file committed at
`Analytics/platform-exports/tiktok-overview-2026-07-18_2026-07-24.csv`.*

**The headline: Upload-Post's account-level numbers are wrong, in two separate
ways. TikTok's own export is ground truth and supersedes the daily series in
`2026-W30-baseline.md`.**

## 1. The daily series is shifted a day

| Date | TikTok export | Upload-Post said |
|---|---|---|
| Jul 21 | **195** | 0 |
| Jul 22 | **409** | 194 |
| Jul 23 | **40** | 423 |
| Jul 24 | **33** | 22 |
| Jul 25 | not in export | 29 |

Compared same-day these disagree wildly (0 vs 195, 423 vs 40). Compared with
Upload-Post shifted one day later, they line up closely: 195/194, 409/423,
40/22, 33/29. So Upload-Post is reporting each day's numbers against the
following date, most likely a UTC-versus-account-local boundary, with the
residual gaps explained by partial-day capture.

**What this changes about the throttle story.** The baseline put the peak on
Jul 23 and the collapse on Jul 24. The real shape is a peak of 409 on **Jul 22**,
the day of the five simultaneous posts, then 40 and 33 on the two days after. The
collapse follows the cadence violation by one day rather than two, which makes
the causal read *tighter* than the baseline claimed, not looser. The conclusion in
`CLAUDE.md` and `HOOK-INTELLIGENCE-2026.md` stands; only the dates move.

## 2. The like counts do not reconcile at all

The export counts **9 likes** in this window (3 on Jul 21, 6 on Jul 22).
Upload-Post's account snapshot the same morning reported **3 likes lifetime**.
These cannot both be true, and the platform's own export is the one to believe.

This is worth flagging rather than quietly absorbing, because the engagement
story has been built on the assumption that near-zero response was the baseline.
Nine likes in two days is still small, but it is three times what we thought, and
it lands on the days when reach was highest.

It does not disturb the 2026-07-25 milestone. Connor confirmed the like on the
Jul 25 post is not his, and that post is a per-post measurement, not part of this
export window. **Open question for Connor:** were the 9 likes on Jul 21 and 22
ours, from the account itself or from friends? If any were strangers, the "first
organic engagement" milestone moves earlier and the account is less cold than the
baseline concluded.

## 3. What the export confirms

- **Zero comments and zero shares** every single day of the window. Consistent
  with every other source. The comment problem is real and is not a measurement
  artifact.
- **1 profile view, total, across seven days.** Reach is not converting to
  curiosity. On the metric ladder this sits just above views and it is nearly nil.
- **Nothing at all before Jul 21.** Three consecutive zero-view days open the
  window. Combined with Upload-Post's 895 lifetime views and the 222 on the Jul 25
  post, essentially the entire lifetime view count of this account was produced in
  five days. The baseline's "~39 views per post across 17 posts" is arithmetically
  true and practically misleading: most posts got nothing, and a few days carried
  everything.

## 4. Standing rule from here

Platform-native exports outrank Upload-Post wherever they overlap. Upload-Post
stays the scheduling layer and the per-post join key (`request_id`), and it is
still the only source of per-post rows, but its account aggregates are now known
to be both date-shifted and under-counted. Any report that cites an account-level
number should say which source it came from.

Ingest with `python3 Analytics/ingest_export.py --tiktok <Overview.csv> --year 2026`.
Re-running is safe; rows already logged are skipped.
