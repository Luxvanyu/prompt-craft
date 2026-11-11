---
name: prompt-craft
description: "任何「把想画的东西写成提示词」的任务都从这里进：先定七维（瞬间→明度→光→空间→色彩→材质→收尾），再按目标模型翻译成可编译的写法，最后过十道自检。当用户要写/改/升级图像提示词（MOSS / Anima / NAI / Midjourney / SD / Flux / 即梦 / 可灵），说「这张图好单调/平庸/AI 味/没设计感」，问审美提升、构图、打光、配色、氛围、电影感、摄影感，贴参考图要「学这个风格」「复刻这张」，或贴回出图说「不对/不像/机位错了」时加载。含：七维决策顺序与量化参数、12 个配方、12 个风格主头、景别/视角/构图表、字数预算、症状→改哪句索引、G1–G98 实测硬规则索引（尺寸标定、介质成像、印刷套印、序列一致性）、十道自检脚本与测图脚本。核心原则：先测再写、写完自检、出图验收，规则是诊断工具不是模板。"
---

# 提示词工坊（prompt-craft）

> 这是**唯一的入口**。决定「画什么、怎么画、写成什么」的那部分在本文档 + `references/`；
> 决定「MOSS 这一台机器会怎么执行」的实测规则在 `references/moss-rules.md` 与 `references/casebook.md`；
> 决定「像不像艺术」的那部分在 `references/aesthetic.md`。

---

## 三十秒上手

| 你现在的情况 | 直接跳 |
|---|---|
| 从零写一份提示词 | `references/entry.md`（十一个槽位填完就是草稿） |
| 有草稿，想变好看 | 本文档「七维决策」第 1–7 节 |
| 不知道用什么调子 | `references/style-heads.md`（12 个主头 + 6 层质感） |
| 不知道写多长 | `references/word-budget.md`（三档预算 + 八段切分 + 删减顺序） |
| 想控制大小/比例 | `references/moss-rules.md`（尺寸四把尺 + G46/G54/G64） |
| 出图不对 | `references/symptoms.md`（症状 → 改哪句 → 对应规则） |
| 贴了参考图要复刻 | 先 `scripts/probe.py` 量，再 `references/casebook.md` 找同类 |
| 想知道某条规则凭什么 | `references/casebook.md`（G1–G98 全部实测证据） |
| 想看还有什么题材没测过 | `references/gap-audit.md`（已验证 / 判死 / 不做） |

---

## 第一原则

> **一图一主张。** 一张图只允许有一个最高对比点、一个主导明度、一个主动作、一个色彩事件。其余全部降级为陪衬。

看到这句就够判断一张图了：画面上有两处一样抢眼，不是更丰富，是更模糊。

---

## 七维决策（顺序不能乱）

明度决定构图能不能立住，光决定明度，空间决定光能不能衰减，色彩是明度之上的一层，材质是光与色彩的接收面，收尾是最后一层薄膜。倒着做就会互相打架。

### 1. 瞬间（Moment）

不写「场景」，写**事情发生前后 0.3 秒**。

| 平均写法（死） | 瞬间写法（活） |
|---|---|
| a girl smiling | caught mid-laugh, eyes still on something just off frame |
| a man in the rain | crossing the street with a folded newspaper over his head, one shoulder already soaked |
| sitting by the window | she has just set the cup down and her hand is still open above it |

判据：这句话里必须有一个**未完成的动作**或**刚留下的痕迹**。都没有，就是摆拍。

### 2. 明度结构（Value plan）

压成三档 darks / mids / lights，两条铁律：

1. **一档主导**，占 55–70%，另两档分剩下的；绝不允许三等分。
2. **焦点 = 最高对比处**，不是最亮处，也不是最中心处。

> shadow 里最亮的亮部，必须比 light 里最暗的暗部更暗。

违反它，图永远「灰、脏、糊」——阴影漏光，明度阶梯被打断，眼睛找不到形。

**三档必须各给数量**（不给数量，「暗一点」会被执行成「暗一半」）：

```
The picture is low key: near black covers about half of it, the middle values hold the
figures, and the only thing that reaches one step short of white is X.
```

### 3. 光（Light）

五问答完才动笔：

| 问题 | 必须给的答案 | 例子 |
|---|---|---|
| 光源是什么 | 具体物件（但**不要给名词**，见下） | late sun through a dirty window / a phone screen |
| 方向 | 相对主体的方位 + 高度 | from camera left, slightly above eye line |
| 质量 | 硬 / 半硬 / 柔 | hard-edged, with no gradient at all |
| 色温 | 冷暖 + 相对差 | 3200K warm on skin against 6500K cold in the shadow |
| 比例 | key:fill 与 key:background，用 stops | key:fill 8:1（3 stops），背景比 key 低 2 stops |

stops→比值：0=1:1 · 1=2:1 · 2=4:1 · 3=8:1 · 4=16:1 · 5=32:1 · 6=64:1

