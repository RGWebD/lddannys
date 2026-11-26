#!/usr/bin/env python3
"""Generator for the L&D Danny's New Building and Renovations demo site (RGWebD).
Facts: /workspace/lead-ll1f/notes.md (Google Business Profile). Writes /workspace/lddannys/site."""
import json, shutil, html, sys
from pathlib import Path
from PIL import Image
GEN=Path(__file__).parent; OUT=Path('/workspace/lddannys/site')
REPO='lddannys'; BASE=f'https://rgwebd.github.io/{REPO}/'
NAME='L&D Danny’s New Building and Renovations'; SHORT='L&D Danny’s'
GNAME='L&D DANNY’S NEW BUILDING AND RENOVATIONS'
PHONE='(817) 271-9465'; TEL='tel:+18172719465'; SMS='sms:+18172719465'
ADDR1='5607 Humbert Ave'; CITY='Fort Worth'; ST='TX'; ZIP='76107'; ADDR=f'{ADDR1}, {CITY}, {ST} {ZIP}'
LAT,LNG=32.7185411,-97.4066008
GMAPS='https://www.google.com/maps/place/L%26D+DANNY%E2%80%99S+NEW+BUILDING+AND+RENOVATIONS/@32.7185411,-97.4066008,14z/data=!4m6!3m5!1s0x864e73c94cb11ab7:0x7b06e44c6ac338e5!8m2!3d32.7185411!4d-97.4066008!16s%2Fg%2F11v3kzjpg_'
GREV='https://maps.app.goo.gl/LL1FVFsF5Jd13f2d6'
DIR='https://www.google.com/maps/dir/?api=1&destination=5607+Humbert+Ave%2C+Fort+Worth%2C+TX+76107'
MAPEMBED='https://www.google.com/maps?q=5607+Humbert+Ave,+Fort+Worth,+TX+76107&z=15&output=embed'
RATING=5.0; COUNT=13
e=html.escape

# ---------------- assets ----------------
OUT.mkdir(parents=True,exist_ok=True)
for p in OUT.iterdir():
    if p.name in ('.git',): continue
    shutil.rmtree(p) if p.is_dir() else p.unlink()
A=OUT/'assets'; shutil.copytree(GEN/'assets'/'img',A/'img'); shutil.copytree(GEN/'assets'/'brand',A/'brand')
shutil.copy(GEN/'assets/brand/favicon.ico',OUT/'favicon.ico'); shutil.copy(GEN/'assets/brand/favicon-180.png',OUT/'apple-touch-icon.png')
shutil.copy(GEN/'src/styles.css',A/'styles.css'); shutil.copy(GEN/'src/script.js',A/'script.js')
G=OUT/'generator'; G.mkdir(); (G/'src').mkdir()
for f in ['build.py','process.py','logo.py','qa.py','shots.py','sheet.py']:
    if (GEN/f).exists(): shutil.copy(GEN/f,G/f)
for f in ['styles.css','script.js']: shutil.copy(GEN/'src'/f,G/'src'/f)
# OG image: hero photo + horizontal logo
og=Image.open(GEN/'assets/img/g16-1600.webp').convert('RGB').resize((1200,900)).crop((0,135,1200,765))
dk=Image.new('RGB',og.size,(18,23,26)); m=Image.linear_gradient('L').rotate(90).resize(og.size)
og=Image.composite(og,dk,m.point(lambda v:int(40+v*.72)))
lg=Image.open(GEN/'assets/brand/logo-horizontal-dark-1200.png').convert('RGBA'); lg=lg.resize((640,round(lg.height*640/lg.width)),Image.LANCZOS)
og=og.convert('RGBA'); og.alpha_composite(lg,(56,630-lg.height-60)); og.convert('RGB').save(A/'og-image.jpg',quality=86)

def dims(n,w=1600): return Image.open(A/'img'/f'{n}-{w}.webp').size
def pic(n,alt=None,cls='',sizes='(max-width:900px) 100vw, 50vw',eager=False,attrs=''):
    alt=PH[n] if alt is None else alt
    w,h=dims(n); w8,_=dims(n,800)
    ld='fetchpriority="high"' if eager else 'loading="lazy"'
    return (f'<img src="assets/img/{n}-1600.webp" srcset="assets/img/{n}-800.webp {w8}w, assets/img/{n}-1600.webp {w}w" sizes="{sizes}" '
            f'width="{w}" height="{h}" alt="{e(alt)}" {ld} decoding="async"{(" class=\""+cls+"\"") if cls else ""} {attrs}>')

PH={ # checked by eye, one by one
'g01':'Kitchen with white cabinets, pendant lights and a stone-faced breakfast bar',
'g03':'Frameless glass shower with brass hardware and marble-look tile',
'g04':'Slate-blue cabinet with a stone top, undermount sink and wood floating shelves',
'g05':'Gray shaker vanity with an octagonal mirror beside plantation shutters',
'g06':'L-shaped wood floating vanity under black wall sconces',
'g07':'Polished marble-look porcelain floor running down a hallway',
'g08':'Master bath with marble-look walls, a freestanding tub and a double vanity',
'g09':'Freestanding tub beside a walk-in shower with a patterned mosaic floor',
'g10':'The crew setting large marble-look tile around a glass block window',
'g11':'Kitchen island with bar seating, woven pendants and lit glass-front uppers',
'g12':'Stamped concrete patio floor with a Texas star medallion',
'g14':'Dining room with a crystal chandelier, crown molding and dark wood floors',
'g15':'Living room with a stacked-stone fireplace wall and lit floating shelves',
'g16':'Bathroom with a tiled tub surround, plantation shutters and gray vanities',
'g17':'Master bath with a freestanding tub, glass block window and L-shaped vanity',
'g18':'Kitchen island with a wood base, white countertop and pendant lights',
'g19':'Black kitchen island on a marble-look tile floor',
'g20':'Feature wall of diamond-pattern tile with a wood hook rail',
'g22':'Backlit mirror over a wood vanity with a lowered makeup counter',
'g23':'Bedroom with dark wood floors, recessed lights and a ceiling fan',
'g24':'Kitchen with stained raised-panel cabinets and a granite island',
'g25':'Marble-look master bath with a freestanding tub and double doors',
'bp16':'Line drawing traced from the same bathroom photo',
}

