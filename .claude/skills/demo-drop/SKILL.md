---
name: demo-drop
description: >-
  Turn raw app screen recordings Connor drops in UI-Library/Recordings/_INBOX/
  into production-ready vertical demo posts and schedule them, one per platform
  per day, for as many days as there are clips. Use whenever Connor says he has
  added recordings, screen recordings, app footage or demo clips, or asks to get
  demo videos posted. Handles the edit (trim, speed up the analysing wait, pad to
  1080x1920, hook overlay, Today-dashboard end card), the copy, and the
  scheduling. This is the video track that runs alongside the carousel track; it
  does not touch carousels or the weekly loop.
---

# demo-drop — screen recordings into scheduled demo posts

The scan flow is the product demo, and a real recording of it beats anything we
can write. This skill is the path from a raw phone clip to a scheduled post.

**Scale to what exists.** One clip is one day of demo posts. Five clips is five
days. If the inbox is empty, say so and stop; never invent filler to fill a
schedule.

## 1. Inventory

```bash
ls -la UI-Library/Recordings/_INBOX/
python3 Content-Engine/build_demo.py --probe UI-Library/Recordings/_INBOX/<clip>
```

Probe reports duration, dimensions, fps and whether there is audio. Audio is
stripped either way.

## 2. Look at the footage before cutting it

Extract frames every second or two and actually look at them:

```bash
python3 -c "
import subprocess, imageio_ffmpeg
ff = imageio_ffmpeg.get_ffmpeg_exe()
for t in range(0, 20, 2):
    subprocess.run([ff,'-y','-ss',str(t),'-i','<clip>','-frames:v','1',f'/tmp/f{t}.png'],
                   capture_output=True)"
```

Then read a contact sheet of them. You are looking for four timestamps:

- **start** — the first frame that is already on the dashboard, past any fumbling
- **speed-from / speed-to** — the analysing wait, the dead spot that kills retention
- **end** — a beat or two after the food is saved to the log

Never guess these. A demo whose payoff is buried behind four seconds of a
spinner is a wasted asset.

## 3. Build

```bash
python3 Content-Engine/build_demo.py \
  --input UI-Library/Recordings/_INBOX/<clip> \
  --id demo-YYYY-MM-DD \
  --hook "<hook, 6 to 10 words>" \
  --cta "<topic CTA, 4 to 7 words>" \
  --start 1.5 --end 14 --speed-from 5 --speed-to 9 --speed 3
```

Target **12 to 25 seconds** for TikTok and Instagram. YouTube Shorts want 30 to
40s to clear the watch-time gate at realistic retention, so for the YouTube cut
either use a longer trim or slow the end card, and say in the report if a clip
was too short to make a good Short.

**Always extract a frame from the finished file and look at it** before
scheduling. The hook overlay and the end card are both burned in; a bad one is
only visible if you look.

## 4. Write the copy

Same rules as everything else: `MASTER-PROMPT-V5.md` sections 4 to 9, guardrails
in `CLAUDE.md`, and **no em dashes anywhere**.

The hook lives on the video, so it must be legible in half a second and true to
what the footage shows. Good demo hooks name the friction the scan removes:

- "I stopped guessing what was in my lunch"
- "Three seconds, no weighing, no searching"
- "This is the whole logging process"
- "What 600 calories actually looks like"

Do not claim precision. The estimate is editable and the copy should let that
show rather than hide it, because the accuracy sceptics are the loudest
commenters in this niche (see the anti-persona in `TARGET-USER-PROFILES.md`).

Every demo post is `persona: P1` or `P4`, `hook_family: OUTCOME` or `POV`,
`visual_recipe: DEMO-VIDEO`, `series: DEMO`.

## 5. Schedule, one per platform per day

Demo slots, chosen to sit clear of the carousel slots already in use:

| Platform | Demo slot | Why |
|---|---|---|
| TikTok | **13:00** | third TikTok post of the day; 08:00 / 13:00 / 19:00 keeps 5h+ gaps and stays inside the 3/day band |
| YouTube | **11:00** | second Short of the day, 6h clear of the 17:00 Short |
| Instagram | **20:30** | see the note below |

**The Instagram exception, and it is deliberate.** Connor asked for one more post
on each platform. TikTok and YouTube can absorb that. Instagram cannot: our own
research caps it at 2 feed posts a day, and a third is the pattern that
pattern-matches to spam and is the suspected cause of the July 22 throttle. So on
a demo day the demo **takes** the 20:30 Instagram slot instead of adding to it,
and that day's second carousel runs on TikTok only. Instagram still gets a demo
every demo day; it just does not get three posts. If this ever needs revisiting,
revisit the cadence research first, not the rule.

Schedule with the Upload-Post SDK, media served from the public repo at the
**commit SHA** (push before scheduling):

```python
c.upload_video(video_path=f"{BASE}/Posts/Demos/{pid}/demo.mp4", title=..., user="Business_Posts",
               platforms=["tiktok"], caption=..., scheduled_date=..., timezone="America/Chicago")
```

YouTube descriptions and Facebook captions take the clickable App Store link;
TikTok and Instagram carry the search phrase instead.

## 6. Record and report

- Write `Posts/Demos/manifest.json` with one entry per demo: id, source clip,
  hook, cta, caption, duration, per-platform job ids and request ids. The
  media-report joins on request_id, so a missing one means that post is
  invisible to analytics forever.
- Append each to `Content-Engine/registry.jsonl` with `series: DEMO`.
- Commit everything, push, then tell Connor: how many clips came in, how many
  days they cover, the slots used, and anything a clip was too short or too messy
  to support.

## Why this track matters

Every carousel argues that the app helps. A demo shows it. If demo posts start
outperforming carousels on saves, follows or app comments, that is the single
most useful thing the analytics could tell us, and it is worth saying loudly in
the next `media-report`. Tag them consistently so that comparison is possible.
