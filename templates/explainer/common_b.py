"""Style B skeleton: light editorial "paper + primary blocks + realistic instruments".
build(dir, cfg) -> dir/reel_ar.html   (same render.js as style A)

cfg keys
  D            duration (s)
  chunks       [[(word,start),...], ...]  caption chunks (same as style A)
  PH           [[start, kicker, hero, sub, color], ...]
               hero markup: [[x]] = yellow highlight box, ~~x~~ = animated strike-through
  defs         extra SVG <defs> (optional)
  scene_svg    SVG for the stage (use SCALE()/WATCH()/CUP() helpers or your own)
  scene_js     must define function scene(t){...}
  init_js      optional
  cards        optional {'top':860,'items':[(label, t_in, color, inner_svg_or_text)]}
  choice       optional {'t':start, 'opts':[(label,color,inner_svg_or_text),(...)]}
  LB           optional leader labels, same format as style A
Optional handle/watermark top-right: set cfg['handle'] (empty = none).
"""
import json, os

CSS = r"""
:root{--paper:#f2eee7;--ink:#1d1a17;--mute:#8b847b;--red:#c8102e;--blue:#1f4e9a;--yel:#e3ae22;}
html,body{margin:0;width:720px;height:1280px;overflow:hidden;background:var(--paper);}
body{font-family:"Alexandria",sans-serif;color:var(--ink);position:relative;
 background:
  radial-gradient(ellipse 520px 760px at 360px 640px,rgba(255,255,255,.55) 0%,rgba(255,255,255,0) 70%),
  repeating-linear-gradient(0deg,rgba(40,30,20,.045) 0 1px,transparent 1px 40px),
  repeating-linear-gradient(90deg,rgba(40,30,20,.045) 0 1px,transparent 1px 40px),
  radial-gradient(ellipse 900px 1100px at 360px 640px,#f4f0ea 40%,#e4ddd2 100%);}
#blocks{position:absolute;inset:0}
.blk{position:absolute;will-change:transform}
svg.stage{position:absolute;inset:0}
#deco{position:absolute;inset:0}
.handle{position:absolute;top:30px;right:32px;font-size:17px;font-weight:600;color:#6d665e;letter-spacing:.3px}
.handle b{direction:ltr;display:inline-block;color:#3b3530}
.top{position:absolute;left:30px;right:30px;top:78px;text-align:center}
#kick{font-size:30px;font-weight:600;color:#5d564e;min-height:40px}
#hero{font-size:104px;font-weight:800;line-height:1.2;margin-top:34px;white-space:nowrap;display:inline-block;transform-origin:50% 60%}
#sub{font-size:30px;font-weight:700;color:var(--ink);margin-top:0;min-height:40px}
.hl{background:var(--yel);color:#1d1a17;border-radius:10px;padding:0 .18em;display:inline-block;box-shadow:0 3px 0 rgba(0,0,0,.12)}
.st{position:relative;display:inline-block;color:#9a938a}
.st:after{content:"";position:absolute;right:-4%;top:52%;height:.09em;width:calc(var(--s,0)*108%);background:var(--red);border-radius:4px}
.cap{position:absolute;left:24px;right:24px;top:996px;text-align:center;font-size:36px;font-weight:700;white-space:nowrap}
.cap span{display:inline-block;padding:2px 8px;border-radius:9px;margin:0 1px}
#prog{position:absolute;right:0;top:1262px;height:5px;background:var(--red);border-radius:3px}
#progbg{position:absolute;left:0;right:0;top:1263px;height:3px;background:rgba(0,0,0,.08)}
.cards{position:absolute;left:0;right:0;display:flex;justify-content:center;gap:16px;direction:rtl}
.tk{width:150px;height:190px;background:#fbf9f5;border:2.5px solid #1d1a17;border-radius:16px;position:relative;text-align:center;box-shadow:0 8px 18px rgba(60,40,20,.18)}
.tk .n{position:absolute;top:8px;left:8px;width:24px;height:24px;border-radius:50%;color:#fff;font-size:15px;font-weight:800;line-height:24px;direction:ltr}
.tk .ic{height:112px;display:flex;align-items:center;justify-content:center;font-size:56px;font-weight:800;margin-top:22px}
.tk .lb{font-size:28px;font-weight:800}
.choice{position:absolute;left:0;right:0;top:470px;display:flex;justify-content:center;gap:26px;direction:rtl}
.opt{width:250px;height:330px;border-radius:22px;color:#fff;text-align:center;position:relative;box-shadow:0 14px 30px rgba(40,25,10,.25)}
.opt .ic{height:230px;display:flex;align-items:center;justify-content:center;font-size:90px;font-weight:800}
.opt .lb{font-size:38px;font-weight:800}
"""

