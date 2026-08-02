# Getting screen recordings to Claude

**This folder means "not done yet."** Once a clip has been posted from, it moves to
[`../_USED/`](../_USED/) in the same run, so whatever is sitting here is always work
still waiting on an edit. You never need to clear it out yourself.

**Do not try to upload videos into this folder from a phone.** GitHub's mobile web
only offers "create file" for text; there is no binary upload from the photo
library. That is a GitHub limitation, not a repo one.

## Route A — Google Drive (works from a phone, recommended)

One-time setup:
1. In Google Drive, create a folder called **`BiteBuddy Recordings`**
2. Share it: **Anyone with the link → Viewer**

Then, every time:
3. Record the flow on your phone
4. Share sheet → **Save to Drive** → `BiteBuddy Recordings`
5. Tell Claude **"clips are in Drive"**

Claude finds them through the Drive connector, pulls the bytes down with `curl`
(outside its context, so a 60 MB clip costs nothing), edits, schedules, commits the
finished `demo.mp4`, harvests stills for the carousel track, and files the raw clip in
`../_USED/`.

**On the link-sharing step:** it has to be link-shared because the connector can
only hand Claude base64 through its context window, which a phone video would
blow out. Worth noting the exposure is close to zero anyway, since these clips
are destined to be public posts on TikTok, Instagram and YouTube. Do not put
anything private in that folder.

## Route B — GitHub upload (desktop browser only)

On a computer: repo → **Add file → Upload files** → drop the clip in this folder →
commit. Keeps everything private. Not available on mobile.

## What to record

Today dashboard → tap scan → point at food → the analysing beat → the result
screen with the numbers → save to the log. That arc is the product demo.

Tips that improve the edit, none required:
- Start on the dashboard, not the home screen or app switcher
- Let the result screen sit still ~2 seconds so the numbers are readable
- Scan something recognisable; a burrito bowl reads better than a protein bar
- Portrait, do not rotate
- Silent is fine, audio is stripped anyway
