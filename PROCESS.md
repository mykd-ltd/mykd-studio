# Soulitude7 design system: packaging, release and change review

How the Soulitude7 design system, its templates and its skills reach each user, how updates run, and how local changes come back to MYKD for review.

Repo: `mykd-studio`. Studio page: `studio.mykd.co.uk/soulitude7/design-system`. Written 20 October 2026.

## The decisions

1. **Updates overwrite.** Each release replaces the four skills whole. Nothing merges. Skill files are prose instructions, and a merge of two sets of instructions produces a third version nobody has tested. Overwriting keeps every user on the exact release MYKD tested.
2. **Local changes live outside the managed files.** Each user keeps a file called `s7-local.md` in their own Claude project. The skills read it before every build. Updates never touch it.
3. **Nothing is lost silently.** Before any update, the user asks Claude to check the system. A script compares their installed skills with the release manifest. Any edit is captured in a report and logged to MYKD before the overwrite.
4. **The design system is never downloaded.** It stays in the MYKD Claude account, shared with each user, and the skills read it live. Most changes (rules, tokens, layouts, images, templates) reach users the moment they are published, with no install.

This is the better route than packaging everything as a download. Only the skills need distributing, because only the skills live in the user's account.

## What ships where

| Part | Lives in | Reaches users by | Update cost for the user |
| --- | --- | --- | --- |
| Design system v1.2 | MYKD Claude account (artifact) | Share with their Claude email | None. Live. |
| Template deck, social tiles canvas | MYKD Claude account (artifacts) | Share with their Claude email | None. Live. |
| Skills: s7-deck, s7-brochure, s7-social-tile, s7-system | `mykd-studio` repo | Plugin marketplace (desktop app) or skill zips (web) | Automatic on desktop. Four uploads on the web. |
| Local rules | User's Soulitude7 project, `s7-local.md` | Starter file on the studio page | None. Never overwritten. |
| Change log | Form on the studio page, to MYKD | Claude fills the form link for the user | One click on Send. |

## The repo

```
mykd-studio/
  .claude-plugin/marketplace.json        marketplace, lists the soulitude7 plugin
  plugins/soulitude7/
    .claude-plugin/plugin.json           version stamped by the build
    skills/s7-deck/SKILL.md
    skills/s7-brochure/SKILL.md
    skills/s7-social-tile/SKILL.md
    skills/s7-system/SKILL.md            check, log, update
    skills/s7-system/manifest.json       sha256 of every managed file, written by the build
    skills/s7-system/scripts/check.py    compares an install with the manifest
  release.json                           version, date, links, release notes, form endpoint
  templates/s7-local.md                  starter local rules file
  tools/build.py                         builds a release
  tools/review.py                        turns a check report into a diff for review
  reviews/                               one review file per report, with your decision
  docs/                                  the studio page, uploaded to studio.mykd.co.uk on your hosting
    soulitude7/design-system/index.html  the page
    soulitude7/design-system/downloads/  zips and s7-local.md, written by the build
```

The repo becomes the master for the skills. Install your own copy from the marketplace too, so you use what the client uses. Changes to a skill are made in the repo, never in a Claude account.

## Changes made to the skills for distribution

The skills in your account told Claude to publish layout and rule changes straight into the design system and the template deck. A client with view access would be refused, and one with edit access would change your master. The packaged copies now do this:

- The "Keeping the design system current" sections in s7-deck and s7-brochure run only when Claude's read of the design system says the user is a writer (you).
- A new layout agreed with a user is built in their document and logged.
- Every skill reads `s7-local.md`, lists "Departures" at the end of each build and offers to log them.
- A new fourth skill, s7-system, runs the check, logs changes and explains updates.

## One-time setup

Step by step guidance for GitHub, GitHub Desktop, the domain and the form is in SETUP.md.

1. **GitHub.** Create a repo called `mykd-studio` and push this folder. The GitHub username is `mykd-ltd`, already set in `release.json`.
2. **Studio page.** Upload `docs/soulitude7/design-system/` into the `soulitude7` folder of the existing `studio.mykd.co.uk` site on your cPanel hosting. GitHub Pages is not used.
3. **Form.** Create a form at Formspree (or any service that accepts a JSON POST) with email notifications to michael@mykd.co.uk. Put its endpoint in `release.json` under `form_endpoint` and rebuild. Until then, the form opens the user's email app with the entry filled in.
4. **Sharing.** Share the design system, the template deck and the social tiles canvas with each user's Claude email.
5. **Each user.** Send the page link. They follow Before you start and Install, then ask Claude to check the Soulitude7 system. A clean check means the install worked.

## Releasing a change

Design system changes: publish them to the design system in Claude. No release. Add a line to the next release notes if users should know. The design system is the only master for every template (release 1.1.0). The template deck, the social tiles canvas and the brochure canvas are previews: never edit them to change a template.

Changing a template:

