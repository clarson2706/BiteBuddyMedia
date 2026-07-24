---
name: carousel-optimize
description: >-
  Close the BiteBuddy marketing feedback loop — gather performance data for every
  carousel already posted (views, likes, comments, shares, saves, swipe-through)
  via the Upload-Post analytics tools, fold it into a persistent append-only
  ledger, analyze what's actually working by format / hook / topic / cover style
  / time slot / platform / hashtag, and emit next-week directives that steer the
  carousel-week generator toward winners and away from flops so the creatives
  compound instead of resetting each week. Use this whenever the task is to
  analyze marketing/carousel performance, review what's working, update the
  analytics ledger, or produce the data-driven brief for the coming week — and it
  runs FIRST in the Sunday-morning pipeline, right before carousel-week. It reads
  and writes Analytics/ and never publishes or generates images.
---

# carousel-optimize — the learning loop for BiteBuddy carousels

Runs at the **top of the Sunday-morning pipeline, before `carousel-week`**. It
turns last weeks' post performance into an explicit steer for the new week, so
every week's creatives are informed by what actually worked. This is the
"constantly improving, constantly tracked" half of the marketing system.

Pipeline position:
```
Sunday AM:  carousel-optimize  →  carousel-week  →  (Connor adds images)
Sunday PM:  carousel-publish (also records fresh metrics when it runs)
```

## Scope boundaries
- **Analyze + steer only.** Never publishes, never generates images, never writes
  post copy. Its output is data + directives; `carousel-week` does the writing.
- The persistent record lives in `Analytics/` and is committed to the
  repo, so the whole history travels with the project.

## Files it owns (`Analytics/`)
| File | Written by | What it is |
|---|---|---|
| `performance-log.jsonl` | `record_metrics.py` | append-only ledger, one snapshot per (post, platform, pull) — never rewritten |
| `leaderboard.json` | `analyze.py` | full rollup by every dimension + ranked posts |
| `next-week-directives.json` | `analyze.py` | compact machine steer `carousel-week` reads |
| `next-week-directives.md` | `analyze.py` | the same, human-readable |

## Procedure

### 1. Gather fresh metrics (needs the Upload-Post connector)
Only posts that have had a few days to mature are worth pulling — so on any given
Sunday you're pulling the **previous** week(s), not the one just posted.

1. Confirm the `mcp__Upload-Post__*` tools are present. If not, **skip to step 3**
   and analyze whatever history already exists (no new pull this run).
2. `list_users` → the profile(s). For each posted carousel, pull per-post numbers
   with `get_post_analytics` / `get_analytics` / `get_platform_metrics`
   (whatever the live schema exposes) — views, likes, comments, shares, saves,
   and swipe-through / completion if the platform returns it.
3. Assemble a **batch JSON array** in the snapshot shape from
   `references/metrics-schema.md`. Critically, copy each post's creative
   attributes from its manifest into the snapshot — `format` and
   `tags` (`hook_type`, `topic`, `cover_style`, `hashtags`) — because those are
   what the analysis correlates against. Also set `slot`/`posted_at`, `platform`,
   `profile`, `week`.

### 2. Record it (deterministic)
```bash
python3 .claude/skills/carousel-optimize/scripts/record_metrics.py --batch <batch.json>
```
Validates and appends to `performance-log.jsonl`. Append-only — re-pulling the
same posts later just adds fresher snapshots; the analyzer uses the latest.

### 3. Analyze → directives (deterministic, no network)
```bash
python3 .claude/skills/carousel-optimize/scripts/analyze.py --min-sample 3
```
Rolls up the ledger and writes the leaderboard + `next-week-directives.{json,md}`.
Add `--weeks 4` to weight recent performance over stale history once the log is
deep. With no data yet it writes a graceful "no-data" directive and exits 0.

### 4. Report + hand off
- Print the top of `next-week-directives.md` for Connor: the lean-into winners,
  the dial-back losers, and the posts to re-cut.
- Leave the directive files in place — `carousel-week` reads
  `next-week-directives.json` at the start of its run and biases the new week.
- Commit the updated `Analytics/` files with the week's push.

## How the steer reaches the creatives
`carousel-week` step 0 loads `next-week-directives.json` when present and:
- allocates extra of the 21 slots to the top `lean_into.format` / `topic`;
- prefers the winning `hook_type` and `cover_style` when writing copy + prompts;
- **re-cuts each `recut_winners` post** — same skeleton, fresh cover slide, new
  food/topic — which is the highest-EV move (proven post, new at-bat);
- avoids the `dial_back` values;
- uses `best_hashtags` in the rotation.
Guardrails always win over the steer: never chase a winner into a medical/outcome
claim or the Meal Advisor.

## Confidence & honesty
`analyze.py` marks a dimension **tentative** below `--min-sample` posts and sets
overall `confidence` low/medium/high. Early on (week 1–2) the steer is weak by
design — don't over-rotate on 3 data points. The signal sharpens as the ledger
grows. North-star truth (installs) isn't per-post attributable from social APIs;
engagement (esp. saves + shares) is the proxy we optimize, and Connor's weekly
App Store install count is the reality check laid over it.

## What this skill does NOT do
Publishing, scheduling, image generation, or writing post copy. It only measures,
remembers, and steers.