**两个必踩的坑**：
- **不要给光源名词**。写 `tube` / `lamp` / `bulb` / `fixture` 就会被画进画面（G11/G41）。只写**落点 + 衰减 + 没照到哪里**。
- **衰减必须写**：`the light dies within arm's reach`——这比任何「dramatic lighting」有效。

### 4. 空间与镜头（Space & lens）

前中后景各司其职：前景遮挡/框景（虚）· 中景主体（唯一实焦）· 后景信息（低对比、低细节、低饱和）。

焦段决定心理：14–24mm 夸张纵深与不安｜35mm 叙事｜50mm 中性｜85–135mm 压缩与孤立｜200mm+ 窥视。

机位高度是最被忽视的杠杆：**低机位=压迫/英雄**，眼平=平等，高机位=审判/脆弱，贴地仰拍=贴地的不安。

**构图三件套（写具体位置，不写构图名词）**：
1. 主体在哪条分数线上（`she stands four tenths of the way across the frame`）
2. 另一侧是什么、有多空（`the right third holds nothing but pavement`）
3. 画框切了什么（头顶余量、脚有没有出框）

细节见 `references/composition.md`（景别 8 级 / 视角 5 种 / 构图 9 种 / 改构图 12 行症状表）。

### 5. 色彩（Color）

不做「配色方案」，做**角色分配 + 面积比**。四个角色各一个色，不许重复上岗：环境色（最大、最不饱和）/ 主体固有色 / 点缀色（最小、最高饱和）/ 中性锚。

面积比默认 **60 / 30 / 8 / 2**。一个 2% 的红点能让整张灰图活；一片 40% 的红只会让画面廉价。

**颜色必须落在被照亮的大面积上**（G9）——把颜色写在暗部或小物件上等于没写。阴影不要用纯黑，给一个色相偏移。

### 6. 材质（Material）

真实感不来自 `detailed`，来自**可见行为**：

| 别写 | 写可见行为 |
|---|---|
| wet hair | strands clumped and stuck to the cheek, a dark water line down the neck |
| wet shirt | the fabric gone dark and clinging, the inner layer showing through |
| water drops | each drop carrying a pinpoint specular highlight |
| leather | a bright band along each fold, the worn edge gone pale |
| wooden table | grain sharper at the near edge, the far end lost in falloff |

**不同材质必须不同细节级**——全图同一细节密度是 AI 味第三大成因，用景深分开最省力。

### 7. 收尾（Finishing）

一层薄膜，决定「这是照片」还是「这是渲染」：颗粒（尺寸/密度/分布）· halation（高对比边缘外溢 6–8px）· bloom（来源必须是画面里的光）· 暗角（只在需要压边时，且不对称）· 轻微失焦。

**默认叠粗颗粒**（除非用户说不要）：

```
One coarse visible grain layer over every surface without exception, each clump two to
three pixels across, and the grain sits over the whole frame evenly including the shadows.
```

---

## 反默认清单

模型的五个出厂设置，每个都要主动打掉一个：

| 出厂设置 | 症状 | 反制写法 |
|---|---|---|
| **居中对称** | 主体正中、地平线居中 | 主体放 0.33/0.66；另一侧显式写成空（G65） |
| **均光无向** | 处处亮、皮肤无立体 | 指定方向 + 质量 + 比例；`the fill side falls three stops under` |
| **纹理均质** | 皮肤布料墙面同一细节密度 | `sharp only on the face, everything past the shoulder already softening` |
| **平均脸** | 对称、无瑕、无记忆点 | `a slightly crooked nose, one eye a little narrower, freckles clustering unevenly` |
| **无瞬间** | 摆拍、素材库感 | 未完成的动作 / 刚留下的痕迹 / 视线还没落到镜头 |

**另外三个高频病灶**：用元素堆叠代替设计（加元素只会变吵）· 用形容词代替参数（`cinematic` `dramatic` 是空转）· 全图同一锐度（真实镜头只有一个焦平面）。

---

## 世界规则：模型不会照字面做的那一类

这一组是 160 多张出图反推出来的，违反任何一条都会整张返工。**完整证据在 `references/casebook.md`，摘要索引在 `references/moss-rules.md`。**

