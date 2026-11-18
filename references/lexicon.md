# 法典词典：把「想要的那个东西」翻译成词

<!-- back -->
返回：总入口 `SKILL.md`｜相关 `references/composition.md`（景别与构图怎么用）、
`references/style-heads.md`（风格头的数值目标）、`references/aesthetic/g-translate.md`（槽位分工）、
`references/real-corpus.md`（查完整提示词长什么样，不只是词）

这份文档解决一件具体的事：**你脑子里有画面，但不知道那个东西在模型里叫什么。**

它不给新规则，只给**名字**。规则在别处，别在这里找。

---

## 零、词从哪来，能用到什么程度

2026-11-16 入库，数据源是社区法典站 `novelai.quicktagcloud.com` 的五部公开法典：

| 法典 | 条数 | 装的是什么 |
|---|---|---|
| 渡鸦的构图鉴 | 6633 | 服饰、姿势、表情、背景、画风、视角、光影，**每条带中文说明** |
| 构图风格 | 64 | 成品场景串，带权重壳，附横竖图尺寸 |
| 解构原典 | 274 | NAI 写法整条示例，**带负向** |
| 更衣人偶 | 430 | 服装组合串 |
| 叫我千藤就好了の衣柜 | 125 | 服装风格 + 历史/文化说明 |

**性质声明（重要）**：这些是社区整理者从出图经验里攒出来的词表，**不是本包实测的结论**。
本包的 G1–G98 是 174 张图逐张量出来的；这份词典是「别人认为模型认识这些词」。
两者可信度不同，用法也不同：

- 词典告诉你**怎么命名**（把意思对准一个已存在的词）；
- 实测告诉你**会不会生效**（写了这个词，画面真的变了吗）。

所以：**词表查完必须回到实测纪律**——写完照 `symptom` 与 `lint.py` 验，不因为「词表里有」就假定有用。

### 怎么把数据装到本机（第一次用跑一次，7 MB）

数据**不入库**（五份 JSON 约 7 MB，索引 1.8 MB），仓库里只有脚本：

```bash
python scripts/fetch_lexicon.py        # 下载五部法典 → 建 scripts/.lexicon/index.json
```

之后随便查：

```bash
python scripts/lexicon.py 逆光            # 中英模糊查
python scripts/lexicon.py --exact caustics
python scripts/lexicon.py --cat           # 法典 / 分类树 / 条数
python scripts/lexicon.py --in 视角构图     # 某分类全部条目
python scripts/lexicon.py --scene         # 64 条成品场景串（带横竖尺寸）
python scripts/lexicon.py --neg 手         # 看这批人怎么写负向
```

索引路径可用环境变量 `TAG_LEXICON_QT` 指到别处。站点改版导致下载失败时，
脚本会打印五个直链让你手动下（`https://novelai.quicktagcloud.com/data/<codex>.json`），
放进同一目录后加 `--no-download` 重建即可。

**只读本文档不跑脚本也完全够用**——下面已经把每类最有用的词挑出来了，
脚本只是让你能查全 7526 条。

---

## 一、三条翻译纪律（用之前先看这条）

同一批词，在不同模型里命运完全不同。**这个词表是 danbooru 系的**，直接照抄只有在 tag 模型上才成立。

### 1. tag 模型：直接抄

Anima / NAI / Illustrious 系：`dutch_angle` 就是 `dutch_angle`，原样进 tag 串。

### 2. MOSS：词只当备忘，不能当句子

MOSS 吃的是描述句，不认识 `dutch_angle` 这种复合 tag 名。它的反应通常是**忽略**，
偶尔会把字面意思画进去（比如把 `from_above` 画成画面里飘着一个「上面」）。

翻译的方法只有一条：**把 tag 换成它在画面上的可见证据**。

