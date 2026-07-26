---
name: creator-pipeline
description: >-
  Run BiteBuddy's creator-outreach pipeline. Two modes gated by day-of-week.
  Sunday: research and write a full week of creator DMs (10 Instagram + 10
  TikTok x 7 days = 140 total), US-based creators only, 2k-50k followers,
  staged into Outreach/queue/YYYY-MM-DD.md, one file per upcoming day, and
  append every creator to Outreach/creators.jsonl. Every day (including
  Sunday): deliver that day's queued file (email once a sending connector is
  connected; otherwise present the full batch in the response) and archive it
  to Outreach/batches/YYYY-MM-DD.md. Use whenever Routine 3 (the daily
  creator-DM routine) fires, or on "run the creator pipeline", "generate
  today's creator batch", "send today's creator email". Replaces the old
  research-every-day behavior; research now happens once a week.
---

# creator-pipeline — Sunday research, daily delivery

Read `Outreach/DM-PLAYBOOK.md` first, always — it is the contract (the deal
terms, hard rules, targeting criteria, tone rules). This file is the
procedure for when/how much to research and how delivery works. Also skim
`Outreach/CREATOR-TERMS.md` and `Outreach/README.md`.

**Changed 2026-07-26:** research used to happen on every daily-routine fire.
It now happens once a week, Sunday morning, producing a full week's worth of
DMs at once. Every day (including Sunday) the pipeline's other job is
delivering that day's pre-staged batch. Get the current date from the
environment (e.g. `date` in Bash, or the `currentDate` system context) —
never assume.

## Step 1 — is today Sunday?

Check the day of week for today's actual date. If yes, run **Phase A** below
before Phase B. If no, skip straight to **Phase B**.

## Phase A — Sunday research (140 creators)

Only runs on Sunday. This is a substantial research operation; expect it to
take multiple subagent rounds, same as the manual runs on 2026-07-25 and
2026-07-26 that this skill formalizes.

1. **Targeting** (from `DM-PLAYBOOK.md`, do not drift from these without
   Connor's explicit say-so): US-based creators only, 2,000-50,000 followers,
   across macro-friendly recipes, budget meals, college food, new-lifter
   fitness, honest weight-loss journeys, busy-parent meals, dietitian
   students. Skip crash-diet/detox/disordered-eating-adjacent content,
   medication- or medical-intervention-focused accounts, mega accounts, and
   anyone with no specific personalizable detail in their real content.
2. **Exclude everyone already in the pipeline.** Read `Outreach/creators.jsonl`
   in full and exclude every handle at any status, not just `sent`. This is
   the single dedupe source of truth.
3. **Fan out research in parallel**, roughly one subagent pair (Instagram +
   TikTok) per day of the coming week, or run it as a small number of larger
   rounds — whichever gets to verified, real, personalizable creators
   fastest. Sonnet is sufficient (this is research + short writing, not
   deep reasoning). Each subagent must:
   - Use WebSearch (and WebFetch if it's working this session, it has not
     been reliable historically, confirm before depending on it) to find
     real, currently-active, verifiable handles — never invent a handle,
     follower count, or content detail.
   - Cross-check each candidate across 2+ independent queries.
   - Confirm US-based-ness specifically (bio location, US school, US
     city/brand/unit references) — drop anyone who can't be confirmed.
   - Write a personalized DM per `DM-PLAYBOOK.md`'s first-message structure
     and hard rules (no em dashes, one specific real detail, "small is the
     pitch," the current 6-months-renewable Pro offer, never "forever").
   - Report honestly if it can't hit its target count — a documented
     shortfall beats a padded list every time. This has happened before
     (TikTok specifically has been a harder search surface some days) and is
     expected to keep happening some weeks; that's fine, report it plainly.
4. **Pretest every link.** Attempt to WebFetch each profile URL and confirm
   it resolves and matches the expected creator (right name/handle, content
   consistent with what was cited in the DM). If WebFetch is unavailable
   this session (it has been down for entire sessions before, confirm with a
   trivial fetch first, e.g. example.com), fall back to the same
   cross-checked WebSearch-snippet method used in the manual runs, and mark
   every entry's confidence level accordingly rather than silently treating
   search-only verification as equivalent to a live fetch.
5. **Split results into 7 daily files**, `Outreach/queue/YYYY-MM-DD.md`, one
   for each of the next Monday through Sunday (if today's date doesn't
   already fall on Monday-starts-the-week, compute the correct 7 calendar
   dates). Each file: 10 Instagram + 10 TikTok, same per-entry format as
   existing `Outreach/batches/*.md` files (handle, profile link, one-sentence
   who-they-are, one-sentence why-fit, ready-to-copy DM, confidence note).
   Include a short header noting total count if under 140, and why.
6. **Append every creator to `Outreach/creators.jsonl`** with
   `status: dm_written` and a note identifying which date's queue file they
   belong to.
7. Commit and push everything from Phase A before moving to Phase B.

## Phase B — daily delivery (every day, including Sunday)

1. Look for `Outreach/queue/<today's date>.md`. This should exist either
   because Phase A just wrote it (Sunday), or because last Sunday's Phase A
   run staged it (Monday-Saturday).
   - **If it's missing** (Sunday's run never happened, failed partway, or
     this is the first time this skill has run): fall back to generating
     just today's single-day batch (10 Instagram + 10 TikTok, same targeting
     rules) using the same research method as Phase A step 3, so Connor
     still gets DMs today. Flag clearly in the delivery that the weekly
     cadence has a gap and Sunday's run needs attention.
2. **Deliver it.**
   - Search for an email-sending tool (`ToolSearch` with a query like "gmail
     send email"). If one is available and connected, send the day's batch
     to Connor's email (see `userEmail` in system context) with two clearly
     separated sections (10 Instagram, 10 TikTok), each entry showing the
     profile link, a one-sentence who-they-are-and-why-fit, and the ready DM.
     Subject line: `BiteBuddy creator DMs — <date>`.
   - If no email tool is available yet (expected until Connor connects one,
     see `CLAUDE.md` activation checklist), present the full batch directly
     in the response instead, exactly as done manually on 2026-07-25 and
     2026-07-26, and note that email delivery is pending the connector.
3. **Archive.** Copy (don't just move, keep history clean) the delivered
   file's content into `Outreach/batches/<today's date>.md` as the permanent
   record of what actually went out. The `queue/` copy can then be deleted
   or left in place, either is fine, `batches/` is the source of truth once
   delivered.
4. Commit and push.

## Hard rules (inherited from `DM-PLAYBOOK.md`, never relaxed here)

- No em dashes anywhere in generated copy.
- Every DM references one specific, real, verified detail — never generic
  praise, never a fabricated detail.
- Never imply BiteBuddy is bigger than it is.
- The offer is always exactly what `DM-PLAYBOOK.md`'s current deal section
  says (6 months free Pro, renews while active, 30% of first payment only) —
  if that document changes, this skill's output changes with it, never the
  other way around.
- A shortfall in count is reported honestly, in the file itself, every time.
  Never pad with an unverifiable or fabricated entry to hit a round number.
- International creators and anyone outside 2k-50k followers are out of
  scope until Connor says otherwise.
