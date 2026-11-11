# 提示词工坊（prompt-craft）

**一份能单独交付的提示词写作方法**：从「想画什么」到「可编译的提示词」，再到「出图后判断它错在哪一句」。

规则全部来自 174 张出图实验（G1–G98 编号，每条带实测数值），不是审美偏好。合并自 `moss-replica` 与 `aesthetic-core` 两个包。

---

## 1. 装到哪里

```
<skills 根目录>/prompt-craft/
├── SKILL.md                入口：七维决策 + 反默认清单 + 模型翻译 + 自检
├── references/
│   ├── entry.md                     填空式入口：00 三问 + 01–08 八槽 + 09/10 两闸，填完就是草稿
│   ├── aesthetic.md                 审美内核正文：为什么不好看、七维决策的哲学层
│   ├── aesthetic/                   附录 A–I（九个专题，按需加载）
│   │   ├── a-value-and-light.md     附录 A 明度与光
│   │   ├── b-composition.md         附录 B 构图
│   │   ├── c-color.md               附录 C 色彩
│   │   ├── d-material.md            附录 D 材质
│   │   ├── e-moment.md              附录 E 瞬间
│   │   ├── f-recipes.md             附录 F 配方（12 套调好参数的方案）
│   │   ├── g-translate.md           附录 G 翻译（七维如何压进 35 个标签）
│   │   ├── h-style-extraction.md    附录 H 风格提取（学这个风格的提取流程）
│   │   └── i-critique.md            附录 I 批评（出图后的诊断法）
│   ├── style-heads.md               12 个风格主头 + 6 层质感 + 互斥纪律
│   ├── word-budget.md               字数预算（450–1100 词三档怎么切、超了按什么顺序删）
│   ├── composition.md               景别 8 级 / 视角 5 种 / 构图 9 种 / 改构图症状表
│   ├── symptoms.md                  症状 → 改哪句 → 规则编号（出图不对时看这个）
│   ├── moss-rules.md                MOSS 实测规则正文 + 完整索引 G1–G98
│   ├── casebook.md                  G1–G98 的实测实录（证据层，要判据来这里）
│   ├── gap-audit.md                 缺口台账（已验证 / 判死 / 按规矩不做）
│   ├── decoupling.md                [P1] 强先验解绑协议：翅膀去光环、饮品去手拿、白裙去头纱三重切断法
│   ├── action-and-motion.md         [P2] 大动态与动作格斗库：四大动作相位、双手解剖闭环、羽翼气动力学
│   ├── multi-character.md           [P3] 双人战术对峙系统：四手全清点（Quad-Lock）、空间属性防火墙
│   ├── medium-and-optics.md         [P4] 介质成像与物理光学：水洼倒影物理证据链、雨窗防避让、纯物理光学
│   ├── battle-damage-and-couture.md [P5] 战损物理与机能装束：三级战损体系、焦羽抽丝、机能四层穿搭法
│   ├── mixed-lighting-and-split-tones.md [P6] 混合光源与色温分裂：主副光权力阶梯、暗部脊梁色彩隔离
│   ├── cinematic-geometries.md      [P7] 21:9宽银幕与极端机位：翼展全屏填塞、60度陡峭大俯拍四事实
│   ├── storyboard-and-continuity.md [P8] 序列叙事与漫画多格分镜：跨格角色硬锚定、BBox坐标硬隔离
│   └── scenery-and-scale.md         [P9] 无人空景与静物尺度：建筑模数不可动物理尺、厘米级三合一锁定
└── scripts/
    ├── probe.py                     测一张图：mean/dark/mid/nw/p1/p99/sat/lit/shadow/soft/strong/flat + 6×6 网格
    ├── lint.py                      草稿十三道关工业级自检（含先验解绑、动作解剖闭环、双人防串色、美学质感巡检）
    ├── preview.py                   把草稿的 bbox 画出来看
    ├── compile_prompt.py            草稿 → MOSS 官方编译格式（abs+xyxy → abs_centralized+yxyx）
    ├── verify.py                    参考图 vs 出图：逐项对照 + 6×6 差值矩阵 + 诊断清单 + 三联色差热图
    ├── render_krea2_html.py         Krea 2 独立渲染器：生成带一键复制与拆解表的 HTML 海报
    └── translate.py                 多引擎通用编译器：一键转 MOSS / NAI v5 3-tier / Anima 9-slot / Krea 2
```