JS_HELP = r"""
const NS='http://www.w3.org/2000/svg', $=id=>document.getElementById(id);
const clamp=(x,a=0,b=1)=>Math.max(a,Math.min(b,x));
const ease=x=>{x=clamp(x);return 1-Math.pow(1-x,3)};
const back=x=>{x=clamp(x);const c=1.70158;return 1+(c+1)*Math.pow(x-1,3)+c*Math.pow(x-1,2)};
const inout=x=>{x=clamp(x);return x<.5?4*x*x*x:1-Math.pow(-2*x+2,3)/2};
const lerp=(a,b,k)=>a+(b-a)*k;
const prog=(t,a,b)=>clamp((t-a)/(b-a));
const rnd=i=>{const s=Math.sin(i*127.1)*43758.5453;return s-Math.floor(s)};
function el(tag,attrs,parent){const e=document.createElementNS(NS,tag);for(const k in attrs)e.setAttribute(k,attrs[k]);parent.appendChild(e);return e}
/* object entrance: slide from dx,dy + fade in [tin,tin+.5], fade out [tout,tout+.4] */
function show(id,t,tin,tout=99,dx=0,dy=40,sc=1){const k=back(prog(t,tin,tin+.55))*(1-0)+0, o=ease(prog(t,tin,tin+.35))*(1-prog(t,tout,tout+.35));
  const e=$(id); if(!e) return 0; const kk=clamp(k,0,1.2);
  e.setAttribute('opacity',o); e.setAttribute('transform',`translate(${(1-kk)*dx} ${(1-kk)*dy})`+(sc!==1?'':'')); return o}
/* instruments */
function setScale(id,g){const e=$(id+'_lcd'); if(e) e.textContent=(Math.round(g*10)/10).toFixed(1)}
function setWatch(id,sec,a0=null,a1=null,ao=0){
  const G=$(id+'_d')||$(id); const cx=+G.dataset.cx, cy=+G.dataset.cy, r=+G.dataset.r;
  const ang=(sec%60)/60*2*Math.PI;
  $(id+'_hand').setAttribute('transform',`rotate(${sec%60*6} ${cx} ${cy})`);
  const A=$(id+'_arc');
  if(a0===null||ao<=0){A.setAttribute('opacity',0);return}
  const R=r*.80, p=s=>[cx+R*Math.sin(s/60*2*Math.PI), cy-R*Math.cos(s/60*2*Math.PI)];
  const [x0,y0]=p(a0),[x1,y1]=p(a1);
  A.setAttribute('d',`M${x0} ${y0} A${R} ${R} 0 ${a1-a0>30?1:0} 1 ${x1} ${y1}`); A.setAttribute('opacity',ao)}
const CLIPS=[];
function drawClips(t){CLIPS.forEach(c=>{const cv=$(c.id),cx=cv.getContext('2d');
  const i=Math.max(0,Math.min(c.imgs.length-1,Math.floor((t-c.t0)*c.fps*c.speed)));
  const o=ease(prog(t,c.tin,c.tin+.4))*(1-prog(t,c.tout,c.tout+.4)); cv.style.opacity=o;
  if(o>0&&c.imgs[i].complete) cx.drawImage(c.imgs[i],0,0,cv.width,cv.height)})}
function setCup(id,crema){const e=$(id+'_crema'); if(e) e.setAttribute('opacity',crema)}
"""

