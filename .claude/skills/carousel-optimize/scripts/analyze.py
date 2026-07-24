#!/usr/bin/env python3
"""
Roll up the performance ledger into a leaderboard + next-week directives.

Reads the append-only ledger written by record_metrics.py, keeps the LATEST
snapshot per (post_id, platform, profile), scores each post, aggregates by every
creative dimension (format, hook_type, topic, cover_style, hashtag, time slot,
platform, profile), and emits:

  Marketing/Analytics/leaderboard.json         # full machine-readable rollup
  Marketing/Analytics/next-week-directives.json# compact steer for carousel-week
  Marketing/Analytics/next-week-directives.md  # the same, human-readable

carousel-week reads the directives at the top of its Sunday run and biases the
new week toward what's winning and away from what's flopping — so the creatives
compound instead of resetting each week. Pure stdlib; no network.

Scoring (documented in references/scoring.md):
  engagement_rate = (likes + 2*comments + 3*shares + 3*saves) / max(views, 1)
    (saves & shares are weighted highest — they're the strongest intent/virality
     signals per the marketing playbook)
  A dimension value needs >= MIN_SAMPLE posts to be a "confident" call; fewer is
  reported as tentative.

Usage:
  python analyze.py [--log ...] [--out-dir Marketing/Analytics]
                    [--weeks N] [--min-sample 3] [--top 5]
"""
import argparse, datetime, json, os, statistics, sys
from collections import defaultdict

DEFAULT_LOG = "Marketing/Analytics/performance-log.jsonl"
DEFAULT_OUT = "Marketing/Analytics"
# creative dimensions we aggregate on. tags.* are read dynamically too.
CORE_DIMS = ["format", "platform", "profile", "slot"]
TAG_DIMS = ["hook_type", "topic", "cover_style"]   # scalar tags
LIST_TAG_DIMS = ["hashtags"]                        # list-valued tags (exploded)


def load_latest(log_path, weeks_filter):
    """Return the latest snapshot per (post_id, platform, profile)."""
    if not os.path.isfile(log_path):
        return []
    latest = {}
    with open(log_path) as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            try:
                s = json.loads(line)
            except ValueError:
                continue
            if weeks_filter and s.get("week") not in weeks_filter:
                continue
            key = (s.get("post_id"), s.get("platform"), s.get("profile"))
            prev = latest.get(key)
            if prev is None or str(s.get("pulled_at", "")) >= str(prev.get("pulled_at", "")):
                latest[key] = s
    return list(latest.values())


def score(snap):
    m = snap.get("metrics", {}) or {}
    def num(k):
        try:
            return float(m.get(k, 0) or 0)
        except (TypeError, ValueError):
            return 0.0
    views = num("views")
    eng = num("likes") + 2 * num("comments") + 3 * num("shares") + 3 * num("saves")
    eng_rate = eng / views if views > 0 else 0.0
    return views, eng_rate


def dims_of(snap):
    """Yield (dim_name, value) pairs for this snapshot."""
    for d in CORE_DIMS:
        v = snap.get(d) if d != "slot" else snap.get("slot") or _slot_from(snap)
        if v:
            yield d, str(v)
    tags = snap.get("tags") or {}
    for d in TAG_DIMS:
        if tags.get(d):
            yield d, str(tags[d])
    for d in LIST_TAG_DIMS:
        for v in tags.get(d, []) or []:
            yield d, str(v)


def _slot_from(snap):
    # allow slot to be derived from posted_at time if not explicit
    pa = snap.get("posted_at") or ""
    if "T" in pa:
        hhmm = pa.split("T", 1)[1][:5]
        return hhmm or None
    return None


