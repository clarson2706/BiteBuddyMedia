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
    """Rows in file order, with years assigned by walking backwards from the end.

    TikTok's Date column is a bare "July 21" with no year, and a full-range export
    spans twelve months, so it wraps: it can open on "August 2" of one year and close
    on "August 1" of the next. Stamping every row with a single year puts 150-odd
    future-dated rows into an append-only log, which is a lie the log can never shed.
    So `year` means **the year of the last row**, and the year decrements each time the
    month jumps up as we walk backwards past a December-to-January boundary.
    """
    raw_rows = []
    # TikTok writes a UTF-8 BOM; without utf-8-sig the first header becomes
    # "﻿Date" and every row silently parses as empty.
    with open(path, newline="", encoding="utf-8-sig") as fh:
        for r in csv.DictReader(fh):
            raw = (r.get("Date") or "").strip()
            if not raw:
                continue
            try:
                md = datetime.strptime(raw, "%B %d")
            except ValueError:
                sys.exit(f"unparseable date {raw!r} — teach this script the format")
            raw_rows.append((md.month, md.day, r))

    years, y, prev_month = [], year, None
    for month, _, _ in reversed(raw_rows):
        if prev_month is not None and month > prev_month:
            y -= 1
        years.append(y)
        prev_month = month
    years.reverse()

    rows = []
    today = datetime.now().date()
    for (month, day, r), yr in zip(raw_rows, years):
        try:
            d = datetime(yr, month, day).date()
        except ValueError:      # Feb 29 landing on the wrong year
            sys.exit(f"{month}/{day} is not a date in {yr} — check --year")
        if d > today:
            sys.exit(f"refusing to log {d.isoformat()}, which is in the future. "
                     f"--year should be the year of the export's LAST row, got {year}")
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


def trim_leading_zeros(rows):
    """Drop the dead run before the account's first recorded activity.

    A year-long export is mostly days that predate the account having any content.
    Those are real reported zeros, but logging 350 of them buries the days that carry
    signal. Zeros *after* first activity are kept: a day that genuinely went to zero is
    exactly the kind of thing worth seeing.
    """
    metrics = ("views", "likes", "comments", "shares", "profileViews")
    for i, r in enumerate(rows):
        if any(r.get(m) for m in metrics):
            return rows[i:], i
    return rows, 0


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
    ap.add_argument("--year", type=int, default=datetime.now().year,
                    help="year of the export's LAST row; earlier rows roll back "
                         "automatically when the range wraps a new year")
    ap.add_argument("--all-rows", action="store_true",
                    help="keep the all-zero run before the account's first activity")
    ap.add_argument("--dry-run", action="store_true")
    a = ap.parse_args()

    rows = parse_tiktok(a.tiktok, a.year)
    if not rows:
        sys.exit("no rows parsed")
    if not a.all_rows:
        rows, dropped = trim_leading_zeros(rows)
        if dropped:
            print(f"skipped {dropped} all-zero rows before first activity "
                  f"(--all-rows keeps them)")
    if not rows:
        sys.exit("every row is zero; nothing to log")
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