JS_COMMON = r"""
const LBL=LB.map(([n,c,d,tp,p,anc,at,out])=>{
  const g=el('g',{},$('labels'));
  const line=el('path',{d:p,stroke:'#1d1a17','stroke-width':1.6,fill:'none'},g);
  const L=line.getTotalLength(); line.setAttribute('stroke-dasharray',L);
  const dot=el('circle',{cx:d[0],cy:d[1],r:4,fill:'#c8102e'},g);
  const tx=el('text',{x:tp[0],y:tp[1],fill:c,'text-anchor':anc},g); tx.textContent=n;
  return {g,line,L,dot,tx,at,out};
});
/* colour blocks: one layout per phase, drift between them */
const BC=['#c8102e','#1f4e9a','#e3ae22','#1f4e9a','#e3ae22'];
function lay(pi){return BC.map((c,k)=>{const s=pi*13+k*7, left=(k+pi)%2===0;
  const w=60+rnd(s+1)*70, h=50+rnd(s+2)*70, y=320+((k+pi*2)%5)*130+rnd(s+3)*40;
  const x=left?-30+rnd(s+4)*50:690-w+rnd(s+5)*50; return [x,y,w,h]})}
const LAYS=PH.map((p,i)=>lay(i));
const BL=BC.map(c=>{const d=document.createElement('div');d.className='blk';d.style.background=c;$('blocks').appendChild(d);return d});
function md(s){return s.replace(/(@[A-Za-z0-9_.]+)/g,'<span style="direction:ltr;unicode-bidi:isolate;display:inline-block">$1</span>').replace(/\[\[(.+?)\]\]/g,'<span class="hl">$1</span>').replace(/~~(.+?)~~/g,'<span class="st">$1</span>')}
let lastPh=-1;
function common(t){
  let i=0; for(let j=0;j<PH.length;j++) if(t>=PH[j][0]) i=j;
  const [ps,kick,hero,sub,col]=PH[i], pe=i+1<PH.length?PH[i+1][0]:99;
  if(i!==lastPh){$('kick').innerHTML=md(kick);$('hero').innerHTML=md(hero);$('sub').innerHTML=md(sub);$('hero').style.color=col;
    const hw=$('hero').scrollWidth; $('hero').style.fontSize=''; if(hw>650) $('hero').style.fontSize=(104*650/hw)+'px'; lastPh=i;}
  const kin=prog(t,ps,ps+.45), kout=1-prog(t,pe-.18,pe);
  $('kick').style.opacity=ease(kin)*kout; $('kick').style.transform=`translateY(${(1-ease(kin))*-12}px)`;
  const hk=back(prog(t,ps+.08,ps+.55)); $('hero').style.opacity=ease(prog(t,ps+.08,ps+.3))*kout;
  $('hero').style.transform=`scale(${.7+.3*hk})`;
  $('sub').style.opacity=ease(prog(t,ps+.35,ps+.75))*kout;
  document.querySelectorAll('#hero .hl,#kick .hl,#sub .hl').forEach((h,j)=>{const k=back(prog(t,ps+.2+j*.15,ps+.6+j*.15));h.style.transform=`scale(${.6+.4*k}) rotate(${(1-k)*-4}deg)`});
  document.querySelectorAll('.st').forEach(s=>s.style.setProperty('--s',inout(prog(t,ps+.6,ps+1.1))));
  // blocks drift
  const bk=inout(prog(t,ps,ps+.7)), A=LAYS[Math.max(0,i-1)], B=LAYS[i];
  BL.forEach((d,k)=>{const a=i?A[k]:B[k],b=B[k];const x=lerp(a[0],b[0],bk),y=lerp(a[1],b[1],bk),w=lerp(a[2],b[2],bk),h=lerp(a[3],b[3],bk);
    d.style.left=x+'px';d.style.top=y+'px';d.style.width=w+'px';d.style.height=h+'px';d.style.opacity=.95*ease(prog(t,0,.6))});
  $('prog').style.width=(720*clamp(t/D))+'px';
  // leader labels
  LBL.forEach(l=>{l.line.setAttribute('stroke-dashoffset',l.L*(1-ease(prog(t,l.at,l.at+.45))));
    l.g.setAttribute('opacity',l.out<99?1-prog(t,l.out,l.out+.4):1);
    l.dot.setAttribute('r',4*ease(prog(t,l.at,l.at+.2)));
    const tk=ease(prog(t,l.at+.25,l.at+.6)); l.tx.setAttribute('opacity',tk);});
  // takeaway cards
  if(CARDS) CARDS.items.forEach((c,j)=>{const e=$('tk'+j),k=back(prog(t,c[1],c[1]+.5));
    e.style.opacity=ease(prog(t,c[1],c[1]+.3))*(CARDS.out?1-prog(t,CARDS.out,CARDS.out+.4):1); e.style.transform=`translateY(${(1-k)*60}px) rotate(${(1-k)*6}deg)`});
  // choice end card
  let wo=1;
  if(CHOICE){const k=prog(t,CHOICE.t,CHOICE.t+.6); wo=1-ease(prog(t,CHOICE.t-.2,CHOICE.t+.2));
    CHOICE.opts.forEach((o,j)=>{const e=$('op'+j),kk=back(prog(t,CHOICE.t+.1+j*.18,CHOICE.t+.65+j*.18));
      e.style.opacity=ease(prog(t,CHOICE.t+.1+j*.18,CHOICE.t+.4+j*.18)); e.style.transform=`translateY(${(1-kk)*80}px) rotate(${(j?3:-3)*(1-kk)+(j?2:-2)*Math.sin(t*2)*.4}deg)`})}
  $('world').setAttribute('opacity',wo);
  // captions
  let ci=-1; for(let j=0;j<CAPS.length;j++) if(t>=CAPS[j][0][1]-0.05) ci=j;
  const cs=$('cs');
  if(ci<0){cs.innerHTML='';} else {
    const ch=CAPS[ci], end=ci+1<CAPS.length?CAPS[ci+1][0][1]-0.05:99;
    const ck=ease(prog(t,ch[0][1]-0.05,ch[0][1]+0.12));
    cs.innerHTML=ch.map(([w,s,e])=>{const on=t>=s&&t<e+0.02, past=t>=s;
      return `<span style="background:${on?'#e3ae22':'transparent'};opacity:${past?1:.3}">${w}</span>`}).join(' ');
    cs.style.opacity=t<end?ck:0; cs.style.transform=`translateY(${(1-ck)*10}px)`;
  }
}
function seek(t){ scene(t); common(t); drawClips(t); }
window.READY=Promise.all(CLIPS.flatMap(c=>c.imgs.map(im=>im.complete?1:new Promise(r=>{im.onload=im.onerror=r}))));
window.seek=seek; window.DURATION=D;
seek(new URLSearchParams(location.search).get('t')*1||3);
"""

