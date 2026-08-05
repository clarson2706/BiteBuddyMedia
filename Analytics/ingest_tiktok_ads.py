#!/usr/bin/env python3
"""Ingest TikTok Ads Manager exports into the permanent record.

Same contract as ingest_export.py: the platform's own export is ground truth, the
raw file is committed verbatim under Analytics/platform-exports/ for provenance,
and the rows are normalised into an append-only log.

Two exports, two logs:

  --hourly     View_Report<range>.xlsx            -> paid-ads.jsonl
  --creatives  ...InsightsCreativesTable<range>   -> paid-ads-creatives.jsonl

Paid rows live apart from performance-log.jsonl, whose rows are organic per-post
snapshots keyed on Upload-Post's request_id. Paid rows share almost none of those
fields and mixing them would silently corrupt every cut in report.py.

Note the overlap that makes this repo's paid and organic tracks the same account:
Spark Ads carry the **organic post_id** of the post being promoted, so a creative
row joins straight back to its performance-log.jsonl row. That join is the only
way to see a post's paid and organic reach side by side.

Null discipline, inherited from ingest_export.py and load-bearing here:

  - CPC and cost-per-conversion are **null** when there were no clicks or
    conversions. TikTok writes 0.00, which reads as "clicks are free" in any
    average.
  - Conversions and SKAN conversions are **0** and stay 0 — TikTok reported them
    as none, which is different from not reporting them. SKAdNetwork postbacks
    lag 24-72h, so a fresh day's 0 is provisional; re-ingest with --force later
    to pick up backfilled postbacks.
  - Rate columns in the export are **fractions** (0.0033 = 0.33%). Every rate
    here is recomputed from raw counts and stored as a percent, so nothing
    depends on which convention a future export uses.
  - Completion and quartile rates are per *video view*, and null for carousels,
    which have no video to retain anyone. Zero would read as "nobody finished it".

Usage:
    python3 Analytics/ingest_tiktok_ads.py --hourly <View_Report.xlsx>
    python3 Analytics/ingest_tiktok_ads.py --creatives <CreativesTable.xlsx>
    python3 Analytics/ingest_tiktok_ads.py --hourly A.xlsx --creatives B.xlsx
    python3 Analytics/ingest_tiktok_ads.py --creatives B.xlsx --date 2026-08-04
    ... --dry-run | --force
"""
import argparse, json, os, re, shutil, sys
from datetime import datetime, timezone

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
LOG_HOURLY = os.path.join(ROOT, "Analytics", "paid-ads.jsonl")
LOG_CREATIVE = os.path.join(ROOT, "Analytics", "paid-ads-creatives.jsonl")
RAW_DIR = os.path.join(ROOT, "Analytics", "platform-exports")

HOURLY_REQUIRED = [
    "Ad ID", "Time", "Spend", "Impressions", "CPM",
    "Clicks (destination)", "CPC (destination)", "Clicks (all)",
    "Video views", "Conversions", "Cost per conversion",
    "Conversions (SKAN)", "Cost per conversion (SKAN)",
]

# Creative export -> log field. Anything not listed is dropped deliberately;
# add it here rather than reaching into the raw row downstream.
CREATIVE_COLS = {
    "Creative asset": "creative_asset",
    "Creative type": "creative_type",
    "Spend": "spend",
    "Impressions": "impressions",
    "Clicks (destination)": "clicks_destination",
    "Clicks (all)": "clicks_all",
    "Paid follows": "paid_follows",
    "Paid likes": "paid_likes",
    "Paid comments": "paid_comments",
    "Paid shares": "paid_shares",
    "Paid profile visits": "paid_profile_visits",
    "Sound clicks": "sound_clicks",
    "Video views": "video_views",
    "2-second video views": "video_views_2s",
    "6-second video views": "video_views_6s",
    "Video views at 25%": "video_views_25pct",
    "Video views at 50%": "video_views_50pct",
    "Video views at 75%": "video_views_75pct",
    "Video views at 100%": "video_views_100pct",
    "Average play time per video view": "avg_play_time_s",
    "6-second focused views": "focused_views_6s",
    "15-second focused views": "focused_views_15s",
    "Conversions": "conversions",
    "Conversions (SKAN)": "conversions_skan",
    "Related campaigns": "campaign_id",
    "Related ad groups": "adgroup_id",
    "Related ads": "ad_id",
    "Identity": "identity",
    "Post ID": "post_id",
    "Primary source": "primary_source",
    "Secondary source": "secondary_source",
    "Created on": "created_on",
    "Currency": "currency",
}
COUNT_FIELDS = {
    "impressions", "clicks_destination", "clicks_all", "paid_follows",
    "paid_likes", "paid_comments", "paid_shares", "paid_profile_visits",
    "sound_clicks", "video_views", "video_views_2s", "video_views_6s",
    "video_views_25pct", "video_views_50pct", "video_views_75pct",
    "video_views_100pct", "focused_views_6s", "focused_views_15s",
    "conversions", "conversions_skan",
}


