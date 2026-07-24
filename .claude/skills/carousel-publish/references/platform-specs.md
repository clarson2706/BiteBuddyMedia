# platform-specs — limits & per-platform posting rules

The readiness check enforces the binding limits; this file is the human
reference for why, plus the per-platform mapping the publish step uses.

## Caption / title limits (the check uses the strictest that applies)
| Platform | Caption/body | Title | Notes |
|---|---|---|---|
| Instagram | 2,200 | — | carousel caption; ~30 hashtag hard cap (we use 3–5) |
| TikTok | 2,200 | — | Photo Mode caption; sound chosen at post time |
| Facebook | 63,206 | — | Page multi-image post |
| YouTube | 5,000 (description) | **100** | Short = the slideshow mp4; `title` becomes the video title, `caption` the description |

`readiness_check.py` fails a post if `caption` > 2,200 or `title` > 100, so the
same copy is safe on every platform.

## Carousel / media rules
| Platform | Format | Min / Max images | Ratio |
|---|---|---|---|
| Instagram | image carousel | 2 – 10 | 4:5 master (1080×1350) |
| TikTok | Photo Mode | 2 – 35 | 4:5 accepted (light letterbox) or 9:16 |
| Facebook | multi-image | 2 – 10 | 4:5 fine |
| YouTube | **Short (video)** | n/a — built by `build_youtube_short.py` | 9:16 (1080×1920) |

- Never 1 image on a carousel platform (kills the reach multiplier) — the check
  fails `< 2` slides.
- YouTube gets the assembled `youtube-short.mp4`, **not** the PNGs.

## Timezone
All `time_local` values are in the manifest's `timezone` (default
`America/Chicago`). Convert to the absolute instant Upload-Post expects
(usually UTC ISO-8601) at scheduling time — do not pass a bare local string
without the offset.

## Hashtags
3–5 per post, always include `#bitebuddy`. Same set cross-posted; platform
tag-culture differences are ignored for v1 (revisit after analytics).
