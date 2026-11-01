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
               'tapping the payment button, opening your paid sheet, printing it, copying your "about me" note, tapping "Send it" to share the site) with Umami, a privacy-friendly analytics '
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
:root{--paper:#ffffff;--ink:#1d2433;--muted:#5b6475;--line:#e2e5ea;--edge:#c9d2ce;--green:#1f5d4c;--green-dark:#164536;--tint:#eef4f1;
--font:"Public Sans",system-ui,-apple-system,"Segoe UI",Roboto,sans-serif;color-scheme:light}
*{box-sizing:border-box}
body{margin:0;background:var(--paper);color:var(--ink);font:400 1.1875rem/1.6 var(--font);overflow-wrap:break-word}
.wrap{max-width:40rem;margin:0 auto;padding:0 max(20px,env(safe-area-inset-right,0px)) 72px max(20px,env(safe-area-inset-left,0px))}
a{color:var(--green-dark)}
.top{display:flex;justify-content:space-between;align-items:center;gap:12px;padding:18px 0;border-bottom:1px solid var(--line);margin-bottom:36px}
.top a{font-size:1rem;color:var(--muted)}
.top a.brand{display:flex;align-items:center;gap:10px;font-weight:700;font-size:1.05rem;color:var(--ink);text-decoration:none}
.mark{width:14px;height:14px;border-radius:4px;background:var(--green);display:inline-block;flex:none}
h1{font-weight:800;font-size:clamp(2.1rem,8.5vw,3rem);line-height:1.05;letter-spacing:-.03em;margin:0 0 14px}
h2{font-weight:800;font-size:1.45rem;line-height:1.15;letter-spacing:-.015em;margin:44px 0 8px}
p,ul,ol{margin:0 0 14px}
li{margin-bottom:6px}
.updated,.lede{color:var(--muted)}
footer{margin-top:64px;padding-top:20px;border-top:1px solid var(--line);font-size:.95rem;color:var(--muted)}
footer a{color:var(--muted)}
:focus-visible{outline:3px solid var(--green);outline-offset:3px;border-radius:6px}
h1{font-size:clamp(2rem,7vw,2.5rem)}
h2{font-size:1.3rem;margin-top:32px}
</style>"""
FONTS = ('<link rel="preconnect" href="https://fonts.googleapis.com"><link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>'
         '<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Public+Sans:wght@400;600;700;800&display=swap">')

def doc(title, inner, desc, path):
    url = SITE + path
    return ('<!doctype html>\n<html lang="en">\n<head>\n<meta charset="utf-8">\n'
            '<meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover">\n<meta name="theme-color" content="#ffffff">\n'
            f'<title>{html.escape(title)}</title>\n<meta name="description" content="{html.escape(desc)}">\n<link rel="canonical" href="{url}">\n'
            + share_meta(title, desc, url) + FONTS + DOC_STYLE + '\n</head>\n<body><div class="wrap">'
            '<div class="top"><a class="brand" href="/"><i class="mark" aria-hidden="true"></i>Switch Kit AI</a><a href="/">Try it free</a></div>\n'
            '<main>' + inner + '</main>\n<footer>Switch Kit AI is operated by Nomad Strategies LLC and isn\'t affiliated with any AI company. '
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
open(os.path.join(DIST, "robots.txt"), "w").write("User-agent: *\nDisallow: /" + KIT + "\n\nSitemap: " + SITE + "/sitemap.xml\n")
open(os.path.join(DIST, "CNAME"), "w").write(DOMAIN + "\n")
# IndexNow (Bing and others): key file at the site root, key kept in indexnow_key.txt
INDEXNOW_KEY = open(os.path.join(HERE, "indexnow_key.txt")).read().strip()
open(os.path.join(DIST, INDEXNOW_KEY + ".txt"), "w").write(INDEXNOW_KEY)
open(os.path.join(DIST, ".nojekyll"), "w").write("")
shutil.copytree(os.path.join(HERE, "assets"), os.path.join(DIST, "assets"))
# ---- Free search pages (guides/) ----
import json
from guides import GUIDES, HOUSE, STYLE as G_STYLE
LIBTXT = open(os.path.join(HERE, "library.js")).read()
def lib_prompt(sid):
    m = re.search(r'\{id:"' + sid + r'",.*?p:"(.*?)"\}', LIBTXT)
    assert m, sid
    return re.sub(r"\s+", " ", m.group(1).replace("{for}", HOUSE).replace("{style}", G_STYLE)).strip()

GUIDE_CSS = """<style>
:root{--paper:#ffffff;--ink:#1d2433;--muted:#5b6475;--line:#e2e5ea;--edge:#c9d2ce;--green:#1f5d4c;--green-dark:#164536;--tint:#eef4f1;
--font:"Public Sans",system-ui,-apple-system,"Segoe UI",Roboto,sans-serif;color-scheme:light}
*{box-sizing:border-box}
body{margin:0;background:var(--paper);color:var(--ink);font:400 1.1875rem/1.6 var(--font);overflow-wrap:break-word}
.wrap{max-width:40rem;margin:0 auto;padding:0 max(20px,env(safe-area-inset-right,0px)) 72px max(20px,env(safe-area-inset-left,0px))}
a{color:var(--green-dark)}
.top{display:flex;justify-content:space-between;align-items:center;gap:12px;padding:18px 0;border-bottom:1px solid var(--line);margin-bottom:36px}
.top a{font-size:1rem;color:var(--muted)}
.top a.brand{display:flex;align-items:center;gap:10px;font-weight:700;font-size:1.05rem;color:var(--ink);text-decoration:none}
.mark{width:14px;height:14px;border-radius:4px;background:var(--green);display:inline-block;flex:none}
h1{font-weight:800;font-size:clamp(2.1rem,8.5vw,3rem);line-height:1.05;letter-spacing:-.03em;margin:0 0 14px}
h2{font-weight:800;font-size:1.45rem;line-height:1.15;letter-spacing:-.015em;margin:44px 0 8px}
p,ul,ol{margin:0 0 14px}
li{margin-bottom:6px}
.updated,.lede{color:var(--muted)}
footer{margin-top:64px;padding-top:20px;border-top:1px solid var(--line);font-size:.95rem;color:var(--muted)}
footer a{color:var(--muted)}
:focus-visible{outline:3px solid var(--green);outline-offset:3px;border-radius:6px}

