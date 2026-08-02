# The converting carousel — structure, CTAs, and what goes on the slides

*Written 2026-08-02 from a research pass on what actually converts for app-marketing
carousels in 2026, then narrowed to BiteBuddy's constraints. `DESIGN-SYSTEM.md` says what
a slide looks like. This says what the deck has to **do**, in what order, and how it asks
for the install. Both bind every generated post.*

---

## 1. What the research says (sourced, not our opinion)

| Finding | Number | Source |
|---|---|---|
| Optimal deck length | **7 to 10 slides.** Under 5 reads as a short post; over 10 causes mid-deck swipe fatigue | adpicto 2026 |
| Slide 1 owns the outcome | the hook slide decides ~80% of the result; if it does not earn the swipe nothing else is seen | adpicto 2026 |
| Healthy swipe-through (1 to 2) | **60 to 75%.** Under 50% is hook failure, not content failure | adpicto 2026 |
| Healthy completion | **25 to 40%**, 45%+ excellent | adpicto 2026 |
| Healthy save rate | **1.5 to 3%** for educational decks. Under 0.5% means the value slides are weak | adpicto 2026 |
| Carousels vs single image | saved roughly **35% more often** | adpicto 2026 |
| Carousels vs video (TikTok) | **81% higher engagement, 82% more likes** across a 698k-post sample; every slide emits its own dwell signal | instacarousel 2026 |
| Peer-referral framing | shares roughly **2x** | adpicto 2026 |
| Keyword / comment CTAs | convert at **5 to 15%** vs **1 to 3%** for "link in bio" | postnitro / creatorflow 2026 |
| Off-platform CTAs | IG de-weights posts that push traffic away. Use sparingly | adpicto / marketingagent 2026 |
| App-marketing creative that works | Hook, Discovery, **Demo (real screen recording)**, Result, Why-it-works | superscale 2026 |
| Format that wins on TikTok photo mode | educational listicles, one item per slide, strong save impulse | instacarousel 2026 |

**The one conclusion that matters for us:** the highest-converting app carousels do not
argue that the app is good. They show a real result, show the screen that produced it,
and ask for a low-friction action. Our CTA is a **search phrase**, not a link, which the
research supports twice over: off-platform links get de-weighted, and keyword-style CTAs
out-convert "link in bio" by roughly 5x.

---

## 2. The BiteBuddy deck skeleton (9 slides, every carousel)

Nine slides sits mid-range in the 7-to-10 window and gives room for a proof slide without
swipe fatigue. Every generated post fills these nine roles in this order. The `role` field
in the manifest names them, and the renderer lays each one out.

| # | Role | Job | Rule |
|---|---|---|---|
| 1 | `HOOK` | earn the swipe | one specific promise, a number or a question. Series chip visible. Buddy small, lower third |
| 2 | `STAKE` | say what they get | names the payoff of swiping. Never a definition or a preamble |
| 3 | `VALUE-1` | first real thing | **value lands by slide 3 or the deck has failed.** IG re-serves carousels that reach slide 3+ |
| 4 | `VALUE-2` | second real thing | one idea per slide, the changing element is the loudest |
| 5 | `VALUE-3` | third real thing | |
| 6 | `PROOF` | the app screen that produced the number | a real screenshot or a real recording still, in the phone silhouette. This is the demo slot |
| 7 | `SAVE` | the screenshot-me slide | the dense summary: cheat grid, ranked recap, the one-card version. Carries the save CTA |
| 8 | `HONEST` | the credibility beat | says the number is an AI estimate the user reviews and can edit. Non-negotiable, see §4 |
| 9 | `CTA` | ask | real Today dashboard in the phone, Buddy beside it, topic line above, download line below |

Shorter decks are allowed down to 7 by dropping `VALUE-3` then `STAKE`. **`PROOF`,
`SAVE`, `HONEST` and `CTA` are never dropped.** They are the four slides that separate a
post that sells an app from a post that is merely nice.

### Why `PROOF` is its own slide and not folded into the CTA

The CTA slide already shows the Today dashboard. `PROOF` shows the screen relevant to
*this post's claim* — the scan result behind the 485, the weekly report behind the trend
statement. The research finding is the practical one: "Demo" is its own beat in the
formats that convert, and a product shot at the end reads as an ad while a product shot
in the middle of an argument reads as a receipt.

---

## 3. The CTA ladder

**One primary CTA per deck, plus one micro-CTA earlier.** Competing asks are the most
common way a deck converts on nothing. The primary always lives on slide 9; the
micro-CTA lives on slide 7 (`SAVE`) or in the pinned comment.

