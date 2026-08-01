# START HERE

**Read this file at the top of every session that touches this repo. It is loaded
automatically by the SessionStart hook in `.claude/settings.json`; if you are reading the
repo some other way, read it anyway before you write anything.**

*Last verified: 2026-07-31. Whoever changes the system updates this file in the same
commit. A stale START-HERE is worse than none.*

---

## 1. What this repo is for

One job: **get people to install BiteBuddy from the App Store.**
`https://apps.apple.com/us/app/bitebuddy-ai-calorie-scanner/id6787834752`

The app is live and has effectively zero users. Distribution is the whole problem.
Content that cannot plausibly end in an install is not worth producing.

**The primary channel is TikTok carousels (Photo Mode).** Everything else is secondary.
When a decision trades TikTok carousel performance for anything else, TikTok wins.

## 2. The one number that matters right now

As of 2026-07-31, pulled live from Upload-Post:

| | TikTok | YouTube |
|---|---|---|
| Lifetime views | **4,408** | 661 |
| Likes | 59 | 5 |
| **Comments** | **0** | **0** |
| **Shares** | **0** | 0 |
| **Followers** | **1** | 5 |
| **Profile views** | **0** | 0 |

Daily TikTok views are climbing hard (1,700 on the most recent full day, from zero two
weeks ago). **Reach is no longer the problem. Conversion off the post is.**

> 4,408 people saw this content. One of them followed. Zero tapped through to the
> profile. Zero commented. Zero shared. At that conversion rate no amount of extra reach
> produces an install.

**So the standing priority is not "more views." It is: give the viewer a reason to tap
the profile, and give the profile a reason to end in an install.** Every change proposed
in this repo should be answerable to that sentence. See `Analytics/CONVERSION.md`.

## 3. Before you generate, render, schedule or publish anything

```bash
python3 Content-Engine/preflight.py            # gate: run it, obey it
```

It exits non-zero when the system is in a state where a run would do damage (stranded
branches, registry drift against the live schedule, missing deps, unlinked platforms,
rate-limit violations). **A non-zero preflight stops the run.** Do not work around it,
fix what it names. `--json` for machine output, `--skip-network` when offline.

## 4. Hard rules that survive every rewrite

These are not style preferences. Each one exists because it was violated once.

1. **Never commit to `main` directly, and never leave a loop run stranded on a branch.**
   Every run ends with a pushed branch **and an open PR**, and the next run's preflight
   refuses to generate while an unmerged loop branch exists. Content memory that is not
   on `main` does not exist. This has already broken once: three separate branches
   (`tender-bardeen`, `jolly-bardeen`, `marketing-report-brainstorm`) carry a whole week
   of posts, a Wednesday mini-run, a `Reports/` tree, a new skill and a `report.py` bug
   fix that `main` has never seen.
2. **Measurement is not a later phase.** If a number is not a line in
   `Analytics/performance-log.jsonl`, it does not exist and may not be cited.
3. **Guardrails outrank every directive, trend and growth tactic.** No medical or
   outcome claims; never feature the Meal Advisor; real screenshots only; app numbers
   are AI estimates the user reviews (claim consistency, never precision); no em dashes
   in outbound copy. Enforced in code by `Content-Engine/copy_lint.py`.
4. **Platform-native exports outrank Upload-Post** wherever they overlap. Upload-Post's
   account aggregates are date-shifted by a day and under-count likes.
5. **Cadence:** TikTok 3/day at 08:00 / 13:00 / 19:00, which is the ceiling not a target.
   Instagram ≤2/day. Never two platforms in the same minute. Five simultaneous posts on
   2026-07-22 is the suspected cause of a throttle.

## 5. What is actually connected (verified 2026-07-31, not assumed)

| Thing | State |
|---|---|
| TikTok | **Linked and healthy.** `@bitebuddyapp`. The channel that matters. |
| YouTube | **Linked.** `@bitebuddy_app`. Reach is real but small and erratic. |
| Instagram | **DISCONNECTED.** `list_users` returns `instagram: ""` — an empty string, not a restriction. This is a token drop, and a reconnect in the Upload-Post dashboard fixes it. It is *not* the spam ban older notes claim. |
| Facebook | Never linked. |
| Upload-Post | **Available two ways:** an MCP tool set in-session (`mcp__Upload-Post__*`) *and* the REST API via `UPLOAD_POST_API_KEY`. Older docs say the MCP server does not exist; that is out of date. Plan: **Basic (paid)**. |
| Canva | Connector attached. Not the batch render path (one page per call, exports undownloadable here). |
| Chain nutrition sources | **Unblocked.** chick-fil-a.com, chipotle.com, starbucks.com, wendys.com, fdc.nal.usda.gov all return 200. Older notes saying these are 403 are stale. |

## 6. Three constraints of the publishing transport you must design around

Discovered the hard way; all three apply to **TikTok**, the primary channel:

1. **`upload_photos` takes `description`, not `caption`.** `caption` is silently
   dropped and the post publishes with only its title. Always verify `post_caption`
   afterwards.
2. **TikTok photo posts cannot carry a sound through the API.** Music is a
   video-only field. Every carousel this system publishes goes out silent, while
   sound is a real distribution lever on Photo Mode. Consequence: slide 1 has to do
   the whole job, and the highest-value post of the week is worth posting by hand.
3. **TikTok pinned comments cannot be posted through the API** (`first_comment` is a
   no-op) and **TikTok posts cannot be deleted** through it either. Pinned comments
   are a manual Connor task; getting a TikTok post right the first time is the only
   option.

## 7. Where everything lives

| Need | File |
|---|---|
| The autonomous system's contract | `WEEKLY-LOOP.md` |
| The procedure that executes it | `.claude/skills/weekly-loop/SKILL.md` |
| **Why views are not becoming installs, and the fix** | `Analytics/CONVERSION.md` |
| The recurring shows and how they are tested | `Content-Engine/SERIES.md` |
| Slide layouts, brand tokens, render routes | `Content-Engine/DESIGN-SYSTEM.md` |
| Who each post is for | `Research/TARGET-USER-PROFILES.md` |
| Hook formulas and 2026 anti-patterns | `Research/HOOK-INTELLIGENCE-2026.md` |
| What was posted, ever (dedupe memory) | `Content-Engine/registry.jsonl` |
| Every number ever recorded | `Analytics/performance-log.jsonl` |
| Publishing transport and its traps | `Content-Engine/UPLOAD-POST.md` |
| The 31-day sprint | `SPRINT-AUG25.md` |
| A standing audit of what is broken | `SYSTEM-AUDIT.md` |

## 8. Approval gates

The weekly loop may **schedule and publish its own carousels** on the linked accounts
without per-post approval (authorized by Connor 2026-07-25). The Sunday report is a
standing veto window; silence means go.

Everything else is Connor's call every time: anything that spends money, changes App
Store copy, DMs real people, or publishes outside the weekly loop. Draft, show, then act.
