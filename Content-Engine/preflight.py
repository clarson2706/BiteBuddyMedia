#!/usr/bin/env python3
"""Preflight: the gate every routine run must pass before it touches anything.

The weekly loop has already failed twice in ways a five-second check would have
caught: a whole week of posts stranded on an unmerged branch (so the dedupe memory
on main never learned about them), and captions silently dropped because the wrong
kwarg name was used. This script turns every such lesson into an assertion.

    python3 Content-Engine/preflight.py                # human output, exit 1 on FAIL
    python3 Content-Engine/preflight.py --json         # machine output
    python3 Content-Engine/preflight.py --skip-network # offline checks only

Exit codes:
    0  clear to run (warnings may still be present)
    1  at least one FAIL: the run must stop and the failure must be fixed or
       explicitly overridden by Connor, never worked around silently
    2  preflight itself broke (treat as a FAIL)

Checks are deliberately blunt. A check that cannot decide returns WARN, never PASS.
"""
import argparse
import collections
import datetime as dt
import json
import os
import re
import subprocess
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
API = "https://api.upload-post.com/api"

# TikTok is the primary channel and 3/day is its ceiling, not a target. Instagram sits
# at 2 because the cap in HOOK-INTELLIGENCE-2026.md is 2 and the 2026-07-22 throttle
# landed there. See START-HERE.md rule 5.
DAILY_CAP = {"tiktok": 3, "instagram": 2, "youtube": 1, "facebook": 2}
MIN_GAP_MIN = 240  # minimum minutes between two posts on the same platform

results = []


def record(status, check, detail, fix=None):
    results.append({"status": status, "check": check, "detail": detail, "fix": fix})


def sh(*args):
    """Run a git command, returning stdout or None. Never raises."""
    try:
        out = subprocess.run(args, cwd=ROOT, capture_output=True, text=True, timeout=90)
        return out.stdout.strip() if out.returncode == 0 else None
    except Exception:
        return None


# --------------------------------------------------------------------------- offline

def check_dependencies():
    missing = []
    for mod, pkg in (("PIL", "pillow"), ("requests", "requests")):
        try:
            __import__(mod)
        except ImportError:
            missing.append(pkg)
    if missing:
        record("FAIL", "dependencies",
               f"missing Python packages: {', '.join(missing)}",
               f"pip install {' '.join(missing)}")
    else:
        record("PASS", "dependencies", "pillow and requests importable")


def check_assets():
    """Render inputs. A missing font or pose silently degrades every slide."""
    needed = [
        "Brand-Assets/fonts/Baloo2.ttf",
        "Brand-Assets/fonts/Inter.ttf",
        "Brand-Assets/buddy-poses/transparent/buddy_idle.png",
        "UI-Library/02-today-home/01-today-home.png",
    ]
    absent = [p for p in needed if not os.path.exists(os.path.join(ROOT, p))]
    if absent:
        record("FAIL", "render-assets", "missing: " + ", ".join(absent),
               "restore the assets before rendering; do not substitute generated art")
    else:
        poses = len(os.listdir(os.path.join(ROOT, "Brand-Assets/buddy-poses/transparent")))
        record("PASS", "render-assets", f"fonts, Today screenshot and {poses} Buddy cutouts present")


