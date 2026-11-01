"""Render the site's icons and share image into assets/.
Usage (from the repo root): python3 tools/render_assets.py /path/to/fonts
Fonts: `npm pack @fontsource/bricolage-grotesque @fontsource/atkinson-hyperlegible`, then untar each into a folder named after the .tgz.
"""
import os, sys, tempfile
from playwright.sync_api import sync_playwright

F = sys.argv[1] if len(sys.argv) > 1 else "/home/claude/fonts"
OUT = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "assets")
os.makedirs(OUT, exist_ok=True)
FONTS = f"""@font-face{{font-family:AR;font-weight:100 900;font-stretch:62% 125%;src:url(file://{F}/archivo/package/files/archivo-latin-wdth-normal.woff2)}}"""

def icon(size, pad):
    # Butter square with a white checkbox and a cobalt tick: the Kitchen Table mark.
    r = 0 if size > 100 else size * 0.2
    box = size * 0.58; bw = max(2, size * 0.075)
    return f"""<html><head><style>body{{margin:0}}
.b{{width:{size}px;height:{size}px;background:#ffd84d;border-radius:{r}px;display:grid;place-items:center}}
.c{{width:{box}px;height:{box}px;border:{bw}px solid #14213d;border-radius:{size*0.09}px;background:#fff;box-sizing:border-box;position:relative}}
.c:after{{content:"";position:absolute;left:{box*0.28}px;top:{box*0.04}px;width:{box*0.22}px;height:{box*0.48}px;border:solid #2340b8;border-width:0 {bw*1.15}px {bw*1.15}px 0;transform:rotate(45deg)}}
</style></head><body><div class="b"><div class="c"></div></div></body></html>"""

share = f"""<html><head><style>{FONTS}body{{margin:0}}
.d{{width:1200px;height:630px;background:#ffd84d;display:flex;flex-direction:column;justify-content:center;padding:0 90px;box-sizing:border-box;font-family:AR;color:#14213d}}
.brand{{font-weight:800;font-stretch:115%;font-size:30px;display:flex;align-items:center;gap:14px;margin-bottom:30px}}
.brand i{{width:28px;height:28px;border:4px solid #14213d;border-radius:6px;background:#fff;box-sizing:border-box}}
h1{{font-weight:800;font-stretch:125%;font-size:96px;line-height:.98;letter-spacing:-3px;margin:0 0 26px;max-width:960px}}
p{{font-size:34px;margin:0;max-width:880px}}
.btn{{margin-top:38px;align-self:flex-start;background:#2340b8;color:#fff;font-weight:800;font-stretch:110%;font-size:30px;border-radius:12px;padding:22px 34px;box-shadow:0 6px 0 #14213d}}
</style></head><body><div class="d"><div class="brand"><i></i>Kitchen Table</div>
<h1>What's for dinner this week?</h1><p>One tap and your AI plans five easy dinners and the shopping list. Free.</p>
<div class="btn">Plan my week's dinners</div></div></body></html>"""

tmp = tempfile.mkdtemp()
with sync_playwright() as p:
    b = p.chromium.launch()
    for name, size, pad in [("favicon-32.png", 32, 2), ("icon-192.png", 192, 26), ("apple-touch-icon.png", 180, 24)]:
        f = os.path.join(tmp, "ic.html"); open(f, "w").write(icon(size, pad))
        pg = b.new_page(viewport={"width": size, "height": size}); pg.goto("file://" + f); pg.wait_for_timeout(300)
        pg.screenshot(path=os.path.join(OUT, name)); pg.close()
    f = os.path.join(tmp, "sh.html"); open(f, "w").write(share)
    pg = b.new_page(viewport={"width": 1200, "height": 630}); pg.goto("file://" + f); pg.wait_for_timeout(600)
    pg.evaluate("document.fonts.ready"); pg.screenshot(path=os.path.join(OUT, "share.png")); b.close()
print("ok", sorted(os.listdir(OUT)))
