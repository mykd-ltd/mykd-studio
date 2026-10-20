---
name: "s7-brochure"
description: "Build Soulitude7 A4 brochures, programme and service guides and retreat workbooks as Design canvas pages from the Soulitude7 design system. Use for any Soulitude7 brochure or guide."
---

# s7-brochure

Build Soulitude7 A4 print documents as pages on a Design canvas. The design system is the single source of truth for the grid, the layouts, the rules, the layout CSS and the page templates. This skill holds only the workflow. If anything here disagrees with the design system, the design system wins.

Design system: https://claude.ai/artifact/TD4zmiVXgsGu95xEFvjZ4p

## Always read from the design system first

Read these files from the design system with the artifact read action and a `path`, every time, before building. Never read its page. Never rely on memory of earlier sessions.

1. `project/brochure.md`: the grid, the layout catalogue and when to use each layout, the long read rules, the column break rule, the full bleed cover fade, all brochure rules, known gaps and the source file list.
2. `project/README.md`: brand fundamentals and the Brochure type section.
3. `project/tokens.json`: tokens and the Brochure type group.
4. `project/brochure/s7-print.css`: the layout styles. Copy it onto the canvas as `project/s7-print.css` and link it from every page.
5. `project/brochure/pages/<name>.dc.html`: one template per layout, listed in `brochure.md`. Read only the templates you need, copy them onto the canvas and edit the copy. Do not redraw layouts from scratch.

If a needed file cannot be read, say so and stop rather than guessing.

## Before you build

1. Ask the user, with the question tool, at the start of every document: document type (flagship brochure, programme or service guide, retreat workbook), page count and format, cover choice, and what content they have. Do not assume a page count. Plan in multiples of four when the user is printing a stapled booklet and say so.
2. Choose layouts using the "Page layouts and when to use them" table in `brochure.md`. If no layout fits, ask the user before inventing one. If the user approves a new layout, build it in their document and log it with the `s7-system` skill. The maintainer (MYKD) also adds it to the design system, as the section on keeping the design system current says.
3. Install the design system on the canvas as `s7ds` (`project/ds/s7ds/tokens.json` plus the `designSystems` record) so the real Logo and PullQuote components mount.

## Output

Design canvas pages only: one `.dc.html` artboard per page, 794 × 1123px, A4. Print PDF export is not part of this skill yet.

## Words

Use the content the user provides first. You may draft copy in the Soulitude7 tone for review and must flag it as draft in your reply. Never invent facts, fees, names or claims. Missing content becomes a visible placeholder such as [FEE]. Fees need confirming before release. Plain British English, no three beat structures. Asides in running copy may take a spaced em dash, once a paragraph at most. Never use a dash on titles, eyebrows, subtitles or other display type: use a colon or a full stop there. Follow the README for logo colourways, icon colour and yellow accents.

## Images

Use the design system image library first (skies, landscapes, cities and culture, portraits). Ask before using any photo from outside it. The photographs in the templates are placeholders: swap them for the right library photo.

Full bleed covers:

- The Full bleed cover template has an optional fade over the photograph, set with tweaks in the Cover fade group: `fadeOn` (toggle), `fadeTone` (`light` or `dark`) and `fadeHeight` (0 to 1123px). Keep the template's structure and change the fade only through the tweaks. Never drag or resize the fade layer, because that fixes its height and breaks the slider.
- `fadeTone` light: white fade, type as on white (yellow eyebrow, ink title, muted subtitle, on-light logo). `fadeTone` dark: ink fade, all type white, on-dark logo. The tone sets the type colours whether the fade is on or off.
- Judge the photograph first. Dark photograph: dark tone, fade off or on as needed. Light photograph: light tone. Scale and crop the photograph so its light area sits behind all the type (from y 281 to the end of the subtitle) and the logo. No dark structure, such as a window bar, a lamp or the subject, may cross the type. Scale the photograph up and anchor it at the top if needed.

## Working method

Build one page at a time. Re-read the live canvas files before editing, because the user hand edits pages. Do not verify rendering unless asked, and say plainly in the reply that the pages are unchecked. When a layout decision is unclear, ask the user an obvious question about the layout and its use rather than guessing, then record the answer in the design system's `brochure.md`.

## Keeping the design system current

**Maintainer only.** Do this only when the artifact read of the design system says you are a writer (MYKD). Everyone else never publishes to the design system, the template deck or any MYKD canvas: build the change in the user's own document, then log it with the `s7-system` skill so MYKD can review it for the next release.

When a layout, rule or style changes during a job, update the design system in the same session: edit `brochure.md`, `brochure/s7-print.css` and the matching `brochure/pages/` template, then publish with the index last, as the design system's own instructions say. Never leave the canvas ahead of the design system. If a publish to the design system is refused as not viewing the latest version, read the design system page once (read action with `page: true`), then retry the edit.

## Local rules and logged changes

This skill is managed by MYKD and is replaced whole at each release. Never edit it to change a rule.

1. Before building, if the user's Claude project holds a document named `s7-local.md`, read it. Its local rules apply on top of the design system. A local rule never overrides a locked brand rule (logo, colour, type, the yellow rules). Where the two conflict, the design system wins and you say so.
2. At the end of every build, list any departure from the design system in your reply under the heading "Departures": a rule the user overrode, a layout or style the system does not hold, a photograph from outside the library, a local rule applied. If there were none, say "Departures: none".
3. If there was a departure, offer to log it with the `s7-system` skill. Logging is how MYKD sees local changes and decides whether to add them to the system.