| 你以为写了就会 | 实际会发生 | 正解 | 规则 |
|---|---|---|---|
| 写「没有窗棂」 | 四重否认也照画窗格 | 给光一个**会产出正确形状的出处**（屋顶一道裂缝） | G80 补二 |
| 写「低机位贴水」 | 翻成站在岸边往下看 | 水面压窄 + 线要收 + 顶端留一条被切掉的边 | G84 / 补 / 补二 / 补三 |
| 写「这是倒影」 | 画成一块发光的东西躺在路上 | 倒影必须被水面事件打断（涟漪穿过时抖、边缘撕开） | G87 |
| 写「招牌」 | 一定长出可读的字 | 要零文字就**先别叫它招牌**，写成「只有光」 | G90 |
| 写「里面什么都没有」 | 会自己填满 | 写「里面装的是什么、什么颜色的」 | G44 |
| 写「路面毫无细节」 | 自动补上皮线、路缘 | 认下先验再规定它的样子 | G42 |
| 给光源名词 | 把灯画进画面 | 只写落点 + 衰减 + 未照亮区 | G41 |
| 写比例尺 | 人物照旧撑满画面 | 给**同深度水平带的对位句**（头顶比哪个边低多少） | G54/G56 |
| 提示词很长 | 人物被画大 1.3–2.9 倍 | 字数就是尺寸主因：默认 200–320 词 | G64 |
| 写「一个人走进来」这种名词组 | 先排人再上色，脸全清楚 | 要无脸就写「背对我们」 | G63 |
| 想让图「不像 AI」而加网点/像素 | 完全出不来 | 细小重复单元是死角（G97）；能活的是错位套印、线稿排线 | G96/G97 |
| 两个角色靠得近 | 两个头叠成一块 | 两个 bbox 上边差 ≥画高 8% + 明写空气间隙 | G93 |

---

## 尺寸控制（第二大返工来源）

模型的优先级是 **名字先验 > bbox > 比例句**。所以四把尺，按效果排序：

1. **去名尺**（最有效）：要小就别给它名字——不叫「马克杯」，写「一只带单柄的白釉圆柱」。
2. **公认尺 + 距离**：砖 24cm、地砖 30cm、门 2m、易拉罐 12cm，配上「离镜头几步」。
3. **同深度对位句**：`the top of her head sits a little below the top edge of the lockers`——**那条边必须在画面上水平贯穿**，且必须同一地面线。
4. **裁切尺**（唯一可靠做「巨大」的）：`her forehead runs out past the top edge`。

反过来要**大**，就写「她站在谁旁边」——模型保比值，会把参照物一起放大（G28/G29/G47/G54/G64）。

---

## 目标模型翻译

七维决策是**思考层**，不是输出层。落到具体模型时：

- **MOSS-Image**：普通场景用**纯 caption**（`{"caption":"..."}` 单键，200–320 词）；要精确物体互锁/多格/落字才用 Layout JSON。`bbox_coord_space:"abs"` + `bbox_format:"xyxy"` + 顶层 width/height。编译 `scripts/compile_prompt.py`。规则全集见 `references/moss-rules.md`。
- **Anima / NAI**：平铺 tag 串 + 画师串位置固定；一律只给正向。
- **Midjourney / SD / Flux**：自然语言长句 + 参数后缀（`--ar` `--stylize`），不要把 bbox 概念搬过去。
- **视频模型（可灵/即梦/Runway）**：同一套七维，但「瞬间」改成「一个连续动作」，且必须写**不动的那些东西**当锚。

---

## 交付前自检

### 自动（脚本）

```
python scripts/probe.py IMG                     # 出图后测：明度五档/近白面积/饱和方向
python scripts/lint.py DRAFT.json               # 草稿十道关（MOSS Layout 用）
python scripts/preview.py DRAFT.json --out L.png  # bbox 画出来看
python scripts/compile_prompt.py DRAFT.json --output OUT.txt
```

顺序固定：**预览 → 调 y → lint → 编译**。

### 手过（八条，逐条答得出来才算完）

1. 这张图的**一个主张**是什么？说不出来就重做。
2. 眯眼看，有**一个明确的明度结构**吗？还是一团灰？
3. 阴影里最亮处，仍暗于亮部最暗处吗？
4. 光有**方向和衰减**吗？
5. 主体在三分之一还是正中？正中是有意的吗？
6. 色彩四个角色**各司其职**吗？点缀色 ≤10% 吗？
7. 材质写了**可见行为**吗？不同材质细节级不同吗？
8. 有没有**形容词空转**（cinematic / beautiful / dramatic / masterpiece）？删掉。

默认纪律：**零文字、零质量词、零画师串、只给正向、默认叠颗粒层**（用户点名要才破）。

---

## 出图后怎么办

**不要重写整份提示词。** 按这个顺序：

1. `scripts/probe.py` 量数值（mean / dark / mid / nw / p99 / sat / lit vs shadow / soft / strong）。
2. `references/symptoms.md` 找症状 → 它指向「改哪一句」和对应规则编号。
3. 只改那一句，重跑 lint，只重出一张。
4. 新发现的机制写回 `references/casebook.md`，编号续下去。

**数值能证明「暗部总量不足」，不能证明「某个东西没有」**——这是最容易犯的判读错误（G53）。

---

## 这个包不含什么

- 不出图。它只负责写、验、诊断。
- `references/casebook.md` 里所有 G 编号都是**某一台模型（MOSS-Image）的实测结论**。换模型时，G1–G98 的「机制」多半仍然成立（那是提示词语义层面的），但具体阈值（词数、bbox 放大倍数）要重新标定。
- `references/gap-audit.md` 里标记「不做」的题材是有意的空白，不是遗漏。
