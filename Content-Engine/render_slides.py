#!/usr/bin/env python3
"""Render BiteBuddy carousel slides from a week's manifest.json.

TikTok is the primary channel, so **9:16 at 1080x1920 is the primary output**. A 4:5
1080x1350 set is rendered alongside it for Instagram and Facebook. The previous version
of this script rendered 4:5 only, which TikTok letterboxes: roughly a third of the
screen went to blank fill bars on the one platform that matters, and the hook shrank
with it.

    python3 Content-Engine/render_slides.py Posts/2026-W31/manifest.json
    python3 Content-Engine/render_slides.py <manifest> --format tiktok   # 9:16 only
    python3 Content-Engine/render_slides.py <manifest> --contact-sheet   # QA strip

Output:
    Posts/<week>/<post-id>/tiktok/NN.png     1080x1920   <- hand these to TikTok
    Posts/<week>/<post-id>/ig/NN.png         1080x1350   <- Instagram and Facebook

The repo is public, so both sets are reachable at raw.githubusercontent.com and can be
handed straight to Upload-Post as public URLs. Always reference the **commit SHA**, not
a branch name: the SHA is immutable, so a later push cannot alter a scheduled post.

Slide data model (all backwards compatible with the string form):

    "just text"                                  -> TYPE-CARD
    {"text": ..., "image": ..., "style": "photo"|"phone"}
    {"kind": "rank", "rank": 1, "name": ..., "stat": ..., "note": ...}
    {"kind": "compare", "a": {...}, "b": {...}, "banner": ...}
    {"kind": "grid", "rows": [{"name": ..., "stat": ...}, ...], "text": ...}
    {"kind": "big", "value": "485", "text": ...}
    {"kind": "step", "step": 2, "text": ..., "running": "310 cal"}

Buddy poses come from the manifest (`post["poses"] = ["cover_pose", "cta_pose"]`), not
from a table inside this file. The old hardcoded POSES dict meant every new post
required a code edit, and a post missing from it silently rendered the wrong mascot.
"""
import argparse
import json
import os
import sys
import textwrap

from PIL import Image, ImageDraw, ImageFont

# --- brand tokens (DESIGN-SYSTEM.md) ------------------------------------------------
CREAM = (255, 248, 241)
PEACH = (244, 162, 97)
ORANGE = (233, 132, 58)
SAGE = (143, 162, 127)
LAVENDER = (201, 196, 242)
CHARCOAL = (58, 58, 58)
INK = (38, 38, 42)

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
FONT_DIR = os.path.join(ROOT, "Brand-Assets", "fonts")
POSE_DIR = os.path.join(ROOT, "Brand-Assets", "buddy-poses", "transparent")
TODAY_SHOT = os.path.join(ROOT, "UI-Library", "02-today-home", "01-today-home.png")

DEFAULT_POSES = ("buddy_idle", "buddy_happy")
BADGES = {
    "S1": "GUESS THE CALORIES",
    "S2": "PROTEIN PER DOLLAR",
    "S3": "WHY TRACKING FAILS",
    "S4": "THE BEST ORDER AT",
    "S5": "BOTH THE SAME CALORIES",
    "S6": "SCANNED, NOT GUESSED",
    "DEMO": "",
    "oneoff": "",
}


class Spec:
    """Canvas geometry for one platform.

    `bottom_safe` is the band the platform's own UI covers. On TikTok the caption,
    username and CTA row eat the bottom of the frame, and the like/comment/share rail
    eats the right edge, so nothing that has to be read may sit there.
    """

    def __init__(self, name, w, h, margin, bottom_safe, right_rail=0):
        self.name, self.w, self.h = name, w, h
        self.margin, self.bottom_safe, self.right_rail = margin, bottom_safe, right_rail

    @property
    def content_w(self):
        return self.w - self.margin * 2

    @property
    def content_bottom(self):
        return self.h - self.bottom_safe

    def scale(self, v):
        """Scale a 4:5-tuned size to this canvas so both formats read the same."""
        return int(v * self.h / 1350)


TIKTOK = Spec("tiktok", 1080, 1920, margin=80, bottom_safe=420, right_rail=150)
IG = Spec("ig", 1080, 1350, margin=90, bottom_safe=180, right_rail=0)
FORMATS = {"tiktok": TIKTOK, "ig": IG}


# --- text helpers -------------------------------------------------------------------

