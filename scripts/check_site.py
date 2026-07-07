from __future__ import annotations

from html.parser import HTMLParser
from pathlib import Path
from urllib.parse import urlsplit
import re
import sys

ROOT = Path(__file__).resolve().parents[1]
HTML_FILES = sorted(p for p in ROOT.rglob("*.html") if ".git" not in p.parts)
ERRORS: list[str] = []


class PageParser(HTMLParser):
    def __init__(self) -> None:
        super().__init__(convert_charrefs=True)
        self.title = ""
        self.in_title = False
        self.description = False
        self.viewport = False
        self.canonical = False
        self.ids: list[str] = []
        self.hrefs: list[str] = []
        self.scripts: list[str] = []
        self.styles: list[str] = []

    def handle_starttag(self, tag: str, attrs_list: list[tuple[str, str | None]]) -> None:
        attrs = dict(attrs_list)
        if tag == "title":
            self.in_title = True
        if tag == "meta" and attrs.get("name") == "description":
            self.description = bool(attrs.get("content"))
        if tag == "meta" and attrs.get("name") == "viewport":
            self.viewport = True
        if tag == "link" and attrs.get("rel") == "canonical":
            self.canonical = bool(attrs.get("href"))
        if tag == "link" and attrs.get("rel") == "stylesheet" and attrs.get("href"):
            self.styles.append(attrs["href"])
        if tag == "script" and attrs.get("src"):
            self.scripts.append(attrs["src"])
        if attrs.get("id"):
            self.ids.append(attrs["id"])
        if tag == "a" and attrs.get("href"):
            self.hrefs.append(attrs["href"])

    def handle_endtag(self, tag: str) -> None:
        if tag == "title":
            self.in_title = False

    def handle_data(self, data: str) -> None:
        if self.in_title:
            self.title += data.strip()


def route_to_file(path: str) -> Path:
    clean = path.split("?", 1)[0]
    if clean == "/":
        return ROOT / "index.html"
    candidate = ROOT / clean.lstrip("/")
    if candidate.suffix:
        return candidate
    return candidate / "index.html"


for path in HTML_FILES:
    rel = path.relative_to(ROOT)
    text = path.read_text(encoding="utf-8")
    parser = PageParser()
    try:
        parser.feed(text)
    except Exception as exc:
        ERRORS.append(f"{rel}: HTML parser failed: {exc}")
        continue

    if not parser.title:
        ERRORS.append(f"{rel}: missing title")
    if not parser.viewport:
        ERRORS.append(f"{rel}: missing viewport meta tag")
    if rel.name != "404.html" and not parser.description:
        ERRORS.append(f"{rel}: missing meta description")
    if rel.name != "404.html" and not parser.canonical:
        ERRORS.append(f"{rel}: missing canonical link")
    duplicates = sorted({item for item in parser.ids if parser.ids.count(item) > 1})
    if duplicates:
        ERRORS.append(f"{rel}: duplicate ids: {', '.join(duplicates)}")
    if "flex-wrap:gap" in text:
        ERRORS.append(f"{rel}: invalid CSS declaration flex-wrap:gap")

    if "<nav" in text:
        if "mobile-menu-toggle" not in text:
            ERRORS.append(f"{rel}: navigation has no mobile menu toggle")
        if "solutions-toggle" not in text:
            ERRORS.append(f"{rel}: Solutions menu is not keyboard/click accessible")
        if "/assets/site-enhancements.css" not in parser.styles:
            ERRORS.append(f"{rel}: shared enhancement stylesheet missing")
        if "/assets/site-enhancements.js" not in parser.scripts:
            ERRORS.append(f"{rel}: shared enhancement script missing")

    page_ids = set(parser.ids)
    for href in parser.hrefs:
        if href.startswith(("http://", "https://", "mailto:", "tel:", "javascript:")):
            continue
        parts = urlsplit(href)
        if href.startswith("#"):
            if parts.fragment and parts.fragment not in page_ids:
                ERRORS.append(f"{rel}: missing local anchor #{parts.fragment}")
            continue
        if not href.startswith("/"):
            continue
        target = route_to_file(parts.path)
        if not target.exists():
            ERRORS.append(f"{rel}: broken internal link {href}")
            continue
        if parts.fragment and target.suffix == ".html":
            target_text = target.read_text(encoding="utf-8")
            if not re.search(rf'id=["\']{re.escape(parts.fragment)}["\']', target_text):
                ERRORS.append(f"{rel}: missing target anchor {href}")

required = [
    ROOT / "robots.txt",
    ROOT / "sitemap.xml",
    ROOT / "404.html",
    ROOT / "privacy/index.html",
    ROOT / "assets/site-enhancements.css",
    ROOT / "assets/site-enhancements.js",
]
for item in required:
    if not item.exists():
        ERRORS.append(f"Missing required file: {item.relative_to(ROOT)}")

sticky_expectations = {
    "index.html": ("Free AEO audit", "#scorecard"),
    "success-stories/index.html": ("Let's talk growth", "#contact"),
    "solutions/seo-aeo-visibility/index.html": ("Free AEO audit", "#scorecard"),
    "solutions/website-optimisation-cro/index.html": ("Free website review", "#review"),
    "solutions/paid-campaigns/index.html": ("Free ad audit", "#audit"),
}
for rel, (label, target) in sticky_expectations.items():
    text = (ROOT / rel).read_text(encoding="utf-8")
    if f'data-mobile-cta="{label}"' not in text or f'data-mobile-target="{target}"' not in text:
        ERRORS.append(f"{rel}: incorrect mobile sticky CTA configuration")

if ERRORS:
    print("Site checks failed:\n")
    for error in ERRORS:
        print(f"- {error}")
    sys.exit(1)

print(f"Site checks passed for {len(HTML_FILES)} HTML files.")
