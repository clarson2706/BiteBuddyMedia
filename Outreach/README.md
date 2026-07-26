# Outreach — the creator engine

$0-upfront creator partnerships: free Pro (6 months, renews while active) + 30% of
each attributed subscriber's first payment. Claude writes everything; Connor
presses send. US-based creators only, 2k-50k followers.

| File | What |
|---|---|
| `DM-PLAYBOOK.md` | the deal, hard rules (no em dashes ever), first-message structure, full conversation flow, canned replies, onboarding pack spec |
| `CREATOR-TERMS.md` | the one-page terms creators agree to ("I agree" in DM) |
| `creators.jsonl` | pipeline tracker, one line per creator, append-only |
| `payouts.jsonl` | the payout ledger behind every PayPal send |
| `queue/YYYY-MM-DD.md` | staged, not-yet-delivered daily batch (10 IG + 10 TikTok), written by the Sunday research run |
| `batches/YYYY-MM-DD.md` | archived record of what was actually delivered for that day |

Cadence: all research happens once a week, Sunday morning (140 DMs: 10 IG + 10
TikTok x 7 days), staged into `queue/`. Each day that file is delivered (email,
once a sending connector is set up; a Gmail connector is planned but not yet
connected, see `CLAUDE.md`) and archived into `batches/`. Full procedure: the
`creator-pipeline` skill (`.claude/skills/creator-pipeline/SKILL.md`). Connor
sends ~20/day spread through the day, forwards replies. Payouts computed in the
Sunday run closest to month end, logged here, sent by Connor via PayPal.
