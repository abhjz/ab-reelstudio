#!/usr/bin/env python3
"""WCAG contrast checker.
  python3 contrast.py "#FFFFFF" "#062C30"        ratio + verdict for one pair
  python3 contrast.py --palette petrol-gaming    every useful text/background pair of a palette
  python3 contrast.py --list                     palette slugs
Verdict: >=4.5 body text OK (>=7 any text) | 3-4.5 large/bold headlines only | <3 shapes, glows, pills only."""
import json, sys, pathlib
HERE = pathlib.Path(__file__).resolve().parent.parent

def lin(c):
    c /= 255
    return c / 12.92 if c <= 0.03928 else ((c + 0.055) / 1.055) ** 2.4

def lum(h):
    h = h.lstrip('#')
    if len(h) != 6: raise ValueError('Use #RRGGBB: ' + h)
    r, g, b = (int(h[i:i + 2], 16) for i in (0, 2, 4))
    return 0.2126 * lin(r) + 0.7152 * lin(g) + 0.0722 * lin(b)

def ratio(a, b):
    la, lb = lum(a), lum(b)
    hi, lo = max(la, lb), min(la, lb)
    return (hi + 0.05) / (lo + 0.05)

def verdict(r):
    return 'any text' if r >= 7 else 'body text OK' if r >= 4.5 else 'large/bold headlines only' if r >= 3 else 'shapes/glows/pills only, NO text'

def palettes():
    return json.loads((HERE / 'palettes.json').read_text())['palettes']

def report(p):
    pairs = [('support text on base', p['support'], p['base']), ('accent text on base', p['accent'], p['base']),
             ('white text on base', '#FFFFFF', p['base']), ('near-black text on base', '#0A0A0A', p['base']),
             ('white text on accent pill', '#FFFFFF', p['accent']), ('near-black text on accent pill', '#0A0A0A', p['accent']),
             ('base text on accent pill', p['base'], p['accent']), ('base text on support panel', p['base'], p['support'])]
    out = [f"{p['name']}  60 {p['base']} · 30 {p['support']} · 10 {p['accent']}"]
    for label, fg, bg in pairs:
        r = ratio(fg, bg); out.append(f"  {label:32} {fg} on {bg}  {r:5.2f}:1  {verdict(r)}")
    return '\n'.join(out)

if __name__ == '__main__':
    a = sys.argv[1:]
    if a == ['--list']: print('\n'.join(p['slug'] for p in palettes()))
    elif len(a) == 2 and a[0] == '--palette':
        m = [p for p in palettes() if p['slug'] == a[1]]
        if not m: sys.exit('Unknown palette. Use --list')
        print(report(m[0]))
    elif len(a) == 2:
        r = ratio(a[0], a[1]); print(f'{r:.2f}:1  {verdict(r)}')
    else: sys.exit(__doc__)
