# Illustrated Scene Backgrounds — Prompt Pack

*The art layer for the 7-slide narrative carousel. `MASTER-PROMPT-V6.md` emits six
`Scene_Brief` fields per row; this doc supplies the locked blocks those briefs are appended to.
Same pattern as `Brand-Assets/MASCOT_IMAGE_GEN_PROMPTS.md`: one master block, one character
lock, a short per-image line. Consistency comes from the locked blocks, never from the brief.*

## Where this applies, and where it does not

Illustrated backgrounds are for **narrative rows only**: Arc_Shape DAY-ARC and INVESTIGATION,
Visual_Recipe STORY-BEAT, TYPE-CARD, PHOTO-FACT.

Rows using RANK-CARD, CHEAT-GRID, COMPARE-SPLIT or QUIZ-CARD keep **real food photography**.
Those decks live or die on the food being real, and a stylized illustration of a burrito bowl
next to a real calorie number reads as a lie. Their scene briefs start with `PHOTO:`.

Slide 7 never gets an illustration. It is the real Today dashboard screenshot in a phone
silhouette with Buddy composited beside it.

## The standing rule this pack has to survive

`CLAUDE.md` bans AI-rendered food, and it is right to. The tell is photorealistic AI food:
uncanny sheen, impossible geometry, melted edges. The mitigation baked into every prompt here is
that these are **openly illustrated scenes about a person**, not fake photographs, and food is
always secondary set dressing rather than a hero close-up. If a generated scene starts looking
like a food photo, it has failed and gets regenerated.

`Research/HOOK-INTELLIGENCE-2026.md` also notes TikTok's July 2026 crackdown on faceless AI
health content. That is a real risk for this vertical. Rotate illustrated rows with real-photo
rows, never run a full week of illustrated decks, and keep the recurring character consistent so
the account reads as authored rather than generated.

---

## STEP 1 — Generate the character sheet FIRST

Generate this once. Keep the winner. Attach it as a reference image on every subsequent
generation. This is the step that prevents the mid-carousel style break, which is the single
most common failure in competitor decks.

```
Character reference sheet, single character, three-quarter view, standing relaxed, neutral warm
expression, plain flat light-grey background.

STYLE: Modern flat vector editorial illustration. Clean confident dark-brown outlines of even
weight around every form. Soft airbrushed cel shading with gentle gradients, painterly warm
light. Naturalistic adult human proportions and anatomy, realistic head-to-body ratio, NOT
chibi, NOT caricature, NOT anime. Muted naturalistic color palette with warm cream and sage
accents. Subtle film grain. The look of a high-end explainer-video still.

CHARACTER: A white woman in her late twenties. Warm fair skin with light freckles scattered
across her nose and cheeks. Shoulder-length wavy auburn hair worn in a loose low ponytail with
a few soft face-framing strands. Green eyes, soft rounded features, natural everyday build,
relaxed and healthy-looking. Small gold stud earrings.

WARDROBE, identical in every image: an oversized cream ribbed knit sweater with sleeves pushed
up to the forearms, and sage-green wide-leg trousers. No apron, no logos, no graphics on
clothing.

NEGATIVE: no text, no words, no letters, no logos, no watermarks, no UI elements, no phone
screens showing content, no distorted or extra fingers, no photorealism, no 3D render, no
purple monster character, no glamour or fashion-model styling, no extreme thinness.
```

Save the approved sheet to `Brand-Assets/scene-character/` and reference it by filename in the
week's manifest so a later batch can reproduce the same person.

## STEP 2 — MASTER BLOCK

Paste verbatim above every scene brief.

```
Same character, same illustration style, same wardrobe as the attached reference image.

STYLE: Modern flat vector editorial illustration. Clean confident dark-brown outlines of even
weight. Soft airbrushed cel shading, gentle gradients, painterly warm natural light.
Naturalistic adult proportions, NOT chibi, NOT anime. Muted naturalistic palette warmed toward
cream (#FFF8F1), soft peach (#F4A261) and sage green (#8FA27F). Subtle film grain.

CHARACTER: white woman, late twenties, warm fair skin with light freckles, shoulder-length wavy
auburn hair in a loose low ponytail, green eyes, natural everyday build. Wearing an oversized
cream ribbed knit sweater with sleeves pushed to the forearms and sage-green wide-leg trousers.

COMPOSITION: vertical portrait 4:5. Keep the TOP THIRD visually calm and uncluttered, open wall
or window light or sky, with no important detail there, because large headline text will be
placed over it. Keep the character and all key action within the central 80% of the frame.
Medium shot, eye level, cinematic but simple.

FOOD RULE: any food is loosely stylized and secondary to the person. Never a photorealistic
close-up of a dish. Food is set dressing, not the subject.

NEGATIVE: no text, no words, no letters, no numbers, no logos, no watermarks, no readable phone
or screen content, no distorted hands or extra fingers, no photorealism, no 3D render, no
purple monster character, no before-and-after framing, no scales or weighing scenes, no glamour
styling, no extreme thinness.
```

## STEP 3 — Append the row's Scene_Brief

One line, 12-30 words, action only. The master block already carries style, character, palette
and composition, so a brief that repeats any of those weakens the generation.

## Reference arc — DAY-ARC

The canonical six-scene sequence. Use it as the shape new DAY-ARC briefs are written against.

| Slide | Beat | Scene brief |
|---|---|---|
| 1 | Cover, morning | Sitting at a sunlit kitchen table holding a mug of coffee in both hands, looking calmly ahead, closed notebook and phone face-down beside her. |
| 2 | The list | Leaning over the kitchen counter writing a shopping list in a small notebook, phone beside her hand, fruit bowl soft at the edge of frame. |
| 3 | The store | Pushing a cart down a wide grocery aisle, reaching toward a shelf, softly abstracted unbranded packaging blurred behind her. |
| 4 | The label, the turn | Standing in the aisle holding up two similar unbranded packages, one in each hand, comparing them with a wry skeptical expression. |
| 5 | Cooking | At the counter in warm late-afternoon light, chopping vegetables on a wooden board, sleeves pushed up, absorbed and content, pan steaming behind. |
| 6 | The plate | Sitting at the table in warm evening light with a finished home-cooked plate, fork in hand, looking down with quiet satisfaction. |

Slide 4 is the turn, and in this arc it is the label comparison. Every DAY-ARC row needs its
own equivalent: the moment the character's assumption meets a number.

Optional slide 7 background, only if the CTA slide needs one behind the phone:

```
An empty, softly defocused warm kitchen at evening, plain wall, out-of-focus counter edge,
gentle lamp glow. No people, no food, no objects in the center of the frame. Very low detail
and low contrast, designed to sit behind a phone mockup and a character cutout. Large clear
calm area through the middle.
```

## Production notes

1. **Generate in order, 1 through 6**, reference attached every time. If a slide drifts,
   regenerate immediately rather than continuing. Drift compounds across a sequence.
2. **Aspect.** Most tools return 1024x1536 (2:3), taller than the 1080x1350 master. Crop to 4:5
   in Canva, which is why the master block keeps action in the central 80%.
3. **Slides 3 and 4 are the risk.** Grocery shelves are where models hallucinate legible text
   and fake brand logos. Reject any output with readable packaging.
4. **Never generate Buddy.** He is composited from
   `Brand-Assets/buddy-poses/transparent/`. An image model drawing him is what made him drift
   before.
5. **Hands.** Slides 2, 4 and 5 are hand-heavy. Check fingers before accepting.
6. Store approved scenes beside the deck they belong to, per the repo convention.
