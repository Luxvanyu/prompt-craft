# 审美内核（从 aesthetic-core 并入）

> 这一份回答「为什么就是不好看」。七维决策的**哲学层**在这里，操作层在 SKILL.md 与各 references。

---


## 正文

## 这份文档解决什么

单调的根因不是词少，是**每个维度都取了平均值**。

模型是平均机器：你说"一个女孩在房间"，它给你平均的脸、平均的窗光、平均的对称构图、平均的材质细节、平均的表情。每一项都不难看，叠在一起就是没有作者的图。

审美不是形容词的密度，是**承诺的密度**——在每一个可以选择的维度上，做一个明确、可被反驳的选择，并且让这些选择互相咬合。

所以这份文档不提供"更高级的词库"，它提供**决策顺序**和**可量化参数**。先决定，再把决定翻译成提示词。

---

## 第一原则

> **一图一主张。** 一张图只允许有一个最高对比点、一个主导明度、一个主动作、一个色彩事件。其余全部降级为陪衬。

看到这句就够判断一张图了：如果画面上有两处一样抢眼，它不是更丰富，是更模糊。

---

## 七维决策（按这个顺序做，每维必须落一个明确选择）

顺序不能乱：明度决定了构图能不能立住，光决定了明度，空间决定了光能不能衰减，色彩是明度之上的一层，材质是光与色彩的接收面，收尾是最后一层薄膜。倒着做就会互相打架。

### 1. 瞬间（Moment）

不写"场景"，写**事情发生前后 0.3 秒**。

| 平均写法（死） | 瞬间写法（活） |
|---|---|
| a girl smiling | caught mid-laugh, eyes still on something just off frame |
| a man in the rain | a man crossing the street with a folded newspaper held over his head, one shoulder already soaked |
| sitting by the window | she has just set the cup down and her hand is still open above it |
| looking at camera | her eyes have not found the lens yet, still tracking something past it |

判据：这句话里必须有一个**未完成的动作**或**刚留下的痕迹**。二者都没有，就是摆拍。

细节见 `references/05-moment.md`。

### 2. 明度结构（Value plan）

把画面压成三档：**darks / mids / lights**。然后强制两条：

1. **一档主导**，占 55–70%，另两档分剩下的。绝不允许三等分。
2. **焦点 = 最高对比处**，不是最亮处，也不是最中心处。

铁律（这条能救 80% 的图）：

> shadow 里最亮的亮部，必须比 light 里最暗的暗部更暗。
> *The lightest lights in the shadows stay darker than the darkest darks in the light.*

违反它的图，看起来永远"灰""脏""糊"——因为阴影漏光，明度阶梯被打断，眼睛找不到形。

阴影内部要**更平**：一个值，清掉所有漏光的小口袋。高光内部也要有 roll-off，不要死白。

判据：眯眼看（或缩到 200px），如果只剩一团均匀的灰，重做明度。

细节见 `references/01-value-and-light.md`。

### 3. 光（Light）

必须答完五问，一个都不能跳：

| 问题 | 必须给的答案 | 例子 |
|---|---|---|
| 光源是什么 | 具体物件，不是"柔光" | a single bare 40W bulb / late sun through a dirty window / a phone screen |
| 方向 | 相对主体的方位 + 高度 | from camera left, slightly above eye line |
| 质量 | 硬 / 半硬 / 柔 / 极柔 | hard-edged with a 1cm penumbra |
| 色温 | 冷暖 + 相对差 | 3200K warm on skin against 6500K cold in the shadow |
| 比例 | key:fill 与 key:background，用 stops | key:fill 8:1 (3 stops), background 2 stops under key |

**比例对照表**（stops → 比值）：0=1:1 · 1=2:1 · 2=4:1 · 3=8:1 · 4=16:1 · 5=32:1 · 6=64:1

常用区间：

- 女性/柔美皮肤 key:fill **2:1 – 2.5:1**
- 男性/硬朗/戏剧 **3:1 – 8:1**
- 商业广告、时装平光 **1:1 – 1.5:1**（但阴影边缘必须是硬的，见配方 5）
- key:background 通常**背景比 key 低 1–2 stops**；夜景/低调落 **2–4 stops under**
- 画面内可见光源（practical）是最热的点，常 **2.5 stops over key**
- **画面里不允许有比 key 更亮的背景物**（除非那件东西就是焦点）

**衰减**：光必须随距离掉。一句话写法——`the light dies within arm's reach`。这条比任何"dramatic lighting"都有效。

细节见 `references/01-value-and-light.md`。

### 4. 空间与镜头（Space & lens）

三个问题：**前中后景各自负责什么**、**焦段**、**机位高度**。

- 前景：遮挡 / 框景 / 质感对比（虚化的一块深色肩、一片叶子、门框）
- 中景：主体，唯一实焦
- 后景：信息或情绪，**必须比主体低对比、低细节、低饱和**

焦段决定透视，透视决定心理：

| 焦段 | 效果 | 用在 |
|---|---|---|
| 14–24mm | 夸张纵深、边缘拉伸、环境压迫 | 空间感、不安、纪实 |
| 35mm | 接近人眼、环境与人物并重 | 叙事、街拍 |
| 50mm | 中性、不干预 | 常规人像 |
| 85–135mm | 压缩、背景融化、脸被"抬举" | 美人、孤立感 |
| 200mm+ | 强压缩、层次叠压 | 城市压缩、窥视感 |

机位高度是被忽视的杠杆：**低机位=压迫/英雄**，**眼平=平等/记录**，**高机位=审判/脆弱**，**俯拍贴地=亲密/无助**。

构图的可审查五维（缺一项就稀释）：

1. **焦点层级**：一个主锚点 + 最多一个次锚点，其余压下去
2. **低活动区**：必须留出不打架的空域，否则焦点被噪声吃掉
3. **分组与剪影**：少数几个 mass，figure-ground 必须分开
4. **视觉流**：边缘/建筑线/光/姿态/视线给方向——且要和"人能走的路"分开标
5. **重量与尺度**：大小、对比、细节密度组织视觉重量；故意失衡不是错误，无意失衡才是

三分法/黄金比只是起点，不是标准。**要写就写具体位置**：`subject on the left third, the right two thirds left as empty wall`。

细节见 `references/02-composition.md`。

### 5. 色彩（Color）

不做"配色方案"，做**色彩角色分配 + 面积比**。

四个角色，各一个颜色，不许重复上岗：

1. **环境色**（最大面积，最不饱和）
2. **主体固有色**（第二面积，中等饱和）
3. **点缀色**（最小面积，最高饱和——就是那个"色彩事件"）
4. **肤色/中性锚**（把上面三者粘住的胶）

面积比默认 **60 / 30 / 8 / 2**。面积失衡会中和掉其它所有对比（Itten 的面积对比原则）——一个 2% 的红点能让整张灰图活，一片 40% 的红只会让画面变廉价。

七种可用的对比，一次只挑一到两种做主：

色相对比 · 明暗对比 · 冷暖对比 · 补色对比 · 同时对比（眼睛自动生成补色，所以大面积绿旁边的一点灰会读成粉）· 饱和度对比 · 面积对比

阴影不要用"黑"：给阴影一个**色相偏移**（偏青、偏蓝紫、偏暖褐），高光给一个**反向偏移**。这是"电影感"里最便宜也最有效的一步。

细节见 `references/03-color.md`。

### 6. 材质（Material）

材质的真实感不来自"detailed"，来自**可见行为**：

| 材质 | 别写 | 写可见行为 |
|---|---|---|
| 湿发 | wet hair | strands clumped and stuck to the cheek, a dark water line running down the neck |
| 湿布 | wet shirt | the fabric gone dark and clinging, the inner layer showing through |
| 水 | water drops | each drop carrying a pinpoint specular highlight, smaller ones beading |
| 皮革 | leather | a bright band along each fold, the worn edge gone pale |
| 旧金属 | old metal | bright scratches on the raised ridges, dark in the grooves |
| 木 | wooden table | grain sharper in the near edge, the far end lost in falloff |
| 布 | linen | washed many times, soft and slightly wrinkled, the fold shadows shallow |

**不同材质必须不同细节级**。模型默认给全图同一个细节密度，这是 AI 味第三大成因。用景深把前后景分开，是最省力的一刀。

细节见 `references/04-material.md`。

### 7. 收尾（Finishing）

一层薄膜，决定"这是照片"还是"这是渲染"：

- **颗粒**：大小（像素级）、密度、色度（是否带彩噪）、分布（中间调与暗部更密更大）
- **halation**：高对比边缘外溢一圈柔光，6–8px
- **bloom / diffusion**：高光周围的光晕，来源必须是画面里的光源
- **vignette**：只在需要压边时加，且要不对称
- **gate weave / 轻微失焦**：极少量，制造"手持"的物理感

颗粒已有既定写法（见用户 MEMORY 的粗颗粒层规则），此处不重复。

---

## 反默认清单（Anti-default）

AI 的五个出厂设置，每个都要主动打掉一个：

