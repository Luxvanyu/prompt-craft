# -*- coding: utf-8 -*-
"""verify.py — 参考图 vs 出图 的逐项数值对比与色差热图。

用法：
    python scripts/verify.py 参考图.png 出图.png --out-dir . --tag 名字
    python scripts/verify.py 参考图.png 出图.png --no-map     # 不出热图，只打表

输出四块：
    1. 逐项对照表（参考 / 出图 / 差值）
    2. 6x6 明度矩阵三张并排（参考 | 出图 | 差值）
    3. 诊断清单，按 [严重]/[明显]/[轻微]/[定位] 排序，每条带「该改哪句话」
    4. 三联对比图 _verify_<tag>.jpg（参考 | 出图 | 色差热图）
"""
import argparse
import io
import os
import sys
import warnings

try:
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
except Exception:
    pass

# Pillow 12+ 对 Image.getdata() 发 DeprecationWarning（Pillow 14 移除），
# 这里仍在用它的旧接口语义，屏蔽掉以免刷屏干扰诊断输出
warnings.filterwarnings("ignore", category=DeprecationWarning)

from PIL import Image, ImageChops, ImageDraw, ImageFilter, ImageStat

try:
    import numpy as _np
except ImportError:  # numpy 缺失时降级：用 PIL 差分近似 probe.py 的梯度阈值
    _np = None

# ---------------------------------------------------------------- 基础度量
KEYS = ["mean", "med", "dark", "mid", "bright", "nw",
        "p1", "p99", "sat", "lit", "shadow", "soft", "strong",
        "hue", "r", "g", "b"]


def load_rgb(path, long_side=760):
    im = Image.open(path).convert("RGB")
    w, h = im.size
    if max(w, h) > long_side:
        k = long_side / max(w, h)
        im = im.resize((max(1, int(w * k)), max(1, int(h * k))), Image.LANCZOS)
    return im


def _lum(im):
    """亮度：与 probe.py 同一套 RGB 加权系数，不用 PIL 的 convert("L")。

    PIL 的 L 转换用 ITU-R 601（0.299/0.587/0.114），probe.py 用 ITU-R 709
    （0.2126/0.7152/0.0722）。纯灰图上一样，有彩色区域会差到 0.016，
    足以让 flat / strong 这类阈值判据差出 0.02，导致两个脚本对同一张图报不同数。
    """
    if _np is not None:
        a = _np.asarray(im.convert("RGB"), dtype=_np.float32) / 255.0
        lum = 0.2126 * a[..., 0] + 0.7152 * a[..., 1] + 0.0722 * a[..., 2]
        return Image.fromarray((lum * 255.0 + 0.5).astype(_np.uint8), mode="L")
    return im.convert("L")


