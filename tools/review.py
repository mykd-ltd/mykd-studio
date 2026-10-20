#!/usr/bin/env python3
"""Turn a user's s7-check report into a review file MYKD can read.

For every edited file, diffs the user's text against the same file at the
release the user had installed (git tag v<release>). Added files are shown
whole. Writes reviews/<date>-<user>-<release>.md.

Usage: python3 tools/review.py path/to/s7-check-report.json
"""
import difflib, json, os, subprocess, sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
PLUGIN = json.load(open(os.path.join(ROOT, "release.json"), encoding="utf-8"))["plugin"]


def released_text(release, rel):
    path = "plugins/%s/skills/%s" % (PLUGIN, rel)
    try:
        return subprocess.check_output(["git", "-C", ROOT, "show", "v%s:%s" % (release, path)],
                                       stderr=subprocess.DEVNULL).decode("utf-8"), "tag v" + release
    except Exception:
        p = os.path.join(ROOT, path)
        if os.path.exists(p):
            return open(p, encoding="utf-8").read(), "working copy (tag v%s not found)" % release
        return "", "nothing (file not in repo)"


def main():
    if len(sys.argv) != 2:
        sys.exit(__doc__)
    r = json.load(open(sys.argv[1], encoding="utf-8"))
    out = ["# Soulitude7 drift review", "",
           "- User: %s" % r.get("user"), "- Installed release: %s" % r["release"],
           "- Checked: %s" % r.get("checked"), "- Summary: %s" % r.get("summary"), "",
           "Decide for each item: adopt into the system, keep as a local rule, or reverse.", ""]
    for s in r["skills"]:
        out.append("## %s: %s" % (s["skill"], s["status"]))
        if s.get("folder"):
            out.append("Folder: `%s`" % s["folder"])
        for e in s.get("edited", []):
            base, src = released_text(r["release"], "%s/%s" % (s["skill"], e["file"]))
            diff = difflib.unified_diff(base.splitlines(), (e["text"] or "").splitlines(),
                                        "release/" + e["file"], "user/" + e["file"], lineterm="", n=2)
            out += ["", "### Edited: %s (compared with %s)" % (e["file"], src), "", "```diff", *diff, "```"]
        for e in s.get("extra", []):
            out += ["", "### Added: %s" % e["file"], "", "```", e["text"] or "(binary)", "```"]
        for m in s.get("missing", []):
            out += ["", "### Missing: %s" % m]
        if s.get("status") == "differs from release":
            out += ["", "Decision: ", ""]
        else:
            out.append("")
    os.makedirs(os.path.join(ROOT, "reviews"), exist_ok=True)
    name = "%s-%s-%s.md" % ((r.get("checked") or "undated")[:10], (r.get("user") or "user").replace(" ", "-").lower(), r["release"])
    path = os.path.join(ROOT, "reviews", name)
    open(path, "w", encoding="utf-8").write("\n".join(out) + "\n")
    print("Review written: " + path)


if __name__ == "__main__":
    main()
