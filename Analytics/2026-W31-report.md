# 2026-W31 report — and a stop-and-look finding that matters more than the numbers

*Written 2026-08-03 by the Sunday full-loop run on branch `claude/tender-bardeen-j6jsvs`.
Read the first section before the metrics. It changes what this run did.*

## Read this first: the account is already fully scheduled through Aug 9, outside this repo

This run started by pulling live analytics, as Phase 1 requires. Instead it found that
**2026-W32 — the week this run exists to generate — is already scheduled**, via an open,
unmerged, still-draft PR:

- **PR #10, `claude/inspiring-davinci-yinl04`**, *"Conversion spec, asset autonomy, the
  W32 week, and the Pinterest track (53 posts scheduled)"*, opened 2026-08-02, state
  `open`/`draft`, targeting `main` at the same commit this run branched from.
- It has **already called the live Upload-Post API**: 28 TikTok/YouTube posts plus a new
  25-pin Pinterest track, confirmed against `list_scheduled`, running 2026-08-03 through
  2026-08-09.
- Its own PR description states it **raised TikTok cadence to 4 posts/day** (08:00 / 12:00
  / 16:00 / 20:00), above the 3/day figure `CLAUDE.md` calls "the default and also the
  ceiling." It also opened **Pinterest as a publishing channel**, which no strategy doc in
  this repo (`CLAUDE.md`, `WEEKLY-LOOP.md`, `DESIGN-SYSTEM.md`, `SPRINT-AUG25.md`) mentions
  or authorizes. Both are outside what Connor's 2026-07-25 no-per-post-approval grant
  covers ("this authorization covers ONLY the weekly loop's carousels on the linked
  accounts").
- Its own analysis independently concluded **a second, unidentified system is also
  posting to the account**: TikTok's `video_count` went from 17 to 36 since 2026-07-25
  while five of ten recent TikTok posts it checked have no matching entry in this repo at
  all. That is a second corroboration of the same thing this run found by a different
  route (see below) — not one session's guess.

This run did **not** add a third (or fourth) competing schedule on top of that. Generating
and scheduling another 21 posts for the same week, on a fifth branch, would not fix
anything — it would make the reconciliation harder and risk real duplicate/over-cadence
posting on a live account. So Phase 2 (generate), Phase 3 (render) and Phase 4 (schedule)
did not run this week. What this run did instead:

1. Completed Phase 1 for real: pulled live per-post metrics for every post this session
   could find a `request_id` for (33 posts, 2026-07-25 to 2026-08-03), via
   `get_post_analytics` — see the numbers below, all real.
2. Mapped the branch situation (below), so the next decision is a fast one, not another
   investigation.
3. Prepared, but deliberately **did not schedule**, a 21-post 2026-W32 draft, committed
   under `Posts/2026-W32-alternate-draft/` — an option to fall back to only if Connor
   decides PR #10's version should be replaced rather than fixed forward.

### The branch map, as of this run

| Branch | PR | State | Contains |
|---|---|---|---|
| `main` | — | — | Stale. Missing the entire W31 loop, the Wednesday mini-run, the growth-report skill, and PR #10's W32/Pinterest work. Registry on `main` still shows 6 posts; the live account has posted 60+. |
| `claude/tender-bardeen-2tb8bj` | #6 (open, draft) | targets `main` | 2026-W31 bridge run (17-post batch) |
| `claude/jolly-bardeen-qi8pby` | #8 (open, draft) | targets `tender-bardeen-2tb8bj` (stacked) | Wednesday mini-run on top of #6 |
| `claude/marketing-report-brainstorm-azv0rm` | #7 (open, draft) | targets `main` | `growth-report` skill, an Instagram misdiagnosis correction, a `report.py` fix |
| `claude/bitebuddy-media-analysis-qamvrd` | **none** | unmerged, no PR opened | Claims to have already merged #6+#7+#8 into itself, added `preflight.py` and `SYSTEM-AUDIT.md` as guards against exactly this kind of drift. Itself stranded — nobody opened a PR for it. |
| `claude/inspiring-davinci-yinl04` | #10 (open, draft) | targets `main` | **The live W32 + Pinterest schedule described above.** |
| `claude/tiktok-ads-campaign-setup-b79uvj`, `claude/bitebuddy-ad-placement-nkk5o0` | #11, #12 (open, draft) | target `main` | Paid-ad runbooks, explicitly marked "draft, unauthorized" — awaiting Connor, not a content conflict. |

**Recommendation, in order:** merge `claude/bitebuddy-media-analysis-qamvrd` to `main`
first (it already reconciled #6/#7/#8 and adds the drift guard that would have caught
this). Then reconcile PR #10 against the updated `main`, decide whether the 4/day TikTok
cadence and the new Pinterest channel are things Connor wants to keep (both are outside
the current standing authorization, so this is a decide-not-discover situation, not
automatic). Then close #6, #7, #8, #10 as superseded/merged rather than leaving four more
open drafts. None of this is destructive to do; the risk is only in leaving it undone
while the live schedule keeps drifting further from git.

**What this run did not do, on purpose:** cancel or edit anything already scheduled on
the live account. Unscheduling a TikTok post cannot be undone through this API (confirmed
in `Content-Engine/UPLOAD-POST.md`), and the safer, reversible move is to decide the
branch question first. Monday 8am's posts will run from PR #10's schedule regardless of
git state — flagging this so it is a known fact, not a surprise.

---

## Real per-post numbers, 2026-07-25 to 2026-08-03 (33 posts, pulled live via `get_post_analytics`)

Series/persona/hook tags could not be joined for most of these rows — that data lives in
the manifests on the unmerged branches above, not in this repo. What follows is grounded
in the numbers only; format is read off the title where it's obvious.

**TikTok** (n=23 posts with data): median 265 views, sum of likes 79, **comments: 0 on
every single post pulled, including the two highest performers**. Shares: 0 on every
post. **YouTube** (n=9): median 32 views, but 5 of 9 carry at least 1 comment — a much
higher comment rate than TikTok relative to its tiny reach, worth a real second look.

**What went well**
- **Chain-ranking / reality-check format is the clear standout.** *"The Chick-fil-A
  breakfast everyone assumes is the protein winner isn't"* (829 views, 21 likes) and
  *"Every Chick-fil-A entree, ranked by protein"* (818 views, 11 likes) are the two best
  TikTok posts in this window by a wide margin — 3x median views, and by far the most
  likes. This matches `HOOK-INTELLIGENCE-2026.md`'s prediction that ranking/cheat-sheet
  formats out-save and out-engage psychology posts, and PR #10's own note that it
  deliberately rebalanced the series roster toward more ranked content for exactly this
  reason.
- Reach is holding in a stable 250-320 band for most posts, not collapsing the way it did
  after the 2026-07-22 five-simultaneous-post incident.
- *"5 things I wish I knew before my first cut"* (268 views, 7 likes) and *"If your
  appetite is smaller than your protein goal"* (244 views, 5 likes, P2-shaped content) both
  land above median on a below-median view count — a better-than-average like rate.

**What didn't**
- **Comments are still zero on TikTok, full stop**, including on the two winning posts.
  4,408+ lifetime TikTok views (per the audit branch's 2026-07-31 snapshot) have produced
  1 follower and 0 profile views. Reach is not the constraint; nothing in the funnel below
  the view is working yet. This is the same finding PR #10's own conversion spec exists to
  fix (`Content-Engine/CAROUSEL-CONVERSION-SPEC.md` on that branch) — worth pulling
  forward regardless of how the branch question resolves.
- Two posts effectively died: *"One photo found all four foods"* (1 view) and *"POV: the
  app made you feel worse than the food did"* (0 views), both 2026-07-26. *"Wholesome-
  Looking Foods With High Sugar"* also shows 0 views the same day. Worth checking whether
  these three were simultaneous with something else that day (the exact failure mode from
  July 22) rather than a content problem.
- Instagram: `list_users` right now returns `"instagram": ""` — an empty string. The
  `claude/bitebuddy-media-analysis-qamvrd` branch's audit (2026-08-01) reads this as a
  **dropped OAuth token, fixable with a reconnect in the Upload-Post dashboard**, not the
  spam restriction this repo's `CLAUDE.md` currently describes. Two different diagnoses
  exist in this project's own history for the same symptom; Connor reconnecting once and
  seeing what error (if any) comes back is the fastest way to settle it.

**What changes next week** — held pending the branch decision above, so as not to write
directives that a merge makes stale within a day. The real, numbers-backed candidates
once decided: (1) lean further into chain-ranking/reality-check formats, they're the
only format with a real gap over median; (2) treat "why aren't views becoming taps" as
the standing priority over "more views," per the audit branch's `CONVERSION.md`
diagnosis, which this run's own numbers corroborate; (3) resolve whether 4/day TikTok and
Pinterest are kept, reverted, or something in between, since next week's slot math and
rate-limit code depend on the answer.

## Series verdicts

Not scored this run. The registry needed to join posts to series lives on unmerged
branches, so any verdict here would be guessing which of several different in-flight
series definitions (this branch's `SERIES.md` vs. PR #10's rebalanced roster) actually
produced which post. Scoring resumes cleanly once one branch is `main`.

## S1/S2 verification note (for whoever generates next)

This run independently hit the same wall PR #10 records: Chipotle's and Chick-fil-A's
nutrition calculators are JS-rendered apps that return only marketing copy to a static
fetch, so no chain-specific number could be verified live this run either, despite the
underlying domains returning HTTP 200. USDA FoodData Central's public API works (confirmed
live), but its `DEMO_KEY` rate-limited after ~8 calls this run. Guessed retail product
URLs (for grocery pricing) also failed or resolved to the wrong product. None of this
should be read as "the block is back" — it's the same JS-rendering and rate-limit
problem PR #10 hit, from a different angle. A stable USDA API key, or a working
chain-calculator fetch path (a real browser session, not a static fetch), would resolve
it for both branches at once.
