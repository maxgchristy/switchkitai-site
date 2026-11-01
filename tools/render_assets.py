"""Render the site's icons and share image into assets/.
Usage (from the repo root): python3 tools/render_assets.py /path/to/fonts
Fonts: `npm pack @fontsource/instrument-serif @fontsource-variable/montserrat @fontsource-variable/azeret-mono`, then untar each into a folder named after the package (e.g. fontsource-instrument-serif).
"""
import os, sys, tempfile
from playwright.sync_api import sync_playwright

F = sys.argv[1] if len(sys.argv) > 1 else "/home/claude/fonts"
OUT = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "assets")
os.makedirs(OUT, exist_ok=True)
FONTS = f"""@font-face{{font-family:IS;font-style:italic;font-weight:400;src:url(file://{F}/fontsource-instrument-serif/package/files/instrument-serif-latin-400-italic.woff2)}}
@font-face{{font-family:MS;font-weight:100 900;src:url(file://{F}/fontsource-variable-montserrat/package/files/montserrat-latin-wght-normal.woff2)}}
@font-face{{font-family:AM;font-weight:100 900;src:url(file://{F}/fontsource-variable-azeret-mono/package/files/azeret-mono-latin-wght-normal.woff2)}}"""

def icon(size, pad):
    # Monogram: Blush italic S in a Bottle Green circle on Cream (brief: mark alone works as app icon and favicon).
    r = 0 if size > 100 else size * 0.2
    circ = size * (0.86 if size <= 64 else 0.78)
    return f"""<html><head><style>{FONTS}body{{margin:0}}
.b{{width:{size}px;height:{size}px;background:#fef3e5;border-radius:{r}px;display:grid;place-items:center}}
.c{{width:{circ}px;height:{circ}px;border-radius:50%;background:#274c2e;color:#e7c2a6;display:grid;place-items:center;font:italic 400 {circ*0.66}px/1 IS;padding-bottom:{circ*0.05}px;box-sizing:border-box}}
</style></head><body><div class="b"><div class="c">S</div></div></body></html>"""

share = f"""<html><head><style>{FONTS}body{{margin:0}}
.d{{width:1200px;height:630px;background:#274c2e;display:grid;grid-template-columns:1fr 360px;gap:60px;align-items:center;padding:0 90px;box-sizing:border-box;color:#e7c2a6;position:relative;overflow:hidden}}
.lock{{display:flex;flex-direction:column;align-items:flex-start;gap:8px;margin-bottom:34px}}
.m{{width:54px;height:54px;border-radius:50%;background:#e7c2a6;color:#0d0d0d;display:grid;place-items:center;font:italic 400 36px/1 IS;padding-bottom:3px;box-sizing:border-box}}
.w{{font:italic 400 34px/.99 IS;letter-spacing:-.029em}}
h1{{font:italic 400 81px/.99 IS;letter-spacing:-.029em;margin:0 0 26px}}
.lbl{{font:600 22px AM;font-variant-caps:all-small-caps;letter-spacing:.048em;color:#0d0d0d;background:#e7c2a6;display:inline-block;padding:14px 22px}}
.arch{{position:relative;height:460px;align-self:end}}
.arch i{{position:absolute;left:0;right:0;bottom:0;border-radius:999px 999px 0 0}}
.arch i:nth-child(1){{top:0;background:#e7c2a6}}
.arch i:nth-child(2){{top:60px;left:40px;right:40px;background:#d78f85}}
.arch i:nth-child(3){{top:120px;left:80px;right:80px;background:#0d0d0d}}
.g{{position:absolute;inset:0;opacity:.09;mix-blend-mode:screen;background:url("data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' width='180' height='180'%3E%3Cfilter id='n'%3E%3CfeTurbulence type='fractalNoise' baseFrequency='.85' numOctaves='2' stitchTiles='stitch'/%3E%3CfeColorMatrix values='0 0 0 0 1 0 0 0 0 1 0 0 0 0 1 0 0 0 .6 0'/%3E%3C/filter%3E%3Crect width='100%25' height='100%25' filter='url(%23n)'/%3E%3C/svg%3E")}}
</style></head><body><div class="d"><div><div class="lock"><div class="m">S</div><div class="w">Switch Kit AI</div></div>
<h1>Everyday Jobs, Done by Your AI in One Tap</h1><span class="lbl">60+ shortcuts. Free to try.</span></div>
<div class="arch"><i></i><i></i><i></i></div><div class="g"></div></div></body></html>"""

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