| 出厂设置 | 症状 | 反制写法 |
|---|---|---|
| **居中对称** | 主体正中、左右平衡、地平线居中 | `subject on the left third, the right side held open as empty space`；`horizon dropped to the lower quarter` |
| **均光无向** | 没有阴影方向、处处明亮、皮肤无立体 | 指定光源 + 方向 + 质量 + 比例；`the fill side falls three stops under` |
| **纹理均质** | 皮肤、布、墙、金属同一个细节密度 | `sharp only on the face, everything past the shoulder already softening` |
| **平均脸** | 对称、无瑕、无记忆点 | `a slightly crooked nose, one eye a little narrower, freckles clustering unevenly across the bridge, a few grey hairs at the temple` |
| **无瞬间** | 摆拍、情绪扁平、像素材库 | 写未完成的动作 / 刚留下的痕迹 / 视线还没落到镜头 |

**额外的三个高频病灶**：

- **元素堆叠代替设计**：加元素不会变丰富，只会变吵。宁可用一个大形状 + 一个空域。
- **形容词代替参数**：`cinematic` `beautiful` `dramatic` 是空转。换成 stops、焦段、面积比、方位。
- **全图同一锐度**：真实镜头只有一个焦平面。写清"哪里开始虚"。

---

## 自检（交付前逐条过）

1. 这张图的**一个主张**是什么？说不出来就重做。
2. 眯眼看，是否有**一个明确的明度结构**？还是一团灰？
3. 阴影里最亮处，是否仍暗于亮部最暗处？
4. 光有没有**方向和衰减**？还是均匀柔光？
5. 画面里有**比 key 更亮的背景物**吗？（有的话，它是不是焦点？不是就压下去）
6. 主体在**三分之一还是正中**？正中是有意的吗？
7. 有**留白/低活动区**吗？还是塞满了？
8. 色彩角色是否**四个各司其职**？点缀色面积是否 ≤10%？
9. 阴影有没有**色相偏移**，还是死黑？
10. 材质有没有写**可见行为**？不同材质是否不同细节级？
11. 是**瞬间**还是**摆拍**？
12. 有没有**形容词空转**（cinematic / beautiful / dramatic / masterpiece）？删掉。

---

## 输出格式对接

七维决策是**思考层**，不是输出层。落到具体模型时按用户的既有格式翻译：

- **MOSS**：平铺 tag 串 + 结尾一句英文锚点；画面含精确文字时改 JSON（bbox 分块，文字内容与位置单列 object 块）；不带 LoRA 触发词、不带质量词。
- **Anima**：人数 → 角色 → 作品 → 画师串 → 特征/场景/镜头标签顺排 + 一句英文描述；不用行前缀；描述里不出现 camera 一词。
- **NAI**：权重语法 + 画师串置顶。
- 一律**只给正向**，负面用户自管（除非明说要）。

翻译对照表、句式模板、以及"七维决策如何压进 35 个标签"的密度控制，见 `references/07-translate.md`。

---

## 配方库

12 个已经调好参数的完整方案（明度/比例/色/焦段/材质/颗粒 + 可粘贴英文），直接挑一个改内容即可，见 `references/06-recipes.md`。

## 从参考图提取风格

用户给图要"学这个风格"时，走提取流程而不是形容词模仿，见 `references/08-style-extraction.md`（含四类信息分离、三层规则、证据充分度、12 项冲突检查）。

## 出图后诊断

图出来了但"不对"时，按症状定位到具体维度并替换规则，而不是堆负面，见 `references/09-critique.md`。


---



# 附：01-value-and-light.md

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


# 附：02-composition.md

构图不是"三分法"，是一组**可被审查的决策**。审不出问题的构图，看起来就是"还行"——而"还行"正是单调。

---

## 一、五个可审查维度

每张图都过一遍，缺一项就会被稀释。

### 1. 焦点层级（Focal hierarchy）

一个**主锚点** + 最多一个**次锚点**，其余全部降级。

降级的手段（按性价比排序）：
1. 压对比（降低明度差）
2. 压细节（虚化）
3. 压饱和（去色）
4. 压面积（缩小）
5. 压位置（推到边缘）

**不要**用"遮挡"来降级——遮挡会变成新的形状，抢注意力。

### 2. 低活动区（Areas of lower activity）

画面里必须有一块"不打架"的空域。

空域的作用不是"留白好看"，是**给焦点腾出对比预算**。全是细节的画面，焦点和背景抢同一份注意力，结果谁都不突出。

写法：`the upper right two thirds is empty wall, deliberately flat and unlit`。

### 3. 分组与剪影（Grouping & silhouette）

把画面看成**少数几个 mass**，不是一堆物体。

判据：眯眼看，能数出几个形状？3–5 个 = 成立；10 个以上 = 没有构图，只有罗列。

figure-ground 必须分开：主体剪影要能脱离背景被单独认出来。分不开就调整明度或虚化，不要靠描边。

### 4. 视觉流（Visual flow）

给眼睛一条路，并且**这条路人走不了**。

- 边缘线、建筑线、透视线 → 指向焦点
- 光的方向、明度梯度 → 把视线推过去
- 姿态、手势、视线 → 最直接的箭头
- **"人能走的路"要另外标**：如果画面里的通道正好指向焦点，观者会"走进"画面，注意力被带到深处而不是主体上。这未必是错，但必须是有意的。

### 5. 重量与尺度（Weight & scale）

视觉重量由：面积 × 对比 × 细节密度 决定。

- 一个大而平的区域，重量可能小于一个小而密的高对比点。
- **故意失衡不是错误**（比如 90% 空 + 10% 主体），无意失衡才是错误。
- 尺度感需要一个**参照物**：人 vs 门、手 vs 杯子、鞋 vs 地砖。

---

## 二、非对称的六种做法

AI 默认居中对称。以下六种都是"打破但不乱"：

| 手法 | 写法 | 效果 |
|---|---|---|
| **三分之一偏置** | `subject on the left third, the right held open` | 最稳的破对称 |
| **前景遮挡** | `a dark out-of-focus shoulder fills the lower right corner` | 制造纵深 + 窥视感 |
| **框景** | `framed by the door opening, the frame edges dark` | 画中画，压缩空间 |
| **地平线偏离** | `horizon dropped to the lower quarter` | 天空成为主体 |
| **荷兰角** | `tilted a few degrees off level` | 不安，慎用，超过 8° 变廉价 |
| **偏心留白** | `the subject pushed to the extreme right edge, cut by the frame` | 出画感、被排斥感 |

**反例警告**：`centered composition` 不是错，但必须有理由（圣像式正面、绝对对称的建筑、刻意的压迫）。默认居中 = 没有决策。

---

## 三、空间：前中后景的职责

| 层 | 职责 | 技术手段 | 常见错误 |
|---|---|---|---|
| **前景** | 遮挡、框景、质感对比、纵深锚 | 虚化到只剩色块；或极近的锐利局部 | 前景太清晰，抢焦点 |
| **中景** | 主体，唯一实焦 | 全图最锐 | 中景塞两个主体 |
| **后景** | 信息或情绪，必须降级 | 低对比、低细节、低饱和、失焦 | 后景有亮点偷注意力 |

**空气透视**：后景越远，对比越低、越偏环境色、越亮（户外）或越暗（室内夜）。写一句 `the far end of the street dissolves into the same grey as the sky` 就能拉开三层。

---

## 四、镜头与透视

### 焦段的心理效应

| 焦段 | 透视 | 心理 | 用在 |
|---|---|---|---|
| 14–18mm | 极端纵深，边缘拉伸 | 空间压迫、不安、超现实 | 狭窄室内、废墟、俯冲 |
| 24mm | 强纵深 | 环境吞人 | 纪实、街头、建筑 |
| 35mm | 接近人眼，环境与人物并重 | 客观、叙事 | 故事场景、双人 |
| 50mm | 中性 | 不干预 | 通用人像 |
| 85mm | 轻微压缩 | 抬举、美化、隔离 | 美人、特写 |
| 135mm | 明显压缩，背景融化 | 孤立、窥视、优雅 | 时装、远景人像 |
| 200mm+ | 强压缩，层次叠压 | 城市压缩、疏离 | 街拍、体育、被观察感 |

**压缩的本质**：把不同距离的东西在画面上"贴"到一起。所以长焦能让远山压在人物肩后——这是"设计感"最便宜的一招。

### 机位高度

| 高度 | 效果 |
|---|---|
| 贴地 / 仰拍 | 主体变大、变英雄、变威胁；背景只剩天空 |
| 胸口 / 眼平 | 平等、记录、可信 |
| 略高（俯 15°） | 温和的俯视，看见桌面/地面信息 |
| 高位俯拍 | 审判、脆弱、几何化 |
| 正俯（top-down） | 图形化、去人化、平面设计感 |

### 景深

写清**哪里开始虚**，比写 `depth of field` 有效十倍：

- `sharp from her lashes to the collar, already soft at the shoulder`
- `only the near edge of the table is in focus, everything else is a wash`
- `deep focus, the back wall as crisp as her face`（少见，但极有设计感）

**深焦是一个被低估的审美选择**：全图都锐，逼你靠构图和明度而不是虚化来分层。这是"电影感"的另一半。

