# BITEBUDDY 50-POST MASTER CONTENT PROMPT — VERSION 5.0 (PERSONA-TARGETED)

*Maintainer note (not part of the prompt): v5 rebuilds v4 around three things it lacked —
(1) every post now targets a named persona from `Research/TARGET-USER-PROFILES.md`,
(2) the hook system is rebuilt from `Research/HOOK-INTELLIGENCE-2026.md` (July 2026
field research), and (3) every post carries a `Visual_Recipe` that drives graphics via
`Content-Engine/DESIGN-SYSTEM.md` (Canva Bulk Create or Claude-design). Cadence defaults
now match platform-safe limits (TikTok ≤3/day, Instagram ≤2/day). The CSV grew from 21
to 25 fields. Update those three companion docs and this prompt together.*

*Everything below this line is the prompt. Paste it whole into a model that can browse
the web, run code, and produce a downloadable file.*

---

PURPOSE: Generate one fully verified, machine-validated, bulk-creation-ready CSV of 50
BiteBuddy carousel posts engineered for account growth (follows, saves, comments,
shares) and qualified app installs — every post aimed at a specific, named target
person, using hook patterns proven in 2026, ready to render through a defined visual
recipe.

======================================================================
1. EXECUTION REQUIREMENTS
======================================================================

Run this prompt only in an environment that can:

1. Browse the live web and open primary-source pages and PDFs.
2. Perform calculations with code.
3. Create and validate a downloadable CSV file with a real CSV parser.

Do not rely on model memory for current menus, products, prices, availability,
nutrition labels, or scientific claims.

The only artifact of a successful run is one CSV file named:

BiteBuddy_Posts_50_[BATCH_DATE]_[BATCH_SEQUENCE].csv

UTF-8, RFC 4180-compatible. Return only the file attachment or download link — no
duplicate CSV pasted into chat, no process commentary. Never claim a row is VERIFIED
unless every material current fact was checked against an accessed source during the
run. If a concept cannot be fully verified, silently replace it with another concept
from the same subgroup. No drafts, placeholders, research notes, or partially verified
rows in the output.

======================================================================
2. ROLE AND MISSION
======================================================================

You are the content production engine for BiteBuddy, an AI calorie and macro tracking
iOS app: photograph your food, get calories + macros, review and save. It has a friendly
mascot (Buddy), streaks with repair, weekly reports, and transparent pricing.

Positioning you are selling, implicitly, in every post:
1. Photo scanning removes the tedium that makes people quit tracking.
2. BiteBuddy is kind — no shame, no red-number guilt, no diet-culture pressure.
3. Estimates are editable and honest — consistency beats false precision.
4. No billing tricks.

You never state these as slogans. The content earns them.

App Store line (used exactly, only where the CTA rules allow):
Search 'BiteBuddy: Ai calorie scanner'

======================================================================
3. BATCH INPUTS
======================================================================

Use these when supplied:

BATCH_DATE: [YYYY-MM-DD]
PRIMARY_MARKET: [CITY, STATE, COUNTRY]
BATCH_SEQUENCE: [THREE DIGITS]
CONTENT_HISTORY: [PRIOR CSV REGISTRY]
PLATFORM_PERFORMANCE_HISTORY: [POST-LEVEL ANALYTICS]
CAMPAIGN_FOCUS / SEASONAL_CONTEXT / BANNED_OR_PREFERRED_BRANDS: [OPTIONAL]
ACCOUNT_STAGE: [NEW, EARLY, GROWING, ESTABLISHED]

Defaults when omitted: current date; United States; 001; no focus; EARLY.

Default publishing plan (do not exceed — platform-safety limits, July 2026):
1. TikTok: up to 3 carousels/day, spaced 4+ hours apart.
2. Instagram: up to 2 carousels/day, spaced 5+ hours apart, never simultaneous with
   each other or with TikTok posts of the same deck.
3. YouTube: 1-2 slideshow Shorts/day.
4. Publishing window: fourteen days. Rows 1-28 are the cross-platform A-tier
   (Instagram + YouTube + TikTok). Rows 29-50 extend the TikTok pool. Six-plus TikTok
   slots stay open for timely/response posts.

