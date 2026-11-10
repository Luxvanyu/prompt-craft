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

细节见 `references/aesthetic/e-moment.md`（附录 E：瞬间）。

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

细节见 `references/aesthetic/a-value-and-light.md`（附录 A：明度与光）。

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

细节见 `references/aesthetic/a-value-and-light.md`（附录 A：明度与光）。

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

细节见 `references/aesthetic/b-composition.md`（附录 B：构图）。

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

细节见 `references/aesthetic/c-color.md`（附录 C：色彩）。

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

细节见 `references/aesthetic/d-material.md`（附录 D：材质）。

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

翻译对照表、句式模板、以及"七维决策如何压进 35 个标签"的密度控制，见 `references/aesthetic/g-translate.md`（附录 G：翻译）。

---

## 配方库

12 个已经调好参数的完整方案（明度/比例/色/焦段/材质/颗粒 + 可粘贴英文），直接挑一个改内容即可，见 `references/aesthetic/f-recipes.md`（附录 F：配方）。

## 从参考图提取风格

用户给图要"学这个风格"时，走提取流程而不是形容词模仿，见 `references/aesthetic/h-style-extraction.md`（附录 H：风格提取）。

## 出图后诊断

图出来了但"不对"时，按症状定位到具体维度并替换规则，而不是堆负面，见 `references/aesthetic/i-critique.md`（附录 I：批评）。


---

---

## 附录索引（九个专题，已独立成篇）

| 编号 | 文件 | 主题 |
|---|---|---|
| A | `references/aesthetic/a-value-and-light.md` | 明度与光 |
| B | `references/aesthetic/b-composition.md` | 构图 |
| C | `references/aesthetic/c-color.md` | 色彩 |
| D | `references/aesthetic/d-material.md` | 材质 |
| E | `references/aesthetic/e-moment.md` | 瞬间 |
| F | `references/aesthetic/f-recipes.md` | 配方 |
| G | `references/aesthetic/g-translate.md` | 翻译 |
| H | `references/aesthetic/h-style-extraction.md` | 风格提取 |
| I | `references/aesthetic/i-critique.md` | 批评 |

> 拆成独立文件是为了按需加载：只在正文指到的那一篇时才去读，不必整份 1651 行一次性载入。