---

## 五、画幅

| 比例 | 适合 | 不适合 |
|---|---|---|
| 1:1 | 图形化、正面、社交媒体 | 叙事、纵深 |
| 4:5 | 人像、时装（竖） | 群像、环境 |
| 2:3 / 3:4 | 全身、竖构图 | 横向展开的动作 |
| 3:2 | 通用、横竖皆可 | — |
| 16:9 | 环境、叙事、宽银幕感 | 单人特写（两侧太空） |
| 21:9 | 极致横向、风景、孤独 | 竖向动作、多人 |
| 9:16 | 手机全屏、竖视频 | 横向空间关系 |

**横图的构图陷阱**：站姿 + 横画幅 = 两侧大片空白。横图优先用**沿水平轴展开的姿态**（侧卧、斜倚、并排、行走），或者让环境承担两侧（长廊、街景、桌面延伸）。

---

## 六、构图检查表

- [ ] 主锚点只有一个？次锚点 ≤1？
- [ ] 有低活动区吗？面积够吗？
- [ ] 眯眼能数出 3–5 个 mass 吗？
- [ ] 主体剪影能脱离背景单独认出吗？
- [ ] 视觉流指向焦点吗？"人能走的路"是否也指向焦点（是否有意）？
- [ ] 有尺度参照物吗？
- [ ] 对称是有意的吗？
- [ ] 前景虚够了吗？后景降级了吗？
- [ ] 焦段和机位是选过的，还是默认的？
- [ ] 写清了"哪里开始虚"吗？
- [ ] 画幅和姿态匹配吗（横图是否用了横向展开的姿态）？


# 附：03-color.md

配色方案（palette）是结果，不是决策。真正的决策是**角色分配 + 面积比 + 阴影色相**。

---

## 一、四个色彩角色

一张图最多四个颜色上岗，每个只干一件事：

| 角色 | 面积 | 饱和 | 职责 | 例子 |
|---|---|---|---|---|
| **环境色** | 最大（40–60%） | 最低 | 定调、托住一切 | 灰蓝的墙、褐的土、绿的雾 |
| **主体固有色** | 第二（25–35%） | 中 | 让主体被识别 | 大衣的驼、裙的深蓝 |
| **点缀色** | 最小（2–10%） | 最高 | 就是那个"色彩事件" | 一枚红扣、一点口红、一盏红灯 |
| **中性锚** | 5–15% | 最低 | 把上面三个粘住 | 肤色、木色、米白、炭灰 |

**面积比默认 60 / 30 / 8 / 2。**

### 面积对比原则（最常被违反的一条）

面积失衡会中和掉其它所有对比。一个 2% 的红点能让整张灰图活起来；一片 40% 的红只会让画面变廉价。

**补色对比的正确用法**：不是五五开，是 **95 : 5**。大面积的一方做底，小面积的一方做刺。

---

## 二、七种对比，一次只用一到两种

| 对比 | 机制 | 提示词写法 |
|---|---|---|
| **色相对比** | 不同色相并置 | `a warm ochre wall against cold blue shadow` |
| **明暗对比** | 明度差 | 见 01，最基础 |
| **冷暖对比** | 色温差 | `3200K skin against 6500K shadow` |
| **补色对比** | 色轮对面 | `a single orange bulb in a teal room` |
| **同时对比** | 眼睛自动生成补色 | 大面积绿旁边的一点灰会读成粉——**可以用来"免费"造色** |
| **饱和度对比** | 艳 vs 灰 | `everything desaturated except her mouth` |
| **面积对比** | 大 vs 小 | 见上 |

同时对比是个便宜伎俩但很好用：想让某个中性色"看起来有色"，就把它放在它的补色旁边。

---

## 三、阴影色相（cinematic 感的 cheapest win）

**阴影永远不要是黑。** 给阴影一个色相偏移，给高光一个反向偏移，画面立刻"有胶片味"。

| 风格 | 阴影偏 | 高光偏 | 提示词 |
|---|---|---|---|
| 冷调胶片 | 青 / 蓝紫 | 暖黄 | `shadows pushed toward cyan, highlights holding a faint amber` |
| 暖调怀旧 | 褐 / 暗红 | 米白 | `shadows sitting in warm brown, highlights bleached to cream` |
| 现代数字 | 中性偏蓝 | 中性 | `shadows clean and slightly blue, no cast in the highlights` |
| 反转片 | 品红 | 青 | `magenta in the shadows, cyan in the highlights` |
| 单色 | 同色相不同明度 | 同 | 见配方 10 |

**实现方式**：不是加滤镜词，是写**光源色温 + 环境反射**。`the shadow side picks up the cold blue of the window` 比 `teal and orange grade` 有效得多——后者会让模型给你一个廉价的 LUT。

---

## 四、色彩与明度的关系

**先明度，后色彩。** 顺序错了，换配色就崩。

具体做法：
1. 先决定 darks/mids/lights 的分布（01）
2. 再把颜色"填"进这三个档——每个档允许的颜色范围要收窄
3. 检查：去色后，三个档还分得开吗？

**常见错误**：一个高饱和色跨了两个明度档 → 明度阶梯被打断 → 画面"糊"。

规则：**高饱和只出现在一个明度档里**。要么在暗部（深红、墨绿），要么在亮部（浅黄、粉），不要跨越。

---

## 五、肤色的处理

肤色是唯一"不能随便调"的颜色，因为人眼对它有硬编码的敏感度。

- 肤色落在**中间调偏高**，且**永远比周围环境暖 200–400K**
- 阴影侧的肤色不要变灰，要变**深 + 偏冷**（不是去饱和）
- 高光侧的肤色不要过曝成白，要**保留一点色相**（`the highlight keeps a trace of red in it`）
- 男性皮肤 key:fill 可以到 8:1 而不"脏"，女性超过 3:1 就开始显硬

**反 AI 味的肤色**：写一个不均匀——`a faint flush across the nose and the tops of the ears, the rest of the face cooler`。真实皮肤的血色分布是不均的。

---

## 六、色彩方案速查（可直接套）

| 名字 | 环境 | 主体 | 点缀 | 阴影偏 | 气质 |
|---|---|---|---|---|---|
| **Deakins 夜** | 冷灰蓝 | 暖褐 | 钨丝灯的橙 | 青 | 孤独、精确 |
| **Kodak 日光** | 米白 / 浅黄绿 | 暖褐 | 一点红 | 偏青 | 怀旧、可信 |
| **青橙大片** | 青蓝 | 橙褐皮肤 | 白 | 深青 | 商业、力量（用滥了，慎用） |
| **莫兰迪** | 灰粉灰绿 | 灰蓝 | 无（靠明度） | 同色相压深 | 静、克制 |
| **霓虹双色** | 品红 | — | 青 | 品红 | 夜、躁 |
| **单色褐** | 褐阶 | 褐阶 | 米白 | 暖深褐 | 老照片、纪实 |
| **高调白** | 白 / 米 | 浅灰 | 一点黑 | 极浅灰蓝 | 临床、干净 |
| **墨绿+铜** | 墨绿 | 铜 / 黄铜 | 暖白 | 深墨绿 | 古典、图书馆 |

---

## 七、检查表

- [ ] 四个角色各司其职？有没有颜色在打两份工？
- [ ] 点缀色面积 ≤10%？
- [ ] 只用了 1–2 种对比？
- [ ] 阴影有色相偏移吗，还是死黑？
- [ ] 高光有反向偏移吗？
- [ ] 高饱和是否只在一个明度档里？
- [ ] 去色后明度结构还在吗？
- [ ] 肤色是否比环境暖？阴影侧是否"深+冷"而不是"灰"？
- [ ] 有没有用 `teal and orange` 这类会触发廉价 LUT 的词？（有就换成物理描述）


# 附：04-material.md

材质不是"detailed"，是**可见行为**。Finishing 不是"film grain"，是**一层有物理参数的薄膜**。

---

## 一、材质的核心原则

> 真实感 = 材料在特定光下的**反应**，不是材料的名字。

同一个"皮革"，在硬侧光下是"折面亮带"，在柔光下是"哑光的一片"。所以材质描写必须和光绑定。

---

## 二、材质字典（按可见行为写）

### 布

| 材料 | 可见行为 | 提示词 |
|---|---|---|
| 棉 | 折痕浅、边缘毛、吸光 | `cotton gone slightly fuzzy at the seam, the folds shallow and matte` |
| 亚麻 | 洗过多次、软、微皱 | `linen washed many times, soft and slightly wrinkled, the fold shadows shallow` |
| 丝 | 折面反光、明暗跳变 | `silk where each fold flips from dark to a hard bright line` |
| 羊毛 | 吸光、边缘绒 | `wool eating the light, the edge of the shoulder a soft halo of fibre` |
| 湿布 | 变深、贴身、透内层 | `the fabric gone dark and clinging, the inner layer showing through` |
| 旧布 | 磨白、起球 | `the elbow worn pale, small pills across the surface` |

### 皮肤