def check_stranded_branches():
    """Content memory that is not on main does not exist.

    The loop writes the registry, the performance log and the week's posts. If a run
    ends on a branch that is never merged, the next run regenerates topics it already
    published and the analytics join loses every post in between. This has happened.
    """
    if sh("git", "rev-parse", "--git-dir") is None:
        record("WARN", "stranded-branches", "not a git checkout, skipped")
        return
    sh("git", "fetch", "-q", "origin")
    heads = sh("git", "for-each-ref", "--format=%(refname:short)", "refs/remotes/origin/claude") or ""
    current = sh("git", "rev-parse", "--abbrev-ref", "HEAD")
    stranded = []
    for branch in [b for b in heads.splitlines() if b.strip()]:
        if branch.replace("origin/", "") == current:
            continue  # the branch this run is working on is allowed to be ahead
        merged = subprocess.run(["git", "merge-base", "--is-ancestor", branch, "origin/main"],
                                cwd=ROOT, capture_output=True)
        if merged.returncode == 0:
            continue
        touched = sh("git", "diff", "--name-only", f"origin/main...{branch}") or ""
        memory = [f for f in touched.splitlines()
                  if re.search(r"registry\.jsonl|performance-log\.jsonl|^Posts/|^Analytics/", f)]
        if memory:
            stranded.append((branch.replace("origin/", ""), len(memory)))
    if stranded:
        listing = "; ".join(f"{b} ({n} memory files)" for b, n in stranded)
        record("FAIL", "stranded-branches",
               f"{len(stranded)} unmerged branch(es) carry content memory main lacks: {listing}",
               "merge or explicitly abandon them before generating; otherwise the registry "
               "will duplicate topics and the analytics join will drop posts")
    else:
        record("PASS", "stranded-branches", "every claude/* branch is merged into main")


def _load_registry():
    path = os.path.join(ROOT, "Content-Engine/registry.jsonl")
    rows = []
    if os.path.exists(path):
        for line in open(path):
            line = line.strip()
            if line:
                try:
                    rows.append(json.loads(line))
                except json.JSONDecodeError:
                    record("WARN", "registry-parse", f"unparseable line: {line[:60]}")
    return rows


def check_registry_sane():
    rows = _load_registry()
    if not rows:
        record("FAIL", "registry", "registry.jsonl is empty — the dedupe memory does not exist",
               "the loop must append every generated post to it, every run")
        return rows
    ids = [r.get("post_id") for r in rows]
    dupes = [i for i, n in collections.Counter(ids).items() if n > 1]
    if dupes:
        record("WARN", "registry", f"duplicate post_ids: {', '.join(map(str, dupes[:5]))}")
    else:
        record("PASS", "registry", f"{len(rows)} posts recorded, ids unique")
    return rows


def check_directives_freshness(max_age_days=8):
    """Generation is gated on this run's directives. A stale file means the gate is
    being satisfied by an old run's output, which is the failure the gate exists for."""
    path = os.path.join(ROOT, "Analytics/next-week-directives.json")
    if not os.path.exists(path):
        record("FAIL", "directives", "next-week-directives.json missing",
               "Phase 1 must write it before Phase 2 generates anything")
        return
    try:
        data = json.load(open(path))
        stamp = dt.datetime.fromisoformat(data["generated_at"].replace("Z", "+00:00"))
    except Exception as exc:
        record("FAIL", "directives", f"unreadable generated_at: {exc}")
        return
    age = (dt.datetime.now(dt.timezone.utc) - stamp).days
    if age > max_age_days:
        record("FAIL", "directives",
               f"directives are {age} days old (generated {stamp.date()})",
               "run Phase 1 analytics first; generation may not read stale directives")
    else:
        record("PASS", "directives", f"generated {stamp.date()}, {age}d old, confidence "
                                     f"{data.get('confidence', 'unset')}")


def check_copy_lint():
    """Every manifest in the repo must survive the guardrail linter."""
    try:
        sys.path.insert(0, os.path.join(ROOT, "Content-Engine"))
        import copy_lint
    except Exception as exc:
        record("WARN", "copy-lint", f"linter unavailable: {exc}")
        return
    manifests = []
    posts_dir = os.path.join(ROOT, "Posts")
    for dirpath, _, files in os.walk(posts_dir):
        if "manifest.json" in files:
            manifests.append(os.path.join(dirpath, "manifest.json"))
    if not manifests:
        record("WARN", "copy-lint", "no manifests found to lint")
        return
    total = 0
    for m in manifests:
        try:
            issues = copy_lint.lint_manifest(m)
        except Exception as exc:
            record("WARN", "copy-lint", f"{os.path.relpath(m, ROOT)}: {exc}")
            continue
        blocking = [i for i in issues if i.severity == "FAIL"]
        total += len(blocking)
        for i in blocking[:6]:
            record("FAIL", "copy-lint", f"{os.path.relpath(m, ROOT)} [{i.post_id}] {i.message}",
                   "fix the copy; guardrails outrank every directive")
    if total == 0:
        record("PASS", "copy-lint", f"{len(manifests)} manifest(s) clean")


