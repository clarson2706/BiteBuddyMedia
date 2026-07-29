#!/usr/bin/env python3
"""Render BiteBuddy carousel slides from a week's manifest.json.

Produces 1080x1350 PNGs per the archetypes in DESIGN-SYSTEM.md, using the brand
palette, the rounded brand font, and the real Buddy cutouts. Written because
Canva's generate-design only emits one page per call, which cannot build an
8-slide carousel, and this environment cannot download Canva exports anyway
(see Content-Engine/TEMPLATES.md).

Output goes to Posts/<week>/<post-id>/NN.png. The repo is public, so those files
are then reachable at raw.githubusercontent.com and can be handed straight to
Upload-Post's upload_photos as public URLs.

Usage:  python3 Content-Engine/render_slides.py Posts/2026-W30/manifest.json
"""
import json, os, sys, textwrap
from PIL import Image, ImageDraw, ImageFont

W, H = 1080, 1350
MARGIN = 90
CREAM = (255, 248, 241)
PEACH = (244, 162, 97)
ORANGE = (233, 132, 58)
SAGE = (143, 162, 127)
LAVENDER = (201, 196, 242)
CHARCOAL = (58, 58, 58)

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
FONT_DIR = os.path.join(ROOT, "Brand-Assets", "fonts")
POSE_DIR = os.path.join(ROOT, "Brand-Assets", "buddy-poses", "transparent")
# The real Today dashboard. HARD REQUIREMENT: the final slide of every carousel shows
# this screenshot inside a phone silhouette, never a text-only "it's on the App Store".
TODAY_SHOT = os.path.join(ROOT, "UI-Library", "02-today-home", "01-today-home.png")

# Which Buddy pose hosts the cover and the CTA, by post id. Chosen to match the
# emotional beat (see Brand-Assets/buddy-poses/README.md).
POSES = {
    "2026-07-25-slot1": ("buddy_thinking", "buddy_level_up"),
    "2026-07-25-slot2": ("buddy_warning_check", "buddy_fiber_shield"),
    "2026-07-26-slot1": ("buddy_thinking", "buddy_balanced_glow"),
    "2026-07-26-slot2": ("buddy_warning_check", "buddy_goal_celebration"),
    "2026-07-25-flex1": ("buddy_thinking", "buddy_goal_celebration"),
    "2026-07-28-flex1": ("buddy_thinking", "buddy_protein_powerup"),
    "2026-07-28-slot2": ("buddy_warning_check", "buddy_level_up"),
    "2026-07-29-slot1": ("buddy_thinking", "buddy_goal_celebration"),
    "2026-07-29-flex1": ("buddy_idle", "buddy_fiber_shield"),
    "2026-07-29-slot2": ("buddy_thinking", "buddy_goal_celebration"),
    "2026-07-30-slot1": ("buddy_protein_powerup", "buddy_protein_powerup"),
    "2026-07-30-flex1": ("buddy_balanced_glow", "buddy_balanced_glow"),
    "2026-07-30-slot2": ("buddy_warning_check", "buddy_level_up"),
    "2026-07-31-slot1": ("buddy_thinking", "buddy_protein_powerup"),
    "2026-07-31-flex1": ("buddy_happy", "buddy_balanced_glow"),
    "2026-07-31-slot2": ("buddy_warning_check", "buddy_balanced_glow"),
    "2026-08-01-slot1": ("buddy_thinking", "buddy_protein_powerup"),
    "2026-08-01-flex1": ("buddy_idle", "buddy_level_up"),
    "2026-08-01-slot2": ("buddy_warning_check", "buddy_balanced_glow"),
    "2026-08-02-slot1": ("buddy_thinking", "buddy_goal_celebration"),
    "2026-08-02-flex1": ("buddy_warning_check", "buddy_level_up"),
    "2026-08-02-slot2": ("buddy_thinking", "buddy_goal_celebration"),
    "2026-07-30-slot2-recut": ("buddy_thinking", "buddy_protein_powerup"),
    "2026-08-02-flex1-recut": ("buddy_thinking", "buddy_protein_powerup"),
}
BADGES = {"S3": "WHY TRACKING FAILS", "S1": "GUESS THE CALORIES",
          "S2": "PROTEIN PER DOLLAR", "oneoff": ""}


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


