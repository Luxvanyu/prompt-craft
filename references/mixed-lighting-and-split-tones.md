<!-- P6 · 双色温分裂 -->
# 混合光源与双色温分裂系统（Phase 6: Mixed Lighting & Color-Temperature Split）

本参考手册规范了 `prompt-craft` 体系在多重冲突光源、双色温对撞（如暖钠灯对撞冷青霓虹、烛火对撞荧光终端）场景下的物理隔离准则与 MOSS-Image 物理级提示词编写规范。

---

## 1. 核心痛点与防崩哲学

在扩散模型中，一旦画面中引入两个不同颜色的光源，极其容易触发以下三大致命缺陷（实测案例详见 `references/gap-audit.md` 第 8 项）：
1. **色光污染与“脏灰泥（Muddy Gray Bleed）”**：
   * 模型在没有空间隔离约束时，会把冷蓝光和暖橙光在受光面上直接相加，生成浑浊的脏灰色或脏紫色，摧毁画面纯净度。
2. **阴影被洗平（Shadow Washout / 失去纵深）**：
   * 两个光源从不同方向照射，模型若处理不当，会用副光填满主光的暗部，导致全图没有纯黑闭环（Gate 8 曝光崩溃），立体感彻底消失。
3. **羽翼双侧色彩混乱**：
   * 双羽翼容易随机沾染不同颜色的光斑，失去与环境光源的方位因果关系。

**防御哲学**：
* **主副权力阶梯（Key vs Rim Hierarchy）**：两盏灯绝对不允许等权重！必须是一方为主导塑形光（Key Light），另一方为极窄的高反差切边光（Rim/Edge Light）。
* **左右空间物理隔离（Spatial Lateral Segregation）**：光源必须分居角色两侧（如高右 vs 低左）。人体的背脊与羽翼中央必须保留一条**纯黑的遮蔽暗脊（Occlusion Spine）**，作为冷暖两色的天然隔离带。
* **羽翼非对称色温响应（Asymmetric Wing Chromatic Response）**：左翼受冷光切边，右翼受暖光浸润，单片羽毛上严禁出现冷暖光晕直接混色。

---

## 2. 双色温分裂三大铁律（The 3 Laws of Split-Tone Lighting）

### 2.1 铁律一：主副光权力阶梯（Key vs Rim Dominance）
在文本中必须明确分级：
* **主光（Key Light）**：负责塑造整体明暗体量与大面积受光面（如 `high camera right, a warm sodium streetlamp casts saturated amber gold across her right cheek, right shoulder, and the front face of her right wing`）。
* **副光（Rim Light）**：仅作为高反差边缘勾勒，宽度极窄（如 `low camera left, a vertical neon sign casts cold electric cyan rim light slicing sharply along her left wingtip, her left sleeve, and the edge of her scabbard`）。

### 2.2 铁律二：暗部脊梁作为色彩断路器（The Occlusion Spine）
为了防止两种色光在角色胸前或面部混合：
* 必须在文本中显式写死**“分界暗部”**与**“禁止混合”**事实：
* 范例：`The two colors never mix into muddy grey, separated by clean neutral mid-tones. Deep occlusion shadows sit between her folded wing primaries and beneath her skirt hem, dropping cleanly to obsidian black.`

### 2.3 铁律三：羽翼色温物理定向（Directional Wing Chromaticity）
大白羽翼作为全图最大的反光面，必须按方位严格划分色温：
* **迎主光翼（Key Wing）**：大面积反射暖调环境光；
* **迎副光翼（Rim Wing）**：仅在最外缘初级飞羽边缘切出一条冷调高光线，羽翼内侧保持中性暗色。

---

## 3. 经典实战组合模板

### 组合 1：【雨夜赛博街巷·暖钠街灯 vs 冷青霓虹】（Sodium Amber vs Electric Cyan）
* **主光**：右上方高压钠灯，暖琥珀金；
* **副光**：左下方垂直霓虹立牌，高反差冷电青；
* **暗部**：湿石板路面与砖墙缝隙保持纯深黑。

### 组合 2：【幽暗藏书阁·暖烛光 vs 幽蓝荧光魔导球】（Candlelight vs Celestial Crystal Glow）
* **主光**：右侧厚重书桌上的黄铜烛台，暖橙烛火；
* **副光**：左侧悬浮的荧光记录晶球，冷幽青蓝发光体；
* **过渡**：桃花心木书架与地板深棕暗部，隔绝冷暖。