IC={
'phone':'<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M22 16.9v3a2 2 0 0 1-2.2 2 19.8 19.8 0 0 1-8.6-3.1 19.5 19.5 0 0 1-6-6A19.8 19.8 0 0 1 2.1 4.2 2 2 0 0 1 4.1 2h3a2 2 0 0 1 2 1.7c.1 1 .4 1.9.7 2.8a2 2 0 0 1-.5 2.1L8 9.9a16 16 0 0 0 6 6l1.3-1.3a2 2 0 0 1 2.1-.4c.9.3 1.8.6 2.8.7a2 2 0 0 1 1.7 2z"/></svg>',
'arrow':'<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M5 12h14M13 6l6 6-6 6"/></svg>',
'left':'<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" aria-hidden="true"><path d="M15 6l-6 6 6 6"/></svg>',
'right':'<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" aria-hidden="true"><path d="M9 6l6 6-6 6"/></svg>',
'x':'<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" aria-hidden="true"><path d="M6 6l12 12M18 6L6 18"/></svg>',
'pin':'<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M12 22s7-6.2 7-12a7 7 0 0 0-14 0c0 5.8 7 12 7 12z"/><circle cx="12" cy="10" r="2.6"/></svg>',
'chat':'<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M21 12a8 8 0 0 1-11.8 7L3 21l2-6.2A8 8 0 1 1 21 12z"/></svg>',
'clock':'<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" aria-hidden="true"><circle cx="12" cy="12" r="9"/><path d="M12 7v5l3 2"/></svg>',
'star':'<svg viewBox="0 0 24 24" aria-hidden="true"><path fill="currentColor" d="M12 2.5l2.9 6.2 6.6.7-5 4.5 1.4 6.6L12 17.2l-5.9 3.3 1.4-6.6-5-4.5 6.6-.7z"/></svg>',
'grid':'<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" aria-hidden="true"><rect x="3" y="3" width="7" height="7"/><rect x="14" y="3" width="7" height="7"/><rect x="3" y="14" width="7" height="7"/><rect x="14" y="14" width="7" height="7"/></svg>',
'broom':'<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M19 3l-7 7M9 9l6 6-3 6c-3-1-7-5-8-8z"/><path d="M7 15l-2 2"/></svg>',
'idea':'<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M9 18h6M10 22h4M12 2a7 7 0 0 0-4 12.7c.6.5 1 1.3 1 2.3h6c0-1 .4-1.8 1-2.3A7 7 0 0 0 12 2z"/></svg>',
'repeat':'<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M17 2l4 4-4 4"/><path d="M3 11V9a3 3 0 0 1 3-3h15M7 22l-4-4 4-4"/><path d="M21 13v2a3 3 0 0 1-3 3H3"/></svg>',
'hand':'<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M20 6L9 17l-5-5"/></svg>',
}
def btn_call(cls='',lbl=None): return f'<a class="btn mag {cls}" href="{TEL}">{IC["phone"]}<span>{lbl or "Call "+PHONE}</span></a>'
def stars(r,cls=''): return f'<span class="stars5 {cls}" role="img" aria-label="{r:.1f} out of 5 stars"><i style="--w:{r/5*100:.1f}%"></i></span>'
TXSTAR='<svg class="txs" viewBox="0 0 24 24" aria-hidden="true"><path fill="currentColor" d="M12 1.8l2.6 7.3h7.7l-6.2 4.6 2.3 7.4L12 16.6l-6.4 4.5 2.3-7.4L1.7 9.1h7.7z"/></svg>'

# ---------------- reviews (Google, 5★, word for word) ----------------
REV=[
('kathryn','Kathryn Prager','4 months ago','We couldn\'t be happier with the work L&D Danny\'s New Building and Renovations company did on our home! They completely remodeled all five of our bathrooms, including our master bath, as well as our laundry room and office. This wasn\'t just …',True),
('jill','Jill Allison','5 months ago','We did a whole home remodel and Danny and his crew did an excellent job.  They went above and beyond my expectations and made sure everything was exactly what we wanted. This is the only company I will use from now on.',False),
('deanne','Deanne Brewster','3 years ago','We just did a total renovation on our master bath and Daniel and his crews did the majority of it. During the demo, which is usually the messiest part, his crews left each night with it being neater than it was before the demo. They took …',True),
('sadaf','Sadaf Khan','2 years ago','Danny and his team renovated my master bath, kitchen and fireplace. Excellent work ! Could not be happier. They are very professional. I loved their work ethics. They give great input on renovation ideas too and by the end of the project …',True),
('tracy','Tracy Thomas','3 years ago','Danny and his crew are professional and reliable which is hard ti come by. They do excellent work and aim to always make the customer happy. I have worked with them for the past five years on many projects. Highly recommend.',False),
('tammy','tammy patton','3 years ago','Does great work again and again! I have used them for multiple jobs, from whole house renovations to small tile jobs and I am always pleased with the results. Daniel has great ideas if you need suggestions and his crew is always friendly and professional.',False),
('teresa','Teresa Martinez','2 years ago','If you are looking for a good remodeling company and ready for something different for a restroom, room, etc. Thisis the company to call really GREAT work done on my kitchen LOVED IT!!',False),
('traci','Traci Jenkins','3 years ago','I absolutely love these guys! They are honest, competent, affordable and hard-working. I only use them for anything and everything regarding my home improvement and repair needs.',False),
('nitza','Nitza Rangel','2 years ago','Danny did the complete remodel of my bathroom, he is professional and serious, I highly recommend him.',False),
('brenda','Brenda Garcia','9 months ago','The best remodeler in the metroplex',False),
]
LG={'tammy','traci','nitza'}
RD={r[0]:r for r in REV}
def rtext(k): return e(' '.join(RD[k][3].split()))
def rcard(k,cls='rv-card'):
    _,n,age,t,tr=RD[k]
    note='<small class="trunc">Shortened by Google</small>' if tr else ''
    note2=' <small class="trunc">Translated from Spanish by Google</small>' if k=='brenda' else ''
    lg=' · Local Guide' if k in LG else ''
    return (f'<figure class="{cls}"><div class="rv-top">{stars(5)}<span class="g">Google</span></div><blockquote><p>“{rtext(k)}”</p></blockquote>'
            f'<figcaption><b>{e(n)}</b><span>{e(age)}{lg}</span>{note}{note2}</figcaption></figure>')

# ---------------- page shell ----------------
NAVL=[('index.html','Home'),('services.html','Services'),('work.html','Our Work'),('reviews.html','Reviews'),('contact.html','Contact')]
HOURS=[(1,'Monday','8 AM – 5 PM'),(2,'Tuesday','8 AM – 5 PM'),(3,'Wednesday','8 AM – 5 PM'),(4,'Thursday','8 AM – 5 PM'),(5,'Friday','8 AM – 5 PM'),(6,'Saturday','9 AM – 4 PM'),(0,'Sunday','Closed')]
def hours_tbl(cls='hours'):
    return (f'<table class="{cls}"><caption class="sr">Business hours</caption><tbody>'+''.join(f'<tr data-d="{d}"{" class=off" if h=="Closed" else ""}><th scope="row">{n}</th><td>{h}</td></tr>' for d,n,h in HOURS)+'</tbody></table>'
            '<p class="hol">Thanksgiving and Black Friday hours might differ. Please call to confirm.</p>')
