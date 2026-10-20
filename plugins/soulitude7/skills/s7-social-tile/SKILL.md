---
name: "s7-social-tile"
description: "Build Soulitude7 1080 x 1080 social tiles from the approved designs in the Soulitude7 design system. Use for any Soulitude7 social post, tile, announcement, testimonial, team introduction or event image."
---

# s7-social-tile

Builds Soulitude7 social tiles from the approved tile templates held in the Soulitude7 design system. The design system is the only master: the rules, the tile templates and their images all live in it. This skill never invents a layout, colour, type style or logo treatment.

## Sources

- Design system (read live every run): https://claude.ai/artifact/TD4zmiVXgsGu95xEFvjZ4p
- Tile templates: `project/social/tiles/<id>.dc.html` in the design system, listed in `project/social.md`.

The social tiles canvas is a preview built from the design system, and the Meet the team tiles canvas holds finished tiles. Never read a layout from either or duplicate their artboards.

If the design system cannot be read, stop and tell the user. Do not build from memory or from this file alone.

## Step 1: read the system

Read `project/README.md` from the design system, including its "Social tile copy" section, then `project/social.md`, then the README of the chosen design (`project/components/<Design>/README.md`) and the README of any asset group used (`project/assets/<Group>/README.md`). Take colours, type styles, spacing, logo rules, copy rules and voice rules from there. Where this file and the design system differ, the design system wins and the difference is reported to the user.

Build from the template file in `project/social/tiles/` for the chosen design and variant. The templates are built to the cards. If a template and its card ever differ, build to the card and tell the user the template needs updating.

## Step 2: choose the design (no guessing)

The approved designs:

| Design | Variants | Use for |
| --- | --- | --- |
| Case study (SocialCaseStudy) | yellow, white | Outcomes, programme messages, brand statements, announcements. Headline of three to five words plus one subheading line. |
| Testimonial (SocialTestimonial) | yellow, white | One client quote with attribution. |
| Team profile (SocialTeamProfile) | big name, khaki, silver (Mist) | Introducing a team member with credentials. |
| Full bleed (SocialFullBleed) | clouds, field, beach photographs | Events, workshops, programme announcements with type on a photograph. |
| Meet the team (MeetTheTeam) | one layout | Team introduction with a portrait panel. |

Rules:

1. Match the request to one design only when it fits exactly one. If two or more could fit, or the ground or variant is not stated, ask. Show the options by name with a one-line description of each. Ask until the choice is certain. Never pick a design or variant silently.
2. Never place two yellow tiles side by side in a set. When building a set, alternate yellow with white or another ground and say so.
3. Meet the team and the Team profile layouts overlap in purpose. Always ask which is wanted.

## Step 3: ask whether it should be editable

Ask: "Do you want an editable image?"

- Yes: build a Design canvas (Artifact type Design) with one 1080 x 1080 artboard per tile. Install the Soulitude7 design system on the canvas as the Design type instructs. Copy the template file from `project/social/tiles/` as the artboard, do not redraw it. Copy its images from the design system into the canvas, server side (publish with `asset: true`, `from_url` = the design system, `asset_ids` = the ids in the template), and remap every `src` to the id the copy returns.
- No: render a PNG at 1080 x 1080 from the same template file, with the fonts embedded. Deliver the PNG to the user.

If the user wants both, build the canvas and export PNGs from it.

## Step 4: collect the text (ask, never invent)

List every text area in the chosen design (eyebrow, headline or quote, subheading, attribution, description, place and date, name, role, credentials, supporting sentence). Compare with what the user supplied. For every area left blank, ask one question that offers:

- a recommended default (for an eyebrow, the recommended entry from the list below; for place and date, "Virtual | October 2026" only if the user confirms the values), or
- removal, where the design allows the element to be dropped, or
- the user supplies the text.

Never invent names, quotes, attributions, dates, places or credentials. Testimonial attributions are a role, never a name, unless the user confirms the client has agreed to be named. Ask whether permission exists to use a quote in a public post.

### Copy rules (from the design system, Social tile copy)

Applies to every tile:

- Sentence case. Programme and event names keep their own capitals.
- No full stop on eyebrows, headlines, subheadings, quotes, attributions, roles or details. Full stops only on a supporting sentence.
- No dashes, no exclamation marks, no emoji, no quotation marks on display type.
- Durations are written out ("Twenty years"). Other numbers are numerals. "7" is always a numeral.
- Balanced line breaks and no widows: join the last two words of every title, quote and subheading with a non-breaking space.
- Hyphenated names never break at the hyphen.

