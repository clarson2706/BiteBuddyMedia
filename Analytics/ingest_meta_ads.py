#!/usr/bin/env python3
"""Ingest a Meta Ads Manager hourly export into the permanent record.

Same contract as ingest_export.py: the platform's own export is ground truth, the
raw file is committed verbatim under Analytics/platform-exports/ for provenance,
and the rows are normalised into an append-only log.

Paid ads get their own log rather than performance-log.jsonl. That log's rows are
organic per-post snapshots keyed on Upload-Post's request_id, and paid rows share
almost none of those fields. Mixing them would make every cut in report.py wrong.

Null discipline, inherited from ingest_export.py and load-bearing here:

  - CPC when there were no clicks is **null**, not 0.00. Meta writes 0.00, which
    reads as "clicks are free" in any average. Same for cost-per-conversion with
    no conversions.
  - Conversions and SKAN conversions are **0** and stay 0 — Meta reported them as
    none, which is different from not reporting them. Note that SKAdNetwork
    postbacks lag 24-72h, so a fresh day's 0 is provisional. Re-ingesting the
    same date later with --force picks up backfilled postbacks.

Usage:
    python3 Analytics/ingest_meta_ads.py --xlsx path/to/View_Report.xlsx
    python3 Analytics/ingest_meta_ads.py --xlsx path/to/report.xlsx --dry-run
    python3 Analytics/ingest_meta_ads.py --xlsx path/to/report.xlsx --force
"""
import argparse, json, os, shutil, sys
from datetime import datetime, timezone

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
LOG = os.path.join(ROOT, "Analytics", "paid-ads.jsonl")
RAW_DIR = os.path.join(ROOT, "Analytics", "platform-exports")

# Meta's hourly export header, as of the 2026-08-04 pull. If a future export
# renames a column this raises rather than silently logging zeros.
REQUIRED = [
    "Ad ID", "Time", "Spend", "Impressions", "CPM",
    "Clicks (destination)", "CPC (destination)", "Clicks (all)",
    "Video views", "Conversions", "Cost per conversion",
    "Conversions (SKAN)", "Cost per conversion (SKAN)",
]


def num(v):
    if v is None:
        return 0.0
    s = str(v).strip()
    if s in ("", "-", "—"):
        return 0.0
    return float(s.replace(",", "").replace("$", ""))


def parse(path):
    try:
        import openpyxl
    except ImportError:
        sys.exit("needs openpyxl:  pip install openpyxl")

    ws = openpyxl.load_workbook(path, data_only=True).worksheets[0]
    rows = list(ws.iter_rows(values_only=True))
    header = [str(c).strip() if c is not None else "" for c in rows[0]]
    missing = [c for c in REQUIRED if c not in header]
    if missing:
        sys.exit(f"export is missing expected columns: {missing}\ngot: {header}")
    idx = {c: header.index(c) for c in REQUIRED}

    days = {}
    for r in rows[1:]:
        ad_id = str(r[idx["Ad ID"]] or "").strip()
        when = str(r[idx["Time"]] or "").strip()
        # Meta appends a totals row with "-" in the identifier columns. Skip it;
        # we re-derive totals from the hourly rows so the two cannot drift.
        if not ad_id or ad_id == "-" or not when or when == "-":
            continue
        date, _, clock = when.partition(" ")
        hour = int(clock.split(":")[0]) if clock else 0
        d = days.setdefault((date, ad_id), {
            "spend": 0.0, "impressions": 0, "clicks_destination": 0,
            "clicks_all": 0, "video_views": 0, "conversions": 0,
            "conversions_skan": 0, "hourly_impressions": [0] * 24,
            "hourly_spend": [0.0] * 24,
        })
        imp = int(num(r[idx["Impressions"]]))
        spend = num(r[idx["Spend"]])
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
        clicks_d, clicks_a = d["clicks_destination"], d["clicks_all"]
        conv = d["conversions"]
        delivering = [h for h, v in enumerate(d["hourly_impressions"]) if v > 0]
        out.append({
            "date": date,
            "ad_id": ad_id,
            "platform": "meta",
            "source": "meta-ads-export",
            "currency": "USD",
            "captured_at": datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"),
            "spend": spend,
            "impressions": imp,
            "cpm": round(spend / imp * 1000, 2) if imp else None,
            "clicks_destination": clicks_d,
            "clicks_all": clicks_a,
            "ctr_destination": round(clicks_d / imp * 100, 3) if imp else None,
            "ctr_all": round(clicks_a / imp * 100, 3) if imp else None,
            # 0.00 from Meta means "no clicks", not "free clicks". Keep it null.
            "cpc_destination": round(spend / clicks_d, 2) if clicks_d else None,
            "video_views": d["video_views"],
            "video_view_rate": round(d["video_views"] / imp * 100, 1) if imp else None,
            "conversions": conv,
            "conversions_skan": d["conversions_skan"],
            "cost_per_conversion": round(spend / conv, 2) if conv else None,
            # SKAN postbacks lag 24-72h; a same-day 0 is provisional, not final.
            "skan_provisional": True,
            "first_delivery_hour": delivering[0] if delivering else None,
            "last_delivery_hour": delivering[-1] if delivering else None,
            "hours_delivering": len(delivering),
            "hourly_impressions": d["hourly_impressions"],
            "hourly_spend": d["hourly_spend"],
        })
    return out


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--xlsx", required=True)
    ap.add_argument("--dry-run", action="store_true")
    ap.add_argument("--force", action="store_true",
                    help="re-log a date already present (picks up late SKAN postbacks)")
    a = ap.parse_args()

    rows = parse(a.xlsx)
    if not rows:
        sys.exit("no data rows found in export")

    seen = set()
    if os.path.exists(LOG):
        with open(LOG) as fh:
            for line in fh:
                if line.strip():
                    r = json.loads(line)
                    seen.add((r.get("date"), r.get("ad_id")))

    fresh = [r for r in rows if a.force or (r["date"], r["ad_id"]) not in seen]
    skipped = len(rows) - len(fresh)

    for r in fresh:
        print(f"  {r['date']}  ad {r['ad_id']}  ${r['spend']}  "
              f"{r['impressions']} imp  CPM ${r['cpm']}  "
              f"{r['clicks_destination']} dest-clicks  {r['conversions']} conv")
    if skipped:
        print(f"  ({skipped} already logged, skipped; use --force to re-log)")

    if a.dry_run:
        print("dry run, nothing written")
        return

    if fresh:
        os.makedirs(os.path.dirname(LOG), exist_ok=True)
        with open(LOG, "a") as fh:
            for r in fresh:
                fh.write(json.dumps(r) + "\n")
        print(f"appended {len(fresh)} row(s) to {os.path.relpath(LOG, ROOT)}")

    os.makedirs(RAW_DIR, exist_ok=True)
    stamp = rows[0]["date"]
    dest = os.path.join(RAW_DIR, f"meta-ads-hourly-{stamp}.xlsx")
    if os.path.abspath(a.xlsx) != os.path.abspath(dest):
        shutil.copy2(a.xlsx, dest)
        print(f"raw export committed to {os.path.relpath(dest, ROOT)}")


if __name__ == "__main__":
    main()
