"""Build the site for switchkitai.com (My AI Cheat Sheet) into docs/ for GitHub Pages.
Usage: python3 build.py support@example.com umami-website-id
Outputs: index.html, kit-x7q2m9.html (paid, noindex), help/privacy/terms, sitemap.xml, robots.txt,
CNAME (custom domain), .nojekyll, 404.html, old /card redirects, assets/.
The paid page keeps its file name so Stripe's existing after-payment redirect still works.
"""
import datetime, html, os, re, shutil, sys

HERE = os.path.dirname(os.path.abspath(__file__))
EMAIL = sys.argv[1] if len(sys.argv) > 1 else "[SUPPORT EMAIL]"
UMAMI = sys.argv[2] if len(sys.argv) > 2 else None
PAY_URL = "https://buy.stripe.com/28EfZgfqN57Gh0QdXx4ko03"  # live $9.99 link; redirects to /kit-x7q2m9.html
SITE = "https://switchkitai.com"
DOMAIN = "switchkitai.com"
KIT = "kit-x7q2m9.html"
DIST = os.path.join(HERE, "docs")
TODAY = datetime.date.today()
TODAY_LONG = TODAY.strftime("%B ") + str(TODAY.day) + TODAY.strftime(", %Y")

if UMAMI and not re.fullmatch(r"[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}", UMAMI):
    sys.exit("Umami website ID doesn't look right")
STATS = ('<script defer src="https://cloud.umami.is/script.js" data-website-id="' + UMAMI +
         '" data-domains="switchkitai.com,www.switchkitai.com" data-do-not-track="true" data-exclude-hash="true"></script>\n') if UMAMI else ""
# Must match exactly what the pages send (see count() in index.html).
ANALYTICS_P = ('<p>We count visits and a few taps (trying a free shortcut, starting and finishing the four questions, tapping a shortcut on your sheet, '
               'tapping the payment button, opening your paid sheet, printing it, copying your "about me" note) with Umami, a privacy-friendly analytics '
               'service that doesn\'t use cookies. Each count can include which ad or link brought you and, for the questions, how many help topics you picked. '
               'It never includes which shortcut you tapped, your answers, which AI you use, your name, your email or anything you type. If your browser sends a '
               '"Do Not Track" signal, we don\'t count your visit.</p>') if UMAMI else "<p>We don't currently use any visit counting.</p>"

def share_meta(title, desc, url):
    a = html.escape
    return ('<meta property="og:type" content="website">\n<meta property="og:site_name" content="Switch Kit AI">\n'
            f'<meta property="og:title" content="{a(title)}">\n<meta property="og:description" content="{a(desc)}">\n'
            f'<meta property="og:image" content="{SITE}/assets/share.png">\n<meta property="og:image:width" content="1200">\n<meta property="og:image:height" content="630">\n'
            f'<meta property="og:url" content="{a(url)}">\n<meta name="twitter:card" content="summary_large_image">\n'
            '<link rel="icon" type="image/png" sizes="32x32" href="/assets/favicon-32.png">\n'
            '<link rel="icon" type="image/png" sizes="192x192" href="/assets/icon-192.png">\n'
            '<link rel="apple-touch-icon" href="/assets/apple-touch-icon.png">\n')

HOME_TITLE = "My AI Cheat Sheet: tap a line, your AI does the rest"
HOME_DESC = "One-tap shortcuts that get ChatGPT, Gemini, Claude or Copilot to plan dinners, write emails, sort out bills and more. No typing, no tech. Free to try."

src = open(os.path.join(HERE, "index.html")).read()
lib = open(os.path.join(HERE, "library.js")).read()
assert "var UNLOCKED=false; /*UNLOCK-FLAG*/" in src
src = src.replace("{{LIBRARY}}", lib).replace("{{STATS}}", STATS).replace("{{PAY_URL}}", PAY_URL)
assert "{{" not in src.replace("{{HEADEXTRA}}", ""), "unfilled placeholder"
home = src.replace("{{HEADEXTRA}}", f'<link rel="canonical" href="{SITE}/">\n' + share_meta(HOME_TITLE, HOME_DESC, SITE + "/"))
kit = src.replace("{{HEADEXTRA}}", '<meta name="robots" content="noindex, nofollow">\n' + share_meta(HOME_TITLE, HOME_DESC, SITE + "/")).replace(
    "var UNLOCKED=false; /*UNLOCK-FLAG*/", "var UNLOCKED=true;")

