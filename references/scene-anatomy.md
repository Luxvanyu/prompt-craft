# 场景串解剖：64 条成品提示词的结构规律

<!-- back -->
返回：总入口 `SKILL.md`｜相关 `references/lexicon.md`（查词）、
`references/entry.md`（八槽起草）、`references/word-budget.md`（分段与预算）

这份文档只做一件事：把「构图风格」法典里 64 条**成品场景串**拆开，
量出它们共同的结构、权重档位和字数分布，然后把规律翻成本包的语法。

**来源与性质**：64 条来自社区整理（`构图风格.xlsx`，作者「凉夏之夜」），
每条配一张例图，横竖从 901×616 到 616×901 都有。
**这批串是 NAI 语法（带 `1.5:: ::` 权重壳），没有一条在本包实测过。**
所以下面写的是「它们怎么写的」，不是「这样写一定成」。

---

## 一、量出来的三个数（先看事实）

对 64 条做机械统计：

| 指标 | 结果 |
|---|---|
| 逗号段数 | 最少 9，平均 **13**，最多 18 |
| 权重壳数量 | 平均 **2.9** 处，60/64 条落在 **3–4** 处 |
| 权重档位 | 只有 **4 档**：1.2（79 次）/ 1.3（42 次）/ 1.4（20 次）/ 1.5（45 次） |
| 权重壳形态 | 全是 `a::b::`，无 `(word:1.3)` 括号式 |
| 横竖比例 | 横 901×616 与竖 616×901 约为 1:1，按题材选 |

**四个发现**：

1. **权重只有 1.2 / 1.3 / 1.4 / 1.5 四档，没有更高的。** 说明这套串的作者
   认为「想要的东西」和「不想要的东西」不靠顶格权重对抗，靠**结构位置**。
   这与本包 `moss-rules.md` 里「负面顶格 (ceiling_light:1.7)」是两套思路——
   后者是修复轮的打法，前者是首轮预防的打法。**两者别混用**。
2. **1.5 档不专属于光。** 45 处 1.5 里，光占一半，另一半是**主体道具、天气、
   环境大件**（花瓣雪片、蒸汽、雨幕、满池荷叶、花墙、灯笼阵）。规律其实是：
   **1.5 = 这张图的「大块头」——占据画面主要面积的那个东西。**
3. **平均 13 段，权重只占 3–4 段，其余 9–10 段是无权重白描。**
   这个比例值得记住：**加权的东西不超过三成**。全篇加权等于全篇不加权。
4. **没有一条写负向。** 64 条全是正向串。负向是另一件事（见 `jiegou_yuandian` 274 条，
   那是带负向的那一批）。

---

## 二、六拍结构（把 64 条叠起来看，骨架是一致的）

把平均 13 段按出场顺序拆开，几乎每条都落在下面六拍里：

| 拍 | 内容 | 典型权重 | 例 |
|---|---|---|---|
| **1. 场所 + 时间** | `in/at/on <地点> <时间>` | 无 | `at a bustling chinese new year market on a historic street at sunset` |
| **2. 景别 + 视角** | 两个词一组，或分开两壳 | **1.2–1.3** | `1.3::close-up on her face::` / `1.2::cowboy shot, three-quarter view::` |
| **3. 动作 + 表情** | `doing X with a Y expression` | 无 | `crouching in front of a brightly lit game stall, completely absorbed` |
| **4. 服装** | `wearing ...` | 无 | `wearing a casual dress and a jacket` |
| **5. 光 / 大块头** | 全图落点 | **1.4–1.5** | `1.5::the scene is vibrantly illuminated by the colorful, harsh lights of the game stall itself::` |
| **6. 背景 + 情绪** | `the background is ... creating a Y atmosphere` | **1.2** | `1.2::the background is a blur of the night market crowd, food stalls, and other neon signs, slice of life, playful mood::` |

**这六拍与本包七维的关系**：两者不是一回事，但能对得上——

