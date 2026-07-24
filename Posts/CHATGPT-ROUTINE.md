# ChatGPT Sunday routine — generate + commit the week's images

This is the **image-generation half** of the weekly pipeline, run by a **ChatGPT
scheduled task**, connected to the **GitHub MCP** for `clarson2706/BiteBuddyMVP`.

## Pipeline (two routines, in order, every Sunday)
1. **~8:00am — Claude Code routine (`carousel-week`)** stages the upcoming week:
   writes the 21 posts' copy + prompts, the `CHATGPT-GENERATION-GUIDE.md`, the
   `assets/today-home-hero.png`, and refreshes `Posts/current-week.json`.
2. **10:00am — this ChatGPT routine** reads that pointer, generates every slide
   image, and commits each PNG into its post's `slides/` folder on `main`.

> The 10am routine must run **after** staging. If the pointer/guide isn't there
> yet, the routine stops cleanly (it does not invent content).

## Setup (one time)
- Connect ChatGPT to the **GitHub MCP** with **write access** to
  `clarson2706/BiteBuddyMVP` (Contents: read & write).
- Create a **ChatGPT scheduled task**: every **Sunday at 10:00am**, with the prompt below.

## The routine prompt (paste verbatim)

```
Every Sunday you generate this week's BiteBuddy carousel images and commit them to
GitHub. Repo: clarson2706/BiteBuddyMVP, branch: main. This repo is PRIVATE: use your
connected, AUTHENTICATED GitHub tool/connector for every read and write — never an
anonymous web request or unauthenticated fetch (those return 404 on a private repo).
The DEFAULT is to GENERATE. Only stop if step 1 truly fails, and if you stop, say the
exact reason — never reply a vague "nothing to generate."

1. Using your authenticated GitHub tool, read Posts/current-week.json (branch main).
   - If it 404s, that is almost always an ACCESS problem, not a missing file: your GitHub
     connection isn't authorized for this private repo. Reply "STOP: 404 reading
     current-week.json — GitHub connection likely not authorized for private repo
     clarson2706/BiteBuddyMVP" and stop. (As a check, also try reading the repo README.md;
     if that 404s too, it confirms an auth/scope problem, not a path problem.)
   - If you cannot read it for any other reason, reply "STOP: could not read
     current-week.json — <what you tried and the error>" and stop.
   - Otherwise take "week", "guide", "hero_asset", "week_dir" from it. THAT week is
     the target, even if it differs from today's calendar week. Never second-guess it
     and never decide it is "not this week."

2. Read the file at "guide" (that week's CHATGPT-GENERATION-GUIDE.md) — the COMPLETE
   spec: 21 posts, every slide's image prompt, the image size (1080x1350), the
   palette, and the exact commit path per slide. Also read "hero_asset"
   (today-home-hero.png): the ONLY screenshot, used unaltered inside a phone
   silhouette on each post's final "Download" slide, and nowhere else.

3. Generate and commit ALL 21 posts, one at a time, in order. IMPORTANT: a slides/
   folder that contains only ".gitkeep" is EMPTY — you still generate it. Do NOT treat
   an existing .gitkeep (or any existing file) as "already done." For each post:
   generate every slide at exactly 1080x1350 px per its prompt, name them
   01.png, 02.png, ... in slide order, and commit each PNG to
   Posts/<week>/<post-id>/slides/NN.png on branch main using your GitHub
   tools (create-or-update; overwriting .gitkeep or an existing file is fine and
   expected). Confirm each commit before the next post.

4. Never generate or invent app UI — only the final slide shows the app, via
   today-home-hero.png in a phone frame. No medical/weight-loss claims. Never feature
   a "Meal Advisor". Never print, echo, or store any GitHub token.

5. When all 21 posts are committed, reply one line per post ("<post-id>: N slides
   committed") then the single word: done. If you had to stop, report the exact step
   and reason instead.
```

## Notes / troubleshooting
- **404 reading `current-week.json` (or any repo path):** the file IS on `main` — a 404
  means ChatGPT's GitHub connection can't SEE this private repo (GitHub returns 404, not
  403, for private resources you're not authorized for). Fix the connection, not the repo:
  - **Fine-grained PAT:** under *Repository access* it must explicitly include
    `clarson2706/BiteBuddyMVP` (the default "only select repositories → none" gives 404),
    with *Contents: Read and write*.
  - **GitHub App / OAuth connector:** the installation must be granted this specific repo
    (org/personal installs don't auto-include every repo), on the account that owns/collaborates on it.
  - Make sure ChatGPT uses its **authenticated** GitHub tool for reads, not an anonymous
    web fetch. Quick isolation test — paste to ChatGPT: *"Using your GitHub tools, read
    `README.md` and `Posts/current-week.json` from `clarson2706/BiteBuddyMVP`
    on `main`; report the HTTP status of each."* Both 404 → auth/scope; only the JSON
    404s → path/branch.
- **"nothing to generate" / early stop:** the prompt removes the two things that caused it
  — (a) a `.gitkeep` in an otherwise-empty `slides/` folder read as "already done," and
  (b) second-guessing the pointer's week against the model's own calendar.
- The pointer (`current-week.json`) is the single source of truth for "which week." If
  it's ever missing, the target is the newest `Posts/<ISO-week>/` folder.
- Nothing here publishes to social — posting is the separate `carousel-publish` step
  that runs after the images land and Connor confirms.
