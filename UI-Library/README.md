# BiteBuddy UI Library

**A living, organized home for every BiteBuddy UI screenshot** — so that when we
build marketing videos (Higgsfield, App Store, ads), the right, *current* screen
image is always one click away.

This exists because raw screenshots go stale the moment the UI changes. Keep
this library current and we never have to guess which capture is up to date.

---

## How to use this (the update workflow)

1. **You:** capture screenshots on-device (any quantity, any names — messy is
   fine) and drop them all into [`_INBOX/`](./_INBOX/).
2. **You:** tell me "I added screenshots" (mention roughly what they are if you
   can — it speeds up sorting).
3. **Me (Claude):** I rename each to the convention below, move it into the
   correct subfolder, replace any older version of the same screen, delete exact
   duplicates, and update the status in this README's manifest. If I can't tell
   what a screenshot is, I'll ask you rather than guess.
4. **When we make a video:** I pull the exact files listed in each concept's
   shot list straight from these folders and hand them to Higgsfield.

**Updating a screen after a UI change:** just drop the new capture in `_INBOX/`
and say which screen it's for. I overwrite the old file in place (same filename),
so every video script keeps pointing at the same path — no broken references.

---

## Naming convention

```
NN-screen-name.png                 e.g.  02-today-home.png
NN-screen-name--state.png          e.g.  02-today-home--rings-full.png
```

- `NN` = the folder's two-digit prefix, so files sort in app-flow order.
- `screen-name` = lowercase kebab-case, matches the manifest below.
- `--state` (optional) = a variant of the same screen: `--empty`, `--rings-full`,
  `--dark`, `--heavy-meal`, `--pro-active`, etc. Use when we want more than one
  capture of the same screen.
- PNG, native device resolution, **light mode** unless the filename says `--dark`.
- Status bar: fine as-is on device; if using the simulator, set the clock to 9:41.

---

## Folder map

| Folder | What lives here |
|---|---|
| [`_INBOX/`](./_INBOX/) | **Drop zone.** Unsorted new screenshots. Should be empty after I process it. |
| [`Recordings/`](./Recordings/) | **Full-UI screen recordings** (Git LFS). Preferred over stills for video — see its README. |
| [`01-onboarding-auth/`](./01-onboarding-auth/) | Welcome, goal, basics, plan, tutorial, sign in/up, legal gate |
| [`02-today-home/`](./02-today-home/) | Today tab — buddy hero, macro rings, streak, XP details |
| [`03-scan-capture/`](./03-scan-capture/) | Scan tab — all 5 capture modes, analyzing, saved foods |
| [`04-food-result/`](./04-food-result/) | The AI result/review screen + its edit sheets |
| [`05-log-diary/`](./05-log-diary/) | Log tab — food diary, food detail |
| [`06-progress-weight/`](./06-progress-weight/) | Progress tab — weight trend chart, log-weight sheet |
| [`07-reports/`](./07-reports/) | Weekly + monthly reports |
| [`08-profile-settings/`](./08-profile-settings/) | Profile, personal plan editor, account |
| [`09-paywall-pro/`](./09-paywall-pro/) | Pro paywall + Pro-active state |
| ~~`10-buddy-poses/`~~ | Moved to [`Brand-Assets/buddy-poses/`](../Brand-Assets/buddy-poses/) — 13 poses, source + RGBA cutouts |

---

## Master manifest — what we have vs. what we still need

> **Starting set:** the 7 screens marked `[x]` below were imported from the
> app's existing captures in `Docs/app-store-screenshots/` and
> `Docs/review-screenshots/`. A few carry a black Dynamic-Island privacy blob
> or minor QA state — fine as reference/framed footage; recapture clean versions
> anytime by dropping them in `_INBOX/`.


Legend: **Status** `[ ]` = missing · `[x]` = captured & filed.
**⭐** = high-priority (used across multiple video concepts).
**Video** column = which of the 5 launch concepts uses it (see
`VIDEO-CONCEPTS.md` if present, or the report in chat).

### 01 — Onboarding & Auth
| ⭐ | Screen | Target file | Video | Status |
|---|---|---|---|---|
|   | Welcome ("Meet your food buddy") | `01-welcome.png` | — | [ ] |
|   | Goal select ("What's your goal?") | `02-goal-select.png` | — | [ ] |
|   | Basics (age/sex/height/weight) | `03-basics.png` | — | [ ] |
|   | Goal weight + timeline | `04-goal-weight.png` | — | [ ] |
| ⭐ | Daily plan payoff ("Your daily plan") | `05-daily-plan.png` | C3,C4 | [x] |
|   | Pro benefits teaser | `06-pro-benefits.png` | — | [ ] |
|   | Tutorial / coach-mark | `07-tutorial.png` | — | [ ] |
|   | Sign in | `08-auth-signin.png` | — | [ ] |
|   | Sign up | `09-auth-signup.png` | — | [ ] |
|   | Legal acceptance gate | `10-legal-acceptance.png` | — | [x] |

### 02 — Today / Home
| ⭐ | Screen | Target file | Video | Status |
|---|---|---|---|---|
| ⭐ | Today home — buddy hero + rings partial | `01-today-home.png` | C1,C3,C4,C5 | [x] |
| ⭐ | Today home — rings full + celebration | `01-today-home--rings-full.png` | C2,C5 | [ ] |
|   | Today's Nutrition detail | `02-todays-nutrition.png` | — | [x] |
| ⭐ | Your Streak detail | `03-your-streak.png` | C1,C5 | [x] |
|   | XP & Levels detail | `04-xp-levels.png` | C1,C5 | [x] |
|   | Macro rings close-up | `05-macro-rings.png` | C2 | [ ] |
| ⭐ | Buddy reaction detail ("Why Buddy feels this way") | `06-buddy-reaction-detail.png` | C5 | [x] |

