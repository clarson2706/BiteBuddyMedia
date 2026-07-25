#!/usr/bin/env python3
"""Pull every available media metric, join it to post metadata, and print the cuts.

Read-only against the platforms. Writes two things: an append to
Analytics/performance-log.jsonl (the permanent record) and a markdown report the
media-report skill turns into prose.

The joins that matter live in the manifests: each post carries its Upload-Post
request_id per platform, and get_post_analytics(request_id) returns that post's
real metrics. That is how a view count becomes "the POV hook on Instagram at
12:30 underperformed", which is the only form of analytics worth having.

Usage:
    python3 Analytics/report.py                 # last 14 days
    python3 Analytics/report.py --days 30
    python3 Analytics/report.py --json          # machine-readable to stdout
"""
import argparse, glob, json, os, statistics, sys
from collections import defaultdict
from datetime import datetime, timedelta, timezone

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
PROFILE = "Business_Posts"
PLATFORMS = ["tiktok", "instagram", "youtube", "facebook"]
LOG = os.path.join(ROOT, "Analytics", "performance-log.jsonl")

# The metric ladder from WEEKLY-LOOP.md, most meaningful first. Views are last on
# purpose: reach without response is not traction.
LADDER = ["app_comments", "shares", "saves", "comments", "likes", "views"]


def client():
    from upload_post import UploadPostClient
    key = os.environ.get("UPLOAD_POST_API_KEY")
    if not key:
        sys.exit("UPLOAD_POST_API_KEY is not set in this session. "
                 "It is applied at session start, so a session that began before the "
                 "variable was added will not see it.")
    return UploadPostClient(key)


def unwrap(r):
    return r.get("result", r) if isinstance(r, dict) else r


def load_posts():
    """Every post we have ever scheduled, with its metadata and per-platform ids."""
    out = []
    for mf in sorted(glob.glob(os.path.join(ROOT, "Posts", "*", "manifest.json"))):
        m = json.load(open(mf))
        for p in m.get("posts", []):
            # Collect every request_id attached to this post, wherever it was stored:
            # scheduled_jobs, a flat per-platform dict, or the legacy flat field. We do
            # not guess which platform an id belongs to; the API response says.
            rids = set()
            for job in (p.get("scheduled_jobs") or {}).values():
                if isinstance(job, dict) and job.get("request_id"):
                    rids.add(job["request_id"])
            for plat in PLATFORMS:
                v = p.get(plat)
                if isinstance(v, dict) and v.get("request_id"):
                    rids.add(v["request_id"])
            if p.get("upload_post_request_id"):
                rids.add(p["upload_post_request_id"])
            jobs = sorted(rids)
            out.append({
                "post_id": p["id"], "week": m.get("week"), "date": p.get("date"),
                "time_local": p.get("time_local"), "title": p.get("title"),
                "series": p.get("series"), "persona": p.get("persona"),
                "hook_family": p.get("hook_family"), "visual_recipe": p.get("visual_recipe"),
                "cta_type": p.get("cta_type"), "jobs": jobs,
                "published": p.get("published") or {},
            })
    return out


def per_post_metrics(c, posts, days):
    """Real metrics per post per platform, via request_id."""
    cutoff = datetime.now(timezone.utc) - timedelta(days=days)
    rows = []
    for p in posts:
        if p["date"]:
            try:
                if datetime.fromisoformat(p["date"]).replace(tzinfo=timezone.utc) < cutoff:
                    continue
            except ValueError:
                pass
        for rid in p["jobs"]:
            try:
                d = unwrap(c.get_post_analytics(rid))
            except Exception:
                continue                      # not published yet, or no data
            for plat, info in (d.get("platforms") or {}).items():
                if not isinstance(info, dict) or not info.get("success"):
                    continue
                met = info.get("post_metrics") or {}
                rows.append({**{k: p[k] for k in
                                ["post_id", "week", "date", "time_local", "title", "series",
                                 "persona", "hook_family", "visual_recipe", "cta_type"]},
                             "platform": plat,
                             "url": info.get("post_url"),
                             "views": met.get("views") or 0,
                             "likes": met.get("likes") or 0,
                             "comments": met.get("comments") or 0,
                             "shares": met.get("shares") or 0,
                             "saves": met.get("saves") or 0})
    return rows


def account_snapshots(c):
    out = {}
    try:
        a = unwrap(c.get_analytics(PROFILE, platforms=PLATFORMS))
    except Exception as e:
        return {"_error": str(e)}
    for plat, v in (a or {}).items():
        if isinstance(v, dict):
            out[plat] = v
    return out


def cut(rows, key):
    """Aggregate rows by a metadata field."""
    g = defaultdict(lambda: {"posts": 0, "views": 0, "likes": 0,
                             "comments": 0, "shares": 0, "saves": 0})
    for r in rows:
        k = r.get(key) or "unset"
        g[k]["posts"] += 1
        for m in ["views", "likes", "comments", "shares", "saves"]:
            g[k][m] += r.get(m) or 0
    for k, v in g.items():
        v["eng"] = v["likes"] + v["comments"] + v["shares"] + v["saves"]
        v["eng_rate"] = (v["eng"] / v["views"] * 100) if v["views"] else 0.0
        v["views_per_post"] = v["views"] / v["posts"] if v["posts"] else 0
    return dict(sorted(g.items(), key=lambda kv: -kv[1]["views"]))


