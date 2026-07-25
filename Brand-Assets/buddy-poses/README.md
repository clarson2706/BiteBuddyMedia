# Buddy poses — the 13 in-app reaction renders

Copied from the iOS app on 2026-07-25 (`BiteBuddyMVP` →
`BiteBuddyMVP/Resources/Assets.xcassets/buddy_*.imageset/`, commit `d563f6a`). **These
are the canonical Buddy.** Use them instead of generating Buddy with an image model —
that is what made him drift between posts.

## What "animations" means here

There are no Lottie files, GIFs, or video. Buddy's in-app animation is **SwiftUI motion
applied to these static renders** — scale, bob, shake, and effect overlays driven by
`Features/Avatar/AvatarReaction.swift` and `AvatarEffects.swift`, with a low/medium/high
intensity for the macro-driven reactions. So for media work, these 13 stills *are* the
asset; any motion is something we add in the editor.

## Two versions

| Folder | What | Use |
|---|---|---|
| `source/` | Exactly as shipped in the app: **1254×1254, RGB, near-white background, no alpha** | Reference / re-cutting |
| `transparent/` | **RGBA cutouts, background removed, trimmed to the subject** | Everything we actually composite |

Use `transparent/`. The source files have a near-white (#F2–#FE) background that leaves a
visible white box when dropped onto our cream `#FFF8F1` slides. The cutouts were made by
keying the neutral bright background only — the cream hoodie is bright but strongly
non-neutral, so it survives intact — then eroding 1px and feathering to kill the halo.
Verified against cream; no fringe, no holes.

Cutouts are trimmed to their bounding box, so sizes vary (≈820–1205 × 980–1113). Position
by the *feet*, not the frame, when placing Buddy on a slide.

## The 13 poses

| File | Pose | In-app trigger | Good for |
|---|---|---|---|
| `buddy_idle` | Neutral idle (breathing/bob) | default state | filler, neutral covers |
| `buddy_happy` | Happy wave | greeting, Today home | covers, welcome beats |
| `buddy_thinking` | Paw on chin, analyzing | scan analyzing | "here's the catch" beats, quiz question slides |
| `buddy_warning_check` | Magnifying-glass inspector | result needs review | reality-check and hidden-calorie covers |
| `buddy_goal_celebration` | Confetti leap | daily goal hit | CTA slides, payoff slides |
| `buddy_level_up` | Triumphant hero pose | streak / XP level-up | streak and habit content |
| `buddy_protein_powerup` | Double-arm flex | high-protein meal | protein rankings, P3 Bulker content |
| `buddy_fiber_shield` | Confident thumbs-up | good fiber | "solid choice" reactions, fiber content |
| `buddy_sugar_lightning` | Buzzing with sparks | high sugar | hidden-sugar reveals |
| `buddy_sugar_crash` | Wiped out | sugar crash | energy-fade and crash explainers |
| `buddy_sodium_fog` | Foggy / hazy | high sodium | sodium reveals |
| `buddy_heavy_meal` | Paw on belly, full | large meal | heavy-meal and portion content |
| `buddy_balanced_glow` | Serene zen glow | balanced day | calm payoffs, kind-tone closers |

The old `UI-Library/10-buddy-poses/README.md` claimed 14 poses. There are 13 — that
folder listed a set that was never exported and has been replaced by this one.

## Usage rules (from `Content-Engine/DESIGN-SYSTEM.md`)

- Buddy hosts the **cover** and the **CTA slide**. He does not appear on every slide —
  the food, the number, and the fact carry the body slides.
- He sits **small, in the lower third**, as a host. He never fills the frame.
- **No drawn effects.** Sparkles, confetti, and glow are composited in the editor to
  match the in-app effect language — never baked into the render or prompted from a
  model.
- Match the pose to the post's emotional beat (table above). A sugar-reveal post closing
  on `buddy_balanced_glow` reads wrong.

## If a new pose is ever needed

`Brand-Assets/MASCOT_IMAGE_GEN_PROMPTS.md` holds the MASTER STYLE BLOCK and the pose
lines. Keep framing identical to these 13 so he stays consistent. Prefer reusing one of
the 13 — a generated Buddy next to a rendered Buddy is visible.