# --------------------------------------------------------------------------- network

def _api_get(path):
    import requests
    key = os.environ.get("UPLOAD_POST_API_KEY")
    resp = requests.get(f"{API}/{path}", headers={"Authorization": f"Apikey {key}"}, timeout=45)
    resp.raise_for_status()
    return resp.json()


def check_api_key():
    if not os.environ.get("UPLOAD_POST_API_KEY"):
        record("FAIL", "upload-post-key", "UPLOAD_POST_API_KEY is not set in this session",
               "environment variables apply at session start; add it in the environment "
               "settings and start a new session. Until then: stage and commit, publish nothing")
        return False
    record("PASS", "upload-post-key", "UPLOAD_POST_API_KEY present")
    return True


def check_platforms():
    """Which platforms are actually publishable right now.

    An empty string is not the same as a linked account. Instagram has read `""` since
    2026-07-29, which is a dropped token and a reconnect, not a ban.
    """
    try:
        data = _api_get("uploadposts/users")
    except Exception as exc:
        record("FAIL", "platform-links", f"list_users failed: {exc}",
               "cannot verify what is publishable; do not schedule blind")
        return set()
    profiles = data.get("profiles") or []
    if not profiles:
        record("FAIL", "platform-links", "no Upload-Post profiles on this key")
        return set()
    accounts = profiles[0].get("social_accounts") or {}
    live, dead = set(), []
    for name, val in accounts.items():
        if isinstance(val, dict) and val.get("handle"):
            live.add(name)
            if val.get("reauth_required"):
                record("WARN", "platform-links", f"{name} linked but flagged reauth_required")
        else:
            dead.append(name)
    plan = data.get("plan", "unknown")
    if "tiktok" not in live:
        record("FAIL", "platform-links", "TikTok is not linked and it is the primary channel",
               "reconnect TikTok in the Upload-Post dashboard before scheduling")
    else:
        record("PASS", "platform-links", f"live: {', '.join(sorted(live))} (plan: {plan})")
    if dead:
        record("WARN", "platform-links",
               f"not publishable: {', '.join(sorted(dead))} — skip these platforms and say so "
               f"in the report rather than scheduling to them")
    return live


def check_schedule_vs_registry(registry):
    """Everything scheduled on the live account must exist in the repo's memory.

    A post that is scheduled but absent from the registry is invisible to dedupe, to
    the analytics join and to Connor's veto window. This is exactly the state the
    account was in on 2026-07-31: nine posts scheduled, zero of them on main.
    """
    try:
        data = _api_get("uploadposts/schedule")
    except Exception as exc:
        record("WARN", "schedule-drift", f"could not read the live schedule: {exc}")
        return []
    scheduled = data.get("scheduled_posts") or []
    if not scheduled:
        record("PASS", "schedule-drift", "nothing scheduled on the live account")
        return scheduled

    known_titles = {(r.get("title") or "").strip().lower() for r in registry}
    orphans = [p for p in scheduled
               if (p.get("title") or "").strip().lower() not in known_titles]
    if orphans:
        sample = "; ".join(f'"{p.get("title", "")[:48]}"' for p in orphans[:4])
        record("FAIL", "schedule-drift",
               f"{len(orphans)} of {len(scheduled)} scheduled posts are absent from "
               f"registry.jsonl: {sample}",
               "the run that scheduled them never committed its manifest to main. Merge "
               "that work before generating, or the next batch will duplicate it")
    else:
        record("PASS", "schedule-drift",
               f"all {len(scheduled)} scheduled posts are present in the registry")
    return scheduled


