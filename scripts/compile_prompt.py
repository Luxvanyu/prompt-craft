#!/usr/bin/env python3
"""Compile a caption or absolute-pixel Layout draft into a MOSS-Image prompt.

Vendored from the official MOSS-Image prompt enhancer
(`moss-image-prompt-enhancer/scripts/compile_prompt.py`, 146 lines).
Copied verbatim except for this header. Behaviour is byte-identical to the
upstream compiler: caption drafts pass through unchanged; Layout drafts are
validated (six top-level keys, width/height multiples of 16, abs+xyxy) and
then rewritten to abs_centralized + yxyx.
"""

import argparse
import json
import math
import sys
from pathlib import Path

# 报错信息含中文，Windows 控制台默认 GBK 会打成乱码（与 lint.py 同处理）
for _s in (sys.stdout, sys.stderr):
    try:
        _s.reconfigure(encoding="utf-8")
    except Exception:
        pass


def require(condition, message):
    if not condition:
        raise ValueError(message)


def fields(value, allowed, required, location):
    require(isinstance(value, dict), f"{location} must be an object")
    unknown = value.keys() - allowed
    missing = required - value.keys()
    require(not unknown,
            f"{location}: unknown fields {sorted(unknown)} — 这个位置只接受 {sorted(allowed)}")
    require(not missing,
            f"{location}: missing fields {sorted(missing)} — 必须有 {sorted(required)}")


def text(value, location):
    require(isinstance(value, str) and bool(value.strip()), f"{location} must be nonempty text")


def strings(value, location):
    require(isinstance(value, list), f"{location} must be an array")
    for index, item in enumerate(value):
        text(item, f"{location}[{index}]")


def centered_box(box, width, height, location):
    require(isinstance(box, list) and len(box) == 4, f"{location} must be [x1,y1,x2,y2] — 左上角起算的绝对像素框，例如 [300, 200, 1200, 900]")
    require(
        all(type(v) in (int, float) and math.isfinite(v) for v in box),
        f"{location} must contain four finite numbers — 例如 [300, 200, 1200, 900]，不要写字符串或 null",
    )
    x1, y1, x2, y2 = box
    require(x1 < x2 and y1 < y2, f"{location} must have positive width and height — 要求 x1<x2 且 y1<y2，现在填的是 {box!r}")
    require(
        0 <= x1 < x2 <= width and 0 <= y1 < y2 <= height,
        f"{location} exceeds the {width}x{height} canvas — 四个值必须落在 0..width / 0..height 之内，现在填的是 {box!r}",
    )
    # Enclose in pixel edges before centering, as in Echidna generation export.
    result = [
        math.floor(round(y1, 9)) - height // 2,
        math.floor(round(x1, 9)) - width // 2,
        math.ceil(round(y2, 9)) - height // 2,
        math.ceil(round(x2, 9)) - width // 2,
    ]
    require(result[0] < result[2] and result[1] < result[3],
            f"{location} is too small at export precision — 框宽或框高不足 1 像素，把 bbox 四个值拉开至少 1 像素间隔")
    return result


