#!/usr/bin/env python3
"""Turn a raw screen recording of the app into a production-ready vertical post.

Connor screen-records one flow: dashboard, scan, food result, log. That raw clip
is the single most valuable asset this account has, because the scan moment is
the product demo and the thing Cal AI built a business on. It is also unusable
as-is: too long, dead air at the start, a slow analysing wait, no hook, no CTA.

This does the edit:
  1. trims the requested start/end
  2. speeds up the analysing wait so the magic moment lands fast
  3. scales and pads to exactly 1080x1920 on brand cream
  4. burns in a hook caption over the opening seconds
  5. appends a still CTA end card built by render_slides.phone_mock()

Output lands in Posts/Demos/<id>/demo.mp4, gets committed, and is served to
Upload-Post from the public repo like every other asset.

ffmpeg comes from the imageio-ffmpeg wheel; this box has no system ffmpeg.

Usage:
  python3 Content-Engine/build_demo.py --input UI-Library/Recordings/_INBOX/clip1.mov \
      --id demo-01 --hook "I stopped guessing what was in my lunch" \
      --cta "See the number before you eat it"
  python3 Content-Engine/build_demo.py --probe UI-Library/Recordings/_INBOX/clip1.mov
"""
import argparse, json, os, subprocess, sys
import imageio_ffmpeg
from PIL import Image, ImageDraw

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from render_slides import (W as SW, H as SH, CREAM, ORANGE, CHARCOAL, SAGE,
                           font, fit_text, load_pose, phone_mock)

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUT_W, OUT_H = 1080, 1920
CREAM_HEX = "0xFFF8F1"
FF = imageio_ffmpeg.get_ffmpeg_exe()


def probe(path):
    r = subprocess.run([FF, "-i", path], capture_output=True, text=True)
    info = {"duration": None, "size": None, "fps": None, "has_audio": "Audio:" in r.stderr}
    for line in r.stderr.splitlines():
        if "Duration:" in line:
            t = line.split("Duration:")[1].split(",")[0].strip()
            h, m, s = t.split(":")
            info["duration"] = int(h) * 3600 + int(m) * 60 + float(s)
        if "Video:" in line and "fps" in line:
            for part in line.split(","):
                if "fps" in part:
                    try:
                        info["fps"] = float(part.strip().split()[0])
                    except ValueError:
                        pass
                if "x" in part and part.strip()[0].isdigit():
                    dims = part.strip().split()[0]
                    if "x" in dims:
                        try:
                            info["size"] = tuple(int(v) for v in dims.split("x")[:2])
                        except ValueError:
                            pass
    return info


def end_card(out_path, cta_line, pose="buddy_goal_celebration"):
    """Still CTA frame at 1080x1920, same language as the carousel CTA slide."""
    img = Image.new("RGB", (OUT_W, OUT_H), CREAM)
    d = ImageDraw.Draw(img)
    d.ellipse([OUT_W - 210, -110, OUT_W + 150, 250], fill=(244, 162, 97))

    f, lines, lh = fit_text(d, cta_line, "Baloo2.ttf", 74, 38, OUT_W - 180, 260, 700)
    y = 210
    for line in lines:
        d.text(((OUT_W - d.textlength(line, font=f)) / 2, y), line, font=f, fill=ORANGE)
        y += lh

    phone = phone_mock(900)
    px, py = (OUT_W - phone.width) // 2 - 110, y + 60
    img.paste(phone, (px, py), phone)
    buddy = load_pose(pose, 430)
    if buddy is not None:
        img.paste(buddy, (px + phone.width - 50, py + phone.height - buddy.height + 20), buddy)

    fd = font("Baloo2.ttf", 52, 700)
    dl = "Download BiteBuddy, free on the App Store"
    d.text(((OUT_W - d.textlength(dl, font=fd)) / 2, OUT_H - 210), dl, font=fd, fill=CHARCOAL)
    fs = font("Inter.ttf", 34, 500)
    sl = "Search 'BiteBuddy: Ai calorie scanner'"
    d.text(((OUT_W - d.textlength(sl, font=fs)) / 2, OUT_H - 140), sl, font=fs, fill=SAGE)
    img.save(out_path)
    return out_path


def hook_overlay(out_path, hook):
    """Transparent PNG of the hook caption, burned over the opening seconds."""
    img = Image.new("RGBA", (OUT_W, OUT_H), (0, 0, 0, 0))
    d = ImageDraw.Draw(img)
    f, lines, lh = fit_text(d, hook, "Baloo2.ttf", 66, 34, OUT_W - 150, 300, 700)
    block = len(lines) * lh
    top = 190
    d.rounded_rectangle([60, top - 40, OUT_W - 60, top + block + 30],
                        radius=40, fill=(255, 248, 241, 240))
    y = top
    for line in lines:
        d.text(((OUT_W - d.textlength(line, font=f)) / 2, y), line, font=f, fill=CHARCOAL)
        y += lh
    img.save(out_path)
    return out_path