def aggregate(snaps):
    """dimension -> value -> {n, median_views, median_eng_rate}"""
    buckets = defaultdict(lambda: defaultdict(list))
    for s in snaps:
        views, eng_rate = score(s)
        for dim, val in dims_of(s):
            buckets[dim][val].append((views, eng_rate))
    out = {}
    for dim, vals in buckets.items():
        rows = []
        for val, pairs in vals.items():
            vv = [p[0] for p in pairs]
            ee = [p[1] for p in pairs]
            rows.append({
                "value": val, "n": len(pairs),
                "median_views": round(statistics.median(vv)),
                "median_eng_rate": round(statistics.median(ee), 4),
            })
        # rank by engagement rate, then reach
        rows.sort(key=lambda r: (r["median_eng_rate"], r["median_views"]), reverse=True)
        out[dim] = rows
    return out


def top_posts(snaps, n):
    scored = []
    for s in snaps:
        views, eng_rate = score(s)
        scored.append({
            "post_id": s.get("post_id"), "platform": s.get("platform"),
            "week": s.get("week"), "format": s.get("format"),
            "views": round(views), "eng_rate": round(eng_rate, 4),
            "title": (s.get("tags") or {}).get("title") or s.get("title"),
            "composite": round(eng_rate * 1000 + views / 1000, 2),
        })
    scored.sort(key=lambda r: r["composite"], reverse=True)
    return scored


