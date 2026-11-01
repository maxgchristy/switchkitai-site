"""Render the site's icons and share image into assets/.
Usage (from the repo root): python3 tools/render_assets.py /path/to/fonts
Fonts: `npm pack @fontsource/bricolage-grotesque @fontsource/atkinson-hyperlegible`, then untar each into a folder named after the .tgz.
"""
import os, sys, tempfile
from playwright.sync_api import sync_playwright

F = sys.argv[1] if len(sys.argv) > 1 else "/home/claude/fonts"
OUT = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "assets")
os.makedirs(OUT, exist_ok=True)
FONTS = f'''@font-face{{font-family:Bric;font-weight:800;src:url(file://{F}/fontsource-bricolage-grotesque-5.3.0/package/files/bricolage-grotesque-latin-800-normal.woff2)}}
@font-face{{font-family:Atk;font-weight:700;src:url(file://{F}/fontsource-atkinson-hyperlegible-5.3.0/package/files/atkinson-hyperlegible-latin-700-normal.woff2)}}
@font-face{{font-family:Atk;font-weight:400;src:url(file://{F}/fontsource-atkinson-hyperlegible-5.3.0/package/files/atkinson-hyperlegible-latin-400-normal.woff2)}}'''

def icon(size, pad):
    w = size - 2 * pad; h = w
    return f'''<html><head><style>{FONTS}body{{margin:0}}
.b{{width:{size}px;height:{size}px;background:#1c2b4f;display:grid;place-items:center;border-radius:{0 if size>100 else size*0.18}px}}
.c{{width:{w*0.78}px;height:{h*0.92}px;background:#fcfcf6;border-radius:{max(2,size*0.04)}px;position:relative}}
.c i{{position:absolute;left:12%;right:12%;top:24%;height:{max(1.5,size*0.035)}px;background:#d94a40}}
.c b{{position:absolute;left:12%;right:24%;top:42%;height:{size*0.16}px;background:#ffe45c;border-radius:{max(1,size*0.02)}px}}
.c u{{position:absolute;left:12%;right:12%;top:68%;height:{max(1,size*0.025)}px;background:#a7c7e7}}
</style></head><body><div class="b"><div class="c"><i></i><b></b><u></u></div></div></body></html>'''

share = f'''<html><head><style>{FONTS}body{{margin:0}}
.d{{width:1200px;height:630px;background:#eef2f6;display:flex;align-items:center;gap:56px;padding:0 70px;box-sizing:border-box;font-family:Atk;color:#1c2b4f}}
.l{{flex:1}}
.brand{{font-family:Bric;font-weight:800;font-size:30px;margin-bottom:26px;display:flex;align-items:center;gap:14px}}
.brand i{{width:30px;height:36px;border:3px solid #1c2b4f;border-radius:5px;background:#fcfcf6;position:relative;box-sizing:border-box}}.brand i:before{{content:"";position:absolute;left:4px;right:4px;top:9px;height:3px;background:#d94a40}}.brand i:after{{content:"";position:absolute;left:4px;right:7px;top:16px;height:8px;background:#ffe45c;border-radius:2px}}
h1{{font-family:Bric;font-weight:800;font-size:76px;line-height:1;letter-spacing:-2px;margin:0 0 20px}}
p{{font-size:30px;margin:0;color:#5c6578}}
.card{{width:500px;background:#fcfcf6;border-radius:8px;box-shadow:0 30px 60px -30px rgba(28,43,79,.5);transform:rotate(2deg);overflow:hidden;
background-image:repeating-linear-gradient(to bottom,transparent 0,transparent 77px,#a7c7e7 77px,#a7c7e7 78px);background-position:0 70px}}
.h{{height:70px;border-bottom:3px solid #d94a40;box-sizing:border-box;padding:0 22px 10px;display:flex;align-items:flex-end;font-family:Bric;font-weight:800;font-size:22px;color:#5c6578}}
.r{{height:78px;display:flex;align-items:center;justify-content:space-between;padding:0 18px 0 22px;font-weight:700;font-size:24px}}
.r span{{padding:2px 4px}} .r.on span{{background:#ffe45c;border-radius:3px}}
.r em{{font-style:normal;font-size:19px;background:#1c2b4f;color:#fff;border-radius:99px;padding:8px 16px}}
</style></head><body><div class="d"><div class="l"><div class="brand"><i></i>Switch Kit AI</div>
<h1>Never know what to ask AI?</h1><p>Tap a line. Your AI does the rest. Free to try.</p></div>
<div class="card"><div class="h">My AI Cheat Sheet</div>
<div class="r on"><span>Plan 5 easy dinners</span><em>Tap</em></div>
<div class="r"><span>Write a polite email</span><em>Tap</em></div>
<div class="r"><span>Plan a weekend away</span><em>Tap</em></div>
<div class="r"><span>Is this message a scam?</span><em>Tap</em></div>
</div></div></body></html>'''

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