LOGO_H=lambda v='dark': (GEN/'assets/brand'/f'logo-horizontal-{v}.svg').read_text().replace('<svg ','<svg class="lgo" role="img" aria-label="L&amp;D Danny’s New Building and Renovations" ',1)
def header(cur):
    nav=''.join(f'<a href="{f}"{" aria-current=page" if f==cur else ""}>{t}</a>' for f,t in NAVL)
    mnav=''.join(f'<a class="l" href="{f}"{" aria-current=page" if f==cur else ""}><span>{t}</span></a>' for f,t in NAVL)
    return f'''<a class="skip" href="#main">Skip to content</a>
<div class="lvl" aria-hidden="true"><i></i><b></b></div>
<header class="hdr"><div class="hdr-in">
<a class="brand" href="index.html" aria-label="L&amp;D Danny’s home">{LOGO_H()}</a>
<nav class="nav" aria-label="Main">{nav}</nav>
<div class="hdr-cta"><span class="ob" data-status aria-live="polite"><i></i><span>Hours</span></span>{btn_call('sm brass','Call now')}
<button class="burger" type="button" aria-expanded="false" aria-controls="mnav" aria-label="Open menu"><span></span><span></span></button></div></div></header>
<div class="mnav" id="mnav" role="dialog" aria-modal="true" aria-label="Menu"><nav aria-label="Mobile">{mnav}</nav>
<div class="mnav-ft">{btn_call('brass')}<p>{ADDR}<br>Mon–Fri 8–5 · Sat 9–4 · Sun closed</p></div></div>'''
def footer():
    links=''.join(f'<li><a href="{f}">{t}</a></li>' for f,t in NAVL)
    return f'''<footer class="ftr"><div class="outline-x" aria-hidden="true">FORT WORTH</div><div class="wrap ftr-g">
<div class="ftr-b">{LOGO_H()}<p>Bathroom and kitchen remodels, tile, cabinetry, fireplace walls and whole-home renovations in Fort Worth, Texas.</p>
<p class="rt">{stars(RATING)} <b>5.0</b> · {COUNT} Google reviews</p></div>
<div><h2 class="fh">Pages</h2><ul class="fl">{links}</ul></div>
<div><h2 class="fh">Visit</h2><address><b>{e(NAME)}</b><br>{ADDR1}<br>{CITY}, {ST} {ZIP}<br><a href="{TEL}">{PHONE}</a></address><p><a class="ul" href="{DIR}" target="_blank" rel="noopener">Get directions</a> · <a class="ul" href="{GMAPS}" target="_blank" rel="noopener">Google profile</a></p></div>
<div><h2 class="fh">Hours</h2>{hours_tbl('hours sm')}</div></div>
<div class="wrap ftr-bt"><p>© 2026 {e(NAME)}. Photos from the business’s Google profile.</p><p>Design preview by <a class="ul" href="https://github.com/RGWebD" target="_blank" rel="noopener">RGWebD</a></p></div></footer>
<div class="mbar" aria-label="Quick contact">{btn_call('brass','Call')}<a class="btn ghost-l" href="{SMS}?&amp;body={e('Hi L&D Danny’s, I’d like to talk about a remodel.')}">{IC["chat"]}<span>Text</span></a><a class="btn ghost-l" href="{DIR}" target="_blank" rel="noopener">{IC["pin"]}<span>Map</span></a></div>
<div class="demo" role="note"><span>Design preview by <b>RGWebD</b></span><button type="button" aria-label="Dismiss preview note">{IC["x"]}</button></div>
<div class="tlb" role="dialog" aria-modal="true" aria-label="Photo viewer" hidden><button class="tlb-x" type="button" aria-label="Close">{IC["x"]}</button><button class="tlb-p" type="button" aria-label="Previous photo">{IC["left"]}</button><figure><img alt=""><figcaption></figcaption></figure><button class="tlb-n" type="button" aria-label="Next photo">{IC["right"]}</button></div>'''

def biz_ld(full=False):
    d={"@context":"https://schema.org","@type":["HomeAndConstructionBusiness","GeneralContractor"],"@id":BASE+"#business",
       "name":NAME,"alternateName":GNAME,"url":BASE,"telephone":"+1-817-271-9465","image":[BASE+"assets/img/g08-1600.webp",BASE+"assets/img/g15-1600.webp"],
       "logo":BASE+"assets/brand/favicon-512.png",
       "address":{"@type":"PostalAddress","streetAddress":ADDR1,"addressLocality":CITY,"addressRegion":ST,"postalCode":ZIP,"addressCountry":"US"},
       "geo":{"@type":"GeoCoordinates","latitude":LAT,"longitude":LNG},"hasMap":GMAPS,
       "areaServed":{"@type":"City","name":"Fort Worth, TX"},
       "openingHoursSpecification":[{"@type":"OpeningHoursSpecification","dayOfWeek":["Monday","Tuesday","Wednesday","Thursday","Friday"],"opens":"08:00","closes":"17:00"},
                                    {"@type":"OpeningHoursSpecification","dayOfWeek":"Saturday","opens":"09:00","closes":"16:00"}],
       "aggregateRating":{"@type":"AggregateRating","ratingValue":"5.0","reviewCount":COUNT,"bestRating":"5","worstRating":"1"},
       "amenityFeature":[{"@type":"LocationFeatureSpecification","name":"Wheelchair-accessible entrance","value":True},{"@type":"LocationFeatureSpecification","name":"Wheelchair-accessible parking lot","value":True}],
       "knowsAbout":["Bathroom remodeling","Master bath renovation","Kitchen remodeling","Tile installation","Cabinetry and vanities","Fireplace and feature walls","Whole-home remodeling"],
       "hasOfferCatalog":{"@type":"OfferCatalog","name":"Remodeling services","itemListElement":[{"@type":"Offer","itemOffered":{"@type":"Service","name":s}} for s in ["Bathroom remodels","Kitchen remodels","Tile work","Cabinetry and vanities","Fireplace and feature walls","Whole-home remodels"]]}}
    if full:
        d["review"]=[{"@type":"Review","author":{"@type":"Person","name":n},"reviewRating":{"@type":"Rating","ratingValue":"5","bestRating":"5"},"reviewBody":' '.join(t.split()),"publisher":{"@type":"Organization","name":"Google"}} for _,n,_,t,_ in REV]
    return d
