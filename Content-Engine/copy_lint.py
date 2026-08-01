#!/usr/bin/env python3
"""Guardrail linter: the content rules, enforced in code instead of in good intentions.

`CLAUDE.md` lists guardrails that outrank every directive and every trend. Until now
the only thing enforcing them was whoever happened to be writing the batch. This file
makes them assertions a run can fail.

    python3 Content-Engine/copy_lint.py Posts/2026-W31/manifest.json
    python3 Content-Engine/copy_lint.py --all          # every manifest in Posts/
    python3 Content-Engine/copy_lint.py --text "some caption to check"

FAIL means the copy may not publish. WARN means it is probably weaker than it should
be. When in doubt the linter reports rather than stays quiet: a false warning costs a
few seconds, a medical claim on a live post costs the account.
"""
import argparse
import glob
import json
import os
import re
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# The canonical App Store search line. The source of truth is
# BiteBuddyMVP/APP_STORE_METADATA.md; this constant must match it exactly.
APP_STORE_SEARCH = "BiteBuddy: Ai calorie scanner"

# --- Guardrails from CLAUDE.md. Each pattern cites the rule it enforces. ------------

MEDICAL_CLAIMS = [
    (r"\blose\s+\d+\s*(lbs?|pounds?|kgs?|kilos?)\b", "outcome claim: a specific weight-loss promise"),
    (r"\b(guaranteed|guarantee)\b", "outcome claim: guarantee language"),
    (r"\bburns?\s+fat\b", "outcome claim: fat-burning"),
    (r"\bmelts?\s+(away\s+)?(fat|pounds|weight)\b", "outcome claim: melting fat or weight"),
    (r"\b(cures?|treats?|heals?|reverses?)\s+\w+", "medical claim: cure, treat, heal or reverse"),
    (r"\b(prevents?|stops?)\s+(diabetes|cancer|disease|illness)\b", "medical claim: disease prevention"),
    (r"\bdoctor\s+recommended\b", "medical claim: implied clinical endorsement"),
    (r"\b(detox|cleanse)\b", "pseudo-medical framing"),
    (r"\b(starve|starving|starvation)\b", "disordered-eating framing"),
    (r"\bcrash\s+diet\b", "disordered-eating framing"),
    (r"\bnever\s+eat\s+\w+\s+again\b", "restriction framing"),
    (r"\b(bad|forbidden|off-limits|clean\s+only)\s+foods?\b", "moralizing food framing; no food is bad"),
    (r"\bcalorie\s+deficit\s+guarantee", "outcome claim"),
    (r"\bdrop\s+\d+\s*(lbs?|pounds?)\b", "outcome claim: a specific weight-loss promise"),
]

PRECISION_CLAIMS = [
    (r"\b100%\s+accurat\w*", "precision claim: app numbers are estimates the user reviews"),
    (r"\bperfectly\s+accurat\w*", "precision claim"),
    (r"\bexact\s+(calories|macros|numbers)\b", "precision claim: claim consistency, never precision"),
    (r"\bnever\s+wrong\b", "precision claim"),
    (r"\bprecise\s+(to\s+the\s+)?(gram|calorie)\b", "precision claim"),
]

BANNED_FEATURES = [
    (r"\bmeal\s+advisor\b", "the Meal Advisor ships disabled and must never be featured"),
]

# House rule, for trust reasons: em dashes read as an AI tell in outbound copy.
EM_DASH = re.compile(r"[—–]")

CTA_TYPES = {"APP", "FOLLOW", "COMMENT", "SAVE_OR_SHARE"}


class Issue:
    def __init__(self, severity, post_id, field, message):
        self.severity = severity
        self.post_id = post_id
        self.field = field
        self.message = message

    def __str__(self):
        return f"{self.severity:4}  {self.post_id:26} {self.field:16} {self.message}"


def _slide_text(slide):
    """A slide is a bare string, or a dict when it carries a real photo/screenshot."""
    if isinstance(slide, dict):
        return slide.get("text", "")
    return slide or ""


def lint_text(text, post_id="-", field="text", outbound=True):
    """Check one string of outbound copy against the guardrails."""
    issues = []
    if not text:
        return issues
    low = text.lower()

    for pattern, why in MEDICAL_CLAIMS + PRECISION_CLAIMS + BANNED_FEATURES:
        if re.search(pattern, low):
            issues.append(Issue("FAIL", post_id, field, f"{why} — matched /{pattern}/"))

    if outbound and EM_DASH.search(text):
        issues.append(Issue("FAIL", post_id, field,
                            "em or en dash in outbound copy (house rule: none, anywhere)"))
    return issues


