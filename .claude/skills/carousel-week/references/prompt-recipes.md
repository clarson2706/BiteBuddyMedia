# prompt-recipes — writing the per-slide ChatGPT prompts + captions + hashtags

How to turn a slide's copy into a paste-ready ChatGPT image prompt, plus the
caption formula and hashtag pools. Connor pastes the week's
`CHATGPT-GENERATION-GUIDE.md` into ChatGPT and gets back one **zip of separate
PNGs per post**, which he drops into each post's `slides/` folder as `01.png…`.

## The content model these recipes serve (don't skip)
- **Educate first, sell last.** Body slides teach; only the **final slide** shows
  the app. See SKILL.md → "Content model."
- **Constant size — every image is `exactly 1080 x 1350 pixels (4:5 vertical)`.**
  Put that phrase in every prompt.
- **Palette:** cream `#FFF8F1` background, accents peach `#F4A261` / deep orange
  `#E9843A` / sage `#8FA27F` / lavender `#C9C4F2`.
- **Text on image:** ChatGPT renders the headline. Give it the EXACT text in
  quotes and say "reading exactly … and nothing else." Keep headlines short.
- **Output packaging:** the guide tells ChatGPT to generate a post's slides in
  order, name them `01.png…`, and return a single downloadable `.zip` named
  `<post-id>.zip` of the separate PNGs — one zip per post, then reply `done`.

## Number-promise integrity (the completion-rate rule)
If the cover promises a number — "7 foods…", "5 reasons…", "6 drinks…" — the deck
delivers **exactly that many value slides**. A "7 foods" post that shows 4 foods
breaks the promise, tanks swipe-through completion (the primary ranking signal),
and earns "that was only 4??" comments that poison trust. Mechanics:
- Deck shape for N-item listicles: **cover + N fact slides + CTA** (drop the
  context slide if needed to stay ≤ 10 slides; the stakes line lives in the
  cover subtitle instead).
- Pick the promised number to fit the slide budget: 5–7 items ⇒ 7–9 slides. Never
  promise more than the deck holds.
- Validation: `title number == count of FACT slides` for every numbered post.

## The slide-type recipes

### A) Cover (educational hook, Buddy as small host)
```
Vertical 4:5 editorial poster, exactly 1080 x 1350 pixels (4:5 vertical), warm
cream (#FFF8F1) background. Big bold rounded headline reading exactly "[HEADLINE]"
in deep orange (#E9843A), with a smaller subtitle reading exactly "[SUB]" in
charcoal. [PASTE THE MASTER STYLE BLOCK for Buddy], posed as [a named pose].
Buddy sits SMALL in the lower third as a friendly host — he does not fill the
frame. Lots of negative space, subtle peach accents. No app screenshots, no
watermark, no drawn effects around Buddy.
```

### B) Educational food-fact slide (the workhorse body slide)
```
Vertical 4:5, exactly 1080 x 1350 pixels (4:5 vertical), warm cream (#FFF8F1)
background. Realistic, appetizing food photography of [FOOD], filling the top
~60% of the frame, natural soft light, no text baked into the food. Below the
photo, a bold rounded headline reading exactly "[FACT]" in deep orange (#E9843A)
on cream. No mascot, no app UI, no watermark. Clean editorial nutrition-post look.
```

### C) Educational text/tip slide (behavior tips, "the fix", story beats)
```
Vertical 4:5, exactly 1080 x 1350 pixels (4:5 vertical), warm cream (#FFF8F1)
background. A clean typographic slide: big bold rounded headline centered reading
exactly "[HEADLINE]" in deep orange (#E9843A)[, with smaller text reading exactly
"[SUB]" in charcoal]. Generous negative space, subtle peach/sage corner accents.
No mascot, no app UI, no watermark.
```