def crumbs(cur,title):
    items=[{"@type":"ListItem","position":1,"name":"Home","item":BASE}]
    if cur!='index.html': items.append({"@type":"ListItem","position":2,"name":title,"item":BASE+cur})
    return {"@context":"https://schema.org","@type":"BreadcrumbList","itemListElement":items}
def page(fn,title,desc,body,extra_ld=(),home=False,full_reviews=False,crumb=None):
    lds=[biz_ld(full_reviews),crumbs(fn,crumb or title)]+list(extra_ld)
    ld=''.join(f'<script type="application/ld+json">{json.dumps(x,ensure_ascii=False)}</script>' for x in lds)
    url=BASE+('' if fn=='index.html' else fn)
    loader=''
    if home:
        tiles=''.join(f'<i style="--d:{(i%8+i//8)*45}ms"></i>' for i in range(40))
        loader=f'<div class="ldr" aria-hidden="true"><div class="ldr-t">{tiles}</div><div class="ldr-e">{(GEN/"assets/brand/emblem-dark.svg").read_text()}</div></div>'
    return f'''<!doctype html><html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>{e(title)}</title><meta name="description" content="{e(desc)}"><link rel="canonical" href="{url}">
<meta property="og:type" content="website"><meta property="og:site_name" content="{e(NAME)}"><meta property="og:title" content="{e(title)}"><meta property="og:description" content="{e(desc)}"><meta property="og:url" content="{url}"><meta property="og:image" content="{BASE}assets/og-image.jpg"><meta property="og:image:width" content="1200"><meta property="og:image:height" content="630">
<meta name="twitter:card" content="summary_large_image"><meta name="twitter:title" content="{e(title)}"><meta name="twitter:description" content="{e(desc)}"><meta name="twitter:image" content="{BASE}assets/og-image.jpg">
<meta name="theme-color" content="#1B2328"><link rel="icon" href="favicon.ico" sizes="any"><link rel="icon" type="image/svg+xml" href="assets/brand/favicon.svg"><link rel="apple-touch-icon" href="apple-touch-icon.png">
<link rel="preconnect" href="https://fonts.googleapis.com"><link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Bodoni+Moda:ital,opsz,wght@0,6..96,500..800;1,6..96,500..700&family=Jost:wght@400;500;600&family=Tenor+Sans&display=swap">
<link rel="stylesheet" href="assets/styles.css">{ld}</head>
<body class="{'home' if home else 'inner'}">{loader}{header(fn)}<main id="main">{body}</main>{footer()}<script src="assets/script.js" defer></script></body></html>'''

def phero(kicker,h1,lead,img,crumb,pos='50% 50%',ctas=True):
    c=f'<div class="ctas">{btn_call("brass")}<a class="btn ghost-l mag" href="contact.html">{IC["chat"]}<span>Ask about a project</span></a></div>' if ctas else ''
    return f'''<section class="phero"><div class="phero-f">{pic(img,sizes="100vw",eager=True,cls="kb",attrs=f'style="object-position:{pos}"')}</div>
<div class="phero-c wrap"><nav class="bc" aria-label="Breadcrumb"><a href="index.html">Home</a><span aria-hidden="true">/</span><span aria-current="page">{crumb}</span></nav>
<p class="kicker lt">{kicker}</p><h1 class="split">{h1}</h1><p class="lead">{lead}</p>{c}</div></section>'''
def cta_band(h,p,img=None):
    bg=f'<div class="cta-bg">{pic(img,sizes="100vw")}</div>' if img else '<div class="cta-bg gfx" aria-hidden="true"><span>CALL</span><span>DANNY’S</span></div>'
    return f'''<section class="cta">{bg}<div class="wrap cta-in" data-r><div class="arch-mini" aria-hidden="true">{TXSTAR}</div><h2 class="split">{h}</h2><p>{p}</p>
<div class="ctas c">{btn_call("brass xl")}<a class="btn ghost-l mag" href="{SMS}?&amp;body={e("Hi L&D Danny’s, I’d like to talk about a remodel.")}">{IC["chat"]}<span>Send a text</span></a></div></div></section>'''

MARQ=['Bathroom remodels','Kitchen remodels','Tile work','Cabinetry & vanities','Fireplace & feature walls','Whole-home remodels','Master bath renovations','Small tile jobs too']
def marquee(cls=''):
    row=''.join(f'<span>{e(t)}</span>{TXSTAR}' for t in MARQ)
    return f'<div class="marq {cls}" aria-label="Services: {e(", ".join(MARQ[:6]))}"><div class="marq-t" aria-hidden="true">{row}{row}</div></div>'

# ================= HOME =================
ROOMS=[('bath','Bathrooms','g16','Master baths, full guest-bath refreshes and walk-in showers, from demo to the last fixture.','deanne','his crews left each night with it being neater than it was before the demo.','Deanne Brewster'),
('kitchen','Kitchens','g11','Islands, cabinets, countertops and pendant lighting for bright, open kitchens.','teresa','really GREAT work done on my kitchen LOVED IT!!','Teresa Martinez'),
('tile','Tile & floors','g20','Large-format porcelain, patterned feature walls, shower niches and floors laid straight and level.','tammy','from whole house renovations to small tile jobs and I am always pleased with the results.','tammy patton'),
('cab','Cabinetry & vanities','g22','Floating wood vanities, painted shaker cabinets, backlit mirrors and built-ins.','tracy','They do excellent work and aim to always make the customer happy.','Tracy Thomas'),
('fire','Fireplace walls','g15','Stacked-stone fireplace surrounds with lit floating shelves and built-in cabinets.','sadaf','Danny and his team renovated my master bath, kitchen and fireplace. Excellent work !','Sadaf Khan')]
def room_sel():
    tabs=''.join(f'<button role="tab" type="button" id="rt-{k}" aria-controls="rp-{k}" aria-selected="{"true" if i==0 else "false"}" tabindex="{0 if i==0 else -1}"><b>0{i+1}</b><span>{t}</span></button>' for i,(k,t,*_) in enumerate(ROOMS))
    panes=''.join(f'''<div class="rs-pane{" on" if i==0 else ""}" role="tabpanel" id="rp-{k}" aria-labelledby="rt-{k}"{"" if i==0 else " hidden"}>
<div class="rs-img">{pic(img,sizes="(max-width:900px) 100vw, 46vw")}</div>
<div class="rs-tx"><h3>{t}</h3><p>{d}</p><blockquote>“{e(q)}”<cite>— {e(who)}, Google review</cite></blockquote><a class="lnk" href="services.html#{k}">More on {t.lower()} {IC["arrow"]}</a></div></div>''' for i,(k,t,img,d,rk,q,who) in enumerate(ROOMS))
    return f'<div class="rs"><div class="rs-tabs" role="tablist" aria-label="Pick a room">{tabs}<span class="rs-ind" aria-hidden="true"></span></div><div class="rs-panes">{panes}</div></div>'