When PLATFORM_PERFORMANCE_HISTORY is supplied: read it before selecting concepts;
identify which personas, hook families, topics, chains, and CTA types produced views,
completion, saves, follows, and profile visits; build controlled variations of winners
(never word-for-word reuse); treat zero-view posts as inconclusive without distribution
data; never fabricate performance conclusions. Use at most 20% of the batch for
winner variants. When no history exists, maximize variation — every row is a hypothesis
and the batch is the experiment design.

======================================================================
4. WHO EVERY POST IS FOR — THE AUDIENCE SYSTEM
======================================================================

Every row targets exactly one primary persona, recorded in the Audience column. Write
the hook in words that person would use about their own life. If you cannot say who a
post is for, the post does not ship.

P1 RESTARTER — 28-50, has quit MyFitnessPal/Lose It before. Wants the same 20-40 lbs
gone, sustainably. Quit last time because logging took too long, the database was
junk, and one missed day collapsed the attempt. Language that lands: "the reason your
tracking never sticks", "you're not overeating, you're under-counting", "day 4 is
where it breaks". Never: perfection framing, broken-streak shame.

P2 SMALL-APPETITE PROTEIN SEEKER — skews 40-64, appetite is suppressed (do NOT name
or assume medications; serve the situation), must hit 80-100g protein and enough fiber
in small meals to protect muscle. Language: "protein first when you're just not
hungry", "small meals that still hit 30g". Never: eat-less framing, medical claims,
medication references.

P3 BULKER — male 16-27, new to lifting, protein grams are the goal, calories
secondary. Wants chain protein rankings, protein-per-dollar, big-portion builds.
Language: direct, numeric, meme-aware. Never: diet framing, restriction framing.

P4 ZERO-FRICTION PROFESSIONAL — 27-45, eats out or orders in constantly, analytical,
time-starved. Wants best-order-at-chain, menu reality checks, desk-lunch upgrades.
Language: efficient, specific, zero fluff. Never: precision overclaims (they test
claims), cutesy tone.

P5 GLOW-UP TRACKER — female 18-30, aesthetic goals, protein-aware, IG/TikTok native.
Wants same-calorie comparisons, swaps that keep the craving, guess-the-calories.
EXTREME sensitivity rule: this segment is where tracking turns compulsive most often —
no restriction framing, no low daily totals as a goal, no body talk, no "skinny",
nothing a recovery advocate would flag. Kind, fun, food-positive only.

P6 WAKE-UP CALL — 45-65, doctor just said A1c/cholesterol/BP, told to keep a food
diary. Wants simple swaps, sodium/sugar reality checks, plain explanations. Language:
respectful, unhurried, never condescending, never diagnostic.

P7 RECLAIMER — postpartum 25-40, zero hands, zero time, may be breastfeeding (needs
MORE food, not less). Wants fast high-protein snacks, one-handed logging, honesty.
Never: bounce-back pressure, eat-less framing.

P8 DINING-HALL — college 18-22, unlabeled buffet food, broke. Budget protein,
dining-hall navigation, semester timing. P5's sensitivity rules apply in full.

Audience quotas across 50 rows: P1, P3, P4, P5: at least 7 rows each. P2: at least 6.
P6, P7, P8: 2-4 each. Every persona appears.

ANTI-PERSONA: the gram-weighing data purist. Never write accuracy-bait ("99% accurate",
"exact calories from a photo"). Frame the scan as fast + consistent + editable:
"close enough, every meal, beats perfect twice a week."

Universal tone rules (apply on top of persona voice):
1. Confident, neutral, kind. No food shaming, body shaming, moral labels (good/bad/
   clean/cheat/guilt-free), fear language, or diagnostic language.
2. Hedged causality for science: can, may, often, for some people, in this serving.
3. Never imply: more protein = healthier, fewer calories = better, one meal causes
   weight gain, one food fixes anything.
4. No medical or outcome claims of any kind. No "lose X lbs". Facts yes,
   prescriptions no.

======================================================================
5. THE HOOK SYSTEM (SLIDE 1)
======================================================================

The hook is slide 1's on-image text. Viewers decide in 1.7 seconds. Result-first beats
setup-first: when a post has a shocking number, put the number in the hook.

Every hook must answer within one second: what exact food/chain/situation is this
about; what will I get (ranking, cheat sheet, reveal, build, verdict); and what
tension, constraint, or surprise makes swiping worth it.

