#!/usr/bin/env python3
"""MOSS Layout 框对齐：16px 吸附 + 背景到前景排序 + 主色采样 + 叠框核验。

做法参考 liangci-ai/MOSS-YXBOX 的几条经验（GRID=16、MIN_BOX=16、
背景到前景排列、palette 锚定）。GRID=16 是 MOSS latent 的硬约束；
MIN_BOX=16 与层级顺序是经验值，换个模型要重新标定。

用法:
  # 1. 按参考图比例算 16 倍数分辨率（默认基准面积 1536×1344 ≈ 2.06M）
  python3 scripts/align_bboxes.py dims <ref_image> [--area 2064384]

  # 2. 参考图叠 10% 坐标网格，照格读框，不靠目测
  python3 scripts/align_bboxes.py grid <ref_image> -o grid_preview.png

  # 3. 吸附到 16px、按背景到前景重排、采样主色、画叠框
  python3 scripts/align_bboxes.py verify <draft.json> --ref <ref_image> \
      --out-draft <aligned_draft.json> --out-overlay <overlay.png> \
      [--extract-palette] [--bg-text "KIVOTOS,山海經"]

只处理 Layout（有 bbox 的框）。Caption 草稿没有框可对齐，会直接报错退出。
`z_layer` 是本工具的工作标记（"bg"/"fg"），对齐时会被剥掉；写进编译稿
compile_prompt.py 会当成未知字段。
"""
import argparse
import json
import math
import sys
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont

for _s in (sys.stdout, sys.stderr):
    try:
        _s.reconfigure(encoding="utf-8")
    except Exception:
        pass

GRID = 16
MIN_BOX = 16
# 默认基准面积：1536×1024 = 1.44:1，正好对上最常用的 3:2 档。
# 原先用 1152²（1.33M）算出来的结果普遍偏小一档。
DEFAULT_AREA = 1536 * 1024
# 长边上限：MOSS 宽银幕档的经验上限，超了按比例压回来再吸附。
MAX_SIDE = 1664

COLORS = {
    "character": (255, 64, 96),
    "object": (48, 180, 255),
    "text": (255, 200, 32),
}

FONT_CANDIDATES = (
    "C:/Windows/Fonts/msyh.ttc",
    "C:/Windows/Fonts/msyhbd.ttc",
    "C:/Windows/Fonts/simhei.ttf",
    "C:/Windows/Fonts/consola.ttf",
    "/System/Library/Fonts/PingFang.ttc",
    "/usr/share/fonts/opentype/noto/NotoSansCJK-Regular.ttc",
    "/usr/share/fonts/truetype/dejavu/DejaVuSansMono.ttf",
)


def _font(size):
    """返回 (font, 能否渲染非 ASCII)。中文字要专门找字体，默认位图字体只有 ASCII。"""
    for cand in FONT_CANDIDATES:
        try:
            return ImageFont.truetype(cand, size), not cand.endswith("consola.ttf")
        except Exception:
            continue
    return ImageFont.load_default(), False


