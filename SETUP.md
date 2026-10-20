# Setup guide: GitHub, the studio page and the change log form

A one-off setup, about an hour of work. Everything here is free. No coding and no command line: Claude runs the build in your folder, and the GitHub Desktop app publishes it.

## What each service does

| Service | What it does here | Cost |
| --- | --- | --- |
| GitHub account | Hosts the skills: the marketplace users add in Claude | Free |
| GitHub Desktop | Publishes changes from your `mykd-studio` folder to GitHub, with buttons instead of commands | Free |
| Your hosting (cPanel) | Serves the page at `studio.mykd.co.uk`, alongside your existing studio pages | Already paid for |
| Formspree | Receives the Log a change form and emails each entry to you | Free plan (about 50 entries a month, check their pricing page) |

## 1. Create a GitHub account

1. Go to github.com/signup and sign up with michael@mykd.co.uk.
2. Username: `mykd-ltd`. It appears in the address users type into Claude: `mykd-ltd/mykd-studio`.
3. Turn on two-factor authentication when GitHub asks.
4. Done: the username is set in `release.json` and the page is rebuilt.

## 2. Install GitHub Desktop

1. Download it from desktop.github.com and install it.
2. Open it and sign in with the GitHub account.
3. Set your name and email (michael@mykd.co.uk) when it asks how to label your changes.

## 3. Put the folder on GitHub

The `mykd-studio` folder is already set up as a Git repository, with release 1.0.0 saved and tagged.

1. In GitHub Desktop: File, Add Local Repository. Choose `00 mykd/clients/soulitude7/Claude design system/mykd-studio`.
2. Select **Publish repository**. Keep the name `mykd-studio`.
3. **Keep this code private**: untick it only once Lisa-Marie has agreed. Users without a GitHub account can add only a public marketplace. Until she agrees, leave it ticked and test with your own account.
4. Select **Publish repository**.
5. On github.com, open the repository and select **Tags**. If `v1.0.0` is not listed, go to **Releases**, **Draft a new release**, type `v1.0.0` as the tag, select the latest commit and publish.

## 4. Switch off GitHub Pages

`studio.mykd.co.uk` already runs on your own hosting (cPanel), with pages such as `/soulitude7/`. The design system page goes there too, so GitHub Pages is not needed. GitHub still hosts the marketplace, which needs no web page.

1. On github.com, open the repository, then **Settings**, **Pages**.
2. Under **Custom domain**, select **Remove**.
3. Under **Build and deployment**, set Branch to **None** and save.
4. Leave the DNS records at GoDaddy as they are. The A record for `studio` must stay.

## 5. Upload the page to studio.mykd.co.uk

1. In cPanel, open **File Manager** and go to the folder that serves `studio.mykd.co.uk`, then into its `soulitude7` folder. It is the folder holding the files you see at `https://studio.mykd.co.uk/soulitude7/`.
2. Upload `mykd-studio/upload/studio-design-system-<version>.zip` into the `soulitude7` folder, select it and choose **Extract**, then delete the zip. The build makes this zip with the permissions the web server needs (folders 755, files 644). A zip made in Finder can extract with permissions that cause a 403 Forbidden error.
3. Check `https://studio.mykd.co.uk/soulitude7/design-system/` opens, shows the MYKD logo and the download buttons work.

## 6. Connect the form

1. Sign up at formspree.io with michael@mykd.co.uk.
2. Create a form called `Soulitude7 change log`. Set notifications to michael@mykd.co.uk.
3. In the form's settings, restrict it to the domain `studio.mykd.co.uk`, if offered, to cut spam.
4. Copy the form endpoint. It looks like `https://formspree.io/f/abcd1234`.
5. Give it to Claude. Claude adds it to `release.json` and rebuilds the page.
6. In GitHub Desktop, write a summary such as `Add form endpoint`, select **Commit to main**, then **Push origin**.

Until this is done, the form opens the user's email app with the entry filled in, so nothing is lost.

## 7. Test it yourself

1. Open the page on your phone and your Mac. Send a test entry through the form and check the email arrives.
2. In the Claude desktop app: Customize, Plugins, Add marketplace, enter `mykd-ltd/mykd-studio`, install Soulitude7.
3. Start a chat and ask Claude to check the Soulitude7 system. It should report release 1.0.0 and no differences.
4. Run the other checks in PROCESS.md under "Test before rollout" with a second Claude account before sending the page to a client.

## Every release after this

1. Ask Claude to make the skill change and build release 1.0.1 (or whichever number). Claude edits the files, updates the release notes and runs the build in your folder.
2. In GitHub Desktop: write a summary such as `Release 1.0.1`, then **Commit to main**.
3. In the **History** tab, right-click that commit, **Create Tag**, enter `v1.0.1`.
4. Select **Push origin**. The marketplace updates within a few minutes.
5. In cPanel File Manager, upload `upload/studio-design-system-<version>.zip` into the `soulitude7` folder, choose **Extract** and allow it to overwrite, then delete the zip.

Desktop users with Sync automatically turned on receive the release without doing anything.