| 词典里的词 | 别这么写（对 MOSS 无效） | 这么写（可见证据） |
|---|---|---|
| `dutch_angle` | `dutch angle` | `the whole frame is tilted about fifteen degrees, so the doorframe runs diagonally across it` |
| `from_below` | `from below` | `the camera sits on the floor beside her shoe and looks steeply up, so her soles are the largest thing in the frame` |
| `backlighting` | `backlighting` | `the only light is behind her, and it comes through the curtain so her front is two stops darker than the rim of her hair` |
| `rim light` | `rim light` | `a single bright line runs along the top edge of her shoulder and stops where her arm turns away` |
| `negative_space` | `negative space` | `the entire left third of the frame is bare wall with nothing on it` |
| `bokeh` | `bokeh` | `the far streetlights are gone soft into round discs about the width of a coin` |
| `chiaroscuro` | `chiaroscuro` | `her lit cheek is the brightest thing in the picture and the other side of her face is not visible at all` |

**判据**：改完之后，一句话里必须有一个**能被坐标、数值、遮挡关系或明暗比例验证的落点**。
做不到，说明你还在用词，没在写画面。

### 3. Krea 2 / MJ / 自然语言模型：同上，但要更抽象

它们比 MOSS 更「愿意猜」，可以留一点术语（`high key`、`backlit` 能用），
但**关键仍然是那条物理落点**。术语是形容词，落点是事实；模型信事实。

---

## 二、词表反用法：这份文档最可能害你的地方

词表天然诱导一件事——**为了用词而加词**。这是本包最反对的写法，所以先说清代价：

1. **一条词 = 一个已命名概念**。写 `backlighting, rim light, contre-jour` 不等于「三重逆光」，
   等于同一件事说三遍，注意力被摊成三份，出图反而更弱。
2. **同义堆叠会让模型取平均**。三个近义词同时出现时，落点定不下来，结果就是你说的
   「有点那个意思但哪儿都不像」。
3. **词表里没有的，别硬造**。生造 tag（`super dramatic extreme lighting`）几乎必失效；
   改成描述它长什么样，永远更有效。
4. **35 个 tag 的预算不变**（见 `aesthetic/g-translate.md` 第二节）。
   查词是为了**换掉**含糊的词，不是为了**变多**。

一句话：**查词是把话说准，不是把话说多。**

---

## 三、机位与景别（86 条）

词典里分四组：镜头视角 32 / 画面大小 20 / 透视深度 11 / 布局风格 23。

### 3.1 镜头视角（32）

| tag | 中文 | 说明 |
|---|---|---|
| `straight-on` | 正面直拍 | 镜头正对角色脸平视拍摄 |
| `from_side` | 侧面视角 | 镜头从角色正侧面拍过去 |
| `profile` | 侧脸 | 只拍侧面轮廓 |
| `three-quarter view` | 四分之三侧 | 介于正面与侧面之间 |
| `from_behind` | 背面视角 | 镜头在角色身后，拍后背 |
| `from_above` | 俯视/俯拍 | 从头顶上方往下拍 |
| `from_below` | 仰视/仰拍 | 从脚边下方往上拍 |
| `dutch_angle` | 荷兰角 | 画面斜向一边 |
| `sideways` | 横躺构图 | 角色或画面横向水平摆放 |
| `upside-down` | 颠倒/倒立 | 画面上下完全倒过来 |
| `group_profile` | 多人侧脸 | 多角色并排拍侧面 |

**第一人称组**（`pov` 族，12 条）：`pov` 通用／`female_pov` 观察者是女性／`pov_hands` 双手入镜／
`pov_legs` 双腿入镜／`pov_breasts` 胸口入镜／`pov_crotch` 胯部入镜／`pov_shadow` 画面里是观察者的影子／
`pov_peephole` 猫眼看出去／`pov_doorway` 门口迎接／`pov_across_bed` 隔床／`pov_across_table` 隔桌／
`pov_dating` 约会面对面。

**介质与转向**：`from_inside` 从内往外拍／`from_outside` 从外往内拍／`looking_inside` 朝门里看／
`looking_outside` 朝窗外看／`partially_underwater_shot` 半水下（水线横穿画面）／
`mirror_selfie` 对镜自拍／`view_between_legs` 腿间视角／`eyewear_view` 透过镜片看／
`dressed_shadow_(meme)` 穿衣影子。

