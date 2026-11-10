#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""MOSS 复刻探针：读一张参考图，输出明度/饱和度/色彩/梯度统计 + 16x11 hex 网格。

用法:
    python probe.py <图片路径>
    python probe.py <图片路径> --patch 0.40,0.28,0.52,0.42@dress

输出段落说明:
    size            宽高
    mean / med      平均与中位明度
    dark/mid/bright dark=L<0.15  mid=0.15..0.75  bright=L>0.75
    nw              近白 L>0.95 占比（<0.01 就写「没有一处真正的白」）
    p1 / p99        1% 与 99% 分位（p1>0.13 说明全图无真黑）
    grid 6x6        区域亮度矩阵，用来定「唯一亮场 / 最暗块」在哪
    rgb             全图平均 RGB
    sat/lit/shadow  全图 / 亮部 top20% / 暗部 bottom25% 的平均饱和度
                    （lit>shadow = 硬太阳正午；shadow>lit = 暗处更浓，如皮革、潮湿）
    soft            梯度 >0.08 之外的占比，即 1 - strong（与 strong 互补，和为 1）
    strong          梯度 >0.08 的像素占比（边缘密度）
    flat            梯度 <0.02 的像素占比（>0.55 大范围 bloom/雾，<0.35 硬光硬边）
    hex 16x11       粗色彩网格，直接读主色，避免「天蓝/青灰」误判
"""
import sys
import numpy as np
from PIL import Image


def probe(path, patches=None):
    im = Image.open(path).convert('RGB')
    W, H = im.size
    a = np.asarray(im).astype(np.float32) / 255.
    lum = 0.2126 * a[..., 0] + 0.7152 * a[..., 1] + 0.0722 * a[..., 2]

    print('size', W, H)
    print('mean %.3f med %.3f' % (lum.mean(), np.median(lum)))
    print('dark %.3f mid %.3f bright %.3f nw %.4f p1 %.3f p99 %.3f' % (
        (lum < .15).mean(), ((lum >= .15) & (lum <= .75)).mean(),
        (lum > .75).mean(), (lum > .95).mean(),
        np.percentile(lum, 1), np.percentile(lum, 99)))

    print('grid 6x6:')
    for i in range(6):
        row = [round(float(lum[i * H // 6:(i + 1) * H // 6,
                              j * W // 6:(j + 1) * W // 6].mean()), 2)
               for j in range(6)]
        print('  ', row)

    print('rgb %.3f %.3f %.3f' % tuple(a.reshape(-1, 3).mean(0)))

    mx = a.max(2)
    mn = a.min(2)
    sat = np.where(mx > 0, (mx - mn) / np.maximum(mx, 1e-6), 0)
    print('sat %.3f lit %.3f shadow %.3f' % (
        sat.mean(),
        sat[lum > np.percentile(lum, 80)].mean(),
        sat[lum < np.percentile(lum, 25)].mean()))

    gy, gx = np.gradient(lum)
    gm = np.hypot(gx, gy)
    # flat = 大范围平缓占比（雾/bloom 诊断，独立阈值）；soft = 1 - strong（与 strong 互补）
    _strong = (gm > .08).mean()
    print('soft %.3f strong %.3f' % (1.0 - _strong, _strong))
    print('flat %.3f' % (gm < .02).mean())
    print('hex 16x11:')
    sm = im.resize((16, 11), Image.BOX)
    for row in np.asarray(sm).astype(np.uint8):
        print('  ' + ' '.join('%02x%02x%02x' % tuple(px) for px in row))

    for name, (x0, y0, x1, y1) in (patches or {}).items():
        p = a[int(H * y0):int(H * y1), int(W * x0):int(W * x1)].reshape(-1, 3)
        m = p.mean(0)
        pmx = p.max(1)
        pmn = p.min(1)
        s = ((pmx - pmn) / np.maximum(pmx, 1e-6)).mean()
        print('%-16s rgb %.2f %.2f %.2f  sat %.2f  lum %.2f' % (
            name, m[0], m[1], m[2], s,
            0.2126 * m[0] + 0.7152 * m[1] + 0.0722 * m[2]))


if __name__ == '__main__':
    if len(sys.argv) < 2 or sys.argv[1] in ('-h', '--help'):
        print(__doc__)
        sys.exit(0)
    patches = {}
    args = sys.argv[2:]
    for i, arg in enumerate(args):
        spec = None
        if arg.startswith('--patch='):
            spec = arg.split('=', 1)[1]
        elif arg == '--patch' and i + 1 < len(args):
            spec = args[i + 1]
        if spec:
            box, name = spec.split('@') if '@' in spec else (spec, 'patch')
            x0, y0, x1, y1 = [float(v) for v in box.split(',')]
            patches[name] = (x0, y0, x1, y1)
    probe(sys.argv[1], patches)
