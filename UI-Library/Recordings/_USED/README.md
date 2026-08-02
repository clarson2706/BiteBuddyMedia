# _USED — recordings that have already been posted from

**Every clip in this folder has been consumed.** It has produced at least one scheduled
post, and its stills are in `../stills/`. Nothing here should be cut into a new demo, and
`_INBOX/` should never contain a copy of anything filed here.

This folder exists so the inbox answers one question honestly: **what still needs work?**
An inbox that keeps finished clips slowly stops meaning anything, and the failure mode is
specific and bad, which is re-cutting a clip that already published and posting the same
demo twice under two ids.

## The rule

A clip moves here in the same run that schedules a post from it, never later:

```bash
git mv "UI-Library/Recordings/_INBOX/<raw name>" \
       "UI-Library/Recordings/_USED/<YYYY-MM-DD>-<what-it-shows>.mp4"
```

Then append one line to `used.jsonl` naming what consumed it. `git mv` rather than
`cp` on purpose: one copy of a 4 MB clip in history is enough, and the rename keeps the
file's history intact.

Raw phone filenames (`ScreenRecording_07-20-2026 19-17-58_1 2.mp4`) get renamed on the
way in. The archive is read by people asking "do we already have footage of the barcode
flow", and that question is unanswerable against a wall of timestamps.

## Which folder means what

| Folder | Meaning |
|---|---|
| `../_INBOX/` | raw, unprocessed, **waiting for an edit**. If it is here, it is work to do |
| `../clips/` | the trimmed working cut that the edit and the stills actually came from |
| `_USED/` | **done.** Already published from. Kept for provenance and for re-harvesting stills |
| `../stills/` | frames pulled out by `Content-Engine/harvest_frames.py`, usable on any slide |

## Still useful after archiving

Archived does not mean spent. A clip here is still the best source of **new** app stills:
`harvest_frames.py` can pull a screen from it that no post has used yet, and that costs
nothing and asks Connor for nothing. Re-harvesting from an archived clip is encouraged.
Re-cutting an archived clip into a second demo post is not, unless the report says so
plainly and the edit is genuinely different.

## `used.jsonl`

One line per archived clip, append-only:

```json
{"clip":"2026-07-20-scan-salmon-plate.mp4","archived":"2026-08-02",
 "inbox_name":"ScreenRecording_07-20-2026 19-17-58_1 2.mp4",
 "used_by":["demo-2026-07-26","2026-07-25-flex1"],
 "stills":["2026-07-20-salmon-plate.jpg"],"note":"..."}
```

`used_by` holds post ids that are traceable in `Content-Engine/registry.jsonl`, so any
later question about where a frame came from has an answer.
