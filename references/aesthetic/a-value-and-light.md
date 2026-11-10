# 附录 A：明度与光

<!-- back -->
返回：`references/aesthetic.md`（审美内核正文）｜总入口 `SKILL.md`

明度是骨架，光是明度的成因。这两块必须一起做，因为"光打得好"这句话在提示词里没有意义，能落地的只有**方向 + 质量 + 比例 + 衰减**。

---

## 一、明度结构（Value plan）

### 为什么明度优先

强灰度构图能扛住任何配色；弱灰度构图，任何配色都救不了。先把画面压成黑白能读，再上色。这样换配色不会破坏结构。

### 三档压缩法

把整张图压成三个 family：**darks / mids / lights**。

三条硬规则：

1. **一档必须主导**，占 55–70%。绝不允许三等分（never even thirds）——均分等于没有主张。
2. **阴影内部要更平**：一个值，清掉所有漏光的小口袋。阴影里出现多个亮阶，就是"脏"的来源。
3. **高光内部要有 roll-off**：最亮处不是死白，是渐次衰减的。死白 = 数字渲染。

### 铁律

> shadow 里最亮的亮部，必须比 light 里最暗的暗部更暗。
> *The lightest lights in the shadows stay darker than the darkest darks in the light.*

这条是判断"灰""糊""脏"的唯一标准。违反了，明度阶梯就断，眼睛找不到形。

### 焦点 = 最高对比处

不是最亮处，不是最中心处，是**相邻明度差最大的那一小块**。

推论：
- 想让脸成为焦点，不必把脸照亮，只要让脸旁边有个深色块。
- 想让焦点弱，就把对比拉平——不需要遮挡它。

### 三种可命名的明度方案

| 方案 | 分布 | 气质 | 提示词写法 |
|---|---|---|---|
| **低调 Low-key** | darks 65% / mids 25% / lights 10% | 沉重、私密、危险 | `the frame is mostly held in the lower third of the tonal range, the highlights confined to a single small area` |
| **高调 High-key** | lights 60% / mids 30% / darks 10% | 干净、临床、漂浮 | `almost the whole frame sits in the upper range, the few darks isolated and small` |
| **全调 Full-range** | mids 55% / darks 25% / lights 20% | 纪实、可信、中性 | `a continuous tonal ramp with no clipped ends, both blacks and whites present but never large` |

### 诊断手法

- **眯眼测试**：半闭眼，halftone 消失，mass 显形。看到几个形？低于三个形 = 结构成立；一片均匀 = 重做。
- **缩略图测试**：缩到 200px，还认得出是什么 = 构图成立。
- **灰度测试**：去色后焦点还在原位 = 明度承担了焦点；焦点消失 = 你在靠颜色撑构图（脆弱）。

---

## 二、光

### 必须答完的五问

| # | 问题 | 不合格答案 | 合格答案 |
|---|---|---|---|
| 1 | 光源是什么 | soft light / studio lighting | a single bare 40W bulb two feet above her head / late sun through a dirty window / a phone screen turned face-up on the table |
| 2 | 方向 | from the side | from camera left, 30° above her eye line |
| 3 | 质量 | soft | hard-edged with a one-centimetre penumbra / wrapped and shadowless within a metre |
| 4 | 色温 | warm | 3200K on the skin, 6500K sitting cold in the shadow side |
| 5 | 比例 | high contrast | key:fill 8:1, background 2 stops under key |

### 比例换算

stops → 比值：**0=1:1 · 1=2:1 · 2=4:1 · 3=8:1 · 4=16:1 · 5=32:1 · 6=64:1**

常用取值：

| 场景 | key:fill | key:background | 备注 |
|---|---|---|---|
| 女性皮肤、柔美 | 2:1 – 2.5:1 | 1–2 stops under | 光要"绕过"阴影侧，不是切断 |
| 男性、硬朗 | 3:1 – 8:1 | 2–3 stops under | 允许硬阴影边缘 |
| 时装/广告平光 | 1:1 – 1.5:1 | 1 stop under | **但阴影边缘必须硬**，否则塌成塑料 |
| 戏剧/惊悚 | 8:1 – 32:1 | 3–4 stops under | 一半脸消失在黑里 |
| 夜景（Deakins 式） | 2.5:1 | 2–4 stops under | practical 2.5 stops over key |

