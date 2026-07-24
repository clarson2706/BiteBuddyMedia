# Analytics — the carousel performance ledger

The persistent memory of the BiteBuddy marketing machine. Owned by the
`carousel-optimize` skill; committed to the repo so the whole history travels
with the project.

| File | What it is |
|---|---|
| `performance-log.jsonl` | **Append-only** ledger — one JSON snapshot per (post, platform, pull). Never rewritten; the analyzer reads the latest snapshot per post. |
| `leaderboard.json` | Full rollup by format / hook / topic / cover / slot / platform / hashtag, plus every post ranked. Regenerated each run. |
| `next-week-directives.json` | Compact machine steer that `carousel-week` reads at the start of its Sunday run. Regenerated each run. |
| `next-week-directives.md` | The same steer, human-readable — read this to see what's working. |

## The loop
```
carousel-publish posts a week  →  a few days pass  →
carousel-optimize pulls the numbers (record_metrics.py)  →
  appends to performance-log.jsonl  →
  analyze.py rolls it up → leaderboard + next-week-directives  →
carousel-week reads the directives and biases the new week  →  repeat
```
Each week's creatives are shaped by what actually worked the weeks before, so the
content compounds. See `.claude/skills/carousel-optimize/` for the mechanics.

## Notes
- `performance-log.jsonl` is the source of truth — don't hand-edit it; append via
  `record_metrics.py`.
- The generated `leaderboard.json` / `next-week-directives.*` are safe to delete;
  they're rebuilt from the ledger on the next `analyze.py` run.
- Engagement (esp. saves + shares) is the optimization proxy; lay the weekly App
  Store install count over it as the north-star reality check.
