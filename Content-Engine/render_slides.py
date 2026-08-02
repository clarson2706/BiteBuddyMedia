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
import json, os, sys, textwrap, zlib
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

# Which Buddy pose hosts the cover and the CTA, by post id. Hand-picked for the posts
# that shipped before pose selection was automated; kept so those decks keep the poses
# they were published with. New posts need no entry here (see pick_poses).
POSES = {
    "2026-07-25-slot1": ("buddy_thinking", "buddy_level_up"),
    "2026-07-25-slot2": ("buddy_warning_check", "buddy_fiber_shield"),
    "2026-07-26-slot1": ("buddy_thinking", "buddy_balanced_glow"),
    "2026-07-26-slot2": ("buddy_warning_check", "buddy_goal_celebration"),
    "2026-07-25-flex1": ("buddy_thinking", "buddy_goal_celebration"),
}
BADGES = {"S3": "WHY TRACKING FAILS", "S1": "GUESS THE CALORIES",
          "S2": "PROTEIN PER DOLLAR", "DEMO": "", "oneoff": ""}

# Automatic pose selection, so a generated post renders without anyone hand-mapping it.
# Cover pose = the question the hook asks; CTA pose = the payoff. Both are real app
# renders from Brand-Assets/buddy-poses/transparent/, never generated. The legacy map
# above still wins for the posts it names, so their hand-picked poses are preserved.
POSE_BY_HOOK = {
    "GUESS": "buddy_thinking", "QUIZ": "buddy_thinking",
    "LIST": "buddy_idle", "CHEAT": "buddy_idle", "ORDER": "buddy_idle",
    "TRACKED": "buddy_sugar_crash", "RIGHTWRONG": "buddy_warning_check",
    "HABIT": "buddy_thinking", "OUTCOME": "buddy_balanced_glow",
    "POV": "buddy_idle", "MISTAKE": "buddy_warning_check",
}
POSE_BY_SERIES = {          # (cover fallback, CTA payoff)
    "S1": ("buddy_thinking", "buddy_goal_celebration"),
    "S2": ("buddy_idle", "buddy_protein_powerup"),
    "S3": ("buddy_sugar_crash", "buddy_level_up"),
    "DEMO": ("buddy_thinking", "buddy_balanced_glow"),
}
DEFAULT_POSES = ("buddy_idle", "buddy_happy")

# Slide roles from CAROUSEL-CONVERSION-SPEC.md §2. Roles are optional: a manifest that
# names none falls back to cover-first / CTA-last, which is how the pre-spec decks work.
COVER_ROLES = {"HOOK", "COVER"}
CTA_ROLES = {"CTA"}
PHONE_ROLES = {"PROOF"}     # the receipts slide always renders the screen as a phone


def pick_poses(post):
    """(cover_pose, cta_pose), derived rather than hand-mapped.

    Order of precedence: explicit poses on the post, the legacy per-id map, then the
    series/hook derivation. Every branch returns real canonical poses.
    """
    explicit = post.get("poses")
    if isinstance(explicit, (list, tuple)) and len(explicit) == 2:
        return tuple(explicit)
    if post["id"] in POSES:
        return POSES[post["id"]]
    cover, cta = POSE_BY_SERIES.get(post.get("series"), DEFAULT_POSES)
    hook_pose = POSE_BY_HOOK.get(post.get("hook_family"), cover)
    # the cover asks and the CTA pays off, so they should not be the same pose
    return (cover if hook_pose == cta else hook_pose), cta


VARIANTS = 5   # raised from 3 on 2026-08-02, when TikTok went to 4 posts/day


def variant_of(post):
    """Which of the five layout looks this deck wears, 0 to 4.

    The anti-slop rule in DESIGN-SYSTEM.md requires consecutive posts not to share an
    identical layout. Derived from the post id so it is stable across re-renders and
    spreads without anyone choosing it. Five rather than three because at 4 posts/day
    a three-look rotation repeats twice within a single day's grid, which is exactly
    the templated read TikTok's 2026 crackdown penalises.
    """
    if isinstance(post.get("variant"), int):
        return post["variant"] % VARIANTS
    # crc32, not a character sum: post ids within a week differ by only a word or two
    # ("...-morning" vs "...-midday"), and a plain sum maps those to the same bucket,
    # which put three identical layouts in one day the first time this ran. Generation
    # should still set "variant" explicitly so a day is guaranteed four distinct looks;
    # this is the fallback for manifests that do not.
    return zlib.crc32(post["id"].encode()) % VARIANTS


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


