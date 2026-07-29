#!/usr/bin/env python3
"""growth.py — deterministic engine for the growth-report skill.

Merges every layer of the funnel into one dated snapshot and prints the
computed digest the skill writes prose around. All judgement lives in the
skill; everything numeric and repeatable lives here.

Inputs (collection happens outside this script):
  --mcp PATH      JSON the skill writes after pulling RevenueCat + Supabase via
                  MCP tools (schema: Reports/README.md, "sources" contract below)
  --social PATH   output of `Analytics/report.py --days N --json` (optional)
  --date YYYY-MM-DD  snapshot date (default: today UTC)
  --no-write      compute and print, skip writing the snapshot
  --json          print the full snapshot instead of the digest

Also reads, directly from the repo, degrading to null when absent:
  Analytics/installs.jsonl        App Store Connect weekly numbers (hand-entered)
  Outreach/creators.jsonl         creator pipeline
  Outreach/payouts.jsonl          creator payouts owed/paid
  Outreach/batches/*.md           DM batches written
  Reports/*-snapshot.json         previous runs, for deltas

Writes Reports/<date>-snapshot.json. Never talks to a network. Never edits an
existing snapshot. Missing sources become nulls + flags, never zeros.
"""
import argparse, glob, json, math, os, re, sys
from datetime import datetime, timezone

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
REPORTS = os.path.join(ROOT, "Reports")

APPLE_CUT = 0.15          # Small Business Program (confirmed in plan review)
MONTHLY_PRICE = 7.99      # live pricing per SPRINT-AUG25.md
HORIZONS = [30, 60, 90]
STALE_DAYS = 7            # installs.jsonl older than this renders STALE


def read_jsonl(path):
    rows = []
    if not os.path.exists(path):
        return None
    with open(path) as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            try:
                rows.append(json.loads(line))
            except json.JSONDecodeError:
                continue
    return rows


def wilson(successes, n, z=1.64):
    """~90% Wilson score interval for a proportion; (lo, point, hi)."""
    if not n:
        return (None, None, None)
    p = successes / n
    denom = 1 + z * z / n
    center = (p + z * z / (2 * n)) / denom
    half = z * math.sqrt(p * (1 - p) / n + z * z / (4 * n * n)) / denom
    return (max(0.0, center - half), p, min(1.0, center + half))


# ---------- layers ----------

def social_layer(path, flags):
    if not path or not os.path.exists(path):
        flags.append("social: no report.py output supplied; social layer null")
        return {"window_days": None, "posts_with_data": None, "totals": None,
                "by_platform": None}
    d = json.load(open(path))
    totals = {k: 0 for k in ["views", "likes", "comments", "shares", "saves"]}
    by_plat = {}
    for r in d.get("per_post", []):
        plat = r.get("platform", "?")
        b = by_plat.setdefault(plat, {k: 0 for k in totals} | {"posts": 0})
        b["posts"] += 1
        for k in totals:
            v = r.get(k) or 0
            totals[k] += v
            b[k] += v
    # follower counts, when the account snapshot exposes them under any name
    for plat, acct in (d.get("accounts") or {}).items():
        cur = acct.get("current") if isinstance(acct, dict) else None
        if isinstance(cur, dict):
            f = next((cur[k] for k in
                      ("followers", "follower_count", "subscribers", "fans")
                      if isinstance(cur.get(k), (int, float))), None)
            by_plat.setdefault(plat, {}).update({"followers": f})
    return {"window_days": d.get("window_days"),
            "posts_with_data": d.get("posts_with_data"),
            "totals": totals, "by_platform": by_plat}