DEFS = r"""
<filter id="shd" x="-30%" y="-30%" width="160%" height="170%"><feDropShadow dx="0" dy="16" stdDeviation="14" flood-color="#3a2410" flood-opacity=".28"/></filter>
<linearGradient id="bMetal" x1="0" y1="0" x2="1" y2="1"><stop offset="0" stop-color="#d9d6d1"/><stop offset=".45" stop-color="#a9a49d"/><stop offset=".55" stop-color="#c9c5bf"/><stop offset="1" stop-color="#7d7871"/></linearGradient>
<linearGradient id="bDark" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#4a4541"/><stop offset="1" stop-color="#1c1917"/></linearGradient>
<pattern id="bBrush" width="6" height="200" patternUnits="userSpaceOnUse"><rect width="6" height="200" fill="#bdb8b1"/><rect width="2" height="200" fill="#a29d96"/><rect x="3" width="1" height="200" fill="#d4d0ca"/></pattern>
<radialGradient id="bFace" cx=".45" cy=".4" r=".7"><stop offset="0" stop-color="#ffffff"/><stop offset="1" stop-color="#e6e2dc"/></radialGradient>
<radialGradient id="bCer" cx=".35" cy=".3" r=".9"><stop offset="0" stop-color="#ecd9bf"/><stop offset=".6" stop-color="#d2b48e"/><stop offset="1" stop-color="#a98559"/></radialGradient>
<radialGradient id="bCrema" cx=".45" cy=".4" r=".6"><stop offset="0" stop-color="#e8a858"/><stop offset=".7" stop-color="#c47a2c"/><stop offset="1" stop-color="#7a3f12"/></radialGradient>
<pattern id="bSpeck" width="23" height="19" patternUnits="userSpaceOnUse"><circle cx="4" cy="5" r="1" fill="#6b4b2a" opacity=".45"/><circle cx="15" cy="13" r=".8" fill="#6b4b2a" opacity=".4"/><circle cx="19" cy="3" r=".6" fill="#3d2814" opacity=".5"/></pattern>
<pattern id="bHatch" width="8" height="8" patternUnits="userSpaceOnUse" patternTransform="rotate(45)"><rect width="8" height="8" fill="none"/><path d="M0 0 V8" stroke="#8b847b" stroke-width="1.2"/></pattern>
"""

