import sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from common import build
os.chdir(os.path.dirname(os.path.abspath(__file__)))
D=31.3
chunks=[
[('الإيروبريس',0.0),('تسوي',0.92),('فيها',1.12)],
[('قهوة',1.36),('نظيفة',1.72),('في',2.14),('دقيقتين',2.22)],
[('بس',2.9),('أغلب',3.12),('الناس',3.48)],
[('يستخدمونها',3.74),('غلط!',4.28)],
[('حط',4.76),('ورقة',5.24),('الفلتر',5.48)],
[('في',5.9),('الغطاء،',6.0),('وبلل',6.58)],
[('الورقة',6.9),('بالماي',7.26)],
[('اطحن',8.18),('خمسة',8.68),('عشر',9.06),('غرام',9.26)],
[('بن',9.54),('طحنة',9.72),('متوسطة،',10.22)],
[('وحطها',10.94),('في',11.28),('الأسطوانة',11.38)],
[('صب',12.22),('ماي',12.66),('حار،',12.92)],
[('حوالي',13.4),('ثمانين',13.98),('درجة،',14.3)],
[('وحرّك',14.78),('عشر',15.46),('ثواني',15.74)],
[('إذا',16.34),('تبي',16.88),('تتعلم',17.14),('أكثر',17.48)],
[('عن',17.7),('القهوة،',17.8),('لا',18.24),('تنسى',18.42)],
[('تتابعني!',18.68)],
[('بعدها',19.72),('ركّب',20.48),('المكبس،',20.82)],
[('واضغط',21.4),('بهدوء',21.8)],
[('لين',22.26),('تسمع',22.64),('الهسهسة',23.0)],
[('والغلطة؟',23.98)],
[('لا',24.58),('تضغط',25.02),('بقوة!',25.44)],
[('الضغط',26.14),('القوي',26.54),('يطلع',26.84)],
[('قهوة',27.18),('مرّة',27.7)],
[('اكتب',28.14),('لي',28.74),('بالتعليقات',28.8)],
[('إيروبريس',29.5),('ولا',30.08),('فرنش',30.38),('بريس؟',30.72)]]
defs='''
<linearGradient id="gWat" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#5d93c4" stop-opacity=".8"/><stop offset="1" stop-color="#2f5a83" stop-opacity=".9"/></linearGradient>
<linearGradient id="gCof" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#7a4826" stop-opacity=".95"/><stop offset="1" stop-color="#3a1f0e" stop-opacity=".98"/></linearGradient>
<linearGradient id="gC" x1="0" x2="1"><stop offset="0" stop-color="#6f6a65"/><stop offset=".5" stop-color="#8a847d"/><stop offset="1" stop-color="#5d5955"/></linearGradient>
<radialGradient id="gGlow" cx=".5" cy=".5" r=".5"><stop offset="0" stop-color="#e0605a" stop-opacity=".5"/><stop offset="1" stop-color="#e0605a" stop-opacity="0"/></radialGradient>
<pattern id="grounds" width="9" height="9" patternUnits="userSpaceOnUse"><rect width="9" height="9" fill="#4a2c18"/><circle cx="2" cy="2" r="1.8" fill="#7a4d2b"/><circle cx="6.5" cy="6" r="1.5" fill="#2c1a0e"/><circle cx="6" cy="1.5" r="1.1" fill="#93603a"/></pattern>
<clipPath id="chClip"><rect x="304" y="560" width="112" height="292"/></clipPath>
<clipPath id="cupClip"><path d="M272 900 H448 L438 965 Q436 976 424 976 H296 Q284 976 282 965 Z"/></clipPath>'''
scene='''
<ellipse id="warn" cx="360" cy="760" rx="270" ry="300" fill="url(#gGlow)" opacity="0"/>
<g id="kettle" opacity="0"><path d="M720 330 C600 340 500 330 372 500" fill="none" stroke="#e9dccb" stroke-width="17" stroke-linecap="round"/><path d="M720 330 C600 340 500 330 372 500" fill="none" stroke="#2a2725" stroke-width="12" stroke-linecap="round"/></g>
<path id="stream" fill="none" stroke="#8fc1ef" stroke-width="5" stroke-linecap="round" opacity="0"/>
<g id="fall" fill="#6b4226"></g><g id="drops" fill="#8fc1ef"></g>
<!-- cup -->
<path d="M446 912 C500 912 500 962 440 962" fill="none" stroke="#e9dccb" stroke-width="9"/><path d="M446 912 C494 912 494 962 440 962" fill="none" stroke="#2a2725" stroke-width="4"/>
<path d="M270 898 H450 L440 966 Q438 978 424 978 H296 Q282 978 280 966 Z" fill="#1a1512" fill-opacity=".85"/>
<g clip-path="url(#cupClip)"><rect id="cupFill" x="262" width="196" fill="url(#gCof)"/></g>
<path d="M270 898 H450 L440 966 Q438 978 424 978 H296 Q282 978 280 966 Z" fill="none" stroke="#e9dccb" stroke-width="2.5"/>
<!-- drip -->
<path id="drip" fill="none" stroke="#7a4826" stroke-width="5" stroke-linecap="round" opacity="0"/>
<!-- chamber -->
<path d="M300 560 V852 H420 V560" fill="#1a1512" fill-opacity=".6"/>
<g clip-path="url(#chClip)">
<path id="water" fill="url(#gWat)"/><path id="coffee" fill="url(#gCof)"/><path id="liqTop" fill="none" stroke-width="2"/>
<rect id="bed" x="304" width="112" fill="url(#grounds)"/>
</g>
<rect id="paper" x="306" width="108" height="5" rx="2" fill="#efe6d8" stroke="#bfb3a3" stroke-width="1" opacity="0"/>
<g id="stir" opacity="0"><path id="stirH" stroke="#bdb6ad" stroke-width="7" stroke-linecap="round" fill="none"/></g>
<path d="M300 560 V852 M420 560 V852" stroke="#e9dccb" stroke-width="3" fill="none"/>
<g stroke="#e9dccb" stroke-width="2"><path d="M420 620 h14 M420 680 h14 M420 740 h14 M420 800 h14"/></g>
<g font-family="Alexandria" font-size="16" fill="#9c8f80" text-anchor="start"><text x="438" y="626">4</text><text x="438" y="686">3</text><text x="438" y="746">2</text><text x="438" y="806">1</text></g>
<!-- cap -->
<rect x="290" y="850" width="140" height="26" rx="6" fill="url(#gC)" stroke="#e9dccb" stroke-width="2.5"/>
<rect x="318" y="876" width="84" height="10" rx="3" fill="#2a2725" stroke="#e9dccb" stroke-width="2"/>
<!-- plunger -->
<g id="plunger" opacity="0" stroke="#e9dccb" stroke-width="2.5" stroke-linejoin="round">
<rect id="pBody" x="309" width="102" fill="#8a857f" fill-opacity=".92"/>
<rect id="pSeal" x="307" width="106" height="16" rx="3" fill="#1f1c1a"/>
<rect id="pTop" x="292" width="136" height="14" rx="4" fill="url(#gC)"/>
</g>
<g id="arrows" fill="none" stroke="#f1e6d6" stroke-width="3" stroke-linecap="round"></g>
<g id="hiss" fill="none" stroke="#f1e6d6" stroke-width="3" stroke-linecap="round"></g>
<g id="badge" opacity="0"><circle cx="210" cy="640" r="30" fill="#e0605a" stroke="#f1e6d6" stroke-width="2.5"/><text x="210" y="654" text-anchor="middle" font-family="Alexandria" font-size="40" font-weight="800" fill="#f1e6d6">!</text></g>
<g id="steam" fill="none" stroke="#f1e6d6" stroke-width="3" stroke-linecap="round"></g>'''
scene_js='''
function scene(t){
  const z=1+0.05*inout(prog(t,0,D));
  $('world').setAttribute('transform',`translate(360 678) scale(${0.9*z}) translate(-360 -740)`);
  // paper
  const pk=ease(prog(t,5.0,6.3));
  $('paper').setAttribute('y',lerp(380,845,pk)); $('paper').setAttribute('opacity',ease(prog(t,4.9,5.2)));
  const wet=prog(t,7.0,7.8); $('paper').setAttribute('fill',wet>0?'#9bb8d0':'#efe6d8');
  const Dr=$('drops'); Dr.innerHTML='';
  if(t>6.9&&t<7.9) for(let i=0;i<10;i++){const k=((t-6.9)*2.2+rnd(i))%1; el('circle',{cx:330+rnd(i+4)*60,cy:lerp(520,840,k),r:3},Dr)}
  // grounds
  const bedIn=inout(prog(t,8.2,11.4)), bedH=34*bedIn;
  $('bed').setAttribute('y',846-bedH); $('bed').setAttribute('height',bedH);
  const F=$('fall'); F.innerHTML='';
  if(t>8.2&&t<11.5) for(let i=0;i<30;i++){const k=((t-8.2)*1.7+rnd(i))%1; el('circle',{cx:330+rnd(i+11)*60,cy:lerp(480,846-bedH,k),r:1.6+rnd(i+5)*2.2},F)}
  // water
  const fill=inout(prog(t,12.3,14.6)), brew=inout(prog(t,13.5,18.5));
  const press=inout(prog(t,21.7,23.9)), ins=ease(prog(t,20.2,21.5));
  const sealY=press>0?lerp(650,846,press):lerp(470,650,ins);
  const base=lerp(846-bedH,650,fill);
  const L=(press>0||ins>0.99)?Math.max(base,Math.min(sealY,846)):base;
  const lv=(t<12.3)?900:(press>0?Math.max(base,sealY):base);
  const top=surface(302,418,lv,fill>0&&fill<1?2.5:1,t*4);
  const body=top+' L418 852 L302 852 Z';
  $('water').setAttribute('d',body); $('coffee').setAttribute('d',body);
  $('water').setAttribute('opacity',t>12.3?1-brew:0); $('coffee').setAttribute('opacity',t>12.3?brew:0);
  $('liqTop').setAttribute('d',top); $('liqTop').setAttribute('opacity',t>12.3&&lv<846?.8:0); $('liqTop').setAttribute('stroke',brew>.5?'#b07440':'#9cc7ee');
  // kettle
  const kk=ease(prog(t,12.0,12.4))*(1-ease(prog(t,14.6,15.1)));
  $('kettle').setAttribute('opacity',kk); $('kettle').setAttribute('transform',`translate(${(1-kk)*120} ${(1-kk)*-60})`);
  const sOn=t>12.4&&t<14.6;
  $('stream').setAttribute('d',`M372 502 C372 540 366 580 ${366+2*Math.sin(t*20)} ${lv}`); $('stream').setAttribute('opacity',sOn?.95:0);
  // stir
  const sp=ease(prog(t,14.7,15.0))*(1-ease(prog(t,16.0,16.3)));
  $('stir').setAttribute('opacity',sp);
  const ang=(t-14.7)*11, tx=360+30*Math.sin(ang), ty=lv+40+6*Math.cos(ang);
  $('stirH').setAttribute('d',`M440 500 L${tx} ${ty}`);
  // plunger
  $('plunger').setAttribute('opacity',ins>0?1:0);
  const jit=(t>24.4&&t<27.9)?3*Math.sin(t*40):0;
  const sy=sealY+jit;
  $('pSeal').setAttribute('y',sy-16); $('pBody').setAttribute('y',sy-290); $('pBody').setAttribute('height',274); $('pTop').setAttribute('y',sy-304);
  const A=$('arrows'); A.innerHTML='';
  const big=(t>24.4&&t<27.9);
  if((press>0&&press<1)||big) [330,390].forEach((x,i)=>{for(let k=0;k<2;k++){const ph=((t*(big?3:1.4)+k*.5+i*.25)%1), y=lerp(sy-350,sy-320,ph);
    el('path',{d:`M${x-9} ${y-9} l9 9 l9 -9`,stroke:big?'#e0605a':'#f1e6d6','stroke-width':big?5:3,opacity:Math.sin(Math.PI*ph)*.9},A)}});
  // drip + cup
  const dripOn=(press>0&&press<1)||(big&&press>=1&&false);
  const cupL=lerp(975,926,press);
  $('cupFill').setAttribute('y',cupL); $('cupFill').setAttribute('height',Math.max(0,978-cupL));
  $('drip').setAttribute('d',`M360 886 L360 ${cupL}`); $('drip').setAttribute('opacity',(press>0&&press<1)?1:0);
  const H=$('hiss'); H.innerHTML='';
  if(t>22.5&&t<24.2) for(let k=0;k<3;k++){const ph=((t*1.6+k/3)%1);el('path',{d:`M${300+k*60} ${860-ph*30} q8 -8 16 0 q8 8 16 0`,opacity:Math.sin(Math.PI*ph)*.7},H)}
  // warning
  const wk=prog(t,4.0,4.3)*(1-prog(t,4.8,5.1)) + prog(t,24.0,24.4)*(1-prog(t,27.9,28.2));
  $('warn').setAttribute('opacity',wk*(.6+.4*Math.sin(t*8)));
  $('badge').setAttribute('opacity',wk); $('badge').setAttribute('transform',`translate(210 640) scale(${.85+.15*Math.sin(t*8)}) translate(-210 -640)`);
  // steam
  const S=$('steam'); S.innerHTML='';
  const st=prog(t,14.8,15.6)*(1-prog(t,20.0,20.4)), st2=prog(t,24.0,24.8);
  if(st>0) for(let k=0;k<3;k++){const ph=((t*.5+k/3)%1), y0=555-ph*70;
    el('path',{d:`M${330+k*30} ${y0} c-12 -16 12 -28 0 -44`,opacity:st*.3*Math.sin(Math.PI*ph)},S)}
  if(st2>0) for(let k=0;k<2;k++){const ph=((t*.5+k/2)%1), y0=890-ph*70;
    el('path',{d:`M${330+k*40} ${y0} c-10 -14 10 -24 0 -38`,opacity:st2*.35*Math.sin(Math.PI*ph)},S)}
  // tiles
  const sec=Math.round(lerp(0,120,prog(t,12.3,23.9)));
  $('tv').textContent=Math.floor(sec/60)+':'+String(sec%60).padStart(2,'0');
  $('wv').textContent=Math.round(200*fill)+' مل';
}'''
cfg=dict(D=D,ch_out=8.1,chunks=chunks,defs=defs,scene_svg=scene,scene_js=scene_js,init_js='',
 header=['طرق التحضير','إيروبريس','قهوة نظيفة في دقيقتين','كيف تشتغل من الداخل'],
 chips=[('البن','15 غ'),('الماء','200 مل'),('الطحنة','متوسطة'),('الحرارة','80°')],
 tiles=['المؤقت','الماء'],
 PH=[[0,'قهوة نظيفة ← بس فيه غلطة!','#f0a347'],[4.7,'الفلتر ← ورقة مبلولة','#6f9fe0'],[8.1,'البن ← 15 غرام · متوسطة','#f0a347'],[12.1,'الماء ← 80° · حرّك 10 ثواني','#6f9fe0'],[16.2,'تابعني ← @your_handle','#f0a347'],[19.6,'ركّب المكبس ← اضغط بهدوء','#7fbf98'],[23.9,'الغلطة ← لا تضغط بقوة','#e0605a'],[28.0,'إيروبريس ← ولا فرنش برس؟','#f0a347']],
 LB=[['ورقة الفلتر','#c99a6a',[420,846],[600,854],'M420 846 H592','start',5.4,8.0],
     ['بن متوسط','#c99a6a',[418,830],[600,838],'M418 830 H592','start',9.6,12.0],
     ['ماي 80°','#6f9fe0',[418,700],[600,708],'M418 700 H592','start',13.2,16.0],
     ['المكبس','#f1e6d6',[428,540],[600,548],'M428 540 H592','start',21.0,24.0]])
build('.',cfg)