def compile_prompt(draft):
    require(isinstance(draft, dict), "Draft must be a JSON object — 最外层必须是 {...}，例如 {\"caption\": \"...\"} 或 Layout 草稿")
    if "caption" in draft:
        fields(draft, {"caption"}, {"caption"}, "Caption draft")
        text(draft["caption"], "caption")
        return draft["caption"]

    root_fields = {"width", "height", "bbox_coord_space", "bbox_format", "summary", "items"}
    fields(draft, root_fields, root_fields, "Layout draft")
    width, height = draft["width"], draft["height"]
    for name, value in (("width", width), ("height", height)):
        if type(value) is int and value > 0 and value % 16 == 0:
            continue
        hint = "常见取值 1536 / 1344 / 1024 / 768（都必须是 16 的倍数）"
        if type(value) in (int, float) and value > 0:
            lo = int(value) // 16 * 16
            hint = ("现在填的是 %r，最近的合法值是 %d 或 %d"
                    % (value, max(16, lo), max(16, lo) + 16))
        else:
            hint = "现在填的是 %r — %s" % (value, hint)
        require(False, "%s must be a positive integer multiple of 16 — %s" % (name, hint))
    require(draft["bbox_coord_space"] == "abs",
            'Draft bbox_coord_space must be "abs" — 草稿一律用绝对像素坐标；'
            f'"abs_centralized" 是编译产物的写法，不要写进草稿。现在填的是 {draft["bbox_coord_space"]!r}。'
            '示例：{"bbox_coord_space": "abs", "bbox_format": "xyxy", "width": 1536, "height": 1024}')
    require(draft["bbox_format"] == "xyxy",
            'Draft bbox_format must be "xyxy" — 草稿按左上角起算的 [x1,y1,x2,y2] 写；'
            f'"yxyx" 是编译产物的顺序，不要写进草稿。现在填的是 {draft["bbox_format"]!r}。'
            '示例：{"label": "character", "bbox": [300, 200, 1200, 900], "caption": "..."}')

    summary = draft["summary"]
    fields(summary, {"caption", "meta", "canvas", "palette"}, {"caption"}, "summary")
    text(summary["caption"], "summary.caption")
    if "canvas" in summary:
        require(summary["canvas"] in ("single", "multi_panel", "collage"),
                "summary.canvas must be single, multi_panel or collage — 不写这个键时默认为单图")
    for key in ("meta", "palette"):
        if key in summary:
            strings(summary[key], f"summary.{key}")

    items = draft["items"]
    require(isinstance(items, list) and bool(items), "items must be a nonempty flat array — items 必须是平铺数组（不要按角色分组嵌套），且至少一项")
    compiled_items = []
    for index, item in enumerate(items):
        location = f"items[{index}]"
        fields(item, {"label", "caption", "bbox", "text", "tags", "palette"},
               {"label", "caption", "bbox"}, location)
        require(item["label"] in ("object", "character", "text"),
                f"{location}.label must be object, character or text — 现在填的是 {item['label']!r}；不要用 type 字段")
        text(item["caption"], f"{location}.caption")
        if item["label"] == "text":
            require("text" in item, f"{location}: text items require literal text — label 为 text 时必须同时给 text 字段写明画面里的字")
        if "text" in item:
            text(item["text"], f"{location}.text")
        for key in ("tags", "palette"):
            if key in item:
                strings(item[key], f"{location}.{key}")
        compiled_items.append({
            key: centered_box(value, width, height, f"{location}.bbox") if key == "bbox" else value
            for key, value in item.items()
        })

    result = {"summary": summary, "items": compiled_items,
              "bbox_coord_space": "abs_centralized", "bbox_format": "yxyx"}
    return json.dumps(result, ensure_ascii=False, separators=(",", ":"), allow_nan=False)


def unique_object(pairs):
    result = {}
    for key, value in pairs:
        require(key not in result, f"Duplicate JSON key: {key}")
        result[key] = value
    return result


def reject_constant(value):
    raise ValueError(f"Invalid JSON number: {value}")


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("draft", type=Path, help="UTF-8 caption or Layout JSON draft")
    parser.add_argument("--output", type=Path, help="Write prompt to a file instead of stdout")
    args = parser.parse_args()
    try:
        if args.output:
            require(args.output.resolve() != args.draft.resolve(),
                    "Output must be separate from the editable draft")
        draft = json.loads(args.draft.read_text(encoding="utf-8"),
                           object_pairs_hook=unique_object, parse_constant=reject_constant)
        prompt = compile_prompt(draft)
        if args.output:
            args.output.parent.mkdir(parents=True, exist_ok=True)
            args.output.write_text(prompt + "\n", encoding="utf-8")
            print(f"Wrote {args.output}", file=sys.stderr)
        else:
            print(prompt)
    except (OSError, ValueError, OverflowError) as error:
        parser.exit(2, f"Error: {error}\n")


if __name__ == "__main__":
    main()
