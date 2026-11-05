"""Build the site for switchkitai.com (Switch Kit AI) into docs/ for GitHub Pages.
Usage: python3 build.py support@example.com umami-website-id
Outputs: index.html, kit-x7q2m9.html (paid, noindex), help/privacy/terms, sitemap.xml, robots.txt,
CNAME (custom domain), .nojekyll, 404.html, old /card redirects, assets/.
The paid page keeps its file name so Stripe's existing after-payment redirect still works.
"""
import datetime, html, os, re, shutil, sys
from urllib.parse import quote

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

def title_case(t):
    words = t.split(" ")
    out = []
    for i, w in enumerate(words):
        lw = w.lower()
        if 0 < i < len(words) - 1 and lw in {"a","an","and","as","at","but","by","for","in","into","of","on","or","the","to","with"}:
            out.append(lw)
        elif w[:1].islower():
            out.append(w[:1].upper() + w[1:])
        else:
            out.append(w)
    return " ".join(out)

def share_meta(title, desc, url):
    a = html.escape
    return ('<meta property="og:type" content="website">\n<meta property="og:site_name" content="Switch Kit AI">\n'
            f'<meta property="og:title" content="{a(title)}">\n<meta property="og:description" content="{a(desc)}">\n'
            f'<meta property="og:image" content="{SITE}/assets/share.png">\n<meta property="og:image:width" content="1200">\n<meta property="og:image:height" content="630">\n'
            f'<meta property="og:url" content="{a(url)}">\n<meta name="twitter:card" content="summary_large_image">\n'
            '<link rel="icon" type="image/png" sizes="32x32" href="/assets/favicon-32.png">\n'
            '<link rel="icon" type="image/png" sizes="192x192" href="/assets/icon-192.png">\n'
            '<link rel="apple-touch-icon" href="/assets/apple-touch-icon.png">\n')