def build(src, post_id, hook, cta, start, end, speed_from, speed_to, speed, hook_secs):
    out_dir = os.path.join(ROOT, "Posts", "Demos", post_id)
    os.makedirs(out_dir, exist_ok=True)
    ov = hook_overlay(os.path.join(out_dir, "_hook.png"), hook)
    ec = end_card(os.path.join(out_dir, "_endcard.png"), cta)
    body = os.path.join(out_dir, "_body.mp4")
    out = os.path.join(out_dir, "demo.mp4")

    # 1) trim + optional speed-up of the analysing wait + pad to 9:16 + hook overlay
    # iPhone recordings are ~19.5:9, taller than 9:16, so fit inside the frame and
    # pillarbox on cream rather than scaling by width (which overshoots the height)
    vf = (f"scale={OUT_W}:{OUT_H}:force_original_aspect_ratio=decrease,"
          f"pad={OUT_W}:{OUT_H}:-1:-1:color={CREAM_HEX},setsar=1")
    cmd = [FF, "-y", "-ss", str(start)]
    if end:
        cmd += ["-to", str(end)]
    cmd += ["-i", src, "-i", ov]
    if speed_from is not None and speed_to is not None and speed != 1.0:
        # speed only the named window, keep the rest real time
        filt = (
            f"[0:v]trim=start={start}:end={speed_from},setpts=PTS-STARTPTS[a];"
            f"[0:v]trim=start={speed_from}:end={speed_to},setpts=(PTS-STARTPTS)/{speed}[b];"
            f"[0:v]trim=start={speed_to}{f':end={end}' if end else ''},setpts=PTS-STARTPTS[c];"
            f"[a][b][c]concat=n=3:v=1:a=0,{vf}[v];"
            f"[v][1:v]overlay=0:0:enable='between(t,0,{hook_secs})'[outv]"
        )
        cmd = [FF, "-y", "-i", src, "-i", ov, "-filter_complex", filt,
               "-map", "[outv]", "-an"]
    else:
        cmd += ["-filter_complex",
                f"[0:v]{vf}[v];[v][1:v]overlay=0:0:enable='between(t,0,{hook_secs})'[outv]",
                "-map", "[outv]", "-an"]
    cmd += ["-r", "30", "-pix_fmt", "yuv420p", "-c:v", "libx264",
            "-preset", "veryfast", body]
    subprocess.run(cmd, check=True, capture_output=True)

    # 2) 3s still end card, then concat
    card = os.path.join(out_dir, "_card.mp4")
    subprocess.run([FF, "-y", "-loop", "1", "-t", "3", "-i", ec,
                    "-vf", f"scale={OUT_W}:{OUT_H},setsar=1", "-r", "30",
                    "-pix_fmt", "yuv420p", "-c:v", "libx264", "-preset", "veryfast", card],
                   check=True, capture_output=True)
    lst = os.path.join(out_dir, "_list.txt")
    open(lst, "w").write(f"file '{body}'\nfile '{card}'\n")
    subprocess.run([FF, "-y", "-f", "concat", "-safe", "0", "-i", lst,
                    "-c:v", "libx264", "-preset", "veryfast", "-pix_fmt", "yuv420p",
                    "-movflags", "+faststart", out], check=True, capture_output=True)

    for f_ in [body, card, lst]:
        os.remove(f_)
    d = probe(out)
    print(f"{post_id}: {d['duration']:.1f}s  {d['size']}  {os.path.getsize(out)//1024} KB  -> {out}")
    return out


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("--probe")
    ap.add_argument("--input"); ap.add_argument("--id")
    ap.add_argument("--hook", default="One photo. Every macro.")
    ap.add_argument("--cta", default="See the number before you eat it")
    ap.add_argument("--start", type=float, default=0)
    ap.add_argument("--end", type=float, default=None)
    ap.add_argument("--speed-from", type=float, default=None)
    ap.add_argument("--speed-to", type=float, default=None)
    ap.add_argument("--speed", type=float, default=3.0)
    ap.add_argument("--hook-secs", type=float, default=2.5)
    a = ap.parse_args()
    if a.probe:
        print(json.dumps(probe(a.probe), indent=1)); sys.exit()
    if not (a.input and a.id):
        sys.exit("need --input and --id (or --probe)")
    build(a.input, a.id, a.hook, a.cta, a.start, a.end,
          a.speed_from, a.speed_to, a.speed, a.hook_secs)
