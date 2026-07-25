# Brand-Assets

Canonical BiteBuddy brand assets, copied out of the iOS app so media work never depends
on cloning the app repo.

```
buddy-poses/
  source/         the 13 poses exactly as shipped in the app (RGB, white bg)
  transparent/    RGBA cutouts — use these for every slide composite
  README.md       what each pose means and when to use it
MASCOT_IMAGE_GEN_PROMPTS.md   MASTER STYLE BLOCK + pose lines, only for new poses
```

Source of truth is the app: `BiteBuddyMVP/Resources/Assets.xcassets/buddy_*.imageset/`.
Copied 2026-07-25 from commit `d563f6a`. If Buddy's design changes in the app, re-copy
and regenerate the cutouts.

**Brand palette** (also in `Content-Engine/DESIGN-SYSTEM.md`): cream `#FFF8F1` ·
peach `#F4A261` · deep orange `#E9843A` · sage `#8FA27F` · lavender `#C9C4F2` (Buddy's).
