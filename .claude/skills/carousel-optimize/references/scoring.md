# scoring — how analyze.py ranks what works

The goal is a defensible, transparent ranking — no black box. Everything here is
stdlib arithmetic you can reproduce by hand.

## Per-post engagement rate
```
engagement_rate = (likes + 2·comments + 3·shares + 3·saves) / max(views, 1)
```
Weights reflect intent depth, straight from the marketing playbook:
- **saves & shares ×3** — the strongest virality/intent signals; a save is
  "I'll act on this," a share is free distribution.
- **comments ×2** — high-effort engagement and a ranking booster (esp. TikTok
  Photo Mode, where comments resurface the post).
- **likes ×1** — cheap, but still the base signal.

`views` is tracked separately as the **reach** score — the shots-on-goal metric.
When present, `swipe_through_rate` is the truest carousel signal (the equivalent
of video watch-time) and is surfaced in the leaderboard.

## Per-post composite (for the re-cut list)
```
composite = engagement_rate·1000 + views/1000
```
Balances "punched above its weight" (rate) against "actually reached people"
(views), so the re-cut list favors posts that were both efficient and big.

## Dimension rollups
For each dimension value (a format, a hook_type, a slot, a hashtag, …) we compute
across its posts:
- `n` — sample size
- `median_views` — reach (median resists one viral outlier skewing the call)
- `median_eng_rate` — efficiency

Values are ranked by `median_eng_rate`, then `median_views`.

## Lean-into vs dial-back
Within each dimension the ranked values are split:
- **head** (top ~half, capped by `--top`) → `lean_into`
- **tail** (the rest, worst-first) → `dial_back`

So the two lists are always distinct and actionable — never "lean into
everything."

## Confidence
- A dimension value with `n < --min-sample` (default 3) is **tentative**; if a
  whole dimension has no value clearing the threshold, it's flagged
  low-confidence and the analyzer falls back to ranking the tentative values so
  there's still a steer.
- Overall `confidence`: `low` when the ledger has < 3·min_sample posts, `high`
  when every reported dimension has a confident value, else `medium`.

**Read the confidence before over-rotating.** Weeks 1–2 are low-confidence by
design — the base playbook still leads; the data only nudges. By week 4+ the
ledger is deep enough to trust hard.

## What we deliberately do NOT score on
- **Installs per post** — social APIs don't attribute installs to a specific
  post, so we optimize the engagement proxy and lay Connor's weekly App Store
  install total over it as the reality check, rather than inventing false
  per-post attribution.
- **Follower count** — a vanity metric; downloads are the north star.
