<!-- P4 · 介质与物理光学 -->
# 介质成像与极端物理光学（Phase 4: Optical Media, Reflections & Physical Optics）

本参考手册规范了 `prompt-craft` 体系在水洼倒影、镜面反射、雨夜窗玻透射、羽毛半透光物理学及水下折射等光学介质场景下的防崩准则与 MOSS-Image 物理级提示词编写标准。

---

## 1. 核心痛点与物理防御哲学

在扩散模型中，光学介质与反射场景是极度容易触发“常识先验冲突”的翻车重灾区（实测案例详见 `references/gap-audit.md` P0 项）：
1. **倒影世界的“天地颠倒”先验冲突**：
   * 现象：写了“四分之三画面是水洼倒影”，出图仍然是“天在上、路在下”的正立画面。
   * 根源：扩散模型在海量真实照片中训练出的“天空必须在顶部、重力向下拉扯”这一世界模型先验，压倒了“这是一个倒影”的文字表述。
2. **介质表面杂质的归属漂移**：
   * 现象：写了“水面漂浮着浮尘与花粉”，出图却变成了“倒影天空里的夜空繁星”；写了“窗户上有雨水流痕”，变成了角色衣服上布满水珠。
   * 根源：模型无法区分“介质表面的微观物理层”与“透射/反射所呈现的远景内容”，容易发生属性错乱。
3. **CG 渲染术语的无效性与毒性（MOSS 禁令）**：
   * 现象：盲目写 `subsurface scattering (SSS)`、`caustics`、`octane render`、`ray tracing`，触发 Gate 5 报警甚至生成廉价塑料 CG 质感。
   * 根源：MOSS 依赖自然语言中的**物理光学现象描述**，而非 3D 软件材质术语。

**防御哲学**：
* **倒影世界的物理证据链（Inversion Evidence Chain）**：必须提供模型无法推翻的物理倒置证据——清晰裁切的水面边缘、倒立延伸的倒像、以及漂浮在水面的物理锚点（落叶/油膜/涟漪）。
* **介质表面归属硬隔离（Surface-Media Ownership）**：水滴、划痕、水草必须显式声明“附着在介质外表面，而非内部空间或人物身上”。
* **纯物理语言替代 CG 术语**：用“光线穿透半透明羽梢边缘、羽轴投射内部深色剪影”替代 `subsurface scattering`；用“网状游动光斑”替代 `caustics`。

---

## 2. 倒影世界的物理证据链法则（Inversion Evidence Chain）

严禁仅在 Prompt 中陈述“This is a reflection in a puddle”。若要让模型稳定生成**纯倒影构图**，必须集齐以下 4 项物理证据链：

1. **俯视与水面边界线（Water Edge Boundary）**：
   * 必须明确机位低且垂直/大角度俯视地表，且画面上部必须有清晰的地面与水面分界线。
   * 范例：`The camera is positioned at knee level looking steeply downward at the wet cobblestone ground, while the horizontal water edge cuts level across the upper third of the frame.`
2. **倒立延伸的视觉事实（Inverted Orientation Facts）**：
   * 不写抽象的“reflected”，写具体的倒置几何形态：
   * 范例：`Her reflected figure appears completely upside-down with her hair trailing downward toward the bottom frame edge, and inverted stone spires plunging downward.`
3. **漂浮物作为 Z 轴物理锚（Surface Floating Anchors）**：
   * 必须在水面上放置打破倒影连续性的实体（如漂浮落叶、水纹微波、花粉颗粒），并声明其投射在浅水底部的阴影：
   * 范例：`Three golden autumn leaves float directly upon the puddle's water plane, casting faint double shadows onto the stone bed below and interrupting the reflected silhouette of her wing.`
4. **水面暗调与天空亮调的色彩映射**：
   * 明确倒像中的亮色是水面镜面折射出的天空光，周边地砖为粗糙暗面。

---

## 3. 窗玻透射与介质归属律（Surface-Media Ownership）

当描写透过带水汽、雨滴或灰尘的透明介质（如咖啡馆玻璃、列车车窗、温室花房）拍摄角色时：

