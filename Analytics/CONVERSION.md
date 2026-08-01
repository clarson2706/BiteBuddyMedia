# Conversion — why 4,408 views have produced zero installs, and the fix

*Written 2026-08-01 from live Upload-Post numbers. This is the most important file in
`Analytics/`, because every other measurement in this repo is upstream of the thing it
describes.*

---

## 1. The number

| TikTok, lifetime | |
|---|---|
| Views | **4,408** |
| Likes | 59 (1.3%, a normal rate) |
| Comments | **0** |
| Shares | **0** |
| Profile views | **0** |
| Followers | **1** |

Daily views went 0 → 194 → 423 → 814 → 1,700 across the last two weeks. The
distribution problem that dominated every report in July is **solved**. TikTok is
showing this account to thousands of people.

And the funnel dies immediately after the view.

## 2. Where it breaks

```
   view  ->  like  ->  profile tap  ->  bio link  ->  App Store page  ->  install
   4,408      59            0            no link         no tracking        unknown
                            ^
                            └── everything stops here
```

Three separate breaks, in order of severity:

**Break 1 — nothing asks for the profile tap.** On TikTok a post cannot link out. The
profile tap is the *only* path from a view to an install, and until 2026-08-01 not one
slide asked for it. The CTA slide said "Download BiteBuddy, free on the App Store" and
named a search phrase, which asks a scrolling stranger to leave the app, open another
app, and type. Almost nobody does that. The tap is the ask that fits the medium.

**Break 2 — there is no bio link, so there is nothing to tap even if they did.**
Whatever is in the profile now, this repo has never specified it, never tracked it, and
never measured it. A profile with no obvious next step converts like a profile with no
profile.

**Break 3 — no attribution exists at all.** `Analytics/installs.jsonl` was designed as
a manual weekly paste from App Store Connect and has never been created. So even on a
week where installs happened, nothing could attribute them to a post, a series, or a
platform. Every optimization the loop has ever run has been optimizing engagement
proxies with no idea whether they lead anywhere.

**This is the same failure the repo was rebuilt to prevent**, one layer down. The old
system measured nothing. The new system measures engagement carefully and still cannot
answer "did this produce a user."

## 3. The fix, in dependency order

### 3.1 Ask for the profile, not the App Store (in the content)

Done, in code: `render_slides.slide_cta()` now closes every carousel with
**"Follow @bitebuddyapp for more"** on a lavender chip beneath the download line, on
every post regardless of its primary CTA type. The download line and the search phrase
stay; the follow ask is added, because it is the only one of the three that the viewer
can act on without leaving the feed.

The stronger version, for the series that earn it: end on a reason to come back.
"Follow, I do a new chain every week" converts better than "follow" because it names
what the follow buys. `SERIES.md` puts that line on S2 and S4 by default.

### 3.2 Make the profile a landing page (Connor, 10 minutes, one time)

The bio is the only clickable surface on TikTok. Treat it as a landing page:

```
Line 1   what it is        AI calorie scanner. Photo your plate, get the number.
Line 2   why it is worth   Free on iOS. Estimates you can edit, no guessing.
Line 3   the ask           Download free ↓
Link     trackable         https://apps.apple.com/us/app/bitebuddy-ai-calorie-scanner/id6787834752?pt=<pt>&ct=tiktok_bio&mt=8
```

The `ct` (campaign token) is what makes App Store Connect break out installs by source.
Use a distinct `ct` per surface so the report can compare them:

| Surface | `ct` value |
|---|---|
| TikTok bio | `tiktok_bio` |
| Instagram bio | `ig_bio` |
| YouTube channel + descriptions | `yt_desc` |
| A creator's link | `creator_<handle>` (already the scheme in `Outreach/`) |

Apple's campaign-token breakdown appears in App Store Connect under App Analytics →
Sources → Campaigns. It costs nothing and it is the only first-party install
attribution available for organic social.

### 3.3 Pin the conversion post (Connor, 2 minutes, then revisit monthly)

Pin one post to the top of the TikTok profile: the one a curious profile-tapper should
see first. **Pin for link-click rate, not for views.** The right candidate is a demo —
the scan flow, start to finish — because it answers "what is this app" in four seconds,
which is exactly the question a profile visitor arrived with.

Until a demo has data, pin the highest-saving carousel.

### 3.4 Start `installs.jsonl` this week (Connor, 10 seconds/week)

One line per week, pasted from App Store Connect → App Analytics → Metrics:

```json
{"week":"2026-W31","impressions":0,"product_page_views":0,"downloads":0,
 "by_campaign":{"tiktok_bio":0,"yt_desc":0},"source":"app-store-connect"}
```

`product_page_views` is the number that matters most right now. It is the direct
measure of break 1 and break 2: if profile taps start happening, product page views
move before downloads do, and it moves within a day rather than a week.

## 4. The conversion scorecard (goes at the top of every weekly report)

The weekly report currently leads with reach. From 2026-08-01 it leads with this table,
because reach is no longer the constraint:

| Metric | This week | Last week | Direction |
|---|---|---|---|
| Views | | | |
| **Profile views** | | | **the primary metric** |
| Follows | | | |
| Saves + shares | | | |
| Product page views (ASC) | | | |
| Downloads (ASC) | | | |
| **Views per profile view** | | | lower is better |

**Views per profile view is the single number this system is now optimizing.** It is
currently undefined, because the denominator is zero. Any week it becomes a finite
number is a week something worked, and the report must name which post did it.

## 5. Honest caveats

- **Upload-Post reports `profileViews: 0` for TikTok**, and TikTok's own export showed
  1 profile view in a seven-day window. So the metric may be under-reported at the
  source. It is not under-reported by three orders of magnitude: 1 follower against
  4,408 views is unambiguous whichever number you trust, and it says the same thing.
- **A follow is not an install** and the ladder still ends at installs. The follow ask
  is a step, not the destination, and if follows start rising while product page views
  stay flat, that is a finding, not a success.
- **Attribution will be partial.** Some people will search the App Store directly after
  seeing a post, and those installs will look organic. That is an argument for keeping
  the search phrase on APP-CTA posts, not for skipping the tracked link.

## 6. What is blocked on Connor

Nothing in section 3.1 (already shipped in code). Everything else:

1. Set the TikTok bio and the tracked link with `ct=tiktok_bio` (10 min, one time).
2. Pin a conversion post (2 min).
3. Paste one `installs.jsonl` line per week (10 sec/week).
4. Reconnect Instagram in Upload-Post — it currently returns an empty string, which is
   a dropped token, not a ban (2 min).

Items 1 and 3 are the two that change what this repo can know about itself.