依赖：`python` + `numpy` + `Pillow`。`preview.py` 找不到字体时会自动降级，不必改。

---

## 2. 五分钟上手

```bash
# ① 起草：按 entry.md 的 00–10 填槽位，产出 draft.json
# ② 看布局：bbox 画出来，检查人物有没有压中线、有没有超出画框
python scripts/preview.py draft.json --out layout.png
# ③ 自检：十三道关，退出码 1 = 有 FAIL
python scripts/lint.py draft.json
# ④ 编译成 MOSS 官方格式
python scripts/compile_prompt.py draft.json --output out.txt
# ⑤ 或一键跨引擎转译到 NAI v5 / Anima / Krea 2
python scripts/translate.py draft.json --target all
# ⑥ 出图后：先量，再对照症状表
python scripts/probe.py out.png
```

**顺序不能换**：预览 → 调 y → lint → 编译/转译。反过来会出现「lint 过了但 bbox 把人放在画面外」。

---

## 3. 三条铁律

1. **一图一主张**：一张图只讲一件事，每件道具都是这件事的证据物。两件事同时发生，人物就会被拆成两个。
2. **明度先于色彩**：先分配暗 / 中 / 亮三档各占多少面积，再谈颜色。颜色写在暗部等于没写。
3. **阴影最亮处必须暗于亮部最暗处**：这是硬光成立的定义。做不到就是阴天。

---

## 4. 十二条最容易翻车的

| # | 坑 | 一句话正解 |
|---|---|---|
| 1 | 人物总是画大 | **提示词长度是尺寸主因**：1000 词以上放大 1.3–2.9 倍；**character 块** 控到 200–320 词即回 1.0 倍（G64）。整份 caption 长度见 `references/word-budget.md` 三档 |
| 2 | 给比例句没用 | 比例句只是安全带；真正管用的是「头顶比某件同深度物体的哪条边低多少」，且那条边必须**水平贯穿**（G54/G56） |
| 3 | 人总是居中 | 模型听 bbox 不听形容词；bbox 中心要真的偏出 0.42–0.58 禁区（G65） |
| 4 | 灯被画进画面 | 光源不许给名词（tube/lamp/bulb/fixture 全禁），只写落点 + 衰减 + 未照亮区（G41） |
| 5 | 硬光变阴天 | 必须写边缘硬度：`cut like a blade, with no gradient at all`（G6） |
| 6 | 整张发灰 | 压亮度只能靠**暗部面积**；写「不是白是浅蓝灰」反而更亮 |
| 7 | 高调图飘 | 高调必须有黑锚点：`the darkest thing in the whole picture`（G4） |
| 8 | 小道具变巨物 | 名字先验 > bbox；占画面 2% 以下**不给 bbox**，写进它所在那块的 caption（G47/G67） |
| 9 | 场景自带的东西画错 | 「没有」一定失败，只能认下先验再规定它的样子（路面必有画线、水面必有涟漪、容器里必有东西）（G27/G42/G44） |
| 10 | 角色带着官方配件 | 光环 / 兽耳 / 校徽是「作品级通用件」，跨作品一律不继承（G66）；按 `decoupling.md` 解绑 |
| 11 | 光斑出来是窗格 | 四重否认也压不住；要给光一个**会产出正确形状的出处**（G80 补二） |
| 12 | 介质风格做不出来 | 细小重复单元（网点/像素/dither）判死（G97）；能活的是错位套印、线稿排线（G96/G98） |

---

## 5. 脚本速查

### probe.py — 单张实测

```bash
python scripts/probe.py IMG
python scripts/probe.py IMG --patch "0.1,0.2,0.3,0.4@左墙"
```

输出：`mean med dark mid bright nw p1 p99 rgb sat lit shadow soft strong flat`、6×6 明度网格、16×11 色块十六进制。