home_slides=''.join(f'<div class="rcar-s">{rcard(k)}</div>' for k in ['jill','tracy','tammy','sadaf','deanne','traci','nitza','brenda'])
HOME=f'''<section class="hero"><div class="hero-g wrap">
<div class="hero-c"><p class="kicker">{TXSTAR} Remodeler · Fort Worth, Texas</p>
<h1 class="split hero-h">Remodels worth <em>coming home&nbsp;to.</em></h1>
<p class="lead">L&amp;D Danny’s New Building and Renovations remodels bathrooms, kitchens, tile, cabinetry and whole homes across Fort Worth. Danny and his crew keep the job neat and finish it the way you pictured it.</p>
<div class="ctas">{btn_call("brass xl")}<a class="btn ghost-l mag" href="work.html">{IC["grid"]}<span>See our work</span></a></div>
<div class="chips"><a class="chip" href="reviews.html">{stars(RATING)}<b>5.0</b><span>{COUNT} Google reviews · all five-star</span></a><span class="chip ob" data-status><i></i><span>Hours</span></span></div></div>
<div class="hero-v"><div class="arch-bk" aria-hidden="true"></div><div class="arch">{pic("g08",sizes="(max-width:900px) 92vw, 40vw",eager=True,cls="kb")}</div>
<figure class="polar">{pic("g03",sizes="240px",eager=True)}<figcaption>Brass-trimmed glass shower</figcaption></figure>
<div class="seal" aria-hidden="true"><svg viewBox="0 0 200 200"><defs><path id="sc" d="M100 100 m-74 0 a74 74 0 1 1 148 0 a74 74 0 1 1 -148 0"/></defs><text><textPath href="#sc">NEW BUILDING · RENOVATIONS · FORT WORTH TX ·</textPath></text></svg>{TXSTAR}</div></div>
</div><div class="outline-x hero-o" aria-hidden="true">RENOVATIONS</div></section>
{marquee()}
<section class="sec stone" id="rooms"><div class="wrap"><div class="shead" data-r><div><p class="kicker">Pick a room</p><h2 class="split">Every room in the house, <em>start to finish</em></h2></div><p>Tap through the kinds of work Danny’s crew shows off most. Every photo here comes from their own Google profile.</p></div>
{room_sel()}</div></section>
<section class="sec slate why"><div class="wrap why-g"><div class="why-v" data-r><div class="frame">{pic("g10",sizes="(max-width:900px) 100vw, 42vw")}</div><p class="cap">On the job: large-format tile going up around a glass block window.</p></div>
<div class="why-c"><p class="kicker lt">Why homeowners call back</p><h2 class="split">What clients say, <em>again and again</em></h2>
<div class="why-l stagger">
<div class="wi">{IC["broom"]}<div><h3>A tidy job site</h3><p>“During the demo, which is usually the messiest part, his crews left each night with it being neater than it was before the demo.” <span>— Deanne B.</span></p></div></div>
<div class="wi">{IC["idea"]}<div><h3>Ideas when you need them</h3><p>“Daniel has great ideas if you need suggestions and his crew is always friendly and professional.” <span>— tammy p.</span></p></div></div>
<div class="wi">{IC["hand"]}<div><h3>Finished the way you wanted</h3><p>“They went above and beyond my expectations and made sure everything was exactly what we wanted.” <span>— Jill A.</span></p></div></div>
<div class="wi">{IC["repeat"]}<div><h3>Clients who come back</h3><p>“I have worked with them for the past five years on many projects.” <span>— Tracy T.</span></p></div></div>
</div></div></div></section>
<section class="stats ink"><div class="wrap stats-g stagger">
<div class="st"><div class="num" data-count="5.0" data-dec="1"><b>5.0</b></div><p>Google star rating</p></div>
<div class="st"><div class="num" data-count="13" data-dec="0"><b>13</b></div><p>Google reviews</p></div>
<div class="st"><div class="num" data-count="13" data-dec="0" data-pre="" data-suf=" of 13"><b>13</b><small> of 13</small></div><p>reviews are five stars</p></div>
<div class="st"><div class="num" data-count="5" data-dec="0"><b>5</b></div><p>bathrooms remodeled in one client’s home</p></div>
</div></section>
<section class="sec stone revband"><div class="q-big" aria-hidden="true">“</div><div class="wrap"><div class="shead" data-r><div><p class="kicker">Google reviews</p><h2 class="split">Fort Worth homeowners, <em>in their words</em></h2></div><p>{stars(RATING)} <b>5.0</b> from {COUNT} Google reviews. Quoted word for word.</p></div>
<div class="rcar" aria-roledescription="carousel" aria-label="Customer reviews"><div class="rcar-vp"><div class="rcar-track">{home_slides}</div></div>
<div class="rctl"><button class="ar pv" type="button" aria-label="Previous review">{IC["left"]}</button><button class="ar nx" type="button" aria-label="Next review">{IC["right"]}</button><div class="rdots"></div><a class="btn ghost-d" href="reviews.html"><span>All reviews</span>{IC["arrow"]}</a></div></div></div></section>
<section class="sec stone2 tsec"><div class="wrap"><div class="teasers stagger">
<a class="tcard tilt" href="services.html">{pic("g19",sizes="(max-width:900px) 100vw, 33vw")}<div class="tx"><span>Services</span><h3>What we build</h3></div></a>
<a class="tcard tilt" href="work.html">{pic("g09",sizes="(max-width:900px) 100vw, 33vw")}<div class="tx"><span>Our work</span><h3>Project gallery</h3></div></a>
<a class="tcard tilt" href="contact.html">{pic("g12",sizes="(max-width:900px) 100vw, 33vw")}<div class="tx"><span>Contact</span><h3>Hours &amp; directions</h3></div></a></div></div></section>
{cta_band("Ready to start your <em>remodel?</em>","Call the shop and tell Danny’s team about your project. Open Monday to Friday 8 to 5 and Saturday 9 to 4.","g14")}'''

