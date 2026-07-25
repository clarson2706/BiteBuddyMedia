#!/usr/bin/env python3
"""Assemble a YouTube Short from a post's rendered carousel slides.

Slides are 1080x1350 (4:5); Shorts want 1080x1920 (9:16), so each slide is
padded top and bottom with brand cream. Duration per slide is chosen so the
whole Short lands in the 30-40s band: research says a 15s Short needs close to
100% retention to clear YouTube's watch-time gate, while a ~35s Short clears at
roughly 65% (see Research/HOOK-INTELLIGENCE-2026.md).

ffmpeg comes from the imageio-ffmpeg wheel because this environment has no
system ffmpeg and cannot reach apt. Upload-Post's server-side ffmpeg also works
but returns an authenticated download URL that its own publisher cannot fetch,
so building locally and committing to the public repo is the reliable path.

Usage:  python3 Content-Engine/build_shorts.py Posts/2026-W30/manifest.json <post-id> [...]
"""
import json, os, subprocess, sys
import imageio_ffmpeg

CREAM = "0xFFF8F1"
TARGET_MIN, TARGET_MAX = 30.0, 40.0
PAD_Y = (1920 - 1350) // 2  # 285


def build(week_dir, post_id):
    slide_dir = os.path.join(week_dir, post_id)
    slides = sorted(f for f in os.listdir(slide_dir) if f.endswith(".png"))
    if not slides:
        raise SystemExit(f"no slides in {slide_dir}")

    per = max(TARGET_MIN / len(slides), 3.0)
    if per * len(slides) > TARGET_MAX:
        per = TARGET_MAX / len(slides)

    ff = imageio_ffmpeg.get_ffmpeg_exe()
    cmd = [ff, "-y"]
    for s in slides:
        cmd += ["-loop", "1", "-t", f"{per:.2f}", "-i", os.path.join(slide_dir, s)]
    cmd += [
        "-filter_complex",
        f"concat=n={len(slides)}:v=1:a=0,"
        f"pad=1080:1920:0:{PAD_Y}:color={CREAM},setsar=1",
        "-r", "30", "-pix_fmt", "yuv420p", "-c:v", "libx264",
        "-preset", "veryfast", "-movflags", "+faststart",
        os.path.join(slide_dir, "short.mp4"),
    ]
    subprocess.run(cmd, check=True, capture_output=True)
    out = os.path.join(slide_dir, "short.mp4")
    print(f"{post_id}: {len(slides)} slides x {per:.2f}s = "
          f"{per * len(slides):.1f}s  ({os.path.getsize(out) // 1024} KB)")
    return out


if __name__ == "__main__":
    manifest = sys.argv[1]
    week_dir = os.path.dirname(manifest)
    ids = sys.argv[2:] or [p["id"] for p in json.load(open(manifest))["posts"]]
    for pid in ids:
        build(week_dir, pid)