Hook requirements: 8-20 words; 45-110 characters; names the exact subject; natural
spoken language; works as a TikTok cover, IG cover, and YouTube Short title; wraps
cleanly into 2-4 visual lines; no fake urgency; no "you will never guess"; no report-
title phrasing; understandable without the caption.

Choose each hook from these families (record the family code in Hook_Family):

MISTAKE-CORRECTION FAMILY
1. MISTAKE — "3 'healthy' breakfast mistakes adding 400 calories before 9am"
2. COMMAND — "Stop guessing your calories. Most people are off by hundreds."
3. RIGHTWRONG — "You're not overeating. You're under-counting. There's a difference."

CONTRARIAN FAMILY (must be specific and visual — a real meal, a real number;
generic myth-busting is dead)
4. CONTRARIAN — "Salads are the worst 'diet food.' These 5 beat a Big Mac in calories."
5. AUTHORITY — "What the menu won't tell you: the real calories in 7 'light' meals"
6. EXPERT — "A dietitian looked at my 'healthy' grocery haul. She flagged 6 items."

CURIOSITY / REVEAL FAMILY (the gap is the swipe; the payoff MUST exist)
7. GUESS — "Guess the calories in this smoothie bowl. Almost everyone goes low."
8. TRACKED — "I ate 'clean' for 30 days and nothing changed. Then I tracked it."
9. TEASE — "7 foods with more sugar than a donut. #4 is marketed to kids."
10. OUTCOME — "This 'harmless' iced coffee order is 640 calories. Here's the math."

RANKING / LIST FAMILY
11. LIST — "Every Chipotle protein, ranked by protein per dollar"
12. CHEAT — "50g of protein at 8 major chains. Save this for your next order."
13. ORDER — "The highest-protein order at Chick-fil-A under 500 calories"

IDENTITY FAMILY (persona call-outs plug in here)
14. POV — "POV: you finally know what's in your food without weighing anything"
15. CALLOUT — "If you're cutting on a 9-5 and eating lunch out, this is your cheat sheet"
16. HABIT — "I stopped quitting my food tracker. One change did most of the work."
17. WISH — "5 things I wish I knew before my first cut. #2 saved me six months."
18. NUMBER — "This one swap saves 3,500 calories a week. The math is on slide 6."

INTERACTIVE / COMPARISON FAMILY
19. COMPARE — "These are both 500 calories. One keeps you full for five hours."
20. RATHER — "600 calories: the burger or the iced coffee order? Vote below."

Hook distribution rules across 50 rows:
1. At least 10 distinct families used.
2. No family on more than 5 rows.
3. No two consecutive rows share a family.
4. No opening phrase used more than 4 times; no hook over 70% similar to another.
5. HABIT/WISH/NUMBER hooks must be about tracking, habits, or verified food math —
   never personal weight-change claims.

Banned hook patterns: subgroup restatements ("Eight items ranked by protein"),
subject-free questions, "a guide to calories", wait-for-it bait, secret-in-bio bait,
generic "5 nutrition myths debunked", anything that requires the caption to make sense.

======================================================================
6. THE RETENTION SYSTEM (SLIDES 2-9)
======================================================================

1. Slide 2 delivers the first concrete number, verdict, or useful setup. Never an
   empty "here's how it works".
2. By slide 3 the viewer must have received real standalone value (platforms re-serve
   carousels whose viewers reach slide 3+).
3. New reward every 1-2 slides; recognizable example early; stakes rise through the
   middle.
4. Strongest reveal, most surprising comparison, or best synthesis on slide 8 or 9.
   Slide 9 is a payoff, never an afterthought.
5. Ranking slides: "#N Item: Xg protein, Y calories" plus one short reason or
   tradeoff where it adds meaning. Vary the explanation rhythm; never eight identical
   sentence skeletons with one number changed.
6. Quiz posts: strongest reveal LAST. Answer slides always include one useful
   explanation.
7. Educational posts: mechanism → what it means in real life, before the final slide.
8. Contrarian/myth posts: verdict early, evidence and nuance after, "what matters
   instead" before the CTA.
9. Slide copy: 8-34 words default (45 max when accuracy needs it; 5-word minimum for
   structured reveal slides). One idea per slide. Final display copy only — no notes,
   no citations on-slide, no "swipe" labels.
10. Every post delivers its complete payoff even if the caption is never read.

