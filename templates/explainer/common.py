"""Shared reel skeleton. build(dir, cfg) -> dir/reel_ar.html"""
import json, os
CSS = open(os.path.join(os.path.dirname(__file__), 'common.css')).read() if os.path.exists(os.path.join(os.path.dirname(__file__), 'common.css')) else ''
JS_HELP = r"""
const NS='http://www.w3.org/2000/svg', $=id=>document.getElementById(id);
const clamp=(x,a=0,b=1)=>Math.max(a,Math.min(b,x));
const ease=x=>{x=clamp(x);return 1-Math.pow(1-x,3)};
const inout=x=>{x=clamp(x);return x<.5?4*x*x*x:1-Math.pow(-2*x+2,3)/2};
const lerp=(a,b,k)=>a+(b-a)*k;
const prog=(t,a,b)=>clamp((t-a)/(b-a));
const rnd=i=>{const s=Math.sin(i*127.1)*43758.5453;return s-Math.floor(s)};
function el(tag,attrs,parent){const e=document.createElementNS(NS,tag);for(const k in attrs)e.setAttribute(k,attrs[k]);parent.appendChild(e);return e}
function surface(x0,x1,y,amp,ph){let d='';for(let x=x0;x<=x1+8;x+=8){const xx=Math.min(x,x1);d+=(d?' L':'M')+xx.toFixed(1)+' '+(y+amp*Math.sin(xx*.06+ph)).toFixed(1)}return d}
"""
JS_COMMON = r"""
const LBL=LB.map(([n,c,d,tp,p,anc,at,out])=>{
  const g=el('g',{},$('labels'));
  const line=el('path',{d:p,stroke:'#9c8f80','stroke-width':1.5,fill:'none'},g);
  const L=line.getTotalLength(); line.setAttribute('stroke-dasharray',L);
  const dot=el('circle',{cx:d[0],cy:d[1],r:4,fill:'#f1e6d6'},g);
  const tx=el('text',{x:tp[0],y:tp[1],fill:c,'text-anchor':anc},g); tx.textContent=n;
  return {g,line,L,dot,tx,at,out};
});
function common(t){
  ['t0','t1','t2','t3'].forEach((id,i)=>{const k=ease(prog(t,.02+i*.06,.4+i*.06));$(id).style.opacity=k;$(id).style.transform=`translateY(${(1-k)*18}px)`});
  $('t3').style.opacity=Math.min(ease(prog(t,.2,.6)),1-prog(t,CH_OUT,CH_OUT+.4));
  const ck=ease(prog(t,.25,.7));
  $('chips').style.opacity=ck*(1-prog(t,CH_OUT,CH_OUT+.4)); $('chips').style.transform=`translateY(${(1-ck)*14}px)`;
  ['tileT','tileW'].forEach((id,i)=>{const k=ease(prog(t,.5+i*.1,.9+i*.1));$(id).style.opacity=k;$(id).style.transform=`scale(${.9+.1*k})`});
  $('wm').style.opacity=.45*ease(prog(t,.3,.8));
  LBL.forEach(l=>{
    l.line.setAttribute('stroke-dashoffset',l.L*(1-ease(prog(t,l.at,l.at+.45))));
    l.g.setAttribute('opacity',l.out<99?1-prog(t,l.out,l.out+.4):1);
    l.dot.setAttribute('r',4*ease(prog(t,l.at,l.at+.2)));
    const tk=ease(prog(t,l.at+.25,l.at+.6)); l.tx.setAttribute('opacity',tk);
    l.tx.setAttribute('transform',`translate(${(1-tk)*12} 0)`);});
  let i=0; for(let j=0;j<PH.length;j++) if(t>=PH[j][0]) i=j;
  const [ps,h,c]=PH[i], pe=i+1<PH.length?PH[i+1][0]:99;
  const kin=ease(prog(t,ps+(i?0:.1),ps+(i?0:.1)+.25)), kout=1-prog(t,pe-.15,pe);
  $('card').style.opacity=ease(prog(t,0,.3));
  $('ch').textContent=h; $('ch').style.color=c; $('bar').style.background=c;
  const k=Math.min(kin,kout); $('ch').style.opacity=k; $('ch').style.transform=`translateY(${(1-k)*14}px)`;
  let ci=-1; for(let j=0;j<CAPS.length;j++) if(t>=CAPS[j][0][1]-0.05) ci=j;
  const cs=$('cs');
  if(ci<0){cs.innerHTML='';} else {
    const ch=CAPS[ci], end=ci+1<CAPS.length?CAPS[ci+1][0][1]-0.05:99;
    const ck2=ease(prog(t,ch[0][1]-0.05,ch[0][1]+0.1));
    cs.innerHTML=ch.map(([w,s,e])=>{const on=t>=s&&t<e+0.02, past=t>=s;
      return `<span style="color:${on?c:'#f1e6d6'};opacity:${past?1:.35}">${w}</span>`}).join(' ');
    cs.style.opacity=t<end?ck2:0; cs.style.transform=`scale(${.92+.08*ck2})`;
  }
}
function seek(t){ scene(t); common(t); }
window.seek=seek; window.DURATION=D;
seek(new URLSearchParams(location.search).get('t')*1||12);
"""
def caps_json(chunks, D):
    # chunks: list of list of (text,start)
    out=[]
    for ci,ch in enumerate(chunks):
        nxt = chunks[ci+1][0][1] if ci+1<len(chunks) else D
        row=[]
        for wi,(txt,s) in enumerate(ch):
            e = ch[wi+1][1] if wi+1<len(ch) else nxt
            row.append([txt,round(s,2),round(e,2)])
        out.append(row)
    return json.dumps(out, ensure_ascii=False)
