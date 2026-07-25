# registry.jsonl — everything we have ever posted

Append-only dedupe memory, one line per staged post, written by weekly-loop Phase 2:

```json
{"post_id":"2026-W31-mon-1","week":"2026-W31","date":"2026-07-27","title":"",
 "topic":"","chain":"","series":"S2","persona":"P3","hook_family":"LIST",
 "visual_recipe":"RANK-CARD","hook_text":"","platforms":["tiktok","instagram"]}
```

Freshness rules that read this file (weekly-loop Phase 2): no topic within 90 days,
no chain+angle within 14 days, no verbatim hook ever. Starts empty because the repo
restarted 2026-07-25; the pre-reset posts live in git history
(`Posts/2026-W30/manifest.json` before commit ff8df43) if a dedupe question ever
reaches back that far.