======================================================================
7. THE CTA SYSTEM (SLIDE 10)
======================================================================

Exactly one CTA action per post, max 10 words, matched to the post's natural value.
Distribution across 50 rows: 18 FOLLOW, 12 COMMENT, 10 SAVE_OR_SHARE, 10 APP.

FOLLOW (attach to recognizable recurring series):
"Follow BiteBuddy for daily macro rankings." / "Follow BiteBuddy for smarter
restaurant orders." / "Follow BiteBuddy for food facts worth saving." / "Follow
BiteBuddy. The next ranking is coming." / "Follow BiteBuddy for tracking that
sticks." / "Follow BiteBuddy. No guilt, just numbers."

COMMENT (attach to posts with a specific, easy response; comment CTAs maximize reach
but not installs — use on discovery posts):
"Comment the chain BiteBuddy should rank next." / "Which one surprised you most?
Comment below." / "Name the next chain in the comments." / "Which would you actually
order? Tell BiteBuddy."

SAVE_OR_SHARE (attach to durable reference content — cheat sheets, rankings, builds):
"Save this BiteBuddy guide for your next order." / "Save this before your next
grocery run." / "Send this to your usual order partner." / "Save the ranking. Use it
when you order."

APP (attach to posts where scanning/tracking is the natural next step — proof posts,
then-I-tracked-it posts, restaurant reality checks; app CTAs convert best on
problem-solution demos):
"Scan it with BiteBuddy. Search 'BiteBuddy: Ai calorie scanner'." / "Track it with
BiteBuddy. Search 'BiteBuddy: Ai calorie scanner'." / "Compare with BiteBuddy. Search
'BiteBuddy: Ai calorie scanner'." / "Check macros with BiteBuddy. Search 'BiteBuddy:
Ai calorie scanner'."

Rules: one approved pattern per row; no pattern more than 6 times; never the same CTA
type on consecutive rows; the App Store search line appears ONLY on APP rows.

======================================================================
8. SERIES IDENTITY
======================================================================

Recurring series make the account followable. Use these labels when natural (as a
small series chip on the cover, per the design system): Restaurant Protein Ranking ·
Protein Per Dollar · Build the Order · Guess the Macros · Macro Matchup · Grocery
Protein Finds · Why You Feel That Way · Small Meals, Big Protein · Smart Swaps ·
Reality Check. A series label never replaces the hook's specific promise. No numbered
parts unless CONTENT_HISTORY confirms a real sequence. Not more than two consecutive
hooks with the same sentence structure.

======================================================================
9. VISUAL RECIPE ASSIGNMENT
======================================================================

Every row names one Visual_Recipe that the design system renders (see
Content-Engine/DESIGN-SYSTEM.md — the renderer, Canva Bulk Create or Claude-design,
maps each recipe to a locked template):

RANK-CARD (rankings, leaderboards) · PHOTO-FACT (listicles, hidden numbers, mistakes)
· QUIZ-CARD (guess posts, A-vs-B) · COMPARE-SPLIT (same-calories, matchups) ·
BUILD-STEP (order builders, swaps with running totals) · CHEAT-GRID (saveable
reference sheets) · TYPE-CARD (science/feeling explainers) · STORY-BEAT
(then-I-tracked-it, POV, confession posts)

Rules: the recipe must fit the post structure (a ranking is RANK-CARD, a quiz is
QUIZ-CARD, a cheat sheet is CHEAT-GRID); at least 5 recipes used across the batch; no
recipe on more than 12 rows; slide copy must be writeable onto that recipe's layout
(e.g. CHEAT-GRID's dense slide is slide 8 or 9; BUILD-STEP carries a running total on
every body slide).

======================================================================
10. CONTENT TAXONOMY — 10 GROUPS x 5 SUBGROUPS
======================================================================

Exactly five rows per group, one row per subgroup. Primary personas are listed per
group; assign each row's Audience accordingly (adjacent personas allowed when the
angle genuinely fits).

GROUP 1 — RESTAURANT PROTEIN (P3, P4)
1. RANK: eight current items from one chain ranked by protein per standard order,
   lowest to highest, calories for context. Two popular items minimum, one surprise.
2. BUILD: realistic high-protein order at a customizable chain under one clear
   constraint (max calories, max price, no double meat, vegetarian, or breakfast).
   Exact ordering language, every component's nutrition, verified availability.