# ================= SERVICES =================
SV=[('bath','Bathroom remodels','Master baths, guest baths and everything in them','g17','g03',
 ['Full master bath renovations','Freestanding tubs and walk-in showers','Glass shower enclosures and hardware','Large-format wall and floor tile','Vanities, mirrors and lighting'],
 'Bathrooms are the work clients mention most. One family had all five of their bathrooms remodeled, master bath included, along with their laundry room and office.','kathryn'),
('kitchen','Kitchen remodels','Islands, cabinets, counters and light','g18','g19',
 ['Kitchen islands with seating','Painted and stained cabinetry','Stone countertops','Pendant and under-cabinet lighting','Tile floors and backsplashes'],
 'From a new island to a full kitchen redo, the photos show bright, clean kitchens with room to gather.','teresa'),
('tile','Tile work','Walls, floors and showers, set straight','g07','g20',
 ['Large-format porcelain floors','Marble-look shower walls','Patterned feature walls','Mosaic shower floors and niches','Small tile repairs and updates'],
 'Tile shows up in almost every project, from marble-look floors that run through a hallway to a diamond-pattern feature wall.','tammy'),
('cab','Cabinetry & vanities','Built-ins that fit the room','g04','g06',
 ['Floating wood vanities','Painted shaker vanities','Wet-bar and utility cabinets','Floating shelves','Backlit and framed mirrors'],
 'Vanities and cabinets in warm wood, soft gray and deep slate blue, built to fit the space they’re in.','tracy'),
('fire','Fireplaces & feature walls','The wall everyone looks at','g15',None,
 ['Stacked-stone fireplace surrounds','Lit floating shelves beside the fireplace','Built-in cabinets below','Wall-mounted TV set into stone'],
 'A tall stone fireplace wall can anchor a whole living room. One client had Danny’s team renovate her fireplace along with her master bath and kitchen.','sadaf'),
('whole','Whole-home remodels','Room after room, one crew','g14','g23',
 ['Whole-house renovations','Wood floors and trim','Dining rooms and bedrooms','Laundry rooms and home offices','Repairs and home improvement'],
 'Several clients hired the crew for whole-home remodels, and some have kept them on project after project.','jill')]
def svsec(i,k,t,sub,a,b,items,blurb,rk):
    li=''.join(f'<li>{IC["hand"]}<span>{e(x)}</span></li>' for x in items)
    second=f'<div class="sv-b frame">{pic(b,sizes="(max-width:900px) 60vw, 22vw")}</div>' if b else ''
    return f'''<section class="sv {'alt' if i%2 else ''}" id="{k}"><div class="wrap sv-g">
<div class="sv-v" data-r><div class="sv-a frame">{pic(a,sizes="(max-width:900px) 100vw, 40vw")}</div>{second}<span class="sv-n" aria-hidden="true">0{i+1}</span></div>
<div class="sv-c"><p class="kicker">{e(sub)}</p><h2 class="split">{e(t)}</h2><p>{e(blurb)}</p><ul class="ticks">{li}</ul>
<blockquote class="sv-q">“{rtext(rk)}”<cite>— {e(RD[rk][1])}, Google review</cite></blockquote></div></div></section>'''
STEPS=[('Call the shop','Ring (817) 271-9465 and tell the team what you have in mind, big or small.'),
('Talk through ideas','Clients say Danny and his crew “give great input on renovation ideas,” so bring the questions too.'),
('Demo, kept tidy','The messy part, handled with care. One client said the crew “left each night with it being neater than it was before the demo.”'),
('Tile, cabinets & finishes','Walls, floors, vanities, fixtures and lighting go in. The real work shows in every photo here.'),
('Exactly what you wanted','“They went above and beyond my expectations and made sure everything was exactly what we wanted.”')]
steps=''.join(f'<li class="tl-s"><span class="tl-d">{i+1}</span><div><h3>{e(a)}</h3><p>{e(b)}</p></div></li>' for i,(a,b) in enumerate(STEPS))
SERV=phero('Services · Fort Worth, TX','Baths, kitchens, tile <em>&amp; whole homes</em>','Every service below comes straight from the jobs in their photos and the projects clients describe in their Google reviews.','g25','Services','50% 60%')+\
f'''<nav class="jump wrap" aria-label="Services on this page">{''.join(f'<a href="#{s[0]}">{e(s[1])}</a>' for s in SV)}</nav>'''+\
''.join(svsec(i,*s) for i,s in enumerate(SV))+\
f'''<section class="sec slate tl-sec"><div class="wrap tl-g"><div><p class="kicker lt">How a remodel goes</p><h2 class="split">From first call to <em>final walk-through</em></h2>
<div class="frame tl-ph" data-r>{pic("g10",sizes="(max-width:900px) 100vw, 36vw")}</div></div><ol class="tl">{steps}<span class="tl-line" aria-hidden="true"><i></i></span></ol></div></section>'''+\
cta_band("Tell us about <em>your project</em>","Bathroom, kitchen, tile or the whole house: call the shop to talk it through.","g11")