### 03 — Scan & Capture
| ⭐ | Screen | Target file | Video | Status |
|---|---|---|---|---|
| ⭐ | Scan home — current (Camera, Voice, Type, Saved) | `01-scan-home.png` | C3 | [x] |
| ⭐ | Camera viewfinder on a meal (Photo mode) | `02-camera-viewfinder.png` | C1,C2,C3,C4 | [x] |
|   | Photo preview ("Use Photo?") | `03-photo-preview.png` | C1,C2 | [x] |
| ⭐ | Analyzing ("Buddy is thinking") | `04-analyzing.png` | C1,C2 | [x] |
|   | AI consent sheet | `05-ai-consent.png` | — | [ ] |
|   | Camera permission | `06-camera-permission.png` | — | [ ] |
| ⭐ | Camera in Barcode mode (switcher on the scan screen) | `02-camera-viewfinder--barcode.png` | C3 | [x] |
| ⭐ | Camera in Label mode (switcher on the scan screen) | `02-camera-viewfinder--label.png` | C3 | [x] |
| ⭐ | Voice entry | `09-voice-entry.png` | C3 | [ ] |
|   | Text description entry | `10-text-entry.png` | — | [ ] |
|   | Manual entry | `11-manual-entry.png` | — | [ ] |
| ⭐ | Saved foods / go-tos | `12-saved-foods.png` | C3 | [ ] |
|   | Search foods | `13-search-foods.png` | — | [ ] |
|   | Create / edit saved item | `14-create-saved-item.png` | — | [ ] |

### 04 — Food Result (the magic screen)
| ⭐ | Screen | Target file | Video | Status |
|---|---|---|---|---|
| ⭐ | Food result — itemized macros | `01-food-result.png` | C1,C2,C4,C5 | [x] |
|   | Food result — variant (Impact bars + salty note) | `01-food-result--turkey-impact.png` | C2,C4 | [x] |
|   | Detailed Impact sheet | `02-detailed-impact.png` | — | [ ] |
|   | Edit Meal Totals sheet | `03-edit-meal-totals.png` | — | [ ] |
|   | Improve Estimate sheet | `04-improve-estimate.png` | — | [ ] |
|   | Edit Food sheet | `05-edit-food.png` | — | [ ] |

### 05 — Log / Diary
| ⭐ | Screen | Target file | Video | Status |
|---|---|---|---|---|
|   | Log diary (day view) | `01-log-diary.png` | C4 | [ ] |
|   | Food detail | `02-food-detail.png` | — | [ ] |

### 06 — Progress / Weight
| ⭐ | Screen | Target file | Video | Status |
|---|---|---|---|---|
|   | Progress trend (chart + goal line) | `01-progress-trend.png` | — | [x] |
|   | Log weight sheet | `02-log-weight.png` | — | [ ] |

### 07 — Reports
| ⭐ | Screen | Target file | Video | Status |
|---|---|---|---|---|
|   | Weekly report (buddy's read) | `01-weekly-report.png` | — | [x] |
|   | Weekly report — "Try this next" 3 steps | `01-weekly-report--next-steps.png` | — | [x] |
|   | Monthly report (Pro) | `02-monthly-report.png` | — | [ ] |

### 08 — Profile / Settings
| ⭐ | Screen | Target file | Video | Status |
|---|---|---|---|---|
|   | Profile | `01-profile.png` | — | [ ] |
|   | Personal plan editor | `02-personal-plan.png` | — | [ ] |
|   | Delete account | `03-delete-account.png` | — | [ ] |

### 09 — Paywall / Pro
| ⭐ | Screen | Target file | Video | Status |
|---|---|---|---|---|
|   | Paywall (annual/monthly/trial) | `01-paywall.png` | — | [x] |
|   | Pro active / unlocked | `02-pro-active.png` | — | [ ] |

### 10 — Buddy poses (mascot overlays)
14 transparent PNGs, one per in-app reaction. See that folder's README for the
full list and which video beats each pose serves. Status tracked there.

---

## Notes / guardrails for video use

- **No claims** beyond the approved caption bank — no "lose X lbs," "guaranteed,"
  or medical language (see `Legal/MEDICAL_AND_NUTRITION_DISCLAIMER.md`).
- **Meal Advisor is "Coming Soon"** and disabled — do **not** feature it as a
  live screen in videos. No folder is allocated for it here for that reason.
- **Barcode & Label are camera modes, not home cards:** the scan home surfaces
  Camera / Voice / Type; **Barcode and Label are a switcher inside the camera
  scan screen.** Capture them as `02-camera-viewfinder--barcode.png` /
  `--label.png` by switching modes in the viewfinder. Concept 3's "5 ways"
  (Photo, Barcode, Label, Voice, Type) still holds.
- Brand colors for any framing/backgrounds live in
  `BiteBuddyMVP/Core/DesignSystem/DesignSystem.swift` (peach `#F4A261`, deep
  orange `#E9843A`, sage `#8FA27F`, lavender `#C9C4F2`, cream `#FFF8F1`).