### D) Guess-the-calories question / answer (F2)
Question (no number — force the swipe):
```
Vertical 4:5, exactly 1080 x 1350 pixels (4:5 vertical), cream (#FFF8F1). A large
realistic appetizing photograph of [FOOD] filling the top ~70%, NO calorie number
shown. Bold headline below reading exactly "[QUESTION]" in deep orange. No mascot,
no app UI.
```
Answer (reveal + small Buddy reaction):
```
Vertical 4:5, exactly 1080 x 1350 pixels (4:5 vertical), cream (#FFF8F1). The same
[FOOD] in the top ~55%. Below it a very large bold number reading exactly "[≈ NNN
cal]" in deep orange, and a line reading exactly "[NOTE]" in charcoal. [MASTER
STYLE BLOCK], posed as [reacting pose] — Buddy SMALL in a bottom corner, not
filling the frame. No app UI.
```

### E) The CTA slide (identical shape on EVERY post — the only app slide)
```
Vertical 4:5, exactly 1080 x 1350 pixels (4:5 vertical), warm cream (#FFF8F1)
background. THIS IS THE ONLY SLIDE THAT SHOWS THE APP. Centered: a clean iPhone
silhouette containing the uploaded screenshot today-home-hero.png (the BiteBuddy
"Today" home screen) placed exactly as-is — do NOT redraw, recolor, or invent any
UI. [MASTER STYLE BLOCK], posed as buddy_goal_celebration, standing beside the
phone, small-to-medium, celebrating. Top headline reading exactly "[TOPIC CTA]" in
deep orange (#E9843A). Below the phone, bold text reading exactly "Download
BiteBuddy — free on the App Store", and a smaller line reading exactly "Search
'BiteBuddy: Ai calorie scanner'". Peach accents. No other text, no watermark.
```
The search line is **exactly** `Search 'BiteBuddy: Ai calorie scanner'` — never
shorten it to `BiteBuddy` (see the App Store search term in BiteBuddyMVP `APP_STORE_METADATA.md`, which
overrides anything older).
The `[TOPIC CTA]` varies per post and ties to its subject ("Know the protein in
any meal", "See your real number", "Skip the label math"). `today-home-hero.png`
is the one screenshot Connor uploads for the whole week (from `assets/`).

## Caption formula (per post)
`[educational hook restated in 1 line] + [1 search keyword phrase] + [1
comment-farming question OR a save prompt]`. Keep it value-first — the caption
should read like useful content, not an ad. ≤ 2 lines.

**Keyword rule (non-negotiable):** every caption works in ONE natural search
phrase — rotate between `AI calorie counter`, `calorie tracker app`,
`calorie scanner app`, `food tracker app`. TikTok/IG index carousels in search;
a keyworded caption keeps pulling installs for months. Weave it in naturally
("caught these with an AI calorie counter"), never as a keyword dump.

**Save prompt:** on reference-value posts (lists, label guides, calorie tables),
end with a save nudge ("save this for your next grocery run") — saves are the
highest-install-intent signal the algorithm reads. Use on ~half the week, not all.
Example:
> "5 ways to actually know what's in your food — no calorie-memorizing required.
> which one do you already do? (the last one is our AI calorie counter trick)"

## Hashtag pools (pick 3–5, rotate; lean nutrition/education)
- **Big:** `#caloriedeficit` `#weightlosstok` `#caloriecounting` `#whatieatinaday`
- **Mid:** `#nutritiontips` `#macrotracking` `#foodtracker` `#highprotein`
  `#healthyswaps`
- **Niche / brand:** `#bitebuddy` `#aicaloriecounter` `#caloriescanner`
Always include `#bitebuddy`. Don't reuse the exact same set two posts in a row.

## Pinned first comment
One playful, value-adding line that invites a reply ("#3 changed how I plate
everything", "comment your guess for the smoothie 👀"). Lifts comments.

## TikTok sound
Left as `SET_AT_POST_TIME` in the manifest — the trending sound is chosen when the
post publishes (it changes daily), not at generation time.
