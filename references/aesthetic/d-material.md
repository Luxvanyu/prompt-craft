# 附录 D：材质

<!-- back -->
返回：`references/aesthetic.md`（审美内核正文）｜总入口 `SKILL.md`

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
