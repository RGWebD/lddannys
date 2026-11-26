import asyncio,sys,json,io,functools,threading,http.server,socketserver
from playwright.async_api import async_playwright
from PIL import Image
import imagehash
BASEURL=sys.argv[1] if len(sys.argv)>1 else None
if not BASEURL:
    class Q(http.server.SimpleHTTPRequestHandler):
        def log_message(self,*a):pass
    socketserver.TCPServer.allow_reuse_address=True
    srv=socketserver.ThreadingTCPServer(('127.0.0.1',8962),functools.partial(Q,directory='/workspace/lddannys/site')); threading.Thread(target=srv.serve_forever,daemon=True).start()
    BASEURL='http://127.0.0.1:8962/'
PAGES=['index','services','work','reviews','contact','404']
fails=[]
def F(m): fails.append(m); print('FAIL',m,flush=True)
async def main():
    async with async_playwright() as p:
        b=await p.chromium.launch(executable_path='/usr/bin/google-chrome')
        for w,h in [(1440,900),(390,844)]:
            for rm in ['no-preference','reduce']:
                ctx=await b.new_context(viewport={'width':w,'height':h},reduced_motion=rm)
                pg=await ctx.new_page(); errs=[]
                pg.on('console',lambda m: errs.append(m.text) if m.type=='error' else None)
                pg.on('pageerror',lambda e: errs.append(str(e)))
                for n in PAGES:
                    errs.clear()
                    if n=='404' and BASEURL.startswith('http://127'): continue
                    url=BASEURL+(n+'.html' if n!='404' else 'nope-404-test')
                    r=await pg.goto(url,wait_until='domcontentloaded' if n=='contact' else 'load',timeout=60000)
                    if n!='404' and r.status!=200: F(f'{n} status {r.status}')
                    await pg.wait_for_timeout(3600 if n=='index' else 400)
                    H=await pg.evaluate('document.body.scrollHeight')
                    for y in range(0,H+900,450): await pg.evaluate(f'scrollTo(0,{y})'); await pg.wait_for_timeout(60)
                    await pg.wait_for_timeout(2400)
                    res=await pg.evaluate('''()=>{
                      const W=document.documentElement.clientWidth,sw=document.documentElement.scrollWidth;
                      const wide=[...document.querySelectorAll('body *')].filter(e=>{const r=e.getBoundingClientRect();return r.right>W+1&&getComputedStyle(e).position!=='fixed'&&!e.closest('.marq,.rcar-track,.outline-x,.cta-bg,.mnav,.rs-tabs,.ldr')}).slice(0,5).map(e=>e.tagName+'.'+e.className+' '+Math.round(e.getBoundingClientRect().right));
                      const broken=[...document.images].filter(i=>i.getAttribute('src')&&i.complete&&i.naturalWidth===0).map(i=>i.getAttribute('src'));
                      const hidden=[...document.querySelectorAll('[data-r],.stagger>*')].filter(e=>parseFloat(getComputedStyle(e).opacity)<0.99).length;
                      const counters=[...document.querySelectorAll('[data-count]')].map(e=>[e.dataset.count,(e.querySelector('b')||e).textContent]);
                      const ld=[...document.querySelectorAll('script[type="application/ld+json"]')].map(s=>s.textContent);
                      const imgs=[...document.images].filter(i=>!i.closest('.tlb')&&!i.closest('.ldr')&&i.getAttribute('src')).map(i=>i.getAttribute('src').split('/').pop().split('-')[0]);
                      const h1=document.querySelectorAll('h1').length;
                      const ring=[...document.querySelectorAll('body *')].filter(e=>{const s=getComputedStyle(e);return s.position==='fixed'&&s.pointerEvents==='none'&&s.borderRadius.includes('50%')}).length;
                      const status=(document.querySelector('[data-status]')||{}).textContent;
                      return {W,sw,wide,broken,hidden,counters,ld,imgs,h1,ring,status,title:document.title}}''')
                    tag=f'{n}@{w}/{rm}'
                    if res['sw']>res['W']: F(f'{tag} overflow {res["sw"]}>{res["W"]} {res["wide"]}')
                    if res['broken']: F(f'{tag} broken {res["broken"]}')
                    if res['hidden']: F(f'{tag} hidden after scroll {res["hidden"]}')
                    for want,got in res['counters']:
                        if abs(float(want)-float(got))>1e-9: F(f'{tag} counter {want}!={got}')
                    if res['h1']!=1: F(f'{tag} h1 count {res["h1"]}')
                    if res['ring']: F(f'{tag} possible cursor ring')
                    e2=[x for x in errs if 'google' not in x.lower() and 'maps' not in x.lower()]
                    if e2: F(f'{tag} console {e2[:3]}')
                    for s in res['ld']:
                        try: json.loads(s)
                        except Exception as ex: F(f'{tag} bad json-ld {ex}')
                    dup=[x for x in set(res['imgs']) if res['imgs'].count(x)>1 and x not in ('logo',)]
                    if dup: F(f'{tag} duplicate photos {dup}')
                    if w==390 and rm=='no-preference':
                        bgb=await pg.query_selector('.burger')
                        await pg.evaluate('scrollTo(0,0)'); await bgb.click(); await pg.wait_for_timeout(600)
                        vis=await pg.evaluate("getComputedStyle(document.querySelector('.mnav')).visibility")
                        if vis!='visible': F(f'{tag} mobile menu not opening')
                        await bgb.click(); await pg.wait_for_timeout(500)
                    if w==1440 and rm=='no-preference': print(n,'ok',len(res['imgs']),'imgs |',res['status'],'|',res['title'][:70],flush=True)
                await ctx.close()
        await b.close()
asyncio.run(main())
print('FAILS',len(fails))