def badge(draw, img, text, right=False):
    if not text:
        return
    f = font("Baloo2.ttf", 30, 700)
    tw = draw.textlength(text, font=f)
    pad_x, pad_y, h = 26, 12, 56
    x = W - MARGIN - tw - pad_x * 2 if right else MARGIN
    draw.rounded_rectangle([x, MARGIN, x + tw + pad_x * 2, MARGIN + h],
                           radius=h // 2, fill=LAVENDER)
    draw.text((x + pad_x, MARGIN + pad_y - 2), text, font=f, fill=CHARCOAL)


def accents(d, variant, idx):
    """The soft background shapes. Three looks, rotated per deck by variant_of().

    DESIGN-SYSTEM.md's anti-slop rule: consecutive posts must not share an identical
    layout. Variant 0 is the original look, so decks that hash to it are unchanged.
    """
    if variant == 0:
        if idx % 3 == 0:
            d.ellipse([W - 210, -110, W + 150, 250], fill=PEACH)
        elif idx % 3 == 1:
            d.rounded_rectangle([-90, H - 240, 190, H + 90], radius=70, fill=LAVENDER)
        else:
            d.ellipse([-130, H - 200, 150, H + 110], fill=SAGE)
    elif variant == 1:
        if idx % 3 == 0:
            d.ellipse([-160, -140, 220, 240], fill=LAVENDER)
        elif idx % 3 == 1:
            d.rounded_rectangle([W - 200, H - 260, W + 110, H + 80], radius=70, fill=PEACH)
        else:
            d.rounded_rectangle([W - 230, -120, W + 90, 180], radius=70, fill=SAGE)
    elif variant == 2:
        # a quiet vertical bar plus one corner arc: the most typographic of the five
        bar = PEACH if idx % 2 == 0 else SAGE
        d.rounded_rectangle([0, 210, 26, H - 210], radius=13, fill=bar)
        if idx % 3 == 2:
            d.ellipse([W - 190, H - 190, W + 130, H + 130], fill=LAVENDER)
    elif variant == 3:
        # horizontal rails top and bottom: reads as a card, holds a grid together
        rail = [PEACH, SAGE, LAVENDER][idx % 3]
        d.rectangle([0, 0, W, 22], fill=rail)
        d.rectangle([0, H - 22, W, H], fill=rail)
        if idx % 3 == 1:
            d.ellipse([W - 150, H - 250, W + 120, H + 20], fill=LAVENDER)
    else:
        # inset outline plus one solid corner block: the most graphic of the five
        block = [SAGE, PEACH, LAVENDER][idx % 3]
        d.rounded_rectangle([40, 40, W - 40, H - 40], radius=54,
                            outline=block, width=10)
        if idx % 2 == 0:
            d.rounded_rectangle([W - 300, -80, W + 80, 120], radius=48, fill=block)
        else:
            d.rounded_rectangle([-80, H - 120, 300, H + 80], radius=48, fill=block)


def slide_role(slide, idx, total):
    """The slide's job, per CAROUSEL-CONVERSION-SPEC.md §2.

    Manifests may name roles explicitly. Older ones do not, so fall back to the shape
    every deck has had since the start: first slide covers, last slide asks.
    """
    if isinstance(slide, dict) and slide.get("role"):
        return slide["role"].upper()
    if idx == 0:
        return "HOOK"
    if idx == total - 1:
        return "CTA"
    return "VALUE"


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


def draw_lines(d, lines, f, y, lh, colour, left=False):
    for line in lines:
        x = MARGIN + 34 if left else (W - d.textlength(line, font=f)) / 2
        d.text((x, y), line, font=f, fill=colour)
        y += lh
    return y


def save_chip(d):
    """The screenshot-me marker on the SAVE slide. Its own visual so the save ask is
    not just a sentence competing with the content."""
    f = font("Baloo2.ttf", 30, 700)
    text = "SAVE THIS"
    tw = d.textlength(text, font=f)
    x0, y0 = W - MARGIN - tw - 52, H - 148
    d.rounded_rectangle([x0, y0, x0 + tw + 52, y0 + 56], radius=28, fill=ORANGE)
    d.text((x0 + 26, y0 + 10), text, font=f, fill=CREAM)


def render_slide(post, idx, total, slide):
    # a slide is either a string or {"text", "image", "style", "role"} when it carries a
    # real photo or screenshot, or fills a named role from the conversion spec
    if isinstance(slide, dict):
        text, image, style = slide["text"], slide.get("image"), slide.get("style", "photo")
    else:
        text, image, style = slide, None, "photo"

    role = slide_role(slide, idx, total)
    is_cover, is_cta = role in COVER_ROLES, role in CTA_ROLES
    if role in PHONE_ROLES and image:
        style = "phone"          # receipts always read as the app, never as a loose photo

    img = Image.new("RGB", (W, H), CREAM)
    d = ImageDraw.Draw(img)
    cover_pose, cta_pose = pick_poses(post)
    var = variant_of(post)
    left = var in (2, 4) and not is_cover and not is_cta

    accents(d, var, idx)
    # the closer is already branded by the phone and the download line; a series chip
    # there only competes with the headline
    badge_text = "" if is_cta else BADGES.get(post.get("series"), "")
    badge(d, img, badge_text, right=(var == 1))

    if is_cta:
        return render_cta(post, img, d, text, cta_pose)

    if image:
        # headline on top, the real thing underneath, filling the slide
        f, lines, lh = fit_text(d, text, "Baloo2.ttf", 74 if is_cover else 60, 34,
                                W - MARGIN * 2, 250, 700)
        # clear the series chip rather than running the headline through it
        y = draw_lines(d, lines, f, MARGIN + (110 if badge_text else 40), lh,
                       ORANGE if is_cover else CHARCOAL, left)

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

    if role == "SAVE":
        # the dense, saveable slide sits on a card so it reads as a reference, not prose
        d.rounded_rectangle([MARGIN - 30, 300, W - MARGIN + 30, H - 300],
                            radius=56, fill=LAVENDER)
        box_h = 620

    colour = ORANGE if is_cover else (SAGE if role == "HONEST" else CHARCOAL)
    max_size = 92 if is_cover else (56 if role == "HONEST" else 72)
    f, lines, lh = fit_text(d, text, "Baloo2.ttf", max_size, 34,
                            W - MARGIN * 2, box_h, 700)

    block_h = len(lines) * lh
    if is_cover:
        y = MARGIN + 130
    elif role == "SAVE":
        y = (H - block_h) // 2          # centred in the card, not offset above it
    else:
        y = (H - block_h) // 2 - 40
    draw_lines(d, lines, f, y, lh, colour, left)

    if pose is not None:
        img.paste(pose, ((W - pose.width) // 2, H - pose.height - 40), pose)

    if role == "SAVE":
        save_chip(d)

    # slide counter, quiet, bottom-left; skipped on the branded cover and CTA
    if not is_cover:
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