def dims_for_ratio(ratio, target_area=DEFAULT_AREA, max_side=MAX_SIDE):
    """按宽高比算最贴近的 16 倍数尺寸，长边不超过 max_side。"""
    tw = max(512, int(round(math.sqrt(target_area * ratio) / GRID)) * GRID)
    th = max(512, int(round(math.sqrt(target_area / ratio) / GRID)) * GRID)
    clamped = False
    if max(tw, th) > max_side:
        # 宽银幕比例按面积算出会顶穿长边上限（21:9 会到 2192 宽），按比例压回来
        clamped = True
        scale = max_side / float(max(tw, th))
        tw = max(512, int(round(tw * scale / GRID)) * GRID)
        th = max(512, int(round(th * scale / GRID)) * GRID)
        if max(tw, th) > max_side:
            if tw >= th:
                tw = (max_side // GRID) * GRID
            else:
                th = (max_side // GRID) * GRID
    return (tw, th), clamped


def compute_dims(ref_path, target_area=DEFAULT_AREA, max_side=MAX_SIDE):
    with Image.open(ref_path) as im:
        w, h = im.size
    (tw, th), clamped = dims_for_ratio(w / float(h), target_area, max_side)
    return (w, h), (tw, th), clamped


def snap16(val, lo, hi):
    snapped = int(round(val / GRID)) * GRID
    return max(lo, min(hi, snapped))


def snap_bbox(box, w, h):
    x1, y1, x2, y2 = box
    sx1 = snap16(x1, 0, w - MIN_BOX)
    sy1 = snap16(y1, 0, h - MIN_BOX)
    sx2 = snap16(x2, sx1 + MIN_BOX, w)
    sy2 = snap16(y2, sy1 + MIN_BOX, h)
    return [sx1, sy1, sx2, sy2], max(abs(sx1 - x1), abs(sy1 - y1), abs(sx2 - x2), abs(sy2 - y2))


def extract_hex_palette(im, box, w, h, k=3, merge=28):
    """框内采样 k 个 #RRGGBB。

    按簇的像素数从多到少排（quantize 的输出顺序不按面积，直接取前几个
    会把 10% 的小色放到第一位），并合并 ΔRGB < merge 的近重复色——
    否则一个灰面会占掉三个槽位。
    """
    iw, ih = im.size
    rx1 = max(0, min(iw - 1, int(round(box[0] / w * iw))))
    ry1 = max(0, min(ih - 1, int(round(box[1] / h * ih))))
    rx2 = max(rx1 + 1, min(iw, int(round(box[2] / w * iw))))
    ry2 = max(ry1 + 1, min(ih, int(round(box[3] / h * ih))))
    crop = im.crop((rx1, ry1, rx2, ry2)).convert("RGB")
    crop.thumbnail((96, 96))
    if crop.width < 1 or crop.height < 1:
        return []
    pal_im = crop.quantize(colors=max(k * 2, 6), method=Image.Quantize.MEDIANCUT)
    counts = pal_im.getcolors(maxcolors=1 << 16) or []
    pal = pal_im.getpalette() or []
    entries = []
    for count, idx in counts:
        r, g, b = pal[idx * 3 : idx * 3 + 3]
        entries.append((count, (r, g, b)))
    entries.sort(key=lambda e: -e[0])
    total = float(sum(c for c, _ in entries)) or 1.0
    out, kept = [], []
    for count, rgb in entries:
        if count / total < 0.015:
            continue          # 抗锯齿过渡色，不是主色
        if all(sum((rgb[i] - s[i]) ** 2 for i in range(3)) > merge ** 2 for s in kept):
            kept.append(rgb)
            out.append("#%02X%02X%02X" % rgb)
        if len(out) >= k:
            break
    return out


def draw_grid(ref_path, out_path):
    im = Image.open(ref_path).convert("RGB")
    w, h = im.size
    draw = ImageDraw.Draw(im)
    font, cjk = _font(max(12, min(w, h) // 40))
    for pct in range(10, 100, 10):
        x = int(round(w * pct / 100.0))
        y = int(round(h * pct / 100.0))
        col = (255, 255, 0) if pct == 50 else (0, 255, 255)
        draw.line([(x, 0), (x, h)], fill=col, width=2 if pct == 50 else 1)
        draw.line([(0, y), (w, y)], fill=col, width=2 if pct == 50 else 1)
        draw.text((x + 3, 4), ".%d" % (pct // 10), fill=(255, 255, 0), font=font)
        draw.text((4, y + 3), ".%d" % (pct // 10), fill=(255, 255, 0), font=font)
    im.save(out_path)
    (ow, oh), (tw, th), clamped = compute_dims(ref_path)
    print("Saved grid preview: %s (orig=%dx%d -> target=%dx%d%s)"
          % (out_path, ow, oh, tw, th, " [clamped to %d]" % MAX_SIDE if clamped else ""))


def _guard_layout(draft, path):
    """不是 Layout 就别继续跑；给中文指引而不是 KeyError。"""
    if isinstance(draft, dict) and "items" in draft and "width" in draft and "height" in draft:
        return
    keys = ", ".join(sorted(draft.keys())) if isinstance(draft, dict) else type(draft).__name__
    raise SystemExit(
        "错误：%s 不是 Layout 草稿（现有顶层键：%s）。\n"
        "align_bboxes 只对齐有 bbox 的框，Caption 草稿没有框可对。两条路：\n"
        "  1) 反推默认出 Layout：按 references/reverse-engineer.md §三 分层出框，再回来对齐；\n"
        "  2) 这一张就用 Caption：跳过本步，直接 lint.py 检查文本。\n"
        "示例：{\"width\": 1536, \"height\": 1024, \"bbox_coord_space\": \"abs\", "
        "\"bbox_format\": \"xyxy\", \"summary\": {\"caption\": \"...\"}, "
        "\"items\": [{\"label\": \"character\", \"caption\": \"...\", \"bbox\": [0, 0, 512, 1024]}]}"
        % (Path(path).name, keys)
    )


def verify_and_align(draft_path, ref_path, out_draft, out_overlay, do_palette=False, bg_text_keys=None):
    draft = json.loads(Path(draft_path).read_text(encoding="utf-8"))
    _guard_layout(draft, draft_path)
    w, h = int(draft["width"]), int(draft["height"])
    items = draft.get("items", [])
    bg_keys = [k.strip().lower() for k in (bg_text_keys or []) if k.strip()]

    for idx, it in enumerate(items):
        if not isinstance(it, dict) or "bbox" not in it or "label" not in it:
            raise SystemExit(
                "错误：items[%d] 缺 label 或 bbox（现有键：%s）。"
                "每个 item 至少要 label / caption / bbox。"
                % (idx, ", ".join(sorted(it.keys())) if isinstance(it, dict) else type(it).__name__)
            )

    im = Image.open(ref_path).convert("RGB") if ref_path else None
    warnings = []
    z_hints = {}
    max_shift = 0

    # 1. 吸附到 16px、记下 z_layer 工作标记、抓兜底大框
    for idx, it in enumerate(items):
        if "z_layer" in it:
            z_hints[id(it)] = str(it.pop("z_layer")).lower()
        new_b, shift = snap_bbox([int(v) for v in it["bbox"]], w, h)
        it["bbox"] = new_b
        max_shift = max(max_shift, shift)
        area_ratio = ((new_b[2] - new_b[0]) * (new_b[3] - new_b[1])) / float(w * h)
        if it["label"] == "object" and area_ratio >= 0.85:
            warnings.append(
                "item[%d] (object) 覆盖画布 %.0f%% —— 别在角色后面塞兜底大框；"
                "拆成局部 object，或确认它排在最前。" % (idx, area_ratio * 100)
            )
        if do_palette and im is not None and "palette" not in it and it["label"] != "text":
            pal = extract_hex_palette(im, new_b, w, h, k=3)
            if pal:
                it["palette"] = pal

    if max_shift > 8:
        warnings.append("有框被挪动了 %d px（16px 吸附上限是 8px），回去看一下原始坐标是不是读错了。" % max_shift)

    # 2. 背景到前景：bg_text(-1) → 大背景(0) → 道具(1) → 角色(2) → 前景文字(3)
    def is_bg_text(it, hint):
        if it["label"] != "text":
            return False
        if hint == "bg":
            return True
        if hint == "fg":
            return False
        t = (it.get("text") or "").lower()
        c = (it.get("caption") or "").lower()
        return any(k in t or k in c for k in bg_keys)

    def z_rank(it):
        b = it["bbox"]
        area_ratio = ((b[2] - b[0]) * (b[3] - b[1])) / float(w * h)
        hint = z_hints.get(id(it))
        if it["label"] == "text":
            # z_layer 对文字同样生效：fg 显式置顶，不会被 --bg-text 的子串误沉到底
            return (-1, -area_ratio) if is_bg_text(it, hint) else (3, -area_ratio)
        if it["label"] == "character":
            if hint == "bg":
                return (2, -1.0 + area_ratio)
            if hint == "fg":
                return (2, 1.0 + area_ratio)
            return (2, area_ratio)
        if hint == "fg":
            return (2.5, area_ratio)
        return (0 if area_ratio >= 0.35 else 1, -area_ratio)

    sorted_items = sorted(items, key=z_rank)
    if [id(x) for x in sorted_items] != [id(x) for x in items]:
        warnings.append("重排为背景到前景（bg_text → 背景 → 道具 → 角色 → 前景文字）。")
        draft["items"] = sorted_items

    if out_draft:
        Path(out_draft).write_text(json.dumps(draft, ensure_ascii=False, indent=2), encoding="utf-8")
        print("Wrote 16px-aligned draft: %s" % out_draft)
        if z_hints:
            print("[ALIGN] z_layer 已剥离，只留在对齐稿；直接编译原稿会报 unknown fields。")

    if out_overlay and im is not None:
        vis = im.resize((w, h), Image.Resampling.LANCZOS)
        draw = ImageDraw.Draw(vis)
        fsize = max(12, min(w, h) // 48)
        font, cjk = _font(fsize)
        band = fsize + 6
        for idx, it in enumerate(draft["items"]):
            x1, y1, x2, y2 = it["bbox"]
            col = COLORS.get(it["label"], (200, 200, 200))
            draw.rectangle([x1, y1, x2, y2], outline=col, width=4)
            tag = "#%d %s" % (idx, it["label"])
            if it.get("text"):
                tag += ": " + it["text"][:12]
            if not cjk and not tag.isascii():
                # 没中文字体时别画豆腐块，退成 ASCII 占位
                tag = tag.encode("ascii", "replace").decode("ascii")
            ty0 = max(0, y1 - band)
            try:
                tw = draw.textlength(tag, font=font)
            except Exception:
                tw = len(tag) * fsize * 0.6
            draw.rectangle([x1, ty0, min(w, x1 + tw + 8), y1], fill=col)
            draw.text((x1 + 4, ty0 + 2), tag, fill=(0, 0, 0), font=font)
        vis.save(out_overlay)
        print("Saved alignment overlay: %s" % out_overlay)

    for msg in warnings:
        print("[ALIGN] %s" % msg)


def main():
    p = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    sub = p.add_subparsers(dest="cmd", required=True)

    dm = sub.add_parser("dims", help="按参考图比例算 16 倍数分辨率")
    dm.add_argument("ref")
    dm.add_argument("--area", type=int, default=DEFAULT_AREA,
                    help="基准面积，默认 %d（1536×1024）" % DEFAULT_AREA)
    dm.add_argument("--max-side", type=int, default=MAX_SIDE,
                    help="长边上限，默认 %d；宽银幕比例会按比例压回来" % MAX_SIDE)

    g = sub.add_parser("grid", help="参考图叠 10%% 坐标网格")
    g.add_argument("ref")
    g.add_argument("-o", "--output", required=True)

    v = sub.add_parser("verify", help="16px 吸附 + 背景到前景排序 + 主色采样 + 叠框")
    v.add_argument("draft")
    v.add_argument("--ref", default=None)
    v.add_argument("--out-draft", default=None)
    v.add_argument("--out-overlay", default=None)
    v.add_argument("--extract-palette", action="store_true")
    v.add_argument("--bg-text", default="",
                   help="逗号分隔的关键词：正文里命中这些子串的 text 排到 character 之前")

    args = p.parse_args()
    if args.cmd == "dims":
        (ow, oh), (tw, th), clamped = compute_dims(args.ref, args.area, args.max_side)
        print("orig=%dx%d (ratio=%.3f) -> target=%dx%d (16mult=%s, area=%.2fM%s)"
              % (ow, oh, ow / oh, tw, th, tw % 16 == 0 and th % 16 == 0, tw * th / 1e6,
                 ", 长边已压到 %d" % args.max_side if clamped else ""))
        print("常用档（同一口径现算）：" + "  ".join(
            "%s %dx%d" % (name, dims_for_ratio(r, args.area, args.max_side)[0][0],
                          dims_for_ratio(r, args.area, args.max_side)[0][1])
            for name, r in (("2:3", 2 / 3.0), ("3:2", 3 / 2.0), ("16:9", 16 / 9.0),
                            ("21:9", 21 / 9.0), ("9:16", 9 / 16.0))))
    elif args.cmd == "grid":
        draw_grid(args.ref, args.output)
    else:
        bg_keys = [x for x in args.bg_text.split(",") if x.strip()]
        verify_and_align(args.draft, args.ref, args.out_draft, args.out_overlay,
                         args.extract_palette, bg_keys)


if __name__ == "__main__":
    main()
