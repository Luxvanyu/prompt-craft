#!/usr/bin/env python3
"""切块看图：把一张参考图切成九宫格 + 指定局部，各自放大到可辨认的尺寸。

看图这一步不能靠「一眼扫过整张图」，那只能拿到印象。要拿到事实，
必须一块一块地看，而且每次只问一个问题。

用法：
  python scripts/crop.py IMG.png --grid 3 --out ./crops
  python scripts/crop.py IMG.png --region hands,0.05,0.55,0.45,0.85 --region face,0.3,0.1,0.6,0.4
  python scripts/crop.py IMG.png --grid 3 --long 1100 --prefix ref1

--region 的名字, x0,y0,x1,y1 全部是画幅比例（0–1）。
--long 是输出长边的像素目标（默认 900），只会放大不会缩小。
--overlap 九宫格的块间重叠比例（默认 0.12），防止关键东西正好切在两块中间。
"""
import argparse
import os
import sys

from PIL import Image

def crop_and_save(im, box, out, name, long_side):
    c = im.crop(box)
    w, h = c.size
    scale = long_side / max(w, h)
    if scale > 1:
        c = c.resize((max(1, int(w * scale)), max(1, int(h * scale))), Image.LANCZOS)
    p = os.path.join(out, name + ".png")
    c.save(p)
    print(f"{name:22s} px={c.size[0]}x{c.size[1]}  box={box}  -> {p}")

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("image")
    ap.add_argument("--grid", type=int, default=0, help="N×N 九宫格")
    ap.add_argument("--region", action="append", default=[], help="name,x0,y0,x1,y1（比例）")
    ap.add_argument("--out", default="crops")
    ap.add_argument("--long", type=int, default=900)
    ap.add_argument("--overlap", type=float, default=0.12)
    ap.add_argument("--prefix", default="")
    a = ap.parse_args()

    im = Image.open(a.image)
    W, H = im.size
    os.makedirs(a.out, exist_ok=True)
    print(f"source {a.image}  {W}x{H}")

    if a.grid:
        n = a.grid
        for r in range(n):
            for c_ in range(n):
                x0 = max(0.0, (c_ / n) - a.overlap / n)
                x1 = min(1.0, ((c_ + 1) / n) + a.overlap / n)
                y0 = max(0.0, (r / n) - a.overlap / n)
                y1 = min(1.0, ((r + 1) / n) + a.overlap / n)
                box = (int(x0 * W), int(y0 * H), int(x1 * W), int(y1 * H))
                crop_and_save(im, box, a.out, f"{a.prefix}g{r}{c_}", a.long)

    for spec in a.region:
        parts = spec.split(",")
        if len(parts) != 5:
            sys.exit(f"bad --region: {spec}")
        name = parts[0]
        x0, y0, x1, y1 = (float(v) for v in parts[1:])
        box = (int(x0 * W), int(y0 * H), int(x1 * W), int(y1 * H))
        if box[2] <= box[0] or box[3] <= box[1]:
            sys.exit(f"empty region: {spec}")
        crop_and_save(im, box, a.out, f"{a.prefix}{name}", a.long)

if __name__ == "__main__":
    main()
