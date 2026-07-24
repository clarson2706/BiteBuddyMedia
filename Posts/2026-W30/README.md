# Week 2026-W30 — carousel materials

Everything for this week's 21 BiteBuddy carousels, packaged and ready to generate.

## What's here
- `CHATGPT-GENERATION-GUIDE.md` — **hand this to ChatGPT** to generate all 21 posts' images
  and **commit them straight into the `slides/` folders** (no manual downloads).
- `assets/today-home-hero.png` — the one screenshot ChatGPT needs (upload it first).
- `<post-id>/prompts.md` — the self-contained generation package for that post.
- `<post-id>/slides/` — where ChatGPT commits that post's finished `01.png…`.
- `manifest.json` — machine source of truth the publishing step reads.

## Your steps
1. **Give ChatGPT GitHub write access** to `clarson2706/BiteBuddyMVP`: connect the GitHub
   connector / a Custom GPT Action (*Contents: read & write*), or have a fine-grained PAT ready to
   paste when it asks. **Never commit the token.**
2. Open ChatGPT, upload `assets/today-home-hero.png`, paste `CHATGPT-GENERATION-GUIDE.md`, and say:
   *"generate and upload the images for week 2026-W30".* It works post by post, commits each
   post's `01.png…` into `Posts/2026-W30/<post-id>/slides/` on `main`, and replies **done**.
3. Skim the new commits (or `git pull`) to confirm the images landed, then reply **"images are in"** —
   the publishing step takes it from there. *(Fallback: if write access isn't set up, ChatGPT returns a
   `<post-id>.zip` per post and you drop the files into each `slides/` folder yourself.)*

## Content model (why it looks the way it does)
- Slides 1…N-1 **teach** (nutrition facts, real food photos, honest tips). No app UI, no per-slide branding.
- The **last slide of every post** is the only app moment: the Today-home hero in a phone silhouette +
  *"Download BiteBuddy — free on the App Store"* + a call-to-action tied to that post's topic.
- Every image is a constant **1080×1350 (4:5)**.

## Non-negotiable visual quality
- Use a deliberate spacing grid on every slide: keep **72–96 px safe margins**, align repeated elements,
  maintain consistent vertical rhythm, and balance negative space. Do not drop copy into oversized generic
  cards or leave the composition feeling accidentally empty.
- Review the carousel both as a contact sheet and at full resolution before committing. Typography must
  have clear hierarchy, comfortable line spacing, and no crowded or orphaned lines.
- On every final CTA slide, the real app screenshot must appear **edge-to-edge inside an unmistakable
  upright iPhone silhouette** with the correct tall aspect ratio, rounded screen corners, a thin uniform
  bezel/device rim, subtle hardware detail, and a grounded shadow. It must visibly read as a phone.
- Never present the screenshot as a floating image, flat card, generic rounded rectangle, placeholder panel,
  or a frame with thick black bars above and below the UI. Keep the supplied screenshot unaltered and use it
  only on the final slide.
- If the spacing, typography, or phone treatment fails this quality bar, revise it before any image is
  committed to GitHub.


## The 21 posts

**2026-07-20**
- 08:00 · `F1-buddys-list` · 7 foods sabotaging your protein goal
- 12:30 · `F2-guess-the-calories` · Guess the calories: fast-food edition
- 19:00 · `F3-i-was-wrong` · I quit calorie tracking 4 times

**2026-07-21**
- 08:00 · `F4-one-snap-demo` · Why you keep quitting food tracking
- 12:30 · `F1-buddys-list` · 5 reasons calorie tracking fails (and the fix)
- 19:00 · `F2-guess-the-calories` · Guess the calories: coffee shop edition ☕

**2026-07-22**
- 08:00 · `F3-i-was-wrong` · I thought I ate 1,500 calories
- 12:30 · `F4-one-snap-demo` · 5 ways to actually know what's in your food
- 19:00 · `F1-buddys-list` · 6 'diet' drinks with more sugar than soda

**2026-07-23**
- 08:00 · `F2-guess-the-calories` · Guess the calories: 'healthy' snacks that aren't
- 12:30 · `F3-i-was-wrong` · The real reason you quit calorie apps
- 19:00 · `F4-one-snap-demo` · How to read a nutrition label in 10 seconds

**2026-07-24**
- 08:00 · `F1-buddys-list` · 7 late-night snacks bigger than you think
- 12:30 · `F2-guess-the-calories` · Guess the protein 💪
- 19:00 · `F3-i-was-wrong` · POV: a calorie app that's actually kind

**2026-07-25**
- 08:00 · `F4-one-snap-demo` · Portion size: the #1 thing people get wrong
- 12:30 · `F1-buddys-list` · Why your calorie app makes you miserable
- 19:00 · `F2-guess-the-calories` · Same dish, restaurant vs homemade

**2026-07-26**
- 08:00 · `F3-i-was-wrong` · 3 years of failed tracking
- 12:30 · `F4-one-snap-demo` · What actually matters on a nutrition label
- 19:00 · `F1-buddys-list` · 6 restaurant meals hiding a full day of calories