.lede{font-size:1.15rem;margin-bottom:24px}
.panel{background:var(--tint);border-radius:16px;padding:20px}
.panel .label{margin:0 0 8px;font-weight:600;font-size:1rem}
.words{margin:0 0 4px;padding:2px 0 2px 14px;border-left:3px solid var(--green);font-size:1.05rem}
.btn{display:flex;align-items:center;justify-content:center;width:100%;min-height:58px;margin-top:16px;border:0;border-radius:10px;background:var(--green);color:#fff;font:700 1.15rem var(--font);text-decoration:none;cursor:pointer;text-align:center;padding:10px 16px;touch-action:manipulation}
.btn:hover{background:var(--green-dark)}
.btn.done{background:var(--green-dark)}
.under{display:flex;flex-wrap:wrap;align-items:center;gap:6px 10px;margin:14px 0 0;font-size:.98rem;color:var(--muted)}
.under select{font:600 1rem var(--font);color:var(--ink);background:var(--paper);border:1.5px solid var(--edge);border-radius:8px;padding:8px 10px;min-height:44px}
.toast{margin:12px 0 0;font-size:1rem;color:var(--green-dark);font-weight:600}
.toast:empty{display:none}
.share{margin:20px 0 0;font-size:1rem;color:var(--muted)}
.share button{background:none;border:0;padding:0;font:600 1rem var(--font);color:var(--green-dark);text-decoration:underline;text-underline-offset:3px;cursor:pointer}
.tip{margin-top:28px}
ul.list{list-style:none;padding:0;margin:14px 0 0;border-top:1px solid var(--line)}
ul.list li{margin:0;border-bottom:1px solid var(--line)}
.row{display:flex;align-items:center;gap:14px;min-height:60px;padding:14px 2px;color:var(--ink);text-decoration:none;font-weight:600;font-size:1.08rem;line-height:1.35}
.row span{flex:1}
.row small{display:block;font-weight:400;color:var(--muted);font-size:.98rem;margin-top:3px}
.row::after{content:"\203A";flex:none;font-size:1.7rem;line-height:1;color:var(--green)}
.row.done::after{content:"\2713";font-size:1.15rem}
@media (hover:hover){.row:hover span{text-decoration:underline;text-underline-offset:3px}}
ol{padding-left:1.2em}
.cta{margin-top:48px;border:1.5px solid var(--green);border-radius:16px;padding:22px}
.cta h2{margin:0 0 8px}
.cta p{margin:0}
</style>"""

GUIDE_JS = """<script>
(function(){
var AIS={chatgpt:{n:"ChatGPT",u:function(p){return "https://chatgpt.com/?q="+encodeURIComponent(p);},f:1},
claude:{n:"Claude",u:function(p){return "https://claude.ai/new?q="+encodeURIComponent(p);},f:1},
gemini:{n:"Gemini",u:function(){return "https://gemini.google.com/app";}},
copilot:{n:"Copilot",u:function(){return "https://copilot.microsoft.com/";}}};
var sel=document.getElementById("ai");if(!sel)return;
try{var s=JSON.parse(localStorage.getItem("macs-ai"));if(s&&AIS[s])sel.value=s;}catch(e){}
sel.addEventListener("change",function(){try{localStorage.setItem("macs-ai",JSON.stringify(sel.value));}catch(e){}});
var ad;try{ad=(new URLSearchParams(location.search).get("utm_content")||"guide").slice(0,40);}catch(e){ad="guide";}
function copyNow(t){var a=document.createElement("textarea");a.value=t;a.setAttribute("readonly","");a.style.cssText="position:fixed;top:0;left:0;opacity:0;font-size:16px";document.body.appendChild(a);a.select();var ok=false;try{ok=document.execCommand("copy");}catch(e){}document.body.removeChild(a);if(!ok){try{navigator.clipboard.writeText(t);ok=true;}catch(e){}}return ok;}
var SHARE_AD=ad;
function shareSite(title,url,toastId){var text="This makes AI easy: tap a line and it does the job. Free.";
  try{if(navigator.share){navigator.share({title:title,text:text,url:url}).then(function(){try{if(window.umami)umami.track("shared",{ad:SHARE_AD});}catch(e){}}).catch(function(){});return;}}catch(e){}
  var ok=false;try{var a=document.createElement("textarea");a.value=url;a.style.cssText="position:fixed;opacity:0;top:0;left:0";document.body.appendChild(a);a.select();ok=document.execCommand("copy");document.body.removeChild(a);}catch(e){}
  var t=document.getElementById(toastId);if(t)t.textContent=ok?"Link copied. Paste it in a text or email to share.":"Share this link: "+url;
  try{if(window.umami)umami.track("shared",{ad:SHARE_AD});}catch(e){}}
var sb=document.getElementById("shareBtn");if(sb)sb.addEventListener("click",function(){shareSite(document.title,location.origin+location.pathname+"?utm_content=share","toast");});
Array.prototype.forEach.call(document.querySelectorAll("[data-p]"),function(b){b.addEventListener("click",function(){
var ai=AIS[sel.value],t=b.getAttribute("data-p");b.href=ai.u(t);var c=copyNow(t);b.classList.add("done");
document.getElementById("toast").textContent=ai.f?(ai.n+" is opening with the words typed in."+(c?" If the box is empty, paste: we copied it too.":"")):(c?"Copied. Paste it into "+ai.n+" and press send.":"Press and hold to copy, then paste it into "+ai.n+".");
try{if(window.umami)umami.track("free-tap",{ad:ad});}catch(e){}});});
})();
</script>"""

def picker():
    return ('<div class="under"><label for="ai">Opens in</label><select id="ai"><option value="chatgpt">ChatGPT</option>'
            '<option value="gemini">Gemini</option><option value="claude">Claude</option><option value="copilot">Copilot</option></select>'
            '<span>Free, no sign-up.</span></div><p class="toast" id="toast" role="status"></p>')

def guide_shell(title, desc, path, body, ld):
    url = SITE + path
    return ('<!doctype html>\n<html lang="en">\n<head>\n<meta charset="utf-8">\n'
            '<meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover">\n<meta name="theme-color" content="#ffffff">\n'
            f'<title>{html.escape(title)}</title>\n<meta name="description" content="{html.escape(desc)}">\n<link rel="canonical" href="{url}">\n'
            + share_meta(title, desc, url) + FONTS + GUIDE_CSS + STATS +
            '<script type="application/ld+json">' + json.dumps(ld) + '</script>\n</head>\n<body><div class="wrap">'
            '<div class="top"><a class="brand" href="/"><i class="mark" aria-hidden="true"></i>Switch Kit AI</a><a href="/guides/">All shortcuts</a></div>\n'
            + body +
            '<footer>Independent guide, not affiliated with OpenAI, Google, Anthropic or Microsoft. Switch Kit AI is operated by Nomad Strategies LLC. '
            '<a href="/help.html">Help</a> · <a href="/privacy.html">Privacy</a> · <a href="/terms.html">Terms</a></footer></div>' + GUIDE_JS + '</body>\n</html>\n')

def tapbtn(prompt, label, cls="btn"):
    return f'<a class="{cls}" href="#" target="_blank" rel="noopener" data-p="{html.escape(prompt)}">{html.escape(label)}</a>'

os.makedirs(os.path.join(DIST, "guides"), exist_ok=True)
guide_paths = []
for g in GUIDES:
    prompt = lib_prompt(g["id"])
    path = "/guides/" + g["slug"] + "/"
    guide_paths.append(path)
    more = "".join(f'<li>{tapbtn(m, m, "row")}</li>' for m in g["more"])
    body = (f'<h1>{html.escape(g["h1"])}</h1><p class="lede">{html.escape(g["intro"])}</p>'
            '<div class="panel"><p class="label">Your AI gets these words:</p>'
            f'<p class="words">{html.escape(prompt)}</p>' + tapbtn(prompt, "Try it now, free") + picker() + '</div>'
            f'<p class="tip"><b>Tip:</b> {html.escape(g["tip"])}</p>'
            '<h2>More ready-made requests</h2><ul class="list">' + more + '</ul>'
            '<h2>How it works</h2><ol><li>Tap the button. Your AI opens in a new tab.</li>'
            '<li>ChatGPT and Claude open with the words already typed. For Gemini or Copilot, we copy them: paste and press send.</li>'
            '<li>Answer its quick questions, or ask it to change anything.</li></ol>'
            f'<p><b>Good to know:</b> {html.escape(g["know"])}</p>'
            '<p class="share">Know someone who\'d find this handy? <button type="button" id="shareBtn">Send them the link</button></p>'
            '<div class="cta"><h2>Want about 60 more like this?</h2><p>Answer four quick questions and get one-tap shortcuts for your household: dinners, emails, bills, trips, home and more. The first 10 are free.</p>'
            '<a class="btn" href="/?utm_content=guide#make">Make my cheat sheet</a></div>')
    ld = {"@context": "https://schema.org", "@type": "HowTo", "name": g["h1"], "description": g["desc"],
          "step": [{"@type": "HowToStep", "text": "Tap Try it now. Your AI opens with the words already typed in."},
                   {"@type": "HowToStep", "text": "Answer its quick questions or ask it to change anything."}]}
    os.makedirs(os.path.join(DIST, "guides", g["slug"]), exist_ok=True)
    open(os.path.join(DIST, "guides", g["slug"], "index.html"), "w").write(guide_shell(g["title"], g["desc"], path, body, ld))

hub_items = "".join(f'<li><a class="row" href="/guides/{g["slug"]}/"><span>{html.escape(g["h1"])}<small>{html.escape(g["desc"].split(". ")[0])}.</small></span></a></li>' for g in GUIDES)
hub_body = ('<h1>Free shortcuts for everyday jobs</h1><p class="lede">Not sure what to ask ChatGPT, Gemini, Claude or Copilot? Pick a job. '
            'Each page has one button that opens your AI with the words already written.</p>'
            '<ul class="list">' + hub_items + '</ul>'
            '<div class="cta"><h2>Get a cheat sheet made for you</h2><p>Answer four quick questions and get one-tap shortcuts for your household. The first 10 are free.</p>'
            '<a class="btn" href="/?utm_content=guides_hub#make">Make my cheat sheet</a></div>')
hub_ld = {"@context": "https://schema.org", "@type": "CollectionPage", "name": "Free AI shortcuts for everyday life",
          "hasPart": [{"@type": "WebPage", "name": g["h1"], "url": SITE + "/guides/" + g["slug"] + "/"} for g in GUIDES]}
open(os.path.join(DIST, "guides", "index.html"), "w").write(guide_shell(
    "Free AI shortcuts for everyday life: what to ask ChatGPT", "One-tap requests for ChatGPT, Gemini, Claude and Copilot: dinners, emails, bills, scams, trips, gifts. Free, no typing.",
    "/guides/", hub_body, hub_ld))
guide_paths.insert(0, "/guides/")

open(os.path.join(DIST, "sitemap.xml"), "w").write(
    '<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n' +
    "".join(f"  <url><loc>{SITE}{p}</loc><lastmod>{TODAY.isoformat()}</lastmod></url>\n" for p in ["/"] + guide_paths + ["/help.html", "/privacy.html", "/terms.html"]) +
    "</urlset>\n")
print("built", sorted(os.listdir(DIST)), len(guide_paths), "guide pages")
