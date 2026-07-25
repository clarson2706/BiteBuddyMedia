# BiteBuddy Mascot — Image Generation Prompt Pack

Give these to an image-generation model (Midjourney, DALL·E, Nano Banana / Gemini, Ideogram, Flux, etc.).
You'll get back one PNG per pose. Paste them here and Fable will animate + cross-fade them with
code-driven motion (bounce, squash, blink, auras, particles, haptics, glass).

## How to use this (read first — it determines whether they animate cleanly)

1. **Generate `buddy_idle` FIRST.** That's the canonical character. Once you have one you love, use it as
   a **reference / style image** for every other pose (most tools let you attach a reference). Change ONLY
   the pose and expression each time. This is the #1 thing that keeps the set consistent.
2. **Effects are NOT in the art.** Do not let the model draw lightning, fog, shields, sparkles, confetti,
   glows, or auras. The character body + face only. Fable adds every effect in code. (Only exception:
   the magnifying-glass prop in `buddy_warning_check`.)
3. **Transparent background (PNG with alpha).** If the tool can't do transparent, use a flat plain
   background and remove it afterward (e.g. remove.bg). A baked background will ruin compositing.
4. **Identical framing every time** — same camera distance, same eye level, character centered, occupying
   the same share of the frame. Cross-fades between poses look broken if scale/position drifts.
5. **Square canvas, high res** (1:1, 2048×2048 if available). No text, no logos, no hard cast shadow.

## MASTER STYLE BLOCK — paste this at the top of EVERY generation

```
A cute chubby round fuzzy monster mascot named BiteBuddy, soft 3D character render, Pixar-like,
wholesome and friendly. Soft lavender / periwinkle purple fuzzy fur with subtle subsurface scattering.
Two small smooth beige curved horns on top of the head. Large round glossy black eyes with bright white
highlights. Small friendly mouth with two tiny lower fangs. Wearing an oversized cream knit hoodie with
drawstrings and a front pocket. Short stubby legs with little clawed feet and small rounded paws.
Soft studio lighting from the upper left, gentle and even. Full body, front-facing, centered, character
fills a consistent portion of the frame. Transparent background. Square 1:1 composition. No text.
Clean, no drawn effects around the character.
```

## PER-POSE PROMPTS

Append each line below to the MASTER STYLE BLOCK. Filename must match exactly (the app already references
these names).

| Filename | Pose + expression line to append |
|---|---|
| `buddy_idle` | *(base/reference)* Standing relaxed and neutral, arms resting at sides, soft gentle closed-mouth smile, calm eyes looking forward. |
| `buddy_happy` | Cheerful and warm, one paw raised in a small friendly wave, slight head tilt, big open happy smile, bright eyes. |
| `buddy_protein_powerup` | Confident strongman flex, both arms bent up with little fists raised, determined proud grin, energetic upright posture. |
| `buddy_sugar_lightning` | Over-excited and jittery, wide sparkling eyes, big open grin, both arms flung up energetically, bouncy hyper posture. *(No lightning drawn.)* |
| `buddy_sugar_crash` | Sleepy and slumped, half-closed droopy tired eyes, small tired mouth, leaning slightly to one side, one paw rubbing an eye, content but drained. |
| `buddy_fiber_shield` | Calm and grounded, steady confident smile, one paw giving a clear thumbs-up, settled stance. *(No shield drawn.)* |
| `buddy_balanced_glow` | Serene and peaceful, softly relaxed content smile, eyes gently closed, paws loosely clasped, harmonious. *(No glow drawn.)* |
| `buddy_heavy_meal` | Full and satisfied, leaning back a little, rounder relaxed belly, one paw resting on tummy, puffed cheeks, heavy content sleepy-satisfied smile. Not sad — cozy and full. |
| `buddy_sodium_fog` | Squinting with scrunched eyes, one paw raised near the face as if gently waving something away, slightly puckered mouth, mildly bothered but friendly. *(No fog drawn.)* |
| `buddy_warning_check` | Curious and inquisitive, one eyebrow raised, holding a small round magnifying glass up in front of one eye, friendly "let me check this" expression. *(Magnifying glass IS included.)* |
| `buddy_goal_celebration` | Joyful mid-jump, both arms thrown up, huge open happy smile, bright starry excited eyes, celebratory leap. *(No confetti drawn.)* |
| `buddy_level_up` | Triumphant heroic pose, fists raised or arms up, proud confident beaming expression, chin up looking slightly upward, victorious. *(No star burst drawn.)* |
| `buddy_thinking` | Thoughtful and curious, one paw on chin, head tilted slightly up, small "hmm" pondering expression, eyes looking up. |

## Optional — extra frames for extra life (nice-to-have, not required)

If your tool keeps the character consistent enough, generating a couple of variant frames lets Fable do
true frame animation instead of just cross-fades:

- `buddy_idle_blink` — same as `buddy_idle` but **eyes fully closed** (for blinking).
- `buddy_idle_mouth_open` — same as `buddy_idle` but **mouth slightly open** (for idle "talking"/breathing).

Skip these if consistency is hard to hold — the 13 core poses are enough for a great result.

## Delivery checklist (what to paste back here)

- [ ] 13 PNGs named exactly as above (`buddy_idle`, `buddy_happy`, … `buddy_thinking`).
- [ ] Transparent backgrounds.
- [ ] Same framing/scale/lighting across all of them.
- [ ] No baked effects (except the magnifying glass).

Once you paste them, Fable adds them to `BiteBuddyMVP/Resources/Assets.xcassets`, wires each to its
`AvatarReactionType`, and builds all the motion on top.
