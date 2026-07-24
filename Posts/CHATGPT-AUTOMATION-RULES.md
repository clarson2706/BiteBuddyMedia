# BiteBuddy carousel generation rules

## Required unit of work: one connected post batch

Each post folder is one complete carousel-generation job.

For every post, in the order defined by `Posts/current-week.json` and that week's generation guide:

1. Read the instructions for that specific post in full before generating any slide.
2. Generate all slides for the post as one visually connected batch. Maintain consistent art direction, typography, spacing, palette, food-photography treatment, and BiteBuddy appearance across the entire carousel.
3. Export the connected batch as separate files named `01.png`, `02.png`, and so on, each exactly 1080 × 1350 pixels.
4. Use the approved weekly hero screenshot unaltered and only on the final Download slide. Never invent app UI.
5. Commit the complete post batch to that post's `slides/` folder and confirm the post-level commit.
6. Only after the complete post commit is confirmed may generation move to the next post.

Do not treat the week as a collection of unrelated individual slide jobs. Do not stop after partially generating a post. A `.gitkeep` file or existing slide file never means a post should be skipped; overwrite incomplete or prior slide output when instructed.

The default is to generate all 21 post batches. The only initial hard stop is failure to read `Posts/current-week.json`, which must be reported with the exact attempted read and error.