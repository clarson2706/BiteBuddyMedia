#!/usr/bin/env python3
"""Ingest a native platform analytics export into the permanent record.

Upload-Post is a convenience layer. The platforms' own exports are ground truth,
and where they disagree the export wins. That is not theoretical: the first
TikTok export we ingested put the daily view series one day earlier than
Upload-Post reported it, and counted 9 likes in a window where Upload-Post's
lifetime total said 3.

So: whenever Connor drops an export, the raw file is committed verbatim under
Analytics/platform-exports/ for provenance, and the rows are normalised into
performance-log.jsonl as ACCOUNT-DAILY snapshots that report.py can read
alongside everything else.

Currently understands TikTok Studio's Overview.csv (Date, Video Views, Profile
Views, Likes, Comments, Shares), where Date is a bare "July 21" with no year.

Usage:
    python3 Analytics/ingest_export.py --tiktok path/to/Overview.csv --year 2026
    python3 Analytics/ingest_export.py --tiktok path/to/Overview.csv --dry-run
"""
import argparse, csv, json, os, shutil, sys
from datetime import datetime

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
LOG = os.path.join(ROOT, "Analytics", "performance-log.jsonl")
RAW_DIR = os.path.join(ROOT, "Analytics", "platform-exports")

# TikTok's Overview export omits saves and any per-post breakdown, so those stay
# null rather than zero. Null means "not reported", zero means "reported as none",
# and collapsing the two is how a pipeline starts lying to itself.
TIKTOK_COLS = {
    "Video Views": "views",
    "Profile Views": "profileViews",
    "Likes": "likes",
    "Comments": "comments",
    "Shares": "shares",
}


def parse_tiktok(path, year):
    rows = []
    # TikTok writes a UTF-8 BOM; without utf-8-sig the first header becomes
    # "﻿Date" and every row silently parses as empty.
    with open(path, newline="", encoding="utf-8-sig") as fh:
        for r in csv.DictReader(fh):
            raw = (r.get("Date") or "").strip()
            if not raw:
                continue
            try:
                d = datetime.strptime(f"{raw} {year}", "%B %d %Y").date()
            except ValueError:
                sys.exit(f"unparseable date {raw!r} — pass the right --year, "
                         "or teach this script the format")
            row = {
                "post_id": "ACCOUNT-DAILY",
                "platform": "tiktok",
                "date": d.isoformat(),
                "source": "tiktok-export",
                "saves": None,
            }
            for col, key in TIKTOK_COLS.items():
                v = (r.get(col) or "").strip().replace(",", "")
                row[key] = int(v) if v.isdigit() else None
            rows.append(row)
    return rows


def existing_keys():
    """(platform, date) already logged from an export, so re-ingesting is safe."""
    seen = set()
    if not os.path.exists(LOG):
        return seen
    for line in open(LOG):
        line = line.strip()
        if not line:
            continue
        try:
            e = json.loads(line)
        except json.JSONDecodeError:
            continue
        if e.get("post_id") == "ACCOUNT-DAILY" and e.get("source", "").endswith("-export"):
            seen.add((e.get("platform"), e.get("date")))
    return seen


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--tiktok", required=True, help="path to TikTok Studio Overview.csv")
    ap.add_argument("--year", type=int, default=datetime.now().year)
    ap.add_argument("--dry-run", action="store_true")
    a = ap.parse_args()

    rows = parse_tiktok(a.tiktok, a.year)
    if not rows:
        sys.exit("no rows parsed")
    seen = existing_keys()
    new = [r for r in rows if (r["platform"], r["date"]) not in seen]
    captured = datetime.now().astimezone().isoformat(timespec="seconds")

    span = f"{rows[0]['date']} to {rows[-1]['date']}"
    print(f"parsed {len(rows)} rows ({span}); {len(new)} new, {len(rows) - len(new)} already logged")
    for r in rows:
        mark = " " if (r["platform"], r["date"]) in seen else "+"
        print(f" {mark} {r['date']}  views={r['views']:<6} likes={r['likes']:<4} "
              f"comments={r['comments']:<4} shares={r['shares']:<4} profile={r['profileViews']}")

    if a.dry_run:
        return
    if new:
        with open(LOG, "a") as fh:
            for r in new:
                fh.write(json.dumps({**r, "captured_at": captured}) + "\n")

    os.makedirs(RAW_DIR, exist_ok=True)
    dest = os.path.join(RAW_DIR, f"tiktok-overview-{rows[0]['date']}_{rows[-1]['date']}.csv")
    shutil.copy(a.tiktok, dest)
    print(f"\nraw export -> {os.path.relpath(dest, ROOT)}")
    print(f"appended {len(new)} rows -> {os.path.relpath(LOG, ROOT)}")


if __name__ == "__main__":
    main()
