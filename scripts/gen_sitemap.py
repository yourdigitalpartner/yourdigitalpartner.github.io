#!/usr/bin/env python3
"""Regenerate sitemap.xml for your-digital-partner.co.uk.

Auto-discovers every indexable page: walks all index.html files, includes a page
iff it declares a <link rel="canonical"> and is NOT marked noindex and is NOT
disallowed in robots.txt. The canonical href is used as the <loc>. lastmod is the
file's last git commit date. No manual list to maintain — new pages of any type
(blog posts, solution pages, nested guides) are picked up automatically.

Run from the repo root before committing:  python3 scripts/gen_sitemap.py
Do NOT hand-edit sitemap.xml.
"""
import re, subprocess, datetime, pathlib

ROOT = pathlib.Path(__file__).resolve().parent.parent
BASE = "https://your-digital-partner.co.uk"
TODAY = datetime.date.today().isoformat()

CANON_RE = re.compile(r'<link[^>]*rel="canonical"[^>]*href="([^"]+)"', re.I)
NOINDEX_RE = re.compile(r'<meta[^>]*name="robots"[^>]*content="[^"]*noindex', re.I)

def robots_disallows():
    rob = ROOT / "robots.txt"
    out = []
    if rob.exists():
        for line in rob.read_text().splitlines():
            if line.lower().startswith("disallow:"):
                p = line.split(":", 1)[1].strip()
                if p:
                    out.append(p)
    return out

DISALLOW = robots_disallows()

def git_date(path):
    try:
        d = subprocess.run(["git", "log", "-1", "--format=%cs", "--", str(path)],
                           cwd=ROOT, capture_output=True, text=True).stdout.strip()
        return d or TODAY
    except Exception:
        return TODAY

def priority(path):
    segs = [s for s in path.split("/") if s]
    if path == "/": return "1.0"
    if path.startswith("/solutions/"): return "0.9"
    if path == "/success-stories/": return "0.8"
    if path == "/blog/": return "0.7"
    if len(segs) >= 3: return "0.5"           # nested guides e.g. .../interactive-guide/
    if path.startswith("/blog/"): return "0.6"  # blog posts
    return "0.6"

def loc_path(url):
    return url[len(BASE):] if url.startswith(BASE) else url

entries = {}  # canonical -> (lastmod, priority)  (dict dedupes shared canonicals)
for f in sorted(ROOT.rglob("index.html")):
    if ".git" in f.parts:
        continue
    html = f.read_text(errors="ignore")
    if NOINDEX_RE.search(html):
        continue
    m = CANON_RE.search(html)
    if not m:
        continue
    canon = m.group(1).strip()
    path = loc_path(canon)
    if any(path.startswith(d) for d in DISALLOW):
        continue
    entries[canon] = (git_date(f), priority(path))

# Order: home first, then by priority desc, then alphabetically for stability
order = sorted(entries.items(), key=lambda kv: (kv[0] != BASE + "/", -float(kv[1][1]), kv[0]))

lines = ['<?xml version="1.0" encoding="UTF-8"?>',
         '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">']
for loc, (lastmod, pri) in order:
    lines.append(f'  <url><loc>{loc}</loc><lastmod>{lastmod}</lastmod><priority>{pri}</priority></url>')
lines.append('</urlset>')
(ROOT / "sitemap.xml").write_text("\n".join(lines) + "\n")
print(f"Wrote sitemap.xml with {len(order)} URLs")