def pick(rows, min_sample, top, best=True):
    """Top/bottom dimension values that clear the sample threshold."""
    conf = [r for r in rows if r["n"] >= min_sample]
    pool = conf if conf else rows           # fall back to tentative if nothing confident
    ordered = pool if best else list(reversed(pool))
    return ordered[:top], bool(conf)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--log", default=DEFAULT_LOG)
    ap.add_argument("--out-dir", default=DEFAULT_OUT)
    ap.add_argument("--weeks", type=int, default=0,
                    help="limit to the N most recent ISO weeks in the log (0 = all)")
    ap.add_argument("--min-sample", type=int, default=3)
    ap.add_argument("--top", type=int, default=5)
    args = ap.parse_args()

    weeks_filter = None
    if args.weeks and os.path.isfile(args.log):
        all_weeks = sorted({json.loads(l).get("week")
                            for l in open(args.log) if l.strip()} - {None})
        weeks_filter = set(all_weeks[-args.weeks:])

    snaps = load_latest(args.log, weeks_filter)
    os.makedirs(args.out_dir, exist_ok=True)

    if not snaps:
        msg = ("No performance data in the ledger yet. Run record_metrics.py after "
               "the first week's posts have matured, then re-run analyze.")
        for name, payload in [
            ("leaderboard.json", {"generated_at": _now(), "n_posts": 0, "note": msg}),
            ("next-week-directives.json", {"generated_at": _now(), "n_posts": 0,
                                           "status": "no-data", "note": msg}),
        ]:
            _write_json(os.path.join(args.out_dir, name), payload)
        _write(os.path.join(args.out_dir, "next-week-directives.md"),
               f"# Next-week directives\n\n_{msg}_\n\n"
               "Until data exists, carousel-week runs on the base playbook.\n")
        print(msg)
        return 0

    agg = aggregate(snaps)
    posts = top_posts(snaps, args.top)
    weeks_covered = sorted({s.get("week") for s in snaps} - {None})

    lean, dial = {}, {}
    confidence_flags = []
    for dim in ["format"] + TAG_DIMS + ["slot", "platform"]:
        rows = agg.get(dim)
        if not rows:
            continue
        conf = any(r["n"] >= args.min_sample for r in rows)
        conf_rows = [r for r in rows if r["n"] >= args.min_sample] or rows
        # split the ranked values into a winning head and a losing tail so lean
        # and dial are always distinct (never swallow the whole list)
        head_n = min(args.top, max(1, len(conf_rows) // 2))
        lean[dim] = [r["value"] for r in conf_rows[:head_n]]
        tail = conf_rows[head_n:]
        dial[dim] = [r["value"] for r in reversed(tail)][:args.top]  # worst first
        if not conf:
            confidence_flags.append(dim)

    best_hashtags = [r["value"] for r in agg.get("hashtags", [])[:args.top]]
    overall_conf = ("low" if len(snaps) < args.min_sample * 3
                    else "medium" if confidence_flags else "high")

    directives = {
        "generated_at": _now(),
        "weeks_covered": weeks_covered,
        "n_posts": len(snaps),
        "confidence": overall_conf,
        "low_confidence_dimensions": confidence_flags,
        "lean_into": lean,
        "dial_back": dial,
        "best_slots": lean.get("slot", []),
        "best_platforms": lean.get("platform", []),
        "best_hashtags": best_hashtags,
        "recut_winners": posts[:args.top],
        "avoid_losers": posts[-args.top:][::-1] if len(posts) > args.top else [],
    }
    leaderboard = {
        "generated_at": _now(), "weeks_covered": weeks_covered,
        "n_posts": len(snaps), "dimensions": agg, "posts_ranked": posts,
    }

    _write_json(os.path.join(args.out_dir, "leaderboard.json"), leaderboard)
    _write_json(os.path.join(args.out_dir, "next-week-directives.json"), directives)
    _write(os.path.join(args.out_dir, "next-week-directives.md"),
           render_md(directives))

    print(f"Analyzed {len(snaps)} post-snapshots across weeks {weeks_covered} "
          f"(confidence: {overall_conf})")
    print(f"  LEAN INTO  format={lean.get('format')} topic={lean.get('topic')} "
          f"slot={lean.get('slot')} platform={lean.get('platform')}")
    print(f"  wrote directives → {args.out_dir}/next-week-directives.md")
    return 0


def render_md(d):
    def line(k):
        vals = d["lean_into"].get(k) or []
        return ", ".join(vals) if vals else "—"
    md = [f"# Next-week directives  ({d['generated_at'][:10]})", ""]
    md.append(f"Based on **{d['n_posts']}** post-snapshots across "
              f"{', '.join(d['weeks_covered']) or 'n/a'}. "
              f"Confidence: **{d['confidence']}**.")
    if d["low_confidence_dimensions"]:
        md.append(f"> Tentative (small sample): "
                  f"{', '.join(d['low_confidence_dimensions'])}.")
    md += ["", "## Lean into (what's winning)",
           f"- **Formats:** {line('format')}",
           f"- **Hook types:** {line('hook_type')}",
           f"- **Topics:** {line('topic')}",
           f"- **Cover styles:** {line('cover_style')}",
           f"- **Best time slots:** {', '.join(d['best_slots']) or '—'}",
           f"- **Best platforms:** {', '.join(d['best_platforms']) or '—'}",
           f"- **Best hashtags:** {', '.join(d['best_hashtags']) or '—'}",
           "", "## Dial back (underperforming)"]
    for k in ["format", "hook_type", "topic", "cover_style"]:
        vals = d["dial_back"].get(k) or []
        if vals:
            md.append(f"- **{k}:** {', '.join(vals)}")
    md += ["", "## Re-cut these winners (fresh cover, same skeleton)"]
    for p in d["recut_winners"]:
        md.append(f"- `{p['post_id']}` ({p.get('format') or '?'}, {p['platform']}) "
                  f"— {p['views']:,} views, {p['eng_rate']*100:.1f}% eng")
    md += ["", "## How carousel-week should use this",
           "Bias the 21 new posts toward the lean-into values above; allocate "
           "extra slots to the top format/topic; re-cut each winner with a fresh "
           "cover; avoid the dial-back values. Keep all guardrails.", ""]
    return "\n".join(md)


def _now():
    return datetime.datetime.now().isoformat(timespec="seconds")


def _write(path, text):
    with open(path, "w") as f:
        f.write(text)


def _write_json(path, obj):
    with open(path, "w") as f:
        json.dump(obj, f, indent=2)
        f.write("\n")


if __name__ == "__main__":
    raise SystemExit(main())