**关键约束**：画面里不允许有比 key 更亮的背景物，除非那件东西就是焦点。这是"注意力不被偷走"的技术条件。

### practical（画面内可见光源）

practical 是最热的点，通常 **2.5 stops over key**。它的作用是：
1. 给观众一个"光从哪来"的物理解释（可信度）
2. 提供一个免费的高光锚点
3. 通过 halation 把周围空气"点亮"（氛围）

写法：`the bulb itself blown to pure white and bleeding a soft halo into the steam around it`。

### 衰减

光必须随距离掉。一句顶十句：

> `the light dies within arm's reach`

配 `the far wall is already three stops down` 一起用。这是把"平"变"深"的最短路径。

### 硬光 vs 柔光：不只是"边缘软硬"

| | 硬光 | 柔光 |
|---|---|---|
| 阴影边缘 | 锐利、可读出形状 | 模糊、无形状 |
| 质感 | **放大**（毛孔、皱纹、布纹全出来） | **抹平**（皮肤变塑料） |
| 立体感 | 靠明暗交界线 | 靠渐变 |
| 风险 | 显脏、显老、显廉价 | 显假、显 AI、无立体 |
| 用法 | 需要质感时用；打在**局部** | 需要干净时用；必须有方向 |

**最高频错误**：为了"好看"选柔光，结果全图无立体 → 这就是 AI 味第二大成因。正确做法是**柔光 + 明确方向 + 足够比例**，或者**硬光只打一小块**。

### 常见布光命名的实操含义

| 名字 | 实际几何 | 效果 | 提示词关键词 |
|---|---|---|---|
| Rembrandt | key 45° 侧上，阴影侧脸颊出现小三角光 | 古典、有体积 | `a small triangle of light on the shadow-side cheek` |
| Split | key 90° 正侧 | 一分为二、道德暧昧 | `the face divided cleanly down the nose bridge` |
| Loop | key 30–45° 侧上，鼻影成小环 | 通用美人光 | `a short shadow looping from the nose` |
| Butterfly | key 正上偏高 | 时尚、眼下小影 | `a small shadow directly under the nose` |
| Top / 顶光 | key 正上 | 眼窝黑、压迫、审讯 | `the eye sockets go black, the cheekbones catching everything` |
| Back / 逆光 | key 在主体后 | 剪影、边缘光、halation | `a hard rim tracing the shoulder, the face two stops under` |
| Uplight | key 从下 | 恐怖、不自然 | `lit from below, the shadows climbing upward` |

---

## 三、把光写成提示词的模板

按顺序填，一段话就够：

```
[光源物件] + [方向/高度] + [质量/边缘] + [色温对比] + [比例] + [衰减] + [practical]
```

实例（低调室内人像）：

> A single bare 40W bulb hangs a foot above her head, slightly camera-left, hard-edged with a one-centimetre penumbra; it burns 3200K into her skin while the shadow side sits cold at 6500K. Key to fill is eight to one, three stops. The light dies within arm's reach — the far wall is already three stops down and the corner is gone. The bulb itself is blown to pure white and bleeds a soft halo into the smoke.

实例（阴天平光，低对比但不塌）：

> Overcast north light, no direction you could point to, but the value structure holds anyway: her coat is the darkest mass at the bottom of the frame, the wall behind is a mid grey, and the only light area is the pale sky in the upper left. Nothing is over key, nothing is clipped.

注意第二例的关键：**光没有方向，但明度有结构**。低对比不等于低设计。

---

## 四、检查表

- [ ] 明度有主导档吗？（55–70%）
- [ ] 阴影内部是一个值，还是漏光的小口袋？
- [ ] 高光有 roll-off 吗，还是死白？
- [ ] 阴影最亮处 < 亮部最暗处？
- [ ] 五问全答完了吗（光源/方向/质量/色温/比例）？
- [ ] 有衰减句吗？
- [ ] 背景有没有比 key 更亮的物件？
- [ ] practical 是否 2.5 stops over？
- [ ] 柔光有没有配方向？（没方向=假）
- [ ] 硬光有没有打在局部？（打满=脏）
