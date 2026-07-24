# ChatGPT Image Generation Guide — Week 2026-W30

Hand this whole file to ChatGPT (a model with image generation **and** GitHub write
access) to generate every slide image for the week **and commit it straight into the
repo**. There are **21 posts**; each has its own set of slides.

## Before you start
1. Upload the one screenshot in this week's `assets/` folder: **`today-home-hero.png`**
   (the BiteBuddy "Today" home screen). Use it ONLY for the final "Download" slide of
   every post — drop it into the phone silhouette exactly as-is. Never redraw or invent app UI.
2. Make sure you can write to GitHub (see "Uploading to GitHub" below).

## Global rules for EVERY image
- **Size: exactly 1080 x 1350 pixels (4:5 vertical). Every image, no exceptions.**
- Background: warm cream `#FFF8F1` unless a prompt says otherwise.
- Render each headline EXACTLY as quoted — correct spelling, no extra text.
- Palette: cream `#FFF8F1` · peach `#F4A261` · deep orange `#E9843A` · sage `#8FA27F` · lavender `#C9C4F2`.
- Body slides EDUCATE (food photography or clean type). **App UI shows up on the last slide only.**
- No watermarks and no drawn effects (glow/sparkles/confetti) around Buddy.

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


## Uploading to GitHub (this is the whole point — no manual downloads)
Commit each finished PNG directly into its post's `slides/` folder in the repo.

- **Repo:** `clarson2706/BiteBuddyMVP`  ·  **Branch:** `main`
- **Path for post `<post-id>` slide `NN`:** `Posts/2026-W30/<post-id>/slides/NN.png`
- **Write access — one of:**
  - the **GitHub connector / a Custom GPT Action** scoped to this repo with *Contents: read & write*, or
  - a **fine-grained Personal Access Token** (repo `clarson2706/BiteBuddyMVP`, *Contents: Read and write*)
    that I paste into the chat when you ask for it.
  - **SECURITY:** never write the token into a file, a commit, a prompt you echo back, or memory.
    Use it only for these API calls, only in this session.

Upload each PNG with the GitHub Contents API (use your code tool in a loop):
```
PUT https://api.github.com/repos/clarson2706/BiteBuddyMVP/contents/Posts/2026-W30/<post-id>/slides/NN.png
Headers: Authorization: Bearer <TOKEN>   Accept: application/vnd.github+json
Body:    { "message": "Add <post-id> slide NN", "content": "<base64 of the PNG>", "branch": "main" }
```
If a file already exists at that path (e.g. a `.gitkeep` or a re-run), first GET the same
URL to read its `sha` and include `"sha"` in the PUT to overwrite. Example (Python):
```python
import base64, requests
OWNER, REPO, BRANCH = "clarson2706", "BiteBuddyMVP", "main"
def upload(path, png_bytes, msg, token):
    url = f"https://api.github.com/repos/{OWNER}/{REPO}/contents/{path}"
    h = {"Authorization": f"Bearer {token}", "Accept": "application/vnd.github+json"}
    sha = requests.get(url, headers=h, params={"ref": BRANCH}).json().get("sha")
    body = {"message": msg, "content": base64.b64encode(png_bytes).decode(), "branch": BRANCH}
    if sha: body["sha"] = sha
    r = requests.put(url, headers=h, json=body); r.raise_for_status(); return r.json()
```
Keep exports reasonably small (a 1080×1350 PNG is a few hundred KB). If a file exceeds the
Contents API limit, fall back to the Git Data API (create blob → tree → commit).

## How to work through the week — ONE POST AT A TIME, in order (Post 01 → Post 21)
For each post below:
1. Read that post's slide list.
2. Generate each slide in order at exactly 1080 x 1350 pixels (4:5 vertical), named `01.png, 02.png, …` in slide order.
3. **Upload each PNG to `Posts/2026-W30/<post-id>/slides/NN.png`** (see above) and
   confirm each commit returned HTTP 200/201.
4. Report "post <post-id>: N slides committed", then move on to the next post.

Do **not** batch everything into one commit dump — keep each post's files in its own folder.
If GitHub write isn't available, fall back to returning one `<post-id>.zip` per post instead.
When all 21 posts are generated and committed, reply with exactly: **done**

---

### Post 01 of 21 — `2026-07-20-slot1` — "7 foods sabotaging your protein goal" (F1-buddys-list, 7 slides)


**Upload target:** commit each finished PNG into `Posts/2026-W30/2026-07-20-slot1/slides/` on branch `main`
of `clarson2706/BiteBuddyMVP`, named `01.png` … `07.png` (one image per slide, in order).
See the week's `CHATGPT-GENERATION-GUIDE.md` → "Uploading to GitHub" for the exact API call.
**Every image size:** exactly 1080 x 1350 pixels (4:5 vertical). No exceptions.
**Text:** render each headline EXACTLY as quoted — correct spelling, no extra words.
**Palette:** cream #FFF8F1 · peach #F4A261 · deep orange #E9843A · sage #8FA27F · lavender #C9C4F2.
**App UI appears on the FINAL slide only** — place the uploaded `today-home-hero.png` in the phone
silhouette exactly as-is. Every other slide is educational: food photography or clean type, no app UI.