def load_pose(name, target_h):
    p = os.path.join(POSE_DIR, name + ".png")
    if not os.path.exists(p):
        return None
    im = Image.open(p).convert("RGBA")
    r = target_h / im.height
    return im.resize((int(im.width * r), target_h), Image.LANCZOS)


def phone_mock(screen_h=690):
    """The real Today screenshot inside a simple phone silhouette."""
    shot = Image.open(TODAY_SHOT).convert("RGB")
    # crop to the dashboard hero so the rings and numbers read at feed size
    shot = shot.crop((0, 0, shot.width, int(shot.height * 0.72)))
    sw = int(screen_h * shot.width / shot.height)
    shot = shot.resize((sw, screen_h), Image.LANCZOS)

    bez, radius = 14, 46
    pw, ph = sw + bez * 2, screen_h + bez * 2
    phone = Image.new("RGBA", (pw, ph), (0, 0, 0, 0))
    pd = ImageDraw.Draw(phone)
    pd.rounded_rectangle([0, 0, pw - 1, ph - 1], radius=radius, fill=(38, 38, 42, 255))

    mask = Image.new("L", (sw, screen_h), 0)
    ImageDraw.Draw(mask).rounded_rectangle([0, 0, sw - 1, screen_h - 1],
                                           radius=radius - bez, fill=255)
    phone.paste(shot, (bez, bez), mask)
    return phone


def image_block(rel_path, style, max_w, max_h):
    """A real photo or a real screenshot, scaled into the slide.

    Never a mock. `photo` gets rounded corners; `phone` gets the same dark
    silhouette as phone_mock() so app screenshots read as the app.
    """
    im = Image.open(os.path.join(ROOT, rel_path)).convert("RGB")
    bez, radius = (14, 46) if style == "phone" else (0, 40)
    inner_w, inner_h = max_w - bez * 2, max_h - bez * 2
    scale = min(inner_w / im.width, inner_h / im.height)
    iw, ih = int(im.width * scale), int(im.height * scale)
    im = im.resize((iw, ih), Image.LANCZOS)

    out = Image.new("RGBA", (iw + bez * 2, ih + bez * 2), (0, 0, 0, 0))
    if bez:
        ImageDraw.Draw(out).rounded_rectangle([0, 0, out.width - 1, out.height - 1],
                                              radius=radius, fill=(38, 38, 42, 255))
    mask = Image.new("L", (iw, ih), 0)
    ImageDraw.Draw(mask).rounded_rectangle([0, 0, iw - 1, ih - 1],
                                           radius=max(radius - bez, 18), fill=255)
    out.paste(im, (bez, bez), mask)
    return out