| 状态 | 可见行为 |
|---|---|
| 干 | 细纹、哑光、粉感 |
| 油/汗 | 鼻梁、额角、锁骨一点镜面高光 |
| 湿 | 成束的头发贴脸、颈侧一道暗水线 |
| 冷 | 鼻尖与耳尖泛红、唇色退 |
| 老 | 眼周细纹、手背血管、颈纹 |

**反平均脸**：`a slightly crooked nose, one eye a little narrower than the other, freckles clustering unevenly across the bridge, fine lines at the outer corners, a few grey hairs at the temple`

### 金属

| 状态 | 可见行为 |
|---|---|
| 新/抛光 | 干净的环境反射、边缘锐利 |
| 旧 | 凸缘亮划痕、凹槽暗、氧化发乌 |
| 黄铜 | 亮处偏黄、暗处偏绿褐 |
| 湿金属 | 水膜让反射变形，滴处有针尖高光 |

`old brass: bright scratches along the raised ridges, dark and green in the grooves`

### 木

`grain sharper at the near edge, the far end already lost in falloff; the varnish gone cloudy in a ring where a glass stood`

### 玻璃 / 水

- 玻璃：**两层反射**（前表面 + 后表面），错位一点
- 水：每滴水一个针尖高光；小的成珠，大的有暗底
- 蒸汽：只在光源附近可见，远离光源就消失

`each drop carrying a pinpoint specular highlight, the smaller ones beading, the larger ones holding a dark centre`

### 纸 / 印刷

`the paper gone slightly wavy from humidity, the ink sitting on top of the fibre rather than in it`

### 头发

| 状态 | 可见行为 |
|---|---|
| 干、蓬 | 单根可见、边缘飞丝、有体积 |
| 干、顺 | 成片高光带（不是一根根） |
| 湿 | 成束、贴头皮、暗水线、发梢分叉 |
| 油 | 根部暗、成缕 |

`wet hair clumped into strands stuck to the cheek, a dark water line running down to the collar`

---

## 三、细节密度：AI 味的第三大成因

模型给全图**同一个细节密度**。真实镜头不是。

三种分层方式：

1. **景深分层**（最省力）：`sharp from her lashes to the collar, already soft at the shoulder`
2. **材质分层**：近处的布看得见织纹，远处的墙只有色块
3. **光分层**：亮部细节多，暗部细节被吃掉

写一句就够：`detail only where the light actually lands, everything in the shadow reduced to a flat shape`

---

## 四、磨损：让东西"用过"

新的东西看起来假，因为真实世界的东西都被用过。

| 物件 | 磨损写法 |
|---|---|
| 皮包 | `scuffs at the corners, the strap darkened where a hand holds it` |
| 鞋 | `the toe creased, the sole edge worn uneven` |
| 桌 | `a ring where a glass stood, the varnish cloudy there` |
| 墙 | `a patch where something was removed, the paint a shade lighter` |
| 书 | `the spine cracked, the corner of the cover turned up` |
| 金属 | `fingerprints dulling the polish where it is handled` |

一句 `well-used, not worn out` 能顶很多形容词。

---

## 五、Finishing：五层薄膜

按顺序叠，每层都有物理参数。

### 1. 颗粒（Grain）

| 参数 | 取值 | 说明 |
|---|---|---|
| 大小 | 2–3 px/颗粒 | 更小=数字，更大=高感胶片 |
| 密度 | 中间调与暗部更密 | 高光里更稀 |
| 色度 | 带轻微彩噪 or 纯灰 | 彩噪=消费级胶片，纯灰=精细扫描 |
| 分布 | 随机、均匀、成团 | 暗部成 4px 的软团 |
| 高光 | 保留"齿感"，不死白 | 关键：高光也有颗粒 |

已有既定写法（用户 MEMORY 的粗颗粒层规则），此处不重复参数，只强调：**颗粒是"物理屏幕"，写在最前面，作用于全图**。

### 2. Halation（光晕溢出）

高对比边缘外溢一圈柔光，**6–8px**。来源是胶片背层的反射。

`a wide soft halation bleeding six to eight pixels around every high-contrast edge`

只在**高光与暗部交界**处出现，不是全图发光。

### 3. Bloom / Diffusion（柔光罩）

高光周围的光晕，**必须来自画面里的光源**。

- 光源附近：明显
- 远离光源：无
- 错误写法：`dreamy glow`（全图发光=廉价）
- 正确写法：`the bulb bleeding into the steam around it, the corners unaffected`

### 4. Vignette（暗角）

只在需要压边时加，且要**不对称**——真实镜头的光学暗角不对称。

`a slight falloff in the lower left corner only`

### 5. Gate weave / 轻微失焦 / 色差

极少量，制造物理感：
- `a hair of chromatic fringing on the high-contrast edge`
- `the frame very slightly unsteady, as if hand-held`
- `the extreme corner soft, the centre clean`

---

## 六、材质检查表

- [ ] 每个材质写了**可见行为**，还是只写了名字？
- [ ] 材质描写和光绑定了吗？（硬光下的皮 vs 柔光下的皮）
- [ ] 不同材质有**不同细节级**吗？
- [ ] 有磨损/使用痕迹吗？
- [ ] 湿/干状态写清了吗？
- [ ] 颗粒：大小/密度/高光齿感/暗部成团 都写了吗？
- [ ] Halation 只在边缘，不是全图？
- [ ] Bloom 只来自光源？
- [ ] 有没有 `dreamy` `glow` `soft light everywhere` 这类会全图发光的词？


# 附：05-moment.md

一张图能"活"，靠的不是表情，是**未完成的动作**。

---

## 一、场景 vs 瞬间

| 场景（死） | 瞬间（活） |
|---|---|
| a woman smiling | caught mid-laugh, eyes still on something just off frame |
| a man in the rain | crossing the street with a folded newspaper over his head, one shoulder already soaked |
| a girl by the window | she has just set the cup down and her hand is still open above it |
| a couple arguing | he has stopped mid-sentence, her hand still on the door handle |
| a woman reading | her finger still holding the page she was about to turn |
| looking at the camera | her eyes have not found the lens yet, still tracking past it |

**判据**：这句话里必须有一个**未完成的动作**或**刚留下的痕迹**。两者都没有，就是摆拍。

---

## 二、四种制造瞬间的机制

### 1. 未完成动作（incomplete action）

抓在动作中段，不是起点也不是终点。

`mid-stride, the trailing foot still off the ground`
`his hand still raised, the knock not yet landed`

### 2. 残留痕迹（residue）

动作已经结束，但物理证据还在。

`the cup still rocking slightly in its saucer`
`a dent in the cushion where someone just stood up`
`steam still curling where the pot was lifted`

残留痕迹是最高级的写法，因为它同时给了"刚发生"和"将发生"，而画面本身是静止的。

### 3. 视线未落（unresolved gaze）

看的方向不是镜头，而且镜头外有明确的东西。

`looking at something past the left edge of the frame, not at us`
`eyes down and to the side, reading something on the table we cannot see`

### 4. 身体不均衡（asymmetric weight）

站得"正"= 摆拍。真实的人总是重心偏一边。

`weight on one hip, the other leg relaxed and slightly bent`
`leaning into the door frame with one shoulder`

---

## 三、情绪的物理载体

不要写情绪词，写**情绪的物理表现**。

| 情绪 | 别写 | 写 |
|---|---|---|
| 疲惫 | tired | `the shoulders dropped, the jaw slack, blinking slower than the light changes` |
| 紧张 | nervous | `the thumb working the edge of the sleeve, the breath held high in the chest` |
| 愤怒 | angry | `the jaw set, the nostrils flared slightly, the eyes not moving` |
| 悲伤 | sad | `the mouth held in a flat line, the eyes wet but not spilling` |
| 期待 | hopeful | `leaning forward slightly, the weight already on the front foot` |
| 冷漠 | cold | `no expression at all, the face held still, the eyes flat and unhurried` |
| 心动 | in love | `the pupils wide, the mouth slightly open, caught before speaking` |

**最强的一招：写"忍住"**。情绪被压住的瞬间，比释放出来更有张力。

`the mouth trying not to move`
`holding still on purpose`
`the smile arriving and then being stopped`

---

## 四、多人场景的叙事

多人图最容易变成"几个人并排站着"。解法是给每个人**不同的时间点**。

- A 已经做完（残留痕迹在他身上）
- B 正在做（未完成动作）
- C 还没开始（视线/预备姿态）

这样一张静止的图就有了时间轴。

同时注意：**每个人的视线要指向不同的东西**，否则会读成"他们在看同一个东西"（除非那正是你要的）。

---

## 五、服装与道具的叙事

衣服和道具不是装饰，是**信息**。

| 细节 | 说明什么 |
|---|---|
| 袖子挽起、袖口有水 | 刚在做事 |
| 一只袜子没穿好 | 匆忙 |
| 领口松了、头发乱了 | 刚被拉扯过 / 刚睡醒 |
| 手里握着没点着的烟 | 在犹豫 |
| 包带压在肩上留下痕 | 背了很久 |
| 鞋跟磨偏 | 走路姿势 / 长期穿着 |
| 桌上有两副餐具，一副没动 | 有人没来 |

