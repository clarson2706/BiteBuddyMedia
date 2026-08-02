#!/usr/bin/env python3
"""Prepare a finished brand film for posting: normalise, then close on real UI.

Distinct from build_demo.py. That one cuts a raw screen recording into a product
demo. This one takes a film that is already edited (Connor's, or a generative tool's)
and does the two things such a film always needs before it goes out:

  1. normalise to 1080x1920, keeping audio, because brand films carry sound and
     build_demo.py deliberately strips it
  2. append the standard CTA end card, which is the **real** Today dashboard from
     UI-Library inside a phone silhouette

Step 2 matters more than it looks. A generated brand film may render app UI that is
close but not real. The end card is the one frame in the post that is a genuine
screenshot with genuine numbers, and it is the frame carrying the download ask. It is
not a fix for fabricated UI earlier in a film, and it is not treated as one: a film
whose fake UI is legible gets re-cut or held, per CLAUDE.md.

Usage:
  python3 Content-Engine/build_brand_film.py --input film.mp4 --id 2026-08-04-dark-hype \
      --cta "See the number before you eat it"
"""
import argparse, os, subprocess, sys
import imageio_ffmpeg

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from build_demo import OUT_W, OUT_H, CREAM_HEX, end_card, probe

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
FF = imageio_ffmpeg.get_ffmpeg_exe()


def build(src, post_id, cta, card_secs, pose):
    out_dir = os.path.join(ROOT, "Posts", "Brand-Films", post_id)
    os.makedirs(out_dir, exist_ok=True)
    card_png = end_card(os.path.join(out_dir, "_endcard.png"), cta, pose)
    body = os.path.join(out_dir, "_body.mp4")
    card = os.path.join(out_dir, "_card.mp4")
    out = os.path.join(out_dir, "post.mp4")

    src_info = probe(src)

    # 1) normalise geometry and audio. Fit inside the frame and pad on brand cream
    # rather than scaling by width, which overshoots on anything taller than 9:16.
    vf = (f"scale={OUT_W}:{OUT_H}:force_original_aspect_ratio=decrease,"
          f"pad={OUT_W}:{OUT_H}:-1:-1:color={CREAM_HEX},setsar=1")
    cmd = [FF, "-y", "-i", src, "-vf", vf, "-r", "30", "-pix_fmt", "yuv420p",
           "-c:v", "libx264", "-preset", "veryfast"]
    if src_info["has_audio"]:
        cmd += ["-c:a", "aac", "-b:a", "128k", "-ar", "44100", "-ac", "2"]
    else:
        # give the body a silent track anyway, so the concat has a stream to match
        cmd = [FF, "-y", "-i", src, "-f", "lavfi", "-i",
               "anullsrc=channel_layout=stereo:sample_rate=44100",
               "-vf", vf, "-r", "30", "-pix_fmt", "yuv420p", "-c:v", "libx264",
               "-preset", "veryfast", "-c:a", "aac", "-b:a", "128k", "-shortest"]
    subprocess.run(cmd + [body], check=True, capture_output=True)

    # 2) the end card as a clip with matching silent audio
    subprocess.run([FF, "-y", "-loop", "1", "-t", str(card_secs), "-i", card_png,
                    "-f", "lavfi", "-i",
                    "anullsrc=channel_layout=stereo:sample_rate=44100",
                    "-vf", f"scale={OUT_W}:{OUT_H},setsar=1", "-r", "30",
                    "-pix_fmt", "yuv420p", "-c:v", "libx264", "-preset", "veryfast",
                    "-c:a", "aac", "-b:a", "128k", "-shortest", card],
                   check=True, capture_output=True)

    # 3) concat. Re-encode rather than stream-copy: the two inputs come from
    # different encoders and a copy-concat produces a file that plays locally and
    # then stalls on the platform.
    lst = os.path.join(out_dir, "_list.txt")
    open(lst, "w").write(f"file '{body}'\nfile '{card}'\n")
    subprocess.run([FF, "-y", "-f", "concat", "-safe", "0", "-i", lst,
                    "-c:v", "libx264", "-preset", "veryfast", "-pix_fmt", "yuv420p",
                    "-c:a", "aac", "-b:a", "128k", "-movflags", "+faststart", out],
                   check=True, capture_output=True)

    for f_ in (body, card, lst):
        os.remove(f_)
    d = probe(out)
    print(f"{post_id}: {d['duration']:.1f}s  {d['size']}  audio={d['has_audio']}  "
          f"{os.path.getsize(out)//1024} KB  -> {os.path.relpath(out, ROOT)}")
    return out


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("--input", required=True)
    ap.add_argument("--id", required=True)
    ap.add_argument("--cta", default="See the number before you eat it")
    ap.add_argument("--card-secs", type=float, default=2.5)
    ap.add_argument("--pose", default="buddy_goal_celebration")
    a = ap.parse_args()
    if not os.path.exists(a.input):
        sys.exit(f"no such file: {a.input}")
    build(a.input, a.id, a.cta, a.card_secs, a.pose)
