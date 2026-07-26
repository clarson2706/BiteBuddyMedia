# Outreach/queue — staged, not-yet-delivered creator DM batches

Written by the Sunday run of the `creator-pipeline` skill
(`.claude/skills/creator-pipeline/SKILL.md`): one file per day,
`YYYY-MM-DD.md`, covering the coming Monday through Sunday (140 creators
total, 10 Instagram + 10 TikTok per day).

Each day, the same skill delivers that day's file (email once a sending
connector is connected, otherwise presented directly in the routine's
response) and archives its content into `Outreach/batches/YYYY-MM-DD.md`,
the permanent record of what actually went out.

This directory is expected to be empty between Sundays and delivery runs,
except for whichever days haven't been delivered yet.
