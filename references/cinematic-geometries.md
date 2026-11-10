<!-- P7 · 21:9 与极端机位 -->
# 电影级 21:9 宽银幕与极端机位构图系统（Phase 7: Cinematic 21:9 & Extreme Camera Geometries）

本参考手册规范了 `prompt-craft` 体系在 21:9 变形宽银幕电影画幅、60 度陡峭大俯角机位及宏大史诗空间下的几何构图与 MOSS-Image 物理级提示词编写规范。

---

## 1. 21:9 变形宽银幕法则（Cinematic 21:9 Anamorphic Rules）

在 21:9（约 2.33:1 ~ 2.39:1）超宽画幅下，AI 生成极易出现“左右死角空洞”、“人物居中被拉成面条”或“左右重复堆砌垃圾资产”的问题：

1. **羽翼全横幅舒展填塞（Wingspan Panoramic Fill）**：
   * 她的大白羽翼是征服 21:9 画幅的终极武器。在提示词中明确要求双翼完全展开至电影级最大翼展：
   * `her massive white feathered wings are unfurled to their maximum cinematic span, stretching horizontally across more than half of the panoramic frame`。
2. **三分线侧向锚定与环境对流（Off-Center Anchor）**：
   * 主体严禁死板居中，置于水平四分之四或三分之一处（`four tenths across the horizontal frame`），留下大半幅展示宏大深渊、远景断桥或浩瀚云海。
3. **单向横切低逆光（Lateral Axis Raking Light）**：
   * 光源沿峡谷轴线水平穿透，将整张横向画面的羽尖与断崖边缘串联起来，形成极具电影感的横向高光带。

---

## 2. 陡峭大俯角 60 度机位法则（Rule B4: Steep 60-Degree High-Angle）

扩散模型在面对俯视时有极其强大的“复原为平视站姿”的先验惰性。严禁写 `directly overhead / looking straight down`（会退化），必须满足以下四条可验证几何事实：

1. **头顶可见性**：必须写出 `the top crown of her head and hair whorl are fully visible`；
2. **身体垂向叠压压缩**：`her shoulders and chest compress vertically in foreshortened stacking`；
3. **鞋履顶面视角**：`her boots are seen strictly from their top toe caps and lacing, never showing the soles`；
4. **地表退行透视**：`the stone pavement fills the lower two thirds of the frame receding away behind her`。

---

## 3. MOSS-Image 实战经典模板

### 模板 1：【21:9 宽银幕·残阳断桥与半屏翼展】（21:9 Widescreen Canyon Span）
* **画幅建议**：`建议尺寸：1792×768（21:9 宽画幅）`。
* **构图核心**：主体四分之四偏左，双翼横跨超半屏吃满横向空间，残阳沿峡谷轴线横切。

### 模板 2：【前上方 60 度俯拍·日晷广场与展开羽扇】（Steep 60-Degree Sundial Plaza）
* **画幅建议**：`建议尺寸：1024×1536（竖幅）或 1536×1024（横幅）`。
* **构图核心**：俯瞰同心圆青铜日晷，双翼如扇形水平贴地展开，长阴影压住罗马数字刻度。
