#!/usr/bin/env python3
"""Build a Soulitude7 release.

Reads release.json and:
1. stamps the version into plugin.json and marketplace.json
2. writes skills/s7-system/manifest.json (sha256 of every managed file)
3. zips each skill, and the whole plugin, into the studio page downloads folder
4. writes the version, release date, links and release notes into the studio page
5. copies release.json next to the page so anyone can check the latest version

Run from the repo root: python3 tools/build.py
Then commit, tag (git tag v<version>) and push. GitHub Pages publishes docs/.
"""
import hashlib, html, json, os, re, shutil, sys, zipfile

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
REL = json.load(open(os.path.join(ROOT, "release.json"), encoding="utf-8"))
PLUGIN = os.path.join(ROOT, "plugins", REL["plugin"])
SKILLS = os.path.join(PLUGIN, "skills")
PAGE_DIR = os.path.join(ROOT, "docs", "soulitude7", "design-system")
DL = os.path.join(PAGE_DIR, "downloads")
V = REL["version"]
FIXED_TIME = (2026, 1, 1, 0, 0, 0)  # stable zip bytes for identical content


def managed_files():
    for skill in sorted(os.listdir(SKILLS)):
        sdir = os.path.join(SKILLS, skill)
        if not os.path.isdir(sdir):
            continue
        for dp, dns, fns in os.walk(sdir):
            dns[:] = sorted(d for d in dns if d != "__pycache__" and not d.startswith("."))
            for fn in sorted(fns):
                if fn.startswith(".") or fn == "manifest.json":
                    continue
                full = os.path.join(dp, fn)
                yield skill, os.path.relpath(full, SKILLS).replace(os.sep, "/"), full


def check_frontmatter():
    for skill in sorted(os.listdir(SKILLS)):
        p = os.path.join(SKILLS, skill, "SKILL.md")
        t = open(p, encoding="utf-8").read()
        m = re.match(r'---\nname: "?([^"\n]+)"?\ndescription: "?(.+?)"?\n---', t)
        if not m or m.group(1) != skill:
            sys.exit("SKILL.md frontmatter name must match its folder: " + skill)
        if len(m.group(2)) > 1024:
            sys.exit("Description over 1024 characters: " + skill)


def stamp_json(path, fn):
    d = json.load(open(path, encoding="utf-8"))
    fn(d)
    with open(path, "w", encoding="utf-8") as f:
        json.dump(d, f, indent=2, ensure_ascii=False)
        f.write("\n")


def zwrite(z, full, arc):
    zi = zipfile.ZipInfo(arc, FIXED_TIME)
    zi.compress_type = zipfile.ZIP_DEFLATED
    zi.external_attr = 0o644 << 16
    z.writestr(zi, open(full, "rb").read())


def build_zips():
    if os.path.isdir(DL):
        for fn in os.listdir(DL):
            if fn.endswith(".zip"):
                os.remove(os.path.join(DL, fn))
    os.makedirs(DL, exist_ok=True)
    files = list(managed_files())
    files += [(s, "%s/manifest.json" % s, os.path.join(SKILLS, s, "manifest.json")) for s in ["s7-system"]]
    out = {}
    for skill in sorted({f[0] for f in files}):
        name = "%s.zip" % skill
        with zipfile.ZipFile(os.path.join(DL, name), "w") as z:
            for s, arc, full in sorted(files, key=lambda x: x[1]):
                if s == skill:
                    zwrite(z, full, arc)
        out[skill] = name
    # all four skills in one zip, for people who upload skill files
    with zipfile.ZipFile(os.path.join(DL, "soulitude7-skills-%s.zip" % V), "w") as z:
        for skill, name in out.items():
            zwrite(z, os.path.join(DL, name), name)
    # whole plugin, for upload on the Plugins page
    with zipfile.ZipFile(os.path.join(DL, "soulitude7-plugin-%s.zip" % V), "w") as z:
        for dp, dns, fns in os.walk(PLUGIN):
            dns[:] = sorted(d for d in dns if d != "__pycache__")
            for fn in sorted(fns):
                if fn.startswith(".") and fn != ".claude-plugin":
                    continue
                full = os.path.join(dp, fn)
                zwrite(z, full, os.path.relpath(full, PLUGIN).replace(os.sep, "/"))
    shutil.copy(os.path.join(ROOT, "templates", "s7-local.md"), os.path.join(DL, "s7-local.md"))
    return out