> **MOSS 落点**：`partially_underwater_shot` 是本组最有价值的一条——它对应 P4 介质成像里
> 「水面横线必须横穿画面中部」的写法。别写词名，写 `the water line cuts straight across
> the middle of the frame, and everything below it is a different, optically broken image`。

### 3.2 画面大小（20）——这一组最该进 tag 串

| tag | 中文 | 人物占比（对应本包景别表） |
|---|---|---|
| `very_wide_shot` | 极远景 | <1/10 |
| `wide_shot` | 全景宽镜头 | 1/8–1/6 |
| `full_body` | 全身构图 | 1/2–3/5 |
| `cowboy_shot` | 牛仔镜头（七分身） | ≈2/3 |
| `upper_body` | 上半身 | 1/2 |
| `portrait` | 胸像 | 脸占大半 |
| `close-up` | 特写 | 脸 = 画面高的 1/2 |
| `lower_body` | 下半身 | 只拍腰以下 |

**裁切组**（`*_out_of_frame` / `cropped_*`，11 条）：`feet_out_of_frame` 脚出画／`head_out_of_frame`
头出画／`eyes_out_of_frame` 眼部出画／`knees_out_of_frame` 膝盖出画／`foot_out_of_frame` 单脚出画／
`cropped_legs`／`cropped_torso`／`cropped_arms`／`cropped_shoulders`／`cropped_head`。

**特殊**：`cut-in` 插入特写块／`split_crop` 分割裁切。

> **这一组比「景别形容词」强得多**：MOSS 里写 `medium shot` 经常无效，但 NAI 里写
> `cowboy_shot` 稳定生效。所以**跨模型时这一组要分别处理**，不要直接搬。
> `*_out_of_frame` 组是本包 G10（裁头）的正向解药之一——出画就说明是「有意的」，
> 比「别裁到头」这种否定式管用（见 `decoupling.md`）。

### 3.3 透视深度（11）

| tag | 中文 | 一句用法 |
|---|---|---|
| `perspective` | 透视 | 通称，太泛，一般别单用 |
| `vanishing_point` | 消失点 | 连线收敛明确时才写；本包 G12 的强写法 |
| `foreshortening` | 透视缩短 | 肢体冲镜头时必写，否则会画短 |
| `forced_perspective` | 强制透视 | 前景巨大、远景极小，需要两个尺度锚 |
| `atmospheric_perspective` | 空气透视 | 远景偏蓝偏灰，拉开距离 |
| `fisheye` | 鱼眼 | 边缘球面畸变，**会与直线纪律冲突**（G14） |
| `depth_of_field` | 景深 | 通称，配 `blurry_background` 更准 |
| `bokeh` | 焦外光斑 | 背景失焦的圆盘 |
| `blurry_foreground` | 前景虚化 | 加层次 |
| `blurry_background` | 背景虚化 | 焦点集中到主体 |
| `variations` | 多版本展示 | 同一角色多套并排，**属排版不属构图** |

### 3.4 布局风格（23）——多人图与参考图用

**双人**：`side-by-side` 并肩／`opposing_sides` 左右对立／`face-to-face` 面对面／
`symmetry` 中轴对称／`rotational_symmetry` 旋转对称／`polar_opposites` 极端反差／
`comparison` 并排对比／`before_and_after` 前后对比。

**群像**：`lineup` 横排列队／`column_lineup` 竖列／`circle_formation` 围圈／
`group_picture` 合影／`everyone` 全员／`absolutely_everyone` 全员大集合／`height_chart` 身高表。

**参考图**：`reference_sheet` 设定参考／`bust_chart` 胸像参考／`multiple_views` 多视图／
`tachi-e` 立绘。

**版面**：`negative_space` 留白／`split_screen` 分屏／`split_theme` 主题分割／
`size_comparison` 体型对比／`age_comparison` 年龄对比。

