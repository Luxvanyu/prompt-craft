#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""真实提示词库：一万条出过图的完整提示词，用来查「别人怎么写」。

    python corpus.py                          概况（两部图包的条数/评分/尺寸/参数）
    python corpus.py --stat                   完整分布（tag 密度、画师数、语法、质量词）
    python corpus.py --find 侧光              在正向全文里搜（中英文都行，查 tag 组合）
    python corpus.py --find "backlight, rim"  搜同时含这几个词条的条目
    python corpus.py --show 3                 随机看 3 条完整提示词（含负向与参数）
    python corpus.py --show 3 --rating safe   只看 safe 的
    python corpus.py --params                 参数分布（Steps/Sampler/CFG/尺寸）

数据要先下：python fetch_lexicon.py --packs   （42 MB，不入库）
没有数据时本脚本会打印上面这行命令，不会抛栈。

与 lexicon.py 的分工：lexicon.py 查「一个词叫什么」，
corpus.py 查「整条提示词长什么样、大家怎么组合」。
"""

from __future__ import print_function

import argparse
import collections
import io
import json
import os
import random
import re
import sys

for _s in (sys.stdout, sys.stderr):
    try:
        _s.reconfigure(encoding="utf-8")
    except Exception:
        pass

HERE = os.path.dirname(os.path.abspath(__file__))
PACKS = [
    ("v5", "nai5_community_pack", "NAI v5 社区图包"),
    ("v45", "nai45_community_pack", "NAI v4.5 社区图包"),
]
HINT = "python " + os.path.join(HERE, "fetch_lexicon.py") + " --packs"


def find_dir():
    env = os.environ.get("TAG_LEXICON_QT")
    if env:
        return os.path.dirname(env) if env.endswith(".json") else env
    for c in (os.path.join(HERE, ".lexicon"),
              HERE,
              os.path.join(HERE, "..", ".lexicon")):
        if os.path.isdir(c):
            return c
    return None


def load_packs(want=None):
    """读缓存里的图包 JSON。返回 [(label, note, entries)]，缺的跳过。"""
    d = find_dir()
    if not d:
        return []
    got = []
    for label, cid, note in PACKS:
        if want and label not in want:
            continue
        p = os.path.join(d, cid + ".json")
        if not os.path.exists(p):
            continue
        try:
            with io.open(p, encoding="utf-8") as f:
                got.append((label, note, json.load(f).get("entries") or []))
        except Exception:
            pass
    return got


def split_tags(tags):
    """按顶层逗号切；括号内的逗号不切。"""
    out, buf, depth = [], [], 0
    for ch in tags or "":
        if ch in "([{":
            depth += 1
        elif ch in ")]}":
            depth = max(0, depth - 1)
        if ch == "," and depth == 0:
            out.append("".join(buf))
            buf = []
        else:
            buf.append(ch)
    if buf:
        out.append("".join(buf))
    return [p.strip() for p in out if p.strip()]


def strip_weight(s):
    return re.sub(r"^[\-\d\.]+::", "", s).strip()


def count_tags(tags):
    return len([p for p in split_tags(re.sub(r"[\d\.\-]+::", "", tags or "")) if p.strip()])


def parse_params(note):
    pat = [("Steps", r"Steps:\s*(\d+)"),
           ("Sampler", r"Sampler:\s*([A-Za-z0-9+ ._-]+)"),
           ("CFG", r"CFG scale:\s*([\d.]+)"),
           ("Size", r"Size:\s*(\d+x\d+)"),
           ("Sched", r"Noise schedule:\s*([A-Za-z ]+)")]
    out = {}
    for k, p in pat:
        m = re.search(p, note or "")
        if m:
            out[k] = m.group(1).strip()
    return out


def median(a):
    a = sorted(a)
    n = len(a)
    if not n:
        return 0
    return a[n // 2] if n % 2 else (a[n // 2 - 1] + a[n // 2]) / 2.0


def top(counter, n=5):
    return "、".join("%s %d" % (k, v) for k, v in counter.most_common(n))


def opening_kind(first):
    """把一条提示词的第一段归类：画师 / 人数词 / 内容。"""
    f = (first or "").lower().replace("_", " ").strip()
    if "artist" in f:
        return "artist"
    if re.match(r"^(\d+\+?\s*(girl|boy|other)s?|solo|no humans|"
                r"multiple (girls|boys|others))\b", f):
        return "count"
    return "content"


def cmd_overview(packs):
    print("真实提示词库：%d 部图包\n" % len(packs))
    for label, note, es in packs:
        rat = collections.Counter(e.get("rating") or "?" for e in es)
        sz = collections.Counter((e.get("imageWidth"), e.get("imageHeight")) for e in es)
        tagc = [count_tags(e.get("tags")) for e in es]
        print("  %-4s %-22s %5d 条" % (label, note, len(es)))
        print("       评分 %s" % top(rat, 4))
        print("       tag 中位 %d，尺寸 top3 %s"
              % (median(tagc), "、".join("%dx%d %d" % (w, h, c) for (w, h), c in sz.most_common(3) if w)))
    print("\n  --stat 完整分布 / --find 词 / --show N / --params")


def cmd_stat(packs):
    for label, note, es in packs:
        n = len(es)
        tagc = [count_tags(e.get("tags")) for e in es]
        art = [len(re.findall(r"artist:", e.get("tags") or "")) for e in es]
        taglen = [len((e.get("tags") or "").strip()) for e in es]
        pos, opening = [], collections.Counter()
        for e in es:
            segs = split_tags(strip_weight((e.get("tags") or "").lstrip()))
            if segs:
                opening[opening_kind(segs[0])] += 1
                idx = [i for i, s in enumerate(segs) if "artist" in s.lower()]
                if idx and len(segs) > 1:
                    pos.append(idx[0] / float(len(segs) - 1))
        rat = collections.Counter(e.get("rating") or "?" for e in es)
        sz = collections.Counter((e.get("imageWidth"), e.get("imageHeight")) for e in es)
        negs = [(e.get("negative") or "").strip() for e in es]
        negl = [len(x) for x in negs if x]
        multi = sum(1 for e in es if len(e.get("characterPrompts") or []) > 1)
        prose = 0
        for e in es:
            t = re.sub(r"[\d\.\-]+::", "", e.get("tags") or "")
            if any(len(p.split()) >= 8 for p in split_tags(t)):
                prose += 1
        quality = collections.Counter()
        for e in es:
            low = (e.get("tags") or "").lower()
            for q in ("masterpiece", "best quality", "very aesthetic",
                      "absurdres", "amazing quality", "highres"):
                if q in low:
                    quality[q] += 1

        print("=" * 60)
        print("%s  %s  %d 条" % (label, note, n))
        print("  正向 tag 数   中位 %d  p25 %d  p75 %d  最多 %d"
              % (median(tagc), sorted(tagc)[n // 4], sorted(tagc)[n * 3 // 4], max(tagc)))
        print("  正向均字数    %.0f 字符（中位 %d）"
              % (sum(taglen) / max(1, len(taglen)), median(taglen)))
        print("  画师标签数    中位 %d  均 %.1f  p75 %d  最多 %d  一个都没有 %.1f%%"
              % (median(art), sum(art) / float(n), sorted(art)[n * 3 // 4], max(art),
                 100.0 * sum(1 for a in art if a == 0) / n))
        print("  画师串相对位置 中位 %.2f  p25 %.2f  p75 %.2f  落在前四分之一 %.1f%%"
              % (median(pos), sorted(pos)[len(pos) // 4], sorted(pos)[len(pos) * 3 // 4],
                 100.0 * sum(1 for x in pos if x <= 0.25) / max(1, len(pos)))
              if pos else "  画师串相对位置  无画师标签")
        print("  开头三分天下  画师 %.1f%%  人数词 %.1f%%  内容 %.1f%%"
              % tuple(100.0 * opening[k] / n for k in ("artist", "count", "content")))
        print("  评分         %s" % top(rat, 5))
        print("  尺寸 top3    %s" % "、".join(
            "%dx%d %.1f%%" % (w, h, 100.0 * c / n) for (w, h), c in sz.most_common(3) if w))
        print("  负向         均 %.0f 字符，%d 条为空，去重后 %.1f%% 是重复模板"
              % (sum(negl) / max(1, len(negl)),
                 sum(1 for x in negs if not x),
                 100.0 * (1 - len(set(x for x in negs if x)) / max(1, len(negl)))))
        print("  多条子提示词  %d 条（%.1f%%）" % (multi, 100.0 * multi / n))
        byrating = collections.defaultdict(lambda: [0, 0])
        for e in es:
            r = e.get("rating") or "?"
            byrating[r][0] += 1
            if len(e.get("characterPrompts") or []) > 1:
                byrating[r][1] += 1
        print("     按评分      " + "、".join(
            "%s %.1f%%" % (r, 100.0 * c[1] / c[0]) for r, c in
            sorted(byrating.items(), key=lambda x: -x[1][0]) if c[0] >= 50))
        buckets = collections.Counter()
        for a in art:
            if a == 0:
                buckets["0"] += 1
            elif a <= 3:
                buckets["1-3"] += 1
            elif a <= 7:
                buckets["4-7"] += 1
            elif a <= 11:
                buckets["8-11"] += 1
            else:
                buckets["12+"] += 1
        print("     画师档位    " + "、".join(
            "%s 个 %.1f%%" % (k, 100.0 * buckets[k] / n)
            for k in ("0", "1-3", "4-7", "8-11", "12+") if buckets[k]))
        print("  含英文长句     %d 条（%.1f%%）" % (prose, 100.0 * prose / n))
        print("  质量词        %s" % "、".join(
            "%s %.1f%%" % (k, 100.0 * v / n) for k, v in quality.most_common()))
        syn = collections.Counter()
        for e in es:
            t = e.get("tags") or ""
            if re.search(r"[\d\.\-]+::", t):
                syn["n::壳::"] += 1
            if re.search(r"\d\.\d+::", t):
                syn["小数权重"] += 1
            if "{" in t:
                syn["{}"] += 1
            if "[" in t:
                syn["[]"] += 1
            if re.search(r"\(\w[\w ]*:\d", t):
                syn["(x:1.2)"] += 1
            if "||" in t:
                syn["||序列||"] += 1
        print("  语法         %s" % "、".join(
            "%s %.1f%%" % (k, 100.0 * v / n) for k, v in syn.most_common()))


def pct_top(counter, total, n=4):
    return "、".join("%s %.1f%%" % (k, 100.0 * v / total)
                    for k, v in counter.most_common(n))


def cmd_params(packs):
    for label, note, es in packs:
        P = [parse_params(e.get("note")) for e in es]
        st = [int(p["Steps"]) for p in P if "Steps" in p]
        cfg = [float(p["CFG"]) for p in P if "CFG" in p]
        print("=" * 60)
        print("%s  %s" % (label, note))
        if st:
            print("  Steps    %s   中位 %d"
                  % (pct_top(collections.Counter(st), len(st)), median(st)))
        smp = collections.Counter(p["Sampler"] for p in P if "Sampler" in p)
        if smp:
            print("  Sampler  %s" % pct_top(smp, sum(smp.values()), 3))
        if cfg:
            print("  CFG      %s   中位 %.1f"
                  % (pct_top(collections.Counter(cfg), len(cfg)), median(cfg)))
        sch = collections.Counter(p["Sched"] for p in P if "Sched" in p)
        if sch:
            print("  Schedule %s" % pct_top(sch, sum(sch.values()), 3))


def cmd_find(packs, words):
    keys = [w.strip().lower() for w in re.split(r"[,，]", words) if w.strip()]
    for label, note, es in packs:
        hits = []
        for e in es:
            hay = " ".join([e.get("tags") or "", e.get("title") or "",
                            e.get("note") or ""]).lower()
            if all(k in hay for k in keys):
                hits.append(e)
        print("=" * 60)
        print("%s：命中 %d 条（正向 tag、标题、说明里都查）" % (label, len(hits)))
        for e in hits[:8]:
            print("\n  [%s] %s | %sx%s" % (e.get("rating") or "?",
                                           (e.get("title") or "")[:40],
                                           e.get("imageWidth"), e.get("imageHeight")))
            t = e.get("tags") or ""
            shown = 0
            for seg in split_tags(t):
                if any(k in seg.lower() for k in keys):
                    print("    · " + seg[:200])
                    shown += 1
            if not shown:  # 命中的是中文标题/说明，没有 tag 段可摘
                for line in (e.get("note") or "").splitlines():
                    if any(k in line.lower() for k in keys):
                        print("    ~ " + line[:200])
                        break
        if len(hits) > 8:
            print("\n  ...还有 %d 条" % (len(hits) - 8))


def cmd_show(packs, n, rating):
    pool = []
    for label, note, es in packs:
        for e in es:
            if rating and (e.get("rating") or "") != rating:
                continue
            pool.append((label, e))
    if not pool:
        print("没有符合条件的条目。")
        return
    random.seed()
    for label, e in random.sample(pool, min(n, len(pool))):
        print("=" * 60)
        print("[%s/%s] %s | %sx%s" % (label, e.get("rating") or "?",
                                      e.get("title") or "", e.get("imageWidth"), e.get("imageHeight")))
        print("\n正向：\n" + (e.get("tags") or ""))
        neg = (e.get("negative") or "").strip()
        if neg:
            print("\n负向：\n" + neg)
        for c in (e.get("characterPrompts") or []):
            print("\n子提示词 %s：\n%s" % (c.get("label"), c.get("prompt")))
        note = (e.get("note") or "").strip()
        if note:
            if not note.startswith("参数"):
                note = "参数：\n" + note
            print("\n" + note)


def main():
    ap = argparse.ArgumentParser(description="查一万条真实提示词怎么写")
    ap.add_argument("words", nargs="?", help="要搜的词（可逗号分隔多个，全部命中才算）")
    ap.add_argument("--stat", action="store_true", help="完整分布")
    ap.add_argument("--params", action="store_true", help="出图参数分布")
    ap.add_argument("--find", metavar="词", help="在正向全文里搜")
    ap.add_argument("--show", type=int, metavar="N", help="随机看 N 条完整提示词")
    ap.add_argument("--rating", help="只显示该评分（safe / r18 / r18g / restricted）")
    ap.add_argument("--pack", help="只用某部图包（v5 / v45）")
    a = ap.parse_args()

    want = [a.pack] if a.pack else None
    packs = load_packs(want)
    if not packs:
        print("找不到图包数据。第一次用先跑一次：")
        print("  " + HINT)
        print("\n（约 42 MB，会存进 scripts/.lexicon，已在 .gitignore 里）")
        return 1

    if a.stat:
        cmd_stat(packs)
    elif a.params:
        cmd_params(packs)
    elif a.find or a.words:
        cmd_find(packs, a.find or a.words)
    elif a.show:
        cmd_show(packs, a.show, a.rating)
    elif a.rating:
        cmd_show(packs, 3, a.rating)
    else:
        cmd_overview(packs)
    return 0


if __name__ == "__main__":
    sys.exit(main())