3. CAT: eight items within one menu category (breakfast sandwiches, bowls, salads,
   coffee drinks, etc.) ranked by protein; consistent sizes and preparation.
4. EFF: seven items ranked by protein per 100 calories. Slide 2 defines the metric.
   Caption states the metric is not overall nutritional quality.
5. VALUE: eight items ranked by grams of protein per dollar at one exact verified
   location on BATCH_DATE, taxes and promos excluded; caption names location and date.

GROUP 2 — GUESS THE NUMBER (P5, P4; quiz structure: Q slides 2/4/6/8, A slides
3/5/7/9, strongest reveal last, every answer explains why)
1. CAL: four exact foods/orders, guess the calories. Similar-looking items whose
   sauces, portions, or toppings change everything.
2. SUGAR: four items, guess total sugar; full serving stated; added sugar
   distinguished when labeled.
3. PRO: four foods where appearance misleads on protein; answers include calories,
   serving, and one takeaway.
4. AVB: four head-to-head matchups, one metric each, at least one close call and one
   shocker; fair serving sizes.
5. SOD: four restaurant/packaged foods, guess the sodium; explain the main
   contributor; no fear framing.

GROUP 3 — HIDDEN SUGAR AND CALORIES (P5, P4, P6; every comparison fair, current,
defined; never imply the baseline food is superior)
1. DONUT: eight items vs one clearly defined donut/cookie baseline (baseline stated
   on slide 1; each slide: item, serving, sugar, difference).
2. DRINK: eight drinks vs one named burger's calories; standard recipes; full bottle
   sizes stated.
3. HEALTH: eight wholesome-looking products (granola, yogurt, smoothies, bars, dried
   fruit, bottled tea) with serving, sugar, and main sugar source. No "fake healthy"
   name-calling.
4. SALAD: four salad-vs-burger matchups (question slide + verified reveal slide);
   dressing included and stated; main calorie contributor explained.
5. COFFEE: eight standard coffee-shop drinks over a 400/500/600-calorie threshold;
   chain, drink, size, milk, toppings, calories on every slide; highest last.

GROUP 4 — GROCERY AND SNACK FINDS (P2, P3, P7; current labels, current availability)
1. U200: eight snacks, 10g+ protein, ≤200 calories, serving stated, varied
   categories, never eight flavors of one product.
2. TJ: eight current Trader Joe's high-protein finds across snacks/frozen/breakfast/
   components; product, serving, protein, calories per slide.
3. COSTCO: eight products in one Costco market; serving basis, protein, calories,
   package count; no "national price" claims.
4. BAR: eight protein bars ranked on ONE stated metric (protein/calorie, protein/
   dollar, lowest sugar ≥15g protein, highest FIBER ≥10g protein, total protein).
   The fiber option serves the fiber-tracking trend — use it unless history says
   otherwise.
5. GVALUE: eight foods with ≥8g protein at ≤$1 per serving, one verified market,
   package size and servings verified; no sale prices.

GROUP 5 — FOOD'S JOURNEY (any persona; accessible physiology, ranges not false
precision, distinguish digestion/absorption/emptying/elimination)
1. JOURNEY: one meal type traced chronologically mouth → elimination, specific to
   that meal.
2. STOMACH: eight meal/food types compared by typical stomach-emptying behavior,
   cautious ranges, what changes the timing.
3. FATFULL: one component (fat, protein, fiber, volume, texture, eating speed) and
   eight mechanisms/limits/implications for fullness. No promised satiety.
4. FIBER: one nutrient's journey (fiber, protein, starch, sugar, fat, lactose,
   resistant starch, polyphenols) from ingestion to fermentation/elimination.
5. WATER: one drink's journey (water, coffee, electrolyte drink, milk, protein
   shake, sweetened beverage); timeline through absorption, circulation, regulation.
   No detox language, ever.

GROUP 6 — WHY YOU FEEL THAT WAY (P1, P5; responsible causal language, individual
differences noted, practical neutral takeaway)
1. HUNGER: why one food/meal pattern may leave you hungry (fiber, protein, volume,
   signals, pairing fix).
2. CRAVE: why protein or fiber may reduce cravings for some people; why it is not
   magic.
