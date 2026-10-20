---
name: "s7-system"
description: "Check the Soulitude7 skills are current and unedited, log a local change to the Soulitude7 design system for MYKD's review, or explain how to update. Use when the user asks to check, update or log a change to the Soulitude7 system, or after a Soulitude7 build that departed from the design system."
---

# s7-system

Keeps each person's copy of the Soulitude7 system in step with the MYKD master, and records local changes so MYKD can review them before each release.

- Release: see `manifest.json` in this folder (`version` and `released`).
- Studio page: https://studio.mykd.co.uk/soulitude7/design-system
- Log a change form: https://studio.mykd.co.uk/soulitude7/design-system/#log
- Contact: michael@mykd.co.uk

How the system is split:

1. The design system, the template deck and the canvases live in MYKD's Claude account and are shared with each user. They update live. Nobody downloads them.
2. The skills (`s7-deck`, `s7-brochure`, `s7-social-tile`, `s7-system`) are packaged by MYKD. Each release replaces them whole. Local edits to a skill are lost at the next update, which is why they are logged first.
3. Local rules belong in a document named `s7-local.md` in the user's own Claude project. Updates never touch it.

## Job 1: check

Run when the user asks to check the system, before any update, and when a skill behaves unexpectedly.

1. Run `scripts/check.py` from this skill's folder with Python 3: `python3 scripts/check.py --out s7-check-report.json`. It finds the installed Soulitude7 skills, compares every file with `manifest.json` and writes a report.
2. Tell the user, in plain words: the installed release, whether it is the latest on the studio page if you can read the page, and any files that were edited, added or are missing.
3. If anything was edited or added, the report holds the edited text. Offer to log it (Job 2) and attach the report, so the edit is not lost when the update overwrites it.
4. If code execution is unavailable, say so and ask the user to send the skill files to michael@mykd.co.uk instead.

## Job 2: log a change

Run when the user asks to log a change, accepts the offer after a build with departures, or after a check that found edits.

1. Draft one entry per change with these fields. Ask only for what you do not already know.
   - Name: the person logging it.
   - Skill and release: for example `s7-deck 1.0.0`.
   - Type: one of `override` (a system rule set aside for one document), `new layout or style`, `local rule` (added to `s7-local.md`), `skill edit`, `problem` (something the system got wrong).
   - What changed: one or two plain sentences.
   - Why: the reason in the user's words.
   - Where: a link to the document, deck or canvas, if there is one.
2. Show the entry to the user and ask them to confirm it.
3. If the change is a local rule and you can write to the user's project, add it to `s7-local.md` under a dated line. If you cannot write there, give the user the line to paste in.
4. Send the entry to MYKD. Build a link to the form with the fields filled in, URL encoded: `https://studio.mykd.co.uk/soulitude7/design-system/?name=…&skill=…&release=…&type=…&change=…&why=…&where=…#log`. Give the user the link and tell them one click on Send finishes it. For a check report, tell them to paste the report into the form's report box.

Never invent a change. Log only what happened in this session or what the user tells you.

## Job 3: update

Explain the update in the way the user installed the skills.

- Claude desktop app, installed as a plugin: Customize, Plugins, the MYKD studio marketplace, Check for updates. If Claude warns that local edits will be overwritten, stop and run Job 1 first.
- Uploaded as skill files: run Job 1, log any edits, then delete the four Soulitude7 skills under Customize, Skills and upload the new files from the studio page.

After an update, read the release notes on the studio page and tell the user what changed in one or two sentences.

## Words

Plain British English. Write Soulitude7 as one word. MYKD in capitals.