def fill(page, key, value):
    pat = re.compile(r"(<!-- build:%s -->).*?(<!-- /build:%s -->)" % (key, key), re.S)
    if not pat.search(page):
        sys.exit("Missing build marker in page: " + key)
    return pat.sub(lambda m: m.group(1) + value + m.group(2), page)


def esc(s):
    return html.escape(s, quote=True)


def render_page(zips):
    p = os.path.join(PAGE_DIR, "index.html")
    page = open(p, encoding="utf-8").read()
    page = fill(page, "version", esc(V))
    page = fill(page, "released", esc(nice_date(REL["released"])))
    page = fill(page, "repo", esc(REL["repo"]))
    page = fill(page, "plugin-zip", '<a class="btn" href="downloads/soulitude7-plugin-%s.zip" download>Download the plugin (%s)</a>' % (esc(V), esc(V)))
    page = fill(page, "skills-zip", '<a class="btn" href="downloads/soulitude7-skills-%s.zip" download>Download the four skills (%s)</a>' % (esc(V), esc(V)))
    links = "".join(
        '<li><a href="%s" target="_blank" rel="noopener">%s</a><span>%s</span></li>' % (esc(l["url"]), esc(l["name"]), esc(l["note"]))
        for l in REL["shared_links"])
    page = fill(page, "links", links)
    rows = []
    for h in REL["history"]:
        notes = "".join("<li>%s</li>" % esc(n) for n in h["notes"])
        rows.append(
            '<article class="rel"><div class="rel-meta"><span class="rel-v">%s</span><span>%s</span></div>'
            '<div><p class="rel-type"><strong>%s.</strong> %s</p><ul>%s</ul></div></article>'
            % (esc(h["version"]), esc(nice_date(h["date"])), esc(h["type"]), esc(h["action"]), notes))
    page = fill(page, "history", "".join(rows))
    page = fill(page, "config", '<script id="studio-config" type="application/json">%s</script>' % json.dumps(
        {"version": V, "endpoint": REL["form_endpoint"], "contact": REL["contact"]}))
    open(p, "w", encoding="utf-8").write(page)


def nice_date(iso):
    y, m, d = iso.split("-")
    months = "January February March April May June July August September October November December".split()
    return "%d %s %s" % (int(d), months[int(m) - 1], y)


def main():
    if not re.fullmatch(r"\d+\.\d+\.\d+", V):
        sys.exit("version must be MAJOR.MINOR.PATCH")
    if REL["history"][0]["version"] != V:
        sys.exit("Add a history entry for %s at the top of release.json first" % V)
    check_frontmatter()
    stamp_json(os.path.join(PLUGIN, ".claude-plugin", "plugin.json"), lambda d: d.__setitem__("version", V))
    stamp_json(os.path.join(ROOT, ".claude-plugin", "marketplace.json"),
               lambda d: [p.__setitem__("version", V) for p in d["plugins"] if p["name"] == REL["plugin"]])
    files = {rel: hashlib.sha256(open(full, "rb").read()).hexdigest() for _, rel, full in managed_files()}
    man = {"plugin": REL["plugin"], "version": V, "released": REL["released"],
           "design_system": REL["design_system"], "files": files}
    with open(os.path.join(SKILLS, "s7-system", "manifest.json"), "w", encoding="utf-8") as f:
        json.dump(man, f, indent=2)
        f.write("\n")
    zips = build_zips()
    render_page(zips)
    shutil.copy(os.path.join(ROOT, "release.json"), os.path.join(PAGE_DIR, "release.json"))
    print("Built %s %s: %d managed files, %d skill zips" % (REL["plugin"], V, len(files), len(zips)))
    print("Next: git add -A && git commit -m 'Release %s' && git tag v%s && git push --tags origin main" % (V, V))


if __name__ == "__main__":
    main()
