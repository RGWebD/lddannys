"""L&D Danny's emblem + wordmark (RGWebD). Text is converted to vector paths with fontTools.
Concept: an arched doorway with a keystone star (new building) framing the L&D monogram (renovations)."""
import io, sys
from pathlib import Path
from fontTools.ttLib import TTFont
from fontTools.varLib import instancer
from fontTools.pens.svgPathPen import SVGPathPen
from fontTools.pens.transformPen import TransformPen
from fontTools.pens.boundsPen import BoundsPen
import cairosvg
from PIL import Image
G='/usr/share/fonts/truetype/sand-box/google/'
OUT=Path(__file__).parent/'assets'/'brand'; OUT.mkdir(parents=True,exist_ok=True)
SLATE='#1B2328'; INK='#12171A'; STONE='#EFE8DC'; BRASS='#B8925A'; BRASS2='#D6B47C'
_fc={}
def font(path,**axes):
    k=(path,tuple(sorted(axes.items())))
    if k not in _fc:
        f=TTFont(G+path)
        if axes: f=instancer.instantiateVariableFont(f,axes)
        _fc[k]=f
    return _fc[k]
BOD=lambda w=700: font('Bodoni Moda/BodoniModa-VariableFont_opsz,wght.ttf',wght=w,opsz=28)
PFI=lambda w=700: font('Playfair Display/PlayfairDisplay-Italic-VariableFont_wght.ttf',wght=w)
TEN=lambda: font('Tenor Sans/TenorSans-Regular.ttf')
def text(f,s,size,x=0,y=0,track=0,anchor='start'):
    """returns (path d, width) — y is baseline"""
    gs=f.getGlyphSet(); cmap=f.getBestCmap(); upm=f['head'].unitsPerEm; sc=size/upm
    adv=[];names=[]
    for ch in s:
        n=cmap[ord(ch)]; names.append(n); adv.append(gs[n].width*sc)
    W=sum(adv)+track*(len(s)-1)
    x0=x-(W/2 if anchor=='middle' else W if anchor=='end' else 0)
    pen=SVGPathPen(gs); cx=x0
    for n,a in zip(names,adv):
        gs[n].draw(TransformPen(pen,(sc,0,0,-sc,cx,y))); cx+=a+track
    d=pen.getCommands()
    return d,W
def glyph_bounds(f,ch,size):
    gs=f.getGlyphSet(); n=f.getBestCmap()[ord(ch)]; bp=BoundsPen(gs); gs[n].draw(bp); sc=size/f['head'].unitsPerEm
    b=bp.bounds; return [v*sc for v in b], gs[n].width*sc
def star(cx,cy,R,r=None):
    import math
    r=r or R*0.42; pts=[]
    for i in range(10):
        a=math.radians(-90+36*i); rr=R if i%2==0 else r
        pts.append(f'{cx+rr*math.cos(a):.2f},{cy+rr*math.sin(a):.2f}')
    return 'M'+' L'.join(pts)+'Z'

def monogram(cx,base,size,col_l,col_amp):
    """L & D centered at cx; returns svg"""
    fL=BOD(800); fA=PFI(700)
    dL,wL=text(fL,'L',size); dD,wD=text(fL,'D',size)
    ampsize=size*0.78; dA,wA=text(fA,'&',ampsize)
    gap=-size*0.06
    total=wL+wA+wD+2*gap; x=cx-total/2
    dL,_=text(fL,'L',size,x,base); dA,_=text(fA,'&',ampsize,x+wL+gap,base-size*0.02); dD,_=text(fL,'D',size,x+wL+wA+2*gap,base)
    return f'<path d="{dL} {dD}" fill="{col_l}"/><path d="{dA}" fill="{col_amp}"/>'

def emblem(fg=STONE,acc=BRASS,bg=None,x=0,y=0,s=1,bold=False):
    """emblem in a 200x240 box: arch doorway + keystone star + threshold + monogram"""
    sw=9 if bold else 6
    g=[f'<g transform="translate({x},{y}) scale({s})">']
    if bg: g.append(f'<rect width="200" height="240" rx="22" fill="{bg}"/>')
    # outer arch (doorway): straight jambs, semicircle head
    L,R,T,B=26,174,30,206; rad=(R-L)/2; cxa=(L+R)/2; cy=T+rad
    g.append(f'<path d="M{L} {B} V{cy} A{rad} {rad} 0 0 1 {R} {cy} V{B}" fill="none" stroke="{acc}" stroke-width="{sw}" stroke-linejoin="miter"/>')
    if not bold:
        L2,R2=L+13,R-13; r2=(R2-L2)/2
        g.append(f'<path d="M{L2} {B} V{cy} A{r2} {r2} 0 0 1 {R2} {cy} V{B}" fill="none" stroke="{acc}" stroke-width="1.6"/>')
    # keystone with star
    kw_t,kw_b,kh=34,24,30
    g.append(f'<path d="M{cxa-kw_t/2} {T-14} H{cxa+kw_t/2} L{cxa+kw_b/2} {T-14+kh} H{cxa-kw_b/2}Z" fill="{acc}"/>')
    g.append(f'<path d="{star(cxa,T+1.5,8.6)}" fill="{bg or SLATE if fg==STONE else fg}"/>')
    # threshold / plinth
    g.append(f'<rect x="{L-14}" y="{B}" width="{R-L+28}" height="{8 if bold else 6}" fill="{acc}"/>')
    g.append(f'<rect x="{L-4}" y="{B+(12 if bold else 10)}" width="{R-L+8}" height="{3 if bold else 2}" fill="{acc}"/>')
    g.append(monogram(cxa,cy+50,52,fg,acc))
    g.append('</g>')
    return ''.join(g)