**"第二副餐具没动"这类写法，是叙事密度的核心**：画面里有一个"不存在的角色"。

---

## 六、构图与情绪的对位

| 情绪 | 构图 | 光 | 空间 |
|---|---|---|---|
| 孤独 | 大面积空域，主体偏角 | 单一光源，周围全暗 | 长焦压缩 or 极广角拉开 |
| 压迫 | 主体被框住、贴边、上方有重物 | 顶光，眼窝黑 | 低机位 + 广角 |
| 自由 | 主体小，天空/海面大 | 高调，逆光 | 广角，地平线低 |
| 亲密 | 极近、局部、遮挡 | 柔光但有方向 | 长焦 + 浅景深 |
| 不安 | 荷兰角、失衡、前景遮挡 | 硬光 + 强衰减 | 广角 + 近前景 |
| 静 | 对称、水平线、留白 | 平光但明度分层 | 中焦，深焦 |
| 欲望 | 局部特写、皮肤、湿 | 侧逆光、边缘光 | 长焦，浅景深 |
| 威胁 | 背光剪影、低机位 | 逆光 + 无 fill | 广角，逼近 |

---

## 七、检查表

- [ ] 有未完成的动作吗？
- [ ] 有残留痕迹吗？
- [ ] 视线落在镜头外吗？
- [ ] 身体重心是偏的吗？
- [ ] 情绪写的是物理表现还是形容词？
- [ ] 多人场景里，每个人在不同时间点吗？
- [ ] 有"不存在的角色"的痕迹吗（第二副餐具）？
- [ ] 构图/光/空间和情绪对位吗，还是随便配的？


# 附：06-recipes.md

每个配方给：明度分布 / 比例 / 光源 / 色彩四角色 / 焦段机位 / 材质重点 / finishing / **可粘贴英文段**。

用法：挑一个最接近气质的，把英文段里的内容换掉，参数不要动。参数是这些配方的全部价值。

---

## 配方 1 · Deakins 夜（孤独、精确、克制）

- **明度**：darks 70% / mids 22% / lights 8%
- **比例**：key:fill 2.5:1（皮肤）；background 2–4 stops under；practical 2.5 stops over key
- **光源**：一盏画面内可见的钨丝灯（桌灯/吊灯/走廊灯），从上方偏侧；硬边小光源；3200K vs 环境 6500K
- **色彩**：环境冷灰蓝 / 主体暖褐 / 点缀钨丝橙 / 中性肤色；60:30:8:2
- **焦段机位**：35–50mm，眼平或略高
- **材质**：深色木、旧金属、哑光墙；只有被灯照到的表面有细节
- **finishing**：颗粒中等偏粗；halation 明显（灯周围）；无 bloom

```
A single tungsten bulb above the table is the only source, hard-edged, 3200K. It is the hottest thing in the frame at two and a half stops over key; the table surface two stops over; her skin sits at key and falls to one stop under on the shadow side. The room behind is between two and four stops under and there is nothing in it brighter than key. The light dies within arm's reach. Key to fill is two and a half to one.
```

---

## 配方 2 · 单窗光（私密、室内、可信）

- **明度**：mids 55% / darks 30% / lights 15%
- **比例**：key:fill **8:1（3 stops）**；背景 2 stops under
- **光源**：一扇侧窗，光从窗口斜进来；半硬（窗框投出软边影）；日光 5600K，室内反射偏暖
- **色彩**：环境灰米 / 主体固有色中饱和 / 点缀一处小高饱和 / 肤色暖
- **焦段机位**：50mm 或 85mm，眼平
- **材质**：窗玻璃的两层反射、窗台的灰、布的折痕（近处可见织纹）
- **finishing**：颗粒细到中；窗框边缘 halation；暗角在窗的对面

```
North daylight through a single window on camera left, half-hard, the window frame throwing a soft-edged shadow across the floor. Key to fill is eight to one — three stops — and the side away from the window is gone. The far wall is two stops under key. The window glass holds two reflections, offset slightly.
```

---

## 配方 3 · 阴天平光（低对比但不塌）

- **明度**：mids 60% / darks 25% / lights 15%——**靠固有色和明度分层，不靠方向光**
- **比例**：key:fill 2:1（几乎没有方向）；background 1 stop under
- **光源**：全天空，无方向；但**必须有明度结构**
- **色彩**：这是配方的核心——环境灰蓝、主体深色 mass、一处浅色高光区（天空/白墙）
- **焦段机位**：35mm，眼平（纪实感）
- **材质**：这是材质的配方——无方向光下所有纹理都平，所以要靠**固有色差**和**湿度**制造层次（湿路面、湿墙）
- **finishing**：颗粒中等；无 halation（没有强高光）；饱和度整体压 15%

```
Overcast, no direction you could point to. The structure comes from mass, not light: her dark coat is the heaviest shape at the bottom of the frame, the wall behind is a mid grey, and the only light area is the pale sky in the upper left. Nothing is over key, nothing is clipped, nothing is pure white. Everything is slightly wet and the wet surfaces are a shade darker than the dry ones.
```

**关键**：低对比 ≠ 低设计。没有方向光时，明度结构必须靠**固有色**承担。

---

## 配方 4 · 黄金逆光（剪影、halation、情绪）

- **明度**：lights 45% / darks 40% / mids 15%——**双极分布，中间调最少**
- **比例**：主体欠曝 1.5–2 stops（相对背景）；背景（天空/水面）过曝 2 stops
- **光源**：低角度太阳在主体正后方偏 15°；极硬；3200–4000K
- **色彩**：环境金橙 / 主体近黑剪影 / 点缀暖白高光 / 无中性锚（剪影里没有肤色）
- **焦段机位**：85–135mm，略低机位
- **材质**：头发边缘的飞丝是主角（逆光下发丝发亮）；薄织物透光；灰尘/水汽在光柱里可见
- **finishing**：**halation 是这个配方的灵魂**——8px 溢出；bloom 只在太阳附近；颗粒中粗

```
Low sun directly behind her, fifteen degrees off axis, hard and 3600K. Her body is a silhouette one and a half stops under the background; the sky behind is two stops over and rolling off, never clipped flat. Every loose hair at the edge of her head is lit and separated. Dust in the air is visible only inside the light. A wide soft halation bleeds eight pixels around her outline.
```

---

## 配方 5 · 硬闪直打（时装、editorial、锋利）

- **明度**：mids 50% / lights 30% / darks 20%
- **比例**：key:fill **1:1 – 1.5:1**（几乎无阴影），**但阴影边缘必须极硬**
- **光源**：机顶小闪光灯 / 裸灯直打，正前方略高；极硬（penumbra < 2mm）；5600K 冷白
- **色彩**：环境低饱和 / 主体高饱和 / 点缀色小面积 / 肤色偏冷
- **焦段机位**：24–35mm，近距离，略低或眼平（广角近摄的轻微变形是特征）
- **材质**：硬光放大质感——毛孔、布纹、金属划痕全部可见；**这是唯一该让硬光打满全脸的配方**
- **finishing**：颗粒细；**无 halation**（闪光灯没有）；背景常是纯色或直接黑；可能有轻微镜头色差

```
Direct on-camera flash, hard, 5600K, two millimetres of penumbra at most. Almost no modelling on the face — key to fill is one to one — but the shadow under the jaw is a crisp cut line, not a gradient. Everything the flash touches is sharp: pores, the weave of the collar, the scratches on the buckle. Background is flat and two stops under.
```

**为什么这个配方违反"柔光=假"的规则却不假**：因为它**有明确方向（正前）**且**阴影边缘是硬的**。假的是"无方向的柔光"，不是"平光"。

---

## 配方 6 · 霓虹双色（夜、躁、类型片）

- **明度**：darks 60% / mids 30% / lights 10%
- **比例**：两个 key（品红 + 青），互相做 fill；比例 3:1 让一边主导
- **光源**：两个画面外/内的霓虹管，一个暖品红（3200K 视觉），一个冷青（9000K）；半硬（霓虹是管状，有方向）
- **色彩**：**面积 9:1**——大面积品红环境，小面积青色点缀；或反过来。绝不对半
- **焦段机位**：35mm，略低
- **材质**：湿路面/湿墙是必须的（反射霓虹）；金属、玻璃、水
- **finishing**：halation 强（霓虹必溢）；bloom 明显；颗粒中粗；可能有轻微色差

```
Two sources: a magenta tube on camera left and a cold cyan one behind her, three to one so the magenta owns the frame. Everything is wet — the pavement holds a broken magenta reflection, the wall behind carries the cyan as a thin rim. Nine parts magenta to one part cyan. Nothing is lit from the front.
```

**警告**：这个配方最容易变廉价。唯一防线是**面积 9:1** 和**必须有湿表面**。干表面的霓虹 = 塑料。

---

## 配方 7 · 高调过曝（干净、临床、漂浮）