> ⚠ **多人组与本包 P3 冲突时要让步**：`symmetry` / `rotational_symmetry` 会强制镜像，
> 而 `multi-character.md` 要求「两人手不同、视线不同」。两者同写，模型给你两个一模一样的人。
> 要对称就明确「对称的是站位，不是动作」。

---

## 四、光与色（123 条）

十二组：单色主题 12 / 黑白与局部上色 9 / 整体色调与配色 14 / 配色关系 12 /
滤镜与后期 8 / 上色技法 7 / 光照方向 4 / 光线形态与光学效果 15 / 时段光线 9 /
自然光源 8 / 人工光源 17 / 阴影与暗部 8。

### 4.1 光照方向（4）——只要这四个词就够定方向

`backlighting` 逆光（边缘亮、正面暗）／`sidelighting` 侧光（一半亮一半暗）／
`overlighting` 顶光（脸部下侧暗）／`underlighting` 底光（诡异，脸上阴影朝上）。

> 词典只有这 4 条，是因为**方向本来只有这 4 种**。本包 `aesthetic/a-value-and-light.md`
> 的「光之五问」里第 2 问（方向）就是在这 4 个里选一个再给角度。
> MOSS 写法见第一节的对照表。

### 4.2 光线形态与光学效果（15）

| tag | 中文 | 备注 |
|---|---|---|
| `light_rays` | 光束 | 通称 |
| `sunbeam` | 阳光束 | 从太阳方向射入的清晰光束 |
| `crack_of_light` | 缝隙光 | 黑暗里门缝透进一条（G80 实测正解） |
| `dappled_sunlight` | 斑驳阳光 | 树影打在身上 |
| `caustics` | 焦散光纹 | 光穿水后在表面形成的波纹亮斑（P4 用） |
| `refraction` | 折射 | 玻璃/水的折弯 |
| `chiaroscuro` | 明暗对照 | 强亮暗反差塑体积 |
| `bloom` | 泛光 | 亮区溢光 |
| `spotlight` | 聚光灯 | 一束只照目标 |
| `dim_lighting` | 昏暗照明 | 有光但很弱 |
| `muzzle_flash` | 枪口火光 | 单帧闪光 |
| `subsurface_scattering` | 次表面散射 | 皮肤/玉/蜡的透光柔亮（本包材质组没覆盖，值得试） |
| `ultraviolet_light` | 紫外线光 | 紫蓝荧光感 |
| `moonlight` | 月光 | 冷光主导 |
| `sunlight` | 阳光 | 太阳主导 |

> **`crack_of_light` 与 `caustics` 是本包 P4 里已经实测过的两条**（G80 / G95 族），
> 值得优先用。`subsurface_scattering` 没测过，但它是「皮肤为什么会透》的唯一现成词，
> 低调人像可以试。

### 4.3 时段光线（9）

`morning` 早晨／`dawn` 黎明／`sunrise` 日出／`day` 白天／`evening` 傍晚／
`sunset` 日落／`dusk` 黄昏／`twilight` 暮光／`night` 夜晚。

> 这 9 个词只管**色温与角度**，不管明度。写 `night` 不等于暗——本包无数例子证明
> 夜景照样能被顶灯照亮。**明度必须另写**（三档压缩法）。

### 4.4 自然光源（8）/ 人工光源（17）

自然：`sun`／`moon`／`fire`／`embers`（余烬火星，做小亮点很好用）／`lightning`／
`aurora`／`star_(sky)`／`starry_sky`。

人工：`candlelight`／`torch`／`lantern`／`wooden_lantern`／`oil_lamp`／`lamp`／
`desk_lamp`／`floor_lamp`／`wall_lamp`／`ceiling_light`／`chandelier`／`lamppost`／
`flashlight`（方向明确的小光束）／`glowstick`／`floodlights`／`stage_lights`／`glowing_headgear`。

> **这一组是 `mixed-lighting-and-split-tones.md` 的弹药库**：P6 里「两套光」的具体名字
> 就在这里挑。挑的时候守两条：**两套光要有色温差**（钠灯 2000K vs 便利店冷白 6500K）、
> **要有一个中性过渡带**（否则边界像贴纸）。

