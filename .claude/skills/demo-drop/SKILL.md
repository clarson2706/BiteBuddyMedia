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

**Read `Content-Engine/DEMO-EDIT-SPEC.md` before cutting anything.** This file is
the procedure: find the clips, run the build, schedule the slots. That one is the
craft: the 8-second payoff rule, the always-cut list, the privacy scrub, speed
ramp limits, hook rules, and what makes a clip unusable. Both apply to every edit.

**Scale to what exists.** One clip is one day of demo posts. Five clips is five
days. If the inbox is empty, say so and stop; never invent filler to fill a
schedule.

## 1. Get the clips

Clips arrive one of two ways (see `UI-Library/Recordings/_INBOX/README.md`).
GitHub mobile cannot upload binaries, so **Drive is the normal route.**

**Drive.** Find them, then pull the bytes with curl so they never enter context:

```python
# find: connector call, cheap, metadata only
mcp__Google_Drive__search_files(query="mimeType contains 'video/' and title contains 'bitebuddy'")
```
```bash
# fetch: bytes go straight to disk, not through the context window
curl -sSL -o UI-Library/Recordings/_INBOX/<name>.mov \
  "https://drive.usercontent.google.com/download?id=<FILE_ID>&export=download&confirm=t"
file UI-Library/Recordings/_INBOX/<name>.mov   # must be video, not HTML
```

**Never use `download_file_content`** for video. It returns base64 into the
context window and a phone clip is tens of megabytes of text.

**If curl returns HTML instead of video**, the file is not link-shared. Say so
plainly and ask Connor to set the Drive folder to "Anyone with the link → Viewer";
do not try to work around it.

**Repo route.** If Connor uploaded from a desktop browser, the clip is already in
`UI-Library/Recordings/_INBOX/` and there is nothing to fetch.

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
spinner is a wasted asset. Then run a precision pass at 0.3 to 0.5s intervals
around each boundary, and walk the privacy scrub checklist in `DEMO-EDIT-SPEC.md`
before you build. Control Center, notification banners and other people's data
are all things a phone recording will hand you if you do not look for them.

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

**The payoff must land under 8 seconds in the finished cut.** That is the one
rule the whole edit serves; see `DEMO-EDIT-SPEC.md` for why and for the worked
example. Speed the setup, never the result screen.

**Always extract a frame from the finished file and look at it** before
scheduling. The hook overlay and the end card are both burned in; a bad one is
only visible if you look. Run the full QA checklist at the end of
`DEMO-EDIT-SPEC.md`, and if a clip fails it, say so and stop rather than
shipping a weak demo to fill a slot.

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

| Platform | Demo slot | Adds or replaces |
|---|---|---|
| TikTok | **13:00** | **replaces** that day's flex-slot carousel |
| Instagram | **20:30** | **replaces** that day's second carousel |
| YouTube | **11:00** | **adds** a second Short, 6h clear of the 17:00 one |

**A demo does not increase the day's post count on TikTok or Instagram; it
changes what fills a slot that was already going to publish.** TikTok runs 3/day
by default (08:00 / 13:00 / 19:00) and 3 is the ceiling in
`HOOK-INTELLIGENCE-2026.md`, not a target to beat. Instagram's cap is 2. Adding a
post on top of either is the exact pattern suspected in the July 22 throttle.

**YouTube is the one exception, deliberately.** It has no comparable per-day cap
in our research, the channel is at 5 subscribers, and it has been reading zero
daily views since July 23. More uploads there is a cheap test rather than a risk.
Revisit this if YouTube reach ever becomes something worth protecting.

**Handle the displaced carousel, do not silently drop it.** When a demo takes the
13:00 TikTok slot:

1. Cancel that carousel's scheduled TikTok job (`cancel_scheduled`).
2. Set its `registry.jsonl` entry to `status: displaced`.
3. The next generation run re-slots displaced entries **before** generating new
   material, so a topic that never published is not burned by the dedupe check.

Say in the report which carousels were displaced and by which demo. A slot that
quietly swallowed a post is how a content pipeline starts lying about its output.

Schedule with the Upload-Post SDK, media served from the public repo at the
**commit SHA** (push before scheduling):

```python
c.upload_video(video_path=f"{BASE}/Posts/Demos/{pid}/demo.mp4", title=..., user="Business_Posts",
               platforms=["tiktok"], caption=..., scheduled_date=..., timezone="America/Chicago")
```

YouTube descriptions and Facebook captions take the clickable App Store link;
TikTok and Instagram carry the search phrase instead.

## 6. Archive the clip you just used

**In the same run that schedules the post, never later.** A clip that published from
stays in the inbox only if someone forgets, and the cost of forgetting is re-cutting
footage that already went out.

```bash
git mv "UI-Library/Recordings/_INBOX/<raw name>" \
       "UI-Library/Recordings/_USED/<YYYY-MM-DD>-<what-it-shows>.mp4"
```

Then append one line to `UI-Library/Recordings/_USED/used.jsonl` naming the clip, the
post ids that consumed it, and the stills harvested from it. Full convention in
`UI-Library/Recordings/_USED/README.md`.

Before archiving, **harvest the screens the demo did not use**, because those frames are
what keeps the carousel track from ever needing a screenshot from Connor:

```bash
python3 Content-Engine/harvest_frames.py --input <clip> --sheet /tmp/sheet.jpg   # look
python3 Content-Engine/harvest_frames.py --input <clip> --auto --prefix <YYYY-MM-DD>-<subject>
```

Look at the sheet before keeping anything: the privacy scrub in `DEMO-EDIT-SPEC.md`
applies to a still exactly as it does to a frame of video. Archived clips stay
re-harvestable forever; what they must not do is get cut into a second demo without the
report saying so.

## 7. Record and report

- Write `Posts/Demos/manifest.json` with one entry per demo: id, source clip,
  hook, cta, caption, duration, per-platform job ids and request ids. The
  media-report joins on request_id, so a missing one means that post is
  invisible to analytics forever.
- Append each to `Content-Engine/registry.jsonl` with `series: DEMO`.
- Commit everything, push, then tell Connor: how many clips came in, how many
  days they cover, the slots used, which clips were archived to `_USED/`, how many
  new stills were harvested, and anything a clip was too short or too messy
  to support.

## Why this track matters

Every carousel argues that the app helps. A demo shows it. If demo posts start
outperforming carousels on saves, follows or app comments, that is the single
most useful thing the analytics could tell us, and it is worth saying loudly in
the next `media-report`. Tag them consistently so that comparison is possible.
