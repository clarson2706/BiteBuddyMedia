#!/usr/bin/env python3
"""
Assemble a post's carousel PNGs into a vertical 1080x1920 slideshow .mp4 for
YouTube Shorts (Option A in Marketing/AUTOMATION-WORKFLOW.md). This is assembly,
not AI generation — each slide is scaled to fit and padded onto a brand-cream
9:16 canvas, shown for a fixed beat, then concatenated.

ffmpeg is optional in this environment. Behaviour:
  * if `ffmpeg` is on PATH -> build the .mp4 locally.
  * otherwise (or with --emit-command) -> print the exact ffmpeg invocation and
    an inputs list, which can be handed to Upload-Post's server-side ffmpeg
    (submit_ffmpeg_job) or run wherever ffmpeg exists. Exit 0 so a no-ffmpeg
    Routine can still capture the command.

Usage:
  python build_youtube_short.py --post-dir Marketing/Posts/2026-W30/2026-07-20-slot1
  python build_youtube_short.py --week 2026-W30 --id 2026-07-20-slot1 [--emit-command]
  optional: --seconds-per-slide 2.5  --fps 30  --out <path>  --posts-root ...
"""
import argparse, json, os, shutil, struct, subprocess, sys

CANVAS_W, CANVAS_H = 1080, 1920          # 9:16 vertical Short
CREAM = "0xFFF8F1"                        # brand background behind letterboxed slides
PNG_SIG = b"\x89PNG\r\n\x1a\n"


def png_dimensions(path):
    with open(path, "rb") as f:
        head = f.read(24)
    if len(head) < 24 or head[:8] != PNG_SIG or head[12:16] != b"IHDR":
        return None
    return struct.unpack(">II", head[16:24])


def collect_slides(slides_dir):
    if not os.path.isdir(slides_dir):
        return []
    return [os.path.join(slides_dir, f)
            for f in sorted(os.listdir(slides_dir))
            if f.lower().endswith(".png") and f[:2].isdigit()]


def build_command(slides, out_path, seconds, fps):
    """Return (argv_list, filtergraph_str). Each image is looped for `seconds`,
    scaled to fit inside 1080x1920 preserving aspect, padded with cream, then all
    are concatenated into one stream."""
    argv = ["ffmpeg", "-y"]
    for s in slides:
        argv += ["-loop", "1", "-t", str(seconds), "-i", s]

    parts = []
    for i in range(len(slides)):
        # scale to fit, then pad to exact canvas, centered, on cream background
        parts.append(
            f"[{i}:v]scale={CANVAS_W}:{CANVAS_H}:force_original_aspect_ratio=decrease,"
            f"pad={CANVAS_W}:{CANVAS_H}:(ow-iw)/2:(oh-ih)/2:color={CREAM},"
            f"setsar=1,fps={fps},format=yuv420p[v{i}]"
        )
    concat_inputs = "".join(f"[v{i}]" for i in range(len(slides)))
    parts.append(f"{concat_inputs}concat=n={len(slides)}:v=1:a=0[v]")
    filtergraph = ";".join(parts)

    argv += ["-filter_complex", filtergraph, "-map", "[v]",
             "-c:v", "libx264", "-pix_fmt", "yuv420p", "-r", str(fps),
             "-movflags", "+faststart", out_path]
    return argv, filtergraph


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--post-dir", help="path to the post folder (contains slides/)")
    ap.add_argument("--week")
    ap.add_argument("--id")
    ap.add_argument("--posts-root", default="Marketing/Posts")
    ap.add_argument("--seconds-per-slide", type=float, default=2.5)
    ap.add_argument("--fps", type=int, default=30)
    ap.add_argument("--out", help="output mp4 path (default: <post-dir>/youtube-short.mp4)")
    ap.add_argument("--emit-command", action="store_true",
                    help="print the ffmpeg command instead of running it")
    args = ap.parse_args()

    if args.post_dir:
        post_dir = args.post_dir
    elif args.week and args.id:
        post_dir = os.path.join(args.posts_root, args.week, args.id)
    else:
        print("need --post-dir OR (--week and --id)", file=sys.stderr)
        return 2

    slides_dir = os.path.join(post_dir, "slides")
    slides = collect_slides(slides_dir)
    if len(slides) < 2:
        print(f"need >= 2 slides in {slides_dir} (found {len(slides)})", file=sys.stderr)
        return 2

    # sanity: warn on unreadable PNGs but don't hard-fail the command emit
    for s in slides:
        if png_dimensions(s) is None:
            print(f"WARNING: {s} not a readable PNG", file=sys.stderr)

    out_path = args.out or os.path.join(post_dir, "youtube-short.mp4")
    argv, filtergraph = build_command(slides, out_path, args.seconds_per_slide, args.fps)

    have_ffmpeg = shutil.which("ffmpeg") is not None
    if args.emit_command or not have_ffmpeg:
        if not have_ffmpeg and not args.emit_command:
            print("ffmpeg not on PATH — emitting command for server-side/remote run.\n",
                  file=sys.stderr)
        print(json.dumps({
            "output": out_path,
            "canvas": f"{CANVAS_W}x{CANVAS_H}",
            "seconds_per_slide": args.seconds_per_slide,
            "fps": args.fps,
            "slides": slides,
            "duration_est_s": round(len(slides) * args.seconds_per_slide, 1),
            "ffmpeg_argv": argv,
            "ffmpeg_command": " ".join(
                (a if a.startswith(("-", "ffmpeg")) or "/" in a else f'"{a}"') for a in argv
            ),
            "filtergraph": filtergraph,
        }, indent=2))
        return 0

    print(f"Building {out_path} from {len(slides)} slides "
          f"(~{len(slides) * args.seconds_per_slide:.0f}s) ...")
    proc = subprocess.run(argv, capture_output=True, text=True)
    if proc.returncode != 0:
        sys.stderr.write(proc.stderr[-2000:])
        print("ffmpeg failed", file=sys.stderr)
        return 1
    print(f"OK -> {out_path} ({os.path.getsize(out_path)/1e6:.1f} MB)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