def measure(im):
    """返回一整套指标。定义与 probe.py 完全一致，两边可以互相对照。"""
    L = _lum(im)
    px = list(L.getdata())
    n = len(px)
    hist = L.histogram()
    cum = 0
    med = 0.0
    for i, c in enumerate(hist):
        if not c:
            continue
        if (cum + c) * 2 >= n:
            med = i / 255.0
            break
        cum += c

    mean = ImageStat.Stat(L).mean[0] / 255.0
    dark = sum(hist[:64]) / n
    mid = sum(hist[64:192]) / n
    bright = sum(hist[192:]) / n
    near_white = sum(hist[240:]) / n
    spx = sorted(px)
    p1 = spx[int(n * 0.01)] / 255.0
    p99 = spx[int(n * 0.99)] / 255.0

    # 6x6 明度矩阵
    grid = []
    W, H = L.size
    for gy in range(6):
        row = []
        for gx in range(6):
            bx0, bx1 = int(W * gx / 6), int(W * (gx + 1) / 6)
            by0, by1 = int(H * gy / 6), int(H * (gy + 1) / 6)
            box = L.crop((bx0, by0, max(bx0 + 1, bx1), max(by0 + 1, by1)))
            row.append(ImageStat.Stat(box).mean[0] / 255.0)
        grid.append(row)

    # 饱和度
    hsv = im.convert("HSV")
    sat = ImageStat.Stat(hsv.split()[1]).mean[0] / 255.0
    rgb = [c / 255.0 for c in ImageStat.Stat(im).mean]

    # 亮部 / 暗部各自的饱和度（G9 方向判据）
    S = hsv.split()[1]
    litpix, shadpix = [], []
    for (lv, sv) in zip(px, S.getdata()):
        if lv >= 204:
            litpix.append(sv)
        elif lv <= 51:
            shadpix.append(sv)
    lit = (sum(litpix) / len(litpix) / 255.0) if litpix else 0.0
    shadow = (sum(shadpix) / len(shadpix) / 255.0) if shadpix else 0.0

    # 软 / 硬：局部梯度幅值占比（与 probe.py 完全同口径：np.gradient + hypot）
    # strong = 边缘像素占比（梯度 > 0.08）；soft = 1 - strong，保持两者互补
    if _np is not None:
        # 直接对 float 亮度求梯度，不做 uint8 量化——
        # 量化会把 <0.02 的微小台阶抬到 1/255≈0.0039 以上，让 flat 系统性偏低（实测差 0.012）
        _a = _np.asarray(im.convert("RGB"), dtype=_np.float32) / 255.0
        _grad_arr = 0.2126 * _a[..., 0] + 0.7152 * _a[..., 1] + 0.0722 * _a[..., 2]
        _gy, _gx = _np.gradient(_grad_arr)
        g_mag = _np.hypot(_gx, _gy)
        strong = float((g_mag > 0.08).mean())
        flat = float((g_mag < 0.02).mean())
    else:
        # numpy 缺失：用 3x3 前向差分近似，阈值按同一归一化口径
        W, H = L.size
        small = L.resize((W, H), Image.NEAREST)
        edges = ImageChops.difference(small, small.filter(ImageFilter.GaussianBlur(1)))
        e_px = list(edges.getdata())
        strong = sum(1 for v in e_px if v > 0.08 * 255) / len(e_px)
        flat = sum(1 for v in e_px if v < 0.02 * 255) / len(e_px)
    soft = 1.0 - strong

    # 主色相：把有色像素按 30 度分桶，取最多的桶
    Hc = hsv.split()[0]
    buckets = [0] * 12
    for (hv, sv, lv) in zip(Hc.getdata(), S.getdata(), px):
        if sv > 40 and 26 < lv < 230:
            buckets[min(11, hv * 12 // 256)] += 1
    hue = buckets.index(max(buckets)) * 30 if sum(buckets) else -1

    return {
        "mean": mean, "med": med, "dark": dark, "mid": mid, "bright": bright,
        "nw": near_white, "p1": p1, "p99": p99, "sat": sat,
        "lit": lit, "shadow": shadow, "soft": soft, "strong": strong, "flat": flat,
        "hue": hue, "r": rgb[0], "g": rgb[1], "b": rgb[2],
        "grid": grid, "size": im.size, "im": im, "L": L,
    }


def ImageFilterGaussian(r):
    """轻量高斯（不额外依赖 scipy），用于估计高频能量。"""
    from PIL import ImageFilter
    return ImageFilter.GaussianBlur(r)


# ---------------------------------------------------------------- 色差热图
def diff_map(a, b):
    """把两张图拉到同尺寸，返回绝对色差热图（越红差越多，越黑越像）。

    归一化用**固定标尺**（每像素通道差 0-255 映射到 0-1），不做逐图 min-max，
    否则两张差不多的图也会被拉成满屏红。
    """
    if a.size != b.size:
        b = b.resize(a.size, Image.LANCZOS)
    d = ImageChops.difference(a, b).convert("L")
    w, h = d.size
    src = d.load()
    out = Image.new("RGB", (w, h))
    dst = out.load()
    for y in range(h):
        for x in range(w):
            v = min(1.0, src[x, y] / 160.0) ** 0.7   # 160 以上算「差透」，做温和提亮
            dst[x, y] = (int(255 * v), int(90 * v * (1 - v)), int(40 * (1 - v)))
    return out


def triptych(ref_im, out_im, heat):
    h = min(ref_im.size[1], out_im.size[1], heat.size[1], 700)
    def fit(im):
        k = h / im.size[1]
        return im.resize((max(1, int(im.size[0] * k)), h), Image.LANCZOS)
    a, b, c = fit(ref_im), fit(out_im), fit(heat)
    gap = 8
    canvas = Image.new("RGB", (a.size[0] + b.size[0] + c.size[0] + gap * 2, h + 24), (16, 16, 16))
    canvas.paste(a, (0, 24))
    canvas.paste(b, (a.size[0] + gap, 24))
    canvas.paste(c, (a.size[0] + b.size[0] + gap * 2, 24))
    d = ImageDraw.Draw(canvas)
    d.text((4, 6), "REF", fill=(200, 200, 200))
    d.text((a.size[0] + gap + 4, 6), "OUT", fill=(200, 200, 200))
    d.text((a.size[0] + b.size[0] + gap * 2 + 4, 6), "DIFF (redder = worse)", fill=(200, 200, 200))
    return canvas


# ---------------------------------------------------------------- 诊断
def diagnose(ref, out):
    """返回 [(级别, 文案, 该改哪句话)]，级别用 0 最严重。"""
    rows = []
    band = lambda m: max([("dark", m["dark"]), ("mid", m["mid"]), ("bright", m["bright"])],
                         key=lambda x: x[1])
    rb, ob = band(ref), band(out)
    if rb[0] != ob[0]:
        rows.append((0, "主导明度档不同：参考 %s %.0f%%，出图 %s %.0f%%"
                     % (rb[0], rb[1] * 100, ob[0], ob[1] * 100),
                     "先改第一句的明度定调（Low key / middle values / high key），"
                     "再按 G4 给黑锚点或给最亮载体"))
    if (ref["lit"] - ref["shadow"]) * (out["lit"] - out["shadow"]) < 0:
        rows.append((0, "lit/shadow 方向反转：参考 lit %.3f vs shadow %.3f，出图 lit %.3f vs shadow %.3f"
                     % (ref["lit"], ref["shadow"], out["lit"], out["shadow"]),
                     "G9：颜色必须落在被照亮的大面积上；把色词从暗部道具挪到被照亮的墙面/地面"))
    if abs(ref["mean"] - out["mean"]) > 0.05:
        rows.append((1, "整体明度偏了 |Δmean| = %.3f（参考 %.3f，出图 %.3f）"
                     % (abs(ref["mean"] - out["mean"]), ref["mean"], out["mean"]),
                     "改明度三档的面积分配，不要改形容词"))
    if abs(ref["soft"] - out["soft"]) > 0.10:
        rows.append((1, "软硬不对 |Δsoft| = %.3f（参考 %.3f，出图 %.3f）"
                     % (abs(ref["soft"] - out["soft"]), ref["soft"], out["soft"]),
                     "G6：硬光要写边缘硬度，软光要写衰减半径；两边只有一句能改"))
    if ref["nw"] < 0.01 and out["nw"] > 0.03:
        rows.append((1, "出图过曝出纯白 %.1f%%（参考只有 %.1f%%）"
                     % (out["nw"] * 100, ref["nw"] * 100),
                     "给最亮载体加一句 stopping a step short of blowing out"))
    if ref["p1"] > 0.13 and out["p1"] < 0.08:
        rows.append((1, "出图出现真黑 p1 = %.3f（参考 %.3f）" % (out["p1"], ref["p1"]),
                     "G4 反向：把「没有任何地方是纯黑」明确写出来，或把暗部抬到有结构的深灰"))
    # 最亮格位移
    def brightest(grid):
        best, pos = -1, (0, 0)
        for y in range(6):
            for x in range(6):
                if grid[y][x] > best:
                    best, pos = grid[y][x], (x, y)
        return pos, best
    rb_pos, rb_v = brightest(ref["grid"])
    ob_pos, ob_v = brightest(out["grid"])
    if abs(rb_pos[0] - ob_pos[0]) + abs(rb_pos[1] - ob_pos[1]) >= 2:
        rows.append((2, "最亮格位置偏了：参考列%d行%d，出图列%d行%d"
                     % (rb_pos[0], rb_pos[1], ob_pos[0], ob_pos[1]),
                     "光落的方位写错了：改光源方向那一句（from the left / behind / overhead）"))
    if ref["hue"] >= 0 and out["hue"] >= 0 and abs(ref["hue"] - out["hue"]) > 30:
        rows.append((2, "主色相偏了 %d°（参考 %d°，出图 %d°）"
                     % (abs(ref["hue"] - out["hue"]), ref["hue"], out["hue"]),
                     "换一个同族但更基础的颜色名，或后退到单色系（G5）"))
    for k in ("sat",):
        if abs(ref[k] - out[k]) > 0.06:
            rows.append((2, "饱和度差 %.3f（参考 %.3f，出图 %.3f）"
                         % (abs(ref[k] - out[k]), ref[k], out[k]),
                         "色相词数量与落点：至少三个有色相的东西，写在大面积上"))
    # 16x11 色块：找最大差格
    return sorted(rows, key=lambda r: r[0])


LEVEL = {0: "[严重]", 1: "[明显]", 2: "[轻微]", 3: "[定位]"}


def fmt_table(ref, out):
    lines = ["%-8s %8s %8s %8s" % ("指标", "参考", "出图", "差值")]
    for k in ("mean", "med", "dark", "mid", "bright", "nw", "p1", "p99",
              "sat", "lit", "shadow", "soft", "strong", "flat"):
        lines.append("%-8s %8.3f %8.3f %+8.3f" % (k, ref[k], out[k], out[k] - ref[k]))
    for k in ("hue", "r", "g", "b"):
        if isinstance(ref[k], int) and isinstance(out[k], int):
            lines.append("%-8s %8d %8d %+8d" % (k, ref[k], out[k], out[k] - ref[k]))
        else:
            lines.append("%-8s %8.3f %8.3f %+8.3f" % (k, ref[k], out[k], out[k] - ref[k]))
    return "\n".join(lines)


def fmt_grid(ref, out):
    out_lines = []
    for gy in range(6):
        a = " ".join("%.2f" % v for v in ref["grid"][gy])
        b = " ".join("%.2f" % v for v in out["grid"][gy])
        d = " ".join("%+.2f" % (out["grid"][gy][gx] - ref["grid"][gy][gx]) for gx in range(6))
        out_lines.append("  R %s   |   O %s   |   D %s" % (a, b, d))
    return "\n".join(out_lines)


def main():
    ap = argparse.ArgumentParser(description="参考图 / 出图 逐项对比")
    ap.add_argument("ref", help="参考图")
    ap.add_argument("out", help="出图")
    ap.add_argument("--out-dir", default=".", help="三联对比图输出目录")
    ap.add_argument("--tag", default="check", help="三联图文件名后缀")
    ap.add_argument("--long-side", type=int, default=760, help="长边缩放基准（默认 760，与 probe.py 一致）")
    ap.add_argument("--no-map", action="store_true", help="不出色差热图")
    a = ap.parse_args()

    ref_im, out_im = load_rgb(a.ref, a.long_side), load_rgb(a.out, a.long_side)
    ref, out = measure(ref_im), measure(out_im)

    print("%s  vs  %s" % (a.ref, a.out))
    print("尺寸：参考 %dx%d，出图 %dx%d" % (ref["size"] + out["size"]))
    print()
    print("== 逐项对照 ==")
    print(fmt_table(ref, out))
    print()
    print("== 6x6 明度矩阵（R 参考 / O 出图 / D 差值）==")
    print(fmt_grid(ref, out))
    print()
    print("== 诊断清单 ==")
    rows = diagnose(ref, out)
    if not rows:
        print("  [通过] 六类判据全部落在容差内")
    for lv, msg, fix in rows:
        print("  %s %s" % (LEVEL[lv], msg))
        print("        → %s" % fix)

    if not a.no_map:
        heat = diff_map(Image.open(a.ref).convert("RGB"), Image.open(a.out).convert("RGB"))
        trip = triptych(Image.open(a.ref).convert("RGB"),
                        Image.open(a.out).convert("RGB"), heat)
        os.makedirs(a.out_dir, exist_ok=True)
        p = os.path.join(a.out_dir, "_verify_%s.jpg" % a.tag)
        trip.save(p, quality=88)
        print()
        print("三联对比图：%s" % p)

    severe = [r for r in rows if r[0] == 0]
    print()
    print("结论：%s" % ("不通过（%d 项严重）" % len(severe) if severe else "通过"))
    return 1 if severe else 0


if __name__ == "__main__":
    sys.exit(main())