| 本包七维（思考层） | 六拍（书写层） |
|---|---|
| 瞬间 | 第 3 拍（动作 + 表情） |
| 明度 | 第 5 拍里隐含（但这批串**基本没写明度数字**，是本篇最大的缺口） |
| 光 | 第 5 拍 |
| 空间 | 第 1 + 2 拍 |
| 色彩 | 第 5 + 6 拍（「warm red glow」「rich saturated palette」这类） |
| 材质 | 几乎没有（这批串不写材质） |
| 收尾 | 第 6 拍的情绪词 |

**结论**：这批串是**「空间 → 人 → 光 → 背景」**的叙事顺序，
而本包主张**「明度 → 光 → 空间 → 色彩 → 材质」**的物理顺序。
两者可以合，但必须补上这批串缺的三样：**明度数字、材质行为、负向**。

---

## 三、权重档位怎么定（照抄它的做法，但有修正）

### 原做法

```text
1.2 → 背景、"the background is ..."
1.2–1.3 → 景别、视角
1.4 → 次级大块头（前景花丛、光斑、道具）
1.5 → 主落点（主光 / 主天气 / 主环境大件）
```

### 本包修正（三条）

1. **景别可以给 1.3，但别给 1.5。** 景别是「怎么看」，不是「看什么」。
   把景别顶格，模型会把资源全花在裁切上，脸反而糊。
2. **光 ≥ 大块头。** 如果 1.5 给了雪/花/蒸汽，光必须也有 1.4 以上，
   否则会出「景很美但像贴纸」的图（这是本包 `symptoms.md` 里
   「有景无光」的典型长相）。
3. **权重总条数 ≤ 4。** 64 条的实测分布是平均 2.9 处、60/64 条在 3–4 处，超过就摊薄。

### 对应到 MOSS

MOSS 没有 `1.5::` 这种壳（写了也不解析，会被当普通文本）。
它的等价物是**句子顺序 + 明说程度**：

| 权重 | MOSS 的等价写法 |
|---|---|
| 1.5 | 单独一句，句首，且带具体量（`the only light in the room is ...` 放最前） |
| 1.3 | 单独一句，句中，不特别强调 |
| 1.2 | 并进背景句，跟着 `the background is ...` |
| 无权重 | 白描，可合并进长句 |

**换句话说：权重壳在 MOSS 里换成了「谁单独占一句」。**
这也解释了本包为什么反复强调「明度头写最前」——那是 MOSS 世界里唯一的 1.5。

---

## 四、四个从这 64 条里抠出来的写法（可直接用）

### 4.1 「情绪落点」要挂在背景句尾，不要单独成句

64 条几乎全部以 `creating a ... atmosphere` / `... mood` / `slice of life` 收尾，
且**挂在最后一个 1.2 壳里**，不另起一句。

```text
1.2::the background is a dense crowd and traditional teahouses, creating a lively, festive, and nostalgic atmosphere::
```

**为什么有效**：情绪词单独成句会被当成「要画一个叫 atmosphere 的东西」；
挂在具体背景后面，它变成对那个背景的**描述词**，模型才对得上。

**MOSS 对应**：`the crowd behind her is a dense blur of teahouse signs, and the whole back half of the
frame reads festive and slightly nostalgic rather than clean`——情绪跟着"背半幅"走。

### 4.2 「介质」一律写成独立块，且带光学后果

这批串里凡是水/雨/雪/蒸汽，都不是形容词而是物体：

- `the wet stone pavement is highly reflective, creating a perfect mirror image of the temple arch`（1.5）
- `a torrential downpour creates a curtain of rain just outside the shelter, blurring the street signs`（1.5）
- `the window is covered in a beautiful layer of condensation, and the lines she draws are sharp`（1.5）
- `a large amount of thick, white steam is rising from the water, creating a dreamy and hazy atmosphere`（1.5）

**规律**：`<介质发生了什么> + <它让什么变了>`。两句合一。

这正是本包 `medium-and-optics.md`（P4）的核心写法，
而这 64 条给了 30 多个现成例句，**可以直接当句式模板换词**。