def store_layer(today, flags):
    rows = read_jsonl(os.path.join(ROOT, "Analytics", "installs.jsonl"))
    if not rows:
        flags.append("store: Analytics/installs.jsonl missing/empty — App Store "
                     "stage is DARK; funnel below Reach is unanchored")
        return {"week": None, "impressions": None, "product_page_views": None,
                "downloads": None, "age_days": None, "stale": True}
    last = rows[-1]
    # age from the ISO week's Monday; good enough for a staleness gate
    age = None
    m = re.match(r"(\d{4})-W(\d{2})", str(last.get("week", "")))
    if m:
        monday = datetime.fromisocalendar(int(m.group(1)), int(m.group(2)), 1)
        age = (today - monday.date()).days
    stale = age is None or age > STALE_DAYS + 7   # a weekly number covers 7 days
    if stale:
        flags.append(f"store: installs.jsonl latest week {last.get('week')} is "
                     f"~{age}d old — STALE")
    return {"week": last.get("week"), "impressions": last.get("impressions"),
            "product_page_views": last.get("product_page_views"),
            "downloads": last.get("downloads"), "age_days": age, "stale": stale}


def outreach_layer(flags):
    creators = read_jsonl(os.path.join(ROOT, "Outreach", "creators.jsonl")) or []
    payouts = read_jsonl(os.path.join(ROOT, "Outreach", "payouts.jsonl")) or []
    by_status = {}
    live_posts = 0
    for c in creators:
        by_status[c.get("status", "?")] = by_status.get(c.get("status", "?"), 0) + 1
        live_posts += len(c.get("posts") or [])
    deal_states = {"deal", "deal_agreed", "signed", "posting", "posted", "live"}
    deals = sum(n for s, n in by_status.items() if s in deal_states)
    batches = len(glob.glob(os.path.join(ROOT, "Outreach", "batches", "*")))
    if not creators:
        flags.append("outreach: creators.jsonl empty")
    return {"creators_tracked": len(creators), "by_status": by_status,
            "deals": deals, "live_posts": live_posts, "batches": batches,
            "payout_rows": len(payouts)}


def revenue_layer(mcp, flags):
    rc = (mcp or {}).get("revenuecat") or {}
    sb = (mcp or {}).get("supabase") or {}
    out = {"mrr_gross": rc.get("mrr"), "revenue_28d": rc.get("revenue_28d"),
           "active_subscriptions_rc": rc.get("active_subscriptions"),
           "active_trials_rc": rc.get("active_trials"),
           "new_customers_28d": rc.get("new_customers_28d"),
           "active_users_28d": rc.get("active_users_28d"),
           "paying_subs_supabase": sb.get("paying_subs_production"),
           "trial_subs_supabase": sb.get("trial_subs_production"),
           "apple_cut": APPLE_CUT, "arpu_gross": None, "mrr_net_est": None}
    if not rc:
        flags.append("revenue: no RevenueCat section in --mcp input")
    subs, mrr = out["active_subscriptions_rc"], out["mrr_gross"]
    if subs and mrr is not None:
        out["arpu_gross"] = round(mrr / subs, 2)
    if mrr is not None:
        out["mrr_net_est"] = round(mrr * (1 - APPLE_CUT), 2)
    a, b = out["active_subscriptions_rc"], out["paying_subs_supabase"]
    if a is not None and b is not None and a != b:
        flags.append(f"revenue: RevenueCat says {a} active sub(s) but Supabase "
                     f"mirror says {b} production paying row(s) — likely app_user_id "
                     "aliasing; RevenueCat is authoritative for subscriber count, "
                     "report the discrepancy")
    return out


def product_layer(mcp, flags):
    sb = (mcp or {}).get("supabase") or {}
    if not sb:
        flags.append("product: no Supabase section in --mcp input")
    keys = ["users_total", "signups_7d", "signups_28d", "onboarded_total",
            "first_scan_users", "wau", "scans_7d", "logs_7d", "excluded_testers"]
    out = {k: sb.get(k) for k in keys}
    out["d1"] = sb.get("d1") or {"cohort": None, "retained": None}
    out["d7"] = sb.get("d7") or {"eligible": None, "retained": None}
    return out


# ---------- funnel ----------