def num(v):
    if v is None:
        return 0.0
    s = str(v).strip()
    if s in ("", "-", "—"):
        return 0.0
    return float(s.replace(",", "").replace("$", "").replace("%", ""))


def now():
    return datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")


def sheet(path):
    try:
        import openpyxl
    except ImportError:
        sys.exit("needs openpyxl:  pip install openpyxl")
    ws = openpyxl.load_workbook(path, data_only=True).worksheets[0]
    rows = list(ws.iter_rows(values_only=True))
    header = [str(c).strip() if c is not None else "" for c in rows[0]]
    return header, rows[1:]


def date_from_name(path, override):
    """TikTok names exports ...<YYYYMMDD><YYYYMMDD>.xlsx (range start, end)."""
    if override:
        return override
    m = re.search(r"(\d{8})(\d{8})", os.path.basename(path))
    if not m:
        sys.exit("cannot infer the report date from the filename; pass --date YYYY-MM-DD")
    d = m.group(1)
    return f"{d[:4]}-{d[4:6]}-{d[6:]}"


def parse_hourly(path):
    header, rows = sheet(path)
    missing = [c for c in HOURLY_REQUIRED if c not in header]
    if missing:
        sys.exit(f"hourly export missing expected columns: {missing}\ngot: {header}")
    idx = {c: header.index(c) for c in HOURLY_REQUIRED}

    days = {}
    for r in rows:
        ad_id = str(r[idx["Ad ID"]] or "").strip()
        when = str(r[idx["Time"]] or "").strip()
        # TikTok appends a totals row with "-" in the identifier columns. Skip it;
        # totals are re-derived from the hourly rows so the two cannot drift.
        if not ad_id or ad_id == "-" or not when or when == "-":
            continue
        date, _, clock = when.partition(" ")
        hour = int(clock.split(":")[0]) if clock else 0
        d = days.setdefault((date, ad_id), {
            "spend": 0.0, "impressions": 0, "clicks_destination": 0,
            "clicks_all": 0, "video_views": 0, "conversions": 0,
            "conversions_skan": 0,
            "hourly_impressions": [0] * 24, "hourly_spend": [0.0] * 24,
        })
        imp, spend = int(num(r[idx["Impressions"]])), num(r[idx["Spend"]])
        d["spend"] += spend
        d["impressions"] += imp
        d["clicks_destination"] += int(num(r[idx["Clicks (destination)"]]))
        d["clicks_all"] += int(num(r[idx["Clicks (all)"]]))
        d["video_views"] += int(num(r[idx["Video views"]]))
        d["conversions"] += int(num(r[idx["Conversions"]]))
        d["conversions_skan"] += int(num(r[idx["Conversions (SKAN)"]]))
        d["hourly_impressions"][hour] = imp
        d["hourly_spend"][hour] = round(spend, 2)

    out = []
    for (date, ad_id), d in sorted(days.items()):
        imp, spend = d["impressions"], round(d["spend"], 2)
        cd, ca, conv = d["clicks_destination"], d["clicks_all"], d["conversions"]
        live = [h for h, v in enumerate(d["hourly_impressions"]) if v > 0]
        out.append({
            "date": date, "ad_id": ad_id, "platform": "tiktok",
            "source": "tiktok-ads-export", "currency": "USD",
            "captured_at": now(),
            "spend": spend, "impressions": imp,
            "cpm": round(spend / imp * 1000, 2) if imp else None,
            "clicks_destination": cd, "clicks_all": ca,
            "ctr_destination": round(cd / imp * 100, 3) if imp else None,
            "ctr_all": round(ca / imp * 100, 3) if imp else None,
            "cpc_destination": round(spend / cd, 2) if cd else None,
            "video_views": d["video_views"],
            "video_view_rate": round(d["video_views"] / imp * 100, 1) if imp else None,
            "conversions": conv, "conversions_skan": d["conversions_skan"],
            "cost_per_conversion": round(spend / conv, 2) if conv else None,
            "skan_provisional": True,
            "first_delivery_hour": live[0] if live else None,
            "last_delivery_hour": live[-1] if live else None,
            "hours_delivering": len(live),
            "hourly_impressions": d["hourly_impressions"],
            "hourly_spend": d["hourly_spend"],
        })
    return out, ("date", "ad_id")


