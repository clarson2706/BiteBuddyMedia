#!/usr/bin/env python3
"""
Sunday-night readiness check for a week of BiteBuddy carousels.

Deterministic gate between "images are in" and "schedule the week". Validates the
manifest + the PNGs Connor dropped, per the checklist in
Marketing/AUTOMATION-WORKFLOW.md. Stdlib only (no Pillow) — PNG dimensions are
read straight from the IHDR chunk.

Per post it verifies:
  - slides/ has >= slides_expected PNGs named 01.png, 02.png, ... in order
  - each image is a real PNG, within size limit, and a sane carousel ratio
  - title/caption within platform limits; 3-5 hashtags incl. #bitebuddy
  - platforms/date/time_local set; no two posts share a slot on the same day
  - pinned_comment present; TikTok sound plan present
  - guardrails: no medical/outcome claims, no "Meal Advisor"

Output: a green/red report to stdout, plus optional --json machine summary.
Exit code 0 only when every post is READY (no hard failures).

With --write it advances each post's `status`:
  - all checks pass                    -> "verified"
  - images present but a check failed  -> stays / set to "images-ready"
  - no images yet                      -> "draft"

Usage:
  python readiness_check.py [--week 2026-W30] [--posts-root Marketing/Posts]
                            [--write] [--json] [--strict-ratio]
"""
import argparse, datetime, json, os, re, struct, sys

# ---- platform limits (conservative; the binding limit across the 4 targets) ---
CAPTION_MAX = 2200        # Instagram / TikTok caption ceiling
TITLE_MAX = 100           # YouTube Short title (post `title` becomes the video title)
MAX_IMAGE_BYTES = 8 * 1024 * 1024
MIN_SLIDES = 2            # a 1-image "carousel" kills the reach multiplier
MAX_SLIDES = 10           # Instagram carousel hard cap
# accepted master ratios (w, h): 4:5 master, 9:16 full-bleed TikTok/Short source
ACCEPTED_RATIOS = {(4, 5), (9, 16)}

# guardrails — case-insensitive; a match is a HARD failure (must be reviewed)
BANNED_PATTERNS = [
    r"\blose\s+\d",            # "lose 10 lbs"
    r"\b\d+\s*(?:lbs?|pounds|kg)\b",
    r"\bguarantee",
    r"\bburns?\s+fat\b",
    r"\bmelts?\s+fat\b",
    r"\bcure[sd]?\b",
    r"\bdetox\b",
    r"\bmeal\s+advisor\b",     # the Coming-Soon feature — never feature it
]
BANNED_RE = re.compile("|".join(BANNED_PATTERNS), re.IGNORECASE)

PNG_SIG = b"\x89PNG\r\n\x1a\n"


def png_dimensions(path):
    """Return (width, height) from a PNG's IHDR, or None if not a valid PNG."""
    try:
        with open(path, "rb") as f:
            head = f.read(24)
        if len(head) < 24 or head[:8] != PNG_SIG or head[12:16] != b"IHDR":
            return None
        w, h = struct.unpack(">II", head[16:24])
        return (w, h)
    except OSError:
        return None


