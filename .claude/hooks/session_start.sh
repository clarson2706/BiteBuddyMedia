#!/usr/bin/env bash
# SessionStart hook: put START-HERE.md in front of every session that opens this repo,
# followed by a fast offline health line so a session cannot start out of date.
#
# This hook must NEVER fail a session. Every command is guarded; the script always
# exits 0. If something here starts erroring, the worst case is a session that reads
# START-HERE.md without the health line, which is still the point.
set -uo pipefail

REPO="$(cd "$(dirname "${BASH_SOURCE[0]}")/../.." && pwd)"
cd "$REPO" 2>/dev/null || exit 0

echo "===== BiteBuddyMedia: START-HERE.md (auto-loaded at session start) ====="
echo
cat START-HERE.md 2>/dev/null || echo "(START-HERE.md missing — that is itself a problem, recreate it)"
echo
echo "===== Live repo health (offline checks only, $(date -u +%Y-%m-%dT%H:%MZ)) ====="

# Stranded loop work: any remote claude/* branch whose commits are not on main.
if git rev-parse --git-dir >/dev/null 2>&1; then
  git fetch -q origin 2>/dev/null || true
  stranded=""
  for b in $(git for-each-ref --format='%(refname:short)' refs/remotes/origin/claude 2>/dev/null); do
    if ! git merge-base --is-ancestor "$b" origin/main 2>/dev/null; then
      touched=$(git diff --name-only origin/main..."$b" 2>/dev/null \
        | grep -E 'registry\.jsonl|performance-log\.jsonl|Posts/|Analytics/' | head -1)
      [ -n "$touched" ] && stranded="$stranded  - ${b#origin/}\n"
    fi
  done
  if [ -n "$stranded" ]; then
    echo "WARNING: unmerged branches carry content memory that main does not have:"
    printf "%b" "$stranded"
    echo "  Generation must not run until these are merged or explicitly abandoned."
    echo "  See rule 1 in START-HERE.md and run: python3 Content-Engine/preflight.py"
  else
    echo "OK: no stranded loop branches."
  fi
fi

# The registry is the dedupe memory. An empty or tiny one after weeks of posting is a bug.
if [ -f Content-Engine/registry.jsonl ]; then
  echo "Registry: $(wc -l < Content-Engine/registry.jsonl | tr -d ' ') posts recorded."
fi
if [ -f Analytics/performance-log.jsonl ]; then
  echo "Performance log: $(wc -l < Analytics/performance-log.jsonl | tr -d ' ') snapshots recorded."
fi

echo
echo "Before generating, rendering, scheduling or publishing: python3 Content-Engine/preflight.py"
exit 0
