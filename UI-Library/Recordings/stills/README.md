# stills — real app frames, harvested from recordings

Frames pulled out of the screen recordings by `Content-Engine/harvest_frames.py`. They
are real app screens, so they satisfy the "real screenshots only" guardrail in
`CLAUDE.md` and can be dropped straight onto a carousel slide:

```json
{"text": "485 total.", "role": "PROOF",
 "image": "UI-Library/Recordings/stills/2026-07-20-salmon-result.jpg", "style": "phone"}
```

**Why this folder matters more than it looks:** it is what makes the carousel track
self-sufficient. A single 30-second recording of the scan flow contains the dashboard,
the camera, the photo confirm, the analysing beat, the itemised result, the impact
breakdown and the log confirmation. That is more distinct screens than the static
screenshot library holds for the same flow, and it stays current with the app instead of
ageing. Nobody has to send a screenshot.

## Harvesting

```bash
# look at the whole clip first, then pick timestamps by eye
python3 Content-Engine/harvest_frames.py --input <clip> --sheet /tmp/sheet.jpg

# save the ones you picked
python3 Content-Engine/harvest_frames.py --input <clip> --at 9.5:2026-07-20-salmon-result

# or let it keep one frame per distinct screen
python3 Content-Engine/harvest_frames.py --input <clip> --auto --prefix 2026-07-20-salmon
```

Naming: `YYYY-MM-DD-<subject>-<screen>.jpg`, dated to the recording, not to the post.

## Rules

- **Look at every frame before it is used.** The privacy scrub in
  `Content-Engine/DEMO-EDIT-SPEC.md` applies here in full: notification banners, Control
  Center, other people's data, a half-open sheet. A still is easier to inspect than
  video and there is no excuse for shipping a bad one.
- Never retouch a number, crop out a disclaimer, or edit the UI. The "AI Estimate" chip
  and the "estimates can be inaccurate" line are features of these screenshots, not
  blemishes. They are how the honesty guardrail shows up visually.
- Archived clips in `../_USED/` are still fair game for new stills.