def build(d, cfg):
    css = open(os.path.join(os.path.dirname(__file__),'common.css')).read()
    chips=''.join(f'<div class="chip"><span>{a}</span><b>{b}</b></div>' for a,b in cfg['chips'])
    h=cfg['header']
    html=f"""<!doctype html>
<html dir="rtl" lang="ar"><head><meta charset="utf-8">
<link href="https://fonts.googleapis.com/css2?family=Alexandria:wght@400;500;600;700;800&display=swap" rel="stylesheet">
<style>{css}</style></head><body>
<svg style="direction:ltr" viewBox="0 0 720 1280" width="720" height="1280">
<defs>{cfg['defs']}</defs>
<g id="world">{cfg['scene_svg']}<g id="labels" font-family="Alexandria, sans-serif" font-size="24" font-weight="600"></g></g>
</svg>
<div class="top"><div class="lbl" id="t0">{h[0]}</div><h1 id="t1">{h[1]}</h1><div class="sub" id="t2">{h[2]}</div><div class="tiny" id="t3">{h[3]}</div></div>
<div class="chips" id="chips">{chips}</div>
<div class="wm" id="wm">{cfg.get("watermark","")}</div>
<div class="tile" id="tileT" style="right:24px"><span>{cfg['tiles'][0]}</span><b id="tv" style="direction:ltr">0:00</b></div>
<div class="tile" id="tileW" style="left:24px"><span>{cfg['tiles'][1]}</span><b id="wv">0</b></div>
<div class="card" id="card"><div id="bar"></div><div id="ch"></div><div id="cs"></div></div>
<script>
{JS_HELP}
const D={cfg['D']}, CH_OUT={cfg['ch_out']}, CAPS={caps_json(cfg['chunks'],cfg['D'])}, PH={json.dumps(cfg['PH'],ensure_ascii=False)}, LB={json.dumps(cfg['LB'],ensure_ascii=False)};
{cfg['init_js']}
{cfg['scene_js']}
{JS_COMMON}
</script></body></html>"""
    open(os.path.join(d,'reel_ar.html'),'w').write(html)
    print('built',d)