DECO = r"""
<g stroke="#8b847b" stroke-width="1.3" fill="none" opacity=".7">
 <line x1="80" y1="470" x2="640" y2="470"/><line x1="110" y1="950" x2="610" y2="950"/>
 <g id="xh1"><circle cx="612" cy="560" r="11"/><path d="M596 560h32M612 544v32"/></g>
 <g><circle cx="96" cy="880" r="11"/><path d="M80 880h32M96 864v32"/></g>
 <rect x="560" y="900" width="70" height="34" fill="url(#bHatch)"/><rect x="560" y="900" width="70" height="34"/>
 <rect x="70" y="500" width="70" height="34" fill="url(#bHatch)"/><rect x="70" y="500" width="70" height="34"/>
</g>"""

def SCALE(id, x, y, w=300):
    """Digital kitchen scale, top-left at (x,y). JS: setScale(id, grams)."""
    h = w * .62
    return f'''<g id="{id}" filter="url(#shd)">
<path d="M{x+w*.04} {y+h*.30} L{x+w*.96} {y+h*.30} L{x+w} {y+h*.92} Q{x+w} {y+h} {x+w*.94} {y+h} L{x+w*.06} {y+h} Q{x} {y+h} {x} {y+h*.92} Z" fill="url(#bDark)"/>
<path d="M{x+w*.08} {y} L{x+w*.92} {y} L{x+w*.98} {y+h*.34} L{x+w*.02} {y+h*.34} Z" fill="url(#bBrush)" stroke="#8d8880" stroke-width="1.5"/>
<rect x="{x+w*.30}" y="{y+h*.48}" width="{w*.56}" height="{h*.36}" rx="8" fill="#0b0a09" stroke="#3c3835" stroke-width="3"/>
<text id="{id}_lcd" x="{x+w*.83}" y="{y+h*.76}" text-anchor="end" font-family="'Share Tech Mono',monospace" font-size="{h*.32}" fill="#f4efe6" style="direction:ltr">0.0</text>
<text x="{x+w*.845}" y="{y+h*.80}" font-family="'Share Tech Mono',monospace" font-size="{h*.09}" fill="#cfc8bd">g</text>
<circle cx="{x+w*.17}" cy="{y+h*.66}" r="{h*.09}" fill="url(#bMetal)" stroke="#2a2725" stroke-width="2"/>
</g>'''