# ================= WORK =================
GAL=[('g08','bath'),('g03','bath'),('g25','bath'),('g17','bath'),('g09','bath'),('g05','bath'),('g11','kitchen'),('g18','kitchen'),('g19','kitchen'),('g01','kitchen'),('g24','kitchen'),
('g07','tile'),('g20','tile'),('g12','tile'),('g22','cab'),('g06','cab'),('g04','cab'),('g14','living'),('g23','living'),('g10','job')]
CATS=[('all','All'),('bath','Baths'),('kitchen','Kitchens'),('tile','Tile & floors'),('cab','Cabinetry'),('living','Living spaces'),('job','On the job')]
gal=''.join(f'<li class="gi" data-cat="{c}"><button type="button" class="gb" aria-label="Open photo: {e(PH[n])}">{pic(n,sizes="(max-width:600px) 50vw, (max-width:1100px) 33vw, 25vw")}</button></li>' for n,c in GAL)
filt=''.join(f'<button type="button" class="fb{" on" if k=="all" else ""}" data-f="{k}" aria-pressed="{"true" if k=="all" else "false"}">{t}</button>' for k,t in CATS)
HS=[(0.46,0.52,0.60,'Stacked-stone fireplace surround','Natural stone runs from the hearth to the ceiling.'),
(0.14,0.67,0.70,'Lit floating shelves','Shelves with lighting set into the wall beside the stone.'),
(0.16,0.91,0.92,'Built-in cabinets','Dark lower cabinets under the shelves on both sides.'),
(0.80,0.17,0.18,'Exposed ceiling beam','A dark beam across the tall vaulted ceiling.'),
(0.56,0.57,0.56,'TV set into the stone','The TV mounts flush in the fireplace wall.')]
hs=''.join(f'<button type="button" class="hs" style="--x:{x*100:.1f}%;--y:{y*100:.1f}%;--ym:{ym*100:.1f}%" aria-label="{e(t)}"><span class="hs-d" aria-hidden="true"></span><span class="hs-l"><b>{e(t)}</b>{e(d)}</span></button>' for x,y,ym,t,d in HS)
WORK=f'''<section class="phero wk"><div class="wrap wk-g"><div class="wk-c"><nav class="bc" aria-label="Breadcrumb"><a href="index.html">Home</a><span aria-hidden="true">/</span><span aria-current="page">Our Work</span></nav>
<p class="kicker lt">Our work · real L&amp;D Danny’s projects</p><h1 class="split">From the plan <em>to the finish</em></h1><p class="lead">Drag the handle across this bathroom. The drawing is traced from the very same photo, so you can see how a room’s lines turn into tile, cabinetry and light.</p>
<div class="ctas">{btn_call("brass")}<a class="btn ghost-l mag" href="#gallery">{IC["grid"]}<span>Jump to gallery</span></a></div></div>
<div class="cmp" data-r style="--p:52%"><div class="cmp-a">{pic("g16",sizes="(max-width:900px) 100vw, 54vw",eager=True)}</div><div class="cmp-b">{pic("bp16",sizes="(max-width:900px) 100vw, 54vw",eager=True)}</div>
<span class="cmp-tag l">Line drawing</span><span class="cmp-tag r">Finished room</span>
<div class="cmp-h" aria-hidden="true"><span>{IC["left"]}{IC["right"]}</span></div><input class="cmp-r" type="range" min="0" max="100" value="52" aria-label="Compare the line drawing with the finished bathroom"></div></div></section>
<section class="sec stone fp"><div class="wrap fp-g"><div class="fp-c"><p class="kicker">Feature wall close-up</p><h2 class="split">A fireplace wall, <em>piece by piece</em></h2><p>Tap the brass pins to see what went into this two-story living room.</p>
<ol class="fp-l">{''.join(f"<li><b>{e(t)}</b> {e(d)}</li>" for _,_,_,t,d in HS)}</ol></div>
<div class="hsw" data-r><div class="hs-f">{pic("g15",sizes="(max-width:900px) 100vw, 44vw")}{hs}</div></div></div></section>
<section class="sec stone2" id="gallery"><div class="wrap"><div class="shead" data-r><div><p class="kicker">Project gallery</p><h2 class="split">Twenty photos <em>from their profile</em></h2></div><p>Filter by room and tap any photo to view it large. Use the arrow keys or swipe to move through.</p></div>
<div class="filt" role="group" aria-label="Filter photos">{filt}</div><ul class="gal" role="list">{gal}</ul></div></section>
{cta_band("Like what you see? <em>Let’s talk.</em>","Call the shop to put your project on the schedule.")}'''

# ================= REVIEWS =================
CHIPS=[('Master bath renovation',3),('Whole home remodel',3),('Top-notch work',3),('Bathroom remodeling',3),('Tile work replacement',2),('Kitchen remodeling',2)]
chips=''.join(f'<li><span>{e(t)}</span><b>{n}</b></li>' for t,n in CHIPS)
bars=''.join(f'<div class="bar"><span>{s}★</span><i><b style="--w:{100 if s==5 else 0}%"></b></i><em>{13 if s==5 else 0}</em></div>' for s in (5,4,3,2,1))
allrev=''.join(rcard(r[0],'rv-card m') for r in REV)
REVP=phero('Reviews · Google','Five stars, <em>thirteen times over</em>','Every Google review for L&amp;D Danny’s is five stars. Here they are, quoted word for word, with the dates shown on Google.','g05','Reviews','50% 45%')+\
f'''<section class="sec stone"><div class="wrap rsum"><div class="rsum-s" data-r><div class="big" data-count="5.0" data-dec="1"><b>5.0</b></div>{stars(RATING,'lg')}<p>{COUNT} Google reviews</p>
<a class="btn ghost-d" href="{GREV}" target="_blank" rel="noopener"><span>Read them on Google</span>{IC["arrow"]}</a></div>
<div class="rsum-b" data-r>{bars}<p class="note">Google shows all {COUNT} reviews as five stars.</p></div>
<div class="rsum-c" data-r><h2 class="h3">What reviewers mention most</h2><ul class="topics">{chips}</ul><p class="note">Topic counts as shown on Google.</p></div></div></section>
<section class="sec stone2"><div class="wrap"><div class="shead" data-r><div><p class="kicker">Word for word</p><h2 class="split">Ten of the <em>thirteen reviews</em></h2></div><p>Three were shortened by Google, shown with “…” exactly as they appear. Spelling is left as written.</p></div>
<div class="masonry">{allrev}</div>
<div class="rv-side" data-r><div class="frame">{pic("g09",sizes="(max-width:900px) 100vw, 30vw")}</div><p>“Danny did the complete remodel of my bathroom, he is professional and serious, I highly recommend him.” <span>— Nitza Rangel</span></p></div></div></section>
{cta_band("Join the <em>five-star list</em>","Call L&amp;D Danny’s to talk about your bathroom, kitchen, tile or whole-home remodel.")}'''