### 4.3 光要写「谁发的 + 落在哪」，不写「什么感觉」

抽取 45 处 1.5/1.4 的光句，全部符合这个形状：

```text
<光源> + <动词：illuminates / filters through / slants through / bathes / creates> + <落点：her hair / the pavement / a rim on her silhouette>
```

对照反面：`beautiful lighting`、`dramatic atmosphere`、`moody lighting` 在这 64 条里
**一次都没出现**，`cinematic lighting` 只出现 3 条。这批作者基本不靠空转词——
这是对本包「禁空转形容词」铁律的一次外部印证（不是全部：那 3 条 `cinematic lighting`
恰好都在写「屏幕光/电影幕光」，是把它当**光源**用而不是当氛围用，用法本身是合法的）。

### 4.4 素材重复用：一张图里同一件事说两次，但角度不同

```text
1.5::the warm, golden light of the sunset mixes with the red glow from lanterns, creating a rich, saturated palette::
...
1.4::the soft, golden light of the setting sun bathes the scene, while a few lit sky lanterns float into the twilight sky::
```

同一张图里，光在前半段（1.5）说一次「是什么光」，在后半段（1.4 或 1.2）说一次
「它让背景变成什么样」。**不是重复，是同一个事实的两个落点。**

这与本包「一条 tag 说三遍会稀释」不矛盾：稀释的是**同义词**，
不是**同一事实的不同落点**。判断标准：两次说的是不是同一个可见结果。
是 → 删一个；不是 → 留着。

---

## 五、64 条的题材分布（想抄现成的先看这里）

| 题材 | 条数（估） | 典型串 |
|---|---|---|
| 日式四季（樱/枫/雪/祭） | ≈18 | 樱花隧道、枫叶倒影、雪中合掌村、夏日祭灯笼 |
| 台湾/东亚街景（夜市/老街/铁轨） | ≈12 | 九份夜巷、平溪天灯、夜市游戏摊、便利店 |
| 海与天（海/湖/星空/黄昏） | ≈10 | 海面落日、满月倒影、天文台银河、海雾 |
| 室内日常（厨房/教室/窗边） | ≈9 | 烘焙厨房、和室障子、书桌、暖气窗 |
| 花与植物（花田/荷塘/花墙） | ≈8 | 荷塘、银草海、九重葛、蒲公英 |
| 城市夜景（霓虹/雨夜/车站） | ≈7 | 雨夜月台、涩谷霓虹、纽约冬夜 |

**用法**：找结构，不抄内容。同一拍换个词就能落到自己的题材里
（例：第 5 拍的光从「樱花隧道」换成「地铁出口的风」）。

---

## 六、三个不能照搬的地方

**1. 全批没写明度。** 64 条里没有一条给 mean / dark / 亮部占比这类数字。
照抄会得到「看着挺美但明度平庸」的图——这正是本包 `a-value-and-light.md`
要补的那一层。**抄结构，明度自己算。**

**2. 全批没有负向。** 需要压的东西（多余的光源、脏颗粒、多余肢体）一个都没写。
本包的处理是「正向占位 > 负向否认 > 只在修复轮用顶格负面」，
所以照抄这批串之后，仍要走一遍 `lint.py`。

**3. 全批是 NAI 语法，MOSS 不认权重壳。** 直接把 `1.5::...::` 贴进 MOSS，
会得到一堆字面符号。必须按第三节的表翻译成「谁单独占一句」。

---

## 七、怎么用这份解剖（三步）

1. **挑一条最接近你题材的串**，`python scripts/lexicon.py --scene` 看全 64 条。
2. **只留它的骨架**（六拍 + 权重档），把词全换掉。
3. **补三件事**：明度数字（`a-value-and-light.md` 三档压缩）、材质行为一句
   （`d-material.md`）、然后跑 `lint.py`。

做完这三步，你得到的是一条**结构借来的、物理自己算的**串——
这就是这份文档能给的，也就是它全部的价值。
