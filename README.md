# 提示词工坊（prompt-craft）· 轻量版

**一份能单独交付的提示词写作方法**：从「想画什么」到「可编译的提示词」，再到「出图后判断它错在哪一句」。

规则全部来自 174 张出图实验（G1–G98 编号，每条带实测数值），不是审美偏好。合并自 `moss-replica` 与 `aesthetic-core` 两个包。

> **这是 `lite` 分支，轻量版。**
> 16 文件、十道关、`SKILL.md` 只有 246 行，脚本只有 4 个（probe / lint / compile_prompt / preview），没有多引擎翻译与参考图对比。适合想自己往上加东西时当起点。
>
> 完整版在 [`main` 分支](https://github.com/Luxvanyu/prompt-craft)：41 文件、十三道关、九期进阶工程（先验解绑 / 大动态格斗 / 双人战术对峙 / 介质光学 / 战损物理 / 双色温 / 极端机位 / 多格分镜 / 无人空景），另有 `translate.py` / `verify.py` / `render_krea2_html.py`。
> ```bash
> git clone https://github.com/Luxvanyu/prompt-craft.git prompt-craft-full
> ```
>
> **本版缺什么**（如果要用，按需从 `main` 搬）：lint 关 11 先验解绑、关 12 动作解剖闭环、关 13 美学质感巡检；`references/` 下的 `aesthetic/` 九篇附录与 P1–P9 进阶文档。

---

## 1. 装到哪里

```
<skills 根目录>/prompt-craft/
├── SKILL.md                入口：七维决策 + 反默认清单 + 模型翻译 + 自检
├── references/
│   ├── entry.md            填空式入口：十一个槽位填完就是一份草稿（从零起草先看这个）
│   ├── aesthetic.md        审美内核：为什么不好看、七维的哲学层、12 配方、风格提取、批评法
│   ├── style-heads.md      12 个风格主头 + 6 层质感 + 互斥纪律
│   ├── word-budget.md      字数预算（450–1100 词三档怎么切、超了按什么顺序删）
│   ├── composition.md      景别 8 级 / 视角 5 种 / 构图 9 种 / 改构图症状表
│   ├── symptoms.md         症状 → 改哪句 → 规则编号（出图不对时看这个）
│   ├── moss-rules.md       MOSS 实测规则正文 + 完整索引 G1–G98
│   ├── casebook.md         G1–G98 的实测实录（证据层，要判据来这里）
│   └── gap-audit.md        缺口台账（已验证 / 判死 / 按规矩不做）
└── scripts/
    ├── probe.py            测一张图：mean/dark/mid/nw/p1/p99/sat/lit/shadow/soft/strong + 6×6 网格
    ├── lint.py             草稿十道关自检
    ├── preview.py          把草稿的 bbox 画出来看
    └── compile_prompt.py   草稿 → MOSS 官方编译格式（与官方产物逐字一致）
```

依赖：`python` + `numpy` + `Pillow`。`preview.py` 找不到字体时会自动降级，不必改。

---

## 2. 五分钟上手

```bash
# ① 起草：按 entry.md 的 00–10 填槽位，产出 draft.json
# ② 看布局：bbox 画出来，检查人物有没有压中线、有没有超出画框
python scripts/preview.py draft.json --out layout.png
# ③ 自检：十道关，退出码 1 = 有 FAIL
python scripts/lint.py draft.json
# ④ 编译成 MOSS 官方格式
python scripts/compile_prompt.py draft.json --output out.txt
# ⑤ 出图后：先量，再对照症状表
python scripts/probe.py out.png
```

**顺序不能换**：预览 → 调 y → lint → 编译。反过来会出现「lint 过了但 bbox 把人放在画面外」。

---

## 3. 三条铁律

1. **一图一主张**：一张图只讲一件事，每件道具都是这件事的证据物。两件事同时发生，人物就会被拆成两个。
2. **明度先于色彩**：先分配暗 / 中 / 亮三档各占多少面积，再谈颜色。颜色写在暗部等于没写。
3. **阴影最亮处必须暗于亮部最暗处**：这是硬光成立的定义。做不到就是阴天。

---

## 4. 十二条最容易翻车的

| # | 坑 | 一句话正解 |
|---|---|---|
| 1 | 人物总是画大 | **提示词长度是尺寸主因**：1000 词以上放大 1.3–2.9 倍，200–320 词落到 1.0 倍（G64） |
| 2 | 给比例句没用 | 比例句只是安全带；真正管用的是「头顶比某件同深度物体的哪条边低多少」，且那条边必须**水平贯穿**（G54/G56） |
| 3 | 人总是居中 | 模型听 bbox 不听形容词；bbox 中心要真的偏出 0.42–0.58 禁区（G65） |
| 4 | 灯被画进画面 | 光源不许给名词（tube/lamp/bulb/fixture 全禁），只写落点 + 衰减 + 未照亮区（G41） |
| 5 | 硬光变阴天 | 必须写边缘硬度：`cut like a blade, with no gradient at all`（G6） |
| 6 | 整张发灰 | 压亮度只能靠**暗部面积**；写「不是白是浅蓝灰」反而更亮 |
| 7 | 高调图飘 | 高调必须有黑锚点：`the darkest thing in the whole picture`（G4） |
| 8 | 小道具变巨物 | 名字先验 > bbox；占画面 2% 以下**不给 bbox**，写进它所在那块的 caption（G47/G67） |
| 9 | 场景自带的东西画错 | 「没有」一定失败，只能认下先验再规定它的样子（路面必有画线、水面必有涟漪、容器里必有东西）（G27/G42/G44） |
| 10 | 角色带着官方配件 | 光环 / 兽耳 / 校徽是「作品级通用件」，跨作品不继承（G66） |
| 11 | 光斑出来是窗格 | 四重否认也压不住；要给光一个**会产出正确形状的出处**（G80 补二） |
| 12 | 介质风格做不出来 | 细小重复单元（网点/像素/dither）判死（G97）；能活的是错位套印、线稿排线（G96/G98） |

---

## 5. 脚本速查

### probe.py — 单张实测

```bash
python scripts/probe.py IMG
python scripts/probe.py IMG --patch "0.1,0.2,0.3,0.4@左墙"
```

输出：`mean med dark mid bright nw p1 p99 rgb sat lit shadow soft strong`、6×6 明度网格、16×11 色块十六进制。

**读法**：`lit / shadow` 是**饱和度的平均，不是明度**——亮部 sat 低于暗部 = 颜色全押在暗处（G9）。

**合格区间**：`mean` 0.38–0.55 · `dark` ≥0.08（low key 0.42–0.65）· `mid` <0.75 · `nw` <0.03 · `p1` <0.10 · `p99` 0.70–0.85 · `sat` ≥0.16 · `lit` ≥ `shadow`。

### lint.py — 十道关

```bash
python scripts/lint.py draft.json
python scripts/lint.py draft.json --ref ref.png            # 加参考图对照（关 2/关 4）
python scripts/lint.py draft.json --intent blown,leak,tilt,soft   # 有意的过曝/漏光/歪/失焦
```

关：1 结构 / 2 数值 / 3 矛盾 / 4 覆盖 / 5 禁用 / 6 机位 / 7 世界逻辑 / 8 曝光 / 9 色彩落点 / 10 构图落位。

### preview.py — 布局预览

```bash
python scripts/preview.py draft.json --out layout.png
python scripts/preview.py draft.json --img out.png --out overlay.png
```

画出所有 bbox + 面积占比 + 像素尺寸 + 中线偏移 + 三分线。

### compile_prompt.py — 编译

```bash
python scripts/compile_prompt.py draft.json --output out.txt
```

草稿用 `bbox_coord_space:"abs"` + `bbox_format:"xyxy"`；编译后变成官方的 `abs_centralized` + `yxyx`。

---

## 6. JSON 格式（MOSS Layout，官方）

```json
{
  "width": 1536, "height": 1024,
  "bbox_coord_space": "abs", "bbox_format": "xyxy",
  "summary": {"caption": "……", "canvas": "single"},
  "items": [
    {"label": "object",    "caption": "……", "bbox": [0, 0, 1536, 520]},
    {"label": "character", "caption": "……", "bbox": [300, 470, 470, 830]}
  ]
}
```

- **普通场景用纯 caption**，不要 JSON：`{"caption": "…"}` 单键，200–320 词。官方原话：*A detailed image does not automatically need Layout.*
- Layout 只留给：要落字的图 / 多格 / 几个物体位置必须精确互锁。
- `summary.canvas` 必须是字符串 `"single"`，不能是对象。

---

## 7. 换模型怎么办

`moss-rules.md` 与 `casebook.md` 里的 G 编号是**MOSS-Image 一台机器的实测**。

| 层 | 换模型后 |
|---|---|
| **机制**（名词先验 > bbox、否定句会变点名、场景自带先验压不住、介质语言必须写进主体块） | 多半仍然成立——它是提示语语义层面的 |
| **阈值**（1000 词放大 1.3–2.9 倍、bbox ×1.5/×2.4、p99 安全区 0.70–0.85） | 必须重新标定 |
| **格式**（Layout JSON / abs+xyxy） | 只对 MOSS 有效 |

换模型时的标定动作：同一场景只改一个变量（词数 / bbox / 一句话），跑三到五张，用 `probe.py` 量，把新数值写进 `casebook.md`，编号续下去。

---

## 8. 三个反复踩的 lint 坑（新 agent 必读）

| 关 | 现象 | 真相 | 怎么过 |
|---|---|---|---|
| 关 7 世界逻辑 | 明明写了「这个台子面朝房间」还是 WARN「有方向性场景没写朝向」 | `orient` 是一张**精确短语表**（`back to the wall` / `faces the wall` / `faces the road` / `facing out` …），近似写法一律不认 | 直接用表里的短语：`her back is to the wall`、`the bench faces the road` |
| 关 9 色彩落点 | 色相词写了不少，还是 WARN「中性色多于色相」 | 只统计 **`summary.caption`**，而且是**子串计数**：`grey green` 同时计入 `grey`（中性）和 `green`（色相）；`pale mint` 里的 `pale` 也算中性 | 大面颜色用不带修饰词的纯色相词：`a sage green celadon`、`a deep indigo black`；`pale` / `near white` 只留给小物件 |
| 关 6 机位 | 写了「倾斜」还是 WARN | 只写 `runs in at an angle` 不算 | 写死 `nothing in the picture is level and nothing in it stands plumb`；视平线写 `reads as a band across the upper third of the frame` |

另外：**bash heredoc 里写长 Python 会 `SyntaxError: unterminated string literal`**（换行断在字符串中间），必须先用写文件工具落地脚本再执行。

---

## 9. 这个包不含什么

- 不出图。它只负责写、验、诊断。
- 不含 LoRA 触发词、不含画师串、不含质量词——这是有意为之，不是缺内容。
- `gap-audit.md` 里标「不做」的题材是留白（比如默认不落字），不是遗漏。

---

## 10. 版本

**v1 · 2026-11-09**。合并自：
- `moss-replica` v2.1（117–174 号 174 张出图实测，G1–G98）
- `aesthetic-core`（七维决策、12 配方、风格提取、批评法，吸收自 `extract-visual-style-2` + `compose-this-scene.skill` + 景别/构图两份中文 skill）

两个源包仍然保留，`prompt-craft` 是它们的**唯一入口**：新任务从这里进，不必分别加载。