### 4.5 阴影与暗部（8）——本包最需要的一组

`shade` 遮光区／`tree_shade` 树荫／`shadow` 投影／`colored_shadow` 彩色阴影／
`window_shadow` 窗影／`darkness` 近全黑／`silhouette` 剪影／`see-through_silhouette` 透视剪影。

> **`colored_shadow` 是这里的宝贝**。本包 164 号（剪影）的核心教训是「暗部必须自己饱和」，
> 而 `colored_shadow` 正是「阴影不是灰黑」的现成词。剪影图、低调图都可以用它换掉
> 「深的暗」这种空转说法。
> `see-through_silhouette` 对应 169 号的「暗形里还有隐约层次」，同样是省事的写法。

### 4.6 色相与配色（12 + 14 + 9 + 8 + 7）

**单色主题**：`pink_theme` `red_theme` `orange_theme` `brown_theme` `yellow_theme`
`green_theme` `aqua_theme` `blue_theme` `purple_theme` `black_theme` `grey_theme` `white_theme`。

**整体色调**：`dark` `muted_colors` `pale_colors` `pastel_colors` `sepia` `high_contrast`
`saturated` `colorful` `neon_palette` `hue_shifting`（明暗区往不同色相偏移，**本包 G5 的现成词**）
`limited_palette` `split_theme`。

**配色关系**：`cool_colors`／`warm_colors`／`analogous_colors`／`complementary_colors`／
`spot_color`（点色，= 本包「唯一强色」）／`color-coded`（角色各有代表色）／
`color_connection`（同色关联）／`color_coordination`（配色呼应）／`rainbow_order`／
`palette_swap`／`color_switch`。

**黑白与局部上色**：`monochrome` `greyscale` `lineart` `partially_colored`
`greyscale_with_colored_background` `monochrome_background` `spot_color` `multiple_monochrome`
`limited_palette`。

**后期效果**：`vignetting` 暗角／`overexposure` 过曝／`chromatic_aberration` 色差／
`heavy_chromatic_aberration` 重色差／`double_exposure` 双重曝光／`inverted_colors` 反相／
`gradient_filter` 渐变滤镜／`iridescent` 虹彩。

> **`spot_color` 值得记住**：它等于本包反复讲的「全图只留一处强色」，
> 而 `hue_shifting` 正好是「暗部不能只变暗、要往蓝紫偏」的现成标签。
> 这两个词在 tag 模型里可以直接替换一长串描述。

---

## 五、其余分类的索引（要用时用脚本查）

| 大类 | 条数 | 里边有什么 | 本包哪个缺口 |
|---|---|---|---|
| 背景 | 336 | 室内 41 / 建筑商业 67 / 城市道路 49 / 天空天体 21 / **天气大气时间 21** / 自然地貌 18 / 水域 13 / 交通内部 8 | P1-5 无人画面、P1-11 天气 |
| 画风 | 139 | 传统媒材 26 / 上色 25 / 纹理特效 22 / 复古审美 17 / 线稿笔触 12 / 艺术流派 12 | P2-13 风格族 |
| 面部表情 | 186 | 基础情绪 57 / 颜文字 41 / 眉眼嘴 29 / 眼型 28 / 特殊瞳孔 14 | 表情层 |
| 身份设定 | 204 | 剑与魔法 21 / 现代职业 21 / 欧洲中世纪 17 / 体育演艺 14 / 星际 13 / 高幻想种族 11 / 修仙 10 | 角色设定 |
| 物体互动 | 196 | 日用 35 / 书写电子 33 / 工具户外 29 / 饮食容器 26 / 武器 21 | 道具语法（G3） |
| 多人互动 | 125 | 头脸触碰 27 / 牵手手臂 21 / 拥抱 13 / 背负支撑 13 / 亲昵 14 / 嬉闹对抗 14 | P1-6 多人关系 |
| 腿部姿势与移动 | 116 | 地面移动 14 / 旋转失衡 11 / 分腿柔韧 9 / 跳跃 8 / 水中 8 / 战斗步法 8 | 动态 |
| 日常行为 | 117 | 饮食烹饪 18 / 洗漱 20 / 学习工作 20 / 娱乐社交 20 / 家务 16 | 生活物证（关 13-A） |
| 手臂姿势 | 78 | 手臂位置 18 / 腿上手位 18 / 头脸附近 14 / 支撑接触 13 | 手部合法性 |
| 手势 | 67 | 双指三指 15 / 双手组合 12 / 单指指向 11 / 张手 11 | 手势段 |
| 眼睛 | 61 | 瞳孔形状 18 / 遮挡配饰 15 / 风格化 10 | 眼部特写 |
| 姿势-基础姿势 | 55 | 全身姿态 18 / 基础体位 13 / 坐蜷 10 / 躯干倾斜 10 | 姿态 |
| 招牌梗 | 26 | JOJO 立 / 碇源堂 / 冈本 pose 等 | 只有玩笑图用 |