def build_funnel(social, store, product, revenue):
    """Stage list top→bottom. conv_to_next only where both counts exist.
    Windows differ per stage (7d/weekly/28d/lifetime) and the digest labels
    them; conversions across mismatched windows are directional, not exact."""
    tot = social.get("totals") or {}
    engagement = None
    if tot:
        engagement = sum(tot.get(k) or 0 for k in
                         ["likes", "comments", "shares", "saves"])
    stages = [
        ("reach (views, window)", (tot or {}).get("views")),
        ("engagement (likes+comments+shares+saves)", engagement),
        ("store page views (wk)", store.get("product_page_views")),
        ("downloads (wk)", store.get("downloads")),
        ("signups (7d)", product.get("signups_7d")),
        ("active trials", revenue.get("active_trials_rc")),
        ("PAYING = activated", revenue.get("active_subscriptions_rc")),
    ]
    out = []
    for i, (name, count) in enumerate(stages):
        conv = None
        if i + 1 < len(stages):
            nxt = stages[i + 1][1]
            if count and nxt is not None:
                conv = round(nxt / count, 4)
        out.append({"name": name, "count": count, "conv_to_next": conv})
    # bottleneck hint: first DARK stage, else worst known conversion
    hint = ""
    for s in out[:-1]:
        if s["count"] is None:
            hint = f"DATA GAP at '{s['name']}' — fix measurement before tactics"
            break
    if not hint:
        known = [s for s in out[:-1] if s["conv_to_next"] is not None
                 and (s["count"] or 0) > 0]
        if known:
            worst = min(known, key=lambda s: s["conv_to_next"])
            hint = (f"worst conversion is '{worst['name']}' → next "
                    f"({worst['conv_to_next']:.2%})")
    return {"stages": out, "bottleneck_hint": hint}


# ---------- projections ----------

def project(revenue, store, social, flags):
    """Three scenarios over 30/60/90 days. Every number traceable to the
    assumptions list. Ranges from the Wilson interval on observed pay rate."""
    new28 = revenue.get("new_customers_28d")
    paying = revenue.get("active_subscriptions_rc")
    arpu = revenue.get("arpu_gross") or MONTHLY_PRICE
    mrr_now = revenue.get("mrr_gross") or 0

    # installs/day: fresh App Store downloads if we have them, else RC
    # new-customers as a labelled proxy (an account is created post-install)
    if store.get("downloads") is not None and not store.get("stale"):
        ipd, ipd_src = store["downloads"] / 7.0, "App Store downloads/7"
    elif new28:
        ipd, ipd_src = new28 / 28.0, "PROXY: RevenueCat new_customers_28d/28"
        flags.append("projections: installs/day is a proxy from RevenueCat "
                     "new-customers; paste App Store numbers to replace it")
    else:
        return {"horizon_days": HORIZONS, "scenarios": None,
                "note": "no install-rate source at all; refusing to project"}

    lo, pt, hi = wilson(paying or 0, new28) if new28 else (None, None, None)
    if pt is None:
        return {"horizon_days": HORIZONS, "scenarios": None,
                "note": "no observed pay rate; refusing to project"}

    conf = "low" if (new28 or 0) >= 50 else "none"

    def run(ipd_path, rate_band, label, extra_assump):
        """ipd_path: fn(day)->installs that day. Returns per-horizon bands."""
        subs, mrrg, mrrn, dls = [], [], [], []
        for h in HORIZONS:
            installs = sum(ipd_path(d) for d in range(1, h + 1))
            band = []
            for r in rate_band:
                s = (paying or 0) + installs * r
                band.append(s)
            subs.append([round(b, 1) for b in band])
            mrrg.append([round(max(b * arpu, mrr_now)) for b in band])
            mrrn.append([round(max(b * arpu, mrr_now) * (1 - APPLE_CUT))
                         for b in band])
            dls.append(round(installs))
        return {"label": label, "confidence": conf,
                "assumptions": [
                    f"installs/day source: {ipd_src}",
                    f"observed pay rate {paying or 0}/{new28} = {pt:.1%}, "
                    f"90% interval [{lo:.1%}, {hi:.1%}] (n={new28} is small; "
                    "treat the width seriously)",
                    f"ARPU ${arpu:.2f}/mo gross; net = gross x {1-APPLE_CUT:.2f} "
                    "(Apple Small Business Program)",
                    "churn assumed 0 over the horizon — the assumption most "
                    "likely to break; one cancel changes everything at this n",
                    "creator 30% first-payment share not modelled (no attributed "
                    "creator installs yet)",
                ] + extra_assump,
                "downloads": dls, "subs": subs,
                "mrr_gross": mrrg, "mrr_net": mrrn}

    scenarios = {
        "current": run(lambda d: ipd, (lo, pt, hi),
                       "current trajectory, nothing changes",
                       [f"flat {ipd:.2f} installs/day"]),
        "sprint": run(lambda d: ipd if d <= 7 else 10.0, (0.02, 0.02, 0.02),
                      "SPRINT-AUG25 plan lands",
                      ["10 installs/day from day 8 (W32 checkpoint) and 2% "
                       "install→pay held, both per SPRINT-AUG25.md — plan "
                       "numbers, not observations"]),
    }
    # breakout: the account's own best observed reach multiple applied to
    # install rate — not an invented viral number
    mult = None
    per_plat = (social.get("by_platform") or {})
    views = [p.get("views") for p in per_plat.values()
             if isinstance(p, dict) and p.get("views")]
    posts = sum(p.get("posts") or 0 for p in per_plat.values()
                if isinstance(p, dict))
    if views and posts:
        avg = sum(views) / max(posts, 1)
        best = max(views)
        if avg > 0:
            mult = max(2.0, round(best / avg, 1))
    if mult:
        scenarios["breakout"] = run(
            lambda d: ipd * (mult if d <= 7 else 2.0), (lo, pt, hi),
            "one post/creator hits",
            [f"week 1 installs x{mult} (account's own best-post reach vs its "
             "average), then a sustained 2x baseline"])
    else:
        flags.append("projections: no social views available, breakout "
                     "scenario skipped")
    return {"horizon_days": HORIZONS, "scenarios": scenarios,
            "pay_rate_interval_90": [lo, pt, hi], "installs_per_day": ipd,
            "installs_per_day_source": ipd_src}