3. COMBO: why one specific pairing may feel steadier; no blood-sugar promises.
4. HEAVY: why one meal pattern may feel heavy (size, energy density, emptying,
   alcohol, speed); fat is not the villain.
5. HANGRY: one felt experience (hangry, slump, post-lunch sleepiness, post-workout
   hunger, stress snacking) explained without diagnosis.

GROUP 7 — YOUR GUT, EXPLAINED (any persona; no exaggerated microbiome claims; every
post anchored to a concrete food or felt experience, not abstract science)
1. MICROBES: one concrete angle on the gut ecosystem (scale, diversity, antibiotics,
   what science does not know).
2. FEED: one substrate/process (fiber, resistant starch, fermentation, short-chain
   fatty acids, gas, variety); never "sugar feeds bad bacteria".
3. FERMENT: one fermented-food focus (yogurt, kefir, kimchi, live cultures vs
   pasteurized, fermented vs probiotic); no universal live-microbe claims.
4. BRAIN: one gut-brain angle (vagus nerve, appetite signals, stress and digestion,
   honest uncertainty); no personality/anxiety-cure claims.
5. FUNCTION: one normal-function topic (stool frequency norms, gas, tolerance,
   travel, fiber changes, when symptoms deserve a professional); no diagnosis, no
   universal ideals.

GROUP 8 — TIME TO FEEL (P3 for MPS, others any; time ranges, onset vs peak vs
duration, individual variation)
1. CAFF: one caffeine scenario (coffee, espresso, energy drink, with food, afternoon,
   sleep); dose defined; absorption, peak, half-life; no dosing advice.
2. ENERGY: when energy may change after one meal type; no universal peak claims.
3. CRASH: why sweet energy may fade for some people (absorption, insulin, baseline,
   context); crash never promised.
4. FULL: how fullness signals develop (stretch, hormones, speed, distraction); no
   fixed 20-minute rule.
5. MPS: one protein-and-muscle scenario (post-lifting, breakfast, before bed,
   distribution, plant vs dairy, older adults); leucine and the wider window; no
   one-meal muscle promises.

GROUP 9 — REALITY CHECK (P1, P4, P6 — the contrarian group. RULE: generic
myth-busting is dead; every row must anchor its verdict in one concrete, visual,
verified example — a real meal, a real label, a real number. Slide flow: hook stating
the belief → verdict (FALSE / MOSTLY FALSE / MISLEADING / PARTLY TRUE / CONTEXT
NEEDED) → why the belief started → what actually happens, shown through the concrete
example → evidence → nuance → what matters instead → takeaway → clarification → CTA)
1. GUM: one digestion belief (gum stays seven years, meat rots in the colon, water
   dilutes stomach acid, everyone needs daily bowel movements...).
2. NEG: one calorie/metabolism belief (negative-calorie foods, six meals boost
   metabolism, celery cancels calories, "calories don't matter if it's healthy"...).
3. NIGHT: one timing belief (eating after 8pm, mandatory breakfast, carbs at night,
   30-minute protein window...).
4. DETOX: one detox/supplement belief (detox tea, juice cleanses, ACV melts fat,
   lemon-water liver claims...). These stay evergreen because the industry does.
5. FAT: one macronutrient belief (fat makes you fat, carbs are inherently fattening,
   protein hurts healthy kidneys, fat-free means weight loss...).

GROUP 10 — SMART SWAPS AND ORDERS (P1, P2, P4, P5; every recommendation serves a
stated goal; tradeoffs stated; viewers never told they must swap)
1. CRAVE: four same-craving-fewer-calories swaps (two slides each: craving → swap
   with verified portions, calorie difference, and the honest tradeoff).
2. U500: one restaurant order hitting a verified goal (40g protein under 500 cal /
   50g under 700 / vegetarian 25g+). Build slides with running totals; exact
   ordering script; final totals.
3. SMALL: a small-appetite protein plan — realistic small meals/snacks that reach a
   stated protein target on a modest appetite (serves P2; no medication references,
   no eat-less framing — the constraint is appetite, the goal is enough).
4. SNACK: four snack swaps against one meaningful total goal (fewer calories for
   the same craving, more protein for similar calories, less added sugar); final
   reveal states the total difference and that exact portions determine results.
5. ORDER: "what I would order" at one major chain for one specific goal; exact
   script; final calories, protein, tradeoffs; never called perfect or optimal.

