#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""法典词典查询器 —— 把「我想要的那个东西叫什么」翻译成 danbooru tag。

    python lexicon.py 逆光              中英双向模糊查（中文标题、tag、说明全文）
    python lexicon.py --exact backlighting   精确查一个 tag
    python lexicon.py --cat             列法典 / 分类树 / 条数
    python lexicon.py --in 视角构图      列某分类下全部条目
    python lexicon.py --codex raven     列某部法典的全部一级分类
    python lexicon.py --scene           列「构图风格」64 条成品场景串（带横竖图）
    python lexicon.py --neg 手           看带负向的法典条目里怎么写负向

索引默认读 scripts/.lexicon/index.json（由 fetch_lexicon.py 生成），
可设 TAG_LEXICON_QT 覆盖；索引不存在时只提示怎么建，不报错退出（不影响主流程）。

数据来源：novelai.quicktagcloud.com 的五部社区法典（渡鸦构图鉴 6633 / 构图风格 64 /
解构原典 274 / 更衣人偶 430 / 千藤衣柜 125）。这些是 danbooru 系模型的词，
MOSS 要按 references/lexicon.md 的「翻译纪律」改写成描述句。
"""
import json
import io
import os
import sys

for _s in (sys.stdout, sys.stderr):
    try:
        _s.reconfigure(encoding="utf-8")
    except Exception:
        pass

DEFAULT = []


def find_index():
    env = os.environ.get("TAG_LEXICON_QT")
    if env:
        return env
    here = os.path.dirname(os.path.abspath(__file__))
    cands = list(DEFAULT) + [
        os.path.join(here, ".lexicon", "index.json"),
        os.path.join(here, "index.json"),
        os.path.join(here, "..", ".lexicon", "index.json"),
    ]
    for c in cands:
        if os.path.exists(c):
            return c
    return None


def load():
    p = find_index()
    if not p:
        print("找不到词典索引。第一次用先跑一次：")
        print("    python %s" % os.path.join(os.path.dirname(os.path.abspath(__file__)), "fetch_lexicon.py"))
        print("它会下载五部法典（约 7 MB）并建好索引（约 1.8 MB）。")
        print("或设环境变量 TAG_LEXICON_QT 指向已有的 index.json。")
        return None
    with io.open(p, encoding="utf-8") as f:
        return json.load(f)


def cut(s, n=90):
    s = " ".join((s or "").split())
    return s if len(s) <= n else s[: n - 1] + "…"


def show(e, verbose=False):
    zh = e.get("zh") or ""
    tag = e.get("t") or ""
    print("  %-34s %s" % (tag, zh))
    if e.get("p"):
        print("      分类：%s" % e["p"])
    if verbose and e.get("n"):
        print("      说明：%s" % cut(e["n"], 200))
    elif e.get("n"):
        print("      %s" % cut(e["n"], 96))
    if verbose and e.get("neg"):
        print("      负向：%s" % cut(e["neg"], 180))


def main():
    argv = sys.argv[1:]
    idx = load()
    if idx is None:
        return 1

    entries = idx["entries"]
    if not argv:
        print("词典：%d 条 / %d 部法典（建于 %s）"
              % (idx["entryCount"], len(idx["codexes"]), idx["builtAt"]))
        for c in idx["codexes"]:
            print("  %-18s %-26s %5d 条  %s"
                  % (c["id"], c["title"], c["count"], c["source"]))
        print("\n用法：python lexicon.py <关键词> | --exact <tag> | --cat | --in <分类>")
        print("      --codex <id> | --scene | --neg <关键词>")
        return 0

    mode = argv[0] if argv[0].startswith("--") else "--fuzzy"
    q = (argv[1] if argv[0].startswith("--") and len(argv) > 1 else
         ("" if argv[0].startswith("--") else argv[0])).strip()

    if mode == "--cat":
        print("词典：%d 条 / %d 部法典" % (idx["entryCount"], len(idx["codexes"])))
        for c in idx["codexes"]:
            subs = {}
            for e in entries:
                if e["c"] != c["id"]:
                    continue
                p = e.get("p") or ""
                parts = [x for x in p.split("/") if x]
                key = parts[0] if parts else "-"
                subs[key] = subs.get(key, 0) + 1
            print("\n[%s] %s —— %d 条" % (c["id"], c["title"], c["count"]))
            for k, v in sorted(subs.items(), key=lambda x: -x[1]):
                print("   %-24s %4d" % (k, v))
        return 0

    if mode == "--codex":
        hit = [c for c in idx["codexes"] if q.lower() in c["id"].lower()
               or q in c["title"]]
        if not hit:
            print("没有这部法典：%s" % q)
            return 1
        for c in hit:
            subs = {}
            for e in entries:
                if e["c"] != c["id"]:
                    continue
                parts = [x for x in (e.get("p") or "").split("/") if x]
                key = parts[0] if parts else "-"
                subs[key] = subs.get(key, 0) + 1
            print("[%s] %s —— %d 条 作者 %s %s"
                  % (c["id"], c["title"], c["count"], c["author"], c["version"]))
            for k, v in sorted(subs.items(), key=lambda x: -x[1]):
                print("   %-24s %4d" % (k, v))
        return 0

    if mode == "--in":
        hit = [e for e in entries if q and q in (e.get("p") or "")]
        if not hit:
            print("没有这个分类：%s（用 --cat 看全部）" % q)
            return 1
        print("%s —— %d 条" % (q, len(hit)))
        for e in hit:
            show(e)
        return 0

    if mode == "--scene":
        hit = [e for e in entries if e["c"] == "composition_style"]
        print("构图风格场景串 —— %d 条（1.5::光:: / 1.2::背景:: 是权重壳）" % len(hit))
        for e in hit:
            wh = e.get("wh") or []
            shape = ""
            if len(wh) == 2:
                shape = "横" if wh[0] > wh[1] else ("竖" if wh[1] > wh[0] else "方")
                shape = " [%s %dx%d]" % (shape, wh[0], wh[1])
            print("\n● %s%s" % (e.get("zh") or "", shape))
            print("  %s" % (e.get("t") or ""))
        return 0

    if mode == "--neg":
        hit = [e for e in entries if e.get("neg") and (
            q.lower() in (e.get("t") or "").lower()
            or q in (e.get("zh") or "")
            or q in (e.get("neg") or ""))]
        print("带负向的条目命中 %d 条" % len(hit))
        for e in hit[:15]:
            show(e, verbose=True)
        return 0

    if mode == "--exact":
        hit = [e for e in entries if q.lower() == (e.get("t") or "").lower()]
        if not hit:
            print("没有这个 tag：%s" % q)
            return 1
        for e in hit:
            show(e, verbose=True)
        return 0

    # 模糊查：中文标题优先，其次 tag，再次说明全文
    ql = q.lower()
    scored = []
    for e in entries:
        t = (e.get("t") or "").lower()
        zh = e.get("zh") or ""
        n = e.get("n") or ""
        if ql in t:
            scored.append((0 if t == ql else (1 if t.startswith(ql) else 2), e))
        elif q in zh:
            scored.append((3 if zh != q else 2, e))
        elif ql in n.lower():
            scored.append((4, e))
    if not scored:
        print("没查到：%s" % q)
        print("提示：中英都试一下，或用 --in 看分类名。")
        return 1
    scored.sort(key=lambda x: (x[0], x[1]["c"]))
    print("命中 %d 条（显示前 20）—— %s" % (len(scored), q))
    for _, e in scored[:20]:
        show(e, verbose=(len(scored) <= 3))
    if len(scored) > 20:
        print("\n……还有 %d 条，加 --in <分类> 收窄，或换个更准的词。" % (len(scored) - 20))
    return 0


if __name__ == "__main__":
    sys.exit(main())
