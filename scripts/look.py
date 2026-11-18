#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""look.py — 让一个视觉模型替你看图，返回结构化文字。

为什么存在：本机主模型的视觉编码会把大图压到 ~1000px，手指、绳结、朝向这类
细节在压缩后不可分辨。这个脚本把图（或局部裁切）发给一个视觉更强的模型，
用一组离散、可验证的问题换回可核对的答案，再交给提示词作者使用。

用法:
    # 单个问题
    python scripts/look.py shot.png -q "她的左手在哪里？握着什么？"

    # 批量问题（每行一条，空行忽略）
    python scripts/look.py shot.png -Q questions.txt

    # 二十问清单（内置）
    python scripts/look.py shot.png --sop

    # 同时看多张（比如九宫格里的某几块）
    python scripts/look.py crops/Ghead.png crops/Ghip.png -q "这两块里她的手各在哪"

环境:
    GEMINI_API_KEY   从环境变量或 ~/.dsh/.credentials.yaml 读取
    LOOK_MODEL       默认 gemini-3-flash-preview
"""

import argparse
import base64
import json
import mimetypes
import os
import re
import sys
import urllib.error
import urllib.request

DEFAULT_MODEL = os.environ.get("LOOK_MODEL", "gemini-3-flash-preview")
ENDPOINT = "https://generativelanguage.googleapis.com/v1beta/models/{model}:generateContent"
CRED = os.path.join(os.path.expanduser("~"), ".dsh", ".credentials.yaml")

# 内置二十问：全部是离散、可验证、能写成一句话的；连续形容词不算答案
SOP_QUESTIONS = [
    "Is any face visible anywhere in the image? Answer yes/no first, then locate it by frame fraction.",
    "How many human-shaped figures are there? Count only figures you can see at least a head-or-torso-worth of.",
    "For each figure: what is each hand doing, and what does each hand hold?",
    "Where is every limb? If a limb is hidden, say hidden and by what.",
    "How many weapons/props are there, and is each one a blade, a sheath, or something else?",
    "How many separate fires, lights, or glowing sources are there, and where?",
    "Is the frame level or tilted? Estimate the rotation in degrees and say what evidence gives it.",
    "Can you see any ground, floor, or horizon? If not, say none.",
    "List every surface that shows motion smear or trailing, and the direction it smears toward.",
    "What is the single darkest thing in the frame, and what is the single lightest?",
    "List each distinct hue you can name, and roughly what fraction of the frame each covers.",
    "What is the dominant material of the frame: paper, canvas, cel, print, photo, or other?",
    "Describe every text element you can read, transcribed exactly, with its position.",
    "Is there grain, paper texture, or halftone? Say which and how coarse.",
    "What is in the top-left corner, and what is in the bottom-right corner?",
    "List anything that occludes something else, as 'A occludes B'.",
    "How many distinct depth layers can you count, and what separates them?",
    "What is the smallest identifiable object in the frame, and how many pixels across is it roughly?",
    "Describe the pose of the largest figure in one sentence, using only body-part positions.",
    "What in this image would a careful viewer most likely misread on first glance, and why?",
]

SYSTEM = (
    "You are a forensic image describer. You answer only from what is visible. "
    "For every answer you either give a concrete, checkable statement, or you write "
    "'UNCLEAR' followed by what specifically you cannot resolve and why. "
    "Never fill a gap with what is typical for this genre. Never use adjectives that "
    "cannot be checked against pixels. Answer in the same language as the question. "
    "Be terse: one line per question, no preamble."
)


def api_key():
    k = os.environ.get("GEMINI_API_KEY") or os.environ.get("GOOGLE_API_KEY")
    if k:
        return k.strip()
    try:
        with open(CRED, "r", encoding="utf-8") as f:
            for line in f:
                m = re.match(r"\s*GEMINI_API_KEY\s*:\s*(\S+)", line)
                if m:
                    return m.group(1).strip().strip("'\"")
    except OSError:
        pass
    sys.exit("找不到 GEMINI_API_KEY（环境变量或 %s）" % CRED)


def part_for(path):
    mt = mimetypes.guess_type(path)[0] or "image/png"
    if mt == "image/jpg":
        mt = "image/jpeg"
    with open(path, "rb") as f:
        data = base64.b64encode(f.read()).decode("ascii")
    return {"inline_data": {"mime_type": mt, "data": data}}


def ask(paths, question, model, temperature=0.0, max_tokens=2048):
    parts = [part_for(p) for p in paths]
    parts.append({"text": question})
    body = {
        "system_instruction": {"parts": [{"text": SYSTEM}]},
        "contents": [{"role": "user", "parts": parts}],
        "generationConfig": {
            "temperature": temperature,
            "maxOutputTokens": max_tokens,
            # Gemini 3 默认开思考，思考 token 会把答案挤断（实测 20 问只回 222 字节）
            "thinkingConfig": {"thinkingBudget": 0},
        },
    }
    req = urllib.request.Request(
        ENDPOINT.format(model=model),
        data=json.dumps(body).encode("utf-8"),
        headers={"Content-Type": "application/json", "x-goog-api-key": api_key()},
        method="POST",
    )
    try:
        with urllib.request.urlopen(req, timeout=180) as r:
            payload = json.loads(r.read().decode("utf-8"))
    except urllib.error.HTTPError as e:
        detail = e.read().decode("utf-8", "replace")[:600]
        sys.exit("HTTP %s: %s" % (e.code, detail))
    except urllib.error.URLError as e:
        sys.exit("网络错误: %s" % e.reason)

    cands = payload.get("candidates") or []
    if not cands:
        fb = payload.get("promptFeedback") or {}
        sys.exit("没有候选结果: %s" % json.dumps(fb, ensure_ascii=False)[:400])
    out = []
    for c in cands[0].get("content", {}).get("parts", []):
        if "text" in c:
            out.append(c["text"])
    return "".join(out).strip()


def main():
    ap = argparse.ArgumentParser(add_help=True, description="让视觉模型替你读图")
    ap.add_argument("images", nargs="+", help="图片路径，可多张")
    ap.add_argument("-q", "--question", help="单个问题")
    ap.add_argument("-Q", "--questions", help="问题清单文件，每行一条")
    ap.add_argument("--sop", action="store_true", help="用内置二十问")
    ap.add_argument("-m", "--model", default=DEFAULT_MODEL)
    ap.add_argument("-t", "--temperature", type=float, default=0.0)
    args = ap.parse_args()

    for p in args.images:
        if not os.path.isfile(p):
            sys.exit("找不到文件: %s" % p)

    if args.sop:
        qs = SOP_QUESTIONS
    elif args.questions:
        with open(args.questions, "r", encoding="utf-8") as f:
            qs = [ln.strip() for ln in f if ln.strip()]
    elif args.question:
        qs = [args.question]
    else:
        sys.exit("给一个问题：-q / -Q / --sop")

    numbered = "\n".join("%d. %s" % (i + 1, q) for i, q in enumerate(qs))
    prompt = (
        "Answer each numbered question about the attached image(s) on its own line, "
        "prefixed with the number. If more than one image is attached, say which image "
        "each answer refers to by its position (1st, 2nd...).\n\n" + numbered
    )
    text = ask(args.images, prompt, args.model, args.temperature)
    print(text)


if __name__ == "__main__":
    main()