def check_rate_limits(scheduled):
    """Enforce cadence on what is actually queued, not on what the plan intended.

    Five simultaneous posts on 2026-07-22 is the suspected cause of a throttle, so the
    thing that matters is spacing, checked against reality.
    """
    if not scheduled:
        record("PASS", "cadence", "nothing queued to check")
        return
    by_platform_day = collections.defaultdict(list)
    for post in scheduled:
        raw = post.get("original_scheduled_str") or post.get("scheduled_date")
        try:
            when = dt.datetime.fromisoformat(raw)
        except Exception:
            continue
        for platform in post.get("platforms") or []:
            by_platform_day[(platform, when.date())].append((when, post.get("title", "")))

    problems = []
    for (platform, day), items in sorted(by_platform_day.items()):
        cap = DAILY_CAP.get(platform, 3)
        if len(items) > cap:
            problems.append(f"{platform} has {len(items)} posts on {day} (cap {cap})")
        items.sort()
        for (a, _), (b, title) in zip(items, items[1:]):
            gap = (b - a).total_seconds() / 60
            if gap < MIN_GAP_MIN:
                problems.append(
                    f"{platform} {day}: only {int(gap)} min before \"{title[:36]}\" "
                    f"(minimum {MIN_GAP_MIN})")

    # Never two platforms in the same minute — the 2026-07-22 pattern.
    minutes = collections.defaultdict(set)
    for post in scheduled:
        raw = post.get("original_scheduled_str") or post.get("scheduled_date")
        try:
            when = dt.datetime.fromisoformat(raw)
        except Exception:
            continue
        for platform in post.get("platforms") or []:
            minutes[when].add(platform)
    for when, plats in minutes.items():
        if len(plats) > 1:
            problems.append(f"{', '.join(sorted(plats))} all publish at {when} (never simultaneous)")

    if problems:
        for p in problems[:8]:
            record("FAIL", "cadence", p, "respace the queue before adding to it")
    else:
        record("PASS", "cadence",
               f"{len(scheduled)} queued posts respect per-platform caps and {MIN_GAP_MIN}min spacing")


# --------------------------------------------------------------------------- driver

def main():
    ap = argparse.ArgumentParser(description=__doc__,
                                 formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--json", action="store_true", help="machine-readable output")
    ap.add_argument("--skip-network", action="store_true", help="offline checks only")
    args = ap.parse_args()

    check_dependencies()
    check_assets()
    check_stranded_branches()
    registry = check_registry_sane()
    check_directives_freshness()
    check_copy_lint()

    if not args.skip_network:
        if check_api_key():
            check_platforms()
            scheduled = check_schedule_vs_registry(registry)
            check_rate_limits(scheduled)
    else:
        record("WARN", "network-checks", "skipped by --skip-network; platform links, "
                                         "schedule drift and cadence are unverified")

    fails = [r for r in results if r["status"] == "FAIL"]
    warns = [r for r in results if r["status"] == "WARN"]

    if args.json:
        print(json.dumps({"ok": not fails, "fails": len(fails), "warns": len(warns),
                          "results": results}, indent=2))
    else:
        width = max(len(r["check"]) for r in results)
        for r in results:
            print(f"{r['status']:5} {r['check']:{width}}  {r['detail']}")
            if r["fix"] and r["status"] == "FAIL":
                print(f"{'':5} {'':{width}}  -> {r['fix']}")
        print()
        if fails:
            print(f"PREFLIGHT FAILED: {len(fails)} blocking problem(s), {len(warns)} warning(s).")
            print("Do not generate, render, schedule or publish until these are resolved.")
        else:
            print(f"Preflight clear. {len(warns)} warning(s) — read them, they are not noise.")

    return 1 if fails else 0


if __name__ == "__main__":
    try:
        sys.exit(main())
    except Exception as exc:  # a broken preflight is a failed preflight, never a pass
        print(f"PREFLIGHT ERROR: {exc}", file=sys.stderr)
        sys.exit(2)