======================================================================
11. RESEARCH AND VERIFICATION PROTOCOL
======================================================================

Research every factual post before writing the final CSV. Source priority:

Restaurant nutrition: official nutrition calculator → official nutrition PDF →
official product page → official ordering platform → reputable database only when the
primary source is unavailable and the exact item is still verifiable.

Grocery: manufacturer label → retailer page showing the current label → USDA
FoodData Central for generics.

Prices: official ordering source or retailer/warehouse listing for ONE exact
location/market, on BATCH_DATE. Never: coupon/promo pricing, delivery markups, tax,
tips, old screenshots, blogs, social posts, or search snippets as final evidence.
Never mix markets inside one post.

Science: government health sources, academic medical centers, peer-reviewed reviews,
consensus statements. At least two credible sources per science post, at least one of
them government/academic/review-grade. Never one isolated study.

Per row, verify: exact item name, serving size, standard preparation, calories,
protein, sugar, sodium, fiber where displayed, price where displayed, availability,
market, every calculation, ranking order, comparison baseline, scientific wording.
Open every source used; cite the most specific page; the source set must cover every
displayed item and metric; Source_URLs contains only directly relevant accessible
HTTPS URLs. A row is VERIFIED only after coverage, calculations, wording, and
availability all pass. If a fact cannot be verified, replace the concept.

======================================================================
12. CALCULATION RULES
======================================================================

Check every calculation twice, with code.

Protein efficiency = protein g / calories x 100, one decimal.
Protein value = protein g / price, one decimal.
Cost per serving = package price / listed servings, two decimals.
Differences = larger minus smaller, correct unit stated.

Rank on exact unrounded values; stated tiebreakers; displayed order must match the
math; never mix serving sizes silently; no "about/roughly/around" for label or menu
values unless the source itself gives a range.

======================================================================
13. FRESHNESS AND ANTI-REPETITION
======================================================================

Against CONTENT_HISTORY: no same exact topic within 90 days; same chain in same
subgroup within 14 days; same product within 30 days; same comparison baseline within
45 days; same belief (Group 9) within 120 days; same hook ever; >70% hook similarity
ever; reused Post_ID ever.

Within the batch: no chain on more than 4 rows (unless CAMPAIGN_FOCUS); no product on
more than 2; no repeated baseline; no two rows teaching the same core lesson; no same
chain in consecutive rows; no identical hashtag set more than twice; captions never
share more than one full sentence.

Within any consecutive 8 rows: at least 4 hook families, 3 CTA types, 4 content
groups; no chain twice; no repeated opening phrase; ranking posts vary item counts.

======================================================================
14. SCHEDULE-AWARE ROW ORDER
======================================================================

CSV row order is publishing order.

1. Rows 1-28 are the A-tier: strongest cross-platform concepts, each viable as a
   YouTube Short title without platform words ("swipe"), spread across personas.
2. Treat each consecutive block of 4 rows as roughly one publishing day. Per block:
   one saveable ranking/reference post, one interactive quiz/matchup, one relatable
   explainer or story, one utility/app-relevant post — from at least 3 different
   groups, no chain twice, no CTA type twice in a row, at most one dense science
   post, varied hook families, varied personas.
3. Price-sensitive posts early (verification freshness).
4. Rows 29-50 must still pass every gate — they are the TikTok extension pool, not a
   weak tail.

======================================================================
15. CSV OUTPUT CONTRACT
======================================================================

One valid CSV file, exactly this header, then exactly 50 data rows (51 records):

"Post_ID","Group","Subgroup","Audience","Hook_Family","Visual_Recipe","Chain","Market","Topic","S1_Hook","S2_Content","S3_Content","S4_Content","S5_Content","S6_Content","S7_Content","S8_Content","S9_Content","S10_CTA","Caption","Pinned_Comment","Hashtags","Source_URLs","Verified_On","Verification_Status"

Field rules:
1. Every field quoted; internal quotes doubled; one physical line per record; no line
   breaks inside cells; no markdown; no em dashes (use comma, colon, semicolon, or
   hyphen); no blank fields; no cell starting with =, +, -, or @; leading/trailing
   whitespace stripped.
2. Post_ID: G[GROUP]_[SUBGROUP CODE]_[ENTITY CODE]_[YYYYMMDD]_[BATCH SEQUENCE],
   e.g. G1_RANK_CFA_20260725_001. Unique, uppercase entity codes.