def WATCH(id, cx, cy, r=150):
    """Analog stopwatch. JS: setWatch(id, sec, arcFromSec, arcToSec, arcOpacity)."""
    ticks = ''.join(
        f'<line x1="{cx}" y1="{cy-r*.86}" x2="{cx}" y2="{cy-r*(.78 if i%5==0 else .82)}" stroke="#2a2725" stroke-width="{3 if i%5==0 else 1.4}" transform="rotate({i*6} {cx} {cy})"/>'
        for i in range(60))
    nums = ''.join(
        f'<text x="{cx+r*.64*__import__("math").sin(n/60*6.2832):.1f}" y="{cy-r*.64*__import__("math").cos(n/60*6.2832)+r*.07:.1f}" text-anchor="middle" font-family="Alexandria" font-size="{r*.14:.0f}" font-weight="600" fill="#2a2725" style="direction:ltr">{n}</text>'
        for n in range(10, 61, 10))
    return f'''<g id="{id}" data-cx="{cx}" data-cy="{cy}" data-r="{r}" filter="url(#shd)">
<rect x="{cx-r*.12}" y="{cy-r*1.22}" width="{r*.24}" height="{r*.16}" rx="4" fill="url(#bMetal)" stroke="#5d5852" stroke-width="2"/>
<rect x="{cx-r*.07}" y="{cy-r*1.10}" width="{r*.14}" height="{r*.14}" fill="url(#bMetal)" stroke="#5d5852" stroke-width="2"/>
<circle cx="{cx}" cy="{cy}" r="{r}" fill="url(#bMetal)" stroke="#6f6a64" stroke-width="2"/>
<circle cx="{cx}" cy="{cy}" r="{r*.91}" fill="url(#bFace)" stroke="#8d8880" stroke-width="2"/>
{ticks}{nums}
<path id="{id}_arc" fill="none" stroke="#e3ae22" stroke-width="{r*.09:.1f}" stroke-linecap="round" opacity="0"/>
<line id="{id}_hand" x1="{cx}" y1="{cy+r*.14}" x2="{cx}" y2="{cy-r*.80}" stroke="#c8102e" stroke-width="4" stroke-linecap="round"/>
<circle cx="{cx}" cy="{cy}" r="{r*.06}" fill="#2a2725"/>
</g>'''

def CUP(id, cx, cy, r=120):
    """Top-view ceramic espresso cup on saucer with crema. JS: setCup(id, cremaOpacity)."""
    return f'''<g id="{id}" filter="url(#shd)">
<ellipse cx="{cx}" cy="{cy}" rx="{r*1.45}" ry="{r*1.38}" fill="url(#bCer)"/><ellipse cx="{cx}" cy="{cy}" rx="{r*1.45}" ry="{r*1.38}" fill="url(#bSpeck)"/>
<ellipse cx="{cx}" cy="{cy}" rx="{r*1.1}" ry="{r*1.05}" fill="none" stroke="#a5835a" stroke-width="2" opacity=".6"/>
<path d="M{cx+r*.95} {cy-r*.22} q{r*.55} {-r*.05} {r*.55} {r*.22} q0 {r*.27} {-r*.55} {r*.22}" fill="none" stroke="#c8a77d" stroke-width="{r*.17:.0f}" stroke-linecap="round"/>
<circle cx="{cx}" cy="{cy}" r="{r}" fill="url(#bCer)"/><circle cx="{cx}" cy="{cy}" r="{r}" fill="url(#bSpeck)"/>
<circle cx="{cx}" cy="{cy}" r="{r*.84}" fill="#3a1d0b"/>
<circle id="{id}_crema" cx="{cx}" cy="{cy}" r="{r*.84}" fill="url(#bCrema)"/>
<ellipse cx="{cx-r*.25}" cy="{cy-r*.3}" rx="{r*.25}" ry="{r*.12}" fill="#fff" opacity=".18" transform="rotate(-30 {cx-r*.25} {cy-r*.3})"/>
</g>'''

def caps_json(chunks, D):
    out = []
    for ci, ch in enumerate(chunks):
        nxt = chunks[ci+1][0][1] if ci+1 < len(chunks) else D
        row = []
        for wi, (txt, s) in enumerate(ch):
            e = ch[wi+1][1] if wi+1 < len(ch) else nxt
            row.append([txt, round(s, 2), round(e, 2)])
        out.append(row)
    return json.dumps(out, ensure_ascii=False)

