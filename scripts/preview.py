# -*- coding: utf-8 -*-
"""构图预览：把 abs/xyxy 草稿的 bbox 画成方块，用来在出图前「看见」排版。
用法：
  python preview.py draft.json                 # 只画方框
  python preview.py draft.json --out p.png
  python preview.py draft.json --img out.png   # 叠在真实出图上
"""
import json, sys, argparse
from PIL import Image, ImageDraw, ImageFont

COLORS = [(255, 90, 90), (90, 160, 255), (255, 200, 60), (120, 220, 120),
          (220, 120, 255), (60, 220, 220), (255, 140, 60), (200, 200, 200)]


def fmt(it, i):
    lab = it.get('label', '?')
    cap = (it.get('caption') or '').split('.')[0]
    cap = cap[:34]
    return '%d %s %s' % (i, lab[:4], cap)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('draft')
    ap.add_argument('--out', default=None)
    ap.add_argument('--img', default=None)
    ap.add_argument('--maxw', type=int, default=760)
    a = ap.parse_args()

    d = json.load(open(a.draft, encoding='utf-8'))
    W, H = int(d['width']), int(d['height'])
    base = Image.open(a.img).convert('RGB').resize((W, H)) if a.img else Image.new('RGB', (W, H), (46, 46, 50))
    ov = Image.new('RGBA', (W, H), (0, 0, 0, 0))
    dr = ImageDraw.Draw(ov)
    size = max(12, W // 90)
    font = ImageFont.load_default()
    for cand in ('C:/Windows/Fonts/consola.ttf',
                 '/System/Library/Fonts/Menlo.ttc',
                 '/usr/share/fonts/truetype/dejavu/DejaVuSansMono.ttf',
                 '/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf'):
        try:
            font = ImageFont.truetype(cand, size)
            break
        except Exception:
            continue

    for i, it in enumerate(d.get('items', [])):
        b = it.get('bbox') or [0, 0, 0, 0]
        x1, y1, x2, y2 = b
        if x2 < x1:
            x1, x2 = x2, x1
        if y2 < y1:
            y1, y2 = y2, y1
        c = COLORS[i % len(COLORS)]
        dr.rectangle([x1, y1, x2, y2], outline=c + (255,), width=max(2, W // 400))
        # 面积占比
        pct = 100.0 * (x2 - x1) * (y2 - y1) / (W * H)
        tag = '%s  %.0f%%  %dx%d' % (fmt(it, i), pct, x2 - x1, y2 - y1)
        tw = dr.textlength(tag, font=font)
        ty = max(0, y1 - (max(12, W // 90) + 6))
        dr.rectangle([x1, ty, x1 + tw + 6, ty + max(12, W // 90) + 6], fill=(0, 0, 0, 170))
        dr.text((x1 + 3, ty + 2), tag, font=font, fill=c + (255,))
        # 中心点与中线偏移
        cx = (x1 + x2) / 2.0
        off = (cx - W / 2.0) / W
        dr.line([cx, y1 - 4, cx, y1 + 16], fill=c + (255,), width=2)
        if abs(off) > 0.001:
            dr.text((cx + 4, y1 + 2), '%+.2f' % off, font=font, fill=c + (255,))

    out = Image.alpha_composite(base.convert('RGBA'), ov).convert('RGB')
    # 中线
    dm = ImageDraw.Draw(out)
    dm.line([W / 2, 0, W / 2, H], fill=(255, 255, 255), width=1)
    dm.line([0, H / 2, W, H / 2], fill=(120, 120, 120), width=1)
    # 三分线
    for f in (1 / 3.0, 2 / 3.0):
        dm.line([W * f, 0, W * f, H], fill=(90, 90, 90), width=1)
        dm.line([0, H * f, W, H * f], fill=(90, 90, 90), width=1)

    if a.maxw and W > a.maxw:
        out = out.resize((a.maxw, int(a.maxw * H / W)), Image.LANCZOS)
    p = a.out or (a.draft.rsplit('.', 1)[0] + ('-on.png' if a.img else '-layout.png'))
    out.save(p)
    print(p)


if __name__ == '__main__':
    main()
