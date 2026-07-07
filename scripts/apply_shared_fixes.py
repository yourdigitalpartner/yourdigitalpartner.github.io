from pathlib import Path
import re

root = Path(__file__).resolve().parents[1]
og_image = "https://146760313.fs1.hubspotusercontent-eu1.net/hubfs/146760313/6B24F59D-9FF0-4D55-BBBA-9A13BC08B8A5.png"

pages = {
    "index.html": ("home", "B2B SEO, AEO & Website CRO | Your Digital Partner", "Win more visibility in Google and AI search, convert more website visitors and build measurable B2B pipeline with senior, hands-on digital marketing support.", "https://your-digital-partner.co.uk/", "Free AEO audit", "#scorecard"),
    "success-stories/index.html": ("success-stories", "B2B Marketing Results & Case Studies | Your Digital Partner", "See documented B2B results across SEO, AEO, website CRO, Google Ads and LinkedIn Ads, including AI visibility growth and pipeline generated.", "https://your-digital-partner.co.uk/success-stories/", "Let's talk growth", "#contact"),
    "solutions/seo-aeo-visibility/index.html": ("seo-aeo", "B2B SEO & AEO Services | Your Digital Partner", "Improve B2B visibility in Google and AI answers with technical SEO, schema, answer-first content and a practical AEO programme built around commercial prompts.", "https://your-digital-partner.co.uk/solutions/seo-aeo-visibility/", "Free AEO audit", "#scorecard"),
    "solutions/website-optimisation-cro/index.html": ("cro", "B2B Website Optimisation & CRO | Your Digital Partner", "Turn more B2B website traffic into leads with heatmaps, session recordings, A/B testing, personalisation and conversion-focused interactive journeys.", "https://your-digital-partner.co.uk/solutions/website-optimisation-cro/", "Free website review", "#review"),
    "solutions/paid-campaigns/index.html": ("paid", "B2B Google & LinkedIn Ads | Your Digital Partner", "Build measurable B2B pipeline with Google Ads and LinkedIn campaigns, precise targeting, conversion-led landing pages and continuous optimisation against revenue.", "https://your-digital-partner.co.uk/solutions/paid-campaigns/", "Free ad audit", "#audit"),
    "solutions/ai-marketing/index.html": ("ai-marketing", "AI-Embedded Marketing | Your Digital Partner", "Put AI to work inside B2B marketing processes, including reporting, content operations, personalisation and automation.", "https://your-digital-partner.co.uk/solutions/ai-marketing/", "", ""),
}

def one(text, old, new, label):
    if old not in text:
        raise RuntimeError(f"Missing {label}")
    return text.replace(old, new, 1)

for rel, (page, title, desc, canonical, cta, target) in pages.items():
    path = root / rel
    text = path.read_text()
    text, count = re.subn(r"<title>.*?</title>", f"<title>{title}</title>", text, count=1, flags=re.S)
    if count != 1: raise RuntimeError(f"No title in {rel}")
    desc_tag = f'<meta name="description" content="{desc}">'
    text, count = re.subn(r'<meta name="description" content=".*?">', desc_tag, text, count=1, flags=re.S)
    if count != 1: raise RuntimeError(f"No description in {rel}")
    if "document.documentElement.classList.add('js')" not in text:
        text = one(text, '<meta name="viewport" content="width=device-width, initial-scale=1">', '<meta name="viewport" content="width=device-width, initial-scale=1">\n<script>document.documentElement.classList.add(\'js\');window.siteMotionOK=!matchMedia(\'(prefers-reduced-motion: reduce)\').matches;window.sitePageVisible=!document.hidden;</script>', "viewport")
    if 'property="og:title"' not in text:
        tags = f'''\n<link rel="canonical" href="{canonical}">
<meta property="og:type" content="website">
<meta property="og:site_name" content="Your Digital Partner">
<meta property="og:title" content="{title}">
<meta property="og:description" content="{desc}">
<meta property="og:url" content="{canonical}">
<meta property="og:image" content="{og_image}">
<meta name="twitter:card" content="summary_large_image">
<meta name="twitter:title" content="{title}">
<meta name="twitter:description" content="{desc}">
<meta name="twitter:image" content="{og_image}">'''
        text = one(text, desc_tag, desc_tag + tags, "social tags")
    if page == "ai-marketing" and 'name="robots"' not in text:
        text = one(text, desc_tag, desc_tag + '\n<meta name="robots" content="noindex,follow">', "noindex")
    if '/assets/site-enhancements.css' not in text:
        text = one(text, '</head>', '<link rel="stylesheet" href="/assets/site-enhancements.css">\n<script src="/assets/site-enhancements.js" defer></script>\n</head>', "shared assets")
    body_attrs = f'data-page="{page}"'
    if cta:
        body_attrs += f' data-mobile-cta="{cta}" data-mobile-target="{target}"'
    text = re.sub(r'<body(?:\s[^>]*)?>', f'<body {body_attrs}>', text, count=1)
    if '<nav' in text:
        text = text.replace('<nav>', '<nav aria-label="Primary">', 1)
        if 'class="solutions-toggle"' not in text:
            text, count = re.subn(r'<li>Solutions ▾\s*<div class="dd">', '<li class="solutions-item"><button class="solutions-toggle" type="button" aria-expanded="false">Solutions <span aria-hidden="true">▾</span></button>\n      <div class="dd">', text, count=1)
            if count != 1: raise RuntimeError(f"No Solutions menu in {rel}")
        if 'class="mobile-menu-toggle"' not in text:
            text, count = re.subn(r'(</a>\s*)<ul>', r'\1<button class="mobile-menu-toggle" type="button" aria-expanded="false" aria-controls="site-menu" aria-label="Open menu">☰</button>\n  <ul id="site-menu">', text, count=1)
            if count != 1: raise RuntimeError(f"No menu insertion point in {rel}")
    if '<footer>' in text and 'href="/privacy/"' not in text:
        text, count = re.subn(r'(<footer>.*?<a href="/solutions/paid-campaigns">Paid</a>)(</span>)', r'\1 · <a href="/privacy/">Privacy</a>\2', text, count=1, flags=re.S)
        if count != 1: raise RuntimeError(f"No footer links in {rel}")
    path.write_text(text)
    print(rel)