def parse_creatives(path, date):
    header, rows = sheet(path)
    missing = [c for c in CREATIVE_COLS if c not in header]
    if missing:
        sys.exit(f"creatives export missing expected columns: {missing}\ngot: {header}")
    idx = {c: header.index(c) for c in CREATIVE_COLS}

    out = []
    for r in rows:
        asset = str(r[idx["Creative asset"]] or "").strip()
        if not asset or asset == "-":
            continue
        rec = {"date": date, "platform": "tiktok",
               "source": "tiktok-ads-creatives-export", "captured_at": now()}
        for col, field in CREATIVE_COLS.items():
            v = r[idx[col]]
            if field in COUNT_FIELDS:
                rec[field] = int(num(v))
            elif field in ("spend", "avg_play_time_s"):
                rec[field] = round(num(v), 2)
            else:
                rec[field] = str(v).strip() if v is not None else None

        imp, spend = rec["impressions"], rec["spend"]
        cd, vv, conv = rec["clicks_destination"], rec["video_views"], rec["conversions"]
        # Every rate recomputed from counts: the export stores rates as fractions
        # (0.0033 = 0.33%) and that convention is not worth depending on.
        rec["cpm"] = round(spend / imp * 1000, 2) if imp else None
        rec["ctr_destination"] = round(cd / imp * 100, 3) if imp else None
        rec["ctr_all"] = round(rec["clicks_all"] / imp * 100, 3) if imp else None
        rec["cpc_destination"] = round(spend / cd, 2) if cd else None
        rec["cost_per_conversion"] = round(spend / conv, 2) if conv else None
        rec["video_view_rate"] = round(vv / imp * 100, 1) if imp else None
        # Retention is per video view, and null for carousels: there is no video
        # to retain anyone, and 0 would read as "nobody finished it".
        rec["completion_rate"] = round(rec["video_views_100pct"] / vv * 100, 2) if vv else None
        rec["reached_25pct_rate"] = round(rec["video_views_25pct"] / vv * 100, 2) if vv else None
        rec["reached_50pct_rate"] = round(rec["video_views_50pct"] / vv * 100, 2) if vv else None
        rec["skan_provisional"] = True
        # Spark Ads carry the organic post_id, so this row joins back to
        # performance-log.jsonl.
        rec["is_spark_ad"] = rec.get("secondary_source") == "TikTok account"
        out.append(rec)
    return out, ("date", "creative_asset")


def append(log, rows, key_fields, force, dry):
    seen = set()
    if os.path.exists(log):
        with open(log) as fh:
            for line in fh:
                if line.strip():
                    r = json.loads(line)
                    seen.add(tuple(r.get(k) for k in key_fields))
    fresh = [r for r in rows if force or tuple(r[k] for k in key_fields) not in seen]
    skipped = len(rows) - len(fresh)
    if skipped:
        print(f"  ({skipped} already logged, skipped; --force to re-log)")
    if dry:
        print(f"  dry run: would append {len(fresh)} row(s) to {os.path.relpath(log, ROOT)}")
        return
    if fresh:
        with open(log, "a") as fh:
            for r in fresh:
                fh.write(json.dumps(r) + "\n")
        print(f"  appended {len(fresh)} row(s) to {os.path.relpath(log, ROOT)}")


def keep_raw(path, name, dry):
    if dry:
        return
    os.makedirs(RAW_DIR, exist_ok=True)
    dest = os.path.join(RAW_DIR, name)
    if os.path.abspath(path) != os.path.abspath(dest):
        shutil.copy2(path, dest)
        print(f"  raw export committed to {os.path.relpath(dest, ROOT)}")


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--hourly")
    ap.add_argument("--creatives")
    ap.add_argument("--date", help="YYYY-MM-DD; inferred from the filename if omitted")
    ap.add_argument("--dry-run", action="store_true")
    ap.add_argument("--force", action="store_true")
    a = ap.parse_args()
    if not a.hourly and not a.creatives:
        sys.exit("pass --hourly and/or --creatives")

    if a.hourly:
        rows, key = parse_hourly(a.hourly)
        if not rows:
            sys.exit("no data rows in the hourly export")
        for r in rows:
            print(f"  {r['date']}  ad {r['ad_id']}  ${r['spend']}  {r['impressions']} imp  "
                  f"CPM ${r['cpm']}  {r['clicks_destination']} dest-clicks  {r['conversions']} conv")
        append(LOG_HOURLY, rows, key, a.force, a.dry_run)
        keep_raw(a.hourly, f"tiktok-ads-hourly-{rows[0]['date']}.xlsx", a.dry_run)

    if a.creatives:
        date = date_from_name(a.creatives, a.date)
        rows, key = parse_creatives(a.creatives, date)
        if not rows:
            sys.exit("no data rows in the creatives export")
        for r in rows:
            label = r["creative_asset"]
            label = label if len(label) <= 46 else label[:43] + "..."
            print(f"  {r['date']}  {label:49s} ${r['spend']:>5}  {r['impressions']:>5} imp  "
                  f"{r['clicks_destination']} dest  play {r['avg_play_time_s']}s")
        append(LOG_CREATIVE, rows, key, a.force, a.dry_run)
        keep_raw(a.creatives, f"tiktok-ads-creatives-{date}.xlsx", a.dry_run)


if __name__ == "__main__":
    main()
