# Demo edit spec — how a raw screen recording becomes a post

*The editorial standard for the video track. `demo-drop` is the procedure (find
clips, build, schedule); this is the craft: what to cut, what to keep, what makes
a clip unusable, and what must never reach a platform. Written 2026-07-25 from
the first real edit and updated whenever a clip teaches us something.*

---

## The one rule everything else serves

**The payoff must land by 8 seconds.** The payoff is the moment the number
appears on the result screen. Everything before it is setup, and setup is the
only thing viewers ever leave during.

The first real clip is the case study. Raw, its 485 cal result arrived at
**15 seconds**: dashboard, camera, framing, confirm, then a six-second analysing
wait. Nobody on TikTok waits 15 seconds for a payoff they were not promised.
Compressing camera-through-analysing 2.5x moved it to **8 seconds** and cost
nothing, because none of that footage is *interesting*, it is just necessary.

If a clip cannot get its payoff under 8 seconds even after compression, it is
either the wrong recording or it needs a harder start point. Say so rather than
shipping a slow one.

---

## The four timestamps

Extract frames every 2 seconds across the whole clip and **look at them**. Never
guess these from duration alone.

| | What you are looking for |
|---|---|
| **start** | First frame already on the dashboard, past any fumbling, tapping into the app, or app switcher |
| **speed-from** | Where setup stops being informative, usually once the camera is up |
| **speed-to** | The instant the result screen appears |
| **end** | One beat after the log confirmation, before anything else happens |

Then run a precision pass at 0.3 to 0.5s intervals around each boundary. A cut
half a second late can include a notification banner or a Control Center swipe.

---

## Always cut

These are non-negotiable and every one of them is a real thing that appears in
phone recordings:

- **iOS Control Center or the swipe that opens it.** The first clip had it from
  ~29s; it was cut at 28.4s. Shipping it looks like a mistake because it is one.
- **Notification banners.** Anything that slides in from the top.
- **The app switcher, home screen, or the tap that launches the app.**
- **Fumbling**: repositioning the phone, a mis-tap, a back-and-forth.
- **The keyboard**, unless the post is specifically about typing a note.
- **Dead air after the log confirms.** The post ends on the win.

## Privacy scrub, before anything is scheduled

Screen recordings capture more than the app, and this is the failure mode most
likely to cause a real problem. Check every clip for:

- **Personal name in the greeting.** The Today screen says "Good evening,
  Connor". That is fine and even humanising for our own account, but it is a
  decision, not an accident. Never ship a clip showing *someone else's* name.
- **Real health data** you are not comfortable publishing. Logged calories,
  weight, streaks and goals are all on screen. The first clip shows 680 cal
  logged and a 2540 remaining target; Connor is publishing his own numbers
  knowingly.
- **Other apps and devices**: the Control Center in the first clip listed a
  named Apple TV. Cut it.
- **Carrier, battery, time, location** in the status bar. Usually harmless,
  occasionally not.
- **Audio.** Recordings often capture ambient room sound including other people
  talking. `build_demo.py` strips audio unconditionally, which is a safety
  feature, not just a format choice.

If anything on this list is present and cannot be cut, do not ship the clip. Ask.

---

## Speed ramps

- Speed **setup**, never the payoff. The result screen, the itemised list and the
  log confirmation always play at real time.
- **2 to 3x** is the usable band. Past 3x the UI reads as glitchy rather than
  fast.
- The analysing screen can be sped freely. It is a progress indicator, and
  Buddy's animation still reads at 2.5x.
- `build_demo.py` supports **one** speed window. If a clip needs two, either pick
  the more wasteful stretch or re-cut the source.

## Hook text

Burned over the opening ~2.5 seconds, so it must be legible in half a second and
**true to what the footage actually shows**.

- 5 to 8 words. "One photo found all four foods" works because the video then
  shows exactly four foods.
- Name the friction the scan removes, or name the surprise.
- **Never claim precision.** No "perfectly accurate", no "exact". The result
  screen itself says estimates can be inaccurate and should be reviewed; the copy
  should agree with the product rather than oversell it. The accuracy sceptics
  are the loudest commenters in this niche (see the anti-persona in
  `TARGET-USER-PROFILES.md`).
- No em dashes. House rule, applies to burned-in text too.

## End card

Fixed, non-negotiable, and identical in language to the carousel CTA slide: the
real Today dashboard in a phone silhouette, Buddy beside it, the topic CTA above,
`Download BiteBuddy, free on the App Store` beneath, and the App Store search line.
Three seconds. Built by `phone_mock()` so the video and carousel tracks cannot
drift apart visually.

## Duration

| Platform | Target | Note |
|---|---|---|
| TikTok, Instagram | **12 to 25s** | shorter is safer; retention is the whole game |
| YouTube Shorts | **30 to 40s** | a 15s Short needs ~100% retention to clear the watch-time gate, a 35s Short clears at ~65% |

A single edit rarely satisfies both. Current practice is one cut in the 20 to 25s
range used everywhere, which is good for TikTok and Instagram and acceptable for
Shorts. If a clip is rich enough to support a longer YouTube cut, make two.

---

## QA before scheduling

1. Extract frames from the **finished** file at the hook, the payoff, and the end
   card, and look at them. The hook and end card are burned in; a bad one is only
   visible if you look.
2. Confirm dimensions are exactly **1080x1920**.
3. Confirm the payoff timestamp is under 8 seconds.
4. Walk the privacy list above.
5. Confirm no em dashes in the hook, caption, or pinned comment.

## When a clip is unusable

Say so and stop. Reasons that disqualify a clip: the payoff cannot get under 8
seconds, the result screen is never held still long enough to read, the food is
unrecognisable, someone else's data is on screen, or the recording is portrait-
rotated mid-take. **Never ship a weak demo to fill a slot.** An empty slot costs
one day; a bad demo of the core product costs more than that.