Generate the slides in order, upload `01.png…` to `Posts/2026-W30/2026-07-20-slot1/slides/`, confirm each commit, then move on.
(Fallback if GitHub write isn't set up: return a `2026-07-20-slot1.zip` of the PNGs instead.)

## Slide 01 — COVER
On-slide text: "7 foods sabotaging your protein goal"

Vertical 4:5 editorial poster, exactly 1080 x 1350 pixels (4:5 vertical), warm cream (#FFF8F1) background. Big bold rounded headline across the top reading exactly "7 foods sabotaging your protein goal" in deep orange (#E9843A). A smaller subtitle just below reading exactly "Hitting your calories but not your protein? These sneak past you." in soft charcoal. A cute chubby round fuzzy monster mascot named BiteBuddy, soft 3D character render, Pixar-like, wholesome and friendly. Soft lavender / periwinkle purple fuzzy fur with subtle subsurface scattering. Two small smooth beige curved horns on top of the head. Large round glossy black eyes with bright white highlights. Small friendly mouth with two tiny lower fangs. Wearing an oversized cream knit hoodie with drawstrings and a front pocket. Short stubby legs with little clawed feet and small rounded paws. Soft studio lighting from the upper left. Posed as: curious, one eyebrow raised, holding a small magnifying glass to one eye. Buddy sits SMALL in the lower third as a friendly host — he does not fill the frame. Lots of negative space, subtle peach (#F4A261) accent shapes. No app screenshots, no watermark, no drawn effects around Buddy.

## Slide 02 — CONTEXT
On-slide text: "Hitting your calories but not your protein? These sneak past you."

Vertical 4:5, exactly 1080 x 1350 pixels (4:5 vertical), warm cream (#FFF8F1) background. A clean typographic slide: a big bold rounded headline centered reading exactly "Hitting your calories but not your protein? These sneak past you." in deep orange (#E9843A). Generous negative space, subtle peach (#F4A261) and sage (#8FA27F) accent shapes in the corners. No mascot, no app UI, no watermark.

## Slide 03 — FACT 1
On-slide text: "Flavored yogurt — often ~4g protein, ~20g sugar"

Vertical 4:5, exactly 1080 x 1350 pixels (4:5 vertical), warm cream (#FFF8F1) background. Realistic, appetizing food photography of a cup of fruit-flavored yogurt with a spoon, filling the top ~60% of the frame, natural soft light, no text baked into the food. Below the photo, a bold rounded headline reading exactly "Flavored yogurt — often ~4g protein, ~20g sugar" in deep orange (#E9843A) on cream. No mascot, no app UI, no watermark. Clean editorial nutrition-post look.

## Slide 04 — FACT 2
On-slide text: "Veggie burgers — many have under 10g protein"

Vertical 4:5, exactly 1080 x 1350 pixels (4:5 vertical), warm cream (#FFF8F1) background. Realistic, appetizing food photography of a veggie burger patty on a bun with lettuce, filling the top ~60% of the frame, natural soft light, no text baked into the food. Below the photo, a bold rounded headline reading exactly "Veggie burgers — many have under 10g protein" in deep orange (#E9843A) on cream. No mascot, no app UI, no watermark. Clean editorial nutrition-post look.

## Slide 05 — FACT 3
On-slide text: "The wrong bars — barely more protein than candy"

Vertical 4:5, exactly 1080 x 1350 pixels (4:5 vertical), warm cream (#FFF8F1) background. Realistic, appetizing food photography of two granola/protein bars, one unwrapped, filling the top ~60% of the frame, natural soft light, no text baked into the food. Below the photo, a bold rounded headline reading exactly "The wrong bars — barely more protein than candy" in deep orange (#E9843A) on cream. No mascot, no app UI, no watermark. Clean editorial nutrition-post look.

## Slide 06 — FACT 4
On-slide text: "Smoothie bowls — fruit-heavy, protein's an afterthought"

Vertical 4:5, exactly 1080 x 1350 pixels (4:5 vertical), warm cream (#FFF8F1) background. Realistic, appetizing food photography of a fruit smoothie bowl topped with granola and berries, filling the top ~60% of the frame, natural soft light, no text baked into the food. Below the photo, a bold rounded headline reading exactly "Smoothie bowls — fruit-heavy, protein's an afterthought" in deep orange (#E9843A) on cream. No mascot, no app UI, no watermark. Clean editorial nutrition-post look.

## Slide 07 — CTA — DOWNLOAD (only app slide)
On-slide text: "Know the protein in any meal · Download BiteBuddy — free on the App Store"

Vertical 4:5, exactly 1080 x 1350 pixels (4:5 vertical), warm cream (#FFF8F1) background. THIS IS THE ONLY SLIDE THAT SHOWS THE APP. Centered: a clean, simple iPhone silhouette / phone frame containing the uploaded screenshot today-home-hero.png (the BiteBuddy 'Today' home screen) placed exactly as-is — do NOT redraw, recolor, crop out, or invent any UI. A cute chubby round fuzzy monster mascot named BiteBuddy, soft 3D character render, Pixar-like, wholesome and friendly. Soft lavender / periwinkle purple fuzzy fur with subtle subsurface scattering. Two small smooth beige curved horns on top of the head. Large round glossy black eyes with bright white highlights. Small friendly mouth with two tiny lower fangs. Wearing an oversized cream knit hoodie with drawstrings and a front pocket. Short stubby legs with little clawed feet and small rounded paws. Soft studio lighting from the upper left. Posed as: joyful mid-jump, both arms thrown up, huge happy smile, starry eyes. Buddy stands beside the phone, small-to-medium, celebrating. A top headline reading exactly "Know the protein in any meal" in deep orange (#E9843A). Below the phone, bold text reading exactly "Download BiteBuddy — free on the App Store", and a smaller line reading exactly "Search 'BiteBuddy: Ai calorie scanner'". Peach (#F4A261) accents. No other text, no watermark.

---

### Post 02 of 21 — `2026-07-20-slot2` — "Guess the calories: fast-food edition" (F2-guess-the-calories, 8 slides)


**Upload target:** commit each finished PNG into `Posts/2026-W30/2026-07-20-slot2/slides/` on branch `main`
of `clarson2706/BiteBuddyMVP`, named `01.png` … `08.png` (one image per slide, in order).
See the week's `CHATGPT-GENERATION-GUIDE.md` → "Uploading to GitHub" for the exact API call.
**Every image size:** exactly 1080 x 1350 pixels (4:5 vertical). No exceptions.
**Text:** render each headline EXACTLY as quoted — correct spelling, no extra words.
**Palette:** cream #FFF8F1 · peach #F4A261 · deep orange #E9843A · sage #8FA27F · lavender #C9C4F2.
**App UI appears on the FINAL slide only** — place the uploaded `today-home-hero.png` in the phone
silhouette exactly as-is. Every other slide is educational: food photography or clean type, no app UI.

Generate the slides in order, upload `01.png…` to `Posts/2026-W30/2026-07-20-slot2/slides/`, confirm each commit, then move on.
(Fallback if GitHub write isn't set up: return a `2026-07-20-slot2.zip` of the PNGs instead.)

## Slide 01 — COVER
On-slide text: "Guess the calories: fast-food edition"

Vertical 4:5 editorial poster, exactly 1080 x 1350 pixels (4:5 vertical), warm cream (#FFF8F1) background. Big bold rounded headline across the top reading exactly "Guess the calories: fast-food edition" in deep orange (#E9843A). A smaller subtitle just below reading exactly "Most people are way off. Keep score as you swipe." in soft charcoal. A cute chubby round fuzzy monster mascot named BiteBuddy, soft 3D character render, Pixar-like, wholesome and friendly. Soft lavender / periwinkle purple fuzzy fur with subtle subsurface scattering. Two small smooth beige curved horns on top of the head. Large round glossy black eyes with bright white highlights. Small friendly mouth with two tiny lower fangs. Wearing an oversized cream knit hoodie with drawstrings and a front pocket. Short stubby legs with little clawed feet and small rounded paws. Soft studio lighting from the upper left. Posed as: thoughtful, one paw on chin, head tilted up, small 'hmm' expression. Buddy sits SMALL in the lower third as a friendly host — he does not fill the frame. Lots of negative space, subtle peach (#F4A261) accent shapes. No app screenshots, no watermark, no drawn effects around Buddy.

## Slide 02 — Q1
On-slide text: "How many calories? 🍔"

Vertical 4:5, exactly 1080 x 1350 pixels (4:5 vertical), warm cream (#FFF8F1) background. A large realistic, appetizing food photograph of a loaded fast-food double burger with sauce filling the top ~70% of the frame — do NOT show any calorie number. A bold headline below reading exactly "How many calories? 🍔" in deep orange (#E9843A). No mascot, no app UI. Make the viewer want to guess.

## Slide 03 — A1
On-slide text: "≈ 1,100 cal — oof"

Vertical 4:5, exactly 1080 x 1350 pixels (4:5 vertical), warm cream (#FFF8F1) background. The same a loaded fast-food double burger with sauce, photographed appetizingly in the top ~55% of the frame. Below it, a very large bold number reading exactly "≈ 1,100 cal" in deep orange (#E9843A), and a line reading exactly "oof" in charcoal. A cute chubby round fuzzy monster mascot named BiteBuddy, soft 3D character render, Pixar-like, wholesome and friendly. Soft lavender / periwinkle purple fuzzy fur with subtle subsurface scattering. Two small smooth beige curved horns on top of the head. Large round glossy black eyes with bright white highlights. Small friendly mouth with two tiny lower fangs. Wearing an oversized cream knit hoodie with drawstrings and a front pocket. Short stubby legs with little clawed feet and small rounded paws. Soft studio lighting from the upper left. Posed as: full and satisfied, leaning back, paw on a rounder belly, cozy sleepy smile. Buddy is SMALL in a bottom corner reacting — not filling the frame. No app UI, no watermark.

## Slide 04 — Q2
On-slide text: "This 'healthy' wrap? 🌯"

Vertical 4:5, exactly 1080 x 1350 pixels (4:5 vertical), warm cream (#FFF8F1) background. A large realistic, appetizing food photograph of a chicken caesar wrap sliced in half on a tray filling the top ~70% of the frame — do NOT show any calorie number. A bold headline below reading exactly "This 'healthy' wrap? 🌯" in deep orange (#E9843A). No mascot, no app UI. Make the viewer want to guess.

## Slide 05 — A2
On-slide text: "≈ 950 cal — the dressing did that"

Vertical 4:5, exactly 1080 x 1350 pixels (4:5 vertical), warm cream (#FFF8F1) background. The same a chicken caesar wrap sliced in half on a tray, photographed appetizingly in the top ~55% of the frame. Below it, a very large bold number reading exactly "≈ 950 cal" in deep orange (#E9843A), and a line reading exactly "the dressing did that" in charcoal. A cute chubby round fuzzy monster mascot named BiteBuddy, soft 3D character render, Pixar-like, wholesome and friendly. Soft lavender / periwinkle purple fuzzy fur with subtle subsurface scattering. Two small smooth beige curved horns on top of the head. Large round glossy black eyes with bright white highlights. Small friendly mouth with two tiny lower fangs. Wearing an oversized cream knit hoodie with drawstrings and a front pocket. Short stubby legs with little clawed feet and small rounded paws. Soft studio lighting from the upper left. Posed as: squinting, one paw waving something away, mildly bothered but friendly. Buddy is SMALL in a bottom corner reacting — not filling the frame. No app UI, no watermark.

## Slide 06 — Q3
On-slide text: "Looks light… 🥣"

Vertical 4:5, exactly 1080 x 1350 pixels (4:5 vertical), warm cream (#FFF8F1) background. A large realistic, appetizing food photograph of a colorful smoothie bowl with granola and fruit filling the top ~70% of the frame — do NOT show any calorie number. A bold headline below reading exactly "Looks light… 🥣" in deep orange (#E9843A). No mascot, no app UI. Make the viewer want to guess.

## Slide 07 — A3
On-slide text: "≈ 700 cal — sugar in a trench coat"

Vertical 4:5, exactly 1080 x 1350 pixels (4:5 vertical), warm cream (#FFF8F1) background. The same a colorful smoothie bowl with granola and fruit, photographed appetizingly in the top ~55% of the frame. Below it, a very large bold number reading exactly "≈ 700 cal" in deep orange (#E9843A), and a line reading exactly "sugar in a trench coat" in charcoal. A cute chubby round fuzzy monster mascot named BiteBuddy, soft 3D character render, Pixar-like, wholesome and friendly. Soft lavender / periwinkle purple fuzzy fur with subtle subsurface scattering. Two small smooth beige curved horns on top of the head. Large round glossy black eyes with bright white highlights. Small friendly mouth with two tiny lower fangs. Wearing an oversized cream knit hoodie with drawstrings and a front pocket. Short stubby legs with little clawed feet and small rounded paws. Soft studio lighting from the upper left. Posed as: over-excited and jittery, wide sparkling eyes, arms flung up. Buddy is SMALL in a bottom corner reacting — not filling the frame. No app UI, no watermark.

## Slide 08 — CTA — DOWNLOAD (only app slide)
On-slide text: "Stop guessing — know any meal in one photo · Download BiteBuddy — free on the App Store"

Vertical 4:5, exactly 1080 x 1350 pixels (4:5 vertical), warm cream (#FFF8F1) background. THIS IS THE ONLY SLIDE THAT SHOWS THE APP. Centered: a clean, simple iPhone silhouette / phone frame containing the uploaded screenshot today-home-hero.png (the BiteBuddy 'Today' home screen) placed exactly as-is — do NOT redraw, recolor, crop out, or invent any UI. A cute chubby round fuzzy monster mascot named BiteBuddy, soft 3D character render, Pixar-like, wholesome and friendly. Soft lavender / periwinkle purple fuzzy fur with subtle subsurface scattering. Two small smooth beige curved horns on top of the head. Large round glossy black eyes with bright white highlights. Small friendly mouth with two tiny lower fangs. Wearing an oversized cream knit hoodie with drawstrings and a front pocket. Short stubby legs with little clawed feet and small rounded paws. Soft studio lighting from the upper left. Posed as: joyful mid-jump, both arms thrown up, huge happy smile, starry eyes. Buddy stands beside the phone, small-to-medium, celebrating. A top headline reading exactly "Stop guessing — know any meal in one photo" in deep orange (#E9843A). Below the phone, bold text reading exactly "Download BiteBuddy — free on the App Store", and a smaller line reading exactly "Search 'BiteBuddy: Ai calorie scanner'". Peach (#F4A261) accents. No other text, no watermark.

---

### Post 03 of 21 — `2026-07-20-slot3` — "I quit calorie tracking 4 times" (F3-i-was-wrong, 6 slides)


**Upload target:** commit each finished PNG into `Posts/2026-W30/2026-07-20-slot3/slides/` on branch `main`
of `clarson2706/BiteBuddyMVP`, named `01.png` … `06.png` (one image per slide, in order).
See the week's `CHATGPT-GENERATION-GUIDE.md` → "Uploading to GitHub" for the exact API call.
**Every image size:** exactly 1080 x 1350 pixels (4:5 vertical). No exceptions.
**Text:** render each headline EXACTLY as quoted — correct spelling, no extra words.
**Palette:** cream #FFF8F1 · peach #F4A261 · deep orange #E9843A · sage #8FA27F · lavender #C9C4F2.
**App UI appears on the FINAL slide only** — place the uploaded `today-home-hero.png` in the phone
silhouette exactly as-is. Every other slide is educational: food photography or clean type, no app UI.

Generate the slides in order, upload `01.png…` to `Posts/2026-W30/2026-07-20-slot3/slides/`, confirm each commit, then move on.
(Fallback if GitHub write isn't set up: return a `2026-07-20-slot3.zip` of the PNGs instead.)

## Slide 01 — COVER
On-slide text: "I quit calorie tracking 4 times · …then something dumb finally worked."

Vertical 4:5 editorial poster, exactly 1080 x 1350 pixels (4:5 vertical), warm cream (#FFF8F1) background. Big bold rounded headline across the top reading exactly "I quit calorie tracking 4 times" in deep orange (#E9843A). A smaller subtitle just below reading exactly "…then something dumb finally worked." in soft charcoal. A cute chubby round fuzzy monster mascot named BiteBuddy, soft 3D character render, Pixar-like, wholesome and friendly. Soft lavender / periwinkle purple fuzzy fur with subtle subsurface scattering. Two small smooth beige curved horns on top of the head. Large round glossy black eyes with bright white highlights. Small friendly mouth with two tiny lower fangs. Wearing an oversized cream knit hoodie with drawstrings and a front pocket. Short stubby legs with little clawed feet and small rounded paws. Soft studio lighting from the upper left. Posed as: sleepy and slumped, droopy tired eyes, one paw rubbing an eye, drained. Buddy sits SMALL in the lower third as a friendly host — he does not fill the frame. Lots of negative space, subtle peach (#F4A261) accent shapes. No app screenshots, no watermark, no drawn effects around Buddy.

## Slide 02 — PAIN
On-slide text: "Typing every meal into a search bar is why I always quit."

Vertical 4:5, exactly 1080 x 1350 pixels (4:5 vertical), warm cream (#FFF8F1) background. A clean typographic slide: a big bold rounded headline centered reading exactly "Typing every meal into a search bar is why I always quit." in deep orange (#E9843A). Generous negative space, subtle peach (#F4A261) and sage (#8FA27F) accent shapes in the corners. No mascot, no app UI, no watermark.

## Slide 03 — INSIGHT
On-slide text: "Tracking only sticks when it's easier than not tracking."

Vertical 4:5, exactly 1080 x 1350 pixels (4:5 vertical), warm cream (#FFF8F1) background. A clean typographic slide: a big bold rounded headline centered reading exactly "Tracking only sticks when it's easier than not tracking." in deep orange (#E9843A). Generous negative space, subtle peach (#F4A261) and sage (#8FA27F) accent shapes in the corners. No mascot, no app UI, no watermark.

## Slide 04 — SHIFT
On-slide text: "So I stopped typing and just started photographing my food."

Vertical 4:5, exactly 1080 x 1350 pixels (4:5 vertical), warm cream (#FFF8F1) background. A clean typographic slide: a big bold rounded headline centered reading exactly "So I stopped typing and just started photographing my food." in deep orange (#E9843A). Generous negative space, subtle peach (#F4A261) and sage (#8FA27F) accent shapes in the corners. No mascot, no app UI, no watermark.

## Slide 05 — PAYOFF
On-slide text: "30 days straight — the first time it ever became a habit."

Vertical 4:5, exactly 1080 x 1350 pixels (4:5 vertical), warm cream (#FFF8F1) background. A clean typographic slide: a big bold rounded headline centered reading exactly "30 days straight — the first time it ever became a habit." in deep orange (#E9843A). Generous negative space, subtle peach (#F4A261) and sage (#8FA27F) accent shapes in the corners. No mascot, no app UI, no watermark.

## Slide 06 — CTA — DOWNLOAD (only app slide)
On-slide text: "The tracker that finally sticks · Download BiteBuddy — free on the App Store"

Vertical 4:5, exactly 1080 x 1350 pixels (4:5 vertical), warm cream (#FFF8F1) background. THIS IS THE ONLY SLIDE THAT SHOWS THE APP. Centered: a clean, simple iPhone silhouette / phone frame containing the uploaded screenshot today-home-hero.png (the BiteBuddy 'Today' home screen) placed exactly as-is — do NOT redraw, recolor, crop out, or invent any UI. A cute chubby round fuzzy monster mascot named BiteBuddy, soft 3D character render, Pixar-like, wholesome and friendly. Soft lavender / periwinkle purple fuzzy fur with subtle subsurface scattering. Two small smooth beige curved horns on top of the head. Large round glossy black eyes with bright white highlights. Small friendly mouth with two tiny lower fangs. Wearing an oversized cream knit hoodie with drawstrings and a front pocket. Short stubby legs with little clawed feet and small rounded paws. Soft studio lighting from the upper left. Posed as: joyful mid-jump, both arms thrown up, huge happy smile, starry eyes. Buddy stands beside the phone, small-to-medium, celebrating. A top headline reading exactly "The tracker that finally sticks" in deep orange (#E9843A). Below the phone, bold text reading exactly "Download BiteBuddy — free on the App Store", and a smaller line reading exactly "Search 'BiteBuddy: Ai calorie scanner'". Peach (#F4A261) accents. No other text, no watermark.

---

### Post 04 of 21 — `2026-07-21-slot1` — "Why you keep quitting food tracking" (F4-one-snap-demo, 6 slides)


**Upload target:** commit each finished PNG into `Posts/2026-W30/2026-07-21-slot1/slides/` on branch `main`
of `clarson2706/BiteBuddyMVP`, named `01.png` … `06.png` (one image per slide, in order).
See the week's `CHATGPT-GENERATION-GUIDE.md` → "Uploading to GitHub" for the exact API call.
**Every image size:** exactly 1080 x 1350 pixels (4:5 vertical). No exceptions.
**Text:** render each headline EXACTLY as quoted — correct spelling, no extra words.
**Palette:** cream #FFF8F1 · peach #F4A261 · deep orange #E9843A · sage #8FA27F · lavender #C9C4F2.
**App UI appears on the FINAL slide only** — place the uploaded `today-home-hero.png` in the phone
silhouette exactly as-is. Every other slide is educational: food photography or clean type, no app UI.

Generate the slides in order, upload `01.png…` to `Posts/2026-W30/2026-07-21-slot1/slides/`, confirm each commit, then move on.
(Fallback if GitHub write isn't set up: return a `2026-07-21-slot1.zip` of the PNGs instead.)

## Slide 01 — COVER
On-slide text: "Why you keep quitting food tracking"

Vertical 4:5 editorial poster, exactly 1080 x 1350 pixels (4:5 vertical), warm cream (#FFF8F1) background. Big bold rounded headline across the top reading exactly "Why you keep quitting food tracking" in deep orange (#E9843A). A smaller subtitle just below reading exactly "It's almost never willpower. It's these three things — and the fix." in soft charcoal. A cute chubby round fuzzy monster mascot named BiteBuddy, soft 3D character render, Pixar-like, wholesome and friendly. Soft lavender / periwinkle purple fuzzy fur with subtle subsurface scattering. Two small smooth beige curved horns on top of the head. Large round glossy black eyes with bright white highlights. Small friendly mouth with two tiny lower fangs. Wearing an oversized cream knit hoodie with drawstrings and a front pocket. Short stubby legs with little clawed feet and small rounded paws. Soft studio lighting from the upper left. Posed as: curious, one eyebrow raised, holding a small magnifying glass to one eye. Buddy sits SMALL in the lower third as a friendly host — he does not fill the frame. Lots of negative space, subtle peach (#F4A261) accent shapes. No app screenshots, no watermark, no drawn effects around Buddy.

## Slide 02 — TIP 1
On-slide text: "1. It takes too long"

Vertical 4:5, exactly 1080 x 1350 pixels (4:5 vertical), warm cream (#FFF8F1) background. A clean typographic slide: a big bold rounded headline centered reading exactly "1. It takes too long" in deep orange (#E9843A). Below it, smaller text reading exactly "Ten taps for one homemade meal? You'll quit by Friday." in charcoal. Generous negative space, subtle peach (#F4A261) and sage (#8FA27F) accent shapes in the corners. No mascot, no app UI, no watermark.

## Slide 03 — TIP 2
On-slide text: "2. You forget in the moment"

Vertical 4:5, exactly 1080 x 1350 pixels (4:5 vertical), warm cream (#FFF8F1) background. A clean typographic slide: a big bold rounded headline centered reading exactly "2. You forget in the moment" in deep orange (#E9843A). Below it, smaller text reading exactly "If it's not fast, it doesn't happen." in charcoal. Generous negative space, subtle peach (#F4A261) and sage (#8FA27F) accent shapes in the corners. No mascot, no app UI, no watermark.

## Slide 04 — TIP 3
On-slide text: "3. Guessing feels pointless"

Vertical 4:5, exactly 1080 x 1350 pixels (4:5 vertical), warm cream (#FFF8F1) background. A clean typographic slide: a big bold rounded headline centered reading exactly "3. Guessing feels pointless" in deep orange (#E9843A). Below it, smaller text reading exactly "Vague numbers you don't trust are easy to ignore." in charcoal. Generous negative space, subtle peach (#F4A261) and sage (#8FA27F) accent shapes in the corners. No mascot, no app UI, no watermark.

## Slide 05 — TIP 4
On-slide text: "The fix: make it a 3-second photo"

Vertical 4:5, exactly 1080 x 1350 pixels (4:5 vertical), warm cream (#FFF8F1) background. A clean typographic slide: a big bold rounded headline centered reading exactly "The fix: make it a 3-second photo" in deep orange (#E9843A). Below it, smaller text reading exactly "Fast + specific is what turns it into a habit." in charcoal. Generous negative space, subtle peach (#F4A261) and sage (#8FA27F) accent shapes in the corners. No mascot, no app UI, no watermark.

## Slide 06 — CTA — DOWNLOAD (only app slide)
On-slide text: "Log any meal in about 3 seconds · Download BiteBuddy — free on the App Store"

Vertical 4:5, exactly 1080 x 1350 pixels (4:5 vertical), warm cream (#FFF8F1) background. THIS IS THE ONLY SLIDE THAT SHOWS THE APP. Centered: a clean, simple iPhone silhouette / phone frame containing the uploaded screenshot today-home-hero.png (the BiteBuddy 'Today' home screen) placed exactly as-is — do NOT redraw, recolor, crop out, or invent any UI. A cute chubby round fuzzy monster mascot named BiteBuddy, soft 3D character render, Pixar-like, wholesome and friendly. Soft lavender / periwinkle purple fuzzy fur with subtle subsurface scattering. Two small smooth beige curved horns on top of the head. Large round glossy black eyes with bright white highlights. Small friendly mouth with two tiny lower fangs. Wearing an oversized cream knit hoodie with drawstrings and a front pocket. Short stubby legs with little clawed feet and small rounded paws. Soft studio lighting from the upper left. Posed as: joyful mid-jump, both arms thrown up, huge happy smile, starry eyes. Buddy stands beside the phone, small-to-medium, celebrating. A top headline reading exactly "Log any meal in about 3 seconds" in deep orange (#E9843A). Below the phone, bold text reading exactly "Download BiteBuddy — free on the App Store", and a smaller line reading exactly "Search 'BiteBuddy: Ai calorie scanner'". Peach (#F4A261) accents. No other text, no watermark.

---

### Post 05 of 21 — `2026-07-21-slot2` — "5 reasons calorie tracking fails (and the fix)" (F1-buddys-list, 7 slides)


**Upload target:** commit each finished PNG into `Posts/2026-W30/2026-07-21-slot2/slides/` on branch `main`
of `clarson2706/BiteBuddyMVP`, named `01.png` … `07.png` (one image per slide, in order).
See the week's `CHATGPT-GENERATION-GUIDE.md` → "Uploading to GitHub" for the exact API call.
**Every image size:** exactly 1080 x 1350 pixels (4:5 vertical). No exceptions.
**Text:** render each headline EXACTLY as quoted — correct spelling, no extra words.
**Palette:** cream #FFF8F1 · peach #F4A261 · deep orange #E9843A · sage #8FA27F · lavender #C9C4F2.
**App UI appears on the FINAL slide only** — place the uploaded `today-home-hero.png` in the phone
silhouette exactly as-is. Every other slide is educational: food photography or clean type, no app UI.

Generate the slides in order, upload `01.png…` to `Posts/2026-W30/2026-07-21-slot2/slides/`, confirm each commit, then move on.
(Fallback if GitHub write isn't set up: return a `2026-07-21-slot2.zip` of the PNGs instead.)

## Slide 01 — COVER
On-slide text: "5 reasons calorie tracking fails (and the fix)"

Vertical 4:5 editorial poster, exactly 1080 x 1350 pixels (4:5 vertical), warm cream (#FFF8F1) background. Big bold rounded headline across the top reading exactly "5 reasons calorie tracking fails (and the fix)" in deep orange (#E9843A). A smaller subtitle just below reading exactly "Most people quit tracking by Thursday. Here's why — and what actually helps." in soft charcoal. A cute chubby round fuzzy monster mascot named BiteBuddy, soft 3D character render, Pixar-like, wholesome and friendly. Soft lavender / periwinkle purple fuzzy fur with subtle subsurface scattering. Two small smooth beige curved horns on top of the head. Large round glossy black eyes with bright white highlights. Small friendly mouth with two tiny lower fangs. Wearing an oversized cream knit hoodie with drawstrings and a front pocket. Short stubby legs with little clawed feet and small rounded paws. Soft studio lighting from the upper left. Posed as: curious, one eyebrow raised, holding a small magnifying glass to one eye. Buddy sits SMALL in the lower third as a friendly host — he does not fill the frame. Lots of negative space, subtle peach (#F4A261) accent shapes. No app screenshots, no watermark, no drawn effects around Buddy.

## Slide 02 — CONTEXT
On-slide text: "Most people quit tracking by Thursday. Here's why — and what actually helps."

Vertical 4:5, exactly 1080 x 1350 pixels (4:5 vertical), warm cream (#FFF8F1) background. A clean typographic slide: a big bold rounded headline centered reading exactly "Most people quit tracking by Thursday. Here's why — and what actually helps." in deep orange (#E9843A). Generous negative space, subtle peach (#F4A261) and sage (#8FA27F) accent shapes in the corners. No mascot, no app UI, no watermark.

## Slide 03 — FACT 1
On-slide text: "You log from memory at night"

Vertical 4:5, exactly 1080 x 1350 pixels (4:5 vertical), warm cream (#FFF8F1) background. A clean typographic slide: a big bold rounded headline centered reading exactly "You log from memory at night" in deep orange (#E9843A). Below it, smaller text reading exactly "Fix: capture it in the moment, not hours later" in charcoal. Generous negative space, subtle peach (#F4A261) and sage (#8FA27F) accent shapes in the corners. No mascot, no app UI, no watermark.

## Slide 04 — FACT 2
On-slide text: "You guess restaurant portions"

Vertical 4:5, exactly 1080 x 1350 pixels (4:5 vertical), warm cream (#FFF8F1) background. A clean typographic slide: a big bold rounded headline centered reading exactly "You guess restaurant portions" in deep orange (#E9843A). Below it, smaller text reading exactly "Fix: use an estimate you can adjust, not a wild guess" in charcoal. Generous negative space, subtle peach (#F4A261) and sage (#8FA27F) accent shapes in the corners. No mascot, no app UI, no watermark.

## Slide 05 — FACT 3
On-slide text: "One 'bad' day and you stop"

Vertical 4:5, exactly 1080 x 1350 pixels (4:5 vertical), warm cream (#FFF8F1) background. A clean typographic slide: a big bold rounded headline centered reading exactly "One 'bad' day and you stop" in deep orange (#E9843A). Below it, smaller text reading exactly "Fix: log the messy days too — that's the whole point" in charcoal. Generous negative space, subtle peach (#F4A261) and sage (#8FA27F) accent shapes in the corners. No mascot, no app UI, no watermark.

## Slide 06 — FACT 4
On-slide text: "It just takes too long"

Vertical 4:5, exactly 1080 x 1350 pixels (4:5 vertical), warm cream (#FFF8F1) background. A clean typographic slide: a big bold rounded headline centered reading exactly "It just takes too long" in deep orange (#E9843A). Below it, smaller text reading exactly "Fix: make logging faster than skipping it" in charcoal. Generous negative space, subtle peach (#F4A261) and sage (#8FA27F) accent shapes in the corners. No mascot, no app UI, no watermark.

## Slide 07 — CTA — DOWNLOAD (only app slide)
On-slide text: "Make tracking take 5 seconds, not 5 minutes · Download BiteBuddy — free on the App Store"

Vertical 4:5, exactly 1080 x 1350 pixels (4:5 vertical), warm cream (#FFF8F1) background. THIS IS THE ONLY SLIDE THAT SHOWS THE APP. Centered: a clean, simple iPhone silhouette / phone frame containing the uploaded screenshot today-home-hero.png (the BiteBuddy 'Today' home screen) placed exactly as-is — do NOT redraw, recolor, crop out, or invent any UI. A cute chubby round fuzzy monster mascot named BiteBuddy, soft 3D character render, Pixar-like, wholesome and friendly. Soft lavender / periwinkle purple fuzzy fur with subtle subsurface scattering. Two small smooth beige curved horns on top of the head. Large round glossy black eyes with bright white highlights. Small friendly mouth with two tiny lower fangs. Wearing an oversized cream knit hoodie with drawstrings and a front pocket. Short stubby legs with little clawed feet and small rounded paws. Soft studio lighting from the upper left. Posed as: joyful mid-jump, both arms thrown up, huge happy smile, starry eyes. Buddy stands beside the phone, small-to-medium, celebrating. A top headline reading exactly "Make tracking take 5 seconds, not 5 minutes" in deep orange (#E9843A). Below the phone, bold text reading exactly "Download BiteBuddy — free on the App Store", and a smaller line reading exactly "Search 'BiteBuddy: Ai calorie scanner'". Peach (#F4A261) accents. No other text, no watermark.

---

### Post 06 of 21 — `2026-07-21-slot3` — "Guess the calories: coffee shop edition ☕" (F2-guess-the-calories, 8 slides)


**Upload target:** commit each finished PNG into `Posts/2026-W30/2026-07-21-slot3/slides/` on branch `main`
of `clarson2706/BiteBuddyMVP`, named `01.png` … `08.png` (one image per slide, in order).
See the week's `CHATGPT-GENERATION-GUIDE.md` → "Uploading to GitHub" for the exact API call.
**Every image size:** exactly 1080 x 1350 pixels (4:5 vertical). No exceptions.
**Text:** render each headline EXACTLY as quoted — correct spelling, no extra words.
**Palette:** cream #FFF8F1 · peach #F4A261 · deep orange #E9843A · sage #8FA27F · lavender #C9C4F2.
**App UI appears on the FINAL slide only** — place the uploaded `today-home-hero.png` in the phone
silhouette exactly as-is. Every other slide is educational: food photography or clean type, no app UI.

Generate the slides in order, upload `01.png…` to `Posts/2026-W30/2026-07-21-slot3/slides/`, confirm each commit, then move on.
(Fallback if GitHub write isn't set up: return a `2026-07-21-slot3.zip` of the PNGs instead.)

## Slide 01 — COVER
On-slide text: "Guess the calories: coffee shop edition ☕"

Vertical 4:5 editorial poster, exactly 1080 x 1350 pixels (4:5 vertical), warm cream (#FFF8F1) background. Big bold rounded headline across the top reading exactly "Guess the calories: coffee shop edition ☕" in deep orange (#E9843A). A smaller subtitle just below reading exactly "Your morning order is sneakier than it looks. Keep score." in soft charcoal. A cute chubby round fuzzy monster mascot named BiteBuddy, soft 3D character render, Pixar-like, wholesome and friendly. Soft lavender / periwinkle purple fuzzy fur with subtle subsurface scattering. Two small smooth beige curved horns on top of the head. Large round glossy black eyes with bright white highlights. Small friendly mouth with two tiny lower fangs. Wearing an oversized cream knit hoodie with drawstrings and a front pocket. Short stubby legs with little clawed feet and small rounded paws. Soft studio lighting from the upper left. Posed as: thoughtful, one paw on chin, head tilted up, small 'hmm' expression. Buddy sits SMALL in the lower third as a friendly host — he does not fill the frame. Lots of negative space, subtle peach (#F4A261) accent shapes. No app screenshots, no watermark, no drawn effects around Buddy.

## Slide 02 — Q1
On-slide text: "Venti caramel frappuccino? 🥤"

Vertical 4:5, exactly 1080 x 1350 pixels (4:5 vertical), warm cream (#FFF8F1) background. A large realistic, appetizing food photograph of a venti caramel frappuccino with whipped cream filling the top ~70% of the frame — do NOT show any calorie number. A bold headline below reading exactly "Venti caramel frappuccino? 🥤" in deep orange (#E9843A). No mascot, no app UI. Make the viewer want to guess.

## Slide 03 — A1
On-slide text: "≈ 470 cal — basically dessert"

Vertical 4:5, exactly 1080 x 1350 pixels (4:5 vertical), warm cream (#FFF8F1) background. The same a venti caramel frappuccino with whipped cream, photographed appetizingly in the top ~55% of the frame. Below it, a very large bold number reading exactly "≈ 470 cal" in deep orange (#E9843A), and a line reading exactly "basically dessert" in charcoal. A cute chubby round fuzzy monster mascot named BiteBuddy, soft 3D character render, Pixar-like, wholesome and friendly. Soft lavender / periwinkle purple fuzzy fur with subtle subsurface scattering. Two small smooth beige curved horns on top of the head. Large round glossy black eyes with bright white highlights. Small friendly mouth with two tiny lower fangs. Wearing an oversized cream knit hoodie with drawstrings and a front pocket. Short stubby legs with little clawed feet and small rounded paws. Soft studio lighting from the upper left. Posed as: full and satisfied, leaning back, paw on a rounder belly, cozy sleepy smile. Buddy is SMALL in a bottom corner reacting — not filling the frame. No app UI, no watermark.

## Slide 04 — Q2
On-slide text: "Grande pumpkin spice latte? 🎃"

Vertical 4:5, exactly 1080 x 1350 pixels (4:5 vertical), warm cream (#FFF8F1) background. A large realistic, appetizing food photograph of a grande pumpkin spice latte with whipped cream and spice filling the top ~70% of the frame — do NOT show any calorie number. A bold headline below reading exactly "Grande pumpkin spice latte? 🎃" in deep orange (#E9843A). No mascot, no app UI. Make the viewer want to guess.

## Slide 05 — A2
On-slide text: "≈ 380 cal — more than a slice of cake"

Vertical 4:5, exactly 1080 x 1350 pixels (4:5 vertical), warm cream (#FFF8F1) background. The same a grande pumpkin spice latte with whipped cream and spice, photographed appetizingly in the top ~55% of the frame. Below it, a very large bold number reading exactly "≈ 380 cal" in deep orange (#E9843A), and a line reading exactly "more than a slice of cake" in charcoal. A cute chubby round fuzzy monster mascot named BiteBuddy, soft 3D character render, Pixar-like, wholesome and friendly. Soft lavender / periwinkle purple fuzzy fur with subtle subsurface scattering. Two small smooth beige curved horns on top of the head. Large round glossy black eyes with bright white highlights. Small friendly mouth with two tiny lower fangs. Wearing an oversized cream knit hoodie with drawstrings and a front pocket. Short stubby legs with little clawed feet and small rounded paws. Soft studio lighting from the upper left. Posed as: squinting, one paw waving something away, mildly bothered but friendly. Buddy is SMALL in a bottom corner reacting — not filling the frame. No app UI, no watermark.

## Slide 06 — Q3
On-slide text: "'Healthy' egg white wrap? 🌯"

Vertical 4:5, exactly 1080 x 1350 pixels (4:5 vertical), warm cream (#FFF8F1) background. A large realistic, appetizing food photograph of an egg white breakfast wrap on a coffee shop counter filling the top ~70% of the frame — do NOT show any calorie number. A bold headline below reading exactly "'Healthy' egg white wrap? 🌯" in deep orange (#E9843A). No mascot, no app UI. Make the viewer want to guess.

## Slide 07 — A3
On-slide text: "≈ 290 cal — the sauce adds 80 more"

Vertical 4:5, exactly 1080 x 1350 pixels (4:5 vertical), warm cream (#FFF8F1) background. The same an egg white breakfast wrap on a coffee shop counter, photographed appetizingly in the top ~55% of the frame. Below it, a very large bold number reading exactly "≈ 290 cal" in deep orange (#E9843A), and a line reading exactly "the sauce adds 80 more" in charcoal. A cute chubby round fuzzy monster mascot named BiteBuddy, soft 3D character render, Pixar-like, wholesome and friendly. Soft lavender / periwinkle purple fuzzy fur with subtle subsurface scattering. Two small smooth beige curved horns on top of the head. Large round glossy black eyes with bright white highlights. Small friendly mouth with two tiny lower fangs. Wearing an oversized cream knit hoodie with drawstrings and a front pocket. Short stubby legs with little clawed feet and small rounded paws. Soft studio lighting from the upper left. Posed as: over-excited and jittery, wide sparkling eyes, arms flung up. Buddy is SMALL in a bottom corner reacting — not filling the frame. No app UI, no watermark.

## Slide 08 — CTA — DOWNLOAD (only app slide)
On-slide text: "Know your order before you sip · Download BiteBuddy — free on the App Store"

Vertical 4:5, exactly 1080 x 1350 pixels (4:5 vertical), warm cream (#FFF8F1) background. THIS IS THE ONLY SLIDE THAT SHOWS THE APP. Centered: a clean, simple iPhone silhouette / phone frame containing the uploaded screenshot today-home-hero.png (the BiteBuddy 'Today' home screen) placed exactly as-is — do NOT redraw, recolor, crop out, or invent any UI. A cute chubby round fuzzy monster mascot named BiteBuddy, soft 3D character render, Pixar-like, wholesome and friendly. Soft lavender / periwinkle purple fuzzy fur with subtle subsurface scattering. Two small smooth beige curved horns on top of the head. Large round glossy black eyes with bright white highlights. Small friendly mouth with two tiny lower fangs. Wearing an oversized cream knit hoodie with drawstrings and a front pocket. Short stubby legs with little clawed feet and small rounded paws. Soft studio lighting from the upper left. Posed as: joyful mid-jump, both arms thrown up, huge happy smile, starry eyes. Buddy stands beside the phone, small-to-medium, celebrating. A top headline reading exactly "Know your order before you sip" in deep orange (#E9843A). Below the phone, bold text reading exactly "Download BiteBuddy — free on the App Store", and a smaller line reading exactly "Search 'BiteBuddy: Ai calorie scanner'". Peach (#F4A261) accents. No other text, no watermark.

---

### Post 07 of 21 — `2026-07-22-slot1` — "I thought I ate 1,500 calories" (F3-i-was-wrong, 6 slides)


**Upload target:** commit each finished PNG into `Posts/2026-W30/2026-07-22-slot1/slides/` on branch `main`
of `clarson2706/BiteBuddyMVP`, named `01.png` … `06.png` (one image per slide, in order).
See the week's `CHATGPT-GENERATION-GUIDE.md` → "Uploading to GitHub" for the exact API call.
**Every image size:** exactly 1080 x 1350 pixels (4:5 vertical). No exceptions.
**Text:** render each headline EXACTLY as quoted — correct spelling, no extra words.
**Palette:** cream #FFF8F1 · peach #F4A261 · deep orange #E9843A · sage #8FA27F · lavender #C9C4F2.
**App UI appears on the FINAL slide only** — place the uploaded `today-home-hero.png` in the phone
silhouette exactly as-is. Every other slide is educational: food photography or clean type, no app UI.

Generate the slides in order, upload `01.png…` to `Posts/2026-W30/2026-07-22-slot1/slides/`, confirm each commit, then move on.
(Fallback if GitHub write isn't set up: return a `2026-07-22-slot1.zip` of the PNGs instead.)

## Slide 01 — COVER
On-slide text: "I thought I ate 1,500 calories · It was actually 2,400."

Vertical 4:5 editorial poster, exactly 1080 x 1350 pixels (4:5 vertical), warm cream (#FFF8F1) background. Big bold rounded headline across the top reading exactly "I thought I ate 1,500 calories" in deep orange (#E9843A). A smaller subtitle just below reading exactly "It was actually 2,400." in soft charcoal. A cute chubby round fuzzy monster mascot named BiteBuddy, soft 3D character render, Pixar-like, wholesome and friendly. Soft lavender / periwinkle purple fuzzy fur with subtle subsurface scattering. Two small smooth beige curved horns on top of the head. Large round glossy black eyes with bright white highlights. Small friendly mouth with two tiny lower fangs. Wearing an oversized cream knit hoodie with drawstrings and a front pocket. Short stubby legs with little clawed feet and small rounded paws. Soft studio lighting from the upper left. Posed as: thoughtful, one paw on chin, head tilted up, small 'hmm' expression. Buddy sits SMALL in the lower third as a friendly host — he does not fill the frame. Lots of negative space, subtle peach (#F4A261) accent shapes. No app screenshots, no watermark, no drawn effects around Buddy.

## Slide 02 — PAIN
On-slide text: "The gap wasn't the meals — it was everything around them."

Vertical 4:5, exactly 1080 x 1350 pixels (4:5 vertical), warm cream (#FFF8F1) background. A clean typographic slide: a big bold rounded headline centered reading exactly "The gap wasn't the meals — it was everything around them." in deep orange (#E9843A). Generous negative space, subtle peach (#F4A261) and sage (#8FA27F) accent shapes in the corners. No mascot, no app UI, no watermark.

## Slide 03 — INSIGHT
On-slide text: "Oils, dressings and 'little bites' can hide 500-900 calories a day."

Vertical 4:5, exactly 1080 x 1350 pixels (4:5 vertical), warm cream (#FFF8F1) background. Realistic, appetizing food photography of a spoon drizzling olive oil over a salad, plus a small dish of dressing, filling the top ~60% of the frame, natural soft light, no text baked into the food. Below the photo, a bold rounded headline reading exactly "Oils, dressings and 'little bites' can hide 500-900 calories a day." in deep orange (#E9843A) on cream. No mascot, no app UI, no watermark. Clean editorial nutrition-post look.

## Slide 04 — SHIFT
On-slide text: "The fix isn't eating less. It's seeing what you actually eat."

Vertical 4:5, exactly 1080 x 1350 pixels (4:5 vertical), warm cream (#FFF8F1) background. A clean typographic slide: a big bold rounded headline centered reading exactly "The fix isn't eating less. It's seeing what you actually eat." in deep orange (#E9843A). Generous negative space, subtle peach (#F4A261) and sage (#8FA27F) accent shapes in the corners. No mascot, no app UI, no watermark.

## Slide 05 — PAYOFF
On-slide text: "Now I know my real number — and it's not scary."

Vertical 4:5, exactly 1080 x 1350 pixels (4:5 vertical), warm cream (#FFF8F1) background. A clean typographic slide: a big bold rounded headline centered reading exactly "Now I know my real number — and it's not scary." in deep orange (#E9843A). Generous negative space, subtle peach (#F4A261) and sage (#8FA27F) accent shapes in the corners. No mascot, no app UI, no watermark.

## Slide 06 — CTA — DOWNLOAD (only app slide)
On-slide text: "See your real number, no guessing · Download BiteBuddy — free on the App Store"

Vertical 4:5, exactly 1080 x 1350 pixels (4:5 vertical), warm cream (#FFF8F1) background. THIS IS THE ONLY SLIDE THAT SHOWS THE APP. Centered: a clean, simple iPhone silhouette / phone frame containing the uploaded screenshot today-home-hero.png (the BiteBuddy 'Today' home screen) placed exactly as-is — do NOT redraw, recolor, crop out, or invent any UI. A cute chubby round fuzzy monster mascot named BiteBuddy, soft 3D character render, Pixar-like, wholesome and friendly. Soft lavender / periwinkle purple fuzzy fur with subtle subsurface scattering. Two small smooth beige curved horns on top of the head. Large round glossy black eyes with bright white highlights. Small friendly mouth with two tiny lower fangs. Wearing an oversized cream knit hoodie with drawstrings and a front pocket. Short stubby legs with little clawed feet and small rounded paws. Soft studio lighting from the upper left. Posed as: joyful mid-jump, both arms thrown up, huge happy smile, starry eyes. Buddy stands beside the phone, small-to-medium, celebrating. A top headline reading exactly "See your real number, no guessing" in deep orange (#E9843A). Below the phone, bold text reading exactly "Download BiteBuddy — free on the App Store", and a smaller line reading exactly "Search 'BiteBuddy: Ai calorie scanner'". Peach (#F4A261) accents. No other text, no watermark.

---

### Post 08 of 21 — `2026-07-22-slot2` — "5 ways to actually know what's in your food" (F4-one-snap-demo, 7 slides)


**Upload target:** commit each finished PNG into `Posts/2026-W30/2026-07-22-slot2/slides/` on branch `main`
of `clarson2706/BiteBuddyMVP`, named `01.png` … `07.png` (one image per slide, in order).
See the week's `CHATGPT-GENERATION-GUIDE.md` → "Uploading to GitHub" for the exact API call.
**Every image size:** exactly 1080 x 1350 pixels (4:5 vertical). No exceptions.
**Text:** render each headline EXACTLY as quoted — correct spelling, no extra words.
**Palette:** cream #FFF8F1 · peach #F4A261 · deep orange #E9843A · sage #8FA27F · lavender #C9C4F2.
**App UI appears on the FINAL slide only** — place the uploaded `today-home-hero.png` in the phone
silhouette exactly as-is. Every other slide is educational: food photography or clean type, no app UI.

Generate the slides in order, upload `01.png…` to `Posts/2026-W30/2026-07-22-slot2/slides/`, confirm each commit, then move on.
(Fallback if GitHub write isn't set up: return a `2026-07-22-slot2.zip` of the PNGs instead.)

## Slide 01 — COVER
On-slide text: "5 ways to actually know what's in your food"

Vertical 4:5 editorial poster, exactly 1080 x 1350 pixels (4:5 vertical), warm cream (#FFF8F1) background. Big bold rounded headline across the top reading exactly "5 ways to actually know what's in your food" in deep orange (#E9843A). A smaller subtitle just below reading exactly "You don't need to memorize a database — just these five habits." in soft charcoal. A cute chubby round fuzzy monster mascot named BiteBuddy, soft 3D character render, Pixar-like, wholesome and friendly. Soft lavender / periwinkle purple fuzzy fur with subtle subsurface scattering. Two small smooth beige curved horns on top of the head. Large round glossy black eyes with bright white highlights. Small friendly mouth with two tiny lower fangs. Wearing an oversized cream knit hoodie with drawstrings and a front pocket. Short stubby legs with little clawed feet and small rounded paws. Soft studio lighting from the upper left. Posed as: curious, one eyebrow raised, holding a small magnifying glass to one eye. Buddy sits SMALL in the lower third as a friendly host — he does not fill the frame. Lots of negative space, subtle peach (#F4A261) accent shapes. No app screenshots, no watermark, no drawn effects around Buddy.

## Slide 02 — TIP 1
On-slide text: "1. Read the serving size first"

Vertical 4:5, exactly 1080 x 1350 pixels (4:5 vertical), warm cream (#FFF8F1) background. Realistic, appetizing food photography of a nutrition label close-up with the serving size highlighted, filling the top ~60% of the frame, natural soft light, no text baked into the food. Below the photo, a bold rounded headline reading exactly "1. Read the serving size first" in deep orange (#E9843A) on cream. A small caption below reading exactly "everything else scales from it" in charcoal. No mascot, no app UI, no watermark. Clean editorial nutrition-post look.

## Slide 03 — TIP 2
On-slide text: "2. Scan the barcode for packaged food"

Vertical 4:5, exactly 1080 x 1350 pixels (4:5 vertical), warm cream (#FFF8F1) background. Realistic, appetizing food photography of a hand holding a packaged snack showing its barcode, filling the top ~60% of the frame, natural soft light, no text baked into the food. Below the photo, a bold rounded headline reading exactly "2. Scan the barcode for packaged food" in deep orange (#E9843A) on cream. A small caption below reading exactly "exact numbers, zero guessing" in charcoal. No mascot, no app UI, no watermark. Clean editorial nutrition-post look.

## Slide 04 — TIP 3
On-slide text: "3. Use your hand as a portion guide"

Vertical 4:5, exactly 1080 x 1350 pixels (4:5 vertical), warm cream (#FFF8F1) background. Realistic, appetizing food photography of a plate next to an open palm for scale, filling the top ~60% of the frame, natural soft light, no text baked into the food. Below the photo, a bold rounded headline reading exactly "3. Use your hand as a portion guide" in deep orange (#E9843A) on cream. A small caption below reading exactly "palm = protein, fist = carbs, thumb = fats" in charcoal. No mascot, no app UI, no watermark. Clean editorial nutrition-post look.

## Slide 05 — TIP 4
On-slide text: "4. Watch liquid calories"

Vertical 4:5, exactly 1080 x 1350 pixels (4:5 vertical), warm cream (#FFF8F1) background. Realistic, appetizing food photography of a lineup of a soda, a juice, and a coffee drink, filling the top ~60% of the frame, natural soft light, no text baked into the food. Below the photo, a bold rounded headline reading exactly "4. Watch liquid calories" in deep orange (#E9843A) on cream. A small caption below reading exactly "drinks and oils add up fastest" in charcoal. No mascot, no app UI, no watermark. Clean editorial nutrition-post look.

## Slide 06 — TIP 5
On-slide text: "5. When in doubt, photograph it"

Vertical 4:5, exactly 1080 x 1350 pixels (4:5 vertical), warm cream (#FFF8F1) background. Realistic, appetizing food photography of a phone photographing a plated dinner from above, filling the top ~60% of the frame, natural soft light, no text baked into the food. Below the photo, a bold rounded headline reading exactly "5. When in doubt, photograph it" in deep orange (#E9843A) on cream. A small caption below reading exactly "AI fills the gaps you can't eyeball" in charcoal. No mascot, no app UI, no watermark. Clean editorial nutrition-post look.

## Slide 07 — CTA — DOWNLOAD (only app slide)
On-slide text: "One photo does all five · Download BiteBuddy — free on the App Store"

Vertical 4:5, exactly 1080 x 1350 pixels (4:5 vertical), warm cream (#FFF8F1) background. THIS IS THE ONLY SLIDE THAT SHOWS THE APP. Centered: a clean, simple iPhone silhouette / phone frame containing the uploaded screenshot today-home-hero.png (the BiteBuddy 'Today' home screen) placed exactly as-is — do NOT redraw, recolor, crop out, or invent any UI. A cute chubby round fuzzy monster mascot named BiteBuddy, soft 3D character render, Pixar-like, wholesome and friendly. Soft lavender / periwinkle purple fuzzy fur with subtle subsurface scattering. Two small smooth beige curved horns on top of the head. Large round glossy black eyes with bright white highlights. Small friendly mouth with two tiny lower fangs. Wearing an oversized cream knit hoodie with drawstrings and a front pocket. Short stubby legs with little clawed feet and small rounded paws. Soft studio lighting from the upper left. Posed as: joyful mid-jump, both arms thrown up, huge happy smile, starry eyes. Buddy stands beside the phone, small-to-medium, celebrating. A top headline reading exactly "One photo does all five" in deep orange (#E9843A). Below the phone, bold text reading exactly "Download BiteBuddy — free on the App Store", and a smaller line reading exactly "Search 'BiteBuddy: Ai calorie scanner'". Peach (#F4A261) accents. No other text, no watermark.

---

### Post 09 of 21 — `2026-07-22-slot3` — "6 'diet' drinks with more sugar than soda" (F1-buddys-list, 7 slides)


**Upload target:** commit each finished PNG into `Posts/2026-W30/2026-07-22-slot3/slides/` on branch `main`
of `clarson2706/BiteBuddyMVP`, named `01.png` … `07.png` (one image per slide, in order).
See the week's `CHATGPT-GENERATION-GUIDE.md` → "Uploading to GitHub" for the exact API call.
**Every image size:** exactly 1080 x 1350 pixels (4:5 vertical). No exceptions.
**Text:** render each headline EXACTLY as quoted — correct spelling, no extra words.
**Palette:** cream #FFF8F1 · peach #F4A261 · deep orange #E9843A · sage #8FA27F · lavender #C9C4F2.
**App UI appears on the FINAL slide only** — place the uploaded `today-home-hero.png` in the phone
silhouette exactly as-is. Every other slide is educational: food photography or clean type, no app UI.

Generate the slides in order, upload `01.png…` to `Posts/2026-W30/2026-07-22-slot3/slides/`, confirm each commit, then move on.
(Fallback if GitHub write isn't set up: return a `2026-07-22-slot3.zip` of the PNGs instead.)

## Slide 01 — COVER
On-slide text: "6 'diet' drinks with more sugar than soda"

Vertical 4:5 editorial poster, exactly 1080 x 1350 pixels (4:5 vertical), warm cream (#FFF8F1) background. Big bold rounded headline across the top reading exactly "6 'diet' drinks with more sugar than soda" in deep orange (#E9843A). A smaller subtitle just below reading exactly "Skipped the soda and grabbed one of these? Check the sugar first." in soft charcoal. A cute chubby round fuzzy monster mascot named BiteBuddy, soft 3D character render, Pixar-like, wholesome and friendly. Soft lavender / periwinkle purple fuzzy fur with subtle subsurface scattering. Two small smooth beige curved horns on top of the head. Large round glossy black eyes with bright white highlights. Small friendly mouth with two tiny lower fangs. Wearing an oversized cream knit hoodie with drawstrings and a front pocket. Short stubby legs with little clawed feet and small rounded paws. Soft studio lighting from the upper left. Posed as: curious, one eyebrow raised, holding a small magnifying glass to one eye. Buddy sits SMALL in the lower third as a friendly host — he does not fill the frame. Lots of negative space, subtle peach (#F4A261) accent shapes. No app screenshots, no watermark, no drawn effects around Buddy.

## Slide 02 — CONTEXT
On-slide text: "Skipped the soda and grabbed one of these? Check the sugar first."

Vertical 4:5, exactly 1080 x 1350 pixels (4:5 vertical), warm cream (#FFF8F1) background. A clean typographic slide: a big bold rounded headline centered reading exactly "Skipped the soda and grabbed one of these? Check the sugar first." in deep orange (#E9843A). Generous negative space, subtle peach (#F4A261) and sage (#8FA27F) accent shapes in the corners. No mascot, no app UI, no watermark.

## Slide 03 — FACT 1
On-slide text: "Bottled sweet tea — often 35g+ sugar, more than cola"

Vertical 4:5, exactly 1080 x 1350 pixels (4:5 vertical), warm cream (#FFF8F1) background. Realistic, appetizing food photography of a tall glass and bottle of iced sweet tea, filling the top ~60% of the frame, natural soft light, no text baked into the food. Below the photo, a bold rounded headline reading exactly "Bottled sweet tea — often 35g+ sugar, more than cola" in deep orange (#E9843A) on cream. No mascot, no app UI, no watermark. Clean editorial nutrition-post look.

## Slide 04 — FACT 2
On-slide text: "Flavored coffee drinks — the syrup still counts"

Vertical 4:5, exactly 1080 x 1350 pixels (4:5 vertical), warm cream (#FFF8F1) background. Realistic, appetizing food photography of an iced flavored coffee drink with syrup and whipped cream, filling the top ~60% of the frame, natural soft light, no text baked into the food. Below the photo, a bold rounded headline reading exactly "Flavored coffee drinks — the syrup still counts" in deep orange (#E9843A) on cream. No mascot, no app UI, no watermark. Clean editorial nutrition-post look.

## Slide 05 — FACT 3
On-slide text: "Some kombucha — 'fermented' isn't 'sugar-free'"

Vertical 4:5, exactly 1080 x 1350 pixels (4:5 vertical), warm cream (#FFF8F1) background. Realistic, appetizing food photography of a glass bottle of kombucha poured into a glass, filling the top ~60% of the frame, natural soft light, no text baked into the food. Below the photo, a bold rounded headline reading exactly "Some kombucha — 'fermented' isn't 'sugar-free'" in deep orange (#E9843A) on cream. No mascot, no app UI, no watermark. Clean editorial nutrition-post look.

## Slide 06 — FACT 4
On-slide text: "Sports drinks — built for a workout, not a desk"

Vertical 4:5, exactly 1080 x 1350 pixels (4:5 vertical), warm cream (#FFF8F1) background. Realistic, appetizing food photography of a bottle of bright-colored sports drink, filling the top ~60% of the frame, natural soft light, no text baked into the food. Below the photo, a bold rounded headline reading exactly "Sports drinks — built for a workout, not a desk" in deep orange (#E9843A) on cream. No mascot, no app UI, no watermark. Clean editorial nutrition-post look.

## Slide 07 — CTA — DOWNLOAD (only app slide)
On-slide text: "See the sugar before you sip · Download BiteBuddy — free on the App Store"

Vertical 4:5, exactly 1080 x 1350 pixels (4:5 vertical), warm cream (#FFF8F1) background. THIS IS THE ONLY SLIDE THAT SHOWS THE APP. Centered: a clean, simple iPhone silhouette / phone frame containing the uploaded screenshot today-home-hero.png (the BiteBuddy 'Today' home screen) placed exactly as-is — do NOT redraw, recolor, crop out, or invent any UI. A cute chubby round fuzzy monster mascot named BiteBuddy, soft 3D character render, Pixar-like, wholesome and friendly. Soft lavender / periwinkle purple fuzzy fur with subtle subsurface scattering. Two small smooth beige curved horns on top of the head. Large round glossy black eyes with bright white highlights. Small friendly mouth with two tiny lower fangs. Wearing an oversized cream knit hoodie with drawstrings and a front pocket. Short stubby legs with little clawed feet and small rounded paws. Soft studio lighting from the upper left. Posed as: joyful mid-jump, both arms thrown up, huge happy smile, starry eyes. Buddy stands beside the phone, small-to-medium, celebrating. A top headline reading exactly "See the sugar before you sip" in deep orange (#E9843A). Below the phone, bold text reading exactly "Download BiteBuddy — free on the App Store", and a smaller line reading exactly "Search 'BiteBuddy: Ai calorie scanner'". Peach (#F4A261) accents. No other text, no watermark.

---

### Post 10 of 21 — `2026-07-23-slot1` — "Guess the calories: 'healthy' snacks that aren't" (F2-guess-the-calories, 8 slides)


**Upload target:** commit each finished PNG into `Posts/2026-W30/2026-07-23-slot1/slides/` on branch `main`
of `clarson2706/BiteBuddyMVP`, named `01.png` … `08.png` (one image per slide, in order).
See the week's `CHATGPT-GENERATION-GUIDE.md` → "Uploading to GitHub" for the exact API call.
**Every image size:** exactly 1080 x 1350 pixels (4:5 vertical). No exceptions.
**Text:** render each headline EXACTLY as quoted — correct spelling, no extra words.
**Palette:** cream #FFF8F1 · peach #F4A261 · deep orange #E9843A · sage #8FA27F · lavender #C9C4F2.
**App UI appears on the FINAL slide only** — place the uploaded `today-home-hero.png` in the phone
silhouette exactly as-is. Every other slide is educational: food photography or clean type, no app UI.

Generate the slides in order, upload `01.png…` to `Posts/2026-W30/2026-07-23-slot1/slides/`, confirm each commit, then move on.
(Fallback if GitHub write isn't set up: return a `2026-07-23-slot1.zip` of the PNGs instead.)

## Slide 01 — COVER
On-slide text: "Guess the calories: 'healthy' snacks that aren't"

Vertical 4:5 editorial poster, exactly 1080 x 1350 pixels (4:5 vertical), warm cream (#FFF8F1) background. Big bold rounded headline across the top reading exactly "Guess the calories: 'healthy' snacks that aren't" in deep orange (#E9843A). A smaller subtitle just below reading exactly "The 'good for you' label hides some big numbers. Keep score." in soft charcoal. A cute chubby round fuzzy monster mascot named BiteBuddy, soft 3D character render, Pixar-like, wholesome and friendly. Soft lavender / periwinkle purple fuzzy fur with subtle subsurface scattering. Two small smooth beige curved horns on top of the head. Large round glossy black eyes with bright white highlights. Small friendly mouth with two tiny lower fangs. Wearing an oversized cream knit hoodie with drawstrings and a front pocket. Short stubby legs with little clawed feet and small rounded paws. Soft studio lighting from the upper left. Posed as: thoughtful, one paw on chin, head tilted up, small 'hmm' expression. Buddy sits SMALL in the lower third as a friendly host — he does not fill the frame. Lots of negative space, subtle peach (#F4A261) accent shapes. No app screenshots, no watermark, no drawn effects around Buddy.

## Slide 02 — Q1
On-slide text: "Granola bar? 🍫"

Vertical 4:5, exactly 1080 x 1350 pixels (4:5 vertical), warm cream (#FFF8F1) background. A large realistic, appetizing food photograph of a single unwrapped granola bar on a napkin filling the top ~70% of the frame — do NOT show any calorie number. A bold headline below reading exactly "Granola bar? 🍫" in deep orange (#E9843A). No mascot, no app UI. Make the viewer want to guess.

## Slide 03 — A1
On-slide text: "≈ 250 cal — one bar"

Vertical 4:5, exactly 1080 x 1350 pixels (4:5 vertical), warm cream (#FFF8F1) background. The same a single unwrapped granola bar on a napkin, photographed appetizingly in the top ~55% of the frame. Below it, a very large bold number reading exactly "≈ 250 cal" in deep orange (#E9843A), and a line reading exactly "one bar" in charcoal. A cute chubby round fuzzy monster mascot named BiteBuddy, soft 3D character render, Pixar-like, wholesome and friendly. Soft lavender / periwinkle purple fuzzy fur with subtle subsurface scattering. Two small smooth beige curved horns on top of the head. Large round glossy black eyes with bright white highlights. Small friendly mouth with two tiny lower fangs. Wearing an oversized cream knit hoodie with drawstrings and a front pocket. Short stubby legs with little clawed feet and small rounded paws. Soft studio lighting from the upper left. Posed as: full and satisfied, leaning back, paw on a rounder belly, cozy sleepy smile. Buddy is SMALL in a bottom corner reacting — not filling the frame. No app UI, no watermark.

## Slide 04 — Q2
On-slide text: "Dried fruit & nut mix? 🥜"

Vertical 4:5, exactly 1080 x 1350 pixels (4:5 vertical), warm cream (#FFF8F1) background. A large realistic, appetizing food photograph of a small bowl of dried fruit and nut trail mix filling the top ~70% of the frame — do NOT show any calorie number. A bold headline below reading exactly "Dried fruit & nut mix? 🥜" in deep orange (#E9843A). No mascot, no app UI. Make the viewer want to guess.

## Slide 05 — A2
On-slide text: "≈ 400 cal — per handful-and-a-half"

Vertical 4:5, exactly 1080 x 1350 pixels (4:5 vertical), warm cream (#FFF8F1) background. The same a small bowl of dried fruit and nut trail mix, photographed appetizingly in the top ~55% of the frame. Below it, a very large bold number reading exactly "≈ 400 cal" in deep orange (#E9843A), and a line reading exactly "per handful-and-a-half" in charcoal. A cute chubby round fuzzy monster mascot named BiteBuddy, soft 3D character render, Pixar-like, wholesome and friendly. Soft lavender / periwinkle purple fuzzy fur with subtle subsurface scattering. Two small smooth beige curved horns on top of the head. Large round glossy black eyes with bright white highlights. Small friendly mouth with two tiny lower fangs. Wearing an oversized cream knit hoodie with drawstrings and a front pocket. Short stubby legs with little clawed feet and small rounded paws. Soft studio lighting from the upper left. Posed as: squinting, one paw waving something away, mildly bothered but friendly. Buddy is SMALL in a bottom corner reacting — not filling the frame. No app UI, no watermark.

## Slide 06 — Q3
On-slide text: "Veggie chips? 🥔"

Vertical 4:5, exactly 1080 x 1350 pixels (4:5 vertical), warm cream (#FFF8F1) background. A large realistic, appetizing food photograph of a bowl of colorful veggie chips filling the top ~70% of the frame — do NOT show any calorie number. A bold headline below reading exactly "Veggie chips? 🥔" in deep orange (#E9843A). No mascot, no app UI. Make the viewer want to guess.

## Slide 07 — A3
On-slide text: "≈ 350 cal — same oil as regular chips"

Vertical 4:5, exactly 1080 x 1350 pixels (4:5 vertical), warm cream (#FFF8F1) background. The same a bowl of colorful veggie chips, photographed appetizingly in the top ~55% of the frame. Below it, a very large bold number reading exactly "≈ 350 cal" in deep orange (#E9843A), and a line reading exactly "same oil as regular chips" in charcoal. A cute chubby round fuzzy monster mascot named BiteBuddy, soft 3D character render, Pixar-like, wholesome and friendly. Soft lavender / periwinkle purple fuzzy fur with subtle subsurface scattering. Two small smooth beige curved horns on top of the head. Large round glossy black eyes with bright white highlights. Small friendly mouth with two tiny lower fangs. Wearing an oversized cream knit hoodie with drawstrings and a front pocket. Short stubby legs with little clawed feet and small rounded paws. Soft studio lighting from the upper left. Posed as: over-excited and jittery, wide sparkling eyes, arms flung up. Buddy is SMALL in a bottom corner reacting — not filling the frame. No app UI, no watermark.

## Slide 08 — CTA — DOWNLOAD (only app slide)
On-slide text: "See the real number on any snack · Download BiteBuddy — free on the App Store"

Vertical 4:5, exactly 1080 x 1350 pixels (4:5 vertical), warm cream (#FFF8F1) background. THIS IS THE ONLY SLIDE THAT SHOWS THE APP. Centered: a clean, simple iPhone silhouette / phone frame containing the uploaded screenshot today-home-hero.png (the BiteBuddy 'Today' home screen) placed exactly as-is — do NOT redraw, recolor, crop out, or invent any UI. A cute chubby round fuzzy monster mascot named BiteBuddy, soft 3D character render, Pixar-like, wholesome and friendly. Soft lavender / periwinkle purple fuzzy fur with subtle subsurface scattering. Two small smooth beige curved horns on top of the head. Large round glossy black eyes with bright white highlights. Small friendly mouth with two tiny lower fangs. Wearing an oversized cream knit hoodie with drawstrings and a front pocket. Short stubby legs with little clawed feet and small rounded paws. Soft studio lighting from the upper left. Posed as: joyful mid-jump, both arms thrown up, huge happy smile, starry eyes. Buddy stands beside the phone, small-to-medium, celebrating. A top headline reading exactly "See the real number on any snack" in deep orange (#E9843A). Below the phone, bold text reading exactly "Download BiteBuddy — free on the App Store", and a smaller line reading exactly "Search 'BiteBuddy: Ai calorie scanner'". Peach (#F4A261) accents. No other text, no watermark.

---

### Post 11 of 21 — `2026-07-23-slot2` — "The real reason you quit calorie apps" (F3-i-was-wrong, 6 slides)


**Upload target:** commit each finished PNG into `Posts/2026-W30/2026-07-23-slot2/slides/` on branch `main`
of `clarson2706/BiteBuddyMVP`, named `01.png` … `06.png` (one image per slide, in order).
See the week's `CHATGPT-GENERATION-GUIDE.md` → "Uploading to GitHub" for the exact API call.
**Every image size:** exactly 1080 x 1350 pixels (4:5 vertical). No exceptions.
**Text:** render each headline EXACTLY as quoted — correct spelling, no extra words.
**Palette:** cream #FFF8F1 · peach #F4A261 · deep orange #E9843A · sage #8FA27F · lavender #C9C4F2.
**App UI appears on the FINAL slide only** — place the uploaded `today-home-hero.png` in the phone
silhouette exactly as-is. Every other slide is educational: food photography or clean type, no app UI.

Generate the slides in order, upload `01.png…` to `Posts/2026-W30/2026-07-23-slot2/slides/`, confirm each commit, then move on.
(Fallback if GitHub write isn't set up: return a `2026-07-23-slot2.zip` of the PNGs instead.)

## Slide 01 — COVER
On-slide text: "The real reason you quit calorie apps · It's not willpower. It's the typing."

Vertical 4:5 editorial poster, exactly 1080 x 1350 pixels (4:5 vertical), warm cream (#FFF8F1) background. Big bold rounded headline across the top reading exactly "The real reason you quit calorie apps" in deep orange (#E9843A). A smaller subtitle just below reading exactly "It's not willpower. It's the typing." in soft charcoal. A cute chubby round fuzzy monster mascot named BiteBuddy, soft 3D character render, Pixar-like, wholesome and friendly. Soft lavender / periwinkle purple fuzzy fur with subtle subsurface scattering. Two small smooth beige curved horns on top of the head. Large round glossy black eyes with bright white highlights. Small friendly mouth with two tiny lower fangs. Wearing an oversized cream knit hoodie with drawstrings and a front pocket. Short stubby legs with little clawed feet and small rounded paws. Soft studio lighting from the upper left. Posed as: squinting, one paw waving something away, mildly bothered but friendly. Buddy sits SMALL in the lower third as a friendly host — he does not fill the frame. Lots of negative space, subtle peach (#F4A261) accent shapes. No app screenshots, no watermark, no drawn effects around Buddy.

## Slide 02 — PAIN
On-slide text: "Searching 'grilled chicken bowl, extra rice, light sauce' — three times a day."

Vertical 4:5, exactly 1080 x 1350 pixels (4:5 vertical), warm cream (#FFF8F1) background. A clean typographic slide: a big bold rounded headline centered reading exactly "Searching 'grilled chicken bowl, extra rice, light sauce' — three times a day." in deep orange (#E9843A). Generous negative space, subtle peach (#F4A261) and sage (#8FA27F) accent shapes in the corners. No mascot, no app UI, no watermark.

## Slide 03 — INSIGHT
On-slide text: "Friction is what kills habits, not a lack of discipline."

Vertical 4:5, exactly 1080 x 1350 pixels (4:5 vertical), warm cream (#FFF8F1) background. A clean typographic slide: a big bold rounded headline centered reading exactly "Friction is what kills habits, not a lack of discipline." in deep orange (#E9843A). Generous negative space, subtle peach (#F4A261) and sage (#8FA27F) accent shapes in the corners. No mascot, no app UI, no watermark.

## Slide 04 — SHIFT
On-slide text: "Take a photo instead of typing a whole paragraph."

Vertical 4:5, exactly 1080 x 1350 pixels (4:5 vertical), warm cream (#FFF8F1) background. A clean typographic slide: a big bold rounded headline centered reading exactly "Take a photo instead of typing a whole paragraph." in deep orange (#E9843A). Generous negative space, subtle peach (#F4A261) and sage (#8FA27F) accent shapes in the corners. No mascot, no app UI, no watermark.

## Slide 05 — PAYOFF
On-slide text: "Logging went from 5 minutes to 5 seconds."

Vertical 4:5, exactly 1080 x 1350 pixels (4:5 vertical), warm cream (#FFF8F1) background. A clean typographic slide: a big bold rounded headline centered reading exactly "Logging went from 5 minutes to 5 seconds." in deep orange (#E9843A). Generous negative space, subtle peach (#F4A261) and sage (#8FA27F) accent shapes in the corners. No mascot, no app UI, no watermark.

## Slide 06 — CTA — DOWNLOAD (only app slide)
On-slide text: "Skip the typing entirely · Download BiteBuddy — free on the App Store"

Vertical 4:5, exactly 1080 x 1350 pixels (4:5 vertical), warm cream (#FFF8F1) background. THIS IS THE ONLY SLIDE THAT SHOWS THE APP. Centered: a clean, simple iPhone silhouette / phone frame containing the uploaded screenshot today-home-hero.png (the BiteBuddy 'Today' home screen) placed exactly as-is — do NOT redraw, recolor, crop out, or invent any UI. A cute chubby round fuzzy monster mascot named BiteBuddy, soft 3D character render, Pixar-like, wholesome and friendly. Soft lavender / periwinkle purple fuzzy fur with subtle subsurface scattering. Two small smooth beige curved horns on top of the head. Large round glossy black eyes with bright white highlights. Small friendly mouth with two tiny lower fangs. Wearing an oversized cream knit hoodie with drawstrings and a front pocket. Short stubby legs with little clawed feet and small rounded paws. Soft studio lighting from the upper left. Posed as: joyful mid-jump, both arms thrown up, huge happy smile, starry eyes. Buddy stands beside the phone, small-to-medium, celebrating. A top headline reading exactly "Skip the typing entirely" in deep orange (#E9843A). Below the phone, bold text reading exactly "Download BiteBuddy — free on the App Store", and a smaller line reading exactly "Search 'BiteBuddy: Ai calorie scanner'". Peach (#F4A261) accents. No other text, no watermark.

---

### Post 12 of 21 — `2026-07-23-slot3` — "How to read a nutrition label in 10 seconds" (F4-one-snap-demo, 6 slides)


**Upload target:** commit each finished PNG into `Posts/2026-W30/2026-07-23-slot3/slides/` on branch `main`
of `clarson2706/BiteBuddyMVP`, named `01.png` … `06.png` (one image per slide, in order).
See the week's `CHATGPT-GENERATION-GUIDE.md` → "Uploading to GitHub" for the exact API call.
**Every image size:** exactly 1080 x 1350 pixels (4:5 vertical). No exceptions.
**Text:** render each headline EXACTLY as quoted — correct spelling, no extra words.
**Palette:** cream #FFF8F1 · peach #F4A261 · deep orange #E9843A · sage #8FA27F · lavender #C9C4F2.
**App UI appears on the FINAL slide only** — place the uploaded `today-home-hero.png` in the phone
silhouette exactly as-is. Every other slide is educational: food photography or clean type, no app UI.

Generate the slides in order, upload `01.png…` to `Posts/2026-W30/2026-07-23-slot3/slides/`, confirm each commit, then move on.
(Fallback if GitHub write isn't set up: return a `2026-07-23-slot3.zip` of the PNGs instead.)

## Slide 01 — COVER
On-slide text: "How to read a nutrition label in 10 seconds"

Vertical 4:5 editorial poster, exactly 1080 x 1350 pixels (4:5 vertical), warm cream (#FFF8F1) background. Big bold rounded headline across the top reading exactly "How to read a nutrition label in 10 seconds" in deep orange (#E9843A). A smaller subtitle just below reading exactly "Four numbers do 90% of the work. Here's the order to read them." in soft charcoal. A cute chubby round fuzzy monster mascot named BiteBuddy, soft 3D character render, Pixar-like, wholesome and friendly. Soft lavender / periwinkle purple fuzzy fur with subtle subsurface scattering. Two small smooth beige curved horns on top of the head. Large round glossy black eyes with bright white highlights. Small friendly mouth with two tiny lower fangs. Wearing an oversized cream knit hoodie with drawstrings and a front pocket. Short stubby legs with little clawed feet and small rounded paws. Soft studio lighting from the upper left. Posed as: curious, one eyebrow raised, holding a small magnifying glass to one eye. Buddy sits SMALL in the lower third as a friendly host — he does not fill the frame. Lots of negative space, subtle peach (#F4A261) accent shapes. No app screenshots, no watermark, no drawn effects around Buddy.

## Slide 02 — TIP 1
On-slide text: "1. Serving size"

Vertical 4:5, exactly 1080 x 1350 pixels (4:5 vertical), warm cream (#FFF8F1) background. Realistic, appetizing food photography of a nutrition label with the serving size line in focus, filling the top ~60% of the frame, natural soft light, no text baked into the food. Below the photo, a bold rounded headline reading exactly "1. Serving size" in deep orange (#E9843A) on cream. A small caption below reading exactly "the number everything is 'per'" in charcoal. No mascot, no app UI, no watermark. Clean editorial nutrition-post look.

## Slide 03 — TIP 2
On-slide text: "2. Servings per container"

Vertical 4:5, exactly 1080 x 1350 pixels (4:5 vertical), warm cream (#FFF8F1) background. Realistic, appetizing food photography of a snack bag next to a nutrition label, filling the top ~60% of the frame, natural soft light, no text baked into the food. Below the photo, a bold rounded headline reading exactly "2. Servings per container" in deep orange (#E9843A) on cream. A small caption below reading exactly "eating the whole thing? multiply" in charcoal. No mascot, no app UI, no watermark. Clean editorial nutrition-post look.

## Slide 04 — TIP 3
On-slide text: "3. Calories + protein"

Vertical 4:5, exactly 1080 x 1350 pixels (4:5 vertical), warm cream (#FFF8F1) background. Realistic, appetizing food photography of a nutrition label with calories and protein highlighted, filling the top ~60% of the frame, natural soft light, no text baked into the food. Below the photo, a bold rounded headline reading exactly "3. Calories + protein" in deep orange (#E9843A) on cream. A small caption below reading exactly "your two anchor numbers" in charcoal. No mascot, no app UI, no watermark. Clean editorial nutrition-post look.

## Slide 05 — TIP 4
On-slide text: "4. Added sugars"

Vertical 4:5, exactly 1080 x 1350 pixels (4:5 vertical), warm cream (#FFF8F1) background. Realistic, appetizing food photography of a nutrition label with the added-sugars line highlighted, filling the top ~60% of the frame, natural soft light, no text baked into the food. Below the photo, a bold rounded headline reading exactly "4. Added sugars" in deep orange (#E9843A) on cream. A small caption below reading exactly "the line most people skip" in charcoal. No mascot, no app UI, no watermark. Clean editorial nutrition-post look.

## Slide 06 — CTA — DOWNLOAD (only app slide)
On-slide text: "Skip the label math — scan it instead · Download BiteBuddy — free on the App Store"

Vertical 4:5, exactly 1080 x 1350 pixels (4:5 vertical), warm cream (#FFF8F1) background. THIS IS THE ONLY SLIDE THAT SHOWS THE APP. Centered: a clean, simple iPhone silhouette / phone frame containing the uploaded screenshot today-home-hero.png (the BiteBuddy 'Today' home screen) placed exactly as-is — do NOT redraw, recolor, crop out, or invent any UI. A cute chubby round fuzzy monster mascot named BiteBuddy, soft 3D character render, Pixar-like, wholesome and friendly. Soft lavender / periwinkle purple fuzzy fur with subtle subsurface scattering. Two small smooth beige curved horns on top of the head. Large round glossy black eyes with bright white highlights. Small friendly mouth with two tiny lower fangs. Wearing an oversized cream knit hoodie with drawstrings and a front pocket. Short stubby legs with little clawed feet and small rounded paws. Soft studio lighting from the upper left. Posed as: joyful mid-jump, both arms thrown up, huge happy smile, starry eyes. Buddy stands beside the phone, small-to-medium, celebrating. A top headline reading exactly "Skip the label math — scan it instead" in deep orange (#E9843A). Below the phone, bold text reading exactly "Download BiteBuddy — free on the App Store", and a smaller line reading exactly "Search 'BiteBuddy: Ai calorie scanner'". Peach (#F4A261) accents. No other text, no watermark.

---

### Post 13 of 21 — `2026-07-24-slot1` — "7 late-night snacks bigger than you think" (F1-buddys-list, 9 slides)

**Upload target:** commit each finished PNG into `Posts/2026-W30/2026-07-24-slot1/slides/` on branch `main`
of `clarson2706/BiteBuddyMVP`, named `01.png` … `09.png` (one image per slide, in order).
See the week's `CHATGPT-GENERATION-GUIDE.md` → "Uploading to GitHub" for the exact API call.
**Every image size:** exactly 1080 x 1350 pixels (4:5 vertical). No exceptions.
**Text:** render each headline EXACTLY as quoted — correct spelling, no extra words.
**Palette:** cream #FFF8F1 · peach #F4A261 · deep orange #E9843A · sage #8FA27F · lavender #C9C4F2.
**App UI appears on the FINAL slide only** — place the uploaded `today-home-hero.png` in the phone
silhouette exactly as-is. Every other slide is educational: food photography or clean type, no app UI.

Generate the slides in order, upload `01.png…` to `Posts/2026-W30/2026-07-24-slot1/slides/`, confirm each commit, then move on.
(Fallback if GitHub write isn't set up: return a `2026-07-24-slot1.zip` of the PNGs instead.)

## Slide 01 — COVER
On-slide text: "7 late-night snacks bigger than you think"

Vertical 4:5 editorial poster, exactly 1080 x 1350 pixels (4:5 vertical), warm cream (#FFF8F1) background. Big bold rounded headline across the top reading exactly "7 late-night snacks bigger than you think" in deep orange (#E9843A). A smaller subtitle just below reading exactly "No bad foods here — just portions that sneak up around 11pm." in soft charcoal. A cute chubby round fuzzy monster mascot named BiteBuddy, soft 3D character render, Pixar-like, wholesome and friendly. Soft lavender / periwinkle purple fuzzy fur with subtle subsurface scattering. Two small smooth beige curved horns on top of the head. Large round glossy black eyes with bright white highlights. Small friendly mouth with two tiny lower fangs. Wearing an oversized cream knit hoodie with drawstrings and a front pocket. Short stubby legs with little clawed feet and small rounded paws. Soft studio lighting from the upper left. Posed as: curious, one eyebrow raised, holding a small magnifying glass to one eye. Buddy sits SMALL in the lower third as a friendly host — he does not fill the frame. Lots of negative space, subtle peach (#F4A261) accent shapes. No app screenshots, no watermark, no drawn effects around Buddy.


## Slide 02 — FACT 1
On-slide text: "'A few' crackers — the sleeve tells a different story"

Vertical 4:5, exactly 1080 x 1350 pixels (4:5 vertical), warm cream (#FFF8F1) background. Realistic, appetizing food photography of a big pile of crackers on a plate, filling the top ~60% of the frame, natural soft light, no text baked into the food. Below the photo, a bold rounded headline reading exactly "'A few' crackers — the sleeve tells a different story" in deep orange (#E9843A) on cream. No mascot, no app UI, no watermark. Clean editorial nutrition-post look.


## Slide 03 — FACT 2
On-slide text: "Handfuls of dry cereal — they add up fast"

Vertical 4:5, exactly 1080 x 1350 pixels (4:5 vertical), warm cream (#FFF8F1) background. Realistic, appetizing food photography of a handful and bowl of dry cereal, filling the top ~60% of the frame, natural soft light, no text baked into the food. Below the photo, a bold rounded headline reading exactly "Handfuls of dry cereal — they add up fast" in deep orange (#E9843A) on cream. No mascot, no app UI, no watermark. Clean editorial nutrition-post look.


## Slide 04 — FACT 3
On-slide text: "A 'spoonful' of PB — often 2-3 servings"

Vertical 4:5, exactly 1080 x 1350 pixels (4:5 vertical), warm cream (#FFF8F1) background. Realistic, appetizing food photography of a spoon loaded with peanut butter over a jar, filling the top ~60% of the frame, natural soft light, no text baked into the food. Below the photo, a bold rounded headline reading exactly "A 'spoonful' of PB — often 2-3 servings" in deep orange (#E9843A) on cream. No mascot, no app UI, no watermark. Clean editorial nutrition-post look.


## Slide 05 — FACT 4
On-slide text: "Trail mix — the chocolate hides real calories"

Vertical 4:5, exactly 1080 x 1350 pixels (4:5 vertical), warm cream (#FFF8F1) background. Realistic, appetizing food photography of a bowl of trail mix with chocolate and nuts, filling the top ~60% of the frame, natural soft light, no text baked into the food. Below the photo, a bold rounded headline reading exactly "Trail mix — the chocolate hides real calories" in deep orange (#E9843A) on cream. No mascot, no app UI, no watermark. Clean editorial nutrition-post look.


## Slide 06 — FACT 5
On-slide text: "Cheese cubes while you scroll — a few = a real snack"

Vertical 4:5, exactly 1080 x 1350 pixels (4:5 vertical), warm cream (#FFF8F1) background. Realistic, appetizing food photography of a small board of cheese cubes, filling the top ~60% of the frame, natural soft light, no text baked into the food. Below the photo, a bold rounded headline reading exactly "Cheese cubes while you scroll — a few = a real snack" in deep orange (#E9843A) on cream. No mascot, no app UI, no watermark. Clean editorial nutrition-post look.

## Slide 07 — FACT 6
On-slide text: "Chips straight from the bag — no bowl, no count"

Vertical 4:5, exactly 1080 x 1350 pixels (4:5 vertical), warm cream (#FFF8F1) background. Realistic, appetizing food photography of an open bag of potato chips tipped toward the camera, filling the top ~60% of the frame, natural soft light, no text baked into the food. Below the photo, a bold rounded headline reading exactly "Chips straight from the bag — no bowl, no count" in deep orange (#E9843A) on cream. No mascot, no app UI, no watermark. Clean editorial nutrition-post look.

## Slide 08 — FACT 7
On-slide text: "Ice cream by the spoonful — the tub keeps score"

Vertical 4:5, exactly 1080 x 1350 pixels (4:5 vertical), warm cream (#FFF8F1) background. Realistic, appetizing food photography of an open pint of ice cream with a spoon standing in it, filling the top ~60% of the frame, natural soft light, no text baked into the food. Below the photo, a bold rounded headline reading exactly "Ice cream by the spoonful — the tub keeps score" in deep orange (#E9843A) on cream. No mascot, no app UI, no watermark. Clean editorial nutrition-post look.

## Slide 09 — CTA — DOWNLOAD (only app slide)
On-slide text: "No shame, just numbers — snap the midnight snack too · Download BiteBuddy — free on the App Store"

Vertical 4:5, exactly 1080 x 1350 pixels (4:5 vertical), warm cream (#FFF8F1) background. THIS IS THE ONLY SLIDE THAT SHOWS THE APP. Centered: a clean, simple iPhone silhouette / phone frame containing the uploaded screenshot today-home-hero.png (the BiteBuddy 'Today' home screen) placed exactly as-is — do NOT redraw, recolor, crop out, or invent any UI. A cute chubby round fuzzy monster mascot named BiteBuddy, soft 3D character render, Pixar-like, wholesome and friendly. Soft lavender / periwinkle purple fuzzy fur with subtle subsurface scattering. Two small smooth beige curved horns on top of the head. Large round glossy black eyes with bright white highlights. Small friendly mouth with two tiny lower fangs. Wearing an oversized cream knit hoodie with drawstrings and a front pocket. Short stubby legs with little clawed feet and small rounded paws. Soft studio lighting from the upper left. Posed as: joyful mid-jump, both arms thrown up, huge happy smile, starry eyes. Buddy stands beside the phone, small-to-medium, celebrating. A top headline reading exactly "No shame, just numbers — snap the midnight snack too" in deep orange (#E9843A). Below the phone, bold text reading exactly "Download BiteBuddy — free on the App Store", and a smaller line reading exactly "Search 'BiteBuddy: Ai calorie scanner'". Peach (#F4A261) accents. No other text, no watermark.

---

### Post 14 of 21 — `2026-07-24-slot2` — "Guess the protein 💪" (F2-guess-the-calories, 8 slides)


**Upload target:** commit each finished PNG into `Posts/2026-W30/2026-07-24-slot2/slides/` on branch `main`
of `clarson2706/BiteBuddyMVP`, named `01.png` … `08.png` (one image per slide, in order).
See the week's `CHATGPT-GENERATION-GUIDE.md` → "Uploading to GitHub" for the exact API call.
**Every image size:** exactly 1080 x 1350 pixels (4:5 vertical). No exceptions.
**Text:** render each headline EXACTLY as quoted — correct spelling, no extra words.
**Palette:** cream #FFF8F1 · peach #F4A261 · deep orange #E9843A · sage #8FA27F · lavender #C9C4F2.
**App UI appears on the FINAL slide only** — place the uploaded `today-home-hero.png` in the phone
silhouette exactly as-is. Every other slide is educational: food photography or clean type, no app UI.

Generate the slides in order, upload `01.png…` to `Posts/2026-W30/2026-07-24-slot2/slides/`, confirm each commit, then move on.
(Fallback if GitHub write isn't set up: return a `2026-07-24-slot2.zip` of the PNGs instead.)

## Slide 01 — COVER
On-slide text: "Guess the protein 💪"

Vertical 4:5 editorial poster, exactly 1080 x 1350 pixels (4:5 vertical), warm cream (#FFF8F1) background. Big bold rounded headline across the top reading exactly "Guess the protein 💪" in deep orange (#E9843A). A smaller subtitle just below reading exactly "Most people are way off on protein. Keep score." in soft charcoal. A cute chubby round fuzzy monster mascot named BiteBuddy, soft 3D character render, Pixar-like, wholesome and friendly. Soft lavender / periwinkle purple fuzzy fur with subtle subsurface scattering. Two small smooth beige curved horns on top of the head. Large round glossy black eyes with bright white highlights. Small friendly mouth with two tiny lower fangs. Wearing an oversized cream knit hoodie with drawstrings and a front pocket. Short stubby legs with little clawed feet and small rounded paws. Soft studio lighting from the upper left. Posed as: thoughtful, one paw on chin, head tilted up, small 'hmm' expression. Buddy sits SMALL in the lower third as a friendly host — he does not fill the frame. Lots of negative space, subtle peach (#F4A261) accent shapes. No app screenshots, no watermark, no drawn effects around Buddy.

## Slide 02 — Q1
On-slide text: "Grilled chicken breast, 6oz? 🍗"

Vertical 4:5, exactly 1080 x 1350 pixels (4:5 vertical), warm cream (#FFF8F1) background. A large realistic, appetizing food photograph of a grilled chicken breast on a plate filling the top ~70% of the frame — do NOT show any calorie number. A bold headline below reading exactly "Grilled chicken breast, 6oz? 🍗" in deep orange (#E9843A). No mascot, no app UI. Make the viewer want to guess.

## Slide 03 — A1
On-slide text: "≈ 50g protein — solid choice"

Vertical 4:5, exactly 1080 x 1350 pixels (4:5 vertical), warm cream (#FFF8F1) background. The same a grilled chicken breast on a plate, photographed appetizingly in the top ~55% of the frame. Below it, a very large bold number reading exactly "≈ 50g protein" in deep orange (#E9843A), and a line reading exactly "solid choice" in charcoal. A cute chubby round fuzzy monster mascot named BiteBuddy, soft 3D character render, Pixar-like, wholesome and friendly. Soft lavender / periwinkle purple fuzzy fur with subtle subsurface scattering. Two small smooth beige curved horns on top of the head. Large round glossy black eyes with bright white highlights. Small friendly mouth with two tiny lower fangs. Wearing an oversized cream knit hoodie with drawstrings and a front pocket. Short stubby legs with little clawed feet and small rounded paws. Soft studio lighting from the upper left. Posed as: full and satisfied, leaning back, paw on a rounder belly, cozy sleepy smile. Buddy is SMALL in a bottom corner reacting — not filling the frame. No app UI, no watermark.

## Slide 04 — Q2
On-slide text: "Store-bought protein shake? 🥤"

Vertical 4:5, exactly 1080 x 1350 pixels (4:5 vertical), warm cream (#FFF8F1) background. A large realistic, appetizing food photograph of a ready-to-drink protein shake bottle filling the top ~70% of the frame — do NOT show any calorie number. A bold headline below reading exactly "Store-bought protein shake? 🥤" in deep orange (#E9843A). No mascot, no app UI. Make the viewer want to guess.

## Slide 05 — A2
On-slide text: "≈ 20g protein — less than the label vibe"

Vertical 4:5, exactly 1080 x 1350 pixels (4:5 vertical), warm cream (#FFF8F1) background. The same a ready-to-drink protein shake bottle, photographed appetizingly in the top ~55% of the frame. Below it, a very large bold number reading exactly "≈ 20g protein" in deep orange (#E9843A), and a line reading exactly "less than the label vibe" in charcoal. A cute chubby round fuzzy monster mascot named BiteBuddy, soft 3D character render, Pixar-like, wholesome and friendly. Soft lavender / periwinkle purple fuzzy fur with subtle subsurface scattering. Two small smooth beige curved horns on top of the head. Large round glossy black eyes with bright white highlights. Small friendly mouth with two tiny lower fangs. Wearing an oversized cream knit hoodie with drawstrings and a front pocket. Short stubby legs with little clawed feet and small rounded paws. Soft studio lighting from the upper left. Posed as: squinting, one paw waving something away, mildly bothered but friendly. Buddy is SMALL in a bottom corner reacting — not filling the frame. No app UI, no watermark.

## Slide 06 — Q3
On-slide text: "Greek yogurt cup? 🥣"

Vertical 4:5, exactly 1080 x 1350 pixels (4:5 vertical), warm cream (#FFF8F1) background. A large realistic, appetizing food photograph of a single-serve greek yogurt cup with a spoon filling the top ~70% of the frame — do NOT show any calorie number. A bold headline below reading exactly "Greek yogurt cup? 🥣" in deep orange (#E9843A). No mascot, no app UI. Make the viewer want to guess.

## Slide 07 — A3
On-slide text: "≈ 15g protein — some are basically pudding"

Vertical 4:5, exactly 1080 x 1350 pixels (4:5 vertical), warm cream (#FFF8F1) background. The same a single-serve greek yogurt cup with a spoon, photographed appetizingly in the top ~55% of the frame. Below it, a very large bold number reading exactly "≈ 15g protein" in deep orange (#E9843A), and a line reading exactly "some are basically pudding" in charcoal. A cute chubby round fuzzy monster mascot named BiteBuddy, soft 3D character render, Pixar-like, wholesome and friendly. Soft lavender / periwinkle purple fuzzy fur with subtle subsurface scattering. Two small smooth beige curved horns on top of the head. Large round glossy black eyes with bright white highlights. Small friendly mouth with two tiny lower fangs. Wearing an oversized cream knit hoodie with drawstrings and a front pocket. Short stubby legs with little clawed feet and small rounded paws. Soft studio lighting from the upper left. Posed as: over-excited and jittery, wide sparkling eyes, arms flung up. Buddy is SMALL in a bottom corner reacting — not filling the frame. No app UI, no watermark.

## Slide 08 — CTA — DOWNLOAD (only app slide)
On-slide text: "Know the protein on every plate · Download BiteBuddy — free on the App Store"

Vertical 4:5, exactly 1080 x 1350 pixels (4:5 vertical), warm cream (#FFF8F1) background. THIS IS THE ONLY SLIDE THAT SHOWS THE APP. Centered: a clean, simple iPhone silhouette / phone frame containing the uploaded screenshot today-home-hero.png (the BiteBuddy 'Today' home screen) placed exactly as-is — do NOT redraw, recolor, crop out, or invent any UI. A cute chubby round fuzzy monster mascot named BiteBuddy, soft 3D character render, Pixar-like, wholesome and friendly. Soft lavender / periwinkle purple fuzzy fur with subtle subsurface scattering. Two small smooth beige curved horns on top of the head. Large round glossy black eyes with bright white highlights. Small friendly mouth with two tiny lower fangs. Wearing an oversized cream knit hoodie with drawstrings and a front pocket. Short stubby legs with little clawed feet and small rounded paws. Soft studio lighting from the upper left. Posed as: joyful mid-jump, both arms thrown up, huge happy smile, starry eyes. Buddy stands beside the phone, small-to-medium, celebrating. A top headline reading exactly "Know the protein on every plate" in deep orange (#E9843A). Below the phone, bold text reading exactly "Download BiteBuddy — free on the App Store", and a smaller line reading exactly "Search 'BiteBuddy: Ai calorie scanner'". Peach (#F4A261) accents. No other text, no watermark.

---

### Post 15 of 21 — `2026-07-24-slot3` — "POV: a calorie app that's actually kind" (F3-i-was-wrong, 6 slides)


**Upload target:** commit each finished PNG into `Posts/2026-W30/2026-07-24-slot3/slides/` on branch `main`
of `clarson2706/BiteBuddyMVP`, named `01.png` … `06.png` (one image per slide, in order).
See the week's `CHATGPT-GENERATION-GUIDE.md` → "Uploading to GitHub" for the exact API call.
**Every image size:** exactly 1080 x 1350 pixels (4:5 vertical). No exceptions.
**Text:** render each headline EXACTLY as quoted — correct spelling, no extra words.
**Palette:** cream #FFF8F1 · peach #F4A261 · deep orange #E9843A · sage #8FA27F · lavender #C9C4F2.
**App UI appears on the FINAL slide only** — place the uploaded `today-home-hero.png` in the phone
silhouette exactly as-is. Every other slide is educational: food photography or clean type, no app UI.

Generate the slides in order, upload `01.png…` to `Posts/2026-W30/2026-07-24-slot3/slides/`, confirm each commit, then move on.
(Fallback if GitHub write isn't set up: return a `2026-07-24-slot3.zip` of the PNGs instead.)

## Slide 01 — COVER
On-slide text: "POV: a calorie app that's actually kind · no red 'over budget' numbers."

Vertical 4:5 editorial poster, exactly 1080 x 1350 pixels (4:5 vertical), warm cream (#FFF8F1) background. Big bold rounded headline across the top reading exactly "POV: a calorie app that's actually kind" in deep orange (#E9843A). A smaller subtitle just below reading exactly "no red 'over budget' numbers." in soft charcoal. A cute chubby round fuzzy monster mascot named BiteBuddy, soft 3D character render, Pixar-like, wholesome and friendly. Soft lavender / periwinkle purple fuzzy fur with subtle subsurface scattering. Two small smooth beige curved horns on top of the head. Large round glossy black eyes with bright white highlights. Small friendly mouth with two tiny lower fangs. Wearing an oversized cream knit hoodie with drawstrings and a front pocket. Short stubby legs with little clawed feet and small rounded paws. Soft studio lighting from the upper left. Posed as: cheerful and warm, one paw raised in a small wave, big open happy smile. Buddy sits SMALL in the lower third as a friendly host — he does not fill the frame. Lots of negative space, subtle peach (#F4A261) accent shapes. No app screenshots, no watermark, no drawn effects around Buddy.

## Slide 02 — PAIN
On-slide text: "Most trackers feel like being scolded by a spreadsheet."

Vertical 4:5, exactly 1080 x 1350 pixels (4:5 vertical), warm cream (#FFF8F1) background. A clean typographic slide: a big bold rounded headline centered reading exactly "Most trackers feel like being scolded by a spreadsheet." in deep orange (#E9843A). Generous negative space, subtle peach (#F4A261) and sage (#8FA27F) accent shapes in the corners. No mascot, no app UI, no watermark.

## Slide 03 — INSIGHT
On-slide text: "Shame doesn't build habits. Small, visible wins do."

Vertical 4:5, exactly 1080 x 1350 pixels (4:5 vertical), warm cream (#FFF8F1) background. A clean typographic slide: a big bold rounded headline centered reading exactly "Shame doesn't build habits. Small, visible wins do." in deep orange (#E9843A). Generous negative space, subtle peach (#F4A261) and sage (#8FA27F) accent shapes in the corners. No mascot, no app UI, no watermark.

## Slide 04 — SHIFT
On-slide text: "Streaks and a buddy that reacts beat a wall of guilt."

Vertical 4:5, exactly 1080 x 1350 pixels (4:5 vertical), warm cream (#FFF8F1) background. A clean typographic slide: a big bold rounded headline centered reading exactly "Streaks and a buddy that reacts beat a wall of guilt." in deep orange (#E9843A). Generous negative space, subtle peach (#F4A261) and sage (#8FA27F) accent shapes in the corners. No mascot, no app UI, no watermark.

## Slide 05 — PAYOFF
On-slide text: "I actually want to open it — that's the whole game."

Vertical 4:5, exactly 1080 x 1350 pixels (4:5 vertical), warm cream (#FFF8F1) background. A clean typographic slide: a big bold rounded headline centered reading exactly "I actually want to open it — that's the whole game." in deep orange (#E9843A). Generous negative space, subtle peach (#F4A261) and sage (#8FA27F) accent shapes in the corners. No mascot, no app UI, no watermark.

## Slide 06 — CTA — DOWNLOAD (only app slide)
On-slide text: "Tracking that's actually kind · Download BiteBuddy — free on the App Store"

Vertical 4:5, exactly 1080 x 1350 pixels (4:5 vertical), warm cream (#FFF8F1) background. THIS IS THE ONLY SLIDE THAT SHOWS THE APP. Centered: a clean, simple iPhone silhouette / phone frame containing the uploaded screenshot today-home-hero.png (the BiteBuddy 'Today' home screen) placed exactly as-is — do NOT redraw, recolor, crop out, or invent any UI. A cute chubby round fuzzy monster mascot named BiteBuddy, soft 3D character render, Pixar-like, wholesome and friendly. Soft lavender / periwinkle purple fuzzy fur with subtle subsurface scattering. Two small smooth beige curved horns on top of the head. Large round glossy black eyes with bright white highlights. Small friendly mouth with two tiny lower fangs. Wearing an oversized cream knit hoodie with drawstrings and a front pocket. Short stubby legs with little clawed feet and small rounded paws. Soft studio lighting from the upper left. Posed as: joyful mid-jump, both arms thrown up, huge happy smile, starry eyes. Buddy stands beside the phone, small-to-medium, celebrating. A top headline reading exactly "Tracking that's actually kind" in deep orange (#E9843A). Below the phone, bold text reading exactly "Download BiteBuddy — free on the App Store", and a smaller line reading exactly "Search 'BiteBuddy: Ai calorie scanner'". Peach (#F4A261) accents. No other text, no watermark.

---

### Post 16 of 21 — `2026-07-25-slot1` — "Portion size: the #1 thing people get wrong" (F4-one-snap-demo, 6 slides)


**Upload target:** commit each finished PNG into `Posts/2026-W30/2026-07-25-slot1/slides/` on branch `main`
of `clarson2706/BiteBuddyMVP`, named `01.png` … `06.png` (one image per slide, in order).
See the week's `CHATGPT-GENERATION-GUIDE.md` → "Uploading to GitHub" for the exact API call.
**Every image size:** exactly 1080 x 1350 pixels (4:5 vertical). No exceptions.
**Text:** render each headline EXACTLY as quoted — correct spelling, no extra words.
**Palette:** cream #FFF8F1 · peach #F4A261 · deep orange #E9843A · sage #8FA27F · lavender #C9C4F2.
**App UI appears on the FINAL slide only** — place the uploaded `today-home-hero.png` in the phone
silhouette exactly as-is. Every other slide is educational: food photography or clean type, no app UI.

Generate the slides in order, upload `01.png…` to `Posts/2026-W30/2026-07-25-slot1/slides/`, confirm each commit, then move on.
(Fallback if GitHub write isn't set up: return a `2026-07-25-slot1.zip` of the PNGs instead.)

## Slide 01 — COVER
On-slide text: "Portion size: the #1 thing people get wrong"

Vertical 4:5 editorial poster, exactly 1080 x 1350 pixels (4:5 vertical), warm cream (#FFF8F1) background. Big bold rounded headline across the top reading exactly "Portion size: the #1 thing people get wrong" in deep orange (#E9843A). A smaller subtitle just below reading exactly "It's not the food — it's how much of it lands on the plate." in soft charcoal. A cute chubby round fuzzy monster mascot named BiteBuddy, soft 3D character render, Pixar-like, wholesome and friendly. Soft lavender / periwinkle purple fuzzy fur with subtle subsurface scattering. Two small smooth beige curved horns on top of the head. Large round glossy black eyes with bright white highlights. Small friendly mouth with two tiny lower fangs. Wearing an oversized cream knit hoodie with drawstrings and a front pocket. Short stubby legs with little clawed feet and small rounded paws. Soft studio lighting from the upper left. Posed as: curious, one eyebrow raised, holding a small magnifying glass to one eye. Buddy sits SMALL in the lower third as a friendly host — he does not fill the frame. Lots of negative space, subtle peach (#F4A261) accent shapes. No app screenshots, no watermark, no drawn effects around Buddy.

## Slide 02 — TIP 1
On-slide text: "Pasta: a serving is often half your plate"

Vertical 4:5, exactly 1080 x 1350 pixels (4:5 vertical), warm cream (#FFF8F1) background. Realistic, appetizing food photography of a measured cup of pasta next to a full plated bowl, filling the top ~60% of the frame, natural soft light, no text baked into the food. Below the photo, a bold rounded headline reading exactly "Pasta: a serving is often half your plate" in deep orange (#E9843A) on cream. No mascot, no app UI, no watermark. Clean editorial nutrition-post look.

## Slide 03 — TIP 2
On-slide text: "Meat runs 1.5-2x a deck of cards"

Vertical 4:5, exactly 1080 x 1350 pixels (4:5 vertical), warm cream (#FFF8F1) background. Realistic, appetizing food photography of a cooked chicken breast beside a deck of cards for scale, filling the top ~60% of the frame, natural soft light, no text baked into the food. Below the photo, a bold rounded headline reading exactly "Meat runs 1.5-2x a deck of cards" in deep orange (#E9843A) on cream. No mascot, no app UI, no watermark. Clean editorial nutrition-post look.

## Slide 04 — TIP 3
On-slide text: "Cheese, nuts & oils look small but aren't"

Vertical 4:5, exactly 1080 x 1350 pixels (4:5 vertical), warm cream (#FFF8F1) background. Realistic, appetizing food photography of a small handful of nuts and a cube of cheese, filling the top ~60% of the frame, natural soft light, no text baked into the food. Below the photo, a bold rounded headline reading exactly "Cheese, nuts & oils look small but aren't" in deep orange (#E9843A) on cream. A small caption below reading exactly "calorie-dense in tiny amounts" in charcoal. No mascot, no app UI, no watermark. Clean editorial nutrition-post look.

## Slide 05 — TIP 4
On-slide text: "The fix: eyeball it, then adjust"

Vertical 4:5, exactly 1080 x 1350 pixels (4:5 vertical), warm cream (#FFF8F1) background. Realistic, appetizing food photography of a plate of food photographed from above, filling the top ~60% of the frame, natural soft light, no text baked into the food. Below the photo, a bold rounded headline reading exactly "The fix: eyeball it, then adjust" in deep orange (#E9843A) on cream. A small caption below reading exactly "an estimate you can correct beats a guess" in charcoal. No mascot, no app UI, no watermark. Clean editorial nutrition-post look.

## Slide 06 — CTA — DOWNLOAD (only app slide)
On-slide text: "Get portions right — then fine-tune the estimate · Download BiteBuddy — free on the App Store"

Vertical 4:5, exactly 1080 x 1350 pixels (4:5 vertical), warm cream (#FFF8F1) background. THIS IS THE ONLY SLIDE THAT SHOWS THE APP. Centered: a clean, simple iPhone silhouette / phone frame containing the uploaded screenshot today-home-hero.png (the BiteBuddy 'Today' home screen) placed exactly as-is — do NOT redraw, recolor, crop out, or invent any UI. A cute chubby round fuzzy monster mascot named BiteBuddy, soft 3D character render, Pixar-like, wholesome and friendly. Soft lavender / periwinkle purple fuzzy fur with subtle subsurface scattering. Two small smooth beige curved horns on top of the head. Large round glossy black eyes with bright white highlights. Small friendly mouth with two tiny lower fangs. Wearing an oversized cream knit hoodie with drawstrings and a front pocket. Short stubby legs with little clawed feet and small rounded paws. Soft studio lighting from the upper left. Posed as: joyful mid-jump, both arms thrown up, huge happy smile, starry eyes. Buddy stands beside the phone, small-to-medium, celebrating. A top headline reading exactly "Get portions right — then fine-tune the estimate" in deep orange (#E9843A). Below the phone, bold text reading exactly "Download BiteBuddy — free on the App Store", and a smaller line reading exactly "Search 'BiteBuddy: Ai calorie scanner'". Peach (#F4A261) accents. No other text, no watermark.

---

### Post 17 of 21 — `2026-07-25-slot2` — "Why your calorie app makes you miserable" (F1-buddys-list, 8 slides)

**Upload target:** commit each finished PNG into `Posts/2026-W30/2026-07-25-slot2/slides/` on branch `main`
of `clarson2706/BiteBuddyMVP`, named `01.png` … `08.png` (one image per slide, in order).
See the week's `CHATGPT-GENERATION-GUIDE.md` → "Uploading to GitHub" for the exact API call.
**Every image size:** exactly 1080 x 1350 pixels (4:5 vertical). No exceptions.
**Text:** render each headline EXACTLY as quoted — correct spelling, no extra words.
**Palette:** cream #FFF8F1 · peach #F4A261 · deep orange #E9843A · sage #8FA27F · lavender #C9C4F2.
**App UI appears on the FINAL slide only** — place the uploaded `today-home-hero.png` in the phone
silhouette exactly as-is. Every other slide is educational: food photography or clean type, no app UI.

Generate the slides in order, upload `01.png…` to `Posts/2026-W30/2026-07-25-slot2/slides/`, confirm each commit, then move on.
(Fallback if GitHub write isn't set up: return a `2026-07-25-slot2.zip` of the PNGs instead.)

## Slide 01 — COVER
On-slide text: "Why your calorie app makes you miserable"

Vertical 4:5 editorial poster, exactly 1080 x 1350 pixels (4:5 vertical), warm cream (#FFF8F1) background. Big bold rounded headline across the top reading exactly "Why your calorie app makes you miserable" in deep orange (#E9843A). A smaller subtitle just below reading exactly "You've deleted at least one. Here's what went wrong — and the fix." in soft charcoal. A cute chubby round fuzzy monster mascot named BiteBuddy, soft 3D character render, Pixar-like, wholesome and friendly. Soft lavender / periwinkle purple fuzzy fur with subtle subsurface scattering. Two small smooth beige curved horns on top of the head. Large round glossy black eyes with bright white highlights. Small friendly mouth with two tiny lower fangs. Wearing an oversized cream knit hoodie with drawstrings and a front pocket. Short stubby legs with little clawed feet and small rounded paws. Soft studio lighting from the upper left. Posed as: curious, one eyebrow raised, holding a small magnifying glass to one eye. Buddy sits SMALL in the lower third as a friendly host — he does not fill the frame. Lots of negative space, subtle peach (#F4A261) accent shapes. No app screenshots, no watermark, no drawn effects around Buddy.


## Slide 02 — CONTEXT
On-slide text: "You've deleted at least one. Here's what went wrong — and the fix."

Vertical 4:5, exactly 1080 x 1350 pixels (4:5 vertical), warm cream (#FFF8F1) background. A clean typographic slide: a big bold rounded headline centered reading exactly "You've deleted at least one. Here's what went wrong — and the fix." in deep orange (#E9843A). Generous negative space, subtle peach (#F4A261) and sage (#8FA27F) accent shapes in the corners. No mascot, no app UI, no watermark.


## Slide 03 — FACT 1
On-slide text: "Typing every single meal"

Vertical 4:5, exactly 1080 x 1350 pixels (4:5 vertical), warm cream (#FFF8F1) background. A clean typographic slide: a big bold rounded headline centered reading exactly "Typing every single meal" in deep orange (#E9843A). Below it, smaller text reading exactly "Fix: photograph it instead of searching a database" in charcoal. Generous negative space, subtle peach (#F4A261) and sage (#8FA27F) accent shapes in the corners. No mascot, no app UI, no watermark.


## Slide 04 — FACT 2
On-slide text: "Guilt-trip notifications"

Vertical 4:5, exactly 1080 x 1350 pixels (4:5 vertical), warm cream (#FFF8F1) background. A clean typographic slide: a big bold rounded headline centered reading exactly "Guilt-trip notifications" in deep orange (#E9843A). Below it, smaller text reading exactly "Fix: pick a tracker that's actually kind to you" in charcoal. Generous negative space, subtle peach (#F4A261) and sage (#8FA27F) accent shapes in the corners. No mascot, no app UI, no watermark.


## Slide 05 — FACT 3
On-slide text: "No idea how to log eating out"

Vertical 4:5, exactly 1080 x 1350 pixels (4:5 vertical), warm cream (#FFF8F1) background. A clean typographic slide: a big bold rounded headline centered reading exactly "No idea how to log eating out" in deep orange (#E9843A). Below it, smaller text reading exactly "Fix: start from an estimate you can edit" in charcoal. Generous negative space, subtle peach (#F4A261) and sage (#8FA27F) accent shapes in the corners. No mascot, no app UI, no watermark.


## Slide 06 — FACT 4
On-slide text: "Never knowing WHY the number is that"

Vertical 4:5, exactly 1080 x 1350 pixels (4:5 vertical), warm cream (#FFF8F1) background. A clean typographic slide: a big bold rounded headline centered reading exactly "Never knowing WHY the number is that" in deep orange (#E9843A). Below it, smaller text reading exactly "Fix: see the reasoning, not just a total" in charcoal. Generous negative space, subtle peach (#F4A261) and sage (#8FA27F) accent shapes in the corners. No mascot, no app UI, no watermark.


## Slide 07 — FACT 5
On-slide text: "One 'bad' day feels like failing the whole week"

Vertical 4:5, exactly 1080 x 1350 pixels (4:5 vertical), warm cream (#FFF8F1) background. A clean typographic slide: a big bold rounded headline centered reading exactly "One 'bad' day feels like failing the whole week" in deep orange (#E9843A). Below it, smaller text reading exactly "Fix: a tracker that just logs it and moves on — no guilt trip" in charcoal. Generous negative space, subtle peach (#F4A261) and sage (#8FA27F) accent shapes in the corners. No mascot, no app UI, no watermark.

## Slide 08 — CTA — DOWNLOAD (only app slide)
On-slide text: "Tracking that doesn't feel like a chore · Download BiteBuddy — free on the App Store"

Vertical 4:5, exactly 1080 x 1350 pixels (4:5 vertical), warm cream (#FFF8F1) background. THIS IS THE ONLY SLIDE THAT SHOWS THE APP. Centered: a clean, simple iPhone silhouette / phone frame containing the uploaded screenshot today-home-hero.png (the BiteBuddy 'Today' home screen) placed exactly as-is — do NOT redraw, recolor, crop out, or invent any UI. A cute chubby round fuzzy monster mascot named BiteBuddy, soft 3D character render, Pixar-like, wholesome and friendly. Soft lavender / periwinkle purple fuzzy fur with subtle subsurface scattering. Two small smooth beige curved horns on top of the head. Large round glossy black eyes with bright white highlights. Small friendly mouth with two tiny lower fangs. Wearing an oversized cream knit hoodie with drawstrings and a front pocket. Short stubby legs with little clawed feet and small rounded paws. Soft studio lighting from the upper left. Posed as: joyful mid-jump, both arms thrown up, huge happy smile, starry eyes. Buddy stands beside the phone, small-to-medium, celebrating. A top headline reading exactly "Tracking that doesn't feel like a chore" in deep orange (#E9843A). Below the phone, bold text reading exactly "Download BiteBuddy — free on the App Store", and a smaller line reading exactly "Search 'BiteBuddy: Ai calorie scanner'". Peach (#F4A261) accents. No other text, no watermark.

---

### Post 18 of 21 — `2026-07-25-slot3` — "Same dish, restaurant vs homemade" (F2-guess-the-calories, 8 slides)


**Upload target:** commit each finished PNG into `Posts/2026-W30/2026-07-25-slot3/slides/` on branch `main`
of `clarson2706/BiteBuddyMVP`, named `01.png` … `08.png` (one image per slide, in order).
See the week's `CHATGPT-GENERATION-GUIDE.md` → "Uploading to GitHub" for the exact API call.
**Every image size:** exactly 1080 x 1350 pixels (4:5 vertical). No exceptions.
**Text:** render each headline EXACTLY as quoted — correct spelling, no extra words.
**Palette:** cream #FFF8F1 · peach #F4A261 · deep orange #E9843A · sage #8FA27F · lavender #C9C4F2.
**App UI appears on the FINAL slide only** — place the uploaded `today-home-hero.png` in the phone
silhouette exactly as-is. Every other slide is educational: food photography or clean type, no app UI.

Generate the slides in order, upload `01.png…` to `Posts/2026-W30/2026-07-25-slot3/slides/`, confirm each commit, then move on.
(Fallback if GitHub write isn't set up: return a `2026-07-25-slot3.zip` of the PNGs instead.)

## Slide 01 — COVER
On-slide text: "Same dish, restaurant vs homemade"

Vertical 4:5 editorial poster, exactly 1080 x 1350 pixels (4:5 vertical), warm cream (#FFF8F1) background. Big bold rounded headline across the top reading exactly "Same dish, restaurant vs homemade" in deep orange (#E9843A). A smaller subtitle just below reading exactly "Who cooked it changes the number more than you'd think. Keep score." in soft charcoal. A cute chubby round fuzzy monster mascot named BiteBuddy, soft 3D character render, Pixar-like, wholesome and friendly. Soft lavender / periwinkle purple fuzzy fur with subtle subsurface scattering. Two small smooth beige curved horns on top of the head. Large round glossy black eyes with bright white highlights. Small friendly mouth with two tiny lower fangs. Wearing an oversized cream knit hoodie with drawstrings and a front pocket. Short stubby legs with little clawed feet and small rounded paws. Soft studio lighting from the upper left. Posed as: thoughtful, one paw on chin, head tilted up, small 'hmm' expression. Buddy sits SMALL in the lower third as a friendly host — he does not fill the frame. Lots of negative space, subtle peach (#F4A261) accent shapes. No app screenshots, no watermark, no drawn effects around Buddy.

## Slide 02 — Q1
On-slide text: "Chicken alfredo — which is higher? 🍝"

Vertical 4:5, exactly 1080 x 1350 pixels (4:5 vertical), warm cream (#FFF8F1) background. A large realistic, appetizing food photograph of a creamy chicken alfredo pasta plate filling the top ~70% of the frame — do NOT show any calorie number. A bold headline below reading exactly "Chicken alfredo — which is higher? 🍝" in deep orange (#E9843A). No mascot, no app UI. Make the viewer want to guess.

## Slide 03 — A1
On-slide text: "Restaurant ≈ 1,200 · Home ≈ 650 — the butter station did it"

Vertical 4:5, exactly 1080 x 1350 pixels (4:5 vertical), warm cream (#FFF8F1) background. The same a creamy chicken alfredo pasta plate, photographed appetizingly in the top ~55% of the frame. Below it, a very large bold number reading exactly "Restaurant ≈ 1,200 · Home ≈ 650" in deep orange (#E9843A), and a line reading exactly "the butter station did it" in charcoal. A cute chubby round fuzzy monster mascot named BiteBuddy, soft 3D character render, Pixar-like, wholesome and friendly. Soft lavender / periwinkle purple fuzzy fur with subtle subsurface scattering. Two small smooth beige curved horns on top of the head. Large round glossy black eyes with bright white highlights. Small friendly mouth with two tiny lower fangs. Wearing an oversized cream knit hoodie with drawstrings and a front pocket. Short stubby legs with little clawed feet and small rounded paws. Soft studio lighting from the upper left. Posed as: full and satisfied, leaning back, paw on a rounder belly, cozy sleepy smile. Buddy is SMALL in a bottom corner reacting — not filling the frame. No app UI, no watermark.

## Slide 04 — Q2
On-slide text: "Caesar salad? 🥗"

Vertical 4:5, exactly 1080 x 1350 pixels (4:5 vertical), warm cream (#FFF8F1) background. A large realistic, appetizing food photograph of a caesar salad with croutons and shaved parmesan filling the top ~70% of the frame — do NOT show any calorie number. A bold headline below reading exactly "Caesar salad? 🥗" in deep orange (#E9843A). No mascot, no app UI. Make the viewer want to guess.

## Slide 05 — A2
On-slide text: "Restaurant ≈ 700 · Home ≈ 350 — the dressing pour is heavier out"

Vertical 4:5, exactly 1080 x 1350 pixels (4:5 vertical), warm cream (#FFF8F1) background. The same a caesar salad with croutons and shaved parmesan, photographed appetizingly in the top ~55% of the frame. Below it, a very large bold number reading exactly "Restaurant ≈ 700 · Home ≈ 350" in deep orange (#E9843A), and a line reading exactly "the dressing pour is heavier out" in charcoal. A cute chubby round fuzzy monster mascot named BiteBuddy, soft 3D character render, Pixar-like, wholesome and friendly. Soft lavender / periwinkle purple fuzzy fur with subtle subsurface scattering. Two small smooth beige curved horns on top of the head. Large round glossy black eyes with bright white highlights. Small friendly mouth with two tiny lower fangs. Wearing an oversized cream knit hoodie with drawstrings and a front pocket. Short stubby legs with little clawed feet and small rounded paws. Soft studio lighting from the upper left. Posed as: squinting, one paw waving something away, mildly bothered but friendly. Buddy is SMALL in a bottom corner reacting — not filling the frame. No app UI, no watermark.

## Slide 06 — Q3
On-slide text: "Fried rice? 🍚"

Vertical 4:5, exactly 1080 x 1350 pixels (4:5 vertical), warm cream (#FFF8F1) background. A large realistic, appetizing food photograph of a plate of fried rice with vegetables and egg filling the top ~70% of the frame — do NOT show any calorie number. A bold headline below reading exactly "Fried rice? 🍚" in deep orange (#E9843A). No mascot, no app UI. Make the viewer want to guess.

## Slide 07 — A3
On-slide text: "Restaurant ≈ 900 · Home ≈ 500 — the wok oil adds up"

Vertical 4:5, exactly 1080 x 1350 pixels (4:5 vertical), warm cream (#FFF8F1) background. The same a plate of fried rice with vegetables and egg, photographed appetizingly in the top ~55% of the frame. Below it, a very large bold number reading exactly "Restaurant ≈ 900 · Home ≈ 500" in deep orange (#E9843A), and a line reading exactly "the wok oil adds up" in charcoal. A cute chubby round fuzzy monster mascot named BiteBuddy, soft 3D character render, Pixar-like, wholesome and friendly. Soft lavender / periwinkle purple fuzzy fur with subtle subsurface scattering. Two small smooth beige curved horns on top of the head. Large round glossy black eyes with bright white highlights. Small friendly mouth with two tiny lower fangs. Wearing an oversized cream knit hoodie with drawstrings and a front pocket. Short stubby legs with little clawed feet and small rounded paws. Soft studio lighting from the upper left. Posed as: over-excited and jittery, wide sparkling eyes, arms flung up. Buddy is SMALL in a bottom corner reacting — not filling the frame. No app UI, no watermark.

## Slide 08 — CTA — DOWNLOAD (only app slide)
On-slide text: "Know the real number, eating out or in · Download BiteBuddy — free on the App Store"

Vertical 4:5, exactly 1080 x 1350 pixels (4:5 vertical), warm cream (#FFF8F1) background. THIS IS THE ONLY SLIDE THAT SHOWS THE APP. Centered: a clean, simple iPhone silhouette / phone frame containing the uploaded screenshot today-home-hero.png (the BiteBuddy 'Today' home screen) placed exactly as-is — do NOT redraw, recolor, crop out, or invent any UI. A cute chubby round fuzzy monster mascot named BiteBuddy, soft 3D character render, Pixar-like, wholesome and friendly. Soft lavender / periwinkle purple fuzzy fur with subtle subsurface scattering. Two small smooth beige curved horns on top of the head. Large round glossy black eyes with bright white highlights. Small friendly mouth with two tiny lower fangs. Wearing an oversized cream knit hoodie with drawstrings and a front pocket. Short stubby legs with little clawed feet and small rounded paws. Soft studio lighting from the upper left. Posed as: joyful mid-jump, both arms thrown up, huge happy smile, starry eyes. Buddy stands beside the phone, small-to-medium, celebrating. A top headline reading exactly "Know the real number, eating out or in" in deep orange (#E9843A). Below the phone, bold text reading exactly "Download BiteBuddy — free on the App Store", and a smaller line reading exactly "Search 'BiteBuddy: Ai calorie scanner'". Peach (#F4A261) accents. No other text, no watermark.

---

### Post 19 of 21 — `2026-07-26-slot1` — "3 years of failed tracking" (F3-i-was-wrong, 6 slides)


**Upload target:** commit each finished PNG into `Posts/2026-W30/2026-07-26-slot1/slides/` on branch `main`
of `clarson2706/BiteBuddyMVP`, named `01.png` … `06.png` (one image per slide, in order).
See the week's `CHATGPT-GENERATION-GUIDE.md` → "Uploading to GitHub" for the exact API call.
**Every image size:** exactly 1080 x 1350 pixels (4:5 vertical). No exceptions.
**Text:** render each headline EXACTLY as quoted — correct spelling, no extra words.
**Palette:** cream #FFF8F1 · peach #F4A261 · deep orange #E9843A · sage #8FA27F · lavender #C9C4F2.
**App UI appears on the FINAL slide only** — place the uploaded `today-home-hero.png` in the phone
silhouette exactly as-is. Every other slide is educational: food photography or clean type, no app UI.

Generate the slides in order, upload `01.png…` to `Posts/2026-W30/2026-07-26-slot1/slides/`, confirm each commit, then move on.
(Fallback if GitHub write isn't set up: return a `2026-07-26-slot1.zip` of the PNGs instead.)

## Slide 01 — COVER
On-slide text: "3 years of failed tracking · vs the week it finally clicked."

Vertical 4:5 editorial poster, exactly 1080 x 1350 pixels (4:5 vertical), warm cream (#FFF8F1) background. Big bold rounded headline across the top reading exactly "3 years of failed tracking" in deep orange (#E9843A). A smaller subtitle just below reading exactly "vs the week it finally clicked." in soft charcoal. A cute chubby round fuzzy monster mascot named BiteBuddy, soft 3D character render, Pixar-like, wholesome and friendly. Soft lavender / periwinkle purple fuzzy fur with subtle subsurface scattering. Two small smooth beige curved horns on top of the head. Large round glossy black eyes with bright white highlights. Small friendly mouth with two tiny lower fangs. Wearing an oversized cream knit hoodie with drawstrings and a front pocket. Short stubby legs with little clawed feet and small rounded paws. Soft studio lighting from the upper left. Posed as: sleepy and slumped, droopy tired eyes, one paw rubbing an eye, drained. Buddy sits SMALL in the lower third as a friendly host — he does not fill the frame. Lots of negative space, subtle peach (#F4A261) accent shapes. No app screenshots, no watermark, no drawn effects around Buddy.

## Slide 02 — PAIN
On-slide text: "Every app before made logging the hardest part of my day."

Vertical 4:5, exactly 1080 x 1350 pixels (4:5 vertical), warm cream (#FFF8F1) background. A clean typographic slide: a big bold rounded headline centered reading exactly "Every app before made logging the hardest part of my day." in deep orange (#E9843A). Generous negative space, subtle peach (#F4A261) and sage (#8FA27F) accent shapes in the corners. No mascot, no app UI, no watermark.

## Slide 03 — INSIGHT
On-slide text: "The best tracker is simply the one you'll actually keep using."

Vertical 4:5, exactly 1080 x 1350 pixels (4:5 vertical), warm cream (#FFF8F1) background. A clean typographic slide: a big bold rounded headline centered reading exactly "The best tracker is simply the one you'll actually keep using." in deep orange (#E9843A). Generous negative space, subtle peach (#F4A261) and sage (#8FA27F) accent shapes in the corners. No mascot, no app UI, no watermark.

## Slide 04 — SHIFT
On-slide text: "One that lets you snap the plate instead of typing it."

Vertical 4:5, exactly 1080 x 1350 pixels (4:5 vertical), warm cream (#FFF8F1) background. A clean typographic slide: a big bold rounded headline centered reading exactly "One that lets you snap the plate instead of typing it." in deep orange (#E9843A). Generous negative space, subtle peach (#F4A261) and sage (#8FA27F) accent shapes in the corners. No mascot, no app UI, no watermark.

## Slide 05 — PAYOFF
On-slide text: "One week in — logged every single day."

Vertical 4:5, exactly 1080 x 1350 pixels (4:5 vertical), warm cream (#FFF8F1) background. A clean typographic slide: a big bold rounded headline centered reading exactly "One week in — logged every single day." in deep orange (#E9843A). Generous negative space, subtle peach (#F4A261) and sage (#8FA27F) accent shapes in the corners. No mascot, no app UI, no watermark.

## Slide 06 — CTA — DOWNLOAD (only app slide)
On-slide text: "The one that finally clicks · Download BiteBuddy — free on the App Store"

Vertical 4:5, exactly 1080 x 1350 pixels (4:5 vertical), warm cream (#FFF8F1) background. THIS IS THE ONLY SLIDE THAT SHOWS THE APP. Centered: a clean, simple iPhone silhouette / phone frame containing the uploaded screenshot today-home-hero.png (the BiteBuddy 'Today' home screen) placed exactly as-is — do NOT redraw, recolor, crop out, or invent any UI. A cute chubby round fuzzy monster mascot named BiteBuddy, soft 3D character render, Pixar-like, wholesome and friendly. Soft lavender / periwinkle purple fuzzy fur with subtle subsurface scattering. Two small smooth beige curved horns on top of the head. Large round glossy black eyes with bright white highlights. Small friendly mouth with two tiny lower fangs. Wearing an oversized cream knit hoodie with drawstrings and a front pocket. Short stubby legs with little clawed feet and small rounded paws. Soft studio lighting from the upper left. Posed as: joyful mid-jump, both arms thrown up, huge happy smile, starry eyes. Buddy stands beside the phone, small-to-medium, celebrating. A top headline reading exactly "The one that finally clicks" in deep orange (#E9843A). Below the phone, bold text reading exactly "Download BiteBuddy — free on the App Store", and a smaller line reading exactly "Search 'BiteBuddy: Ai calorie scanner'". Peach (#F4A261) accents. No other text, no watermark.

---

### Post 20 of 21 — `2026-07-26-slot2` — "What actually matters on a nutrition label" (F4-one-snap-demo, 6 slides)


**Upload target:** commit each finished PNG into `Posts/2026-W30/2026-07-26-slot2/slides/` on branch `main`
of `clarson2706/BiteBuddyMVP`, named `01.png` … `06.png` (one image per slide, in order).
See the week's `CHATGPT-GENERATION-GUIDE.md` → "Uploading to GitHub" for the exact API call.
**Every image size:** exactly 1080 x 1350 pixels (4:5 vertical). No exceptions.
**Text:** render each headline EXACTLY as quoted — correct spelling, no extra words.
**Palette:** cream #FFF8F1 · peach #F4A261 · deep orange #E9843A · sage #8FA27F · lavender #C9C4F2.
**App UI appears on the FINAL slide only** — place the uploaded `today-home-hero.png` in the phone
silhouette exactly as-is. Every other slide is educational: food photography or clean type, no app UI.

Generate the slides in order, upload `01.png…` to `Posts/2026-W30/2026-07-26-slot2/slides/`, confirm each commit, then move on.
(Fallback if GitHub write isn't set up: return a `2026-07-26-slot2.zip` of the PNGs instead.)

## Slide 01 — COVER
On-slide text: "What actually matters on a nutrition label"

Vertical 4:5 editorial poster, exactly 1080 x 1350 pixels (4:5 vertical), warm cream (#FFF8F1) background. Big bold rounded headline across the top reading exactly "What actually matters on a nutrition label" in deep orange (#E9843A). A smaller subtitle just below reading exactly "Calories are the headline — but they're not the whole story." in soft charcoal. A cute chubby round fuzzy monster mascot named BiteBuddy, soft 3D character render, Pixar-like, wholesome and friendly. Soft lavender / periwinkle purple fuzzy fur with subtle subsurface scattering. Two small smooth beige curved horns on top of the head. Large round glossy black eyes with bright white highlights. Small friendly mouth with two tiny lower fangs. Wearing an oversized cream knit hoodie with drawstrings and a front pocket. Short stubby legs with little clawed feet and small rounded paws. Soft studio lighting from the upper left. Posed as: curious, one eyebrow raised, holding a small magnifying glass to one eye. Buddy sits SMALL in the lower third as a friendly host — he does not fill the frame. Lots of negative space, subtle peach (#F4A261) accent shapes. No app screenshots, no watermark, no drawn effects around Buddy.

## Slide 02 — TIP 1
On-slide text: "Calories: the headline, not the story"

Vertical 4:5, exactly 1080 x 1350 pixels (4:5 vertical), warm cream (#FFF8F1) background. Realistic, appetizing food photography of a nutrition label with the calorie number in focus, filling the top ~60% of the frame, natural soft light, no text baked into the food. Below the photo, a bold rounded headline reading exactly "Calories: the headline, not the story" in deep orange (#E9843A) on cream. No mascot, no app UI, no watermark. Clean editorial nutrition-post look.

## Slide 03 — TIP 2
On-slide text: "Protein: the number most people under-eat"

Vertical 4:5, exactly 1080 x 1350 pixels (4:5 vertical), warm cream (#FFF8F1) background. Realistic, appetizing food photography of a nutrition label with the protein line highlighted, filling the top ~60% of the frame, natural soft light, no text baked into the food. Below the photo, a bold rounded headline reading exactly "Protein: the number most people under-eat" in deep orange (#E9843A) on cream. No mascot, no app UI, no watermark. Clean editorial nutrition-post look.

## Slide 04 — TIP 3
On-slide text: "Fiber + added sugar tell you quality"

Vertical 4:5, exactly 1080 x 1350 pixels (4:5 vertical), warm cream (#FFF8F1) background. Realistic, appetizing food photography of a nutrition label with fiber and sugar lines highlighted, filling the top ~60% of the frame, natural soft light, no text baked into the food. Below the photo, a bold rounded headline reading exactly "Fiber + added sugar tell you quality" in deep orange (#E9843A) on cream. A small caption below reading exactly "not just quantity" in charcoal. No mascot, no app UI, no watermark. Clean editorial nutrition-post look.

## Slide 05 — TIP 4
On-slide text: "Ingredients: shorter usually means simpler"

Vertical 4:5, exactly 1080 x 1350 pixels (4:5 vertical), warm cream (#FFF8F1) background. Realistic, appetizing food photography of a product's ingredients list on the back of a package, filling the top ~60% of the frame, natural soft light, no text baked into the food. Below the photo, a bold rounded headline reading exactly "Ingredients: shorter usually means simpler" in deep orange (#E9843A) on cream. No mascot, no app UI, no watermark. Clean editorial nutrition-post look.

## Slide 06 — CTA — DOWNLOAD (only app slide)
On-slide text: "Know what matters — let AI do the reading · Download BiteBuddy — free on the App Store"

Vertical 4:5, exactly 1080 x 1350 pixels (4:5 vertical), warm cream (#FFF8F1) background. THIS IS THE ONLY SLIDE THAT SHOWS THE APP. Centered: a clean, simple iPhone silhouette / phone frame containing the uploaded screenshot today-home-hero.png (the BiteBuddy 'Today' home screen) placed exactly as-is — do NOT redraw, recolor, crop out, or invent any UI. A cute chubby round fuzzy monster mascot named BiteBuddy, soft 3D character render, Pixar-like, wholesome and friendly. Soft lavender / periwinkle purple fuzzy fur with subtle subsurface scattering. Two small smooth beige curved horns on top of the head. Large round glossy black eyes with bright white highlights. Small friendly mouth with two tiny lower fangs. Wearing an oversized cream knit hoodie with drawstrings and a front pocket. Short stubby legs with little clawed feet and small rounded paws. Soft studio lighting from the upper left. Posed as: joyful mid-jump, both arms thrown up, huge happy smile, starry eyes. Buddy stands beside the phone, small-to-medium, celebrating. A top headline reading exactly "Know what matters — let AI do the reading" in deep orange (#E9843A). Below the phone, bold text reading exactly "Download BiteBuddy — free on the App Store", and a smaller line reading exactly "Search 'BiteBuddy: Ai calorie scanner'". Peach (#F4A261) accents. No other text, no watermark.

---

### Post 21 of 21 — `2026-07-26-slot3` — "6 restaurant meals hiding a full day of calories" (F1-buddys-list, 8 slides)

**Upload target:** commit each finished PNG into `Posts/2026-W30/2026-07-26-slot3/slides/` on branch `main`
of `clarson2706/BiteBuddyMVP`, named `01.png` … `08.png` (one image per slide, in order).
See the week's `CHATGPT-GENERATION-GUIDE.md` → "Uploading to GitHub" for the exact API call.
**Every image size:** exactly 1080 x 1350 pixels (4:5 vertical). No exceptions.
**Text:** render each headline EXACTLY as quoted — correct spelling, no extra words.
**Palette:** cream #FFF8F1 · peach #F4A261 · deep orange #E9843A · sage #8FA27F · lavender #C9C4F2.
**App UI appears on the FINAL slide only** — place the uploaded `today-home-hero.png` in the phone
silhouette exactly as-is. Every other slide is educational: food photography or clean type, no app UI.

Generate the slides in order, upload `01.png…` to `Posts/2026-W30/2026-07-26-slot3/slides/`, confirm each commit, then move on.
(Fallback if GitHub write isn't set up: return a `2026-07-26-slot3.zip` of the PNGs instead.)

## Slide 01 — COVER
On-slide text: "6 restaurant meals hiding a full day of calories"

Vertical 4:5 editorial poster, exactly 1080 x 1350 pixels (4:5 vertical), warm cream (#FFF8F1) background. Big bold rounded headline across the top reading exactly "6 restaurant meals hiding a full day of calories" in deep orange (#E9843A). A smaller subtitle just below reading exactly "One dinner out can quietly erase a week of effort. Here's why." in soft charcoal. A cute chubby round fuzzy monster mascot named BiteBuddy, soft 3D character render, Pixar-like, wholesome and friendly. Soft lavender / periwinkle purple fuzzy fur with subtle subsurface scattering. Two small smooth beige curved horns on top of the head. Large round glossy black eyes with bright white highlights. Small friendly mouth with two tiny lower fangs. Wearing an oversized cream knit hoodie with drawstrings and a front pocket. Short stubby legs with little clawed feet and small rounded paws. Soft studio lighting from the upper left. Posed as: curious, one eyebrow raised, holding a small magnifying glass to one eye. Buddy sits SMALL in the lower third as a friendly host — he does not fill the frame. Lots of negative space, subtle peach (#F4A261) accent shapes. No app screenshots, no watermark, no drawn effects around Buddy.


## Slide 02 — FACT 1
On-slide text: "Shareable appetizers are portioned for the table"

Vertical 4:5, exactly 1080 x 1350 pixels (4:5 vertical), warm cream (#FFF8F1) background. Realistic, appetizing food photography of a loaded shareable restaurant appetizer platter, filling the top ~60% of the frame, natural soft light, no text baked into the food. Below the photo, a bold rounded headline reading exactly "Shareable appetizers are portioned for the table" in deep orange (#E9843A) on cream. No mascot, no app UI, no watermark. Clean editorial nutrition-post look.


## Slide 03 — FACT 2
On-slide text: "Restaurant pasta — often 2-3x a home portion"

Vertical 4:5, exactly 1080 x 1350 pixels (4:5 vertical), warm cream (#FFF8F1) background. Realistic, appetizing food photography of a large plate of creamy restaurant pasta, filling the top ~60% of the frame, natural soft light, no text baked into the food. Below the photo, a bold rounded headline reading exactly "Restaurant pasta — often 2-3x a home portion" in deep orange (#E9843A) on cream. No mascot, no app UI, no watermark. Clean editorial nutrition-post look.


## Slide 04 — FACT 3
On-slide text: "Poke bowls — the sauce and rice do the damage"

Vertical 4:5, exactly 1080 x 1350 pixels (4:5 vertical), warm cream (#FFF8F1) background. Realistic, appetizing food photography of a poke bowl with rice, fish, and drizzled sauce, filling the top ~60% of the frame, natural soft light, no text baked into the food. Below the photo, a bold rounded headline reading exactly "Poke bowls — the sauce and rice do the damage" in deep orange (#E9843A) on cream. No mascot, no app UI, no watermark. Clean editorial nutrition-post look.


## Slide 05 — FACT 4
On-slide text: "The free refill is the part nobody counts"

Vertical 4:5, exactly 1080 x 1350 pixels (4:5 vertical), warm cream (#FFF8F1) background. Realistic, appetizing food photography of a fast-food combo meal with burger, fries and a large soda, filling the top ~60% of the frame, natural soft light, no text baked into the food. Below the photo, a bold rounded headline reading exactly "The free refill is the part nobody counts" in deep orange (#E9843A) on cream. No mascot, no app UI, no watermark. Clean editorial nutrition-post look.


## Slide 06 — FACT 5
On-slide text: "Burrito bowls — double rice, double everything"

Vertical 4:5, exactly 1080 x 1350 pixels (4:5 vertical), warm cream (#FFF8F1) background. Realistic, appetizing food photography of a fully loaded burrito bowl with rice, beans, cheese and guacamole, filling the top ~60% of the frame, natural soft light, no text baked into the food. Below the photo, a bold rounded headline reading exactly "Burrito bowls — double rice, double everything" in deep orange (#E9843A) on cream. No mascot, no app UI, no watermark. Clean editorial nutrition-post look.

## Slide 07 — FACT 6
On-slide text: "Burger night — the fries are a second meal"

Vertical 4:5, exactly 1080 x 1350 pixels (4:5 vertical), warm cream (#FFF8F1) background. Realistic, appetizing food photography of a cheeseburger with a large side of golden fries, filling the top ~60% of the frame, natural soft light, no text baked into the food. Below the photo, a bold rounded headline reading exactly "Burger night — the fries are a second meal" in deep orange (#E9843A) on cream. No mascot, no app UI, no watermark. Clean editorial nutrition-post look.

## Slide 08 — CTA — DOWNLOAD (only app slide)
On-slide text: "Eat out without flying blind — snap the plate · Download BiteBuddy — free on the App Store"

Vertical 4:5, exactly 1080 x 1350 pixels (4:5 vertical), warm cream (#FFF8F1) background. THIS IS THE ONLY SLIDE THAT SHOWS THE APP. Centered: a clean, simple iPhone silhouette / phone frame containing the uploaded screenshot today-home-hero.png (the BiteBuddy 'Today' home screen) placed exactly as-is — do NOT redraw, recolor, crop out, or invent any UI. A cute chubby round fuzzy monster mascot named BiteBuddy, soft 3D character render, Pixar-like, wholesome and friendly. Soft lavender / periwinkle purple fuzzy fur with subtle subsurface scattering. Two small smooth beige curved horns on top of the head. Large round glossy black eyes with bright white highlights. Small friendly mouth with two tiny lower fangs. Wearing an oversized cream knit hoodie with drawstrings and a front pocket. Short stubby legs with little clawed feet and small rounded paws. Soft studio lighting from the upper left. Posed as: joyful mid-jump, both arms thrown up, huge happy smile, starry eyes. Buddy stands beside the phone, small-to-medium, celebrating. A top headline reading exactly "Eat out without flying blind — snap the plate" in deep orange (#E9843A). Below the phone, bold text reading exactly "Download BiteBuddy — free on the App Store", and a smaller line reading exactly "Search 'BiteBuddy: Ai calorie scanner'". Peach (#F4A261) accents. No other text, no watermark.

---