- **明度**：lights 60% / mids 32% / darks 8%
- **比例**：key:fill 2:1；背景比 key 高 0.5–1 stop（**唯一允许背景亮于主体的配方**）
- **光源**：大面积柔光（柔光箱/白墙反射），正面偏上；极柔；略暖或中性
- **色彩**：白/米为主，**必须有 8% 的深色锚**（一点黑发、一个深色物件），否则画面"飘走"
- **焦段机位**：85mm，眼平
- **材质**：白棉、瓷、纸、皮肤（高调下皮肤要保留色相，不能过曝成白）
- **finishing**：高光有长 roll-off（不是死白）；颗粒细；**无暗角**

```
Almost the entire frame sits in the upper range — white cotton, pale wall, bleached light — with one small dark anchor: her black hair and the shadow under the collar. Highlights roll off slowly rather than clipping; there is no pure white anywhere. Skin keeps a trace of red in the brightest area. Key to fill is two to one, background half a stop over key.
```

---

## 配方 8 · 伦勃朗低调（古典、体积、庄重）

- **明度**：darks 65% / mids 25% / lights 10%
- **比例**：key:fill **8:1 – 16:1**；背景 **4 stops under**（接近纯黑但有细节）
- **光源**：单灯，45° 侧上方，硬边或半硬；暖（3000–3400K）；无 fill，靠墙面微弱反弹
- **色彩**：环境深褐 / 主体暖褐 / 点缀一处冷光（窗/金属）/ 肤色暖
- **焦段机位**：85–135mm，略低（仰视增加庄重）
- **材质**：粗糙的布、旧木、哑光金属；**暗部要有细节**（不是死黑）
- **finishing**：颗粒中；暗部颗粒更粗；**无 bloom**（单灯没有）

```
One lamp at forty-five degrees above and to the left, hard-edged, 3200K. A small triangle of light sits on the shadow-side cheek. Key to fill is twelve to one and the background is four stops under — not black, still readable, just barely. The dark side of the frame holds shape without any fill.
```

---

## 配方 9 · Kodak 日光（怀旧、可信、胶片）

- **明度**：mids 50% / lights 30% / darks 20%（全调）
- **比例**：key:fill 3:1；background 1 stop under
- **光源**：下午三四点的太阳，斜 45°；半硬；5200K，略暖
- **色彩**：**这是色彩配方**——高光偏暖黄（奶油），阴影偏青绿；肤色暖红；整体饱和略降
- **焦段机位**：35–50mm，眼平
- **材质**：棉、木、旧漆、草；一切"被太阳晒过"
- **finishing**：颗粒中等带轻微彩噪；halation 中等；**高光长 roll-off 是这个配方的签名**

```
Afternoon sun at forty-five degrees, half-hard, 5200K. Highlights roll off into a warm cream rather than clipping; shadows sit in a cool green-cyan. Skin reads warm red against all of it. Saturation is slightly pulled back everywhere. The light is soft enough to keep detail in the brightest shirt but hard enough to draw a clear shadow line on the wall.
```

---

## 配方 10 · 限制色海报（图形、平面设计感）

- **明度**：**三档必须清晰分离**，每档一个色（例如 深墨绿 / 灰米 / 暖白）
- **比例**：无连续渐变，只有平涂块 + 一处渐变
- **光源**：**逻辑光**（不是物理光）——用一个方向的阴影统一，但光是平的
- **色彩**：**总共 3–5 色，不超过**；靠面积和对比造层次，不靠颜色数量
- **焦段机位**：图形化透视（正侧、正俯、正前），避免随机角度
- **材质**：纸、印刷网点、丝网印的错位
- **finishing**：**不要颗粒**（或极细）；要印刷质感（套色偏移、纸纹）

```
Three colours only: a deep ink green, a warm off-white, and a pale grey. Flat fills, no gradients except one. Shadows are a single flat shape in the ink green, not a soft falloff. Screen-printed: the registration is off by half a millimetre on one edge, the paper fibre shows through the pale areas.
```

**这一套的审美价值**：它逼你只靠**形状 + 面积 + 明度**做设计，是训练构图的最好练习。

---

## 配方 11 · 雾与空气透视（纵深、诗意、距离）

- **明度**：lights 40% / mids 45% / darks 15%——**远处最亮（雾），近处最暗**
- **比例**：对比随距离**递减**：近景 key:fill 8:1，中景 4:1，远景 2:1
- **光源**：低角度侧逆光穿过雾；或全散射的雾天
- **色彩**：环境雾白/灰蓝；主体深色剪影；点缀一处暖（灯/窗）
- **焦段机位**：85–200mm（压缩让雾层叠起来），或 24mm（雾把空间吞掉）
- **材质**：湿、冷、粗糙；远处只剩色块
- **finishing**：**雾就是 finishing**——不要额外 bloom；颗粒中；远处对比自然塌陷

```
The near figure is eight to one; the middle distance four to one; the far treeline is two to one and the same grey as the sky. Contrast falls with distance, not with focus. A low side-back light picks the fog out in one place only — everything else is flat.
```

**核心技术**：**对比随距离递减**。写这一句，纵深自己就出来了。这比 `depth` `atmospheric` 有效十倍。

---

## 配方 12 · 顶光压迫（商业、惊悚、审讯）

- **明度**：darks 60% / mids 30% / lights 10%
- **比例**：key:fill **16:1 以上**（几乎没有 fill）；背景 3 stops under
- **光源**：正上方硬光（裸灯/天窗/单管日光灯）；极硬；冷白 6000K 或冷绿
- **色彩**：环境冷绿/冷灰 / 主体近黑 / 点缀一处惨白 / 肤色偏冷偏黄（不健康）
- **焦段机位**：24–35mm，**低机位仰拍**（压迫感的来源）
- **材质**：硬光下所有瑕疵都被放大——汗、油、皱纹、毛孔；这是"不美化"的配方
- **finishing**：颗粒中；灯管 halation 强；暗角重且不对称

```
A single bare tube directly overhead, hard, 6000K. The eye sockets go black, the cheekbones and the bridge of the nose catch everything, and the shadow under the chin is a hard edge. Key to fill is sixteen to one. Shot from below eye level on a wide lens so the ceiling presses down. Nothing is flattered.
```

---

## 混搭配方的规则

配方可以组合，但要遵守：

| 可以叠 | 不能叠 |
|---|---|
| 配方 4（逆光）+ 配方 11（雾） | 配方 7（高调）+ 配方 8（低调）——明度结构互斥 |
| 配方 1（夜景）+ 配方 6（霓虹） | 配方 3（阴天）+ 配方 12（顶光）——光的方向逻辑互斥 |
| 配方 9（日光）+ 配方 11（雾） | 配方 5（硬闪）+ 配方 4（逆光）——光源位置互斥 |
| 配方 2（窗光）+ 配方 8（伦勃朗） | 配方 10（限制色）+ 配方 6（霓虹）——色彩系统互斥 |

**判断标准**：两套配方的**明度分布**和**光源逻辑**能不能同时成立。不能就换，不要硬拼。


# 附：07-translate.md

七维决策是思考层。真正决定出图的是**三个槽位**，每个槽位能承载的信息类型不同。

---

## 一、三个槽位，各装什么

| 槽位 | 能装 | 不能装 | 注意力权重 |
|---|---|---|---|
| **平铺 tag 串** | 模型认识的**名词/状态/已知概念** | 比例、衰减、因果关系、空间关系 | 中（会被稀释） |
| **结尾英文描述句** | **设计决策**：光的方向与比例、衰减、不对称、瞬间、材质行为 | 大量并列名词（会互相抵消） | **最高** |
| **JSON 分块（bbox）** | 精确位置、文字内容、多主体归属 | 全局氛围 | 高（但会锁死构图） |

**结论**：审美决策主要靠**描述句**承载，tag 只负责"有哪些东西"。把比例、衰减、瞬间写进 tag 串是无效的——模型不解析那些。

---

## 二、tag 预算（35 个标签的分配）

按用户既有密度规则（约 35 个平铺标签 + 一句英文描述）：

| 类别 | 数量 | 说明 |
|---|---|---|
| 人数 / 角色 / 作品 / 画师串 | 4–6 | 固定项，不动 |
| 身份锚（外观固定特征） | 6–8 | 眼镜娘那套固定设定 |
| 服装 | 3–5 | 只写能看见的 |
| 动作 / 姿态 | 2–3 | **只留一个主轴**（堆多了必变形） |
| 场景 / 环境 | 3–4 | 少而准 |
| **光** | **3–4** | 见下方词表 |
| **构图 / 镜头** | **3–4** | 见下方词表 |
| 材质状态 | 2–3 | 湿/旧/汗/皱 |
| finishing | 2–3 | 颗粒/光晕/景深 |

**光 + 构图合计 6–8 个标签**，这是审美的骨架。少于 4 个 = 模型回到默认均光居中。

---

## 三、光与构图的可用标签词表

这些是 danbooru 系模型真正认识的词，不是自造词。

### 光

`backlighting` `rim light` `contre-jour` `hard lighting` `soft lighting` `dappled sunlight` `god rays` `volumetric lighting` `chiaroscuro` `low key` `high key` `silhouette` `split lighting` `light from above` `candlelight` `moonlight` `neon lights` `light rays` `bloom` `halation` `lens flare` `window light` `sunbeam`