HOME_TITLE = "Switch Kit AI: everyday jobs, done by your AI in one tap"
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
:root{--cream:#fef3e5;--night:#0d0d0d;--green:#274c2e;--blush:#e7c2a6;--pink:#d78f85;--hair:rgba(13,13,13,.18);--hair-light:rgba(231,194,166,.35);
--serif:"Instrument Serif",Georgia,serif;--sans:"Montserrat",system-ui,-apple-system,"Segoe UI",sans-serif;--mono:"Azeret Mono",ui-monospace,Menlo,monospace;--ease:cubic-bezier(.4,0,.2,1);color-scheme:light}
*{box-sizing:border-box}
body{margin:0;background:var(--cream);color:var(--night);font:400 16px/1.59 var(--sans);letter-spacing:.008em;overflow-x:hidden;overflow-wrap:break-word}
.wrap{max-width:74rem;margin:0 auto;padding:0 max(20px,env(safe-area-inset-right,0px)) 0 max(20px,env(safe-area-inset-left,0px))}
a{color:var(--green)}
h1,h2,h3{font-family:var(--serif);font-style:italic;font-weight:400;letter-spacing:-.029em;line-height:.99;margin:0}
h1{font-size:36px;margin:0 0 18px}
h2{font-size:36px;margin:48px 0 14px}
p,ul,ol{margin:0 0 14px}
li{margin-bottom:6px}
.top{display:grid;grid-template-columns:1fr auto 1fr;align-items:center;padding:20px 0 14px;border-bottom:1px solid var(--hair)}
.top a.brand{grid-column:2;display:flex;flex-direction:column;align-items:center;gap:4px;text-decoration:none;color:var(--night)}
.monogram{width:34px;height:34px;border-radius:50%;background:var(--green);color:var(--blush);display:grid;place-items:center;font:italic 400 22px/1 var(--serif);padding-bottom:2px}
.wordmark{font:italic 400 24px/.99 var(--serif);letter-spacing:-.029em}
.top a.small{grid-column:3;justify-self:end;font:600 14px var(--mono);font-variant-caps:all-small-caps;letter-spacing:.048em;color:var(--night);text-decoration:none;border-bottom:1px solid var(--hair)}
.updated{font:600 14px var(--mono);font-variant-caps:all-small-caps;letter-spacing:.048em}
.lede{margin:0;font-size:16px;max-width:34em}
footer{background:var(--night);color:var(--blush);margin:64px calc(50% - 50vw) 0;padding:44px calc(50vw - 50%) 48px;font-size:14px;text-align:center}
footer a{color:var(--pink)}
footer .lockup{display:flex;flex-direction:column;align-items:center;gap:6px;margin-bottom:18px}
footer .monogram{background:var(--blush);color:var(--night)}
:focus-visible{outline:2px solid var(--green);outline-offset:3px}
.grain{position:relative;isolation:isolate}
.grain::after{content:"";position:absolute;inset:0;z-index:0;pointer-events:none;background:url("data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' width='180' height='180'%3E%3Cfilter id='n'%3E%3CfeTurbulence type='fractalNoise' baseFrequency='.85' numOctaves='2' stitchTiles='stitch'/%3E%3CfeColorMatrix values='0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 .6 0'/%3E%3C/filter%3E%3Crect width='100%25' height='100%25' filter='url(%23n)'/%3E%3C/svg%3E");opacity:.16;mix-blend-mode:multiply}
.grain.dark::after{mix-blend-mode:screen;opacity:.09}
.grain > *{position:relative;z-index:1}
@media (min-width:980px){
  .wrap{padding-left:40px;padding-right:40px}
  h1{font-size:54px}
  main{max-width:48rem}
}
main{padding-top:40px}
main h1{font-size:36px}
main h2{font-size:36px;margin-top:40px}
</style>"""
FONTS = ('<link rel="preconnect" href="https://fonts.googleapis.com"><link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>'
         '<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Instrument+Serif:ital,wght@0,400;1,400&family=Montserrat:ital,wght@0,100..900;1,100..900&family=Azeret+Mono:ital,wght@0,100..900;1,100..900&display=swap">')

def doc(title, inner, desc, path):
    url = SITE + path
    return ('<!doctype html>\n<html lang="en">\n<head>\n<meta charset="utf-8">\n'
            '<meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover">\n<meta name="theme-color" content="#fef3e5">\n'
            f'<title>{html.escape(title)}</title>\n<meta name="description" content="{html.escape(desc)}">\n<link rel="canonical" href="{url}">\n'
            + share_meta(title, desc, url) + FONTS + DOC_STYLE + '\n</head>\n<body><div class="wrap">'
            '<div class="top"><a class="brand" href="/" aria-label="Switch Kit AI, home"><span class="monogram" aria-hidden="true">S</span><span class="wordmark">Switch Kit AI</span></a><a class="small" href="/">Try it free</a></div>\n'
            '<main>' + inner + '</main>\n<footer><div class="lockup"><span class="monogram" aria-hidden="true">S</span><span class="wordmark">Switch Kit AI</span></div>Switch Kit AI is operated by Nomad Strategies LLC and isn\'t affiliated with any AI company. '
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
    "help": ("Help & refunds · Switch Kit AI", "What's free, what you get for $9.99, how the shortcuts work, refunds and contact."),
    "privacy": ("Privacy policy · Switch Kit AI", "We never see your chats or ask for passwords, and your answers stay on your device."),
    "terms": ("Terms of use · Switch Kit AI", "Terms for Switch Kit AI."),
}
for name, (title, desc) in pages.items():
    inner = open(os.path.join(HERE, "pages", name + ".html")).read().replace("{{EMAIL}}", EMAIL).replace("{{UPDATED}}", TODAY_LONG).replace("{{ANALYTICS}}", ANALYTICS_P)
    inner = re.sub(r"<(h[12])>(.*?)</\1>", lambda m: "<%s>%s</%s>" % (m.group(1), title_case(m.group(2)), m.group(1)), inner)
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
:root{--cream:#fef3e5;--night:#0d0d0d;--green:#274c2e;--blush:#e7c2a6;--pink:#d78f85;--hair:rgba(13,13,13,.18);--hair-light:rgba(231,194,166,.35);
--serif:"Instrument Serif",Georgia,serif;--sans:"Montserrat",system-ui,-apple-system,"Segoe UI",sans-serif;--mono:"Azeret Mono",ui-monospace,Menlo,monospace;--ease:cubic-bezier(.4,0,.2,1);color-scheme:light}
*{box-sizing:border-box}
body{margin:0;background:var(--cream);color:var(--night);font:400 16px/1.59 var(--sans);letter-spacing:.008em;overflow-x:hidden;overflow-wrap:break-word}
.wrap{max-width:74rem;margin:0 auto;padding:0 max(20px,env(safe-area-inset-right,0px)) 0 max(20px,env(safe-area-inset-left,0px))}
a{color:var(--green)}
h1,h2,h3{font-family:var(--serif);font-style:italic;font-weight:400;letter-spacing:-.029em;line-height:.99;margin:0}
h1{font-size:36px;margin:0 0 18px}
h2{font-size:36px;margin:48px 0 14px}
p,ul,ol{margin:0 0 14px}
li{margin-bottom:6px}
.top{display:grid;grid-template-columns:1fr auto 1fr;align-items:center;padding:20px 0 14px;border-bottom:1px solid var(--hair)}
.top a.brand{grid-column:2;display:flex;flex-direction:column;align-items:center;gap:4px;text-decoration:none;color:var(--night)}
.monogram{width:34px;height:34px;border-radius:50%;background:var(--green);color:var(--blush);display:grid;place-items:center;font:italic 400 22px/1 var(--serif);padding-bottom:2px}
.wordmark{font:italic 400 24px/.99 var(--serif);letter-spacing:-.029em}
.top a.small{grid-column:3;justify-self:end;font:600 14px var(--mono);font-variant-caps:all-small-caps;letter-spacing:.048em;color:var(--night);text-decoration:none;border-bottom:1px solid var(--hair)}
.updated{font:600 14px var(--mono);font-variant-caps:all-small-caps;letter-spacing:.048em}
.lede{margin:0;font-size:16px;max-width:34em}
footer{background:var(--night);color:var(--blush);margin:64px calc(50% - 50vw) 0;padding:44px calc(50vw - 50%) 48px;font-size:14px;text-align:center}
footer a{color:var(--pink)}
footer .lockup{display:flex;flex-direction:column;align-items:center;gap:6px;margin-bottom:18px}
footer .monogram{background:var(--blush);color:var(--night)}
:focus-visible{outline:2px solid var(--green);outline-offset:3px}
.grain{position:relative;isolation:isolate}
.grain::after{content:"";position:absolute;inset:0;z-index:0;pointer-events:none;background:url("data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' width='180' height='180'%3E%3Cfilter id='n'%3E%3CfeTurbulence type='fractalNoise' baseFrequency='.85' numOctaves='2' stitchTiles='stitch'/%3E%3CfeColorMatrix values='0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 .6 0'/%3E%3C/filter%3E%3Crect width='100%25' height='100%25' filter='url(%23n)'/%3E%3C/svg%3E");opacity:.16;mix-blend-mode:multiply}
.grain.dark::after{mix-blend-mode:screen;opacity:.09}
.grain > *{position:relative;z-index:1}
@media (min-width:980px){
  .wrap{padding-left:40px;padding-right:40px}
  h1{font-size:54px}
  main{max-width:48rem}
}

.band{display:grid;gap:28px;padding:40px 0 48px;border-bottom:1px solid var(--hair)}
.panel{border:1px solid var(--hair);border-radius:4px;padding:20px}
.panel .label{margin:0 0 10px;font:600 14px var(--mono);font-variant-caps:all-small-caps;letter-spacing:.048em}
.words{margin:0;padding:16px 18px;background:var(--blush);color:var(--night);border-radius:4px;font-size:16px}
.btn{display:flex;align-items:center;justify-content:center;width:100%;min-height:56px;margin-top:14px;border:0;border-radius:0;background:var(--green);color:var(--blush);font:600 16px var(--mono);font-variant-caps:all-small-caps;letter-spacing:.048em;text-decoration:none;cursor:pointer;text-align:center;padding:10px 16px;touch-action:manipulation;transition:transform 600ms var(--ease)}
@media (hover:hover){.btn:hover{transform:translateY(-2px)}}
.btn.done{background:var(--night)}
.toast{margin:12px 0 0;font-size:14px;color:var(--green);font-weight:700}
.toast:empty{display:none}
.under{display:flex;flex-wrap:wrap;align-items:center;gap:6px 10px;margin:0 0 16px;font-size:14px}
.under label{font:600 14px var(--mono);font-variant-caps:all-small-caps;letter-spacing:.048em}
.under select{font:400 16px var(--sans);color:var(--night);background:var(--cream);border:1px solid var(--hair);border-radius:4px;padding:8px 10px;min-height:44px}
.share{margin:20px 0 0;font-size:14px}
.share button{background:none;border:0;padding:0;margin-left:4px;color:var(--green);font:600 14px var(--mono);font-variant-caps:all-small-caps;letter-spacing:.048em;cursor:pointer;border-bottom:1px solid var(--green)}
.tip{margin-top:32px}
ul.list{list-style:none;padding:0;margin:16px 0 0}
ul.list li{margin:0;border-bottom:1px solid var(--hair)}
ul.list li:first-child{border-top:1px solid var(--hair)}
.row{display:flex;align-items:center;gap:16px;min-height:60px;padding:14px 2px;color:var(--night);text-decoration:none;font-weight:700;font-size:16px;line-height:1.4;transition:transform 600ms var(--ease)}
@media (hover:hover){.row:hover{transform:translateY(-2px)}}
.row:before{content:"";flex:none;width:20px;height:20px;border:1px solid var(--night);border-radius:4px;align-self:flex-start;margin-top:1px}
.row.done:before{background:var(--night) url("data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 24 24'%3E%3Cpath d='M5 12.5l4.5 4.5L19 7.5' fill='none' stroke='%23e7c2a6' stroke-width='2.6' stroke-linecap='round' stroke-linejoin='round'/%3E%3C/svg%3E") center/16px no-repeat}
.row span{flex:1}
.row small{display:block;font-weight:400;font-size:14px;margin-top:3px}
.hub .row:before{display:none}
.hub .row:after{content:"open";flex:none;font:600 13px var(--mono);font-variant-caps:all-small-caps;letter-spacing:.048em;color:var(--green)}
ol{padding-left:1.2em}
details.alt{margin:8px 0 0;border-top:1px solid var(--hair);border-bottom:1px solid var(--hair);max-width:48rem}
details.alt summary{cursor:pointer;padding:14px 50px 14px 0;font-weight:700;list-style:none;position:relative}
details.alt summary::-webkit-details-marker{display:none}
details.alt summary::after{content:"open";position:absolute;right:0;top:50%;transform:translateY(-50%);font:600 13px var(--mono);font-variant-caps:all-small-caps;letter-spacing:.048em;color:var(--green)}
details.alt[open] summary::after{content:"close"}
.cta{margin-top:48px;background:var(--green);color:var(--blush);border-radius:4px;padding:28px}
.cta h2{margin:0 0 10px;color:var(--blush)}
.cta p{margin:0}
.cta .btn{background:var(--blush);color:var(--night)}
@media (prefers-reduced-motion:no-preference){.fade{opacity:0;animation:fadein 600ms var(--ease) forwards;animation-delay:calc(var(--i,0) * 40ms)}@keyframes fadein{to{opacity:1}}}
@media (prefers-reduced-motion:reduce){.btn,.row{transition:none}}
@media (min-width:980px){
  .band{padding:56px 0 64px}
  .band.split{grid-template-columns:minmax(0,1fr) minmax(0,1fr);column-gap:72px;align-items:start}
  .band h1{font-size:54px}
  .band:not(.split) h1{font-size:54px}
  .band .lede{font-size:24px;line-height:1.4;max-width:22em}
  .tip,.wrap > h2,.wrap > ol,.wrap > p,.cta,.wrap > ul.list:not(.hub){max-width:48rem}
  ul.list.hub{display:grid;grid-template-columns:1fr 1fr;column-gap:48px}
  ul.list.hub li:nth-child(2){border-top:1px solid var(--hair)}
}
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
    return ('<div class="under"><label for="ai">My AI</label><select id="ai"><option value="chatgpt">ChatGPT</option>'
            '<option value="gemini">Gemini</option><option value="claude">Claude</option><option value="copilot">Copilot</option></select>'
            '<span>Every button on this site will open it.</span></div>')

def guide_shell(title, desc, path, body, ld):
    url = SITE + path
    return ('<!doctype html>\n<html lang="en">\n<head>\n<meta charset="utf-8">\n'
            '<meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover">\n<meta name="theme-color" content="#fef3e5">\n'
            f'<title>{html.escape(title)}</title>\n<meta name="description" content="{html.escape(desc)}">\n<link rel="canonical" href="{url}">\n'
            + share_meta(title, desc, url) + FONTS + GUIDE_CSS + STATS +
            '<script type="application/ld+json">' + json.dumps(ld) + '</script>\n</head>\n<body><div class="wrap">'
            '<div class="top"><a class="brand" href="/" aria-label="Switch Kit AI, home"><span class="monogram" aria-hidden="true">S</span><span class="wordmark">Switch Kit AI</span></a><a class="small" href="/guides/">All shortcuts</a></div>\n'
            + body +
            '<footer><div class="lockup"><span class="monogram" aria-hidden="true">S</span><span class="wordmark">Switch Kit AI</span></div>Independent guide, not affiliated with OpenAI, Google, Anthropic or Microsoft. Switch Kit AI is operated by Nomad Strategies LLC. '
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
    gi = GUIDES.index(g)
    others = GUIDES[gi + 1:] + GUIDES[:gi]
    rel = ([o for o in others if o["id"][0] == g["id"][0]] + [o for o in others if o["id"][0] != g["id"][0]])[:4]
    related = ('<h2>More Free Shortcuts</h2><ul class="list hub">' + "".join(
        f'<li><a class="row" href="/guides/{o["slug"]}/"><span>{html.escape(title_case(o["h1"]))}</span></a></li>' for o in rel) +
        '</ul><p><a href="/guides/">See all free shortcuts</a></p>')
    body = ('<div class="band split">' + f'<div class="bandText fade" style="--i:0"><h1>{html.escape(title_case(g["h1"]))}</h1><p class="lede">{html.escape(g["intro"])}</p></div>'
            '<div class="panel fade" style="--i:3"><p class="label">Your AI gets these words</p>'
            f'<p class="words">{html.escape(prompt)}</p>' + tapbtn(prompt, "Try it now, free") + '<p class="toast" id="toast" role="status"></p></div></div>'
            f'<p class="tip"><b>Tip:</b> {html.escape(g["tip"])}</p>'
            '<h2>More Ready-Made Requests</h2><ul class="list">' + more + '</ul>'
            '<h2>How It Works</h2><ol><li>Tap the button. Your AI opens in a new tab.</li>'
            '<li>ChatGPT and Claude open with the words already typed. For Gemini or Copilot, we copy them: paste and press send.</li>'
            '<li>Answer its quick questions, or ask it to change anything.</li></ol>'
            '<details class="alt"><summary>I use Gemini, Claude or Copilot, not ChatGPT</summary>' + picker() + '</details>'
            f'<p><b>Good to know:</b> {html.escape(g["know"])}</p>'
            '<p class="share">Know someone who\'d find this handy? <button type="button" id="shareBtn">Send them the link</button>'
            f' or <a href="https://www.pinterest.com/pin/create/button/?url={quote(SITE + path)}&amp;media={quote(SITE + "/assets/pins/" + g["slug"] + ".png")}&amp;description={quote(g["title"])}" target="_blank" rel="noopener">save it on Pinterest</a>.</p>'
            + related +
            '<div class="cta grain dark"><h2>Want About 60 More Like This?</h2><p>Answer four quick questions and get one-tap shortcuts for your household: dinners, emails, bills, trips, home and more. The first 10 are free.</p>'
            '<a class="btn" href="/?utm_content=guide#make">Make my cheat sheet</a></div>')
    ld = {"@context": "https://schema.org", "@type": "HowTo", "name": g["h1"], "description": g["desc"],
          "step": [{"@type": "HowToStep", "text": "Tap Try it now. Your AI opens with the words already typed in."},
                   {"@type": "HowToStep", "text": "Answer its quick questions or ask it to change anything."}]}
    os.makedirs(os.path.join(DIST, "guides", g["slug"]), exist_ok=True)
    open(os.path.join(DIST, "guides", g["slug"], "index.html"), "w").write(guide_shell(g["title"], g["desc"], path, body, ld))

hub_items = "".join(f'<li><a class="row" href="/guides/{g["slug"]}/"><span>{html.escape(title_case(g["h1"]))}<small>{html.escape(g["desc"].split(". ")[0])}.</small></span></a></li>' for g in GUIDES)
hub_body = ('<div class="band"><h1>Free Shortcuts for Everyday Jobs</h1><p class="lede">Not sure what to ask ChatGPT, Gemini, Claude or Copilot? Pick a job. '
            'Each page has one button that opens your AI with the words already written.</p></div>'
            '<p><b>New for the holidays:</b> <a href="/guides/ai-christmas-photo-ideas/">AI Christmas photo ideas</a>: turn a family or pet photo into a card picture in one tap. Also: <a href="/guides/printable-ai-cheat-sheet/">a one-page printable cheat sheet</a> to give to a parent.</p>'
            '<ul class="list hub">' + hub_items + '</ul>'
            '<div class="cta grain dark"><h2>Get a Cheat Sheet Made for You</h2><p>Answer four quick questions and get one-tap shortcuts for your household. The first 10 are free.</p>'
            '<a class="btn" href="/?utm_content=guides_hub#make">Make my cheat sheet</a></div>')
hub_ld = {"@context": "https://schema.org", "@type": "CollectionPage", "name": "Free AI shortcuts for everyday life",
          "hasPart": [{"@type": "WebPage", "name": g["h1"], "url": SITE + "/guides/" + g["slug"] + "/"} for g in GUIDES]}
open(os.path.join(DIST, "guides", "index.html"), "w").write(guide_shell(
    "Free AI shortcuts for everyday life: what to ask ChatGPT", "One-tap requests for ChatGPT, Gemini, Claude and Copilot: dinners, emails, bills, scams, trips, gifts. Free, no typing.",
    "/guides/", hub_body, hub_ld))
guide_paths.insert(0, "/guides/")

# ---- Printable one-page cheat sheet (for the fridge, or to hand to a parent) ----
PRINT_ITEMS = [
    ("Plan dinners", "m1"), ("Use what's in the fridge", "m2"), ("Write a polite email", "e1"), ("Say no nicely", "e2"),
    ("Check if a message is a scam", "p2"), ("Explain a bill or letter", "b1"), ("Find money I'm wasting", "b2"),
    ("Something's broken at home", "h1"), ("Questions for the doctor", "w1"), ("Explain a medical word", "w2"),
    ("Gift ideas", "f1"), ("Help with my phone", "p1"),
]
PRINT_CSS = ('<style>.sheet{list-style:none;padding:0;margin:24px 0 0;counter-reset:n}.sheet li{border-top:1px solid var(--hair);padding:14px 0;counter-increment:n}'
             '.sheet li:last-child{border-bottom:1px solid var(--hair)}.sheet b{display:block;font:600 14px var(--mono);font-variant-caps:all-small-caps;letter-spacing:.048em}'
             '.sheet b:before{content:counter(n) ". "}.sheet span{display:block;margin-top:4px}'
             '@media (min-width:980px){.sheet{display:grid;grid-template-columns:1fr 1fr;column-gap:48px}}'
             '@media print{.fade{opacity:1!important;animation:none!important}.top a.small,.noprint,footer,.cta{display:none!important}body{font-size:12px}.band{padding:12px 0}.sheet{display:grid;grid-template-columns:1fr 1fr;column-gap:24px}.sheet li{padding:6px 0;break-inside:avoid}h1{font-size:28px}}</style>')
sheet_items = "".join(f'<li><b>{html.escape(t)}</b><span>{html.escape(lib_prompt(sid))}</span></li>' for t, sid in PRINT_ITEMS)
print_body = ('<div class="band split"><div class="bandText fade" style="--i:0"><h1>Printable AI Cheat Sheet: 12 Things to Ask</h1>'
              '<p class="lede">Not sure what to ask ChatGPT, Gemini, Claude or Copilot? Print this page and keep it by the computer, or hand it to someone who\'s just starting out. '
              'Copy any line into your AI and press send.</p></div>'
              '<div class="panel fade noprint" style="--i:3"><p class="label">One page, free</p><p>Fits on one sheet of paper. Every line also works as a one-tap button on our free shortcut pages.</p>'
              '<button type="button" class="btn" onclick="window.print()">Print this sheet</button>'
              '<p class="share">Helping a parent or friend? <button type="button" id="shareBtn">Send them the link</button></p><p class="toast" id="toast" role="status"></p></div></div>'
              '<div hidden>' + picker() + '</div><ol class="sheet">' + sheet_items + '</ol>'
              '<p class="noprint" style="margin-top:24px">Want these as one-tap buttons instead? <a href="/guides/">See all free shortcuts</a>.</p>'
              '<div class="cta grain dark"><h2>Get a Cheat Sheet Made for You</h2><p>Answer four quick questions and get one-tap shortcuts for your household. The first 10 are free.</p>'
              '<a class="btn" href="/?utm_content=printable#make">Make my cheat sheet</a></div>')
print_ld = {"@context": "https://schema.org", "@type": "WebPage", "name": "Printable AI cheat sheet: 12 things to ask ChatGPT",
            "description": "A free one-page printable list of everyday things to ask ChatGPT, Gemini, Claude or Copilot."}
os.makedirs(os.path.join(DIST, "guides", "printable-ai-cheat-sheet"), exist_ok=True)
open(os.path.join(DIST, "guides", "printable-ai-cheat-sheet", "index.html"), "w").write(guide_shell(
    "Printable AI cheat sheet: 12 things to ask ChatGPT (free)",
    "A free one-page printable list of everyday things to ask ChatGPT, Gemini, Claude or Copilot: dinners, emails, bills, scams, doctor visits and more. Great for beginners.",
    "/guides/printable-ai-cheat-sheet/", PRINT_CSS + print_body, print_ld))
guide_paths.append("/guides/printable-ai-cheat-sheet/")

# ---- Seasonal: AI Christmas photo ideas (peak searches mid-December; pins need to go up in November) ----
XMAS_INTRO = "I'm going to send you a photo. When I do, "
XMAS_KEEP = " Keep everyone's faces, hair and expressions exactly as they are so they still look like themselves. If I haven't sent the photo yet, ask me for it."
XMAS = [
    ("Classic Christmas card", "turn it into a classic Christmas card photo: everyone together in front of a decorated tree and a fireplace, warm twinkly lights, cozy and natural. Leave space at the bottom for a short greeting."),
    ("Santa caught in our living room", "make it look like Santa Claus was caught on camera in our living room on Christmas Eve, leaving presents by the tree, like a real night-time home photo. Keep the room looking like our room."),
    ("Snowy cabin portrait", "put us outside a cozy log cabin in gently falling snow, wearing warm winter sweaters and scarves, soft evening light."),
    ("Matching pajamas morning", "show us on Christmas morning in matching red plaid pajamas, sitting by the tree with mugs of cocoa and wrapped presents."),
    ("Vintage holiday postcard", "turn it into a 1950s-style illustrated Christmas postcard with soft colors and a hand-lettered \"Merry Christmas\" at the top."),
    ("Watercolor card", "turn it into a gentle watercolor painting for a holiday card, with a snowy background and a few holly leaves around the edge."),
    ("Family in a snow globe", "put us inside a glass snow globe with a tiny snowy village, sitting on a wooden table with soft lights behind it."),
    ("Pet in a Santa hat", "give my pet a little Santa hat and scarf, sitting by a decorated tree, as a cute holiday card photo."),
]
XMAS_MSG = "Help me write a short message for our Christmas card. Ask me who it's from and one or two things that happened this year, then give me 3 options: one funny, one warm, one short. Keep it short and simple. Use plain English."
xp = lambda d: XMAS_INTRO + d + XMAS_KEEP
x_rows = "".join(f'<li>{tapbtn(xp(d), t, "row")}</li>' for t, d in XMAS[1:])
x_path = "/guides/ai-christmas-photo-ideas/"
x_body = ('<div class="band split"><div class="bandText fade" style="--i:0"><h1>AI Christmas Photo Ideas, Ready to Tap</h1>'
          '<p class="lede">Turn an ordinary family or pet photo into a Christmas card picture. Tap a style, your AI opens with the request already written, then send it your photo. '
          'Works with ChatGPT and Gemini, free.</p></div>'
          '<div class="panel fade" style="--i:3"><p class="label">Start here: classic Christmas card</p>'
          f'<p class="words">{html.escape(xp(XMAS[0][1]))}</p>' + tapbtn(xp(XMAS[0][1]), "Try it now, free") +
          '<p class="toast" id="toast" role="status"></p></div></div>'
          '<p class="tip"><b>How to add your photo:</b> after your AI opens, tap the <b>+</b> or paperclip next to the message box, choose a photo from your phone, and press send. '
          'Pick a clear photo where everyone\'s face is easy to see.</p>'
          '<h2>More Christmas Photo Styles</h2><ul class="list">' + x_rows + '</ul>'
          '<h2>Now Write the Card</h2><ul class="list"><li>' + tapbtn(XMAS_MSG, "Write the message inside our Christmas card", "row") + '</li></ul>'
          '<h2>Tips for Better Pictures</h2><ol>'
          '<li>If a face doesn\'t look right, reply: "Keep their face exactly like the original photo" and ask it to try again.</li>'
          '<li>Words on pictures sometimes come out misspelled. Ask it to fix them, or add your greeting later in your card app.</li>'
          '<li>Free accounts have a daily limit on pictures. If you hit it, try again tomorrow or switch to Gemini.</li></ol>'
          '<details class="alt"><summary>I use Gemini, Claude or Copilot, not ChatGPT</summary>' + picker() + '</details>'
          '<p><b>Good to know:</b> your photo goes straight from your phone to your own AI. Switch Kit AI never sees it. Only use photos of people who\'d be happy to see themselves on a card.</p>'
          '<p class="share">Know someone making cards this year? <button type="button" id="shareBtn">Send them the link</button>'
          f' or <a href="https://www.pinterest.com/pin/create/button/?url={quote(SITE + x_path)}&amp;media={quote(SITE + "/assets/pins/ai-christmas-photo-ideas.png")}&amp;description={quote("AI Christmas photo ideas: one-tap prompts for ChatGPT and Gemini")}" target="_blank" rel="noopener">save it on Pinterest</a>.</p>'
          '<div class="cta grain dark"><h2>Want About 60 More Like This?</h2><p>Answer four quick questions and get one-tap shortcuts for your household: gifts, dinners, cards, trips and more. The first 10 are free.</p>'
          '<a class="btn" href="/?utm_content=xmas_photo#make">Make my cheat sheet</a></div>')
x_ld = {"@context": "https://schema.org", "@type": "HowTo", "name": "Make an AI Christmas photo with ChatGPT or Gemini",
        "step": [{"@type": "HowToStep", "text": "Tap a style. Your AI opens with the request already written."},
                 {"@type": "HowToStep", "text": "Attach a clear family or pet photo and press send."},
                 {"@type": "HowToStep", "text": "Ask it to fix anything, like keeping faces exactly the same."}]}
os.makedirs(os.path.join(DIST, "guides", "ai-christmas-photo-ideas"), exist_ok=True)
open(os.path.join(DIST, "guides", "ai-christmas-photo-ideas", "index.html"), "w").write(guide_shell(
    "AI Christmas photo ideas: 8 one-tap ChatGPT and Gemini prompts for family photos (free)",
    "Turn a family or pet photo into a Christmas card picture: classic tree and fireplace, Santa caught in your living room, snowy cabin, matching pajamas and more. One tap opens ChatGPT or Gemini with the prompt written. Free.",
    x_path, x_body, x_ld))
guide_paths.insert(1, x_path)

open(os.path.join(DIST, "sitemap.xml"), "w").write(
    '<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n' +
    "".join(f"  <url><loc>{SITE}{p}</loc><lastmod>{TODAY.isoformat()}</lastmod></url>\n" for p in ["/"] + guide_paths + ["/help.html", "/privacy.html", "/terms.html"]) +
    "</urlset>\n")
# ---- Pinterest images, one per free page (see pins.py). Never stops the build. ----
try:
    import pins
    PIN_LIST = [{"slug": g["slug"], "headline": title_case(g["h1"]), "label": "Free AI shortcut", "card_label": "Ask your AI",
                 "card_text": g["more"][0], "title": g["title"], "desc": g["desc"], "link": "/guides/" + g["slug"] + "/"} for g in GUIDES]
    PIN_LIST.append({"slug": "printable-ai-cheat-sheet", "headline": "Printable AI Cheat Sheet", "label": "Free, one page",
                     "card_label": "12 things to ask your AI", "items": [t for t, _ in PRINT_ITEMS[:7]], "more": "…and 5 more",
                     "title": "Printable AI cheat sheet: 12 things to ask ChatGPT (free)",
                     "desc": "A free one-page list of everyday things to ask ChatGPT, Gemini, Claude or Copilot. Print it for the fridge or give it to a parent.",
                     "link": "/guides/printable-ai-cheat-sheet/"})
    PIN_LIST.insert(0, {"slug": "ai-christmas-photo-ideas", "headline": "AI Christmas Photo Ideas", "label": "Free, one tap",
                     "card_label": "Turn a family photo into", "items": [t for t, _ in XMAS[:7]], "more": "…plus the card message",
                     "title": "AI Christmas photo ideas: one-tap prompts for ChatGPT and Gemini",
                     "desc": "Turn a family or pet photo into a Christmas card picture: tree and fireplace, Santa caught in your living room, snowy cabin, matching pajamas. Tap a style, add your photo. Free.",
                     "link": "/guides/ai-christmas-photo-ideas/"})
    pins.render(PIN_LIST, DIST, SITE)
except Exception as e:
    print("pins: skipped", e)
print("built", sorted(os.listdir(DIST)), len(guide_paths), "guide pages")
