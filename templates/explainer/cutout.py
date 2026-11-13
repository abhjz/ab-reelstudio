"""White-background cutout for Gemini object images.
usage: python3 cutout.py raw/in.jpg out.png [--size 1024]
Flood-fills near-white pixels connected to the image border, feathers the edge,
crops to the object. Works because prompts ask for a pure #FFFFFF background."""
import sys
import numpy as np
from PIL import Image, ImageFilter
from collections import deque

src, dst = sys.argv[1], sys.argv[2]
size = int(sys.argv[sys.argv.index('--size') + 1]) if '--size' in sys.argv else 1024
im = Image.open(src).convert('RGB')
im.thumbnail((size, size), Image.LANCZOS)
a = np.asarray(im).astype(np.int16)
h, w, _ = a.shape
# "white-ish": bright and low saturation
mx, mn = a.max(2), a.min(2)
thr = int(sys.argv[sys.argv.index("--thr") + 1]) if "--thr" in sys.argv else 228
bg_like = (mn > thr) & (mx - mn < 18)
mask = np.zeros((h, w), bool)
q = deque()
for x in range(w):
    for y in (0, h - 1):
        if bg_like[y, x] and not mask[y, x]: mask[y, x] = True; q.append((y, x))
for y in range(h):
    for x in (0, w - 1):
        if bg_like[y, x] and not mask[y, x]: mask[y, x] = True; q.append((y, x))
while q:
    y, x = q.popleft()
    for dy, dx in ((1, 0), (-1, 0), (0, 1), (0, -1)):
        ny, nx = y + dy, x + dx
        if 0 <= ny < h and 0 <= nx < w and not mask[ny, nx] and bg_like[ny, nx]:
            mask[ny, nx] = True; q.append((ny, nx))
alpha = Image.fromarray(np.where(mask, 0, 255).astype(np.uint8))
alpha = alpha.filter(ImageFilter.MinFilter(3)).filter(ImageFilter.GaussianBlur(1.2))
out = im.convert('RGBA'); out.putalpha(alpha)
bbox = alpha.point(lambda v: 255 if v > 10 else 0).getbbox()
out = out.crop(bbox)
out.save(dst)
print(dst, out.size)