**不要用**：`cinematic lighting` `dramatic lighting` `beautiful lighting` `professional lighting`——这些是空转，模型给你平均值。

### 构图 / 镜头

`from side` `from above` `from below` `dutch angle` `close-up` `upper body` `cowboy shot` `full body` `wide shot` `negative space` `off-center` `foreshortening` `depth of field` `blurry background` `bokeh` `foreground blur` `profile` `three-quarter view` `looking away` `looking to the side`

**破对称专用**：`off-center` + `negative space`（这两个词是模型唯一稳定响应的构图标签）

### 材质状态

`wet hair` `wet clothes` `sweat` `glossy skin` `worn` `wrinkles` `dust` `steam` `smoke` `fog` `rain` `crumpled`

### finishing

`film grain` `35mm film` `kodak portra 400` `cinestill 800t` `expired film` `vignette` `chromatic aberration` `soft focus`

（用户已有粗颗粒层的既定写法，MOSS 里写在 summary.caption 最前面。）

---

## 四、描述句模板（一句，必须含五件事）

```
[瞬间/未完成动作] + [光源物件 + 方向 + 质量] + [比例或衰减] + [不对称/留白] + [一个材质可见行为]
```

**一句话，不要分号堆叠。** 五个成分里缺任何一个，模型就往默认值回退。

### 模板实例

**室内窗光（配方 2）**
> She has just set the cup down and her hand is still open above it, the only light a north window on camera left, half-hard and eight to one, dying within arm's reach so the far wall is already gone, and she sits on the left third with the right side of the frame held as empty wall.

**夜景（配方 1）**
> The bulb above the table is the hottest thing in the frame and everything else falls away from it — her skin at key, the room three stops under, nothing behind her brighter than the lamp — and she is caught mid-turn, not yet facing the lens.

**逆光（配方 4）**
> Low sun directly behind her, hard and warm, her body one and a half stops under the sky so she reads as a silhouette, every loose hair at the edge of her head lit and separated, and she is off-center with the empty bright sky filling the upper right.

**时装硬闪（配方 5）**
> Direct on-camera flash, hard, almost no modelling on the face but the shadow under the jaw a crisp cut line, everything it touches sharp — pores, the weave of the collar, the scratches on the buckle — and she is pushed to the right edge, half out of frame.

**阴天（配方 3）**
> Overcast with no direction to the light at all, so the structure comes from mass instead: her dark coat the heaviest shape at the bottom, the wall a mid grey, the pale sky the only light area, everything slightly wet and a shade darker where the water sits.

---

## 五、三个模型的落地写法

### MOSS（平铺 tag + 结尾句；含文字时改 JSON）

顺序：**人数 → 内容标签顺排 → 光 → 构图 → 材质 → finishing → 结尾英文句**

```
1girl, solo, [角色锚点...], [服装...], [动作主轴], [场景...], backlighting, rim light, hard lighting, off-center, negative space, depth of field, wet hair, film grain, 35mm film, <结尾英文描述句>
```

要点：
- 不带 LoRA 触发词、不带质量词（用户既定）
- 颗粒层写在 caption 最前面
- 需要精确文字/多主体归属 → 改 JSON，把文字内容单列 object 块

### Anima（平铺 danbooru tag + 一句英文）

顺序：**人数 → 角色名 → 作品 → 画师串 → 特征/场景/镜头标签顺排 + 一句英文描述**

要点：
- 不用 `角色名:` `scene:` `camera:` 这类行前缀
- 描述句里**绝不出现 camera 一词**（会被画成相机），改说 `the viewer` / `the foreground`

### NAI（权重语法 + 画师串置顶）

- 画师串按既定置顶（SFW / NSFW 两套）
- 光与构图的标签给 1.1–1.3 的轻权重，不要顶格
- 比例/衰减仍写在句子里，NAI 对自然语言的响应比 MOSS 强

---

## 六、标签稀释：最常见的失败模式

**现象**：加了 8 个美学标签，出图反而更平。

**原因**：并列的形容词在注意力里互相抵消。`soft lighting, hard lighting, dramatic lighting, moody lighting` 四个一起写 = 模型取平均 = 无光。

**规则**：
1. **一组只留一个**：光只留 3–4 个且互相兼容（`backlighting` + `rim light` + `hard lighting` 兼容；`backlighting` + `window light` 不兼容）
2. **宁可少一个，不要多一个**：删掉最不确定的那个标签，通常更好
3. **用句子补，不用标签补**：想说"衰减"就写进句子，不要找标签

---

## 七、从"单调提示词"升级的实操流程

给一段现有的提示词，按这五步改：

1. **删**：所有质量词、空转形容词（cinematic / beautiful / masterpiece / dramatic）
2. **定**：挑一个配方（06），把它的明度分布和比例记住
3. **加**：光 3–4 个 + 构图 3–4 个标签（从词表里挑，兼容的）
4. **写**：一句英文描述句，五个成分齐全
5. **减**：如果标签总数超过 40，从"场景/环境"里删（环境最不承担设计）

---

## 八、对照示例（同一内容，两版）

### 单调版

```
1girl, solo, glasses, black hair, school uniform, classroom, window, sitting, smile, soft lighting, depth of field, masterpiece, best quality, cinematic
```

问题：居中、均光、无比例、无衰减、摆拍、质量词空转。

### 审美版（配方 2 单窗光 + 眼镜娘固定设定）

```
1girl, solo, short black bob, blunt fringe, ahoge, round glasses, black eyes, white sailor uniform, red sailor collar, navy pleated skirt, white thigh-highs, sitting, classroom, desk, window light, hard lighting, from side, off-center, negative space, depth of field, dust, worn, film grain, 35mm film, she has just set the cup down and her hand is still open above it, the only light a north window on camera left, half-hard and eight to one, dying within arm's reach so the far wall is already gone, and she sits on the left third with the right side of the frame held as empty wall
```

改动清单：
- 删了 3 个质量词 + `cinematic`
- 删了 `smile`（改成瞬间）
- 加了光 2 个、构图 3 个、材质 2 个、finishing 2 个
- 加了五成分描述句
- 身份锚点保留不动

---

## 九、翻译检查表

- [ ] 描述句五成分齐全？（瞬间/光源+方向+质量/比例或衰减/不对称/材质行为）
- [ ] 光标签 3–4 个，且互相兼容？
- [ ] 构图标签里有 `off-center` 或 `negative space` 吗？
- [ ] 质量词全删了吗？
- [ ] 标签总数 ≤40？
- [ ] 动作标签只有一个主轴？
- [ ] 比例/衰减写进了句子而不是标签？
- [ ] Anima 描述句里没有 `camera` 一词？
- [ ] MOSS 里没有 LoRA 触发词、没有质量词？


# 附：08-style-extraction.md

用户给图说"学这个风格"时，不要用形容词模仿（"类似那种复古电影感"），走提取流程。

本文件是 `ajinnaaa/extract-visual-style-2` 方法论的精简操作版。

---

## 一、四类信息必须分离

看到一张图，先把它拆成四类，混在一起就会把场景规则当全局规则。

| 类别 | 内容 | 归属 |
|---|---|---|
| **Content** | 身份、物体、地点、动作、服装、logo、文字 | 只属于这张图，不进风格 |
| **Transferable style** | 形状语法、边缘行为、色彩角色、灯光逻辑、质感、空间、构图、运动、finishing | 可迁移，这才是"风格" |
| **Production locks** | 画幅、分辨率、媒介、合成目的、模型约束 | 全局约束 |
| **Scene locks** | 只在这个场景成立的东西（雨、雪、特定建筑） | 场景级，不能全局化 |

**最常见的错误**：把场景锁当全局规则。参考图是"雨夜霓虹"，提取出的风格就变成"必须有霓虹和雨"——那不是风格，是内容。

---

## 二、三层规则架构

| 层 | 说明 | 例子 |
|---|---|---|
| **Stable core** | 每张图都成立的 | "阴影偏青，高光偏暖" |
| **Conditional variants** | 特定条件下才用 | "夜景时背景落 3 stops；日景落 1 stop" |
| **Scene-specific locks** | 只对这一张/这一组 | "这个场景有一盏钨丝吊灯" |

写规则时必须标层，否则下一张图就会误用。

---

## 三、证据充分度

| 样本数 | 标签 | 能下什么结论 |
|---|---|---|
| 1 张 | provisional single-sample | 只能提"观察"，不能称"风格" |
| 2–5 张 | tentative shared style | 可以提共性，但要标 tentative |
| 6+ 张，覆盖不同主体/环境/光照/景别 | stronger series-level evidence | 可以定 stable core |

**判据**：如果 6 张图里光照条件全一样，证据强度仍等于 1 张。

---

## 四、每条规则的记录格式

```
[规则] location/owner + direction/behavior + relative strength + visual purpose + condition/exception + failure mode
[证据] 可见证据（具体到画面位置）
[覆盖] 样本数 / 覆盖了哪些变量
[层级] stable core / conditional / scene lock
[状态] observed / inferred / proposed / unknown
[置信度] high / medium / low
```

