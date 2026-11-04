"""Pinterest images: one tall (1000x1500) pin per free page, saved to docs/assets/pins/<slug>.png.
Rendered with headless Chrome (installed on GitHub's build machines). If Chrome isn't found, pins are skipped
and the rest of the site still builds. Also writes docs/assets/pins/pins.json (title, description, link, image)
so pins can be posted to the Switch Kit AI Pinterest account.
"""
import html, json, os, shutil, subprocess, tempfile

GOOGLE_FONTS = ('<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Instrument+Serif:ital@1'
                '&family=Montserrat:wght@400;700&family=Azeret+Mono:wght@600&display=block">')

CSS = """<style>
*{box-sizing:border-box;margin:0}
html,body{width:1000px;height:1500px;overflow:hidden}
body{background:#fef3e5;color:#0d0d0d;font:400 24px/1.59 "Montserrat",sans-serif;display:flex;flex-direction:column;align-items:center;padding:56px 64px 52px}
.lock{display:flex;flex-direction:column;align-items:center;gap:8px}
.mono{width:56px;height:56px;border-radius:50%;background:#274c2e;color:#e7c2a6;display:grid;place-items:center;font:italic 400 36px/1 "Instrument Serif",serif;padding-bottom:3px}
.word{font:italic 400 36px/.99 "Instrument Serif",serif;letter-spacing:-.029em}
.arch{position:relative;margin-top:40px;width:100%;flex:1;background:#274c2e;color:#e7c2a6;border-radius:436px 436px 4px 4px;
 padding:170px 64px 56px;display:flex;flex-direction:column;justify-content:flex-start;overflow:hidden}
.arch:before{content:"";position:absolute;inset:28px 28px 0;border:1px solid #d78f85;border-bottom:0;border-radius:408px 408px 0 0;opacity:.7}
.arch > *{position:relative;z-index:1}
.label{font:600 24px "Azeret Mono",monospace;font-variant-caps:all-small-caps;letter-spacing:.048em;text-align:center}
h1{font:italic 400 122px/.99 "Instrument Serif",serif;letter-spacing:-.029em;text-align:center;margin:0;text-wrap:balance}
h1.long{font-size:81px}
.mid{flex:1;display:flex;flex-direction:column;justify-content:center;padding:24px 0 40px}
.card{background:#e7c2a6;color:#0d0d0d;border-radius:4px;padding:30px 34px}
.card .label{text-align:left;font-size:24px;margin-bottom:10px}
.card p{font-size:36px;line-height:1.35}
.card p.more{font-size:30px;margin-top:6px}
.card ol{padding-left:1.3em;font-size:30px;line-height:1.45}
.foot{margin-top:30px;font:600 24px "Azeret Mono",monospace;font-variant-caps:all-small-caps;letter-spacing:.048em;color:#274c2e}
</style>"""


def pin_html(p, font_css):
    head = html.escape(p["headline"])
    cls = ' class="long"' if len(p["headline"]) > 30 else ""
    if p.get("items"):
        card = "<ol>" + "".join(f"<li>{html.escape(i)}</li>" for i in p["items"]) + "</ol>" + (f'<p class="more">{html.escape(p["more"])}</p>' if p.get("more") else "")
    else:
        card = f'<p>“{html.escape(p["card_text"])}”</p>'
    return ('<!doctype html><html><head><meta charset="utf-8">' + font_css + CSS + '</head><body>'
            '<div class="lock"><div class="mono">S</div><div class="word">Switch Kit AI</div></div>'
            f'<div class="arch"><div class="label">{html.escape(p["label"])}</div><div class="mid"><h1{cls}>{head}</h1></div>'
            f'<div class="card"><div class="label">{html.escape(p["card_label"])}</div>{card}</div></div>'
            '<div class="foot">Free, one tap · switchkitai.com</div></body></html>')


def find_chrome():
    for name in ("google-chrome", "google-chrome-stable", "chromium", "chromium-browser"):
        path = shutil.which(name)
        if path:
            return path
    return None


def render(pins, dist, site):
    """pins: list of dicts with slug, headline, label, card_label, card_text or items, title, desc, link."""
    out_dir = os.path.join(dist, "assets", "pins")
    os.makedirs(out_dir, exist_ok=True)
    font_css = os.environ.get("PIN_FONT_CSS") or GOOGLE_FONTS
    chrome = find_chrome()
    made = []
    if not chrome:
        print("pins: Chrome not found, skipping images")
    tmp = tempfile.mkdtemp()
    for p in pins:
        png = os.path.join(out_dir, p["slug"] + ".png")
        if chrome:
            src = os.path.join(tmp, p["slug"] + ".html")
            open(src, "w", encoding="utf-8").write(pin_html(p, font_css))
            try:
                subprocess.run([chrome, "--headless=new", "--no-sandbox", "--disable-gpu", "--hide-scrollbars",
                                "--force-device-scale-factor=1", "--window-size=1000,1500", "--virtual-time-budget=10000",
                                "--screenshot=" + png, "file://" + src],
                               check=True, timeout=90, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
            except Exception as e:
                print("pins: could not render", p["slug"], e)
        if os.path.exists(png):
            made.append({"slug": p["slug"], "title": p["title"][:100], "description": p["desc"][:500],
                         "link": site + p["link"] + "?utm_content=pinterest", "image": site + "/assets/pins/" + p["slug"] + ".png"})
    shutil.rmtree(tmp, ignore_errors=True)
    open(os.path.join(out_dir, "pins.json"), "w").write(json.dumps(made, indent=1))
    print("pins:", len(made), "images")
    return made