def badge(draw, img, text):
    if not text:
        return
    f = font("Baloo2.ttf", 30, 700)
    tw = draw.textlength(text, font=f)
    pad_x, pad_y, h = 26, 12, 56
    draw.rounded_rectangle([MARGIN, MARGIN, MARGIN + tw + pad_x * 2, MARGIN + h],
                           radius=h // 2, fill=LAVENDER)
    draw.text((MARGIN + pad_x, MARGIN + pad_y - 2), text, font=f, fill=CHARCOAL)


def render_cta(post, img, d, text, cta_pose):
    """Final slide: topic CTA + the real Today dashboard in a phone + download line."""
    # the App Store search line lives at the bottom of this slide, so strip it from the
    # headline when the post's CTA text already carries it
    headline = text.split("Search '")[0].strip() if "Search '" in text else text
    f, lines, lh = fit_text(d, headline, "Baloo2.ttf", 62, 34, W - MARGIN * 2, 210, 700)
    y = 128
    for line in lines:
        d.text(((W - d.textlength(line, font=f)) / 2, y), line, font=f, fill=ORANGE)
        y += lh

    phone = phone_mock(690)
    px, py = (W - phone.width) // 2 - 96, y + 34
    img.paste(phone, (px, py), phone)

    buddy = load_pose(cta_pose, 360)
    if buddy is not None:
        img.paste(buddy, (px + phone.width - 44, py + phone.height - buddy.height + 18), buddy)

    fd = font("Baloo2.ttf", 44, 700)
    dl = "Download BiteBuddy, free on the App Store"
    d.text(((W - d.textlength(dl, font=fd)) / 2, H - 148), dl, font=fd, fill=CHARCOAL)

    if post.get("cta_type") == "APP":
        fs = font("Inter.ttf", 30, 500)
        sl = "Search 'BiteBuddy: Ai calorie scanner'"
        d.text(((W - d.textlength(sl, font=fs)) / 2, H - 92), sl, font=fs, fill=SAGE)
    return img


def render_slide(post, idx, total, slide):
    # a slide is either a string or {"text", "image", "style"} when it carries a
    # real photo or screenshot
    if isinstance(slide, dict):
        text, image, style = slide["text"], slide.get("image"), slide.get("style", "photo")
    else:
        text, image, style = slide, None, "photo"

    img = Image.new("RGB", (W, H), CREAM)
    d = ImageDraw.Draw(img)
    is_cover, is_cta = idx == 0, idx == total - 1
    cover_pose, cta_pose = POSES.get(post["id"], ("buddy_idle", "buddy_happy"))

    # soft accent shapes, varied per slide so the deck does not look stamped
    if idx % 3 == 0:
        d.ellipse([W - 210, -110, W + 150, 250], fill=PEACH)
    elif idx % 3 == 1:
        d.rounded_rectangle([-90, H - 240, 190, H + 90], radius=70, fill=LAVENDER)
    else:
        d.ellipse([-130, H - 200, 150, H + 110], fill=SAGE)

    badge(d, img, BADGES.get(post.get("series"), ""))

    if is_cta:
        return render_cta(post, img, d, text, cta_pose)

    if image:
        # headline on top, the real thing underneath, filling the slide
        f, lines, lh = fit_text(d, text, "Baloo2.ttf", 74 if is_cover else 60, 34,
                                W - MARGIN * 2, 250, 700)
        y = MARGIN + 40
        for line in lines:
            d.text(((W - d.textlength(line, font=f)) / 2, y), line, font=f,
                   fill=ORANGE if is_cover else CHARCOAL)
            y += lh

        block = image_block(image, style, W - MARGIN * 2, H - y - 120)
        img.paste(block, ((W - block.width) // 2, y + 34), block)

        if is_cover:
            pose = load_pose(cover_pose, 250)
            if pose is not None:
                img.paste(pose, (W - pose.width - 30, H - pose.height - 20), pose)
        else:
            fs = font("Inter.ttf", 26, 500)
            d.text((MARGIN, H - 60), f"{idx + 1}/{total}", font=fs, fill=SAGE)
        return img

    if is_cover:
        pose = load_pose(cover_pose, 470)
        box_h = 620
    else:
        pose = None
        box_h = 780

    colour = ORANGE if (is_cover or is_cta) else CHARCOAL
    max_size = 92 if is_cover else (78 if is_cta else 72)
    f, lines, lh = fit_text(d, text, "Baloo2.ttf", max_size, 34,
                            W - MARGIN * 2, box_h, 700)

    block_h = len(lines) * lh
    y = MARGIN + 130 if (is_cover or is_cta) else (H - block_h) // 2 - 40
    for line in lines:
        d.text(((W - d.textlength(line, font=f)) / 2, y), line, font=f, fill=colour)
        y += lh

    if pose is not None:
        img.paste(pose, ((W - pose.width) // 2, H - pose.height - 40), pose)

    # slide counter, quiet, bottom-left; skipped on the branded cover and CTA
    if not is_cover and not is_cta:
        fs = font("Inter.ttf", 26, 500)
        d.text((MARGIN, H - 78), f"{idx + 1}/{total}", font=fs, fill=SAGE)
    return img


def main(manifest_path):
    m = json.load(open(manifest_path))
    week_dir = os.path.dirname(manifest_path)
    made = []
    for post in m["posts"]:
        out = os.path.join(week_dir, post["id"])
        os.makedirs(out, exist_ok=True)
        slides = post["slides"]
        for i, text in enumerate(slides):
            img = render_slide(post, i, len(slides), text)
            fp = os.path.join(out, f"{i + 1:02d}.png")
            img.save(fp, optimize=True)
            made.append(fp)
        print(f"{post['id']}: {len(slides)} slides")
    print(f"total {len(made)} PNGs")


if __name__ == "__main__":
    main(sys.argv[1] if len(sys.argv) > 1 else "Posts/2026-W30/manifest.json")