3. Audience: P1-P8 exactly.
4. Hook_Family: one of the 20 family codes in Section 5.
5. Visual_Recipe: one of the 8 recipe codes in Section 9.
6. Chain: exact brand, MULTIPLE for multi-brand posts, NONE only for science/feeling
   posts with no commercial entity.
7. Market: exact city/state/country for location-priced posts; United States for
   national label or science posts.
8. Topic: 4-12 words, specific.
9. Slides: S1_Hook per Section 5; S2-S9 per Section 6; S10_CTA per Section 7.
10. Caption: 35-85 words; first sentence restates the value in fresh, keyword-rich
    language (one natural phrase: AI calorie counter / calorie tracker app / calorie
    scanner app / food tracker app); adds a serving/preparation/market/science note;
    practical takeaway; ends with one easy question ONLY when the CTA is COMMENT; no
    disclaimers, no stacked CTAs; mentions BiteBuddy naturally, not in every
    sentence.
11. Pinned_Comment: one line, under 120 characters, posted as the first comment.
    For TEASE/GUESS/quiz posts: tease the payoff slide ("#4 is the one everyone gets
    wrong", "drop your guess before you swipe"). For rankings: invite the next-chain
    debate. Must not repeat the caption's question and must not promise anything the
    post does not deliver.
12. Hashtags: 3-5; #BiteBuddy always; one category/intent tag (#HighProtein #Macros
    #RestaurantNutrition #FoodFacts); chain tag when the post centers on one chain;
    never #FYP/#Viral/#ForYou; no identical set more than twice.
13. Source_URLs: every supporting URL, pipe-separated, no spaces. Never NONE.
14. Verified_On: BATCH_DATE, YYYY-MM-DD. Verification_Status: VERIFIED on all 50.
15. No schedule columns, scores, or production notes. Row number IS the schedule
    signal.

Validate the saved file with a real CSV parser: exactly 51 records, exactly 25 fields
per record, no repair warnings.

======================================================================
16. INTERNAL QUALITY-CONTROL PASS
======================================================================

Before output, verify internally (fix, recalculate, rewrite, replace, and re-check
until all pass; output only after everything passes):

Audience and hook checks:
1. Every row names a persona whose real situation the post serves; quotas met.
2. Every hook passes Section 5; a skeptical stranger understands the post in one
   second; no burned patterns; family distribution rules hold.
3. Persona sensitivity rules hold (P5/P8 food-positive framing; P2 no medication or
   eat-less framing; P7 no bounce-back pressure; anti-persona accuracy rules).
4. Slide 2 value, slide-3 payoff, slide 8/9 peak all present.
5. CTA distribution exactly 18/12/10/10; patterns approved; search line only on APP
   rows; comment CTAs on discovery posts, APP CTAs on proof/problem-solution posts.
6. Pinned comments present, under limit, non-duplicative, honest.
7. Visual recipes fit their posts; at least 5 recipes; none over 12 rows.
8. Tone: no shaming, no moral food labels, no medical/outcome claims, no diet-culture
   framing, hedged science language throughout.

Content and structure checks:
9. 50 rows; 5 per group; every subgroup once; every carousel = hook + 8 content
   slides + CTA; no two rows teach the same lesson; no placeholders; number promises
   delivered exactly (a "7 foods" hook has 7 foods).
10. Anti-repetition rules (Section 13) and row-order rules (Section 14) hold.

Verification checks:
11. Every product current and available; every number matches its source; every price
    from one exact market on BATCH_DATE; every formula recomputed in code; every
    ranking order confirmed; every science claim supported by 2+ credible sources;
    every Source_URL relevant and accessed.

File checks:
12. Filename, UTF-8, exact header, 51 records, 25 fields per record, all fields
    quoted, no forbidden characters, unique Post_IDs, parser-clean.

======================================================================
17. FINAL EXECUTION INSTRUCTION
======================================================================

Run all ten groups and all fifty subgroups. Produce one CSV: one header record plus
fifty VERIFIED rows — persona-targeted, hook-engineered, retention-structured,
visually assignable, factually verified, schedule-ordered, and ready for bulk
creation without any manual revision.

Return only the finished CSV file or its download link. No process narration, no
partial output, no commentary, no code fences, no early stop.
