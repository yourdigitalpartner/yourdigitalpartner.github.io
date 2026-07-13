#!/usr/bin/env python3
"""
ensure_tracking.py — guarantees every published HTML page carries the
HubSpot tracking loader (portal 146760313, EU1).

Run from the repo root before every push (same pattern as gen_sitemap.py):

    python3 scripts/ensure_tracking.py

Behaviour:
  - Scans every *.html file in the repo (excluding .git).
  - If a page already has the loader: leaves it untouched.
  - If a page is missing it: injects the standard snippet immediately
    before </head>, matching the placement used on the core pages.
  - Idempotent: safe to run any number of times, never double-injects.
  - Exit code 0 if all pages were already tracked, 1 if any were fixed
    (so it can double as a CI check: fixes locally, flags in CI).
"""

import sys
from pathlib import Path

PORTAL_MARKER = "hs-scripts.com/146760313"

SNIPPET = (
    "    <!-- Start of HubSpot Embed Code -->\n"
    '    <script type="text/javascript" id="hs-script-loader" async defer '
    'src="//js-eu1.hs-scripts.com/146760313.js"></script>\n'
    "    <!-- End of HubSpot Embed Code -->\n"
    "</head>"
)

def main() -> int:
    repo_root = Path(__file__).resolve().parent.parent
    fixed, ok, skipped = [], [], []

    for path in sorted(repo_root.rglob("*.html")):
        if ".git" in path.parts:
            continue
        html = path.read_text(encoding="utf-8")

        if PORTAL_MARKER in html:
            ok.append(path)
            continue

        if html.count("</head>") != 1:
            # Malformed or fragment file — flag it, never guess.
            skipped.append(path)
            continue

        path.write_text(html.replace("</head>", SNIPPET, 1), encoding="utf-8")
        fixed.append(path)

    rel = lambda p: p.relative_to(repo_root)
    for p in fixed:
        print(f"INJECTED : {rel(p)}")
    for p in skipped:
        print(f"SKIPPED (no single </head>, fix manually): {rel(p)}")
    print(f"\n{len(ok)} already tracked, {len(fixed)} injected, {len(skipped)} skipped")

    return 1 if (fixed or skipped) else 0

if __name__ == "__main__":
    sys.exit(main())