def build(d, cfg):
    cards = cfg.get('cards')
    choice = cfg.get('choice')
    cards_html = ''
    if cards:
        cards_html = f'<div class="cards" style="top:{cards.get("top",840)}px">' + ''.join(
            f'<div class="tk" id="tk{j}" style="opacity:0"><div class="n" style="background:{c[2]}">{j+1}</div><div class="ic">{c[3]}</div><div class="lb">{c[0]}</div></div>'
            for j, c in enumerate(cards['items'])) + '</div>'
    choice_html = ''
    if choice:
        choice_html = '<div class="choice">' + ''.join(
            f'<div class="opt" id="op{j}" style="background:{o[1]};opacity:0"><div class="ic">{o[2]}</div><div class="lb">{o[0]}</div></div>'
            for j, o in enumerate(choice['opts'])) + '</div>'
    js_cfg = (f"const D={cfg['D']}, CAPS={caps_json(cfg['chunks'], cfg['D'])}, PH={json.dumps(cfg['PH'], ensure_ascii=False)}, "
              f"LB={json.dumps(cfg.get('LB', []), ensure_ascii=False)}, CARDS={json.dumps(cards, ensure_ascii=False) if cards else 'null'}, "
              f"CHOICE={json.dumps(choice, ensure_ascii=False) if choice else 'null'};")
    html = ('<!doctype html><html dir="rtl" lang="ar"><head><meta charset="utf-8">'
            '<link href="https://fonts.googleapis.com/css2?family=Alexandria:wght@400;500;600;700;800;900&family=Share+Tech+Mono&display=swap" rel="stylesheet">'
            '<style>' + CSS + '</style></head><body>'
            '<div id="blocks"></div>'
            '<svg class="stage" style="direction:ltr" viewBox="0 0 720 1280" width="720" height="1280"><defs>' + DEFS + cfg.get('defs', '') + '</defs>'
            + DECO +
            '<g id="world">' + cfg['scene_svg'] + '<g id="labels" font-family="Alexandria, sans-serif" font-size="24" font-weight="700"></g></g></svg>'
            + (('<div class="handle"><b>' + cfg['handle'] + '</b></div>') if cfg.get('handle') else '') +
            '<div class="top"><div id="kick"></div><div id="hero"></div><div id="sub"></div></div>'
            + cfg.get('overlay_html','') + cards_html + choice_html +
            '<div class="cap" id="cs"></div><div id="progbg"></div><div id="prog"></div>'
            '<script>' + JS_HELP + js_cfg + cfg.get('init_js', '') + cfg['scene_js'] + JS_COMMON + '</script></body></html>')
    open(os.path.join(d, 'reel_ar.html'), 'w').write(html)
    print('built (style B)', d)


# ---------- Photo assets (Gemini-generated cutouts in coffee-daily/assets_b/) ----------
ASSETS = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'assets_b')

def _size(name):
    from PIL import Image
    return Image.open(os.path.join(ASSETS, name + '.png')).size

def asset_url(name):
    return 'file://' + os.path.join(ASSETS, name + '.png')

def IMG(id, name, x, y, w, extra=''):
    """Place a photo cutout (assets_b/<name>.png) with top-left (x,y) and width w. Animate with show(id,...)."""
    W, H = _size(name)
    return f'<g id="{id}" filter="url(#shd)"><image href="{asset_url(name)}" x="{x}" y="{y}" width="{w}" height="{w*H/W:.1f}"/>{extra}</g>'

def SCALE_IMG(id, x, y, w=420):
    """Photo scale with live LCD digits. JS: setScale(id, grams)."""
    W, H = _size('scale'); k = w / W
    # LCD parallelogram in native px: TL(210,400) TR(482,488) BL(157,462)
    lcd = (f'<g transform="matrix(1 0.3235 -0.8548 1 210 400)">'
           f'<text id="{id}_lcd" x="250" y="50" text-anchor="end" font-family="\'Share Tech Mono\',monospace" font-size="48" fill="#f4efe6" style="direction:ltr">0.0</text>'
           f'<text x="254" y="50" font-family="\'Share Tech Mono\',monospace" font-size="16" fill="#cfc8bd">g</text></g>')
    return (f'<g id="{id}" filter="url(#shd)"><g transform="translate({x} {y}) scale({k:.4f})">'
            f'<image href="{asset_url("scale")}" width="{W}" height="{H}"/>{lcd}</g></g>')

