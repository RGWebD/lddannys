(()=>{
const d=document,root=d.documentElement,RM=matchMedia('(prefers-reduced-motion: reduce)').matches;
root.classList.add('js');
const $=(s,c=d)=>c.querySelector(s),$$=(s,c=d)=>[...c.querySelectorAll(s)];
/* loader (home, once per session) */
const ldr=$('.ldr');
if(ldr){ if(RM||sessionStorage.getItem('ldd-seen')){ldr.classList.add('gone')} else {sessionStorage.setItem('ldd-seen','1');setTimeout(()=>ldr.classList.add('go'),1150);setTimeout(()=>ldr.classList.add('gone'),2300)} }
/* split headings into words */
$$('.split').forEach(h=>{let i=0;const walk=n=>{[...n.childNodes].forEach(c=>{if(c.nodeType===3){const parts=c.textContent.split(/(\s+)/);const f=d.createDocumentFragment();parts.forEach(p=>{if(!p)return;if(/^\s+$/.test(p)){f.append(' ');return}const w=d.createElement('span');w.className='w';const s=d.createElement('span');s.style.setProperty('--i',i++);s.textContent=p;w.append(s);f.append(w)});c.replaceWith(f)}else if(c.nodeType===1&&!c.classList.contains('w'))walk(c)})};walk(h);h.setAttribute('aria-label',h.textContent.replace(/\s+/g,' ').trim())});
/* reveal */
const io=new IntersectionObserver(es=>es.forEach(en=>{if(en.isIntersecting){en.target.classList.add('in');io.unobserve(en.target)}}),{rootMargin:'0px 0px -8% 0px',threshold:.08});
$$('[data-r],.stagger,.split').forEach(el=>RM?el.classList.add('in'):io.observe(el));
/* header + level + mbar */
const hdr=$('.hdr'),lvl=$('.lvl'),mbar=$('.mbar');
const onS=()=>{const y=scrollY,h=root.scrollHeight-innerHeight;hdr.classList.toggle('sc',y>30);lvl.style.setProperty('--p',h>0?Math.min(1,y/h):0);if(mbar)mbar.classList.toggle('show',y>innerHeight*.55);tlUpd()};
/* timeline */
const tl=$('.tl');function tlUpd(){if(!tl)return;const r=tl.getBoundingClientRect(),vh=innerHeight;const p=Math.max(0,Math.min(1,(vh*.7-r.top)/r.height));tl.querySelector('.tl-line').style.setProperty('--tp',RM?1:p);$$('.tl-s',tl).forEach(s=>{if(RM||s.getBoundingClientRect().top<vh*.72)s.classList.add('lit')})}
addEventListener('scroll',onS,{passive:true});addEventListener('resize',onS);onS();
/* mobile menu */
const bg=$('.burger'),mn=$('#mnav');
if(bg){const set=o=>{bg.setAttribute('aria-expanded',o);mn.classList.toggle('open',o);d.body.style.overflow=o?'hidden':'';bg.setAttribute('aria-label',o?'Close menu':'Open menu')};
bg.addEventListener('click',()=>set(bg.getAttribute('aria-expanded')!=='true'));d.addEventListener('keydown',e=>{if(e.key==='Escape'&&mn.classList.contains('open')){set(false);bg.focus()}});$$('a',mn).forEach(a=>a.addEventListener('click',()=>set(false)))}
/* open / closed in Fort Worth time */
(()=>{const els=$$('[data-status]');if(!els.length)return;
const now=new Date(),parts=Object.fromEntries(new Intl.DateTimeFormat('en-US',{timeZone:'America/Chicago',weekday:'short',hour:'numeric',minute:'numeric',hour12:false,year:'numeric',month:'numeric',day:'numeric'}).formatToParts(now).map(p=>[p.type,p.value]));
const wd=['Sun','Mon','Tue','Wed','Thu','Fri','Sat'].indexOf(parts.weekday),hr=(+parts.hour%24)+(+parts.minute)/60,mo=+parts.month,dy=+parts.day,yr=+parts.year;
const H={0:null,1:[8,17],2:[8,17],3:[8,17],4:[8,17],5:[8,17],6:[9,16]};
// Thanksgiving = 4th Thursday of November; Black Friday the day after: Google says hours might differ
const first=new Date(Date.UTC(yr,10,1)).getUTCDay(),tg=1+((4-first+7)%7)+21;const hol=mo===11&&(dy===tg||dy===tg+1);
const fmt=h=>{const H12=h%12||12;return H12+(h<12?' AM':' PM')};
let cls,txt;
if(hol){cls='unk';txt='Holiday hours may vary · call'}
else{const t=H[wd];if(t&&hr>=t[0]&&hr<t[1]){cls='open';txt='Open now · until '+fmt(t[1])}
else{let n=wd,add=0;if(t&&hr<t[0]){}else{do{n=(n+1)%7;add++}while(!H[n])}const nt=H[n];cls='closed';txt='Closed · opens '+(add===0?'today':add===1?'tomorrow':['Sun','Mon','Tue','Wed','Thu','Fri','Sat'][n])+' '+fmt(nt[0])}}
els.forEach(el=>{el.classList.add(cls);el.querySelector('span').textContent=txt});
$$('.hours tr[data-d="'+wd+'"]').forEach(r=>r.classList.add('today'))})();
/* counters */
const cio=new IntersectionObserver(es=>es.forEach(en=>{if(!en.isIntersecting)return;cio.unobserve(en.target);const el=en.target,b=el.querySelector('b'),to=parseFloat(el.dataset.count),dec=+el.dataset.dec||0;
if(RM){b.textContent=to.toFixed(dec);return}const t0=performance.now(),D=1600;const f=t=>{const k=Math.min(1,(t-t0)/D),v=to*(1-Math.pow(1-k,3));b.textContent=(k<1?v:to).toFixed(dec);if(k<1)requestAnimationFrame(f)};b.textContent=(0).toFixed(dec);requestAnimationFrame(f)}),{threshold:.4});
$$('[data-count]').forEach(el=>cio.observe(el));
/* room selector */
$$('.rs').forEach(rs=>{const tabs=$$('[role=tab]',rs),ind=$('.rs-ind',rs);
const place=t=>{if(innerWidth>1100){ind.style.setProperty('--t',t.offsetTop+'px');ind.style.setProperty('--h',t.offsetHeight+'px')}else{ind.style.setProperty('--l',t.offsetLeft+'px');ind.style.setProperty('--wd',t.offsetWidth+'px')}};
const sel=(t,focus)=>{tabs.forEach(x=>{const on=x===t;x.setAttribute('aria-selected',on);x.tabIndex=on?0:-1;const p=d.getElementById(x.getAttribute('aria-controls'));p.hidden=!on;p.classList.toggle('on',on)});place(t);if(focus){t.focus();t.scrollIntoView({block:'nearest',inline:'nearest'})}};
tabs.forEach((t,i)=>{t.addEventListener('click',()=>sel(t));t.addEventListener('keydown',e=>{let j=null;if(e.key==='ArrowRight'||e.key==='ArrowDown')j=(i+1)%tabs.length;if(e.key==='ArrowLeft'||e.key==='ArrowUp')j=(i-1+tabs.length)%tabs.length;if(e.key==='Home')j=0;if(e.key==='End')j=tabs.length-1;if(j!==null){e.preventDefault();sel(tabs[j],true)}})});
const cur=()=>tabs.find(t=>t.getAttribute('aria-selected')==='true');addEventListener('resize',()=>place(cur()));addEventListener('load',()=>place(cur()));place(cur())});
/* reviews carousel */
$$('.rcar').forEach(c=>{const tr=$('.rcar-track',c),sl=$$('.rcar-s',c),dots=$('.rdots',c);let i=0,timer=null;
const per=()=>innerWidth<=900?1:3,max=()=>Math.max(0,sl.length-per());
const db=[];const mk=()=>{dots.innerHTML='';db.length=0;for(let k=0;k<=max();k++){const b=d.createElement('button');b.type='button';b.setAttribute('aria-label','Go to review '+(k+1));b.addEventListener('click',()=>go(k));dots.append(b);db.push(b)}};
const go=k=>{i=Math.max(0,Math.min(max(),k));tr.style.transform=`translateX(${-i*100/per()}%)`;db.forEach((b,j)=>b.setAttribute('aria-current',j===i));sl.forEach((s,j)=>{const vis=j>=i&&j<i+per();s.setAttribute('aria-hidden',!vis);$$('a,button',s).forEach(x=>x.tabIndex=vis?0:-1)})};
$('.pv',c).addEventListener('click',()=>go(i<=0?max():i-1));$('.nx',c).addEventListener('click',()=>go(i>=max()?0:i+1));
const play=()=>{if(RM)return;stop();timer=setInterval(()=>go(i>=max()?0:i+1),6500)},stop=()=>clearInterval(timer);
c.addEventListener('mouseenter',stop);c.addEventListener('mouseleave',play);c.addEventListener('focusin',stop);c.addEventListener('focusout',play);
let sx=null;c.addEventListener('touchstart',e=>{sx=e.touches[0].clientX;stop()},{passive:true});c.addEventListener('touchend',e=>{if(sx===null)return;const dx=e.changedTouches[0].clientX-sx;if(Math.abs(dx)>40)go(dx<0?i+1:i-1);sx=null;play()});
addEventListener('resize',()=>{mk();go(i)});mk();go(0);play()});
/* compare slider */
$$('.cmp').forEach(c=>{const r=$('.cmp-r',c);const set=v=>c.style.setProperty('--p',v+'%');r.addEventListener('input',()=>set(r.value));
if(!RM){let done=false;const o=new IntersectionObserver(es=>{if(es[0].isIntersecting&&!done){done=true;o.disconnect();let t0=performance.now();const f=t=>{const k=Math.min(1,(t-t0)/1800);const v=52+Math.sin(k*Math.PI*2)*28*(1-k);set(v);r.value=v;if(k<1)requestAnimationFrame(f);else{set(52);r.value=52}};requestAnimationFrame(f)}},{threshold:.5});o.observe(c)}});
/* hotspots */
const hss=$$('.hs');const fitHs=()=>hss.forEach(h=>{h.classList.remove('rev');const l=$('.hs-l',h),r=h.getBoundingClientRect();const w=l.offsetWidth||220;if(r.right+w+20>root.clientWidth)h.classList.add('rev')});
hss.forEach(h=>{h.addEventListener('click',()=>{const on=!h.classList.contains('on');hss.forEach(x=>x.classList.remove('on'));h.classList.toggle('on',on)})});
if(hss.length){addEventListener('resize',fitHs);addEventListener('load',fitHs);fitHs();d.addEventListener('click',e=>{if(!e.target.closest('.hs'))hss.forEach(x=>x.classList.remove('on'))})}
/* gallery filter */
$$('.filt').forEach(f=>{const items=$$('.gi');$$('.fb',f).forEach(b=>b.addEventListener('click',()=>{$$('.fb',f).forEach(x=>{x.classList.toggle('on',x===b);x.setAttribute('aria-pressed',x===b)});const k=b.dataset.f;items.forEach(it=>it.hidden=!(k==='all'||it.dataset.cat===k))}))});
/* lightbox */
const lb=$('.tlb');if(lb){const im=$('img',lb),cap=$('figcaption',lb);let list=[],idx=0,last=null;
const show=k=>{idx=(k+list.length)%list.length;const src=list[idx];im.src=src.currentSrc||src.src;im.alt=src.alt;cap.textContent=src.alt};
const open=(btn)=>{const scope=btn.closest('.gal');list=$$('.gi:not([hidden]) img',scope);last=btn;show(list.indexOf($('img',btn)));lb.hidden=false;d.body.style.overflow='hidden';$('.tlb-x',lb).focus()};
const close=()=>{lb.hidden=true;im.removeAttribute('src');d.body.style.overflow='';if(last)last.focus()};
$$('.gb').forEach(b=>b.addEventListener('click',()=>open(b)));
$('.tlb-x',lb).addEventListener('click',close);$('.tlb-p',lb).addEventListener('click',()=>show(idx-1));$('.tlb-n',lb).addEventListener('click',()=>show(idx+1));
lb.addEventListener('click',e=>{if(e.target===lb)close()});
d.addEventListener('keydown',e=>{if(lb.hidden)return;if(e.key==='Escape')close();if(e.key==='ArrowRight')show(idx+1);if(e.key==='ArrowLeft')show(idx-1);if(e.key==='Tab'){const f=$$('button',lb);const a=f.indexOf(d.activeElement);e.preventDefault();f[(a+(e.shiftKey?-1:1)+f.length)%f.length].focus()}});
let sx=null;lb.addEventListener('touchstart',e=>sx=e.touches[0].clientX,{passive:true});lb.addEventListener('touchend',e=>{if(sx===null)return;const dx=e.changedTouches[0].clientX-sx;if(Math.abs(dx)>40)show(dx<0?idx+1:idx-1);sx=null})}
/* sms form */
$$('.qf').forEach(f=>f.addEventListener('submit',e=>{e.preventDefault();const n=f.n.value.trim(),err=$('.qf-err',f);if(!n){err.hidden=false;f.n.focus();return}err.hidden=true;
const body=`Hi L&D Danny's, this is ${n}.`+(f.p.value.trim()?` Callback: ${f.p.value.trim()}.`:'')+` Project: ${f.t.value}.`+(f.m.value.trim()?` ${f.m.value.trim()}`:'');
location.href='sms:+18172719465?&body='+encodeURIComponent(body)}));
/* magnetic buttons + tilt (pointer:fine only, no cursor follower) */
if(!RM&&matchMedia('(pointer:fine)').matches){
$$('.mag').forEach(b=>{b.addEventListener('mousemove',e=>{const r=b.getBoundingClientRect();b.style.transform=`translate(${(e.clientX-r.left-r.width/2)*.18}px,${(e.clientY-r.top-r.height/2)*.28}px)`});b.addEventListener('mouseleave',()=>b.style.transform='')});
$$('.tilt').forEach(c=>{c.addEventListener('mousemove',e=>{const r=c.getBoundingClientRect(),x=(e.clientX-r.left)/r.width-.5,y=(e.clientY-r.top)/r.height-.5;c.style.transform=`perspective(900px) rotateY(${x*8}deg) rotateX(${-y*8}deg) translateY(-4px)`});c.addEventListener('mouseleave',()=>c.style.transform='')});
/* hero parallax */
const hv=$('.hero-v');if(hv){const pol=$('.polar',hv),seal=$('.seal',hv);addEventListener('scroll',()=>{const y=scrollY;if(y>innerHeight)return;pol.style.translate=`0 ${y*-.08}px`;seal.style.translate=`0 ${y*.12}px`},{passive:true})}}
/* demo pill */
const dm=$('.demo');if(dm){if(sessionStorage.getItem('ldd-demo'))dm.classList.add('gone');$('button',dm).addEventListener('click',()=>{dm.classList.add('gone');sessionStorage.setItem('ldd-demo','1')})}
})();
