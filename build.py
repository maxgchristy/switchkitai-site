"""Build the site for switchkitai.com (Kitchen Table) into docs/ for GitHub Pages.
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
    return ('<meta property="og:type" content="website">\n<meta property="og:site_name" content="Kitchen Table">\n'
            f'<meta property="og:title" content="{a(title)}">\n<meta property="og:description" content="{a(desc)}">\n'
            f'<meta property="og:image" content="{SITE}/assets/share.png">\n<meta property="og:image:width" content="1200">\n<meta property="og:image:height" content="630">\n'
            f'<meta property="og:url" content="{a(url)}">\n<meta name="twitter:card" content="summary_large_image">\n'
            '<link rel="icon" type="image/png" sizes="32x32" href="/assets/favicon-32.png">\n'
            '<link rel="icon" type="image/png" sizes="192x192" href="/assets/icon-192.png">\n'
            '<link rel="apple-touch-icon" href="/assets/apple-touch-icon.png">\n')

HOME_TITLE = "Kitchen Table: everyday jobs, done by your AI in one tap"
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
            '<div class="top"><a class="brand" href="/" aria-label="Kitchen Table, home"><span class="monogram" aria-hidden="true">K</span><span class="wordmark">Kitchen Table</span></a><a class="small" href="/">Try it free</a></div>\n'
            '<main>' + inner + '</main>\n<footer><div class="lockup"><span class="monogram" aria-hidden="true">K</span><span class="wordmark">Kitchen Table</span></div>Kitchen Table is operated by Nomad Strategies LLC and isn\'t affiliated with any AI company. '
            '<a href="/help.html">Help &amp; refunds</a> · <a href="/privacy.html">Privacy</a> · <a href="/terms.html">Terms</a></footer></div></body>\n</html>\n')

def redirect(to):
    return ('<!doctype html><html lang="en"><head><meta charset="utf-8"><meta name="robots" content="noindex">'
            f'<meta http-equiv="refresh" content="0; url={to}"><link rel="canonical" href="{SITE}/">'
            f'<title>Kitchen Table</title></head><body><a href="{to}">Continue to Kitchen Table</a>'
            f'<script>location.replace("{to}"+(location.search&&"{to}".indexOf("?")<0?location.search:""));</script></body></html>\n')

if os.path.exists(DIST):
    shutil.rmtree(DIST)
os.makedirs(DIST)
open(os.path.join(DIST, "index.html"), "w").write(home)
open(os.path.join(DIST, KIT), "w").write(kit)
pages = {
    "help": ("Help & refunds · Kitchen Table", "What's free, what you get for $9.99, how the shortcuts work, refunds and contact."),
    "privacy": ("Privacy policy · Kitchen Table", "We never see your chats or ask for passwords, and your answers stay on your device."),
    "terms": ("Terms of use · Kitchen Table", "Terms for Kitchen Table."),
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
            '<div class="top"><a class="brand" href="/" aria-label="Kitchen Table, home"><span class="monogram" aria-hidden="true">K</span><span class="wordmark">Kitchen Table</span></a><a class="small" href="/guides/">All shortcuts</a></div>\n'
            + body +
            '<footer><div class="lockup"><span class="monogram" aria-hidden="true">K</span><span class="wordmark">Kitchen Table</span></div>Independent guide, not affiliated with OpenAI, Google, Anthropic or Microsoft. Kitchen Table is operated by Nomad Strategies LLC. '
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
            '<p class="share">Know someone who\'d find this handy? <button type="button" id="shareBtn">Send them the link</button></p>'
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
            '<ul class="list hub">' + hub_items + '</ul>'
            '<div class="cta grain dark"><h2>Get a Cheat Sheet Made for You</h2><p>Answer four quick questions and get one-tap shortcuts for your household. The first 10 are free.</p>'
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