By element:

| Element | Rule |
| --- | --- |
| Eyebrow | Required on Case study, Testimonial and Meet the team big name. One to three words. Recommend the entry from the list below; the requester may replace it with their own. Typed in sentence case: the style sets capitals. None on Full bleed. On Khaki and Silver it is the person's name. |
| Case study headline | Three to five words. Three lines at most. |
| Case study subheading | Up to ten words. One thought. Must not repeat the headline. |
| Testimonial quote | Up to 12 words, two to four lines. The client's own words, cut only at a clause end. No quotation marks. |
| Attribution | A role of up to four words. Never a name or a firm unless the client agreed. |
| Name | Full name, two lines at most. |
| Role (big name, MeetTheTeam) | Up to eight words, two lines at most. Khaki and Silver have no role line. |
| Credentials headline (Khaki, Silver) | Up to eight words, four lines at most. Playfair Medium. |
| Supporting sentence | One sentence with a full stop, up to 20 words. Khaki and Silver only on the Team profile; big name has none. |
| Full bleed title | The event name on two short lines. The second line is italic. |
| Full bleed description | One line, about 45 characters. |
| Place and date | "Place | Month YYYY": spaced pipe, month and year only. |

Recommended eyebrows: Case study "Client impact" or "Announcement". Testimonial "Client impact". Meet the team big name and MeetTheTeam "Meet the team". Khaki and Silver: the person's name. Always recommend the list entry first. If the requester gives their own eyebrow, use it without asking for approval, provided it is one to three words in sentence case with no full stop, dash or emoji. If it breaks those limits, propose a compliant version and ask.

If copy runs over, propose a shorter version and ask. Do not shrink the type.

## Step 5: images

- Team profile and Meet the team: use the Team portraits group in the design system. Each team member needs two files: the photograph with its background, and a cut-out with the background removed. If the person has no portrait there, ask the user to upload one, and for a cut-out remove the background. Then tell the user the portrait must be added to the Team portraits group of the design system so it is available next time (add it yourself only if you have edit access to the design system; otherwise say it needs adding).
- Team profile portrait rule (19 October 2026): big name keeps the photograph's background, in colour, with the yellow soft-light layer at 50 per cent. Khaki and silver always use the cut-out portrait, with no overlay. Never use a photograph with its background on khaki or silver, and never use a cut-out on big name.
- Meet the team (MeetTheTeam) keeps the photograph's background and forces black and white. Ask which treatment is wanted and, for colour, build from the Team profile big name layout or as markup without the grayscale filter.
- Portrait colour: colour is the preference. Black and white is allowed only if the whole set is black and white. Never mix.
- Full bleed: use only images in the Full bleed with text group of the design system. Never use an image outside the group. If the user wants a new photograph, say it must be approved by eye on a tile and added to the group first.
- Every image carries a strong sense of light and yellow, with a calm, low-detail area behind any type.

## Step 6: build to the design

- 1080 x 1080. Margin 96px on every side (`spacing-tile`). Align left.
- Use the design's own type styles, colours, spacing tokens and logo colourway. The background decides the logo colourway: on-yellow on yellow, on-light on white and Mist, on-dark only over photography and khaki. Full logo 60px high, bottom left on the margins. Avatar only on Meet the team and the big name layout, in a 100 x 70px box.
- Yellow ground: title in white Playfair Display SemiBold, eyebrow and supporting text in plum (`text-on-brand`). Light ground: title in `text-default`, eyebrow and subheading in `text-brand`. Titles on light grounds are never yellow.
- Team profile text colours: big name eyebrow `text-brand`, name `text-default`, role `text-muted`. Khaki: eyebrow `text-default`, headline white, supporting sentence `text-default`. Silver: eyebrow `text-brand`, headline `text-default`, supporting sentence `text-default`. Khaki and silver headlines are `social-display-m` in Playfair Medium (never SemiBold). The supporting sentence is `social-body-l` at 33 / 140%.
- Never recolour logos, redraw the supergraphic, or add icons from another set.

## Step 7: anything beyond the design

If the request needs something the approved designs do not contain (a different layout, an icon, a second logo, a new colour, an extra text block, a new photograph, a different size), say so plainly before building. State what is new, confirm the user wants it, then build it from the design system's colours, type styles, spacing, radius and logo rules, and label it as a new element in the reply. If it cannot be built within the system, say that and offer the nearest approved design.

