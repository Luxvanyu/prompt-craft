#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""法典词典：一键下载 + 建索引（第一次用跑这个，之后不用再跑）。

    python fetch_lexicon.py                 下载五部法典并建 index.json
    python fetch_lexicon.py --packs         额外下载两个图包（42 MB，给 corpus.py 用）
    python fetch_lexicon.py --out DIR       指定输出目录
    python fetch_lexicon.py --no-download   只用本地已有的 JSON 重建索引

输出 `<out>/index.json`（约 1.8 MB / 7500+ 条，中英双向），lexicon.py 默认读这里。
加 `--packs` 会另外存两个图包原始 JSON（每个 17–25 MB），corpus.py 读它们；
图包**不进索引**（10958 条完整提示词塞进 index 会把文件撑到几十 MB），
索引只收五部「词表型」法典。

数据来源是社区法典站公开接口：
  https://novelai.quicktagcloud.com/data/<codex_id>.json
站点是 JS 壳，HTML 里没有数据；上面这个直链才是真数据（2026-11 实测可用）。
如果站点改版，跑 `--cat` 之外的办法：打开 data/codexes.json 看当前有哪几部法典。

五部法典的性质见 references/lexicon.md，两个图包的性质见 references/real-corpus.md：
社区整理，不是本包实测。
"""
import argparse
import datetime
import io
import json
import os
import sys
import urllib.request

for _s in (sys.stdout, sys.stderr):
    try:
        _s.reconfigure(encoding="utf-8")
    except Exception:
        pass

HERE = os.path.dirname(os.path.abspath(__file__))
BASE = "https://novelai.quicktagcloud.com/data/"
UA = "Mozilla/5.0 (compatible; prompt-craft-lexicon/1.0)"

# 只取这五部：带中文说明、带成品串、带负向，其余对写提示词没用
SOURCES = [
    ("raven", "raven_composition"),
    ("composition_style", "composition_style"),
    ("jiegou", "jiegou_yuandian"),
    ("kisegaeningyou", "kisegaeningyou"),
    ("qianteng", "qianteng"),
]

# 图包型法典：每条是完整提示词（正向+负向+参数），只给 corpus.py 用，不进索引
PACK_SOURCES = [
    ("nai5_community_pack", "NAI v5 社区图包"),
    ("nai45_community_pack", "NAI v4.5 社区图包"),
]


def fetch(codex_id, cache_dir):
    """下载一部法典；本地已有就直接用。返回 dict 或 None。"""
    local = os.path.join(cache_dir, codex_id + ".json")
    if os.path.exists(local):
        try:
            with io.open(local, encoding="utf-8") as f:
                return json.load(f)
        except Exception:
            pass  # 坏文件，重下
    url = BASE + codex_id + ".json"
    print("  下载 %s ..." % url, end=" ")
    try:
        req = urllib.request.Request(url, headers={"User-Agent": UA})
        with urllib.request.urlopen(req, timeout=60) as r:
            raw = r.read()
        d = json.loads(raw.decode("utf-8"))
        with io.open(local, "wb") as f:
            f.write(raw)
        print("%d 条 / %.1f KB" % (len(d.get("entries") or []), len(raw) / 1024))
        return d
    except Exception as e:
        print("失败（%s）" % e)
        return None


def build(codexes, out_dir):
    entries = []
    meta = []
    for cid, d in codexes:
        es = d.get("entries") or []
        meta.append({
            "id": cid,
            "title": d.get("title") or cid,
            "author": d.get("author") or "",
            "version": d.get("version") or "",
            "count": len(es),
        })
        for e in es:
            rec = {
                "c": cid,
                "t": (e.get("tags") or "").strip(),
                "zh": (e.get("title") or "").strip(),
                "n": (e.get("note") or "").strip(),
                "p": "/".join(e.get("path") or []),
            }
            if e.get("negative"):
                rec["neg"] = e["negative"].strip()
            if e.get("rating"):
                rec["r"] = e["rating"]
            w, h = e.get("imageWidth"), e.get("imageHeight")
            if w and h:
                rec["wh"] = [w, h]
            entries.append(rec)

    out = {
        "builtAt": datetime.date.today().isoformat(),
        "entryCount": len(entries),
        "codexes": meta,
        "entries": entries,
    }
    dst = os.path.join(out_dir, "index.json")
    with io.open(dst, "w", encoding="utf-8") as f:
        json.dump(out, f, ensure_ascii=False, separators=(",", ":"))
    print("\n写入 %s" % dst)
    print("  %d 条 / %d 部法典 / %.1f KB"
          % (len(entries), len(meta), os.path.getsize(dst) / 1024))
    for m in meta:
        print("  %-20s %-24s %5d 条" % (m["id"], m["title"], m["count"]))
    print("\n现在可以查了：python %s 逆光" % os.path.join(HERE, "lexicon.py"))
    return dst


def pull_packs(out_dir, offline):
    """下载两个图包。返回成功数。"""
    print("图包（给 corpus.py 用，不进索引）：取 %d 部" % len(PACK_SOURCES))
    ok = 0
    for codex_id, _title in PACK_SOURCES:
        if offline and not os.path.exists(os.path.join(out_dir, codex_id + ".json")):
            print("  跳过（无本地缓存）：%s" % codex_id)
            continue
        if fetch(codex_id, out_dir):
            ok += 1
    if ok:
        print("\n现在可以查了：python %s" % os.path.join(HERE, "corpus.py"))
    else:
        print("\n图包没下到。手动下载这两份放进 %s：" % out_dir)
        for codex_id, _ in PACK_SOURCES:
            print("  " + BASE + codex_id + ".json")
    return ok


def main():
    ap = argparse.ArgumentParser(description="下载法典数据并建词典索引")
    ap.add_argument("--out", default=os.path.join(HERE, ".lexicon"),
                    help="输出目录（默认 scripts/.lexicon）")
    ap.add_argument("--no-download", action="store_true",
                    help="只用本地缓存，不联网")
    ap.add_argument("--packs", action="store_true",
                    help="额外下载两个图包（42 MB，给 corpus.py 查完整提示词用）")
    ap.add_argument("--packs-only", action="store_true",
                    help="只下两个图包，不碰词典索引")
    a = ap.parse_args()

    out_dir = os.path.abspath(a.out)
    os.makedirs(out_dir, exist_ok=True)

    if a.packs_only:
        n = pull_packs(out_dir, a.no_download)
        print("\n提示：把 %s 加进 .gitignore，数据不入库。" % os.path.relpath(out_dir))
        return 0 if n else 1

    print("法典词典：取 %d 部" % len(SOURCES))
    got = []
    for cid, codex_id in SOURCES:
        if a.no_download and not os.path.exists(os.path.join(out_dir, codex_id + ".json")):
            print("  跳过（无本地缓存）：%s" % codex_id)
            continue
        d = fetch(codex_id, out_dir)
        if d:
            got.append((cid, d))

    if not got:
        print("\n一部都没拿到。检查网络，或手动下载这几份放进 %s：" % out_dir)
        for _, cid in SOURCES:
            print("  " + BASE + cid + ".json")
        if not a.packs:
            return 1
        print("\n先继续试图包。")
    else:
        build(got, out_dir)

    if a.packs:
        print()
        if not pull_packs(out_dir, a.no_download) and not got:
            return 1

    print("\n提示：把 %s 加进 .gitignore，数据不入库。" % os.path.relpath(out_dir))
    return 0


if __name__ == "__main__":
    sys.exit(main())