def prior_snapshot(platform):
    """Most recent account snapshot for this platform already in the log."""
    if not os.path.exists(LOG):
        return None
    best = None
    for line in open(LOG):
        line = line.strip()
        if not line:
            continue
        try:
            r = json.loads(line)
        except json.JSONDecodeError:
            continue
        if r.get("platform") == platform and r.get("post_id") in (
                "ACCOUNT-SNAPSHOT", "PRE-RESET-AGGREGATE"):
            if best is None or (r.get("captured_at") or "") > (best.get("captured_at") or ""):
                best = r
    return best


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--days", type=int, default=14)
    ap.add_argument("--json", action="store_true")
    ap.add_argument("--no-write", action="store_true")
    a = ap.parse_args()

    c = client()
    posts = load_posts()
    rows = per_post_metrics(c, posts, a.days)
    accounts = account_snapshots(c)
    now = datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")

    result = {"captured_at": now, "window_days": a.days,
              "posts_with_data": len(rows), "per_post": rows, "accounts": {},
              "cuts": {}, "warnings": []}

    for plat, v in accounts.items():
        if plat.startswith("_"):
            continue
        prev = prior_snapshot(plat)
        cur = {k: v.get(k) for k in
               ["followers", "impressions", "reach", "likes", "comments",
                "shares", "saves", "profileViews", "video_count"]}
        delta = {}
        if prev:
            for k, label in [("impressions", "views"), ("followers", "followers"),
                             ("likes", "likes"), ("comments", "comments")]:
                if cur.get(k) is not None and prev.get(label) is not None:
                    try:
                        delta[k] = cur[k] - prev[label]
                    except TypeError:
                        pass
        ts = [x for x in (v.get("reach_timeseries") or []) if x.get("value") is not None]
        result["accounts"][plat] = {"current": cur, "delta_since_last_report": delta,
                                    "daily": ts[-14:]}

    for key in ["series", "persona", "hook_family", "visual_recipe",
                "cta_type", "platform", "time_local"]:
        result["cuts"][key] = cut(rows, key)

    # Honesty guards. These exist because a confident read of four data points is
    # how a content system talks itself into the wrong strategy.
    n = len(rows)
    if n < 8:
        result["warnings"].append(
            f"Only {n} post-platform rows in this window. Every cut below is anecdote, "
            "not trend. Report direction at most, never a verdict, and do not kill or "
            "scale a series on this evidence.")
    total_eng = sum(r["likes"] + r["comments"] + r["shares"] + r["saves"] for r in rows)
    if total_eng == 0 and rows:
        result["warnings"].append(
            "Zero engagement across every post in the window. That is a content signal, "
            "not a distribution one: the people who saw these felt nothing worth acting on.")
    result["warnings"].append(
        "Engagement counts include any interaction from our own accounts. Before calling "
        "a comment a win, confirm it came from a stranger. This has already produced one "
        "wrong conclusion (2026-07-25).")

    if a.json:
        print(json.dumps(result, indent=2))
        return

    print(f"MEDIA REPORT  {now}   window {a.days}d   {n} post-platform rows")
    for w in result["warnings"]:
        print(f"  !! {w}")
    for plat, d in result["accounts"].items():
        cur, dl = d["current"], d["delta_since_last_report"]
        print(f"\n{plat.upper()}  followers={cur.get('followers')} "
              f"views={cur.get('impressions')} likes={cur.get('likes')} "
              f"comments={cur.get('comments')}"
              + (f"   delta: {dl}" if dl else ""))
        if d["daily"]:
            print("   daily: " + ", ".join(f"{x['date'][5:]}={x['value']}" for x in d["daily"][-8:]))
    if rows:
        print("\nPER POST")
        for r in sorted(rows, key=lambda r: -r["views"]):
            print(f"  {r['date']} {r['time_local']:>5} {r['platform']:9} "
                  f"v={r['views']:5} l={r['likes']:3} c={r['comments']:3} s={r['shares']:3}  "
                  f"[{r['series']}/{r['hook_family']}/{r['cta_type']}] {r['title'][:44]}")
        for key in ["platform", "series", "hook_family", "cta_type", "visual_recipe"]:
            print(f"\nBY {key.upper()}")
            for k, v in result["cuts"][key].items():
                print(f"  {str(k):22} posts={v['posts']:2} views={v['views']:5} "
                      f"eng={v['eng']:3} eng_rate={v['eng_rate']:.2f}% "
                      f"v/post={v['views_per_post']:.0f}")

    if not a.no_write:
        with open(LOG, "a") as f:
            for r in rows:
                f.write(json.dumps({**r, "captured_at": now,
                                    "source": "media-report"}) + "\n")
            for plat, d in result["accounts"].items():
                f.write(json.dumps({"post_id": "ACCOUNT-SNAPSHOT", "platform": plat,
                                    "captured_at": now, "source": "media-report",
                                    **{("views" if k == "impressions" else k): val
                                       for k, val in d["current"].items()}}) + "\n")
        print(f"\nappended {len(rows)} post rows + {len(result['accounts'])} snapshots to "
              f"{os.path.relpath(LOG, ROOT)}")


if __name__ == "__main__":
    main()
