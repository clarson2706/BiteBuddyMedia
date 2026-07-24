#!/usr/bin/env python3
"""
Append a batch of per-post performance snapshots to the append-only ledger.

Claude gathers the numbers by calling the Upload-Post analytics tools
(get_analytics / get_post_analytics / get_platform_metrics / get_history) in a
session where the connector is enabled, writes them to a batch JSON file in the
snapshot shape below, and runs this script to fold them into the ledger. The
ledger is append-only (one JSON object per line) so history is never lost —
`analyze.py` always reads the LATEST snapshot per (post_id, platform, profile).

Snapshot shape (one object; a batch file is a JSON array of these):
  {
    "post_id": "2026-07-20-slot1",     # required
    "platform": "tiktok",              # required
    "profile": "Business_Posts",       # optional (which account posted it)
    "week": "2026-W30",                # optional but recommended
    "format": "F1-buddys-list",        # optional; enables format analysis
    "tags": {                          # optional; the richer the better
      "hook_type": "mistake-listicle",
      "topic": "hidden-calories",
      "cover_style": "buddy-shock",
      "hashtags": ["#caloriedeficit", "#bitebuddy"]
    },
    "posted_at": "2026-07-20T08:00:00",
    "metrics": {                       # required; needs at least "views"
      "views": 124000, "likes": 8200, "comments": 410,
      "shares": 900, "saves": 2600,
      "swipe_through_rate": 0.58       # optional if the platform reports it
    }
  }

Usage:
  python record_metrics.py --batch batch.json
  cat batch.json | python record_metrics.py            # or from stdin
  optional: --log Marketing/Analytics/performance-log.jsonl
"""
import argparse, datetime, json, os, sys

DEFAULT_LOG = "Marketing/Analytics/performance-log.jsonl"
REQUIRED = ("post_id", "platform")


def validate(item, i):
    errs = []
    if not isinstance(item, dict):
        return [f"item {i}: not an object"]
    for k in REQUIRED:
        if not item.get(k):
            errs.append(f"item {i}: missing '{k}'")
    m = item.get("metrics")
    if not isinstance(m, dict) or "views" not in m:
        errs.append(f"item {i}: metrics.views required")
    else:
        try:
            float(m["views"])
        except (TypeError, ValueError):
            errs.append(f"item {i}: metrics.views not numeric")
    return errs


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--batch", help="JSON file with an array of snapshots (else stdin)")
    ap.add_argument("--log", default=DEFAULT_LOG)
    args = ap.parse_args()

    raw = open(args.batch).read() if args.batch else sys.stdin.read()
    try:
        data = json.loads(raw)
    except ValueError as e:
        print(f"batch is not valid JSON: {e}", file=sys.stderr)
        return 2
    if isinstance(data, dict):
        data = [data]
    if not isinstance(data, list) or not data:
        print("batch must be a non-empty JSON array of snapshots", file=sys.stderr)
        return 2

    errs = []
    for i, item in enumerate(data):
        errs += validate(item, i)
    if errs:
        print("VALIDATION FAILED:", file=sys.stderr)
        print("\n".join(f"  - {e}" for e in errs), file=sys.stderr)
        return 1

    now = datetime.datetime.now().isoformat(timespec="seconds")
    os.makedirs(os.path.dirname(args.log) or ".", exist_ok=True)
    n = 0
    with open(args.log, "a") as f:
        for item in data:
            item.setdefault("pulled_at", now)
            f.write(json.dumps(item, separators=(",", ":")) + "\n")
            n += 1
    total = sum(1 for _ in open(args.log))
    print(f"Recorded {n} snapshot(s) → {args.log} ({total} total in ledger)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
