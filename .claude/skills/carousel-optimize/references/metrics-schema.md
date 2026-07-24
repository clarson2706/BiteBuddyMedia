# metrics-schema — the snapshot shape for the ledger

`record_metrics.py` ingests a **batch = JSON array of snapshot objects**. One
snapshot = one post's numbers on one platform at one pull time. Claude builds
these from the Upload-Post analytics tool responses, enriched with the post's
creative attributes from its manifest.

```json
[
  {
    "post_id": "2026-07-20-slot1",
    "platform": "tiktok",
    "profile": "Business_Posts",
    "week": "2026-W30",
    "format": "F1-buddys-list",
    "posted_at": "2026-07-20T08:00:00",
    "slot": "08:00",
    "tags": {
      "hook_type": "mistake-listicle",
      "topic": "hidden-calories",
      "cover_style": "buddy-shock",
      "hashtags": ["#caloriedeficit", "#caloriecounting", "#bitebuddy"]
    },
    "metrics": {
      "views": 124000,
      "likes": 8200,
      "comments": 410,
      "shares": 900,
      "saves": 2600,
      "swipe_through_rate": 0.58
    }
  }
]
```

## Field reference
| Field | Required | Source | Notes |
|---|---|---|---|
| `post_id` | ✅ | manifest | ties the snapshot back to the post |
| `platform` | ✅ | — | `tiktok` / `instagram` / `facebook` / `youtube` |
| `metrics.views` | ✅ | Upload-Post | denominator for engagement rate |
| `profile` | — | `list_users` | which account posted it (dimension) |
| `week` | — | manifest | enables `--weeks N` recency weighting |
| `format` | — | manifest | primary creative dimension |
| `slot` / `posted_at` | — | manifest | time-slot dimension (`slot` derived from `posted_at` if absent) |
| `tags.hook_type` | — | manifest tags | e.g. mistake-listicle / confession / guess-the-number / product-demo |
| `tags.topic` | — | manifest tags | the subject, e.g. hidden-calories / fast-food |
| `tags.cover_style` | — | manifest tags | the cover treatment / Buddy pose |
| `tags.hashtags` | — | manifest | list; exploded and ranked individually |
| `metrics.{likes,comments,shares,saves}` | — | Upload-Post | drive the engagement score |
| `metrics.swipe_through_rate` | — | Upload-Post | recorded when available; the truest carousel signal |

**The tags are what make the loop smart.** The more consistently `carousel-week`
tags each post (via the manifest `tags` object) and Claude copies those tags into
the snapshot, the sharper the "what works" analysis. A snapshot with only
`views` still counts for reach, but can't teach the generator *why* it won.

## Getting the numbers
Whatever the live Upload-Post schema names them, map onto the above:
- `get_post_analytics` — per-post detail (preferred).
- `get_analytics` / `get_platform_metrics` / `get_total_impressions` — account /
  platform rollups; use to backfill when per-post detail is thin.
- `get_history` — the list of what was posted, to enumerate `post_id`s.
