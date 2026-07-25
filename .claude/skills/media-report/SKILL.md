---
name: media-report
description: >-
  Pull every available BiteBuddy media metric across TikTok, Instagram, YouTube
  and Facebook, join it to each post's series / persona / hook family / visual
  recipe / CTA type / time slot, and report what is actually performing versus
  not, with trends over time. Use whenever Connor asks how the content is doing,
  what is working, whether a series or hook is landing, how a specific post
  performed, or for a read on the accounts. Read-only: it never generates,
  schedules, edits or publishes anything. Distinct from the weekly-loop skill,
  whose analytics phase exists to gate generation; this one exists to answer the
  question honestly and can be run any time, as often as wanted.
---

# media-report — what is working, what is not, and what changed

Read-only. You are not deciding next week's content here, you are telling Connor
the truth about the numbers. If a run of this skill would change what gets
posted, that decision belongs to `weekly-loop`, not here.

## Run it

```bash
python3 Analytics/report.py --days 14        # default window
python3 Analytics/report.py --days 30        # longer trend
python3 Analytics/report.py --json           # machine-readable
python3 Analytics/report.py --no-write       # skip the log append (rare)
```

Needs `UPLOAD_POST_API_KEY` in the environment (`pip install upload-post` if the
SDK is missing). Environment variables are applied at **session start**, so a
session that began before the key was added will not see it; start a new one.

The script pulls account-level metrics per platform, then per-post metrics via
each post's `request_id` from the week manifests, joins them to that post's
metadata, prints the cuts, and appends everything to
`Analytics/performance-log.jsonl` so the record grows every time you look.

## Then write the report

Save to `Analytics/<YYYY-MM-DD>-media-report.md` and put the same thing in your
message to Connor. Four sections, in this order.

**1. Headline.** Two or three sentences. What changed since the last report and
what it means. Lead with the thing that would change a decision, not the biggest
number.

**2. What is working.** Name specific posts and the *attribute* that plausibly
explains them: series, hook family, persona, recipe, platform, time slot. Always
against the metric ladder below, never views first.

**3. What is not.** Same specificity. Separate **weak content** (people saw it
and did nothing) from **weak distribution** (few people saw it at all) whenever
the data allows the distinction, because the fixes are opposite.

**4. What I would change.** Three to five concrete moves, each traceable to a
number in this report. If the data does not support a change, say so and
recommend holding. "Keep going, too early to tell" is a legitimate and often
correct recommendation.

## The metric ladder (rank findings by this, not by views)

1. **Installs** — only from `Analytics/installs.jsonl`, which Connor pastes from
   App Store Connect
2. **Link clicks** and **"what app is this?" comments** — highest-intent signals
   we can see
3. **Saves and shares**
4. **Follows and profile visits**
5. **Views** — last. Reach without response is not traction.

A post with 40 views and one genuine question beats a post with 400 silent
views, and the report should say so plainly when that happens.

## Honesty rules (these exist because each one has already been violated once)

- **Own engagement is not engagement.** Comments and follows from the BiteBuddy
  account, from Connor, or from friends are not evidence. On 2026-07-25 four
  self-posted Instagram comments were briefly read as audience response and
  produced a wrong conclusion. Check before crediting anything, and label counts
  as unverified when you cannot.
- **Small samples are anecdote.** Under roughly 8 post-platform rows, report
  direction at most. Never scale or kill a series on four data points; the
  series protocol in `Content-Engine/SERIES.md` requires two weeks and four
  posts minimum for a verdict, and this report must respect that.
- **Do not infer a penalty from a low view count alone.** Distinguish "few saw
  it" from "many saw it and ignored it" using per-post views versus the account's
  recent per-post average.
- **Report zeros loudly.** A week of zero comments is the most important sentence
  in the report, not a gap to skim past.
- **Never fabricate a cause.** "Views rose and the only change was the cover" is
  a hypothesis, not a finding. Say which it is.
- **Name the source of every account-level number.** Upload-Post's account
  aggregates are known to be date-shifted by a day and to under-count likes
  (`2026-07-25-tiktok-export-reconciliation.md`). Where a platform-native export
  covers the same window, it wins. Per-post rows via `request_id` are unaffected.

## Useful context to fold in

- `Analytics/2026-W30-baseline.md` — the zero point every trend is measured from
  (read its 2026-07-25 correction; the TikTok daily series in the body is wrong)
- `Analytics/platform-exports/` — native exports Connor drops, ingested by
  `Analytics/ingest_export.py`. Ground truth wherever they overlap Upload-Post.
- `Content-Engine/SERIES.md` — the series under test and their verdict rules
- `Posts/<week>/manifest.json` — what each post actually was
- `SPRINT-AUG25.md` — the sprint checkpoints, while the sprint is live
- YouTube has read zero daily views since 2026-07-23 despite videos publishing.
  Until that resolves, treat YouTube reach numbers as suspect and say so rather
  than averaging them into a healthy-looking total.

## Finish

Commit the report and the updated log (`Analytics/` is always committed, never
gitignored), then give Connor the four sections in chat. Keep it short enough to
read on a phone: the tables live in the file, the judgement goes in the message.