# ---------- deltas ----------

SCORECARD = [
    ("mrr_gross", ("revenue", "mrr_gross")),
    ("active_subscriptions", ("revenue", "active_subscriptions_rc")),
    ("active_trials", ("revenue", "active_trials_rc")),
    ("new_customers_28d", ("revenue", "new_customers_28d")),
    ("downloads_wk", ("store", "downloads")),
    ("signups_7d", ("product", "signups_7d")),
    ("wau", ("product", "wau")),
    ("views_window", ("social", "totals", "views")),
    ("engagement_window", None),   # computed
    ("creators_tracked", ("outreach", "creators_tracked")),
    ("creator_posts_live", ("outreach", "live_posts")),
]


def dig(snap, path):
    cur = snap
    for k in path:
        if not isinstance(cur, dict):
            return None
        cur = cur.get(k)
    return cur


def scorecard_values(snap):
    vals = {}
    for name, path in SCORECARD:
        if name == "engagement_window":
            t = dig(snap, ("social", "totals")) or {}
            vals[name] = (sum(t.get(k) or 0 for k in
                              ["likes", "comments", "shares", "saves"])
                          if t else None)
        else:
            vals[name] = dig(snap, path)
    return vals


def deltas_vs_previous(snap, date_str):
    prev_files = sorted(f for f in glob.glob(os.path.join(REPORTS, "*-snapshot.json"))
                        if os.path.basename(f) < f"{date_str}-snapshot.json")
    if not prev_files:
        return {"vs": None}
    prev = json.load(open(prev_files[-1]))
    cur_v, prev_v = scorecard_values(snap), scorecard_values(prev)
    out = {"vs": prev.get("date")}
    for k, v in cur_v.items():
        pv = prev_v.get(k)
        out[k] = round(v - pv, 2) if isinstance(v, (int, float)) and \
            isinstance(pv, (int, float)) else None
    return out