**查法**（不用打开 JSON）：

```bash
python scripts/lexicon.py 天气            # 中英模糊查
python scripts/lexicon.py --in 背景        # 列出一整类
python scripts/lexicon.py --codex raven    # 看这部法典的完整分类
python scripts/lexicon.py --scene          # 64 条成品场景串
```

---

## 六、三个「词典没说、但你要知道」的坑

**1. 词典的 `safe` 标签不可靠。** 渡鸦那部 6633 条**全部标 `safe`**，包括明显不安全的服装词条。
rating 字段是按条目登记的，不是按标签判定的，别拿它当过滤条件。

**2. 同一个 tag 在不同法典里有不同解释。** 例如 `backlighting` 在渡鸦里出现三次
（背景/画风/色彩光影），说明分别是「背景呈现方式」「边缘发亮正面更暗」「光从背后照来」。
三类不同用法会被并成一个词，写的时候要自己确认是哪一类。

**3. 偏门 tag 的命中率随模型版本变。** `pc-98_(style)`、`frutiger_metro`、`sofmap_background`
这类是「特定人群认识」的词，在 Anima/NAI v5 上不稳。**小众词先用一条图验证**，
别一张重要图里塞三个没验证过的偏门 tag。

---

## 七、这份词典不做什么

- 不替代 `composition.md` 的景别表——那张表给的是**人物占画面高的分数**，这张表给的是**词**。
  两者一起用：先按分数定景别，再来这里找对应的 tag。
- 不替代 `symptoms.md`——出了图不像，看症状表，不是翻词典。
- 不承诺效果。词表里 7526 条，本包实测过的大概不到 60 条。
  **没实测过的词，第一次用都要单独试一张。**

---

## 八、场景串：64 条成品串，翻翻看就行

渡鸦那部里有一份 `composition_style`（64 条），是**别人写完、出过图的整串提示词**，
横竖各半（901×616 / 616×901），平均 13 段，权重只压 3–4 处。

```bash
python scripts/lexicon.py --scene          # 64 条全列（带横竖与尺寸）
python scripts/lexicon.py --scene 雨       # 只看含某个词的
```

**它值得看的只有一件事：别人怎么把一句话写成可见的东西。** 具体四种写法（介质独立成块、
情绪挂在背景句尾、光写「谁发的+落在哪」、同一事实两个落点）在 `references/scene-anatomy.md`
里有逐条拆解和例句。

⚠️ **但不要照着它的顺序写。** 那 64 条出自同一位整理者、题材偏斜（日式四季、东亚街景、
海与天占了大半），而且 NAI 靠 `1.5:: ::` 权重壳在任意位置提权——MOSS 没有这个机制，
靠的是单向注意力的位置权重，`lint.py` 关 8 要求前 80 词就把明度与光调定下来。

> **来找写法，不要来找顺序。** 顺序在 MOSS 里是另一套：光与明度提到第一段。