def ratio_ok(w, h, strict):
    from math import gcd
    if w == 0 or h == 0:
        return False
    g = gcd(w, h)
    r = (w // g, h // g)
    if r in ACCEPTED_RATIOS:
        return True
    if strict:
        return False
    # non-strict: accept anything portrait-ish (taller than wide, within 0.6-0.9 w/h)
    return 0.5 <= (w / h) <= 0.92


def check_slides(post, week_dir, strict_ratio):
    """Return (n_present, errors, warnings) for a post's slides folder."""
    errors, warnings = [], []
    slides_dir = os.path.join(week_dir, post["slides_dir"])
    expected = int(post.get("slides_expected") or 0)

    if not os.path.isdir(slides_dir):
        return 0, [f"slides dir missing: {post['slides_dir']}"], warnings

    pngs = sorted(f for f in os.listdir(slides_dir) if f.lower().endswith(".png"))
    n = len(pngs)
    if n == 0:
        return 0, ["no images yet"], warnings

    # names must be 01.png, 02.png, ... contiguous
    expected_names = [f"{i:02d}.png" for i in range(1, n + 1)]
    if pngs != expected_names:
        errors.append(f"slide filenames not 01..{n:02d} in order (found {pngs})")

    if expected and n < expected:
        errors.append(f"{n} PNGs present but slides_expected={expected}")
    if n < MIN_SLIDES:
        errors.append(f"only {n} slide(s); need >= {MIN_SLIDES} for a carousel")
    if n > MAX_SLIDES:
        errors.append(f"{n} slides exceeds max {MAX_SLIDES} (Instagram cap)")

    for name in pngs:
        p = os.path.join(slides_dir, name)
        size = os.path.getsize(p)
        if size > MAX_IMAGE_BYTES:
            errors.append(f"{name} is {size/1e6:.1f}MB > 8MB")
        dims = png_dimensions(p)
        if dims is None:
            errors.append(f"{name} is not a readable PNG")
            continue
        w, h = dims
        if not ratio_ok(w, h, strict_ratio):
            warnings.append(f"{name} is {w}x{h} — unusual carousel ratio")
    return n, errors, warnings


def check_meta(post):
    errors, warnings = [], []
    title = (post.get("title") or "").strip()
    caption = (post.get("caption") or "").strip()
    tags = post.get("hashtags") or []
    plats = post.get("platforms") or []

    if not title:
        errors.append("title empty")
    elif len(title) > TITLE_MAX:
        errors.append(f"title {len(title)} chars > {TITLE_MAX} (YouTube title limit)")

    if not caption:
        errors.append("caption empty")
    elif len(caption) > CAPTION_MAX:
        errors.append(f"caption {len(caption)} chars > {CAPTION_MAX}")

    if not (3 <= len(tags) <= 5):
        errors.append(f"{len(tags)} hashtags (need 3-5)")
    if tags and not all(str(t).startswith("#") for t in tags):
        errors.append("some hashtags missing '#'")
    if "#bitebuddy" not in [str(t).lower() for t in tags]:
        warnings.append("no #bitebuddy in hashtags")

    if not post.get("date") or not post.get("time_local"):
        errors.append("date/time_local not set")
    if not plats:
        errors.append("platforms empty")

    if not (post.get("pinned_comment") or "").strip():
        warnings.append("pinned_comment empty")
    if "tiktok" in plats and not (post.get("tiktok_sound") or "").strip():
        warnings.append("tiktok_sound not set")

    # guardrail scan across all human-facing copy
    blob = " ".join([title, caption, post.get("pinned_comment") or ""] +
                    [str(t) for t in tags])
    for m in BANNED_RE.finditer(blob):
        errors.append(f"GUARDRAIL: banned phrase '{m.group(0)}' in copy")
    return errors, warnings


def detect_week(posts_root):
    """Pick the week folder to check: the earliest week whose first post date is
    today or later; else the most recent week present."""
    if not os.path.isdir(posts_root):
        return None
    weeks = []
    for name in os.listdir(posts_root):
        mpath = os.path.join(posts_root, name, "manifest.json")
        if os.path.isfile(mpath):
            try:
                d = json.load(open(mpath))
                dates = [p["date"] for p in d.get("posts", []) if p.get("date")]
                if dates:
                    weeks.append((min(dates), name))
            except (OSError, ValueError, KeyError):
                continue
    if not weeks:
        return None
    today = datetime.date.today().isoformat()
    future = sorted(w for w in weeks if w[0] >= today)
    return (future[0] if future else sorted(weeks)[-1])[1]


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--week", help="ISO week label, e.g. 2026-W30 (default: auto-detect)")
    ap.add_argument("--posts-root", default="Marketing/Posts")
    ap.add_argument("--write", action="store_true", help="advance status in manifest")
    ap.add_argument("--json", action="store_true", help="also print a JSON summary")
    ap.add_argument("--strict-ratio", action="store_true",
                    help="require exact 4:5 or 9:16 (default: any portrait)")
    args = ap.parse_args()

    week = args.week or detect_week(args.posts_root)
    if not week:
        print(f"No week folders under {args.posts_root}", file=sys.stderr)
        return 2
    week_dir = os.path.join(args.posts_root, week)
    manifest_path = os.path.join(week_dir, "manifest.json")
    if not os.path.isfile(manifest_path):
        print(f"manifest not found: {manifest_path}", file=sys.stderr)
        return 2

    manifest = json.load(open(manifest_path))
    posts = manifest.get("posts", [])

    # detect slot collisions (same date + time_local)
    seen = {}
    collisions = set()
    for p in posts:
        key = (p.get("date"), p.get("time_local"))
        if key in seen:
            collisions.add(p["id"])
            collisions.add(seen[key])
        else:
            seen[key] = p["id"]

    ready, blocked, waiting = [], [], []
    report_lines = []
    summary = {"week": week, "posts": []}

    for p in posts:
        n, s_err, s_warn = check_slides(p, week_dir, args.strict_ratio)
        m_err, m_warn = check_meta(p)
        errors = s_err + m_err
        warnings = s_warn + m_warn
        if p["id"] in collisions:
            errors.append("slot collision (same date+time as another post)")

        no_images = (n == 0)
        if no_images:
            state = "WAITING"          # Connor hasn't dropped images
            waiting.append(p["id"])
            new_status = "draft"
        elif errors:
            state = "BLOCKED"
            blocked.append(p["id"])
            new_status = "images-ready"
        else:
            state = "READY"
            ready.append(p["id"])
            new_status = "verified"

        if args.write:
            p["status"] = new_status

        icon = {"READY": "✅", "BLOCKED": "❌", "WAITING": "⏳"}[state]
        report_lines.append(f"{icon} {p['id']}  [{p.get('format','?')}]  "
                            f"{n} slides  — {state}")
        for e in errors:
            report_lines.append(f"      ✗ {e}")
        for w in warnings:
            report_lines.append(f"      ! {w}")
        summary["posts"].append({
            "id": p["id"], "state": state, "slides": n,
            "errors": errors, "warnings": warnings,
        })

    if args.write:
        with open(manifest_path, "w") as f:
            json.dump(manifest, f, indent=2)
            f.write("\n")

    print(f"Readiness check — {week}  ({len(posts)} posts)")
    print("=" * 60)
    print("\n".join(report_lines))
    print("=" * 60)
    print(f"READY {len(ready)}   BLOCKED {len(blocked)}   WAITING {len(waiting)}")
    if blocked:
        print(f"  blocked: {', '.join(blocked)}")
    if waiting:
        print(f"  waiting on images: {', '.join(waiting)}")
    all_green = (len(ready) == len(posts) and posts)
    print("ALL GREEN — safe to schedule the week." if all_green
          else "NOT all green — fix blocked posts / wait on images before scheduling.")

    summary["ready"] = ready
    summary["blocked"] = blocked
    summary["waiting"] = waiting
    summary["all_green"] = all_green
    if args.json:
        print("\n--- JSON ---")
        print(json.dumps(summary, indent=2))

    return 0 if all_green else 1


if __name__ == "__main__":
    raise SystemExit(main())