# ---------- digest ----------

def fmt(v):
    if v is None:
        return "null"
    if isinstance(v, float):
        return f"{v:,.2f}".rstrip("0").rstrip(".")
    return f"{v:,}"


def print_digest(snap):
    print(f"# growth.py digest — {snap['date']}\n")
    if snap["flags"]:
        print("## FLAGS (repeat these in the report)")
        for f in snap["flags"]:
            print(f"- {f}")
        print()
    print("## Scorecard (delta vs", snap["deltas"].get("vs"), ")")
    d = snap["deltas"]
    for k, v in scorecard_values(snap).items():
        dv = d.get(k)
        arrow = "" if dv in (None, 0) else (f"  ({'+' if dv > 0 else ''}{fmt(dv)})")
        print(f"- {k}: {fmt(v)}{arrow}")
    print("\n## Funnel")
    for s in snap["funnel"]["stages"]:
        conv = f"  → {s['conv_to_next']:.2%}" if s["conv_to_next"] is not None else ""
        print(f"- {s['name']}: {fmt(s['count'])}{conv}")
    print(f"- bottleneck hint: {snap['funnel']['bottleneck_hint']}")
    proj = snap["projections"]
    print("\n## Projections (30/60/90d)")
    if not proj.get("scenarios"):
        print(f"- {proj.get('note')}")
    else:
        for name, sc in proj["scenarios"].items():
            print(f"\n### {name} — {sc['label']} [confidence: {sc['confidence']}]")
            for a in sc["assumptions"]:
                print(f"  * {a}")
            for i, h in enumerate(HORIZONS):
                lo_, pt_, hi_ = sc["mrr_net"][i]
                print(f"  +{h}d: ~{sc['downloads'][i]} downloads, "
                      f"subs {sc['subs'][i][0]}-{sc['subs'][i][2]}, "
                      f"MRR net ${lo_}-${hi_} (mid ${pt_})")
    print("\n(digest only — the skill writes the actual report)")


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--mcp", required=True)
    ap.add_argument("--social")
    ap.add_argument("--date")
    ap.add_argument("--no-write", action="store_true")
    ap.add_argument("--json", action="store_true")
    a = ap.parse_args()

    today = (datetime.strptime(a.date, "%Y-%m-%d").date() if a.date
             else datetime.now(timezone.utc).date())
    date_str = today.isoformat()
    flags = []
    mcp = json.load(open(a.mcp)) if os.path.exists(a.mcp) else None
    if mcp is None:
        flags.append("mcp: input file missing — revenue and product layers null")

    social = social_layer(a.social, flags)
    store = store_layer(today, flags)
    product = product_layer(mcp, flags)
    revenue = revenue_layer(mcp, flags)
    outreach = outreach_layer(flags)
    funnel = build_funnel(social, store, product, revenue)
    projections = project(revenue, store, social, flags)

    snap = {"schema": 1, "date": date_str,
            "generated_at": datetime.now(timezone.utc).isoformat(timespec="seconds"),
            "flags": flags,
            "sources": {"mcp_pulled_at": (mcp or {}).get("pulled_at"),
                        "social_file": bool(a.social),
                        "installs_stale": store.get("stale")},
            "social": social, "store": store, "product": product,
            "revenue": revenue, "outreach": outreach, "funnel": funnel,
            "projections": projections}
    snap["deltas"] = deltas_vs_previous(snap, date_str)

    if not a.no_write:
        os.makedirs(REPORTS, exist_ok=True)
        out = os.path.join(REPORTS, f"{date_str}-snapshot.json")
        if os.path.exists(out):
            sys.exit(f"refusing to overwrite existing snapshot {out}; "
                     "pass --no-write or a different --date")
        with open(out, "w") as f:
            json.dump(snap, f, indent=1)
        print(f"wrote {os.path.relpath(out, ROOT)}\n")

    if a.json:
        print(json.dumps(snap, indent=2))
    else:
        print_digest(snap)


if __name__ == "__main__":
    main()
