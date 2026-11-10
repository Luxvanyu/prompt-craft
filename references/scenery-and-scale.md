<!-- P9 · 无人空景与尺度标定 -->
# 无人空景与纯静物尺度锚定系统（Phase 9: Non-Character Scenery & Scale Anchor）

本参考手册规范了 `prompt-craft` 体系在无人环境（空景、废墟、神殿内景、战后战场）与桌面静物特写场景下的空间尺度锚定、防道具膨胀法则与 MOSS-Image 物理级提示词编写规范。

---

## 1. 核心痛点与物理防御哲学

在扩散模型中，以往几乎所有构图和景别都依赖“人体身高的比例尺（G8）”作为锚。一旦画面中**完全没有人物**，极易触发两大致命缺陷（实测案例详见 `references/gap-audit.md` 第 5 项与 G26 实测）：
1. **“英雄道具膨胀”先验（The Hero Prop Inflation Trap）**：
   * 现象：画面只写一把剑、一个发夹或一只茶杯，模型因缺乏人体对照，会默认赋予其“巨型英雄奇观道具”体量——发夹被画成 50cm 大金属雕塑，茶杯被画成脸盆大的水缸。
2. **空间空洞与失焦（Dead Space & Lack of Narrative Breath）**：
   * 现象：纯静物或空景容易沦为冰冷死板的 3D 样板房贴图，缺乏叙事张力与温度。

**防御哲学**：
* **建筑模数作为不可动物理尺（Architectural Modular Rulers）**：使用人尽皆知的标准规格建筑构件（如 60 厘米见方的铺石地砖、4 厘米厚的橡木桌面厚度）作为天然比例尺，道具尺寸与建筑构件建立直接的物理除法关系。
* **厘米级上限与排他性否定声明（Metric Bounds & Negative Upper Limits）**：直接给出真实公分数值，并显式否定其被放大的可能（`strictly a small delicate pin, never a large sculpture`）。
* **痕迹物理学与“缺席的主角”（Traces of the Absent Protagonist）**：空景中必须包含“角色离开不久的物理事实”（石缝中插着的佩剑、台面上微温的茶杯、散落的白羽、地表拖曳的长斜影），让无人的画面依然在讲人的故事。

---

## 2. 尺度锚定三大铁律（The 3 Laws of Scale Anchoring）

### 2.1 铁律一：建筑构件当尺子（Architectural Ruler Protocol）
* 严禁让道具孤立悬浮于画面中；
* 必须将其放置在带有清晰重复模数的建筑结构上：
  * 地面：`two sixty-centimetre paving slabs`（六十公分见方地砖）；
  * 桌面：`a four-centimetre-thick rustic oak tabletop`（四公分厚实木桌沿）；
  * 墙面：`a standard two-metre-tall arched wooden door`（两米高标准门框）。

### 2.2 铁律二：双重尺度锁定（公分数 + 身体部位比对 + 否定句）
单纯写“比地砖小”模型可能会把地砖一起放大。必须三合一闭环：
1. **真实厘米数**：`eight centimetres tall` / `five centimetres long`；
2. **通识物体比对**：`no larger than a clenched fist`（不超过握紧的拳头）/ `no wider than two fingers`；
3. **排他性否定**：`strictly a small personal pin and not a large sculpture`。

### 2.3 铁律三：单向斜影作为空间主角（The Diagonal Shadow Actor / G80 补二）
* 在空景中，平直的受光容易让空间扁平无趣；
* 必须让画外光源投射出**极具纵深感的对角线长斜影**（如插在地面的长剑投下的针状锐利斜影、窗框横木斜斜切过桌面与地板的明暗四边形），阴影直接承担引导观者视线的骨架作用。

---

## 3. MOSS-Image 实战经典模板

### 模板 1：【战后神殿·残阳插剑与落羽空景】（Altar Ruins & Abandoned Rapier）
* **定位**：战后空景叙事，尺度由 60cm 地砖拼缝锚定。
* **道具**：80cm 露出的细剑插地、5cm 金色发夹遗落、4 片白色绒羽散落。
* **光影**：低角度残阳在地面拉出极长的针状细影。

### 模板 2：【晨曦窗前·桌面静物与窗影四边形】（Quiet Morning Window & Still Life）
* **定位**：室内静物特写，尺度由 8cm 陶瓷茶杯与 20cm 展开手记锚定。
* **道具**：白瓷茶杯、真皮手记、折叠发带。
* **光影**：窗外早晨硬阳光穿透窗棂，在木质桌面和地板上投下清晰的倾斜四边形光斑。