DOC_STYLE = """<style>
:root{--desk:#eef2f6;--card:#fcfcf6;--ink:#1c2b4f;--pencil:#5c6578;--line:#d9e2ec;--margin:#d94a40;--hi:#ffe45c;
--display:"Bricolage Grotesque","Avenir Next","Segoe UI",sans-serif;--body:"Atkinson Hyperlegible","Segoe UI",Verdana,sans-serif;color-scheme:light}
*{box-sizing:border-box}
body{margin:0;background:var(--desk);color:var(--ink);font-family:var(--body);font-size:1.15rem;line-height:1.6;overflow-wrap:break-word}
.wrap{max-width:40rem;margin:0 auto;padding:16px max(16px,env(safe-area-inset-right,0px)) 56px max(16px,env(safe-area-inset-left,0px))}
a{color:var(--ink)}
.top{display:flex;justify-content:space-between;align-items:center;gap:12px;margin-bottom:24px}
.brand{font-family:var(--display);font-weight:800;font-size:1.15rem;text-decoration:none;display:flex;align-items:center;gap:10px}
.mark{width:22px;height:26px;border-radius:4px;background:var(--card);border:2px solid var(--ink);position:relative;display:inline-block}
.mark:before{content:"";position:absolute;left:3px;right:3px;top:7px;height:2px;background:var(--margin)}
.mark:after{content:"";position:absolute;left:3px;right:5px;top:12px;height:6px;background:var(--hi);border-radius:2px}
.sheet{background:var(--card);border-radius:6px;padding:20px 18px 24px;box-shadow:0 18px 40px -26px rgba(28,43,79,.45);border-top:3px solid var(--margin)}
h1{font-family:var(--display);font-weight:800;font-size:clamp(2rem,7vw,2.5rem);line-height:1.08;letter-spacing:-.02em;margin:0 0 4px}
h2{font-family:var(--display);font-weight:700;font-size:1.3rem;margin:28px 0 6px}
p,ul{margin:0 0 12px}
li{margin-bottom:6px}
.updated,.lede{color:var(--pencil)}
footer{margin-top:32px;font-size:.95rem;color:var(--pencil)}
footer a{color:var(--pencil)}
:focus-visible{outline:3px solid var(--ink);outline-offset:3px}
</style>"""
FONTS = ('<link rel="preconnect" href="https://fonts.googleapis.com"><link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>'
         '<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Atkinson+Hyperlegible:wght@400;700&family=Bricolage+Grotesque:opsz,wght@12..96,700;12..96,800&display=swap">')

def doc(title, inner, desc, path):
    url = SITE + path
    return ('<!doctype html>\n<html lang="en">\n<head>\n<meta charset="utf-8">\n'
            '<meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover">\n<meta name="theme-color" content="#eef2f6">\n'
            f'<title>{html.escape(title)}</title>\n<meta name="description" content="{html.escape(desc)}">\n<link rel="canonical" href="{url}">\n'
            + share_meta(title, desc, url) + FONTS + DOC_STYLE + '\n</head>\n<body><div class="wrap">'
            '<div class="top"><a class="brand" href="/"><i class="mark" aria-hidden="true"></i>Switch Kit AI</a><a href="/">Try a shortcut free</a></div>\n'
            '<div class="sheet">' + inner + '</div>\n<footer>Switch Kit AI is operated by Nomad Strategies LLC and isn\'t affiliated with any AI company. '
            '<a href="/help.html">Help &amp; refunds</a> · <a href="/privacy.html">Privacy</a> · <a href="/terms.html">Terms</a></footer></div></body>\n</html>\n')

def redirect(to):
    return ('<!doctype html><html lang="en"><head><meta charset="utf-8"><meta name="robots" content="noindex">'
            f'<meta http-equiv="refresh" content="0; url={to}"><link rel="canonical" href="{SITE}/">'
            f'<title>Switch Kit AI</title></head><body><a href="{to}">Continue to Switch Kit AI</a>'
            f'<script>location.replace("{to}"+(location.search&&"{to}".indexOf("?")<0?location.search:""));</script></body></html>\n')

if os.path.exists(DIST):
    shutil.rmtree(DIST)
os.makedirs(DIST)
open(os.path.join(DIST, "index.html"), "w").write(home)
open(os.path.join(DIST, KIT), "w").write(kit)
pages = {
    "help": ("Help & refunds · My AI Cheat Sheet", "What's free, what you get for $9.99, how the shortcuts work, refunds and contact."),
    "privacy": ("Privacy policy · My AI Cheat Sheet", "We never see your chats or ask for passwords, and your answers stay on your device."),
    "terms": ("Terms of use · My AI Cheat Sheet", "Terms for My AI Cheat Sheet by Switch Kit AI."),
}
for name, (title, desc) in pages.items():
    inner = open(os.path.join(HERE, "pages", name + ".html")).read().replace("{{EMAIL}}", EMAIL).replace("{{UPDATED}}", TODAY_LONG).replace("{{ANALYTICS}}", ANALYTICS_P)
    open(os.path.join(DIST, name + ".html"), "w").write(doc(title, inner, desc, "/" + name + ".html"))
# Old links: /card and /card.html went home with a tag; /guides/* went home. Any unknown page goes home too.
open(os.path.join(DIST, "card.html"), "w").write(redirect("/?utm_content=card"))
os.makedirs(os.path.join(DIST, "card"))
open(os.path.join(DIST, "card", "index.html"), "w").write(redirect("/?utm_content=card"))
open(os.path.join(DIST, "404.html"), "w").write(redirect("/"))
open(os.path.join(DIST, "sitemap.xml"), "w").write(
    '<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n' +
    "".join(f"  <url><loc>{SITE}{p}</loc><lastmod>{TODAY.isoformat()}</lastmod></url>\n" for p in ("/", "/help.html", "/privacy.html", "/terms.html")) +
    "</urlset>\n")
open(os.path.join(DIST, "robots.txt"), "w").write("User-agent: *\nDisallow: /" + KIT + "\n\nSitemap: " + SITE + "/sitemap.xml\n")
open(os.path.join(DIST, "CNAME"), "w").write(DOMAIN + "\n")
open(os.path.join(DIST, ".nojekyll"), "w").write("")
shutil.copytree(os.path.join(HERE, "assets"), os.path.join(DIST, "assets"))
print("built", sorted(os.listdir(DIST)))