1. **介质表面物理层独立化**：
   * 必须用独立的完整句子，将水滴/冷凝雾气绑定在玻璃的特定表面。
   * 范例：`A dense layer of fine water droplets and running condensation streaks clings strictly to the cold exterior surface of the vertical glass window pane, and not to the interior room or figures.`
2. **水珠的微透镜折射功能**：
   * 将介质上的水珠描述为高光微透镜，用于交代光源方位：
   * 范例：`Each droplet acts as a tiny convex lens, catching and refracting the exterior streetlights as brilliant point highlights.`
3. **内外空间景深隔离**：
   * 明确界定“玻璃在前景两步处，角色在玻璃内侧三步处”，让模型在深度通道中把水珠与人物面部分离。

---



### 3.1 致命陷阱：主体面部避让先验（The Occlusion Evasion Trap）
* **实测翻车现象**：若只写「整面窗户布满雨滴与水痕，透过玻璃看室内人物」，模型出图时，**背景空旷处水痕密集，但一到人物面部、头发和胸口，水痕瞬间凭空消失**。人物仿佛贴在玻璃前侧或被开了一块干净的天窗。
* **真因**：二次元模型强先验将「美少女面部与身体」视为核心资产，注意力机制会自动抑制脸部和主体身上的前景遮挡物（脏污/水渍/噪点）。
* **破解三铁律**：
  1. **显式声明全幅无死角（Zero Clear Spots）**：`The water rivulets cover the entire sheet of glass continuously with zero clear spots, cutting uninterrupted over the scene behind it.`
  2. **逐项点名碾过身体部位（Direct Overlap Naming）**：必须指名道姓写水痕切过哪些部位：`thick vertical water rivulets slide directly over her face, her hair, her chest, and her white dress, leaving no part of her figure clean or untouched.`
  3. **赋予微透镜折射形变（Refraction Distortion）**：写出水痕对人物外观的物理改变：`visibly refracting, splitting, and distorting her skin tone and fabric contours through the wet glass plane.`

## 4. 纯物理光学现象描写词典（Anti-CG Optics Dictionary）

严禁使用 CG 渲染术语，统一使用下表的物理级视觉表象替代：

| 禁用 CG 术语（Gate 5 拦截） | 推荐的物理现象表象描述 | 视觉机制解释 |
| :--- | :--- | :--- |
| `subsurface scattering (SSS)` | `translucent glowing light penetrating the outer feather barbs, causing feather edges to illuminate softly from within while opaque central shafts stay in sharp silhouette` | 描述光穿透半透明介质时的边缘内发光现象 |
| `caustics` | `a dynamic cellular web of rippling gold refraction light projected across her dress and the shallow pool floor` | 描述光线经水面弯曲折射后在受光面上汇聚的网状焦斑 |
| `ray tracing / SSR` | `fresnel specular sheen across the wet stone paving where light at grazing angles reflects with mirror-like clarity` | 描述掠射角处的高反射率（菲涅尔效应） |
| `volumetric god rays` | `visible diagonal shafts of dusty morning sunlight cutting through the air where airborne motes catch brilliant specular glints` | 用受光微尘表现丁达尔光束 |
| `bloom / glow` | `halation of warm light bleeding softly across the dark silhouette edges of her hair` | 模拟胶片高光边缘的微光晕染现象 |

---

## 5. MOSS-Image 实战经典模板

### 模板 1：【雨后石桥·纯倒影构图】（Puddle Mirror Reflection）
* **机位**：膝盖高度大俯角，地平线被水岸线取代，水面横向切线压在画面上三分之一。
* **物理锚**：水面漂浮的落叶与油膜截断倒立羽翼，池底浅石产生双重投影。
* **光影**：水面映照晚霞强光，周边湿石砖呈现深色菲涅尔硬高光。

### 模板 2：【雨夜车窗·双层介质透光与羽翼半透光】（Rain-Streaked Glass & Translucent Barbs）
* **机位**：平视透过垂直玻璃窗，窗框中柱保持笔直。
* **介质层**：水滴冷凝在玻璃外表面，点状折射外界霓虹灯。
* **光学层**：室外逆光打穿人物的羽毛边缘，半透明羽梢呈现透光微亮，羽轴维持纯黑剪影。
