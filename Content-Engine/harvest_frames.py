#!/usr/bin/env python3
"""Pull real app stills out of a screen recording, so carousels never wait on a screenshot.

The carousel track needs pictures of the app. Asking Connor for a fresh screenshot every
week is the manual step that kills an autonomous loop, and the screenshot library goes
stale the moment the UI moves. A screen recording solves both: one clip contains every
screen in the flow, already real, already current.

This turns a clip into named stills under UI-Library/Recordings/stills/, which is a path
`render_slides.py` can put straight on a slide. It never invents, upscales, redraws or
otherwise touches the pixels beyond a JPEG encode.

Three modes:

  # 1. look first: a contact sheet of the whole clip, so you pick timestamps by eye
  python3 Content-Engine/harvest_frames.py --input <clip> --sheet /tmp/sheet.jpg

  # 2. harvest the frames you picked
  python3 Content-Engine/harvest_frames.py --input <clip> \
      --at 2.4:dashboard 6.1:analysing 9.8:result

  # 3. or let it pick: keeps frames that differ enough from the last kept one
  python3 Content-Engine/harvest_frames.py --input <clip> --auto --prefix 2026-08-02-burrito

Mode 3 is the one the weekly loop runs unattended. Mode 1 exists because a frame chosen
without looking is how a half-open menu or a notification banner ends up in a post; the
privacy scrub in DEMO-EDIT-SPEC.md applies to stills exactly as it does to video.
"""
import argparse, os, subprocess, sys
import imageio_ffmpeg
from PIL import Image

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
STILLS = os.path.join(ROOT, "UI-Library", "Recordings", "stills")
FF = imageio_ffmpeg.get_ffmpeg_exe()

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from build_demo import probe


def frame_at(src, t, out_path):
    """One frame, at a timestamp, unmodified."""
    subprocess.run([FF, "-y", "-ss", str(t), "-i", src, "-frames:v", "1",
                    "-q:v", "2", out_path], check=True, capture_output=True)
    return out_path


def difference(a, b, size=(64, 80)):
    """Mean absolute pixel difference of two frames, 0 to 255. Cheap scene detector."""
    pa = Image.open(a).convert("L").resize(size).tobytes()
    pb = Image.open(b).convert("L").resize(size).tobytes()
    return sum(abs(x - y) for x, y in zip(pa, pb)) / len(pa)


def sample_times(src, step):
    d = probe(src)["duration"] or 0
    # skip the first and last half second: both ends of a phone recording usually hold
    # a finger, a swipe-up bar or a still-settling screen
    t = 0.5
    while t < d - 0.5:
        yield round(t, 2)
        t += step


def contact_sheet(src, out_path, step, cols=6, thumb_w=220):
    times = list(sample_times(src, step))
    tmp = [frame_at(src, t, f"/tmp/_hf_{i}.jpg") for i, t in enumerate(times)]
    if not tmp:
        sys.exit("clip too short to sample")
    first = Image.open(tmp[0])
    tw = thumb_w
    th = int(first.height * tw / first.width)
    rows = (len(tmp) + cols - 1) // cols
    sheet = Image.new("RGB", (cols * tw, rows * th), (255, 248, 241))
    for i, p in enumerate(tmp):
        sheet.paste(Image.open(p).resize((tw, th)), ((i % cols) * tw, (i // cols) * th))
        os.remove(p)
    sheet.save(out_path, quality=88)
    print(f"{out_path}  {len(tmp)} frames at {step}s, {times[0]}s to {times[-1]}s")
    print("timestamps left to right, top to bottom:")
    print("  " + "  ".join(f"{t}" for t in times))
    return out_path


def harvest(src, picks):
    os.makedirs(STILLS, exist_ok=True)
    out = []
    for t, name in picks:
        p = os.path.join(STILLS, f"{name}.jpg")
        frame_at(src, t, p)
        out.append(p)
        print(f"{t:>6.2f}s -> {os.path.relpath(p, ROOT)}")
    return out


def auto_pick(src, prefix, step, threshold, limit):
    """Keep frames that differ enough from the last kept one: one still per distinct screen."""
    kept, last = [], None
    for t in sample_times(src, step):
        cur = frame_at(src, t, "/tmp/_hf_cur.jpg")
        if last is None or difference(cur, last) >= threshold:
            kept.append(t)
            last = f"/tmp/_hf_last_{len(kept)}.jpg"
            Image.open(cur).save(last, quality=95)
        if len(kept) >= limit:
            break
    picks = [(t, f"{prefix}-{i + 1:02d}") for i, t in enumerate(kept)]
    print(f"{len(picks)} distinct frames kept from {src} (threshold {threshold})")
    return harvest(src, picks)


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("--input", required=True)
    ap.add_argument("--sheet", help="write a contact sheet here and stop")
    ap.add_argument("--at", nargs="+", default=[],
                    help="timestamps to save, as SECONDS:name (e.g. 9.8:salmon-result)")
    ap.add_argument("--auto", action="store_true", help="pick distinct frames automatically")
    ap.add_argument("--prefix", help="filename prefix for --auto, e.g. 2026-08-02-burrito")
    ap.add_argument("--step", type=float, default=1.0, help="sampling interval, seconds")
    ap.add_argument("--threshold", type=float, default=12.0,
                    help="--auto: mean pixel difference that counts as a new screen")
    ap.add_argument("--limit", type=int, default=8, help="--auto: max stills to keep")
    a = ap.parse_args()

    if not os.path.exists(a.input):
        sys.exit(f"no such clip: {a.input}")
    if a.sheet:
        contact_sheet(a.input, a.sheet, a.step)
    elif a.auto:
        if not a.prefix:
            sys.exit("--auto needs --prefix")
        auto_pick(a.input, a.prefix, a.step, a.threshold, a.limit)
    elif a.at:
        picks = []
        for spec in a.at:
            t, _, name = spec.partition(":")
            if not name:
                sys.exit(f"--at wants SECONDS:name, got {spec!r}")
            picks.append((float(t), name))
        harvest(a.input, picks)
    else:
        sys.exit("need --sheet, --at or --auto")