def font(path, size, weight=None):
    f = ImageFont.truetype(os.path.join(FONT_DIR, path), size)
    if weight is not None:
        try:
            f.set_variation_by_axes([weight])
        except Exception:
            pass
    return f


def fit_text(draw, text, fnt_path, max_size, min_size, box_w, box_h, weight=None):
    """Largest size at which the wrapped text fits the box."""
    for size in range(max_size, min_size - 1, -2):
        f = font(fnt_path, size, weight)
        avg = draw.textlength("x", font=f) or 1
        cols = max(8, int(box_w / avg))
        for c in range(cols, 6, -1):
            lines = textwrap.wrap(text, width=c)
            if not lines:
                continue
            widest = max(draw.textlength(l, font=f) for l in lines)
            if widest <= box_w:
                lh = int(size * 1.22)
                if len(lines) * lh <= box_h:
                    return f, lines, lh
                break
    f = font(fnt_path, min_size, weight)
    return f, textwrap.wrap(text, width=26), int(min_size * 1.22)


def draw_block(d, text, x, y, box_w, box_h, colour, spec, max_size, min_size=34,
               align="center", fnt="Baloo2.ttf", weight=700):
    """Draw wrapped text into a box and return the y just below it."""
    f, lines, lh = fit_text(d, text, fnt, spec.scale(max_size), spec.scale(min_size),
                            box_w, box_h, weight)
    for line in lines:
        tw = d.textlength(line, font=f)
        lx = x + (box_w - tw) / 2 if align == "center" else x
        d.text((lx, y), line, font=f, fill=colour)
        y += lh
    return y


# --- image helpers ------------------------------------------------------------------

def load_pose(name, target_h):
    p = os.path.join(POSE_DIR, name + ".png")
    if not os.path.exists(p):
        return None
    im = Image.open(p).convert("RGBA")
    r = target_h / im.height
    return im.resize((max(1, int(im.width * r)), target_h), Image.LANCZOS)


def _rounded(im, radius, bezel):
    """Wrap an image in the dark phone silhouette (bezel) or just round its corners."""
    iw, ih = im.size
    out = Image.new("RGBA", (iw + bezel * 2, ih + bezel * 2), (0, 0, 0, 0))
    if bezel:
        ImageDraw.Draw(out).rounded_rectangle([0, 0, out.width - 1, out.height - 1],
                                              radius=radius, fill=INK + (255,))
    mask = Image.new("L", (iw, ih), 0)
    ImageDraw.Draw(mask).rounded_rectangle([0, 0, iw - 1, ih - 1],
                                           radius=max(radius - bezel, 18), fill=255)
    out.paste(im, (bezel, bezel), mask)
    return out


def phone_mock(screen_h):
    """The real Today screenshot inside a phone silhouette. Never redrawn, never mocked."""
    shot = Image.open(TODAY_SHOT).convert("RGB")
    shot = shot.crop((0, 0, shot.width, int(shot.height * 0.72)))  # dashboard hero
    sw = int(screen_h * shot.width / shot.height)
    return _rounded(shot.resize((sw, screen_h), Image.LANCZOS), 46, 14)


def image_block(rel_path, style, max_w, max_h):
    """A real photo or a real screenshot, scaled into the slide. Never a mock."""
    im = Image.open(os.path.join(ROOT, rel_path)).convert("RGB")
    bez, radius = (14, 46) if style == "phone" else (0, 40)
    scale = min((max_w - bez * 2) / im.width, (max_h - bez * 2) / im.height)
    im = im.resize((max(1, int(im.width * scale)), max(1, int(im.height * scale))),
                   Image.LANCZOS)
    return _rounded(im, radius, bez)


# --- chrome -------------------------------------------------------------------------

def accent(d, spec, idx):
    """Soft background shapes, varied per slide so a deck does not look stamped.

    Template variation is a survival trait in 2026, not polish: TikTok's AI-slop
    crackdown names faceless health accounts, and identical layouts are the tell.
    """
    w, h = spec.w, spec.h
    r = spec.scale(180)
    if idx % 4 == 0:
        d.ellipse([w - r * 2, -r, w + r, r * 1.4], fill=PEACH)
    elif idx % 4 == 1:
        d.rounded_rectangle([-r, h - r * 1.4, r * 1.1, h + r], radius=spec.scale(70),
                            fill=LAVENDER)
    elif idx % 4 == 2:
        d.ellipse([-r * 1.4, h - r * 1.2, r * 0.9, h + r], fill=SAGE)
    else:
        d.rounded_rectangle([w - r * 1.6, h - r * 1.1, w + r, h + r],
                            radius=spec.scale(70), fill=PEACH)


