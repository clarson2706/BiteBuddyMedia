# upload-post-mapping — manifest → Upload-Post MCP calls

How each manifest post becomes scheduled posts on Upload-Post. The Upload-Post
connector must be **enabled in the session** (its `mcp__Upload-Post__*` tools
present) before any of this runs.

> ⚠️ **Confirm the live tool schema before calling.** Upload-Post evolves its
> MCP tool parameters. At run time, inspect the actual parameter names/shape of
> `mcp__Upload-Post__upload_photos` and `mcp__Upload-Post__upload_video` (they
> load with the connector) and map the fields below onto whatever the live
> schema names them. The mapping here is the intent, not a frozen contract.

## Preflight (once per run)
1. `get_account_info` → confirm token valid; note the plan (free tier = 10
   uploads/mo — a full week is 84 publishes, so a paid plan is required for the
   real cadence).
2. `list_users` → get the profile (e.g. `Business_Posts`) and read its
   `social_accounts`. **Only schedule platforms that are actually linked**
   (non-empty). If a platform is unlinked, skip it for every post and report it.
3. If nothing is linked → **dry-run**: run the readiness check + build the Shorts
   + print the schedule you *would* submit, but call no upload tool. Report that
   publishing is blocked on account linking.

## Per post (only READY posts from the readiness check)
Split each post into two kinds of upload:

### A) Photo carousel → Instagram / TikTok / Facebook
Call `upload_photos` once (or per platform if the tool requires it) with:
| Manifest field | Upload-Post intent |
|---|---|
| profile from `list_users` | `user` / profile handle |
| linked subset of `platforms` (minus youtube) | target platforms |
| `slides/01.png … NN.png` in order | the `photos` (see "Getting images in" below) |
| `title` | post title where the platform uses one |
| `caption` + `hashtags` joined | caption/body (append hashtags after the caption text) |
| `date`+`time_local`+tz | `scheduled_date` as an absolute ISO-8601 instant (UTC) |
| `tiktok_sound` | TikTok sound, if the tool accepts it and it isn't `SET_AT_POST_TIME` |

### B) YouTube Short → YouTube
1. Build the mp4: `build_youtube_short.py --week <W> --id <id>` →
   `<id>/youtube-short.mp4`. If local ffmpeg is missing, the script emits the
   ffmpeg spec — run it via Upload-Post's `submit_ffmpeg_job` /
   `get_ffmpeg_job` / `download_ffmpeg_result`, then use the result.
2. `upload_video` with: the mp4, `title` (≤100), `caption` as description,
   `hashtags`, platform `youtube`, same `scheduled_date`.

## Clickable-link rule (the direct install funnel — do this on every post)
Instagram captions can't carry a clickable link ("link in bio" only), but two of
our four platforms CAN — always use them:
- **YouTube description**: append on its own lines after the caption+hashtags:
  `⬇️ Download BiteBuddy free:` + `https://apps.apple.com/us/app/bitebuddy-ai-calorie-scanner/id6787834752`
- **Facebook caption**: append the same link line (Facebook auto-links URLs).
  Use a per-platform text override (e.g. `facebookTitle` in `platformOptions`)
  so the Instagram/TikTok caption stays clean.
- **Instagram `altText`**: pass the post `title` as alt text on `upload_photos`
  (accessibility + search indexing, zero cost).

## Getting images in (URL vs upload)
Upload-Post needs the media reachable. Two paths — use whichever the live tools
support:
- **Direct upload:** if `upload_photos`/`upload_video` accept file paths or a
  media-upload handle, upload the local PNGs / mp4 directly (preferred — no
  hosting needed).
- **Public URL:** otherwise the PNGs must be at a public URL. The repo is
  private, so do **not** assume raw GitHub URLs work. Confirm a hosting path
  before relying on URLs; if none, stay in dry-run and flag it.

## Async + results
- Uploads return a `request_id`. Poll `get_status` (or `get_job_status`) until
  `success`.
- On success: write the returned per-platform post ID/URL into the post's
  `results` and set `status: "scheduled"` (or `"posted"` if it fired
  immediately).
- On failure: retry with backoff; if still failing set `status: "failed"`, log
  the error into `results`, and surface it to Connor — never silently drop.

## What NOT to do
- Don't schedule WAITING (no-images) or BLOCKED posts.
- Don't invent images or screenshots.
- Don't exceed the plan's monthly upload quota — check before scheduling a full
  week on the free tier.
