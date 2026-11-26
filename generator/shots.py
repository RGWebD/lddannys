import asyncio,sys,functools,threading,http.server,socketserver
from playwright.async_api import async_playwright
tag=sys.argv[1]; pages=sys.argv[2].split(',') if len(sys.argv)>2 else ['index']
widths=[int(x) for x in sys.argv[3].split(',')] if len(sys.argv)>3 else [1440,390]
class Q(http.server.SimpleHTTPRequestHandler):
    def log_message(self,*a):pass
socketserver.TCPServer.allow_reuse_address=True
srv=socketserver.ThreadingTCPServer(('127.0.0.1',8961),functools.partial(Q,directory='/workspace/lddannys/site'));threading.Thread(target=srv.serve_forever,daemon=True).start()
async def main():
    async with async_playwright() as p:
        b=await p.chromium.launch(executable_path='/usr/bin/google-chrome')
        for w in widths:
            ctx=await b.new_context(viewport={'width':w,'height':900 if w>500 else 844},device_scale_factor=1)
            pg=await ctx.new_page()
            await pg.add_init_script("sessionStorage.setItem('ldd-seen','1')")
            for n in pages:
                await pg.goto(f'http://127.0.0.1:8961/{n}.html',wait_until='domcontentloaded'); await pg.wait_for_timeout(1800)
                await pg.screenshot(path=f'/workspace/lddannys-work/{tag}_{n}_{w}_top.png')
                H=await pg.evaluate('document.body.scrollHeight')
                for y in range(0,H,450): await pg.evaluate(f'scrollTo(0,{y})'); await pg.wait_for_timeout(80)
                await pg.wait_for_timeout(2200); await pg.evaluate('scrollTo(0,0)'); await pg.wait_for_timeout(500)
                await pg.screenshot(path=f'/workspace/lddannys-work/{tag}_{n}_{w}_full.png',full_page=True)
                print(n,w,H)
            await ctx.close()
        await b.close()
asyncio.run(main())