def badge(d, spec, text):
    if not text:
        return
    f = font("Baloo2.ttf", spec.scale(30), 700)
    tw = d.textlength(text, font=f)
    pad_x, h = spec.scale(26), spec.scale(56)
    top = spec.margin
    d.rounded_rectangle([spec.margin, top, spec.margin + tw + pad_x * 2, top + h],
                        radius=h // 2, fill=LAVENDER)
    d.text((spec.margin + pad_x, top + spec.scale(10)), text, font=f, fill=CHARCOAL)


def progress(d, spec, idx, total):
    """Dots, not '3/8'. A dot row reads as 'nearly there' and pulls the next swipe;
    slide completion is the primary ranking signal on both platforms."""
    if total < 2:
        return
    r, gap = spec.scale(9), spec.scale(26)
    span = total * gap - (gap - r * 2)
    x = (spec.w - span) / 2
    y = spec.content_bottom + spec.scale(28)
    for i in range(total):
        fill = ORANGE if i <= idx else (226, 216, 206)
        d.ellipse([x, y, x + r * 2, y + r * 2], fill=fill)
        x += gap


# --- slide kinds --------------------------------------------------------------------

def slide_cover(d, img, spec, post, text, image, pose_name):
    """The hook. On a carousel the hook IS slide 1, and it does the whole job: there is
    no sound on an API-published TikTok photo post to help it."""
    y = spec.margin + spec.scale(110)
    box_h = spec.scale(420 if image else 620)
    y = draw_block(d, text, spec.margin, y, spec.content_w, box_h, ORANGE, spec, 96, 44)

    if image:
        avail_h = spec.content_bottom - y - spec.scale(120)
        block = image_block(image, "photo", spec.content_w, avail_h)
        img.paste(block, ((spec.w - block.width) // 2, int(y + spec.scale(34))), block)

    pose = load_pose(pose_name, spec.scale(430 if not image else 240))
    if pose is not None:
        # bottom-LEFT: TikTok's like/comment/share rail owns the right edge
        img.paste(pose, (spec.margin - spec.scale(20),
                         spec.content_bottom - pose.height + spec.scale(10)), pose)


def slide_type(d, spec, text, idx):
    """One idea, generous space, and an accent bar so it does not read as a blank card
    with a sentence floating in it."""
    box_h = spec.scale(700)
    y = (spec.content_bottom - box_h) // 2 + spec.scale(40)
    bar_y = y - spec.scale(46)
    d.rounded_rectangle([spec.margin, bar_y, spec.margin + spec.scale(96),
                         bar_y + spec.scale(14)], radius=7,
                        fill=[PEACH, SAGE, LAVENDER][idx % 3])
    draw_block(d, text, spec.margin, y, spec.content_w, box_h, CHARCOAL, spec, 76, 38,
               align="left")


def slide_big(d, spec, value, text):
    """The reveal. Show the number first and explain after: outcome-showcase was the
    highest-performing hook type in the 4,000-video study."""
    f = font("Baloo2.ttf", spec.scale(300), 700)
    tw = d.textlength(str(value), font=f)
    y = spec.scale(360)
    d.text(((spec.w - tw) / 2, y), str(value), font=f, fill=ORANGE)
    if text:
        draw_block(d, text, spec.margin, y + spec.scale(360), spec.content_w,
                   spec.scale(400), CHARCOAL, spec, 62, 34)


def slide_rank(d, spec, rank, name, stat, note):
    """RANK-CARD. The changing rank numeral is the loudest element and the rhythm of
    the deck. This is the workhorse layout for the ranked-chain series."""
    numeral = font("Baloo2.ttf", spec.scale(230), 700)
    label = f"#{rank}"
    y = spec.scale(300)
    d.text((spec.margin, y), label, font=numeral, fill=PEACH)
    nx = spec.margin + d.textlength(label, font=numeral) + spec.scale(34)

    ny = y + spec.scale(30)
    ny = draw_block(d, name, nx, ny, spec.w - nx - spec.margin, spec.scale(240),
                    CHARCOAL, spec, 74, 34, align="left")

    if stat:
        f = font("Baloo2.ttf", spec.scale(58), 700)
        tw = d.textlength(stat, font=f)
        pad = spec.scale(30)
        chip_y = y + spec.scale(300)
        d.rounded_rectangle([spec.margin, chip_y, spec.margin + tw + pad * 2,
                             chip_y + spec.scale(96)], radius=spec.scale(48), fill=ORANGE)
        d.text((spec.margin + pad, chip_y + spec.scale(14)), stat, font=f, fill=CREAM)

    if note:
        draw_block(d, note, spec.margin, y + spec.scale(440), spec.content_w,
                   spec.scale(300), CHARCOAL, spec, 48, 30, align="left",
                   fnt="Inter.ttf", weight=500)


def slide_compare(d, spec, a, b, banner):
    """COMPARE-SPLIT, stacked rather than side-by-side: on a 9:16 frame a vertical
    split gives each side a readable half instead of two narrow columns."""
    half = (spec.content_bottom - spec.margin) // 2
    for i, side in enumerate((a, b)):
        top = spec.margin + spec.scale(70) + i * half
        d.rounded_rectangle([spec.margin, top, spec.w - spec.margin, top + half - spec.scale(70)],
                            radius=spec.scale(40), fill=(LAVENDER if i == 0 else (232, 240, 226)))
        inner = top + spec.scale(40)
        inner = draw_block(d, side.get("name", ""), spec.margin + spec.scale(30), inner,
                           spec.content_w - spec.scale(60), spec.scale(200), CHARCOAL,
                           spec, 62, 32)
        if side.get("stat"):
            draw_block(d, side["stat"], spec.margin + spec.scale(30), inner + spec.scale(16),
                       spec.content_w - spec.scale(60), spec.scale(120), ORANGE, spec, 54, 30)

    if banner:
        f = font("Baloo2.ttf", spec.scale(52), 700)
        tw = d.textlength(banner, font=f)
        by = spec.margin + spec.scale(70) + half - spec.scale(104)
        d.rounded_rectangle([(spec.w - tw) / 2 - spec.scale(34), by,
                             (spec.w + tw) / 2 + spec.scale(34), by + spec.scale(88)],
                            radius=spec.scale(44), fill=ORANGE)
        d.text(((spec.w - tw) / 2, by + spec.scale(12)), banner, font=f, fill=CREAM)


def slide_grid(d, spec, rows, text):
    """CHEAT-GRID: the screenshot-me slide. Cheat sheets are the most-saved carousel
    type and saves are a heavy ranking input, so every deck that can carry one should."""
    y = spec.margin + spec.scale(90)
    if text:
        y = draw_block(d, text, spec.margin, y, spec.content_w, spec.scale(200),
                       ORANGE, spec, 64, 34) + spec.scale(30)

    rows = rows[:8]
    avail = spec.content_bottom - y - spec.scale(30)
    rh = max(spec.scale(96), avail // max(1, len(rows)))  # fill the space, do not bunch
    gap = spec.scale(16)
    pad = spec.scale(30)
    fstat = font("Baloo2.ttf", int(rh * 0.32), 700)

    for i, row in enumerate(rows):
        top = y + i * rh
        d.rounded_rectangle([spec.margin, top, spec.w - spec.margin, top + rh - gap],
                            radius=spec.scale(26), fill=(255, 255, 255))
        stat = row.get("stat", "")
        stat_w = d.textlength(stat, font=fstat) if stat else 0

        # The name gets whatever width the stat leaves. Shrink it until it fits rather
        # than letting the two collide, which is what a fixed size did.
        name = row.get("name", "")
        name_limit = spec.content_w - stat_w - pad * 3
        fname = font("Baloo2.ttf", int(rh * 0.30), 700)
        while fname.size > 18 and d.textlength(name, font=fname) > name_limit:
            fname = font("Baloo2.ttf", fname.size - 2, 700)

        row_mid = top + (rh - gap) / 2
        d.text((spec.margin + pad, row_mid - fname.size * 0.72), name,
               font=fname, fill=CHARCOAL)
        if stat:
            d.text((spec.w - spec.margin - pad - stat_w, row_mid - fstat.size * 0.72),
                   stat, font=fstat, fill=ORANGE)


def slide_step(d, spec, step, text, running):
    """BUILD-STEP: the running total in the corner is the retention device."""
    f = font("Baloo2.ttf", spec.scale(54), 700)
    chip = f"STEP {step}"
    tw = d.textlength(chip, font=f)
    top = spec.margin + spec.scale(90)
    d.rounded_rectangle([spec.margin, top, spec.margin + tw + spec.scale(56),
                         top + spec.scale(92)], radius=spec.scale(46), fill=SAGE)
    d.text((spec.margin + spec.scale(28), top + spec.scale(14)), chip, font=f, fill=CREAM)

    draw_block(d, text, spec.margin, top + spec.scale(160), spec.content_w,
               spec.scale(520), CHARCOAL, spec, 70, 34, align="left")

    if running:
        fr = font("Baloo2.ttf", spec.scale(50), 700)
        tw = d.textlength(running, font=fr)
        d.text((spec.w - spec.margin - tw, spec.content_bottom - spec.scale(80)),
               running, font=fr, fill=ORANGE)


def slide_image(d, img, spec, text, image, style, is_cover=False):
    """Headline on top, the real thing underneath. Receipts, not renders."""
    y = spec.margin + spec.scale(100)
    y = draw_block(d, text, spec.margin, y, spec.content_w, spec.scale(260),
                   ORANGE if is_cover else CHARCOAL, spec, 74, 34)
    avail = spec.content_bottom - y - spec.scale(60)
    block = image_block(image, style, spec.content_w, avail)
    img.paste(block, ((spec.w - block.width) // 2, int(y + spec.scale(34))), block)


def _centered_fitted(d, text, fnt, size, colour, y, spec, weight=700, max_w=None):
    """Draw one centered line, shrinking until it fits. Never let a line run off the
    canvas: the download line did exactly that at 1080 wide and published as
    'wnload BiteBuddy, free on the App Sto'."""
    limit = max_w or spec.content_w
    for s in range(size, 14, -2):
        f = font(fnt, s, weight)
        tw = d.textlength(text, font=f)
        if tw <= limit:
            d.text(((spec.w - tw) / 2, y), text, font=f, fill=colour)
            return f.size
    return size


def slide_cta(d, img, spec, post, text, pose_name):
    """The last slide, every carousel, no exceptions.

    Three asks, in this order: the topic line, the product shown rather than described,
    and the follow prompt. People need to SEE the product to want it, and the follow is
    what turns one view into a second one. 4,408 TikTok views have produced 1 follower,
    so the follow ask is not decoration.

    Everything sits above `content_bottom`. On TikTok the lower band of the frame is
    covered by the caption and username overlay, and an install ask nobody can read is
    the same as no install ask.
    """
    headline = text.split("Search '")[0].strip() if "Search '" in text else text
    y = spec.margin + spec.scale(70)
    y = draw_block(d, headline, spec.margin, y, spec.content_w, spec.scale(220),
                   ORANGE, spec, 66, 34)

    # Reserve the three closing lines first, then give the phone whatever is left.
    closing_h = spec.scale(230)
    avail = spec.content_bottom - y - closing_h - spec.scale(60)
    phone_h = max(spec.scale(320), min(spec.scale(680), int(avail)))

    phone = phone_mock(phone_h)
    buddy = load_pose(pose_name, int(phone_h * 0.52))

    # Center the phone and Buddy as one group, and keep the group clear of the
    # right-hand action rail on TikTok.
    overlap = spec.scale(40)
    group_w = phone.width + (buddy.width - overlap if buddy is not None else 0)
    max_group_w = spec.w - spec.margin - spec.right_rail - spec.margin
    if group_w > max_group_w:
        shrink = max_group_w / group_w
        phone = phone_mock(int(phone_h * shrink))
        if buddy is not None:
            buddy = load_pose(pose_name, int(buddy.height * shrink))
        group_w = phone.width + (buddy.width - overlap if buddy is not None else 0)

    gx = (spec.w - spec.right_rail - group_w) // 2
    py = int(y + spec.scale(30))
    img.paste(phone, (gx, py), phone)
    if buddy is not None:
        img.paste(buddy, (gx + phone.width - overlap,
                          py + phone.height - buddy.height), buddy)

    base = py + phone.height + spec.scale(44)
    size = _centered_fitted(d, "Download BiteBuddy, free on the App Store",
                            "Baloo2.ttf", spec.scale(46), CHARCOAL, base, spec)
    base += int(size * 1.35)
    size = _centered_fitted(d, "Search 'BiteBuddy: Ai calorie scanner'",
                            "Inter.ttf", spec.scale(30), SAGE, base, spec, weight=500)
    base += int(size * 1.6)

    # The follow ask. Every carousel carries it, whatever the post's primary CTA is.
    follow = "Follow @bitebuddyapp for more"
    ff = font("Baloo2.ttf", spec.scale(34), 700)
    tw = d.textlength(follow, font=ff)
    d.rounded_rectangle([(spec.w - tw) / 2 - spec.scale(28), base - spec.scale(12),
                         (spec.w + tw) / 2 + spec.scale(28), base + spec.scale(56)],
                        radius=spec.scale(34), fill=LAVENDER)
    d.text(((spec.w - tw) / 2, base), follow, font=ff, fill=CHARCOAL)


# --- dispatch -----------------------------------------------------------------------

def render_slide(post, idx, total, slide, spec):
    if isinstance(slide, dict):
        data = dict(slide)
    else:
        data = {"text": slide}
    kind = data.get("kind")
    text = data.get("text", "")

    img = Image.new("RGB", (spec.w, spec.h), CREAM)
    d = ImageDraw.Draw(img)
    is_cover, is_cta = idx == 0, idx == total - 1

    poses = post.get("poses") or DEFAULT_POSES
    cover_pose = poses[0] if len(poses) > 0 else DEFAULT_POSES[0]
    cta_pose = poses[1] if len(poses) > 1 else DEFAULT_POSES[1]

    accent(d, spec, idx)
    # A per-post badge beats the series default: an S2 episode ranking protein per 100
    # calories should not wear a chip that reads PROTEIN PER DOLLAR.
    badge(d, spec, post.get("series_badge", BADGES.get(post.get("series"), "")))

    if is_cta:
        slide_cta(d, img, spec, post, text, cta_pose)
        return img

    if is_cover:
        slide_cover(d, img, spec, post, text, data.get("image"), cover_pose)
    elif kind == "rank":
        slide_rank(d, spec, data.get("rank", idx), data.get("name", ""),
                   data.get("stat", ""), data.get("note", ""))
    elif kind == "compare":
        slide_compare(d, spec, data.get("a", {}), data.get("b", {}), data.get("banner", ""))
    elif kind == "grid":
        slide_grid(d, spec, data.get("rows", []), text)
    elif kind == "big":
        slide_big(d, spec, data.get("value", ""), text)
    elif kind == "step":
        slide_step(d, spec, data.get("step", idx), text, data.get("running", ""))
    elif data.get("image"):
        slide_image(d, img, spec, text, data["image"], data.get("style", "photo"))
    else:
        slide_type(d, spec, text, idx)

    progress(d, spec, idx, total)
    return img


def contact_sheet(paths, out_path, per_row=8):
    """One strip per deck so a human can actually eyeball a week before it schedules."""
    if not paths:
        return None
    thumbs = [Image.open(p).resize((216, int(216 * Image.open(p).height / Image.open(p).width)))
              for p in paths[:per_row]]
    w = sum(t.width for t in thumbs)
    h = max(t.height for t in thumbs)
    sheet = Image.new("RGB", (w, h), (240, 240, 240))
    x = 0
    for t in thumbs:
        sheet.paste(t, (x, 0))
        x += t.width
    sheet.save(out_path)
    return out_path


def main():
    ap = argparse.ArgumentParser(description=__doc__,
                                 formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("manifest", nargs="?", default="Posts/2026-W30/manifest.json")
    ap.add_argument("--format", choices=["tiktok", "ig", "both"], default="both")
    ap.add_argument("--contact-sheet", action="store_true",
                    help="also write a QA strip per deck")
    args = ap.parse_args()

    manifest = json.load(open(args.manifest))
    week_dir = os.path.dirname(args.manifest)
    formats = list(FORMATS) if args.format == "both" else [args.format]

    made = 0
    for post in manifest["posts"]:
        slides = post["slides"]
        for fmt in formats:
            spec = FORMATS[fmt]
            out = os.path.join(week_dir, post["id"], fmt)
            os.makedirs(out, exist_ok=True)
            paths = []
            for i, slide in enumerate(slides):
                img = render_slide(post, i, len(slides), slide, spec)
                fp = os.path.join(out, f"{i + 1:02d}.png")
                img.save(fp, optimize=True)
                paths.append(fp)
                made += 1
            if args.contact_sheet:
                contact_sheet(paths, os.path.join(week_dir, post["id"], f"_sheet-{fmt}.png"))
        print(f"{post['id']}: {len(slides)} slides x {len(formats)} format(s)")

    print(f"total {made} PNGs")
    print("Reminder: commit and push before scheduling, and reference the commit SHA "
          "in media URLs, never a branch name.")


if __name__ == "__main__":
    sys.exit(main() or 0)