| `cta_type` | Slide 9 line | Use when | Expected yield |
|---|---|---|---|
| `APP` | topic line + `Download BiteBuddy, free on the App Store` + `Search 'BiteBuddy: Ai calorie scanner'` | the post's payoff is something the app does | the install ask. Highest intent, lowest volume |
| `SAVE` | "Save this for the next time you are ordering" | reference content, cheat sheets, chain rankings | highest yield of the four archetypes for educational decks |
| `COMMENT` | "Comment your guess before you swipe" / "Name the next chain" | quiz and list formats | 5 to 15% band, and comments are our best install proxy |
| `FOLLOW` | "Follow for one of these every Tuesday" | series episodes, when the promise is repeatable | works only when paired with a stated cadence |

Rules:

- **Never a bare link CTA.** No "link in bio". The App Store search phrase is the route,
  and it is the exact string in `BiteBuddyMVP/APP_STORE_METADATA.md`, never paraphrased.
- **Every deck still ends on the phone.** Even a `SAVE` or `FOLLOW` post shows the real
  dashboard on slide 9. Only the words above it change. A sentence about an app is not a
  demo of one.
- YouTube descriptions and Facebook captions carry the clickable App Store link. TikTok
  and Instagram carry the search phrase, because those are the platforms that punish
  outbound links.
- The micro-CTA is a different verb from the primary. Save then install, or comment then
  install. Never save then save.
- Cap: **at most 2 of any 7 consecutive posts carry `cta_type: APP`.** An account that
  asks for the install every time reads as an ad account and stops being served.

---

## 4. What goes on the slides

Content types, ranked by what the research says converts for apps, and what each one
means for us:

1. **A real result with a real number.** "485 calories, and the crab cake is 140 of it."
   The number is the content; the app is how the number was obtained.
2. **The screen that produced it.** Real screenshot or a real still lifted from a
   recording. Never redrawn, never mocked, never an AI render of a UI.
3. **A reference table worth saving.** The cheat grid, the ranked chain list. This is what
   earns the 1.5 to 3% save rate; a deck with no saveable slide is entertainment.
4. **The friction, named honestly.** The under-counting, the day-4 collapse, the
   log-of-shame spiral. This is the only content Cal AI cannot run credibly, so it is
   structurally ours.
5. **Real food photography.** Never AI-rendered food. It is the fastest slop tell and it
   is exactly the profile TikTok's July 2026 crackdown targets.
6. **The estimate disclosure.** Slide 8 exists because the accuracy sceptics are the
   loudest commenters in this niche. Saying "AI estimate you can edit" before they say it
   converts the objection into a credibility beat. Claim consistency, never precision.

Never on a slide, in any deck, at any time: medical or outcome claims, weight-loss
promises, crash-diet or disordered-eating framing, the Meal Advisor, invented UI, or
invented numbers. Guardrails in `CLAUDE.md` win over anything in this file.

---

## 5. Asset autonomy (the rule that keeps this hands-off)

**Generation never asks Connor for a screenshot.** Every image a deck needs comes from one
of three places that already exist in the repo:

1. `UI-Library/**` — the 19 canonical app screenshots.
2. `UI-Library/Recordings/stills/` — frames harvested from screen recordings by
   `Content-Engine/harvest_frames.py`. A single recording yields fresh, real, in-motion app
   imagery that no screenshot library can match, and harvesting is automatic.
3. `Brand-Assets/buddy-poses/transparent/` — the 13 canonical Buddy renders, selected
   automatically by series and hook family.

Food photography is the one asset class not in the repo. Until a licensed source is wired
in, decks that need a food photo use a recording still of the real plate (which is better
anyway, since it is the plate the app actually scanned), and decks with no photo available
render as typographic layouts. **A post is never delayed waiting on an asset, and a
missing asset is never solved by generating a fake one.** It is solved by rendering the
typographic variant and saying so in the report.

## 6. Measuring whether any of this is true

Every number in §1 is somebody else's. Ours go in `Analytics/performance-log.jsonl`, and
the weekly report is expected to compare us against that table directly: swipe-through
against 60 to 75%, save rate against 1.5 to 3%, completion against 25 to 40%. Where the
platform does not expose a metric the report says so rather than substituting a proxy
silently. The first report that can run this comparison should say plainly which of these
benchmarks BiteBuddy does not clear, because that is the fastest route to knowing whether
the problem is the hook, the value slides, or the ask.
