#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Render Krea 2 prompts into a beautiful, self-contained HTML deliverable with copy controls."""

import argparse
import html
import json
import os
import re
import sys
from pathlib import Path


HTML_TEMPLATE = """<!DOCTYPE html>
<html lang="zh-CN">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>{page_title}</title>
<style>
  :root {{
    --bg: #0f1117;
    --card-bg: #1a1d27;
    --card-border: #2a2e3d;
    --text-primary: #e6e8ee;
    --text-secondary: #9ba1b0;
    --accent: #ff79c6;
    --accent-glow: rgba(255, 121, 198, 0.2);
    --cyan: #8be9fd;
    --green: #50fa7b;
    --yellow: #f1fa8c;
    --purple: #bd93f9;
  }}
  * {{ box-sizing: border-box; margin: 0; padding: 0; }}
  body {{
    font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, Helvetica, Arial, sans-serif;
    background-color: var(--bg);
    color: var(--text-primary);
    line-height: 1.6;
    padding: 30px 20px;
    display: flex;
    justify-content: center;
  }}
  .container {{
    max-width: 900px;
    width: 100%;
  }}
  header {{
    text-align: center;
    margin-bottom: 30px;
    padding-bottom: 20px;
    border-bottom: 1px solid var(--card-border);
  }}
  h1 {{
    font-size: 26px;
    font-weight: 700;
    color: var(--accent);
    margin-bottom: 8px;
    text-shadow: 0 0 15px var(--accent-glow);
  }}
  .intro {{
    color: var(--text-secondary);
    font-size: 15px;
  }}
  .card {{
    background: var(--card-bg);
    border: 1px solid var(--card-border);
    border-radius: 12px;
    padding: 24px;
    margin-bottom: 24px;
    position: relative;
    box-shadow: 0 8px 24px rgba(0,0,0,0.3);
  }}
  .card-header {{
    display: flex;
    justify-content: space-between;
    align-items: center;
    margin-bottom: 14px;
  }}
  .card-title {{
    font-size: 17px;
    font-weight: 600;
    color: var(--cyan);
    display: flex;
    align-items: center;
    gap: 8px;
  }}
  .copy-btn {{
    background: var(--card-border);
    border: 1px solid rgba(255,255,255,0.1);
    color: var(--text-primary);
    padding: 6px 14px;
    border-radius: 6px;
    font-size: 13px;
    cursor: pointer;
    transition: all 0.2s ease;
  }}
  .copy-btn:hover {{
    background: var(--accent);
    color: #fff;
    box-shadow: 0 0 10px var(--accent-glow);
  }}
  .prompt-content {{
    font-family: ui-monospace, SFMono-Regular, Menlo, Monaco, Consolas, monospace;
    font-size: 14px;
    line-height: 1.7;
    white-space: pre-wrap;
    word-break: break-word;
    color: #f8f8f2;
    background: #13151c;
    padding: 16px;
    border-radius: 8px;
    border: 1px solid rgba(255,255,255,0.05);
  }}
  .translation-content {{
    font-size: 14px;
    line-height: 1.8;
    color: var(--text-secondary);
    background: #13151c;
    padding: 16px;
    border-radius: 8px;
  }}
  .breakdown-table {{
    width: 100%;
    border-collapse: collapse;
    margin-top: 10px;
    font-size: 13.5px;
  }}
  .breakdown-table th, .breakdown-table td {{
    padding: 10px 14px;
    border: 1px solid var(--card-border);
    text-align: left;
  }}
  .breakdown-table th {{
    background: rgba(255,255,255,0.03);
    color: var(--purple);
    font-weight: 600;
  }}
  .breakdown-table td.slot-name {{
    white-space: nowrap;
    font-weight: 600;
    color: var(--yellow);
    width: 140px;
  }}
  .poem-box {{
    text-align: center;
    padding: 16px;
    margin-top: 10px;
    background: linear-gradient(135deg, rgba(255,121,198,0.1), rgba(189,147,249,0.1));
    border: 1px dashed var(--accent);
    border-radius: 8px;
    color: var(--accent);
    font-size: 16px;
    letter-spacing: 2px;
    font-family: "PingFang SC", "Hiragino Sans GB", "Microsoft YaHei", sans-serif;
  }}
  footer {{
    text-align: center;
    margin-top: 30px;
    font-size: 13px;
    color: var(--text-secondary);
  }}
</style>
<script>
function copyText(id, btn) {{
  const text = document.getElementById(id).innerText;
  navigator.clipboard.writeText(text).then(() => {{
    const old = btn.innerText;
    btn.innerText = "已复制 ✓";
    btn.style.background = "#50fa7b";
    btn.style.color = "#000";
    setTimeout(() => {{
      btn.innerText = old;
      btn.style.background = "";
      btn.style.color = "";
    }}, 1500);
  }}).catch(() => {{
    alert("复制失败，请手动选取复制");
  }});
}}
</script>
</head>
<body>
<div class="container">
  <header>
    <h1>{page_title}</h1>
    <p class="intro">{intro_text}</p>
  </header>

  <div class="card">
    <div class="card-header">
      <div class="card-title"><span>✦</span> 英文提示词 (Krea 2 Prompt)</div>
      <button class="copy-btn" onclick="copyText('krea-prompt', this)">复制提示词</button>
    </div>
    <div class="prompt-content" id="krea-prompt">{prompt_text}</div>
  </div>

  <div class="card">
    <div class="card-header">
      <div class="card-title"><span>✦</span> 中文对照解析 (Translation)</div>
      <button class="copy-btn" onclick="copyText('krea-translation', this)">复制翻译</button>
    </div>
    <div class="translation-content" id="krea-translation">{translation_text}</div>
  </div>

  <div class="card">
    <div class="card-title" style="margin-bottom: 14px;"><span>✦</span> 核心维度设计逻辑 (Breakdown Rationale)</div>
    <table class="breakdown-table">
      <thead>
        <tr>
          <th>维度模块</th>
          <th>设计考量与实测依据</th>
        </tr>
      </thead>
      <tbody>
        {breakdown_html}
      </tbody>
    </table>
  </div>

  <div class="poem-box">
    {poem}
  </div>

  <footer>
    <p>{signature}</p>
  </footer>
</div>
</body>
</html>
"""