### lint.py — 十三道关

```bash
python scripts/lint.py draft.json
python scripts/lint.py draft.json --ref ref.png            # 加参考图对照（关 2/关 4）
python scripts/lint.py draft.json --intent blown,leak,tilt,soft   # 有意的过曝/漏光/歪/失焦
```

关：1 结构 / 2 数值 / 3 矛盾 / 4 覆盖 / 5 禁用 / 6 机位 / 7 世界逻辑 / 8 曝光 / 9 色彩落点 / 10 构图落位 / 11 先验解绑 / 12 动作与解剖锁定 / 13 美学质感与反八股（全 WARN，不拦交付）。

### verify.py — 参考图 vs 出图

```bash
python scripts/verify.py 参考图.png 出图.png --out-dir . --tag 名字
python scripts/verify.py 参考图.png 出图.png --no-map       # 只打表，不出热图
```

输出四块：逐项对照表（mean/med/dark/mid/bright/nw/p1/p99/sat/lit/shadow/soft/strong/hue/rgb）、
6×6 明度矩阵三张并排（参考 | 出图 | 差值）、诊断清单（`[严重]/[明显]/[轻微]`，每条带「该改哪句话」）、
三联对比图 `_verify_<tag>.jpg`（参考 | 出图 | 色差热图，**红得多＝差得多，黑＝一致**）。
退出码 1 = 有 `[严重]` 项。

### translate.py — 多引擎转译

```bash
python scripts/translate.py draft.json --target all
python scripts/translate.py draft.json --target nai      # NAI v5 / v4.5 (带负向)
python scripts/translate.py draft.json --target anima    # Anima
python scripts/translate.py draft.json --target krea2    # Krea 2
```

支持一键转译输出至 MOSS、NovelAI、Anima 与 Krea 2，并自动适配各引擎语法。

> **转译结果是起点，不是终点。** 脚本给的是骨架（基础 tag + 空间句），风格头、明度定调、材质可见行为仍需按 `references/style-heads.md` 手写；质量词与画师串一律不自动加——那是本 skill 第一条纪律。

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

---

---

## 5.5 依赖与换机器

| 依赖 | 必需？ | 缺了会怎样 |
|---|---|---|
| Python 3.9+ | **必需** | 所有脚本都跑不了 |
| numpy | **必需** | `lint.py` 直接 import 失败；`probe.py` / `verify.py` 的 `flat` 与梯度指标会退回 PIL 近似，与 lint 对不上 |
| Pillow 9+ | **必需** | `probe.py` / `verify.py` / `render_krea2_html.py` 跑不了 |
| json-prompt-visualizer 技能 | 可选 | 只影响 `canvas.py` 画布预览 |
| 系统中文字体 | 可选 | 只影响 `render_krea2_html.py` 生成的 HTML 字体回退 |

```bash
pip install numpy Pillow
```

**换机器要改的一处**：`references/casebook.md` 里 `canvas.py` 的命令写的是本机绝对路径，换成你自己 skills 目录下的对应路径即可。另外 `canvas.py` 的 `shortName()` 补丁没跟着本包分发，别人拿到的是原版——框头会退化成「物体」，不影响出图，只影响画布可读性。

**已知限制**：

- 所有阈值（词数、bbox 放大倍数、`flat` 的 0.35/0.55）都是在 MOSS-Image 上标定的。换模型时 G 编号的**机制**多半仍成立，但数值要重新测。
- `lint.py` 关 13 是启发式检查（正则 + 关键词表），宁可多报也不错放，WARN 不必逐条消掉。
- `verify.py` 的 `getdata()` 接口在 Pillow 14 会移除，本包已屏蔽告警，但届时需要换写法。

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

- **普通场景用纯 caption**，不要 JSON：`{"caption": "…"}` 单键。整份长度按 `references/word-budget.md` 三档（紧 450–550 / 标准 600–800 / 宽 850–1100）；**单个 character 块** 200–320 词。官方原话：*A detailed image does not automatically need Layout.*
- Layout 只留给：要落字的图 / 多格 / 几个物体位置必须精确互锁。