def lint_post(post):
    """Check one manifest post: slides, caption, pinned comment, CTA and hashtags."""
    issues = []
    pid = post.get("id", "?")
    slides = post.get("slides") or []

    for i, slide in enumerate(slides):
        text = _slide_text(slide)
        issues += lint_text(text, pid, f"slide {i + 1}")
        words = len(text.split())
        if words > 22:
            issues.append(Issue("WARN", pid, f"slide {i + 1}",
                                f"{words} words; slides read at feed size, aim for under 15"))

    for field in ("caption", "pinned_comment", "cta", "title"):
        issues += lint_text(post.get(field, ""), pid, field)

    # Structure rules from DESIGN-SYSTEM.md and HOOK-INTELLIGENCE-2026.md.
    if not slides:
        issues.append(Issue("FAIL", pid, "slides", "post has no slides"))
    elif not 5 <= len(slides) <= 10:
        issues.append(Issue("WARN", pid, "slides",
                            f"{len(slides)} slides; 5 to 8 is the researched band, 10 is the ceiling"))

    # The CTA slide is a hard requirement. Note what the renderer already injects:
    # render_slides.render_cta() always draws "Download BiteBuddy, free on the App Store"
    # and adds the search line when cta_type is APP. So the final slide's *text* is the
    # topic line above the phone, and it must not try to repeat either injected line.
    cta_type = post.get("cta_type")
    if cta_type and cta_type not in CTA_TYPES:
        issues.append(Issue("FAIL", pid, "cta_type",
                            f"unknown cta_type {cta_type!r}; expected one of {sorted(CTA_TYPES)}"))
    if not cta_type:
        issues.append(Issue("WARN", pid, "cta_type",
                            "no cta_type; the weekly CTA mix cannot be balanced without it"))

    if slides:
        last = _slide_text(slides[-1]).strip()
        if not last:
            issues.append(Issue("FAIL", pid, "cta slide", "final slide has no topic CTA line"))
        if "free on the app store" in last.lower():
            issues.append(Issue("WARN", pid, "cta slide",
                                "the download line is injected by the renderer; repeating it "
                                "here prints it twice"))

    # An APP-CTA post is the one that names the search phrase. It is injected on the CTA
    # slide, so this only has to hold in the caption for platforms that read captions.
    if cta_type == "APP":
        caption = (post.get("caption") or "") + " " + (post.get("cta") or "")
        if APP_STORE_SEARCH.lower() not in caption.lower() and \
                "apps.apple.com" not in caption.lower():
            issues.append(Issue("WARN", pid, "cta",
                                f"APP-CTA post: caption names neither the search phrase "
                                f"\"{APP_STORE_SEARCH}\" nor the App Store link. The CTA slide "
                                f"carries it, but the caption is the searchable copy"))

    tags = post.get("hashtags") or []
    if tags and not 3 <= len(tags) <= 8:
        issues.append(Issue("WARN", pid, "hashtags",
                            f"{len(tags)} hashtags; 3 to 8 targeted tags, stuffing is penalised"))

    if not post.get("persona"):
        issues.append(Issue("WARN", pid, "persona", "no persona named; every post targets one"))

    return issues


def lint_manifest(path):
    data = json.load(open(path))
    issues = []
    for post in data.get("posts", []):
        issues += lint_post(post)
    return issues


def main():
    ap = argparse.ArgumentParser(description=__doc__,
                                 formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("manifest", nargs="*", help="manifest.json path(s)")
    ap.add_argument("--all", action="store_true", help="lint every manifest under Posts/")
    ap.add_argument("--text", help="lint one string instead of a manifest")
    args = ap.parse_args()

    if args.text:
        issues = lint_text(args.text)
        for i in issues:
            print(i)
        print("clean" if not issues else f"{len(issues)} issue(s)")
        return 1 if any(i.severity == "FAIL" for i in issues) else 0

    paths = list(args.manifest)
    if args.all or not paths:
        paths = sorted(glob.glob(os.path.join(ROOT, "Posts", "**", "manifest.json"),
                                 recursive=True))
    if not paths:
        print("no manifests found")
        return 0

    all_issues = []
    for path in paths:
        issues = lint_manifest(path)
        all_issues += issues
        rel = os.path.relpath(path, ROOT)
        print(f"\n=== {rel} ===")
        if not issues:
            print("  clean")
        for i in issues:
            print(f"  {i}")

    fails = [i for i in all_issues if i.severity == "FAIL"]
    warns = [i for i in all_issues if i.severity == "WARN"]
    print(f"\n{len(fails)} FAIL, {len(warns)} WARN across {len(paths)} manifest(s)")
    return 1 if fails else 0


if __name__ == "__main__":
    sys.exit(main())