**禁止**：只凭画面断言具体摄影机、镜头型号、胶片、LUT、软件。可以说"看起来像高感负片的行为"，不能说"这是 Portra 400"。

---

## 五、十二个视觉系统（互不越界）

提取时逐项过，每项只写属于它的东西：

1. **Project identity** — 这个项目的不可变量（画幅、视角习惯、主题）
2. **Rendering & shape** — 边缘行为、形状语法、线条 vs 块面
3. **Color** — 角色分配、面积比、阴影/高光色相
4. **Lighting** — 光源类型、方向、质量、比例、衰减
5. **Space** — 透视类型、层数、空气透视
6. **Composition & lens** — 焦段、机位、构图习惯
7. **Material** — 粗糙度、光泽、半透、湿润、磨损
8. **Character** — 剪影、比例、脸部构造、身份差异手段
9. **Background** — 细节密度、边缘锐度、与主体的分离手段
10. **Coexistence & compositing** — 角色与背景的相对锐度/对比/明度/饱和度分离、共享光向
11. **Effects physics** — 源、附着、传播、衰减、残留
12. **Motion & time** — 静止/运动、模糊类型、时间点

---

## 六、提示词模块顺序（12 块）

提取完成后，按这个顺序组装（内容无关的模板）：

```
1  global style core
2  color
3  lighting preset
4  space / composition / lens
5  material
6  character
7  background
8  coexistence / compositing
9  effects physics
10 motion / temporal
11 negatives（只针对已证实的失效模式）
12 production / scene locks
```

内容无关的提示词以 `【在这里填写人物或场景内容】` 开头，内容插在 6–7 之间。

---

## 七、十二项冲突检查（交付前必过）

1. 场景规则被当成全局规则了吗？
2. "提议"被写成"事实"了吗？（proposed vs observed）
3. 两套 lighting preset 互斥吗？（一个说顶光，一个说侧窗）
4. 调色覆盖了材质固有色吗？（把木头调成蓝的）
5. 雾/虚化破坏了主体可读性吗？
6. 角色与背景的光向一致吗？
7. 角色与背景的色温兼容吗？
8. 颗粒在角色与背景上是同一个参数吗？
9. 透视在角色与背景上一致吗？
10. 特效发光了，但不影响邻近表面吗？（发光物必须照亮周围）
11. 负面压制了想要的材质吗？（例如负面写 `grain` 却要胶片感）
12. 内容泄漏进 content-free prompt 了吗？
13. 每个数字都有依据吗？（stops、焦段、面积比）

---

## 八、校准模式（用户给结果图说"不对"）

不要堆负面。流程是：

1. 让用户指出"哪里不对"（或自己诊断，见 09）
2. 定位到**哪个视觉系统**出错
3. **替换那条规则**，而不是加一条负面
4. 只改一处，重跑
5. 保留改动前后的对照

**为什么替换优于负面**：负面是"不要 X"，模型仍不知道要什么，容易把 X 旁边的正确东西一起压掉（最典型：负面写 `grain` 会把颗粒和细节一起抹平）。

---

## 九、提取检查表

- [ ] 四类信息分离了吗？内容有没有混进风格？
- [ ] 每条规则标了层级（stable / conditional / scene lock）？
- [ ] 证据充分度标了吗？1 张就别说"风格"？
- [ ] 有没有断言具体器材/胶片/LUT？
- [ ] 十二个系统逐项过了吗？
- [ ] 冲突检查 13 项过了吗？
- [ ] 数字（stops、焦段、面积）都有依据吗？


# 附：09-critique.md

图出来了但"不对"，按症状定位到具体维度，**替换规则**，不是加负面。

---

## 一、症状 → 维度 对照表

| 症状 | 最可能的维度 | 具体原因 | 修法 |
|---|---|---|---|
| 整体发灰、脏 | 明度 | 阴影漏光，明度阶梯断裂 | 加"阴影内部一个值"、降 fill、把 shadow 最亮处压到亮部最暗处以下 |
| 糊、看不清形 | 明度 + 构图 | 三档均分 / mass 太多 | 定一个主导档到 60%+，删掉一半元素 |
| 平、无立体 | 光 | 无方向柔光 | 指定光源物件 + 方向；key:fill 提到 4:1 以上 |
| 假、像渲染 | 光 + finishing | 无衰减 / 高光死白 | 加"the light dies within arm's reach"；写 roll-off |
| 塑料皮肤 | 光 + 材质 | 硬光打满 / 无纹理 | 硬光只打局部；加毛孔、细纹、不均匀血色 |
| 像素材库 | 瞬间 | 摆拍 | 换成未完成动作 + 视线未落镜头 |
| 居中、呆板 | 构图 | 默认对称 | `off-center` + `negative space` + 句子写三分之一 |
| 空、没内容 | 构图 | 缺低活动区的对立面——缺"信息层" | 加一个叙事道具（第二副餐具、磨偏的鞋跟） |
| 抢眼但不知道看哪 | 焦点层级 | 两个等强锚点 | 压掉一个（降对比/虚化/去色） |
| 颜色廉价 | 色彩 | 面积失衡 / 高饱和跨明度档 | 点缀色压到 ≤10%；高饱和只留一档 |
| 颜色"塑料" | 色彩 | 阴影是死黑，高光无偏移 | 给阴影色相偏移（偏青/偏蓝紫），高光反向 |
| 色调怪 | 色彩 | 用了 `teal and orange` 类词 | 换成物理描述（光源色温 + 环境反射） |
| 全图一样锐 | 材质 | 无细节分层 | 写"哪里开始虚"；或改深焦并靠明度分层 |
| 材质假 | 材质 | 只写名字没写行为 | 换成可见行为（湿发成束贴脸、皮革折面亮带） |
| 太干净 | 材质 | 无磨损 | 加 scuffs / washed many times / 起球 / 指纹 |
| 颗粒变脏斑 | finishing | 负面写了 grain/noise，或颗粒参数缺失 | 检查负面；补"rounded and evenly spread"三条防脏锁 |
| 发光但周围没亮 | finishing | bloom 未影响邻近表面 | 写"the halo lights the steam around it" |
| 多人肢体错乱 | 结构 | 朝向约束堆太多 | 只留一个主轴；手放身体近侧可见处 |
| 横图两侧空 | 画幅 | 站姿 + 横画幅 | 换横向展开姿态（侧卧/斜倚/并排/行走） |

---

## 二、诊断三步

### 1. 去色看明度

黑白化。焦点还在原位 → 明度承担了焦点（健康）。焦点消失 → 你在靠颜色撑构图（脆弱，换配色就崩）。

### 2. 眯眼看 mass

半闭眼。数出几个形？3–5 = 成立。一片均匀 = 明度无结构。10+ = 元素堆叠。

### 3. 缩到 200px

还认得出是什么、焦点在哪 → 构图成立。认不出 → 主体剪影没分离。

---

## 三、替换优先于叠加

**错误做法**（会越改越糟）：

```
原提示词 + hard lighting + dramatic lighting + high contrast + strong shadows + chiaroscuro
```

五个同义词并列 = 注意力抵消 = 回到默认。

**正确做法**：

```
原提示词 - soft lighting - cinematic lighting
+ hard lighting + backlighting
+ 句子: "low sun behind her, hard, her body one and a half stops under the sky"
```

**一次只改一个维度**，改完看图，再改下一个。同时改三个就不知道是哪个起的作用。

---

## 四、反复出现的三类顽固问题

### 1. 怎么调都平

**根因**：模型在"无方向光"的潜空间里。加多少形容词都在同一个区域。

**解法**：换**光源物件**，不是换形容词。`soft lighting` → `a bare bulb one foot above her head`。物件一变，模型换到另一个潜空间区域。

### 2. 怎么调都脏

**根因**：阴影里有多个亮阶（漏光），或负面里写了会连带抹掉细节的词。

**解法**：检查负面有没有 `grain` `noise` `texture` `detailed`；正向加"阴影内部一个值"。

### 3. 怎么调都不像"作品"

**根因**：缺**一个主张**。所有维度都在中位数。

**解法**：回到七维，逐项问"这一项我选了哪个极端？"。七项全在中位 = 没有作者。至少三项要推到极端（明度、比例、面积、焦段、机位、瞬间、材质任选）。

---

## 五、判断"够不够好"的三个快速测试

1. **三秒测试**：看三秒，能说出这张图在讲什么吗？说不出 = 无主张。
2. **遮住测试**：遮住主体，背景还有信息吗？没有 = 背景只是填充。
3. **换色测试**：换成完全不同的配色，结构还在吗？不在 = 靠颜色撑的。

---

## 六、诊断检查表

- [ ] 去色后焦点还在原位？
- [ ] 眯眼能数出 3–5 个 mass？
- [ ] 200px 缩略图还认得出？
- [ ] 定位到的是**一个**维度吗？
- [ ] 是替换规则还是堆了同义词？
- [ ] 负面里有没有会连带抹掉细节的词？
- [ ] 七维里至少有 3 项推到极端了吗？
