from pathlib import Path

path = Path(__file__).resolve().parents[1] / "privacy/index.html"
text = path.read_text()
text = text.replace('<title>Privacy Policy | Your Digital Partner</title>\n<meta name="robots" content="noindex">', '<title>Privacy Notice | Your Digital Partner</title>\n<meta name="description" content="How Your Digital Partner collects, uses and protects information submitted through this website.">\n<link rel="canonical" href="https://your-digital-partner.co.uk/privacy/">')
text = text.replace('<body>', '<body data-page="privacy">')
text = text.replace('Last updated: [DATE]', 'Last updated: 7 July 2026')
text = text.replace('Your Digital Partner is operated by Chris Chapman, a UK-based digital marketing consultant. Contact: cpfc89@hotmail.com.', 'Your Digital Partner is operated by Chris Chapman, a UK-based digital marketing consultant. For privacy questions, use the contact form on the homepage and state that your message relates to privacy.')
text = text.replace('This site uses [HubSpot analytics / your analytics tool] to understand how visitors use it. You can decline non-essential cookies where prompted.', 'The current website code does not include a first-party analytics platform. Website forms are processed using HubSpot, which may use essential or functional browser storage to deliver the form service.')
text = text.replace('[This is a template — review and complete before relying on it. Consider professional advice for full compliance.]', 'Information is kept only for as long as it is reasonably needed to respond to an enquiry, provide the requested service, maintain appropriate business records or meet legal obligations.')
text = text.replace('<a class="back" href="/">← Back to homepage</a>', '<p style="margin-top:20px">You may also raise a concern with the UK Information Commissioner\'s Office.</p><a class="back" href="/">← Back to homepage</a>')
if '/assets/site-enhancements.css' not in text:
    text = text.replace('</head>', '<link rel="stylesheet" href="/assets/site-enhancements.css">\n</head>')
path.write_text(text)
print('Privacy notice updated')
