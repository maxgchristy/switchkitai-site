"""Render the site's icons and share image into assets/.
Usage (from the repo root): python3 tools/render_assets.py /path/to/fonts
Fonts: `npm pack @fontsource/bricolage-grotesque @fontsource/atkinson-hyperlegible`, then untar each into a folder named after the .tgz.
"""
import os, sys, tempfile
from playwright.sync_api import sync_playwright

F = sys.argv[1] if len(sys.argv) > 1 else "/home/claude/fonts"
OUT = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "assets")
os.makedirs(OUT, exist_ok=True)
FONTS = f"""@font-face{{font-family:PS;font-weight:800;src:url(file://{F}/fontsource-public-sans-5.3.0/package/files/public-sans-latin-800-normal.woff2)}}
@font-face{{font-family:PS;font-weight:600;src:url(file://{F}/fontsource-public-sans-5.3.0/package/files/public-sans-latin-600-normal.woff2)}}
@font-face{{font-family:PS;font-weight:400;src:url(file://{F}/fontsource-public-sans-5.3.0/package/files/public-sans-latin-400-normal.woff2)}}"""

def icon(size, pad):
    # Green square, three white lines with a check on the first: a simple list of things done.
    r = 0 if size > 100 else size * 0.2
    return f"""<html><head><style>body{{margin:0}}
.b{{width:{size}px;height:{size}px;background:#1f5d4c;border-radius:{r}px;display:flex;flex-direction:column;justify-content:center;gap:{size*0.11}px;padding:0 {size*0.24}px;box-sizing:border-box}}
.b i{{display:block;height:{max(2,size*0.075)}px;background:#fff;border-radius:{size}px}}
.b i:nth-child(2){{width:78%}} .b i:nth-child(3){{width:56%}}
</style></head><body><div class="b"><i></i><i></i><i></i></div></body></html>"""

share = f"""<html><head><style>{FONTS}body{{margin:0}}
.d{{width:1200px;height:630px;background:#fff;display:flex;flex-direction:column;justify-content:center;padding:0 90px;box-sizing:border-box;font-family:PS;color:#1d2433}}
.brand{{font-weight:600;font-size:28px;display:flex;align-items:center;gap:14px;margin-bottom:34px}}
.brand i{{width:22px;height:22px;border-radius:6px;background:#1f5d4c}}
h1{{font-weight:800;font-size:92px;line-height:1;letter-spacing:-3px;margin:0 0 26px;max-width:900px}}
p{{font-size:34px;margin:0;color:#5b6475;max-width:880px}}
.btn{{margin-top:40px;align-self:flex-start;background:#1f5d4c;color:#fff;font-weight:700;font-size:30px;border-radius:14px;padding:22px 34px}}
</style></head><body><div class="d"><div class="brand"><i></i>Switch Kit AI</div>
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