def WATCH_IMG(id, x, y, w=380):
    """Photo stopwatch (empty dial) with needle + yellow arc. JS: setWatch(id, sec, from, to, arcOpacity)."""
    W, H = _size('stopwatch'); k = w / W
    cx, cy, r = 377, 536, 300
    return (f'<g id="{id}" filter="url(#shd)"><g transform="translate({x} {y}) scale({k:.4f})">'
            f'<image href="{asset_url("stopwatch")}" width="{W}" height="{H}"/>'
            f'<g id="{id}_d" data-cx="{cx}" data-cy="{cy}" data-r="{375}">'
            f'<path id="{id}_arc" fill="none" stroke="#e3ae22" stroke-width="22" stroke-linecap="round" opacity=".0" style="mix-blend-mode:multiply"/>'
            f'<line id="{id}_hand" x1="{cx}" y1="{cy+50}" x2="{cx}" y2="{cy-r*.92:.0f}" stroke="#c8102e" stroke-width="9" stroke-linecap="round"/>'
            f'<circle cx="{cx}" cy="{cy}" r="16" fill="#2a2725"/><circle cx="{cx}" cy="{cy}" r="6" fill="#c8102e"/></g></g></g>')


# ---------- Video clips (Google Flow / Veo, white background) ----------
def clip_frames(mp4, out_dir, fps=30, crop=None, white=0.92, feather=90):
    """Extract a Flow clip to JPG frames. Lifts the light-grey studio background to pure white
    (colorlevels input max = white) and feathers the frame edges to white so a multiply-blended
    clip has no visible rectangle. crop='w:h:x:y' (on the 720x1280 source) optional. Returns frame count."""
    import subprocess
    import numpy as np
    from PIL import Image
    os.makedirs(out_dir, exist_ok=True)
    vf = (f'crop={crop},' if crop else '') + f'fps={fps},colorlevels=rimax={white}:gimax={white}:bimax={white}'
    subprocess.run(['ffmpeg', '-v', 'error', '-y', '-i', mp4, '-vf', vf, '-q:v', '2', os.path.join(out_dir, '%04d.jpg')], check=True)
    files = sorted(f for f in os.listdir(out_dir) if f.endswith('.jpg'))
    if feather and files:
        w, h = Image.open(os.path.join(out_dir, files[0])).size
        yy, xx = np.mgrid[0:h, 0:w]
        d = np.minimum(np.minimum(xx, w - 1 - xx), np.minimum(yy, h - 1 - yy)).astype(np.float32)
        m = np.clip(d / feather, 0, 1); m = (m * m * (3 - 2 * m))[..., None]
        for f in files:
            fp = os.path.join(out_dir, f)
            a = np.asarray(Image.open(fp).convert('RGB')).astype(np.float32)
            Image.fromarray((a * m + 255 * (1 - m)).astype(np.uint8)).save(fp, quality=92)
    return len(files)

def CLIP(id, frames_dir, n, x, y, w, h, t0, fps=30, speed=1.0, tin=None, tout=99):
    """HTML layer: canvas showing a frame sequence, multiplied onto the paper so a white background vanishes.
    Plays from scene time t0 (holds last frame). Fades in at tin (default t0), out at tout.
    Returns (html, js). Put html in cfg['overlay_html'] and js in cfg['init_js']."""
    tin = t0 if tin is None else tin
    srcs = [ 'file://' + os.path.join(os.path.abspath(frames_dir), f'{i:04d}.jpg') for i in range(1, n + 1)]
    html = (f'<canvas id="{id}" width="{w*2}" height="{h*2}" style="position:absolute;left:{x}px;top:{y}px;'
            f'width:{w}px;height:{h}px;mix-blend-mode:multiply;opacity:0;pointer-events:none"></canvas>')
    js = (f"CLIPS.push({{id:'{id}',t0:{t0},fps:{fps},speed:{speed},tin:{tin},tout:{tout},"
          f"imgs:{json.dumps(srcs)}.map(s=>{{const im=new Image();im.src=s;return im}})}});")
    return html, js