1. Ask Claude to build a working copy of the templates to change, as a deck or a canvas, from the design system.
2. Edit the working copy by hand.
3. Ask Claude to push the changes back. Claude compares each edited slide or artboard with its master file and copies the changes into `deck/slides/`, `social/tiles/` or `brochure/pages/`. It also updates `deck.md`, `social.md`, `brochure.md` or the card README where a rule has changed, then publishes.
4. Ask Claude to rebuild the previews if they should show the change. Each preview is labelled with the design system version it was built from.

Three things make step 3 cleaner:

- **New images.** Any image added on the working copy is added to the design system's asset groups first. Claude then switches the template to the design system's id for it.
- **Template names.** Keep each artboard or slide name close to the template it came from, so it is clear which master it updates. A brand new layout is fine too. Say that it is new.
- **Rules.** If a change alters a rule, such as spacing or when to use a layout, say so. Claude writes it into the guidance as well as the file.

Skill changes:

1. Edit the skill in `plugins/soulitude7/skills/`.
2. Pick the version in `release.json`:
   - patch (1.0.1): a fix, nothing looks different
   - minor (1.1.0): a new layout, format or skill step
   - major (2.0.0): a rule changed and older skills would build off brand
3. Add a history entry at the top of `release.json` with the date, type, action and notes.
4. Run `python3 tools/build.py`. It stamps the version, writes the manifest, rebuilds the zips and writes the version, links and notes into the page. It stops if the history entry is missing or a skill's frontmatter is wrong.
5. Commit, tag and push in GitHub Desktop, then upload `docs/soulitude7/design-system/` to your hosting. The tag matters: review.py diffs user edits against it.
6. For a major release, email each user on the day.

Desktop users with Sync automatically turned on receive the release without action. Web users swap the four skills.

## Reviewing local changes

Changes reach you three ways:

1. **Logged entries** from the form: a rule set aside for one document, a new layout or style, a local rule, a skill edit or a problem. Each carries the user, skill, release, what changed, why and a link.
2. **Check reports** pasted into the form. Save the report as JSON and run `python3 tools/review.py report.json`. It writes `reviews/<date>-<user>-<release>.md` with a diff of every edited file against the release tag and the text of any added file.
3. **Local rules files.** Ask each user for their `s7-local.md` before a minor or major release.

Before each release, go through every entry and review file and record one decision against each:

- **Adopt.** Add it to the design system or the skills, and note it in the release notes.
- **Keep local.** It suits one user and stays in their `s7-local.md`.
- **Reverse.** It breaks the brand. Tell the user why and what to use instead.

Write the decision in the review file, and reply to the user. The page tells users they will hear the decision, so this step closes the loop.

## Test before rollout

These have not been proven in a client account yet. Run each with a test Claude account before sending the page to Lisa-Marie or Clare.

1. **Cross-account reads.** The skills read the design system files by path. Confirm a user's Claude can read `project/README.md` from your shared design system. If it cannot, the fallback is to bundle a snapshot of the design system files into the plugin and treat every design system change as a release.
2. **Marketplace sync.** Anthropic's documentation says Check for updates pulls the latest release and Cowork warns before overwriting local edits. Public bug reports describe personal GitHub marketplaces failing to re-sync. Test an update from 1.0.0 to 1.0.1. If it fails, users fall back to the plugin zip.
3. **Public repo.** A marketplace added by a user without GitHub access needs a public repo. The skills hold Soulitude7 brand rules and links to your shared artifacts, though the artifacts stay private to the people you share them with. Get Lisa-Marie's agreement before the repo goes public.
4. **check.py on the web.** On claude.ai the script runs in Claude's sandbox. Confirm it finds the uploaded skills. If it reports them as not found, users send their skill files by email instead.
5. **Design system link in s7-social-tile.** Closed 20 October 2026. `claude.ai/code/artifact/d43cfe38…` and `claude.ai/artifact/TD4zmiVXgsGu95xEFvjZ4p` are the same artifact. Every skill now uses the second form (release 1.1.0).
6. **Footer.** The shared footer's Cookie settings button does nothing on this page, because the page sets no cookies and has no cookie bar. Decide whether the footer component should hide it on pages without a bar.

## A simpler route if Soulitude7 grows

If Soulitude7 moves to a Claude Team plan, an Owner syncs the `mykd-studio` repo from the organisation settings and marks the plugin as required. It then installs and updates for everyone automatically, and the studio page only carries the change log and release notes.

## Sources

- [Use skills in Claude](https://support.claude.com/en/articles/12512180-use-skills-in-claude)
- [Install plugins (Cowork)](https://claude.com/docs/cowork/guide/plugins)
- [Manage plugins for your organisation](https://support.claude.com/en/articles/13837433-manage-claude-cowork-plugins-for-your-organization)
- [Report: personal marketplace never re-syncs](https://claudeissues.com/issue/73907-cowork-personal-marketplace-never-re-syncs-update-reports-latest-version-while-r)