def wordmark(x,y,fg,acc,size=64,sub=True,anchor='start',track_main=None):
    f=BOD(700); t=TEN()
    tm=size*0.08 if track_main is None else track_main
    d1,w1=text(f,'L&D DANNY’S',size,0,0,tm)
    out=[]
    # main line: L&D in brass? keep fg, apostrophe ok
    x0 = x - (w1/2 if anchor=='middle' else 0)
    dA,_=text(f,'L&D',size,x0,y,tm); _,wld=text(f,'L&D ',size,0,0,tm)
    dB,_=text(f,'DANNY’S',size,x0+wld+tm,y,tm)
    out.append(f'<path d="{dA}" fill="{acc}"/><path d="{dB}" fill="{fg}"/>')
    W=w1
    if sub:
        ss=size*0.235; d2,w2=text(t,'NEW BUILDING & RENOVATIONS',ss,0,0,ss*0.42)
        # stretch tracking so sub matches main width
        n=len('NEW BUILDING & RENOVATIONS'); base_w=w2-ss*0.42*(n-1); tr=(w1-base_w)/(n-1)
        d2,_=text(t,'NEW BUILDING & RENOVATIONS',ss,x0,y+size*0.62,tr)
        out.append(f'<path d="{d2}" fill="{fg}" fill-opacity=".86"/>')
        out.append(f'<rect x="{x0}" y="{y+size*0.20}" width="{w1}" height="{max(1.4,size*0.022)}" fill="{acc}"/>')
    return ''.join(out),W

def svgdoc(w,h,body,bg=None):
    b=f'<rect width="{w}" height="{h}" fill="{bg}"/>' if bg else ''
    return f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {w} {h}" width="{w}" height="{h}">{b}{body}</svg>'

def save(name,svg):
    (OUT/f'{name}.svg').write_text(svg)
def png(name,svg,w):
    cairosvg.svg2png(bytestring=svg.encode(),write_to=str(OUT/f'{name}.png'),output_width=w)

variants={'dark':(STONE,BRASS),'light':(SLATE,'#9A7440'),'mono-light':(STONE,STONE),'mono-dark':(INK,INK)}
for v,(fg,acc) in variants.items():
    em=emblem(fg,acc)
    save(f'emblem-{v}',svgdoc(200,240,em))
    wm,W=wordmark(0,62,fg,acc,64)
    save(f'wordmark-{v}',svgdoc(int(W)+4,112,wm))
    # horizontal: emblem 120 tall + wordmark
    em2=emblem(fg,acc,x=0,y=0,s=0.5)
    wm2,W2=wordmark(118,72,fg,acc,52)
    save(f'logo-horizontal-{v}',svgdoc(int(118+W2+6),122,em2+wm2))
    # stacked
    wm3,W3=wordmark(0,0,fg,acc,46,anchor='middle')
    Wst=max(W3,200)+20
    em3=emblem(fg,acc,x=Wst/2-100,y=0)
    wm3,_=wordmark(Wst/2,300,fg,acc,46,anchor='middle')
    save(f'logo-stacked-{v}',svgdoc(int(Wst),345,em3+wm3))
# favicon: bold arch, no inner line, on slate tile
fav=svgdoc(200,240,emblem(STONE,BRASS2,bg=SLATE,bold=True))
def favdoor():
    L,R,T,B=22,178,22,214; rad=(R-L)/2; cy=T+rad; cxa=100
    g=f'<path d="M{L} {B} V{cy} A{rad} {rad} 0 0 1 {R} {cy} V{B}Z" fill="{BRASS2}"/>'
    g+=f'<path d="{star(cxa,T+30,15)}" fill="{SLATE}"/>'
    g+=monogram(cxa,cy+64,70,SLATE,SLATE)
    return g
fav_sq=f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="-20 0 240 240" width="240" height="240"><rect x="-20" width="240" height="240" rx="44" fill="{SLATE}"/>{favdoor()}</svg>'
save('favicon',fav_sq)
for s in (16,32,48,180,192,512): png(f'favicon-{s}',fav_sq,s)
ims=[Image.open(OUT/f'favicon-{s}.png') for s in (16,32,48)]
Image.open(OUT/'favicon-512.png').save(OUT/'favicon.ico',sizes=[(16,16),(32,32),(48,48)])
# big pngs for OG / site
png('emblem-dark-800',(OUT/'emblem-dark.svg').read_text(),800)
png('logo-horizontal-dark-1200',(OUT/'logo-horizontal-dark.svg').read_text(),1200)
print('ok')