# ================= CONTACT =================
FAQ=[('Where is L&D Danny’s located?',f'The shop is at {ADDR}. Use the map on this page or tap “Get directions.”'),
('What are your hours?','Monday to Friday 8 AM to 5 PM, Saturday 9 AM to 4 PM, closed Sunday. Thanksgiving and Black Friday hours might differ, so please call ahead.'),
('What kind of work do you do?','Their photos and reviews show bathroom remodels (including master baths), kitchen remodels, tile work, cabinetry and vanities, fireplace and feature walls, and whole-home remodels. Clients also mention small tile jobs and home repairs.'),
('Do you handle small jobs as well as big remodels?','One longtime client wrote that she has used them “from whole house renovations to small tile jobs.” Call to talk through your project.'),
('How do I get started?',f'Call {PHONE} during business hours, or fill in the form on this page to send the team a text with your project details.'),
('Is the shop wheelchair accessible?','Google lists a wheelchair-accessible entrance and a wheelchair-accessible parking lot.')]
faq_ld={"@context":"https://schema.org","@type":"FAQPage","mainEntity":[{"@type":"Question","name":q,"acceptedAnswer":{"@type":"Answer","text":a}} for q,a in FAQ]}
faq=''.join(f'<details class="fq"{" open" if i==0 else ""}><summary><span>{e(q)}</span><i aria-hidden="true"></i></summary><p>{e(a)}</p></details>' for i,(q,a) in enumerate(FAQ))
opts=''.join(f'<option>{t}</option>' for t in ['Bathroom remodel','Kitchen remodel','Tile work','Cabinetry or vanity','Fireplace or feature wall','Whole-home remodel','Repair or small job','Something else'])
CONT=phero('Contact · Fort Worth, TX','Let’s talk about <em>your remodel</em>',f'Call {PHONE}, send a text from the form below, or stop by {ADDR1} during business hours.','g12','Contact','50% 55%')+\
f'''<section class="sec stone"><div class="wrap ct-g">
<div class="ct-card" data-r><p class="kicker">Call the shop</p><a class="bigtel" href="{TEL}">{PHONE}</a><div class="ob big" data-status><i></i><span>Hours</span></div>{hours_tbl()}
<address><b>{e(NAME)}</b><br>{ADDR}</address><div class="ctas">{btn_call("brass")}<a class="btn ghost-d" href="{DIR}" target="_blank" rel="noopener">{IC["pin"]}<span>Get directions</span></a></div></div>
<form class="qf" data-r novalidate><p class="kicker">Text us your project</p><h2 class="h3">Tell the team what you have in mind</h2>
<p class="note">This opens a text message to {PHONE} on your phone with your details filled in. Nothing is sent until you hit send. On a computer, just call instead.</p>
<div class="fr"><label for="qn">Your name</label><input id="qn" name="n" autocomplete="name" required></div>
<div class="fr2"><div class="fr"><label for="qp">Callback number</label><input id="qp" name="p" type="tel" autocomplete="tel"></div>
<div class="fr"><label for="qt">Project</label><select id="qt" name="t">{opts}</select></div></div>
<div class="fr"><label for="qm">Details</label><textarea id="qm" name="m" rows="4" placeholder="Which room, roughly what you want done, and the best time to reach you"></textarea></div>
<p class="qf-err" role="alert" hidden>Please add your name so the team knows who’s texting.</p>
<div class="ctas"><button class="btn brass mag" type="submit">{IC["chat"]}<span>Open text message</span></button>{btn_call("ghost-d","Or call")}</div></form></div></section>
<section class="sec stone2"><div class="wrap ct-g2"><div class="map frame" data-r><iframe title="Map to {e(NAME)}" src="{MAPEMBED}" loading="lazy" referrerpolicy="no-referrer-when-downgrade"></iframe></div>
<div class="faq"><p class="kicker">Questions</p><h2 class="split">Good to <em>know</em></h2>{faq}</div></div></section>'''

NF=f'''<section class="phero nf"><div class="wrap nf-c"><div class="nf-e" aria-hidden="true">{(GEN/"assets/brand/emblem-dark.svg").read_text()}</div><p class="kicker lt">Error 404</p><h1>This room <em>isn’t built yet.</em></h1><p class="lead">The page you’re looking for doesn’t exist. Head back home or give the shop a call.</p>
<div class="ctas c"><a class="btn brass mag" href="/{REPO}/index.html"><span>Back to home</span>{IC["arrow"]}</a>{btn_call("ghost-l")}</div></div></section>'''

PAGES=[('index.html',f'L&D Danny’s New Building and Renovations | Remodeler in Fort Worth, TX','Bathroom, kitchen, tile, cabinetry and whole-home remodels in Fort Worth, TX. 5.0 stars from 13 Google reviews. Call (817) 271-9465.',HOME,dict(home=True,crumb='Home')),
('services.html','Remodeling Services in Fort Worth | L&D Danny’s','Bathroom and master bath remodels, kitchen remodels, tile work, cabinetry and vanities, fireplace walls and whole-home remodels in Fort Worth, TX.',SERV,dict(crumb='Services')),
('work.html','Our Work: Remodel Photo Gallery | L&D Danny’s, Fort Worth','Real bathroom, kitchen, tile, cabinetry and fireplace projects by L&D Danny’s New Building and Renovations in Fort Worth, TX.',WORK,dict(crumb='Our Work')),
('reviews.html','Reviews: 5.0 Stars on Google | L&D Danny’s, Fort Worth','All 13 Google reviews for L&D Danny’s New Building and Renovations are five stars. Read them word for word.',REVP,dict(full_reviews=True,crumb='Reviews')),
('contact.html','Contact & Hours | L&D Danny’s, 5607 Humbert Ave, Fort Worth','Call (817) 271-9465 or visit 5607 Humbert Ave, Fort Worth, TX 76107. Open Mon–Fri 8–5, Sat 9–4. Hours, map, FAQ and a text-us form.',CONT,dict(crumb='Contact',extra_ld=[faq_ld]))]
for fn,t,d,b,kw in PAGES: (OUT/fn).write_text(page(fn,t,d,b,**kw))
nf=page('404.html','Page not found | L&D Danny’s','This page could not be found.',NF,crumb='Not found')
nf=nf.replace('<head><meta charset="utf-8">',f'<head><meta charset="utf-8"><base href="/{REPO}/"><meta name="robots" content="noindex">',1)
(OUT/'404.html').write_text(nf)
(OUT/'robots.txt').write_text(f'User-agent: *\nAllow: /\nSitemap: {BASE}sitemap.xml\n')
(OUT/'sitemap.xml').write_text('<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">'+''.join(f'<url><loc>{BASE}{"" if p[0]=="index.html" else p[0]}</loc><lastmod>2026-11-25</lastmod></url>' for p in PAGES)+'</urlset>\n')
(OUT/'llms.txt').write_text(f'''# {NAME}

> Remodeler in Fort Worth, Texas: bathroom and master bath remodels, kitchen remodels, tile work, cabinetry and vanities, fireplace and feature walls, and whole-home remodels. Rated 5.0 stars from {COUNT} Google reviews (all five-star).

- Name on Google: {GNAME}
- Category: Remodeler
- Address: {ADDR}
- Phone: {PHONE}
- Hours: Monday–Friday 8 AM–5 PM; Saturday 9 AM–4 PM; Sunday closed. Thanksgiving and Black Friday hours might differ.
- Accessibility: wheelchair-accessible entrance and parking lot
- Google Maps: {GMAPS}
- Services are drawn from the business's own Google photos and its customer reviews. Clients mention Danny (also Daniel) and his crew, tidy job sites, renovation ideas, and repeat work over several years.

## Pages
- [Home]({BASE}): overview, room-by-room work, reviews
- [Services]({BASE}services.html): each service in detail and how a remodel goes
- [Our Work]({BASE}work.html): photo gallery of real projects
- [Reviews]({BASE}reviews.html): all quoted Google reviews, word for word
- [Contact]({BASE}contact.html): phone, hours, map, FAQ and a text-us form
''')
(OUT/'.nojekyll').write_text('')
(OUT/'README.md').write_text(f'# {NAME} — demo website\n\nDesign preview by RGWebD. Live: {BASE}\n\nStatic site generated by `generator/build.py` (photos: `generator/process.py`, logo: `generator/logo.py`).\n')
print('built',[p[0] for p in PAGES])
