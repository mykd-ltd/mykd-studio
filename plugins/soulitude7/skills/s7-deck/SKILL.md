---
name: "s7-deck"
description: "Build Soulitude7 presentations as Claude Slides decks from the Soulitude7 design system and its presentation template. Use for any Soulitude7 deck, pitch or talk slides."
---

# s7-deck

Build Soulitude7 presentations as 1920 × 1080 Claude Slides decks. The design system is the single source of truth for the grid, the slide layouts, the panel rule, the slide type sizes and every rule. The template deck is the master copy of the slides and the source of their images. This skill holds only the workflow. If anything here disagrees with the design system, the design system wins.

- Design system: https://claude.ai/artifact/TD4zmiVXgsGu95xEFvjZ4p
- Template deck: https://claude.ai/artifact/4nmQSCKnJ1qsRnRk3zvQ8s

## Always read from the design system first

Read these with the artifact read action and a `path`, every time, before building. Never read the design system's page. Never rely on memory of earlier sessions.

1. `project/deck.md`: the grid, the slide layout catalogue and when to use each layout, the panel rule, all slide rules, the template asset table and known gaps.
2. `project/README.md`: brand fundamentals, the Slide type table, the logo rules for slides.
3. The template deck's `project/deck.json` and the `project/slides/<id>.html` files you need, read from the template deck itself. They are the master copies. The design system's `project/deck/slides/` copies are a reference only.

If a needed file cannot be read, say so and stop rather than guessing.

## Before you build

1. Ask the user, with the question tool, at the start of every deck: purpose and audience, slide count, which cover (Full bleed, White with photo or Yellow), which layouts, and what content they have. Do not assume a slide count.
2. Choose layouts from the "Slide layouts and when to use them" table in `deck.md`. One cover per deck. If no layout fits, ask the user before inventing one. If the user approves a new layout, build it in their document and log it with the `s7-system` skill. The maintainer (MYKD) also adds it to the design system, as the section on keeping the design system current says.

## Building a deck

1. Create the deck from the Slides type with a title, as the Slides type's instructions say. Install the design system (folder `s7ds`: `project/ds/s7ds/tokens.json` plus the `designSystems` record). Use the template deck's `faces` (Playfair Display and Inter from Google Fonts).
2. Copy the images the chosen slides use from the template deck into the new deck, server side: publish with `asset: true`, `from_url` = the template deck, `asset_ids` = the ids from the slide files (ten at most per call). Each copy gets a new id. Remap every `src="/_blob/<old id>"` in the copied slides to the new id the copy returned. Never leave a template deck id in a new deck.
3. Copy each chosen slide file from the template deck, keep its structure and positions, and replace the words. Number the slides and the contents list to match the new deck. Keep the speaker notes that explain the layout only if the user wants a template; otherwise replace them with presenter notes or remove them.
4. Write the index first with the full `order`, then the cover, then the rest, as the Slides type's instructions say.

## Rules to hold on every slide

These are summarised from `deck.md`; read it for the full set.

- Panel rule: photograph panels and the Mist sidebar are 601px wide, 40px from the top and bottom edges, bleed off the side edge, square on the bleed edge and 16px on the inner corners. Text keeps 74px clear. Only the avatar and the page number sit on a photograph, over a light plum fade at the bottom.
- Logo: full logo on covers and the back cover; the avatar, 62 × 41px, bottom left everywhere else; colourway set by what sits behind it.
- Eyebrow rule: the running head names the section, so title blocks carry no eyebrow unless it names a sub-section. A title never repeats the running head.
- Yellow: never two yellow slides side by side; one yellow cell at most in a testimonials bento; white SemiBold titles on yellow.
- Type: the Slide type sizes only; nothing below 24px. If copy runs over, split the slide; never shrink type.
- Full bleed cover tint: adjust only by setting the `tint` layer's opacity or width. Check white type reaches 3:1 at the title and 4.5:1 at the eyebrow.
- White with photo cover: for a two-line title, move both photographs down 122px and shorten them by the same.
- Programme or service slides side by side alternate the photograph: left (`retreats-full-height`), then right (`retreats-full-height-right`). Body copy under the title stays at 170 characters or fewer.
- Contents list: up to seven rows; seven rows take 10px row padding. Widen the title column to 380px on every row when a title will not fit 330px.
- Never use the same photograph twice in one deck.

## Words

Use the content the user provides first. You may draft copy in the Soulitude7 tone for review and must flag it as draft in your reply. Never invent facts, fees, names, statistics or quotes. Missing content becomes a visible placeholder such as [FEE]. Fees need confirming before release. Quotes need permission to publish; attributions are roles unless the client agreed to be named. Plain British English, no three beat structures. Never use a dash on titles, eyebrows, subtitles or other display type: use a colon or a full stop. Join the last two words of every title and paragraph with a non breaking space. Write Soulitude7 as one word.

## Images

Use the design system image library first (skies, landscapes, cities and culture, portraits, full bleed with text). Ask before using any photo from outside it. A library photo not in the template deck: read it from the design system by its asset id and upload it to the new deck. Follow the portrait crop rule in `deck.md`. Type sits directly on a photograph only on the Full bleed cover, with a Full bleed with text image. Icons are yellow: a library icon the template deck does not hold needs its `fill="currentColor"` set to `#FCCD33` before upload, because an icon inside `<img>` renders black.

## Working method

Build a few slides at a time. Re-read the live deck files before editing, because the user hand edits slides. Do not verify rendering unless asked, and say plainly in the reply that the slides are unchecked. When a layout decision is unclear, ask the user rather than guessing, then record the answer in `deck.md`.

## Keeping the design system current

**Maintainer only.** Do this only when the artifact read of the design system says you are a writer (MYKD). Everyone else never publishes to the design system, the template deck or any MYKD canvas: build the change in the user's own document, then log it with the `s7-system` skill so MYKD can review it for the next release.

When a slide layout, rule or style changes during a job, update the template deck and the design system in the same session: edit the template slide, then `deck.md`, the matching `deck/slides/` copy and, for type or logo rules, the README. Publish to the design system with the index last, updating its `lastChange`, as the design system's own instructions say. Never leave a deck ahead of the template, or the template ahead of the design system. If a publish to the design system or the template deck is refused as not viewing the latest version, read the files you are changing again into a fresh folder, reapply the edits there and publish from that folder; if it is still refused, read the page once (read action with `page: true`), then retry.

## Local rules and logged changes

This skill is managed by MYKD and is replaced whole at each release. Never edit it to change a rule.

1. Before building, if the user's Claude project holds a document named `s7-local.md`, read it. Its local rules apply on top of the design system. A local rule never overrides a locked brand rule (logo, colour, type, the yellow rules). Where the two conflict, the design system wins and you say so.
2. At the end of every build, list any departure from the design system in your reply under the heading "Departures": a rule the user overrode, a layout or style the system does not hold, a photograph from outside the library, a local rule applied. If there were none, say "Departures: none".
3. If there was a departure, offer to log it with the `s7-system` skill. Logging is how MYKD sees local changes and decides whether to add them to the system.