## Step 8: voice rules (check every word)

- Soulitude7 is one word, no space, everywhere in text. Never "Soulitude 7".
- British spelling. Sentence case for headings, labels and buttons. Programme and event names keep their own capitals.
- Curly quotes and apostrophes. No emoji. Dates are month and year, no day. The pipe separates place and date: "Virtual | October 2026".
- No dashes of any kind on a tile. The design system allows a spaced em dash only for asides in running copy, never on social tiles (confirmed 20 October 2026). Use a colon or a full stop where a dash would go.
- Voice is direct and unhurried, second person, short declaratives, no exclamation marks.

## Step 9: open rules, apply the safe default and flag

The design system lists rules not yet settled. Apply the safe default and mention it in the reply where it applies:

- Known low contrast pairs, kept as designed by Michael and not to be flagged again as open: white title on yellow (1.51:1), yellow text on white (1.51:1), muted text on white (2.75:1, including the big name role), white headline on khaki (1.66:1), yellow eyebrow on silver (1.4:1). Large short text only, never body copy.
- Yellow accent text on light grounds: only at `social-caption` or `social-sub-xl` size and above, and only for eyebrows, subheadings, attributions and event details. This size floor was confirmed by Michael on 19 October 2026.
- Closed on 19 October 2026: the SemiBold exception for khaki and silver headlines (now Medium) and the supporting line size (now 33 / 140%).
- Copy limits in Step 4 (12-word quote, eight-word credentials headline, 45-character description) were set on 19 October 2026 and have not yet been checked by rendering. If a tile overflows, shorten the copy and report the overrun.
- Still open: the MeetTheTeam component code forces black and white; and an on-light logo over a bright yellow part of a photograph is proposed, not approved.

## Step 10: final checklist before delivery

Confirm each item and fix any failure before sending:

1. The design and variant were confirmed by the user, not assumed.
2. Every text area is filled, removed or confirmed. Nothing invented.
3. Copy fits the Step 4 limits and passes the voice rules. The eyebrow is the recommended entry or the requester's own, within the format limits.
4. No full stops, dashes or quotation marks on display type. No widows.
5. Logo colourway matches the ground, size is 60px high (avatar 100 x 70px), bottom left on the margins.
6. Margins are 96px (64px inside a panel). Nothing overlaps type.
7. Images come from the approved groups, or the user was told the new image needs adding and approving.
8. Portrait treatment matches across the whole set. Team profile: photograph with background on big name, cut-out on khaki and silver.
9. No two yellow tiles side by side in a set.
10. Anything new beyond the design was confirmed and is labelled as new.
11. Size is 1080 x 1080.

## Output and naming

Name files `s7-<design>-<short title>.png`, lower case, words joined by hyphens, for example `s7-case-study-introducing-our-associates.png`. Deliver in the conversation. For an editable image, deliver the Design canvas link as well, and say the canvas is private until shared from its Share menu. In the reply, state in one or two sentences what was built, which design and variant, and any default applied or element flagged.

## Keeping the design system current

**Maintainer only.** Do this only when the artifact read of the design system says you are a writer (MYKD). Everyone else never publishes to the design system or to any MYKD preview: build the change in the user's own document, then log it with the `s7-system` skill so MYKD can review it for the next release.

When a tile design, rule or style changes during a job, change the design system first: the card README, the template in `social/tiles/`, `social.md` and any new image in its asset group. Publish to the design system with the index last, updating its `lastChange`, as the design system's own instructions say. Then rebuild the social tiles canvas preview from the design system and label it with the design system version it was built from. Never edit the preview to change a tile.

## Local rules and logged changes

This skill is managed by MYKD and is replaced whole at each release. Never edit it to change a rule.

1. Before building, if the user's Claude project holds a document named `s7-local.md`, read it. Its local rules apply on top of the design system. A local rule never overrides a locked brand rule (logo, colour, type, the yellow rules). Where the two conflict, the design system wins and you say so.
2. At the end of every build, list any departure from the design system in your reply under the heading "Departures": a rule the user overrode, a layout or style the system does not hold, a photograph from outside the library, a local rule applied. If there were none, say "Departures: none".
3. If there was a departure, offer to log it with the `s7-system` skill. Logging is how MYKD sees local changes and decides whether to add them to the system.
