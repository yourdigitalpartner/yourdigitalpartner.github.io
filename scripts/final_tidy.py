from pathlib import Path
import re

root = Path(__file__).resolve().parents[1]
html_files = [
    root / "index.html",
    root / "success-stories/index.html",
    root / "solutions/seo-aeo-visibility/index.html",
    root / "solutions/website-optimisation-cro/index.html",
    root / "solutions/paid-campaigns/index.html",
    root / "solutions/ai-marketing/index.html",
]

def escape_bare_ampersands(value):
    return re.sub(r"&(?!#?[A-Za-z0-9]+;)", "&amp;", value)

for path in html_files:
    text = path.read_text()
    text = re.sub(r"<title>(.*?)</title>", lambda m: f"<title>{escape_bare_ampersands(m.group(1))}</title>", text, count=1, flags=re.S)
    text = re.sub(r'(<meta (?:property="og:title"|name="twitter:title") content=")(.*?)(">)', lambda m: m.group(1) + escape_bare_ampersands(m.group(2)) + m.group(3), text)
    path.write_text(text)

# Improve the interactive AEO tabs with explicit tab semantics.
path = root / "solutions/seo-aeo-visibility/index.html"
text = path.read_text()
text = text.replace('<div class="chat-tabs" id="tabs">', '<div class="chat-tabs" id="tabs" role="tablist" aria-label="AI assistant examples">', 1)
text = text.replace('<button type="button" class="chat-tab on" aria-selected="true">ChatGPT</button>', '<button type="button" class="chat-tab on" role="tab" aria-selected="true" aria-controls="chat-panel">ChatGPT</button>', 1)
text = text.replace('<button type="button" class="chat-tab" aria-selected="false">Gemini</button>', '<button type="button" class="chat-tab" role="tab" aria-selected="false" aria-controls="chat-panel">Gemini</button>', 1)
text = text.replace('<button type="button" class="chat-tab" aria-selected="false">Claude</button>', '<button type="button" class="chat-tab" role="tab" aria-selected="false" aria-controls="chat-panel">Claude</button>', 1)
text = text.replace('<button type="button" class="chat-tab" aria-selected="false">Perplexity</button>', '<button type="button" class="chat-tab" role="tab" aria-selected="false" aria-controls="chat-panel">Perplexity</button>', 1)
text = text.replace('<div class="chat-body">', '<div class="chat-body" id="chat-panel" role="tabpanel" aria-live="polite">', 1)
path.write_text(text)

# Add a text summary for the first comparison chart as well.
path = root / "success-stories/index.html"
text = path.read_text()
needle = '          <text class="peaklab" x="322" y="24">8.1% — highest in category</text>\n        </svg>'
if 'View the citation-rate result as text' not in text:
    text = text.replace(needle, needle + '\n        <details class="chart-data"><summary>View the citation-rate result as text</summary><p>The client reached an 8.1% owned-domain citation rate, the highest in its category, while the two tracked competitors declined during the same period.</p></details>', 1)
path.write_text(text)

print("Final tidy complete")
