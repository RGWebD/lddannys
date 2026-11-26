"""Logo presentation sheet for L&D Danny's (RGWebD) -> assets/brand/logo-presentation.png"""
import asyncio
from pathlib import Path
from playwright.async_api import async_playwright
B=Path(__file__).parent/'assets'/'brand'
def svg(n): return (B/f'{n}.svg').read_text()
html=f'''<!doctype html><html><head><meta charset="utf-8"><link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Bodoni+Moda:ital,opsz,wght@0,6..96,700;1,6..96,600&family=Jost:wght@400;600&family=Tenor+Sans&display=swap">
<style>body{{margin:0;width:1800px;font-family:Jost;background:#EFE8DC;color:#1B2328}}
.h{{padding:60px 70px 30px;display:flex;justify-content:space-between;align-items:end}}h1{{font:700 54px 'Bodoni Moda';margin:0}}h1 em{{color:#8E6C3B;font-weight:600}}.k{{font:14px 'Tenor Sans';letter-spacing:.24em;text-transform:uppercase;color:#8E6C3B}}
.g{{display:grid;grid-template-columns:repeat(6,1fr);gap:22px;padding:0 70px 22px}}.c{{border-radius:18px;padding:36px;display:flex;align-items:center;justify-content:center;position:relative;min-height:220px}}
.c small{{position:absolute;left:18px;bottom:12px;font:12px 'Tenor Sans';letter-spacing:.18em;text-transform:uppercase;opacity:.6}}
.d{{background:#1B2328;color:#EFE8DC}}.l{{background:#fbf8f2;border:1px solid #D5C8B2}}.br{{background:#B8925A}}
.s2{{grid-column:span 2}}.s3{{grid-column:span 3}}.s4{{grid-column:span 4}}.c svg{{width:100%;height:auto;display:block}}
.sw{{display:flex;gap:16px;padding:0 70px 60px}}.sw div{{flex:1;border-radius:14px;height:130px;padding:14px;display:flex;flex-direction:column;justify-content:flex-end;font-size:14px}}.sw b{{font-weight:600}}
.fav{{display:flex;gap:26px;align-items:end}}.fav img{{display:block}}.fav span{{display:block;font-size:11px;text-align:center;margin-top:6px;opacity:.7}}
.note{{padding:0 70px 50px;font-size:16px;max-width:1300px;color:#5B625F}}</style></head><body>
<div class="h"><div><div class="k">Logo concept · for review</div><h1>L&amp;D Danny’s <em>brand mark</em></h1></div><div class="k">RGWebD · Nov 2026</div></div>
<div class="g"><div class="c d s4" style="min-height:300px"><div style="width:880px">{svg("logo-horizontal-dark")}</div><small>Horizontal · dark</small></div>
<div class="c d s2" style="min-height:300px"><div style="width:230px">{svg("emblem-dark")}</div><small>Emblem</small></div>
<div class="c l s4"><div style="width:820px">{svg("logo-horizontal-light")}</div><small>Horizontal · light</small></div>
<div class="c l s2"><div style="width:300px">{svg("logo-stacked-light")}</div><small>Stacked · light</small></div>
<div class="c d s2"><div style="width:300px">{svg("logo-stacked-dark")}</div><small>Stacked · dark</small></div>
<div class="c br s2"><div style="width:170px">{svg("emblem-mono-dark")}</div><small>One-colour ink</small></div>
<div class="c d s2"><div style="width:170px">{svg("emblem-mono-light")}</div><small>One-colour stone</small></div>
<div class="c l s3"><div class="fav">{"".join(f'<div><img src="favicon-{s}.png" width="{s}" height="{s}"><span>{s}px</span></div>' for s in (16,32,48,180))}</div><small>Favicons / app icon</small></div>
<div class="c l s3"><div style="width:640px">{svg("wordmark-light")}</div><small>Wordmark only</small></div></div>
<div class="sw"><div style="background:#12171A;color:#EFE8DC"><b>Ink</b>#12171A</div><div style="background:#1B2328;color:#EFE8DC"><b>Deep slate</b>#1B2328</div><div style="background:#B8925A"><b>Brass</b>#B8925A</div><div style="background:#D6B47C"><b>Light brass</b>#D6B47C</div><div style="background:#EFE8DC;border:1px solid #D5C8B2"><b>Limestone</b>#EFE8DC</div><div style="background:#D5C8B2"><b>Travertine</b>#D5C8B2</div></div>
<p class="note">Concept: an arched doorway with a keystone (new building) framing the L&amp;D monogram (renovations); the keystone carries a Texas star. Type: Bodoni Moda (display, converted to paths), Playfair Display Italic ampersand, Tenor Sans for the tagline, Jost for body text. Their Google map pin shows an existing “L&amp;D DANNY BUILDING” logo that we could not download — if they have it, this can be adjusted to match.</p></body></html>'''
(B/'presentation.html').write_text(html)
async def main():
    async with async_playwright() as p:
        b=await p.chromium.launch(executable_path='/usr/bin/google-chrome'); pg=await b.new_page(viewport={'width':1800,'height':1000})
        await pg.goto((B/'presentation.html').as_uri()); await pg.wait_for_timeout(1500)
        await pg.screenshot(path=str(B/'logo-presentation.png'),full_page=True); await b.close()
asyncio.run(main()); (B/'presentation.html').unlink(); print('sheet ok')
