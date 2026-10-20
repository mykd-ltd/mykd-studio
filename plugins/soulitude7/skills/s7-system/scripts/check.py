#!/usr/bin/env python3
"""Compare the installed Soulitude7 skills with the release manifest.

Writes a JSON report listing every managed file as unchanged, edited or
missing, plus any extra files, with the full text of edited and extra
files so MYKD can diff them against the release.

Usage: python3 check.py [--root DIR ...] [--out report.json] [--user NAME]
"""
import argparse, hashlib, json, os, sys, datetime, getpass

HERE = os.path.dirname(os.path.abspath(__file__))
MANIFEST = os.path.join(os.path.dirname(HERE), "manifest.json")
# The folder that holds this skill holds the other installed skills too, so search it first.
SKILLS_HOME = os.path.dirname(os.path.dirname(HERE))
DEFAULT_ROOTS = [SKILLS_HOME, "~/.claude", "/mnt/skills", "~/.config/claude", "~/Library/Application Support/Claude", "."]
MAX_TEXT = 200_000


def sha(path):
    h = hashlib.sha256()
    with open(path, "rb") as f:
        for chunk in iter(lambda: f.read(65536), b""):
            h.update(chunk)
    return h.hexdigest()


def find_installs(roots, names):
    """Return {skill_name: [folder, ...]} for folders named like a managed skill holding SKILL.md.

    A plugin install may prefix the folder name, as in "soulitude7:s7-deck", so a folder
    matches when its name is the skill name or ends with ":" plus the skill name."""
    found = {n: [] for n in names}
    seen = set()
    for root in roots:
        root = os.path.expanduser(root)
        if not os.path.isdir(root):
            continue
        for dirpath, dirnames, filenames in os.walk(root):
            dirnames[:] = [d for d in dirnames if not d.startswith(".git") and d != "node_modules"]
            base = os.path.basename(dirpath).rsplit(":", 1)[-1]
            if base in found and "SKILL.md" in filenames:
                real = os.path.realpath(dirpath)
                if real not in seen:
                    seen.add(real)
                    found[base].append(dirpath)
    return found


def read_text(path):
    try:
        with open(path, "r", encoding="utf-8") as f:
            t = f.read()
        return t if len(t) <= MAX_TEXT else t[:MAX_TEXT] + "\n[truncated]"
    except (UnicodeDecodeError, OSError):
        return None


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--root", action="append", help="folder to search (repeatable)")
    ap.add_argument("--out", default="s7-check-report.json")
    ap.add_argument("--user", default=None)
    a = ap.parse_args()

    with open(MANIFEST, encoding="utf-8") as f:
        man = json.load(f)
    files = man["files"]  # "skill/rel/path" -> sha256
    skills = sorted({k.split("/", 1)[0] for k in files})
    installs = find_installs(a.root or DEFAULT_ROOTS, skills)

    report = {
        "report": "s7-check",
        "release": man["version"],
        "released": man.get("released"),
        "checked": datetime.datetime.now().isoformat(timespec="seconds"),
        "user": a.user or getpass.getuser(),
        "skills": [],
    }
    drift = 0
    notfound = 0
    for s in skills:
        managed = {k.split("/", 1)[1]: v for k, v in files.items() if k.startswith(s + "/")}
        if not installs[s]:
            report["skills"].append({"skill": s, "status": "not found"})
            notfound += 1
            continue
        for folder in installs[s]:
            entry = {"skill": s, "folder": folder, "edited": [], "missing": [], "extra": [], "unchanged": 0}
            for rel, digest in managed.items():
                p = os.path.join(folder, rel)
                if not os.path.exists(p):
                    entry["missing"].append(rel)
                elif sha(p) != digest:
                    entry["edited"].append({"file": rel, "text": read_text(p)})
                else:
                    entry["unchanged"] += 1
            for dp, _, fns in os.walk(folder):
                for fn in fns:
                    rel = os.path.relpath(os.path.join(dp, fn), folder).replace(os.sep, "/")
                    if rel not in managed and rel != "manifest.json" and "__pycache__" not in rel and not fn.startswith("."):
                        entry["extra"].append({"file": rel, "text": read_text(os.path.join(dp, fn))})
            n = len(entry["edited"]) + len(entry["missing"]) + len(entry["extra"])
            entry["status"] = "matches release" if n == 0 else "differs from release"
            drift += n
            report["skills"].append(entry)

    if notfound:
        report["summary"] = "%d skill(s) not found; run again with --root set to the folder that holds the installed skills" % notfound
    elif drift == 0:
        report["summary"] = "matches release %s" % man["version"]
    else:
        report["summary"] = "%d file(s) differ from release %s" % (drift, man["version"])
    with open(a.out, "w", encoding="utf-8") as f:
        json.dump(report, f, indent=2, ensure_ascii=False)

    print("Soulitude7 check: " + report["summary"])
    for e in report["skills"]:
        if e["status"] == "not found":
            print("  %s: not found" % e["skill"])
            continue
        bits = []
        if e["edited"]: bits.append("edited " + ", ".join(x["file"] for x in e["edited"]))
        if e["missing"]: bits.append("missing " + ", ".join(e["missing"]))
        if e["extra"]: bits.append("added " + ", ".join(x["file"] for x in e["extra"]))
        print("  %s: %s%s" % (e["skill"], e["status"], (" (" + "; ".join(bits) + ")") if bits else ""))
    print("Report: " + os.path.abspath(a.out))
    return 0


if __name__ == "__main__":
    sys.exit(main())
