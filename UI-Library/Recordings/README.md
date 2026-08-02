# Recordings — full-UI screen recordings

Screen recordings of the app in motion. **Preferred over static screenshots for
video** — a real recording of the scan flow (photo → "Buddy is thinking" →
itemized result) is authentic and un-fakeable, whereas asking generative video
to "animate" a screenshot warps the UI text and invents fake buttons.

**Division of labor for the videos:**
- **Real recordings (this folder)** → every shot that shows the actual app.
- **Higgsfield** → the non-UI parts: human hook, the buddy mascot, b-roll,
  backgrounds, transitions. Composite the real recording on top in the edit.

---

## Storage: Git LFS

Recordings are large, so video files here are tracked with **Git LFS** (config in
the repo-root `.gitattributes`). `.mov`, `.mp4`, and `.m4v` under this folder are
stored as LFS pointers, keeping git history lean.

**One-time setup on your machine (Mac):**
```bash
git lfs install          # installs the LFS hooks (once per machine)
```
That's it — `.gitattributes` already declares the tracking, so any video you add
under `Recordings/` is handled by LFS automatically when you commit.

**To add a recording:**
```bash
# drop your .mov into Recordings/_INBOX/ then:
git add UI-Library/Recordings/_INBOX/your-walkthrough.mov
git commit -m "Add UI walkthrough recording"
git push
git lfs ls-files         # confirm it's tracked by LFS (not raw in git)
```

> If you upload via the GitHub web UI instead, LFS tracking still applies because
> `.gitattributes` is committed — but the web uploader has file-size limits, so
> for big recordings prefer committing from your Mac.

---

## Folders

| Folder | What lives here |
|---|---|
| [`_INBOX/`](./_INBOX/) | **Drop zone** for raw full-walkthrough recordings (any names). If a file is here, it still needs an edit. |
| [`clips/`](./clips/) | Per-screen clips I segment out of the raw recordings, named to match the screen (e.g. `03-scan-capture__scan-flow.mov`). |
| [`_USED/`](./_USED/) | **Already posted from.** A clip moves here in the same run that schedules a post from it, with a line in `_USED/used.jsonl` saying which posts consumed it. Still re-harvestable for stills, never re-cut into a second demo by default. |
| [`stills/`](./stills/) | Frames pulled out of recordings by `Content-Engine/harvest_frames.py`. These are real app screens and can go straight onto a carousel slide, which is why the carousel track never has to ask for a screenshot. |

---

## How to record a clean walkthrough

- Use iOS **Screen Recording** (Control Center). Optionally also film your
  hands/face separately for hook footage.
- Move **slowly and deliberately** — pause ~2 seconds on each key screen so
  clean clips and freeze-frames can be pulled.
- Do the **real scan flow live** (photo → analyzing → result) — that live
  transition is the money shot; don't cut straight to the result.
- **Light mode**, 60fps if available, a couple of takes.
- Hit every screen in the `../README.md` manifest so no page is stuck with only
  a single still.

## What happens after you add one
Tell me "recording is in `Recordings/_INBOX`" and I'll:
- log it, note the timestamp of each screen,
- segment it into per-screen clips under `clips/` (named to the manifest),
- pull key freeze-frames into the matching screenshot folders,
- and map each clip to the video concepts that use it.

*(Note: the automated split needs a video toolchain — if it's unavailable in a
given session I'll give you exact CapCut/QuickTime trim in/out timestamps per
screen so you can export the clips in a couple of minutes.)*
