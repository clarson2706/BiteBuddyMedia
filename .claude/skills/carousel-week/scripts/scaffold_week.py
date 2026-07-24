#!/usr/bin/env python3
"""
Scaffold one week of BiteBuddy carousel posts.

Creates the post-folder tree + a manifest.json skeleton with all 21 posts
(3/day x 7 days) pre-populated with id/date/time/format/platforms/status, so the
skill only has to fill in the creative fields (title, copy, caption, hashtags,
prompts). Deterministic on purpose — folder/rotation bookkeeping should never be
done by hand.

Usage:
    python scaffold_week.py [--week-start YYYY-MM-DD] [--tz America/Chicago]
                            [--posts-root Marketing/Posts] [--force]

--week-start defaults to the NEXT Monday (so a Sunday run stages the week ahead).
"""
import argparse, datetime, json, os, sys

SLOTS = ["08:00", "12:30", "19:00"]          # local time, per AUTOMATION-WORKFLOW.md
FORMATS = [                                   # rotate so no format repeats within a day
    "F1-buddys-list",
    "F2-guess-the-calories",
    "F3-i-was-wrong",
    "F4-one-snap-demo",
]
PLATFORMS = ["instagram", "tiktok", "facebook", "youtube"]

PROMPTS_STUB = """# Generation package — {post_id} ({fmt})

**Upload target:** commit each finished PNG into `Marketing/Posts/<week>/{post_id}/slides/`
on branch `main` of clarson2706/BiteBuddyMVP, named 01.png, 02.png, ... (one per slide,
in order). See the week's CHATGPT-GENERATION-GUIDE.md -> "Uploading to GitHub".
**Every image size:** exactly 1080 x 1350 pixels (4:5 vertical). No exceptions.
**Content model:** body slides EDUCATE (nutrition facts / food photos / clean type).
App UI appears on the FINAL slide only — the Today-home hero in a phone silhouette
+ "Download BiteBuddy — free on the App Store" + a topic call-to-action.

<!-- The carousel-week skill fills the per-slide prompts below. -->

## Slide 01 — COVER
_(prompt goes here)_

## Slide 02
_(prompt goes here)_
"""


def next_monday(today: datetime.date) -> datetime.date:
    # 0 = Monday. If today is Monday, jump to the following Monday.
    return today + datetime.timedelta(days=(7 - today.weekday()) % 7 or 7)


def iso_week_label(d: datetime.date) -> str:
    y, w, _ = d.isocalendar()
    return f"{y}-W{w:02d}"


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--week-start", help="Monday of the target week (YYYY-MM-DD)")
    ap.add_argument("--tz", default="America/Chicago")
    ap.add_argument("--posts-root", default="Marketing/Posts")
    ap.add_argument("--force", action="store_true",
                    help="overwrite an existing manifest for this week")
    args = ap.parse_args()

    if args.week_start:
        start = datetime.date.fromisoformat(args.week_start)
        if start.weekday() != 0:
            print(f"WARNING: {start} is not a Monday.", file=sys.stderr)
    else:
        start = next_monday(datetime.date.today())

    week = iso_week_label(start)
    week_dir = os.path.join(args.posts_root, week)
    manifest_path = os.path.join(week_dir, "manifest.json")
    if os.path.exists(manifest_path) and not args.force:
        print(f"manifest already exists: {manifest_path} (use --force to overwrite)")
        return 1

    os.makedirs(week_dir, exist_ok=True)
    posts, gidx = [], 0
    for day in range(7):
        d = start + datetime.timedelta(days=day)
        for slot_i, hhmm in enumerate(SLOTS, start=1):
            fmt = FORMATS[gidx % len(FORMATS)]
            gidx += 1
            post_id = f"{d.isoformat()}-slot{slot_i}"
            slides_dir = os.path.join(week_dir, post_id, "slides")
            os.makedirs(slides_dir, exist_ok=True)
            # keep the empty slides dir in git so Connor has a target to drop into
            open(os.path.join(slides_dir, ".gitkeep"), "w").close()
            prompts_path = os.path.join(week_dir, post_id, "prompts.md")
            if not os.path.exists(prompts_path) or args.force:
                with open(prompts_path, "w") as f:
                    f.write(PROMPTS_STUB.format(post_id=post_id, fmt=fmt))
            posts.append({
                "id": post_id,
                "date": d.isoformat(),
                "time_local": hhmm,
                "format": fmt,
                "title": "",
                "slides_dir": f"{post_id}/slides",
                "slides_expected": 0,
                "caption": "",
                "hashtags": [],
                "pinned_comment": "",
                # creative attributes the optimize loop correlates on; the skill
                # fills these so carousel-optimize can learn what works.
                "tags": {"hook_type": "", "topic": "", "cover_style": ""},
                "tiktok_sound": "SET_AT_POST_TIME",
                "platforms": PLATFORMS,
                "cta": "link in bio — search BiteBuddy on the App Store",
                "status": "draft",
                "results": {},
            })

    manifest = {"week": week, "timezone": args.tz,
                "generated_at": datetime.datetime.now().isoformat(timespec="seconds"),
                "posts": posts}
    with open(manifest_path, "w") as f:
        json.dump(manifest, f, indent=2)
        f.write("\n")

    # Stable pointer the ChatGPT Sunday routine reads to find THIS week's batch.
    # Refreshed every run so there is always one known path to the current week.
    pointer = {
        "week": week,
        "guide": f"Marketing/Posts/{week}/CHATGPT-GENERATION-GUIDE.md",
        "readme": f"Marketing/Posts/{week}/README.md",
        "hero_asset": f"Marketing/Posts/{week}/assets/today-home-hero.png",
        "week_dir": f"Marketing/Posts/{week}",
        "posts": len(posts),
        "status": "staged",
        "updated_at": datetime.datetime.now().isoformat(timespec="seconds"),
    }
    with open(os.path.join(args.posts_root, "current-week.json"), "w") as f:
        json.dump(pointer, f, indent=2)
        f.write("\n")

    print(f"Scaffolded {len(posts)} posts for {week} ({start} .. "
          f"{start + datetime.timedelta(days=6)})")
    print(f"  manifest: {manifest_path}")
    print(f"  pointer:  {os.path.join(args.posts_root, 'current-week.json')} -> {week}")
    print(f"  format rotation per day: {[p['format'].split('-')[0] for p in posts[:3]]} ...")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