def _strip_empty_blocks(html_text):
    """为空的可选块（诗、署名）剥掉外层容器，避免页面上留一个空框。"""
    import re as _re
    if _re.search(r'<div class="poem-box">\s*</div>', html_text):
        html_text = _re.sub(r'<div class="poem-box">\s*</div>\s*', '', html_text)
    if _re.search(r'<footer>\s*<p>\s*</p>\s*</footer>', html_text):
        html_text = _re.sub(r'<footer>\s*<p>\s*</p>\s*</footer>\s*', '', html_text)
    return html_text


DEFAULT_BREAKDOWN = [
    ("主体细节 (Subject)", "精准确立角色的辨识特征与服装剪裁，避免脸部平均化与肢体僵硬。"),
    ("画幅用途 (Canvas)", "采用黄金比例景深，为人物留足自然舒展与光影流动的物理空间。"),
    ("环境场景 (Environment)", "多层空间景深组织，道具作为故事物理证据，杜绝空洞单调。"),
    ("构图机位 (Composition)", "避开中线死区，三层透视与对角线引导，构筑电影级透视张力。"),
    ("光影影调 (Lighting)", "单一主导光明确方向与衰减比，受光面保色，暗部深沉不飘灰。"),
    ("风格媒介 (Style)", "高精动漫电影级数字插画风格，细腻线稿与柔和渐变交融。"),
    ("材质色彩 (Color)", "严守 60/30/8/2 色彩角色分配法则，主色与点缀色层次分明。"),
    ("质量保障 (Safeguard)", "全面剔除漂白词，末尾自然融合负向约束，保障肢体五官完美。"),
]


def render_html(data, output_path):
    title_cn = data.get("title_cn") or data.get("chinese_title") or "Krea2提示词"
    title_emoji = data.get("title_emoji", "🎬")
    page_title = f"{title_emoji} Krea 2 提示词 - {title_cn}"
    intro_text = data.get("intro_text", "由 prompt-craft 全流程深度定制，通过物理光影与七维决策驱动生成。")
    prompt_text = data.get("prompt_text") or data.get("prompt_en") or ""
    translation_text = data.get("translation_text") or data.get("translation_cn") or "暂无中文对照"
    poem = data.get("poem", "")
    signature = data.get("signature", "")

    rows = data.get("breakdown_rows", DEFAULT_BREAKDOWN)
    row_html_list = []
    for item in rows:
        if isinstance(item, (list, tuple)) and len(item) >= 2:
            s_name, s_rat = item[0], item[1]
        elif isinstance(item, dict):
            s_name = item.get("slot_cn") or item.get("slot") or item.get("module") or "维度"
            s_rat = item.get("rationale") or item.get("why") or item.get("logic") or ""
        else:
            continue
        row_html_list.append(
            f'<tr><td class="slot-name">{html.escape(s_name)}</td><td>{html.escape(s_rat)}</td></tr>'
        )
    breakdown_html = "\n        ".join(row_html_list)

    rendered = HTML_TEMPLATE.format(
        page_title=html.escape(page_title),
        intro_text=html.escape(intro_text),
        prompt_text=html.escape(prompt_text),
        translation_text=html.escape(translation_text),
        breakdown_html=breakdown_html,
        poem=html.escape(poem),
        signature=html.escape(signature)
    )
    rendered = _strip_empty_blocks(rendered)

    out_file = Path(output_path)
    out_file.parent.mkdir(parents=True, exist_ok=True)
    with open(out_file, "w", encoding="utf-8") as f:
        f.write(rendered)
    print(f"HTML rendered successfully: {out_file}")
    return out_file


def main():
    parser = argparse.ArgumentParser(description="Render Krea 2 Prompt HTML deliverable")
    parser.add_argument("--input", required=True, help="Input JSON file with prompt payload")
    parser.add_argument("--output", default="Krea2提示词/Krea2_prompt.html", help="Output HTML file path")
    args = parser.parse_args()

    with open(args.input, "r", encoding="utf-8") as f:
        data = json.load(f)

    render_html(data, args.output)


if __name__ == "__main__":
    main()
