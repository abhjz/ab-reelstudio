#!/usr/bin/env python3
"""build_quran.py <config.json>  ->  <out>/reel.html + <out>/recitation.wav

Config (all text and audio come from the Tarteel connector; never type verses by hand):
{
  "template": "sky" | "mushaf" | "moon",      # sky.html, mushaf.html, moon.html (a different look each reel)
  "theme": "sharh" | "duha",                   # sky only
  "sura": "<surah name>", "reciter": "<reciter name>",   # header text (moon: leave empty, give "sura" per item)
  "watermark": "",                             # empty = none
  "lead": 1.0,                                 # seconds of silence before the first verse
  "out": "reel-01",
  "items": [ {"text": "<Uthmani text>", "num": 0, "en": "<translation or empty>", "sura": "<moon only>", "audio": "path/to/verse.mp3"} ]
}
num 0 = Basmala (no verse number shown). Needs ffmpeg + numpy.
"""
import json, os, subprocess, sys, wave
import numpy as np

here = os.path.dirname(os.path.abspath(__file__))
cfg = json.load(open(sys.argv[1]))
out = cfg.get('out', 'reel'); os.makedirs(os.path.join(out, 'audio'), exist_ok=True)
lead = float(cfg.get('lead', 1.0))
kind = cfg.get('template', 'sky')
tpl_file = {'sky': 'sky.html', 'mushaf': 'mushaf.html', 'moon': 'moon.html'}[kind]

def run(*a): subprocess.run(list(a), check=True)
def dur(w): return float(subprocess.check_output(['ffprobe', '-v', 'error', '-show_entries', 'format=duration', '-of', 'csv=p=0', w]))

run('ffmpeg', '-v', 'error', '-y', '-f', 'lavfi', '-i', 'anullsrc=r=48000:cl=mono', '-t', str(lead), f'{out}/audio/silence.wav')
names, t, items = ['silence.wav'], lead, []
for i, it in enumerate(cfg['items']):
    w = f'{out}/audio/{i}.wav'
    run('ffmpeg', '-v', 'error', '-y', '-i', it['audio'], '-ar', '48000', '-ac', '1', w)
    row = dict(text=it['text'], num=it.get('num', i), en=it.get('en', ''), s=round(t, 3))
    if it.get('sura'): row['sura'] = it['sura']
    items.append(row); names.append(f'{i}.wav'); t += dur(w)
D = round(t + 1.8, 2)
open(f'{out}/audio/list.txt', 'w').write(''.join(f"file '{n}'\n" for n in names))
run('ffmpeg', '-v', 'error', '-y', '-f', 'concat', '-safe', '0', '-i', f'{out}/audio/list.txt', '-c', 'pcm_s16le', f'{out}/recitation.wav')

with wave.open(f'{out}/recitation.wav') as wf:
    a = np.frombuffer(wf.readframes(wf.getnframes()), dtype=np.int16).astype(np.float32) / 32768
hop = 48000 // 30
rms = [float(np.sqrt(np.mean(a[i:i + hop] ** 2))) for i in range(0, len(a), hop)]
mx = max(rms) or 1; env, v = [], 0
for r in rms:
    v = max(r / mx, v * 0.82); env.append(round(v, 3))
env += [0] * 90

data = dict(D=D, items=items, rms=env)
if kind == 'sky': data['theme'] = cfg.get('theme', 'sharh')
html = open(os.path.join(here, tpl_file), encoding='utf-8').read()
html = html.replace('__SURA__', cfg.get('sura', '')).replace('__REC__', cfg.get('reciter', '')) \
           .replace('__WM__', cfg.get('watermark', '')).replace('__DATA__', json.dumps(data, ensure_ascii=False))
open(f'{out}/reel.html', 'w', encoding='utf-8').write(html)
print('built', out, 'duration', D, 's;', len(items), 'items')
