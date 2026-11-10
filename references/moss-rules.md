# MOSS 实测规则全集（G1–G98）

> 这一份是「这台机器会怎么执行」的字典。写提示词时**不必通读**，按症状查 `symptoms.md`，按编号查 `casebook.md`。
>
> 这里合并了 MOSS 实测规则的全部正文（第 0 步 → 流程 → 机位 → 光 → 明度 → 格式 → 世界逻辑核心组 → 参数）
> 与完整规则索引表。所有 G 编号的**机制**换模型多半仍成立，但**阈值**（词数、bbox 放大倍数）要重新标定。

---


# MOSS-Image 实测规则正文（第 0 步 → 流程 → 机位 → 光 → 明度 → 格式 → 核心组 → 参数）

> **赶时间 / 从零起草 → 先看 `references/entry.md`（填空式入口）。**
> 八个槽位填完就是一份草稿，不用读完全文。本文档是它的依据与字典，遇到「为什么」再回来查。
>
> **出图不对 → 先看 `references/symptoms.md`（症状 → 改哪句）。**
> 别重写整份提示词，按症状表找到那一句，只改它。
>
> **要选风格 / 定调子 → 看 `references/style-heads.md`（12 个主头 + 6 层质感）。**
> 一张图只开一个主头，质感层最多两层。
>
> **不知道写多长 / 写到哪停 → 看 `references/word-budget.md`（字数预算）。**
> 三段必写：风格头、光路三落点、尺寸锚对位句；气氛形容词随时可砍。
>
> **要工具 / 要装到别处 → 看同级的 `README.md`（安装、五分钟上手、脚本速查、参数表）。**

## 这份文档解决什么

用户贴一张图，要一份能还原它的 MOSS 提示词。难点不在词量，在**机位、透视、光、明度关系**这四件事——它们决定"像不像"，而颜色和服装细节只决定"是不是这个角色"。

本文件是 2026-11 一整批（21 张，参考集为 `参考图目录/` 的 56 张 NAI V4.5 出图）复刻过程中沉淀的规则。**每一条都是实测或翻车换来的，不是审美偏好。**

---

## 第 0 步：先测，再写

不许凭眼睛判断。同一个"蓝色"可能是天蓝也可能是青灰，同一个"暖光"可能是亮部更饱和也可能是暗部更饱和——写反了气氛全错。

### 探针脚本

已随技能附带，直接用：

```
python scripts/probe.py <图片路径>
```

需要定点取色时追加 `--patch "x0,y0,x1,y1@名字"`（归一化 0–1 坐标，可重复多次）：

```
python scripts/probe.py IMG --patch "0.40,0.28,0.52,0.42@dress" --patch "0.20,0.22,0.30,0.36@hair"
```

输出段落：`size` / `mean` `med` / `dark mid bright nw p1 p99` / `grid 6x6` / `rgb` / `sat lit shadow` / `soft strong` / `hex 16x11` / 各 patch 的 `rgb sat lum`。各指标怎么用见下表。

### 读什么

| 指标 | 怎么用 |
|---|---|
| `dark/mid/bright` 占比 | 定"一图一档主导"。中调 85–90% = 插画感；中调 50–60% + 暗部三四成 = 电影感 |
| `nw`（L>0.95） | <1% 就写「没有一处真正的白」；炼化 56 张中位只有 0.005 |
| `p1` | >0.13 说明全图无真黑，写「最暗处仍是暖褐/冷蓝，不是黑」 |
| `sat lit` vs `sat shadow` | **决定气质，必须实测**（见下） |
| `soft` / `strong` | soft = 1 − strong，两者恒和 1；strong >0.10 是硬边密度够 |
| `flat` | >0.55 是大范围 bloom/雾；<0.35 是硬光硬边 |
| 6×6 亮度矩阵 | 定"唯一亮场在哪格、最暗在哪格"，再写进 caption |
| 16×11 hex 网格 | 直接读出主色，避免"天蓝/青灰"这种误判 |

### 饱和度三条实测样本（都不能套模板）

| 图 | 亮部 sat | 暗部 sat | 气质 |
|---|---|---|---|
| 万寿菊+蓝墙 | **0.442** | 0.325 | 硬太阳正午，越亮越艳 |
| 图书馆皮沙发 | 0.334 | **0.686** | 暗处是浓红棕，亮处被冲成奶油 |
| 温室吊椅 | 0.318 | **0.486** | 晒得发白又潮湿 |

### 元信息优先

`参考图目录/` 里的 PNG 元数据带完整 NAI 原始提示词与参数，能读就不要猜：

```python
from PIL import Image; import json
im = Image.open(P); t = im.text
print(t['Description'])
c = json.loads(t['Comment'])
print(c['seed'], c['steps'], c['scale'], c['sampler'], c['width'], c['height'])
print(c['v4_prompt']['caption']['char_captions'])
```

贴图若不在 `炼化` 里，最新文件在 `C:\Users\Administrator\.dsh\cache\attachments\request-images\*/*`（按 mtime 取最新；`objects` 目录可能滞后）。

---

## A. 流程（4 条）

- **A1** 每张先跑探针，再动笔。
- **A2** 补关键色块 patch 采样 + 16×11 hex 网格。
- **A3** 有 NAI 元数据就读，不猜构图。
- **A4** 交付格式固定：**一句横竖建议 + 理由 → 整块可复制（编译后一行 JSON）→ 4–7 条要点**（机位怎么定、光怎么写、为什么分这块）。

---

## B. 机位与透视（8 条，最容易翻车）

- **B1 不写形容词，写可验证的画面事实。**
  ✗ `from below` ✓ `their ankles and shoes buried in the flowers and never once visible`
  机位不是描述相机，是描述"只有这个角度才成立的事实"。

- **B2 `full body` 会吞掉机位词**，出成平视正面全身像。复杂机位图里删掉它。

- **B3 `from below` + `foreshortening` + `wide angle distortion` 会出脚底板视角。**
  正解：删掉后两个，让**膝盖**（不是脚）正对镜头做近大远小，鞋落右下角并写 `seen from its front and top, never from its sole`。

- **B4 `directly overhead looking straight down` 会退化成正常立姿。**
  俯拍写"前上方约 60 度"，并列四条只有这个角度才看得见的事实：头顶发旋可见 / 肩胸压缩成一叠 / 靴子看正面与顶面 / 地面往身后退出画框。

- **B5 倾斜只写 `dutch angle` 会被摆正。**
  写「整幅画被顺时针旋转约 20 度」+ 点名三条以上长线 + `there is not one level edge and not one plumb line` + **连竖直物一起歪**（蜡烛要斜、火苗要歪）。

- **B6 畸变要具体到物体**：电线杆外弓、两排建筑内倾、卷帘门如桶壁弯走、远处街口缩成一个小圆洞。要"写大点"就夸张写。

- **B7 广角贴近才有的内倾，中等焦段不能写。**
  游戏桌面第一版写"书架立柱内倾"→ 机位被判错。改写成"站在她右侧、只比头顶略高、下俯 45 度"，立柱就保持竖直。

- **B8 纵深靠三层叠压**（前景遮挡 / 中景主体 / 背景），不靠灭点。
  零透视也是一种选择：齐胸、水平、正对墙时所有竖线严格平行画框（巨壶、停牌砖墙都用这个）。

- **B9 面积词是几何指令，不是语气。**
  `fills the top quarter of the frame` → 模型真的盖一块天花板，low key 直接毁。
  想要"上方有一条顶棚、后面是开阔夜空"这种半开放结构，必须写成
  「顶部六分之一的一条窄横带 + 它后面是空的」，不能写"填满"。
  同类：`fills the frame` / `covers the whole background` / `from edge to edge` 都会变实体。

- **B10 空暗不等于墙。**
  `a flat empty dark with no stars and nothing in it` 会被画成**暗色实体**（墙、隧道壁）。
  要写「它不是墙、不是建筑、不是任何实体，只是没有东西」
  （`it is not a wall, not a building, not any solid thing, it is simply nothing`）。
  模型默认把"暗"解释成"有个东西在那里，只是暗"。

- **B11 可坐物比姿势词强势。**
  画面里只要有台子、箱子、台阶、台阶沿，人就会被放上去坐/靠，
  "她蹲着"这类姿势形容词会输。蹲/跪/躺必须写几何排除：
  「鞋底平放在地上」「髋部低于台沿」「她不在上面」「这只是一级台阶，太矮了坐不上」。

- **B12 场景自带先验，要显式否认。**
  加油站 = 地面必有标线；卧室 = 床上必有褶皱；教室 = 必有课桌。
  不想要就明写 `there is not one painted line, arrow or marking on it anywhere`。

---

## C. 光（7 条）

- **C1 把光写成布光说明书就丢了味道。**
  方向 / 光比 / 衰减 / 明度带百分比写满，出来的是技术正确但没有气味的图。

- **C2 "光的味道" = 五件物质性的事**（这是整批里最重要的一条）：
  1. **碎光斑**：光被花隙/百叶/树叶切成成百小光池，各自 bloom 并彼此融合
  2. **透体发光**：花瓣、薄布、纸、水、蒸汽本身是发光体，光从内部透出
  3. **彩色反光**：水面把暖橙反弹到小腿内侧、冷天光填正面 → 同一张脸「下暖上冷」
  4. **小幅过曝 + bloom 吃轮廓**：轮廓是被光晕软化的，不是画出来的细 rim line
  5. **空气介质**：尘埃/飞沫/落瓣悬在镜头与主体之间，光条因此读作实体

- **C3 多光源写「它们永不相混」**，并写交界处（下巴、袖口一半暖一半冷）。

- **C4 每个光源写衰减**：`the light dies within a forearm's reach`。

- **C5 近白 <1% 就写「没有一处真正的白」**。

- **C6 反向光与投影写具体**：鼻影爬到额头、眉骨进阴影、格子窗投影随台阶角度被拉长变形（写成规整网格就变贴图）。

- **C7 不要自行加浓。** 加 `god rays` / `high contrast` 那次被否，原版更好。

---

## D. 明度与色彩（7 条）

- **D1 一图一档主导，三档绝不均分。** 炼化 56 张没有一张均分。
- **D2 中调 85–90% = 插画感；中调 50–60% + 暗部三四成 = 电影感。** 两种画风不能混。
- **D3 饱和度方向必须实测**（见上表），写反气氛全错。
- **D4 单色系最稳。** 停牌砖墙：墙、砖、皮肤、地面全是同一支红土橙；温室：全图一支黄赭，找不到一个蓝像素。
  写成"红墙 + 橙砖 + 米色皮肤"会拆成三种颜色，画面立刻变杂。
- **D5 互补色要有第三色压场。** 万寿菊那张用锈棕屋顶（面积小但在顶部）压住橙与蓝。
- **D6 两个高饱和色不要大面积直接相接**，中间放隔离带（近黑夹克）。
- **D7 留一个 <5% 的小面积亮点**（一处饱和色 / 黄衣黄袜 / 剑鞘淡蓝），这是 60-30-8-2 里的那个 2。

---

## E. MOSS 格式（6 条）

- **E1 只给正向**，不给负面（用户明说才给），不带质量词（masterpiece / best quality / ultra-detailed / high contrast 全停用）。
- **E2 器材名、胶片名、渲染引擎名无效。** 写肉眼可见的画面表现。
- **E3 光影与色温词放在人物/衣物名词之前。** 先 `white shirt` 再补 `lit only by overhead green neon`，衬衫仍是暖白。
- **E4 JSON 分块的时机**：多层空间、多主体、要精确控制位置或图内文字。单主体单层空间用平铺 tag 串就够。
- **E5 文字用 `text` item 单独一块**，字符串用英文双引号，换行 `\n`。竖排中文里阿拉伯数字改汉字。
- **E6 角色名是 character caption 的第一个词，不是可选项。**
  格式固定：`名字, a girl ...`。名字写 Danbooru 全名（`sunaookami shiroko`、`rikuhachima aru`、`takanashi hoshino`）。
  作品名只出现在人物块里（`aru (blue archive)` 这种写法可以），**summary 和场景块里一个都不许出现**——版权大词进 summary 会出真人假发感。
  原创角色就在开头写 `original character,`。
  **这条是 29 号翻车的直接原因**：JSON 时代我把名字丢了，只留外观描写，模型认不出，出成"通用黑发恶魔娘"。早期平铺 tag 稿（04/07/10）都写对了（`sunaookami shiroko, a teenage girl standing on...`），改 JSON 时漏掉。
  名字后面必须跟**正确的外观**兜底——写错外观等于给模型错误锚点（29 号我把角色的发色和角写成黑的，实际是浅色长发的角、红瞳、白衬衫红领带、黑百褶裙、红长外套披肩不穿袖、橙红光环）。
  lint 关 1 会查：character caption 以 `a/an/the/she/he/they/her/his` 开头就报 WARN。

### JSON 分块的两个实战要点

1. **按空间层或人物分块，不按属性分块。** 暗三角一块、亮面一块、人物一块（把"站在交界线上、头肩在暗、腰裙在靴在亮"写进人物本身）、影子一块、碎晶一块（写"有前有后"）。
2. **块序即注意力序**：style/camera → 主人物（定调）→ 次人物（句首 `In sharp contrast, NO...` 切断前块属性）→ 文字/字幕。

### 文字块的透视（39 v6 实测，m03023）

MOSS 的 text 块默认把文字画成**正对观众**的平面字，哪怕它所属的物是斜的。39 的 HOT FOOD 告示贴在斜玻璃上，出图却是平贴画面的正脸字。正解写在 text caption 里，四件事缺一不可：

1. **共面句**：`it lies in the same plane as the sloped glass itself, so it does not face the viewer flat: it reads as a poster seen at an angle`。
2. **近大远小写成可验证事实**：`its left edge nearer to the camera and taller, its right edge farther away and visibly shorter`——只写 "in perspective" 没用，要写哪条边大哪条边小。
3. **横边收敛要对标邻近物**：`the top and bottom edges of the paper converge gently toward that far right edge the same way the window frame behind it does`——借画面里已有的透视线给它对齐基准。
4. **文字行跟随表面**：`the printed lines follow the surface of the glass rather than the picture plane, so the letters sit slightly smaller and closer together at the far end`。

方向判断：先看清楚那个面在画面里「远处在哪」（39 的玻璃远端在右），再把近端边、远端边、收敛方向逐个写死。纸面内的小角度旋转（胶带贴歪 4 度）与透视是两回事，分开写、都保留。

### 贯穿画面的长物件必须单独给 item，否则只画一段（47 号实测，m03193）

47 号的晒衣绳原本只写在「被单」那条 caption 里，没有自己的 item 和 bbox。出图：绳子只画了被单那一段，两头凭空断掉。用户原话「这个晒衣绳它只有一半」。

原因很直接：**模型在哪个 bbox 里画东西，就只在那个 bbox 的范围内画。** 一条横贯全画面的绳子如果寄生在别的物体的 bbox 里，它就只有那个 bbox 那么长。

正解：

- 凡是**贯穿或横跨画面**的线状物（绳子、电线、晾衣绳、轨道、扶手、栏杆、管线），一律单独一条 item，bbox 从画面一端拉到另一端（例：`[0, 296, 1536, 392]`）。
- caption 里显式写它「不中途停止」：`runs the whole width of the frame ... it enters the picture at the left edge, passes behind the big sheet, comes out on the other side of it, and leaves the picture at the right edge`。
- 写清两端固定在什么上（两根方钢柱、焊脚板、四颗螺栓），否则两头会虚掉。
- 写形状时给「可量」的弯曲：`sags a hand's width in the middle, and the sag is one smooth curve and not a straight line`。

同一条也适用于「必须连续的地面/墙面/台面」——它们都应该有自己的满幅 bbox，别寄生在别的块里。

**但满幅不等于水平**（47 号 v3→v4 实测，m03214）。把绳子的 bbox 拉成 `[0, 186, 1536, 266]` 之后，绳子确实完整了，用户却说「改完绳子之后整个画面构图都变了」——一条横贯上三分之一的强水平线把画面切成上下两半，其余元素被迫围绕这条线重排，原本「人 + 被单 + 光带」的三角结构散掉。

正解：**长物件要完整，但要走纵深，不要走水平。**

- 两端不放在同一高度、同一进深。改成「近柱在左前、远柱在右后」：`the near post stands at the left of the frame, about two metres from the camera ... the far post stands beyond the right edge of the sheet, about five metres away`。
- 在画面上就成了一条斜线：`runs to the right and slightly upward on the picture plane ... comes out on the other side of it thinner and higher`。斜线是纵深线，加强透视；水平线是分割线，破坏构图。
- 用粗细写纵深：`at the near post it is as thick as a pencil lead, at the far post it is half that`。同一条线在画面里粗细渐变，比任何透视词都管用。
- 高度选在**与主体互动的位置**（绳穿过被单顶部、略高于她头顶），不要放在构图分界线的高度（上三分之一、正中）。
- bbox 仍是满幅，但只覆盖它实际经过的那条斜带（200px 左右高），不要给成整幅高度的方框。

自查：把长物件单独看，如果它在画面里是一条**水平线**，它就在切画面。改成斜的，或者降到与主体咬合的高度。

### G12 补：人物的姿态和道具的支撑不能互相矛盾（47 号实测，m03177）

47 号写她「双手举高去够夹子」，同时又写「盆一手扶在胯边」——**她只有两只手**。模型没法让一个没人扶的盆贴在胯边，就把它画成浮空的。用户原话「除了有个盆子浮空了，其他都挺好」。

规律：**道具的支撑方式必须从人物姿态里长出来，不能另外声明。**

- 双手举高 → 手上什么都不能拿，所有随身物必须落地或挂起。
- 单手拿东西 → 明写另一只手在做什么，以及这只手抓在物体的哪个部位（`her fingers are hooked over the rim`）。
- 东西靠身体 → 明写靠在哪块身体上、重量压在哪个点，并且这个身体部位必须是自由的（胯、肘弯、肩，不能是正在用的手）。
- 干脆让它落地最省事：`its flat base set square on the concrete and its whole weight on the floor: nothing is lifting it, nobody is holding it, and it is not touching her leg`。

自查一句：把人物 caption 里所有动作列出来，再逐个问道具「它是被谁托着的」——如果答案需要用到一只已经在做别的事的手，这个道具一定会浮起来。

### 一致性可以消化位置偏差（46 号实测，m03152）

46 号第二版出图，302 仍然落在门板中间偏下——但模型顺手给走廊上**每一扇门都在同一高度装了同样的牌**，于是它从「放错了」变成了「这栋楼的规矩」。用户判定：「这样也行，虽然这个门牌还是在这里，但是所有人的门牌都在这里，也合理了。」

结论有三条：

1. **重复元素要主动写成一致的**。写「走廊上每一扇门都在同一个高度、同一侧装着同样的牌」，一致性本身就是写实，也是给模型的一个强约束——它会把这条规律复制到每一个同类物体上。
2. **位置偏差纠正不了时，一致性是次优解**。单点放错的元素会被读成错误；成组一致放错的元素会被读成惯例。二者观感差一个量级。
3. **反过来的警告**：如果一个元素只出现一次、位置又可疑，它一定会被读成错误。所以要么把它挂到构件上（上一条规则），要么让它成组出现。

### 文字块的位置：必须挂在具体建筑构件上，否则一定跑到正中（46 号实测，m03135）

46 号写 `screwed to the door at the height of her shoulder`，出图 302 跑到了门板正中央。原因：**文字块对模型来说是一个「标签」，标签的默认位置是所属物的几何中心**。你只给一个高度，它就按「居中 + 那个高度」摆，门是竖向长条，结果就是正中。

正解：位置句必须挂在**可数的构件**上，并且显式否认中心。

- 挂在构件上：`a hand's width below its top edge, level with the top rail`（不是「在门上」，是「在门顶横档下方一手宽」）。
- 给相对人的后果：`well above her head, so that from where she sits it is up and behind her shoulder and she would have to tilt her head back to see it`。
- 显式否认三连：`it is not in the middle of the door, it is not at the height of her face and it is not beside the handle`。
- bbox 也要跟着挪到门的上部，别留在中间。

同一条适用于所有「贴在某个大面上的小东西」：告示、门牌、价签、开关、挂钩。**只要它属于一个大面，就必须用大面的边/档/缝来定位，再否认一次中心。**

### G12 每件道具都要回答「谁支撑它」（46 号实测，m03116）

46 号写 `An umbrella stands against the door frame beside her, closed, its point on the floor and its handle hooked over the frame's edge`。出图：一把收起的伞直挺挺立在人身旁，尖端戳地，什么也没扶。用户原话「这个伞在人旁边立起来了直接，物体应当符合物理定律」。

原因有两层：

1. **我写的支撑关系是假的**。收起的伞是一根细钢尖 + 一根柄，重心在伞身中间，尖端戳地根本站不住；「handle hooked over the frame's edge」也没说清挂在哪个具体凸起上。
2. **模型对 bbox 里的道具默认「立着、居中、完整展示」**，因为它在展示物体，不是在摆放物体。你不给它接触与支撑，它就让东西浮着或立着。

正解：每件道具写三件事——**接触点、支撑方式、为什么不会倒（或为什么会倒）**。

- 能躺就写躺：`lies flat on the lino, on its side, its whole length supported by the floor, and nothing is holding it up`。
- 要立就必须写清靠在什么上、靠在哪一点：`leaning with its top against the wall and its foot against the skirting, held by the friction of the wall`。
- 要挂就写清挂在哪个凸起上，并且写它离地多高。
- 再补一句物理否认：`because a closed umbrella with a steel ferrule cannot stand on its point and it is not leaning on anything either`。这句是给模型的排除项，非常有效。

顺带一条通用检查：**道具 bbox 不要贴着人物 bbox**。贴着了模型会把它塞在人脚边、画成一坨认不出的东西（45 号的书包就是这么废的）。

**固定构筑物永远不站在台阶/坡道上**（51 号石灯，m03737）。我写「the stone lantern stands on the left of the flight above her」——只给了方位与高度，没写它立在什么地面上，模型就把它搁在台阶中间，看得人直想不通。

固定构筑物（石灯、石柱、邮筒、垃圾桶、消防栓、招牌立杆、拴马桩）的写法，三件事缺一不可：

1. **它站的那块地面要有名字**：`a flat ledge of dressed stone cut into the mossy bank beside the flight`、`the paved apron at the foot of the steps`、`the gravelled strip between the path and the wall`。台阶、斜坡、楼梯本身不是可以放东西的地面。
2. **写清它与主体结构的相对关系**：`one step's width clear of the line of the steps`、`out to the side, where a person walking up would pass it at shoulder height`。
3. **显式否认它插在台阶里**：`it does not stand on the steps at all ... no step continues under its base, no step edge crosses its plinth, and it is not standing in the middle of the flight either`。再在 summary 补一句总纲：`Nothing stands on the steps themselves except her: no furniture, no post and no lantern interrupts the treads.`

尺寸也要换成相对的：**别写「三倍坐高」这种会把它放大的倍数**，写 `twice her seated height` 这种与实际器物（春日灯籠约 2 米）吻合的倍率。倍数写大了，模型会连它脚下那块地一起放大，于是只能塞在台阶上。

### G3 补：模型的默认脸是微笑，「没有表情」不能靠否定词写（45 号实测，m03083）

45 号琴房写的是 `eyes open and fixed on nothing, the muscles around them are slack, her mouth is slightly open with no shape to it`——全是「没有」：没有焦点、没有形状、松弛。出图她是一张明快的、微微含笑的脸，故事（练到天黑、人已经空了）全丢了。原因很直接：**模型的默认人脸就是微笑**，你写「松弛」，它就给你「放松的微笑」；你写「没有形状」，它给你「自然的表情」。

正解三步：

1. **先给她一个正在做的动作，不是一种状态**。45 改成「她在听最后一个音消失」——听是一个动作，模型有画面可画。可选动作：听、忍、数、等、憋着笑、憋着不说话、怕吵醒人。
2. **显式禁止笑**：`and she is not smiling at all`，再加毫米级的嘴角方向 `the corners of her mouth are pulled down by a millimetre and not up`。只写 `not smiling` 不够，要给反方向的几何。
3. **眼睛要说清是哪种闭/哪种睁**：`closed the way a person closes them to hear better rather than the way a person closes them to smile, so the lids come down flat and the lashes lie against the cheek and the brow above them stays level and slightly lowered`。眉毛必须一起写——笑起来眉毛会上扬，听的时候眉毛是平的、内侧略压。

附带两条：表情要跟身体一起给证据（头偏几度把耳朵转向声源、下颌松垂、脖子上的筋因为头前倾而绷起）；再加一处「保持同一个表情一小时」的痕迹（眼下的皮是松的、颊上有一道浅褶），脸才有时间感。

### 极简档：除了光影，其余一律压到最短（用户 m03863 定，2026-11-06）

当用户说「太复杂了」「极简化」时，按这个额度写：

- **summary ≤ 270 词**，只装四件东西：一句话明度头、光源与光落三处、未照亮区、机位一句。
- **items ≤ 5 块**，能把地板和地上的东西合成一块就合成。
- **除 summary 的光段之外，每块 caption ≤ 3 句**；人物块 ≤ 8 句，且只写「在哪 + 朝哪 + 一个动作 + 一句光」。
- 删掉：故事小传（改写进 summary 一句）、证据物清单、比例尺清单、材质纹理描写、颜色清单、情绪解释。

判断标准：把 summary 的光段整段删掉，剩下的内容还应该能让人看懂「谁在哪做什么」。看不懂就是写多了。

### 人物：只写「在哪 + 朝哪 + 一个动作」（用户 m03837 定，2026-11-06）

写复杂姿态必然出畸形。人物块只保留四件东西，别的全删：

1. **她在哪** —— 用**一个同高的具体物**锚定，不要用「第三级踏板」这种要模型自己数的序号：`her feet are on the tread that sits level with the third shelf from the floor`、`she sits on the bench with the bench edge under her thighs`。
2. **身体朝哪** —— `facing the shelves, turned a quarter towards the viewer`。
3. **一个主动作** —— `her right arm is stretched along the top shelf, her hand open, reaching for a book`。
4. **一个支撑**（只有需要时才写）—— `her left hand holds the front edge of the shelf above her head`。

删掉：肘的角度、手指几根、指尖离目标多远、重心在哪只脚、脊柱弧度、肩膀塌不塌、衣服褶皱走向、两只脚分别踩哪里。这些每多一句，畸形概率涨一档。

**一件道具只能配一个动作**：腋下夹书 + 手臂上举 + 手扶书架 = 三件事，模型必错。要么把书放进地上那堆，要么去掉扶书架这个动作。

**道具 bbox 不许进人物 bbox**：贴着人的小道具会被画成贴着人、比例被人物撑大（54 号地上那叠书被画成前景巨书）。

### 文字块：默认不写（用户 m03822 定）

除非用户明确要求画面里有字（招牌、价签、编号、显示数字），否则**不要生成 text 块**。理由：文字块是失败率最高的一块，模型要么糊成乱码，要么把字画成正对观众的平面贴纸；即使十关全过，出图也常常只有这一块是废的。需要“有标识感”的地方，用**没有字的形状**代替：空白的搪瓷牌、磨掉的丝印、只剩一个圆钉的标牌、被撕掉一半的贴纸。

### 编译报错的三个坑（2026-11-06）

- `summary.canvas` 是**字符串** `"single"`（或 `"multi_panel"` / `"collage"`），写成 `{"width":..,"height":..}` 会报 `Error: summary.canvas must be single, multi_panel or collage`。
- 顶层写 `"canvas"` 字段会报 `Error: Layout draft: unknown fields ['canvas']`。
- 顶层必须有 `width` / `height`（16 的倍数）、`bbox_coord_space: "abs"`、`bbox_format: "xyxy"`；编译产物才变成 `abs_centralized` + `yxyx`。

### 编译

```
python scripts/compile_prompt.py X.json --output X.txt
```

草稿格式：`width` / `height`（16 倍数）+ `bbox_coord_space:"abs"` + `bbox_format:"xyxy"`，坐标从左上角起算。编译器转成 `abs_centralized` + `yxyx` 并删掉宽高。

### 官方 Layout JSON schema 对照（官方仓库 `OpenMOSS/MOSS-Image` → `skills/moss-image-prompt-enhancer/references/layout.md`）

交付前按这张表核一遍，十关不查这些：

| 项 | 官方规定 | 草稿写法 | 编译产物 |
|---|---|---|---|
| `summary.canvas` | `single` / `multi_panel` / `collage` 三选一 | 可写，编译器接受 | 保留 |
| `summary.caption` | 整体场景与风格；画风/媒介开头句放它最前 | ✓ | ✓ |
| `items[].label` | 只能是 `object` / `character` / `text` | ✓ | ✓ |
| `items[].bbox` | 整数，宽高为正 | `[x1,y1,x2,y2]` | `[y1-H/2, x1-W/2, y2-H/2, x2-W/2]` |
| `bbox_coord_space` | `abs_centralized`（中心原点，x 右 y 下） | `abs` | 编译器改写 |
| `bbox_format` | `yxyx` | `xyxy` | 编译器改写 |
| `summary.palette` / `items[].palette` | 支持，HEX 数组 | 可选 | 保留 |
| 不要写 | `width`/`height` 进产物、`anchors`/`must_not`、`panels`/`watermarks` label | — | 编译器已删宽高 |

`summary.meta` 只在整页版式（poster / photobook 内页）时用，普通插图留空。

**分辨率与文字**（官方 §0/§8）：图内要落字且必须清晰 → 面积 ≥1.6MP（1024×1536=1.57MP 差一点，用 1088×1632=1.78MP），Steps 50 + SLG `single_layers` 22；只落中等字号短词 → SLG 置空 + 16 步 + 0.6MP 也行。

**§5/§6 的两条硬要求（十关不查，但会出假发感与儿童头身比）**：
- 头发必须写 `natural fine [发色] real human hair` + `thin wispy bangs` + `loose flyaway strands`，否则是假发质感。
- 露脚趾写官方措辞 `five distinct, natural toes clearly visible`，并砍掉远端那只脚的细节；全身镜头必须保留「双脚与地面/支点的关系」，删掉就变五头身儿童。

---

## F. 一条元规则

**以上全部是诊断工具，不是套用模板。**

今天有三次拿上一张的规律套下一张都错了：加浓（Misaki）、立柱内倾（游戏桌面）、亮部更饱和（温室）。**每张都重新测。**

---

## G. 世界逻辑与故事（先于一切技术参数）

用户原话（m01020）：「图片要有故事感，有那种你一看就知道信息和氛围的感觉」。
（m01048）「车站是不是应该面对车道，而不是背对车道，你好好想想」。
技术全对但**现实逻辑错**的图，会被一眼看穿。这两条比明度、比光比都靠前。

### G1 先过一遍常识，再动笔

写之前用一句话问自己：**这个场景在现实里长这样吗？** 逐项排查：

| 场景 | 必然成立的事 |
|---|---|
| 候车亭 / 站台 | **人坐在长凳上面朝车道**，长凳背靠墙或背靠空地，亭子开口朝路 |
| 加油站 | 车道在加油机旁，人不会站在车道上 |
| 教室 | 学生面朝讲台，讲台在教室一端 |
| 卧室 | 床靠墙，床头不悬空 |
| 餐厅 | 客人面朝桌子，背对通道 |
| 商店 | 柜台在里面，顾客在外面 |

**最常见的错：把主体的朝向和场景的朝向搞反。** 生成模型默认"人朝镜头、背景当墙"，于是长凳背对马路、人正对观众——功能上说不通。修法是把**场景的方向性**写成硬约束：`the bench faces the road, so her back is to the shelter wall and she is looking across the road, away from the viewer`。

### G2 先写故事，再从故事里挑那一瞬间（一张图只讲一件事）

用户原话（m01875）：「你写提示词之前你先谱写好故事再从故事里面挑出最有美感的那一刻，画出来」。

**顺序不许颠倒。** 不是先想构图再往里塞道具，而是：

1. **写故事小传**（5–8 句，不写任何视觉词）：她是谁、什么时间、为什么到这里、来之前发生了什么、此刻在等什么、接下来要做什么。写到你**能说出她下一秒的动作**为止。
2. **定地点**：故事里的行为必须发生在**做这件事的地方**。
   - 喝奶茶 → 奶茶店（柜台、菜单板、封口机、取餐台、店员都在），不是随便一张户外矮桌。
   - 吃便当 → 便利店或长椅；等车 → 站台；剪头发 → 理发店。
   **地点错 = 世界逻辑错，比任何参数问题都致命。**（30 号把喝奶茶放在旧骑楼下，被否）
3. **挑瞬间**：故事往往有十来个时刻，只选**一个画面里能同时交代起因和结果**的。判据是三问——
   - 这一秒她的身体是**静止**的吗？（动作正在发生时模型画不好，且故事读不出）
   - 这一秒**有东西正在失败/正在发生**吗？（冰化了一半、车没来、吸管咬扁、杯子空了）
   - 只看这**一个画面**，故事能不能被反推出来？
4. **出证据清单**：把这一瞬间里"因为前面发生过什么才留下的痕迹"列成 5–8 件道具，每件必须能回答"它为什么是这个样子"。
5. **再动笔写 caption**，先写地点与光的物理（谁在这儿、光从哪来），最后写她那件"没成功"的小事。

**任何一件不说话的道具都是噪音，删掉。**

范例（候车亭那张就是这么来的）：

```
story:  她走了很远来赶这一班车，可今天没有车。
        她先在站牌前站了很久，然后坐在长凳上，把鞋踢掉了一只，
        把喝完的瓶子踩扁，车票一直捏在手里。
        她还在看路的尽头——下一班要到傍晚。
moment: 她已经不再看站牌了，坐在长凳上，一只鞋脱在脚边，
        头偏过去看路的尽头。
```

道具清单与承担的证据：

| 道具 | 承担什么 |
|---|---|
| 一串从画面外走进来的脚印 | 她走了很远 |
| 压扁的空瓶、被瓶底压住的票 | 等的时间很长 |
| 站牌上的 `NO SERVICE TODAY` | 答案是"没有车" |
| 踢掉的一只鞋 | 等到放弃体面 |
| 她盯着路的尽头 | 还在等 |

**六件东西说同一句话**＝故事感。任何一件不说话的道具都是噪音，删掉。

**反例（30 号，被否）**：故事里没有"她为什么坐在旧骑楼下"这一环节，于是墙上那块灯箱只承担了"加一个冷色"的功能——它不是故事的证据，是装饰，模型就把它画成一块贴上去的补丁。**凡是只为配色/明度服务的道具，都会背叛你。**

### G13 注意力预算：不写毫米级的细枝末节（51 号实测，m03494）

用户原话（m03494）：「你不能写那种诸如硬币那种细小的东西在石缝里面那种细枝末节的事情，那样会影响模型的注意力」。

51 号 v1 写了 `a ten-yen coin that has rolled into the joint between two stones`、`a cedar leaf, dry and curled`、`a fine scatter of grit and dry earth`。这三件东西不承担故事，却每一件都要模型花像素去"精确落位"，结果是：注意力从「她绑鞋带」这件正事上被抽走，画面读起来是散的。

**判据**——一件道具能不能写，看它是否同时满足：

1. **它回答"为什么"**：能反推出前因或后果（断掉的带子→鞋坏了；另一只鞋摆整齐→她的秩序感）。
2. **它在画面上占得住**：至少一个手掌大，或者虽然小但属于**成组**（一排吊环、一串夹子）。
3. **不需要精确落位**：不要求"卡在某两块石头之间"这种毫米级位置。凡是"必须卡进某个缝里才对"的东西，模型一定画歪，画歪就是瑕疵。

**不写的**：硬币、落叶、砂砾、尘埃颗粒、飞虫、发丝级配饰、贴着地面滚的小物件、"散落一地"的任何东西。
**改法**：
- 需要"这里有人待过"的感觉 → 用**一件大的、有形状的**东西（压扁的瓶子、踢掉的鞋、摊开扣着的书），不用十件小的。
- 需要冷色/暖色点缀 → 换到**大面积**上（暮色天空、浴衣的灰蓝、被照亮的墙），不要靠一张小纸片（G9 同理）。
- 需要空气感 → 只写光柱本身和它落在石头上的硬边，不写尘埃与飞虫。

**收尾一句封死**（51 号 v2 实测有效）：`Nothing else in the frame asks for attention: no litter, no coins, no leaves, no grit, no scattered small objects anywhere on the steps.`——模型对"没有 X"是听得懂的，写上这句能把它自己补的小杂物压掉。

**证据物数量的上限是 3–5 件**（G2 说 5–8 件是上限，但那是每件都在讲不同的话时；同一句话只需要三件，第四件开始就是重复，重复就会变成噪音）。

### G3 表情：一句简单描写就够（2026-11-06 用户改定，肌肉动向会抢戏）

用户原话（m03593）：「表情不用写肌肉动向，简单描写就行」。

此前（45 号起）写的是毫米级肌肉：`brows pulled together and down`、`mouth corners pulled down by a millimetre`、`lids come down flat`、`tongue pressed against her lower lip`。问题有两个：一是**词量太大**，一条 character caption 里塞进四五处面部形变，注意力从"她在做什么"转到"她的脸"，手和道具反而画得潦草；二是**写太细的嘴部动作容易画出怪脸**（舌头顶唇这类具体动作，模型经常画成吐舌或歪嘴）。

**现在的写法**——三件，一句到两句：

```
Her expression is quiet concentration, plain and simple:
she is looking down at her hands, her mouth is slightly open, and she is not smiling.
```

1. **一句人话概括情绪**（quiet concentration / tired / distracted / pleased）——这是模型真正能检索的部分。
2. **视线落点**（looking down at her hands / out of the window at the empty platform）——决定头与眼的方向。
3. **一个面部事实**（mouth slightly open / mouth closed / not smiling）——只需要一个，多了就抢戏。

`and she is not smiling` 这一句仍要留：模型默认脸是微笑（45 号教训），但**只用一句否定**压住它，不再用肌肉细节去描述"不笑"。

**不写的**：眉毛毫米级位移、眼睑开合角度、嘴角上下几毫米、舌头、咬肌、面部皱纹。这些留给模型自己填，它填的通常比写死的自然。

### G4 高调必须有黑锚点

只写「最深处不是黑，是尘土蓝棕」→ 实测 dark 掉到 1.1%，画面没有底、整体飘。
高调图的正确写法：**「全图只有两处真正接近黑——长凳下、铁皮顶内侧」**，既保住亮调，又有压舱石。

### G5 「统一」与「唯一」不能并存

同时写「一切漂白成同一支暖白」和「蓝围裙是唯一冷色」→ 模型优先执行前者，把后者也漂了（实测 sat 掉到 0.075，整张退化成灰白照片）。
正确写法是**把例外显式排除**：`apart from the blue of her pinafore, every surface in the frame bleaches to the same warm bone white`。

### G6 硬光写边缘，不只写长短

`shadows are short` 只解决长度；实测 strong 只有 0.085，影子边缘全被柔化，光从正午退化成阴天。
必须补：`each shadow edge is cut like a blade, with no gradient at all`。

### G7 饱和度低不等于"高级"，先看它是不是事故

实测 sat 0.075 + rgb 0.712/0.704/0.697（三值几乎相等）= 整张图退化成灰白照片，不是风格。
判断标准：**画面里应该有色差的地方有没有色差**。蓝围裙如果读成灰蓝，就是事故。

### G8 人物永远会自动撑满画面——必须给比例尺

用户原话（m01101）：「人物在这个图片里显得很大」。
实测：出图里她坐姿占画面高度 60%，而设定是「一个空荡荡的候车亭里的一个小人」。

**机制**：模型在二次元语料上训练，"有人物"就等于"人物是主体"，会自动把她放大到填满画面。只写"她很渺小"没有用，**渺小是形容词，比例才是事实**。

三种写法，至少给两种：

1. **分数**：`her seated body is about a quarter of the picture's height and less than a tenth of its width`
2. **相对物**：`two thirds of the bench is empty beside her`、`the empty bench beside her is wider than she is`、`the wall behind her is twice her seated height`
3. **可量距离**：`a metre and a half of empty air between the top of her head and the roof`、`the sign hangs with its top at two and a half metres, well above her head`

外加**机位距离**：`the viewer stands on the opposite shoulder seven metres away, with the whole width of the road between`。距离一写，透视缩小就跟着来了。

**反例**：只写 `small in the frame` / `tiny figure` / `dwarfed by the shelter`——全是形容词，模型照旧放大。
**检查**：出图后量她的高度占比，与设定差 10 个百分点以上就是事故。

**人物显大，往往是空间写小了，不是人写大了**（50 号电车实测，m03317 用户原话「老问题，人物太大只了」）。50 号 v1 写了「她占画面高的一半」，模型画出 56%——**比例是准的**，但画面里车厢天花板压得低、座椅画得大，整节车厢被她撑满，读起来就是「人物太大」。只缩比例治不了这个，必须同时把空间撑开：

1. **给内部尺寸锚**（不是给她的尺寸）：`the floor-to-ceiling height of the carriage is one and a half times her standing height`、`the connecting door at the far end is a head taller than she is`、`the window sill runs at her waist height`、`the seat cushion is at her knee`。空间一有尺寸，她的尺寸就被反推出来了。
2. **把场景做成有纵深**：`the carriage runs away from the camera toward the connecting door at the far end`、`the window band and the strap rail recede with the depth`。
3. **放一个前景大物当比例尺**：`the nearest seat back cuts into the bottom left corner of the frame, much nearer to the camera than she is and so much bigger, its top edge reaching a third of the picture's height up from the bottom edge`。前景一大，中景的人立刻显小——这比任何分数都管用。
4. **机位拉远**：三米改六米，十米外的门当远处锚点。
5. 长物件（吊环横杆、扶手）也要写「向深处退」：`it is a receding line and not a flat bar pinned to the picture plane, and the straps at the far end are visibly smaller than the ones near the camera`。否则它会变成贴在图面上的一条横杠，把纵深压平，人就又显大了。

### G9 颜色必须落在被照亮的大面积上，否则图一定发灰

39 便利店 sat **0.113**、42 楼梯间 sat **0.146**，而同期 40 厨房 sat **0.246**（用户判"厨房那张好了"）。三张写法一模一样，差别只在**颜色写在哪**：

| | 最暗端 | 最亮端 | 被照亮的最大面积 | sat |
|---|---|---|---|---|
| 40 厨房 ✓ | 柜内黑 | 窗玻璃 | **honey wood 台面 + cream 瓷砖** | .246 |
| 39 便利店 ✗ | deep **cool grey** 钢皮 | **cream** 杯盖 | **pale grey 台面 + 奶油货架** | .113 |
| 42 楼梯间 ✗ | 井道黑 | 窗玻璃 | **dirty cream 墙 + grey terrazzo** | .146 |

**机制**：模型忠实执行配色表。我把色相给了红杯套（小）、蓝托盘（小）、红鞋（小），把大面积全给了 grey / cream / pale——它就画出一张灰图，**而且它是对的**。写「gets stronger in it rather than paler」也救不回来，因为没有一个有色的面可以变浓。

42 更隐蔽：`bottle green` 墙裙我写了，但它压在 dado rail 以下的暗区，被压成黑——**颜色写在暗部等于没写**。

**规则**：
1. 先决定**哪块面最大、最亮**（台面 / 墙 / 地面 / 桌面），把饱和色给它，写具体色名（ochre / butter / amber / yellow-green），不写 grey / cream / pale。
2. 中性色只留给小物件（钢边、铆钉、窗台、纸）。
3. 暗部只能承担「暗」，不承担色彩任务；写了绿的墙裙就要让光照到它。
4. 光本身要有色相：`it is not white light - it is an old warm-white tube, the colour of weak tea`，接 `everything it falls on takes that colour and gets stronger in it rather than paler`。

**lint 关 9**（色彩落点）自动查三件事：summary 里色相词 <3 → WARN；中性色词多于色相词 → WARN；写了「最亮的东西」但附近 200 字无色相 → WARN（玻璃/窗/天空/太阳/灯管豁免）。
**出图后看 sat**：目标 ≥0.16；<0.13 就是灰图，回来看这一条。

### G10 全图只允许一个视点，每一句都要服从它

39 v3（m02895）她被画成坐在柜台**里侧**、隔着柜台看观众 = 店员在自家收银台吃饭；带铆钉的柜台前面板占满下 1/3。42 v3（m02897）她被顶到左上角、头被裁、站着扶扶手，坐第三级系鞋带的故事全没。

**两条真因**：
1. **视点句自相矛盾**：39 的 summary 里同时有 `photographed the way a person sitting down and eating alone would see it` 和 `seen from across the counter`。模型任选一个执行，选了后者，整个空间翻到对面。
2. **比例句被字面执行并裁头**：42 写 `horizon runs level across the top of her head` + `four fifths of the frame is the flight below`——模型把「视平线过她头顶」执行成「她头顶贴上边缘」，再按四比五填楼梯，人就顶出画面被裁。还有一处：正文写 `the window is in the middle of the picture's upper half`，模型干脆把窗裁掉只留光斑——「窗在画面某处」这类位置句不如「窗在镜头背后，只留它投在对面墙上的光斑」可靠。

**规则**：
1. 动笔前先定一句话视点（谁在看、从哪看、离多远、什么角度），写进 summary；其余每一句（柜台、窗、货架、反射）都必须与它自洽。写完逐句问：「这句在哪个视点下成立？」两个视点打架就删一个。
2. 视点要推出**物理后果**并写明：坐柜台边 → 只见台面不见前板（`the front panel is below the bottom edge of the frame and is never seen`）；店在身后 → 货架不入画，只留玻璃挡板上的反射。
3. 人物完整入画必须**写余量**，不许用「贴边」句式：写 `all of her is inside the frame with a full step of wall between the top of her head and the top edge`，不写 `horizon runs across the top of her head` / `four fifths of the frame is X`（这类句子模型会字面执行，把 X 顶到边缘并裁掉人）。
4. 场景内光源可以「在镜头背后」：写 `the window stands behind the camera and is never seen; the only evidence of it in the frame is the slab of light it throws across the wall opposite`。这比把窗塞进画面更稳，而且扶手影子落在光斑上的意外之美要主动写进去（`the handrail between the camera and the wall throws its own shadow diagonally across the slab`）。

### G10 补：视点和明度必须同源——先定镜头站在哪一侧，再决定哪一端暗（58 号 v1 翻车，2026-11-06）

58 号 v1 同时写了「镜头在廊下往外看院子」和「画面顶部暗、底部亮」，两句各自成立，合起来不可能：站在廊下往外看时，廊下的板在**镜头这一侧**（画面下方），阳光在院子里（画面上方），应该是**上亮下暗**。模型只会挑一句执行，于是要么把院子放到画面上方却仍然压暗，要么把暗部塞到底边。

规则：
1. 动笔前写死一句「镜头站在哪、朝哪看」，例如 `the viewer is standing out in the garden in the sun looking in at a shaded veranda`。
2. 由这一句**推导**出明暗：镜头站在太阳这一侧 → 前景亮、屋顶下暗 → 上暗下亮；镜头站在阴影里往亮处看 → 上亮下暗。明度头里的「上/下/左/右 哪端亮」必须是这句的结论，不能是另写的偏好。
3. 同一个视点还要推出**道具的相对位置**：镜头站在院子里，那她脚前的板才是亮的、她身后屋里才是黑的（本图三带：屋檐与屋内 / 檐影里的板与她 / 脚下阳光里的板）。
4. 自查一句：把明度头那句「X 在上、Y 在下」单独拿出来，问「镜头站在哪才能同时看到这两个」——答不上来就是视点写错了，不是明度写错了。


### G11 灯不要画进画面，写「光从哪来、打到哪、哪没打到」

39 v4（m02976）里那支便利店顶灯「太出戏」（m02980 原话）——它成了画面里最亮的实体，抢掉人物，而且一个大白灯箱在深夜便利店里看着像棚拍灯。**只要把光源写成实体，模型就会把它当主体画亮。**

**正解：光源移到画框外，用光路三件套取代灯本身。**

1. **一句话交出来源，同时封死实体**：
   `There is one hard light source and you never see it: the fitting is above and behind the camera's right shoulder, outside the frame, so the picture holds no lamp, no tube, no diffuser and no glowing panel of any kind anywhere in it - only the light that fitting throws.`
   封死清单要逐个点名（lamp / tube / diffuser / glowing panel / fixture），只说 `no light source in frame` 不够。
2. **三个落点，且明确「只落这三处」**：`it lands in three places and nowhere else:` 后面列具体物（台面靠窗远端 + 窗台 / 她头顶与近侧肩 / 柜台外侧地板条带）。落点必须是**物**，不是方位（写 `on the sill`，不写 `on the right`）。
3. **衰减写方向与档位**：`the brightest part of the counter is a band that starts under her forearm and runs away toward the window, and it falls off toward both ends and toward the camera, so the near end under her elbow is a stop darker than the far end.`
4. **未照亮区逐项点名**：`Everything the light does not reach holds no light of its own and keeps its colour anyway: the ceiling across the top of the frame, the panel under the counter, the inside of the window frame, and the far side of her face.`（注意用 `holds no light of its own`，别用 `unlit`——`unlit` 会撞关 3 的暗调词表。）
5. **留一个空块给顶棚**：把原来写灯的那个 item 改成 `it holds no light of its own ... no lamp, no tube, no diffuser, no glowing panel, no fixture of any kind`。空块比删块好——它占住画面顶部，防止模型自己补一盏灯进来。
6. **颜色要跟着光走**：写 `it is old warm-white light, the colour of weak tea`，不写 `it is an old warm-white tube`——**「tube」这个词本身就会画出一支灯管**。同理避开 `the tube above turns all of it warmer`，改成 `the light from behind the camera turns all of it warmer`。

检查口径：全文搜 `tube` / `lamp` / `fixture` / `diffuser`，每一处命中都必须在否认句或画外句里，否则就是给模型递了一支灯。

---

## 第 3.5 步：构图（景别 → 构图 → 光，顺序不可换）

写任何一条提示词之前，先在这一层做三个决定，再动笔写光。完整表在 `references/composition.md`（景别 8 级换算、视角 5 种写法、构图 9 种可执行句、改构图 12 条手段、诊断七问、给方案规矩）。

三句硬约束：

1. **景别 = 机位距离 + 人物占画面高的分数**，两个数必须同时给，且必须补余量句（`all of her is inside the frame with a hand's width between the top of her head and the top edge`）。只给分数会裁头（G10）。
2. **不写构图名词**。`rule of thirds` 无效；`she stands four tenths of the way across the frame, and the whole left third of it is empty shelf, lit flat` 有效。
3. **改构图先改位置与光，最后才改语言**：bbox、机位句、亮块位置优先于形容词。想移注意力就搬亮块，比挪人有效十倍。

**一图只用一种视角**，写两种视点就翻面（G10 教训：39 号「坐在她旁边」+「隔着柜台看」同时出现，整张空间反转）。

看图诊断七问（问完再改）：主体在哪占多大 / 视线朝哪、留没留白 / 有几条线收到哪、有无切画面的线 / 三层哪里是空的 / 最亮的块抢不抢 / 边缘切了什么 / 这张图靠什么站住。

### 画面上下就是远近：bbox 必须服从纵深（56 号实测，2026-11-06）

平视时，**画面上方＝远，下方＝近**。凡是「她走过去才遇到的东西」，y 必须比她小（更高）；凡是「在她和镜头之间的东西」，y 必须比她大（更低）。写反了模型不会纠正，它只会把断枝画在她脚下——变成绊脚石。

同时三条：

1. **地面/路径/走廊这类连续面，bbox 要从底边一直覆盖到消失点**，不能只覆盖人物附近那一段。56 v1 的路径块只写了 `[0,780,1024,1420]`，而她站在 790–960，等于路径的远端在她脚下就断了，纵深受阻。
2. **远处的东西要写「比她小，因为更远」**，不能只靠 bbox 缩小——模型会把远处小物放大成本体大小。
3. **前景与主体是两层时，前景块的 y 必须完全在主体之下**，且写明「out of focus because it is closer than anything else」。

自查一句：把她脚下的 y 画一条横线，问「这条线以上是什么、以下是什么」——以上必须是远方，以下必须是镜头到她之间的地。

### 自拍、手持设备与「谁是镜头」（61 号实测，2026-11-06）

61 号第一版把「手机背面」画进了画面，出图立刻读成「有人拍她，她手里举着手机」——不是自拍。原因不是构图，是物理：

1. **自拍时，手机在镜头的位置上，所以画里不可能出现自己的手机。** 想画「举着手机的手」，只能画**伸向镜头的那条手臂**：从画面某个下角进来、在手腕之前被画框切断，越靠近边缘越宽越虚。
2. **自拍的光是正面偏上的平光**（屏幕就在镜头旁），不是从下往上的脚光。写 `the light comes from the front and a little above, cold and flat, so there is a small shadow under her nose and under her jaw and nowhere else`。
3. **自拍的机位**：镜头在她一臂之外、略高于眼，广角把远处的街推远、把近肩和手臂拉宽。这句要写，否则出来是普通街景 + 一个贴在前景的大头。
4. **自拍里她的视线是进镜头的**（看镜头＝看屏幕），不是「低头看手里的手机」。
5. 若真要在画里看到手机（镜子自拍/别人代拍），必须在 caption 里交代镜子或第二个人，不能靠模型自己圆。

**光环（halo）必须给尺寸和位置**，否则会画成浮在背景上的一只大白环：`a four pointed star halo floating just above the back of her head, one head high across and a dull pale grey rather than bright`。三条缺一不可：贴哪个位置（头顶后侧）、多大（一个头高）、多亮（暗白、不发光）。

### 朝向必须拆成三句，缺一句就画反（62 号第一版实测，m04167）

**补一条（77 号实测）：左右方向词一律不可靠。** 写了 `riding from the left of the picture towards the right`，出图是从右往左骑。左右会被镜像、会被"行进方向=朝右"的默认吞掉。
改用**可核对的物象事实**：`her front wheel is the one on the left of the picture and her rear wheel the one on the right`；`her face is turned towards the left edge`；`the back of her head is towards the right edge`。这类句子模型没法反过来理解。

用户跑 62 号第一版时反馈「角色的朝向错了」。当时我写的是 `seen from behind and from the side, three quarters turned away` —— 一句糊的话同时承担三件事，模型只取了「背对」。以后一律拆成三句，每句只回答一个问题：

1. **她面朝画面的哪里**（物理指向）：`she walks towards the right edge of the picture`。
2. **观者看见她的哪一面**：`the viewer sees her left side, her left cheek and the tip of her nose in outline`。要写具体到能验证的部位（哪侧脸、哪侧肩、鼻尖、后脑），不写 `three quarters turned away` 这种角度黑话。
3. **她的脸朝哪里 / 看不看得见**：`her head is tipped down and to the right at the water, and she never looks at the viewer` 或 `her face is not visible at all`。

补充三条：
- **小尺寸人物用侧面（full profile）**。一个占画面 1/6 的人，侧面剪影比 3/4 背影可读十倍，也更像海报。
- **不要同时写「背影」和「侧脸」**——除非明确说「她回头看」。背影+侧脸=模型给你一张拧了 180 度的头。
- 朝向一旦定死，**道具也跟着定向**：伞往行进方向倾、视线落点在她前方、脚步朝她面朝的方向。道具反向是最容易被一眼看出的破绽。

### G14 名画融合：点名作品 > 描述结构（64 号 v4 实测通过，m04292 用户判「这回还原了」）

要复述一幅名画，**把作品的作者与标题写进句子，比自己描述结构有效十倍**。v1–v3 我把旋涡圈数、星的环数、带的宽度全写出来，三次都不像；v4 只加了一句 `This sky is painted the way Vincent van Gogh painted the sky in The Starry Night`，并删掉我自己的细节，一次就过。原因是：结构写再细也只是我的转述，作品名是模型本来就有的完整先验。

三条写法：

1. **写成「画法」不写「复制」**：`This sky is painted the way Vincent van Gogh painted the sky in The Starry Night.` 不用 `in the style of`（会变成滤镜式的表面模仿），不用 `a copy of`（会把人物挤掉，出成那张画本身）。
2. **点名之后必须自己删细节**：只保留 3–4 个可验证骨架（64 号留的是：两条 S 带互缠 / 沟是天空唯一的暗 / 星有黄环 / 右上小橙月）。留得多，模型会按我的错解画（v2 被我写成满屏靶心）。
3. **名字只锚它该锚的那一层**：名字放在该元素的块首句 + summary 首句；人物、地面、道具照旧用自己的写法。否则整张变成那张画，人没了。

竖幅 vs 横幅：原画多半是横幅，竖版等于「裁进它的某一段」。裁的时候要给它**纵向行程**（`from the top edge of the frame down to just above the village`），并明确「这张里只出现这一段」，否则模型硬塞整幅。想真正还原画面节奏时，主动建议改横版。

同一套还适用于：某位画家的画法（`painted the way Hokusai printed` / `the way Vermeer lit a room`）、某种版画工艺（`printed in flat areas of colour with the paper left bare`）、某种摄影（`lit the way Fan Ho lit a Hong Kong alley`）。作品名/人名只用在**它真正解释得通的那一层**。

### 手势必须写成「哪一面朝观众」+ 每根手指一段（69–71 号三连翻车，m04417 用户给图解）

连着三版都画错：写「食指和中指竖起、另两指收进掌心」→ 出标准剪刀手；写「五指张开」→ 仍然糊成一块。原因是**手不是形状，是两面**：手背有指节和骨，掌心有掌纹和指腹。不指定哪一面朝观众，模型就挑自己最熟的那一面（手背＋V）。

写法四条：

1. **先定每只手的朝向**：`the palm of that hand is turned in towards her own face, so we see the back of it` / `the palm is turned out towards us, so we see the open palm`。这一句比后面所有手指描述都重要。
2. **再用「那一面专有的东西」证明它**：手背写「指节、四根骨、皮肤绷紧」；掌面写「三道掌纹、指腹朝我们、整只手在自己的影子里」。写不到这些，模型会自己换面。
3. **每根手指一段，只写长度、方向、高低，不写左右**：`the index is the highest and the most vertical; the middle is as long and leans a hair to one side; the ring a little shorter; the little finger the shortest, set apart with a clear gap` —— 左右写多了必错，高低和长短不会错。
4. **双手手势要写两手的相对位置**：`one above the other on nearly the same vertical line, with a hand's width of white ground between them, and the upper palm faces down while the lower palm faces up`。手势的意义常在两手之间的那块空处，不在手上。

反例留档：`index and middle fingers up in a V, the other two folded into the palm` = 剪刀手配方，永远不要写。要「张开」就写 `all five extended and all separated, none of them touching another`。

**实测确认（2026-11-06，71 号）：** 按这套写法出图，用户回「还行吧，算你过关」——双手版成立。两条必须记住的几何：
1. **掌心相对要求两手都往身体中线收**，一上一下叠在同一条竖线上，中间留一掌宽白底。把手分在身体左右两侧时，两只掌心物理上不可能相对，模型只能各画各的。
2. **手要够大才画得出手指**：机位收到腰以上、每只手占画面宽 1/6。人物 3/4 高时手只有巴掌大，五指必然糊成一团。
3. 除手以外一切从简：无裙褶细节、无鞋、无道具、无地平线。注意力被别处分掉，手指就丢。

### G15 倒影与镜像：只说「这是倒影」不算数，要有只能倒置的证据（77 号实测，m04697）

77 号写的是「四分之五的画面是水洼的倒影，天在上还是倒的」，出图仍然是一张**天在上、路在下**的普通风景照：模型的世界先验「天在上」比「这是一面镜子」这句陈述强得多。

四条写法：

1. **给物理上只能成立的倒置证据**，不要给解释：水面那条横线必须**横穿画面中部**（不是贴着底边），树冠必须**长在画面下缘**、根朝上，人的脚必须**朝画面上方**。任一条单独出现就足以让模型翻转整个空间。
2. **写「倒影比实物暗、比实物软」的定量关系**：`the water holds the whole image a fifth darker than the sky really is, and takes the fine edge off everything it holds, so no reflected edge is quite sharp`。这句话本身不能建立倒影，但能让「镜面」看起来像水而不是像贴图。
3. **介质上的痕迹必须单独成块，并且显式否认它在内容上**：77 号把「水面上的尘埃与花粉」写进了天空块，出图变成**晴天的满天星**。正确写法：`these specks lie on the film of the water and not in the sky, and the sky behind them is completely clean`。
4. **倒影里的光源要说清是「映出来的」**：`the light comes from the sky the puddle is holding` —— 真实光源在画面外，画内只有它的像，所以这里允许出现"天上的亮"，但画内不得再有任何灯。

**78 号实测（倒影第一次成立，但人物倒影不行）**：dark 0.134 / soft 0.821 / sat 0.287 / p99 0.975。倒影整件事**成立了**——底部的叶子确实叶尖朝上、水里的云确实倒着、她自己确实头朝下。但暴露三条，必须补：

1. **倒影两半必须是同一片天，要把这句话写出来**：`the blue in the water is the same blue the sky is, only one step deeper`。不写，模型会把下半画成青绿、上半画成深蓝，两半像两张图拼在一起。
2. **水面必须有近岸，或者水面自身的痕迹要铺满全幅**：78 号的水一路流出画面下缘，于是下半幅读起来像**嵌进画面的一块镜子**而不是一洼水。写法：`the near edge of the flood is inside the frame, a ragged wet line across the bottom, and past it the ground is merely damp`。
3. **人物倒影要写「整个人都在，被水面压扁」，只写 head 就会出一个头**：78 号只写了「她的头顶指向画面下缘」，结果倒影只有一个粉色的头。写法：`her whole reflection is there, from the soles of her shoes to the crown of her head, and it is squashed to two thirds of her height by the angle of the water`。倒影和她之间不能隔空——`the soles of her shoes touch the soles of the reflected shoes with nothing between them`。

配套：**剪影照必须写「暗部是最饱和的」**（77 号参考暗部 sat 0.619、出图 0.264）。深蓝天这类「又暗又艳」的东西是剪影图的气血，只写它暗，模型会把它拉灰。写法：`the deepest blue is both the darkest large area and the most saturated thing in the picture`。

### G16 介质照明的第二件：擦痕必须和她手上的湿痕连在一起（79 号实测通过，m04789）

79 号（雨窗）整件事成立了：雨痕竖直、末端挂珠、玻璃内侧起雾、只有一处清楚。但有两个尾巴：

1. **擦痕和手脱开了**：写了「她用手背擦开一道」，模型把擦痕画在画面中间、把手画在右边，两只手和那道痕没有关系，看起来像在招手。正解是把手和痕绑在同一处：`her hand is pressed flat on that patch and the patch is exactly as wide as her hand and starts where her wrist is`。
2. **「一道弧」会被画成螺旋**：写 `the stroke starts low, sweeps up and to the left, and ends in a small hooked flick`，出图是一圈一圈的大漩涡，像刷锅。正解是把它写成**单程**：`one single pass of the hand and no going back over the same place, so every streak inside it runs the same way and none of them curls`。
3. 人物会被放大：写了 `a third of the height of the picture`，出图占了五分之三。无人/小人物的图里比例尺要写两遍（分数 + 具体物件对照）。

**介质类已验证的四种现象（79 号一次全中，可复用）：**
- 竖向雨痕 + 末端挂胖水珠 + 水珠下一小截滑动湿痕（停住的那几条没有拖痕）
- 雨痕穿过哪里，后面的东西就在那条线上**错位**（灯柱横向断两次、路沿跳）
- 起雾的内侧 + 一处被擦开（全图只有那一块是清楚的）
- 水珠是凸透镜，每颗里有一份倒过来的小街景

### G17 独立小道具必须自己「站在一个面上」，否则会被就近吸附（80 号实测）

80 号空房间整件事成立：没人、高调、三处黑、地板上的窗形光斑、墙上一道长斜影。只错一样——**那只绿玻璃杯跑到地板上去了**。

我在 summary 里写了「A glass of water stands on the windowsill」，也给杯子单开了 item、bbox 压在窗台最低处。但杯子还是被挪到了画面中间的地上，离开它背光的位置，于是那只「全图唯一饱和色」失去了存在的理由。

原因：**家具 caption 里的从属关系，管不住独立 item 的位置**。独立 item 的 bbox 只告诉模型「放在这个矩形里」，不告诉它「此处有没有一个可以放东西的面」；模型发现那个矩形底下是空的、没有台面，就自动挪到最近一个看起来能放东西的平面上。

正解三条：
1. **把这个「面」的画面位置写死**：不是 `stands on the windowsill`，而是 `the windowsill is a flat ledge that runs the whole width of the window at one below the middle of the frame, and the glass stands on that ledge with its base sitting on it and the ledge visible on both sides of it`。
2. **bbox 底边与那条面线重合**（不是压在家具 bbox 中间），左右留出可见的台面。
3. **显式否认地面**：`it is not on the floor and not standing on anything lower than the sill`。

同样适用于：桌上的杯、架上的书、台面上的工具、床头柜上的东西——凡是「小物件 + 大平面」的组合。

**另记一条 80 号的意外收获**：我写「the light from the window does not reach this wall」，模型却在那面墙上画了一道很长很斜的影（是窗框透过来的），比我的设定好看得多。教训是——**先算清光能打到哪，再决定墙上要不要留影；把墙堵死不如留一条斜影**。斜影几乎是所有空景里最便宜的构图材料。

### G18 双人图：四只手要逐只点名，身高差要用画面坐标写（81 号实测失败）

81 号（末班巴士，一个托住另一个睡着的头）整条故事**没发生**：托着脸的那只手是睡着的人**自己的**，坐着的人两只手都平放在座位上，两个人根本没接触。同时写的高度差也失效——两个人在画面里几乎一样高。

五个原因，全部是双人图专属的：

1. **「the seated girl's palm」这类指代在双人图里会失效**。单人有「她」，双人有「她和她」，模型分不清这个 palm 长在谁身上，于是把托脸的手给了被托的那个人——因为它就在那儿，最近。写法：**每只手都带上人名**，`hoshino's right palm is turned up under aru's forehead`、`aru's own right hand is closed around the strap`，一次也不要用 the seated girl / the other one。
2. **必须数清四只手，逐只交代**。双人图固定写法：`four hands are in the picture and each one is doing one thing: hoshino's right is under aru's forehead, hoshino's left is flat on the bench, aru's right is closed on the strap, aru's left hangs at her side open and touches nothing`。少交代一只，模型就自己编一只，而且往往编成"撑着被托的人自己的头"。
3. **要显式否认错的那只手**：`aru's head is not resting on her own hand and not on her own arm: it is held up entirely by hoshino's palm`。这是 81 号唯一真正缺的一句。
4. **身高差不能用分数写，要用画面坐标写**。写 `aru is four fifths of the height of the picture` 会得到两个差不多高的人——因为弯腰这个动作把身高抵消掉了。改成描述两个头顶落在哪：`aru's crown is inside the top fifth of the frame, and hoshino's crown is below the middle of the frame, so the two heads are a head and a half apart`。
5. **接触块的 bbox 只框接触面，不要框到脸**。81 号把接触 bbox 框到了睡着的人整个头脸，模型就在那个矩形里画了一只"扶着脸的手"，完全不管手连到谁。

**G18 补充：接触点的读法由 bbox 决定，不由文字决定（81b 实测通过，m04859）**

81b 通过了（四只手点名 + 否认自撑 + 画面坐标写身高差），但读法变了：我写的是「掌心贴太阳穴、维住她的头」，出图变成**手放在她头顶上（head pat）**。原因是接触块 bbox 的上沿压在坐着的那个人的头顶上，模型就把手放在矩形最上沿。

要把读法锁在「托」而不是「拍」，接触 bbox 必须覆盖**接触面本身**，并补一句水平位置：`the palm is at the height of her eyes, not on the crown of her head`。手放头顶是安慰，手在颧骨太阳穴是承重——这两件事的读法差很远。

### G19 光环、发光件与小道具的尺度三分钟（81 号实测）

- **光环写 faint 不算数**。要写尺寸和否定：`a ring no wider than her head, flat and thin, it does not glow, it casts no light, it is not a light source in the scene, and it does not overlap the window or the sky`。81 号两个光环被画成巨大的发光圆环，还横跨窗户，成了全图最亮的东西（p99 0.957）。
- **小道具的尺度要以人为参照**，不能以自己为参照。写 `the same height as her thigh` 会得到一个半人高的书包；写 `no taller than her own head` 才稳。
- **「画面里没有灯」必须逐项否认**：`there is no light fixture, no lamp, no ceiling panel and no glowing surface anywhere inside the frame`。81 号右上角出现一盏亮着的灯，尽管我在 summary 里写了光来自画外。


## G20 每一处光照都要能在 bbox 几何上兑现（83 号实测，2026-11-06）

83 号混合光：文字写了 200 词的「她左半身橘、右半身冷白、分界线从锁骨到膝盖」，出图她是**单色暖光**，身上没有任何分界，也只有一道影子。

对账一下几何就清楚了：暖光斑 bbox x 0–700，冷光斑 bbox x 820–1536，她的 bbox x 812–1080。**冷光能到她，暖光根本到不了她**。文字说的「两光夹着她」在画面上从来没有成立过，模型于是自己编了一种光。

这就是混合光（以及一切多光源、以及「某个东西被某道光打到」）的检查法，三句话：

1. **光从哪个方向进、落在画面的哪一块**——用可以指认的东西定位（`the parallelogram reaches from the bottom-left corner to just past the middle of the floor`）。
2. **主体站在哪一块**——她的 bbox 和那道光的 bbox 重叠的部分，才是她身上会被照到的地方。
3. **如果要「两种光同时照到她」，两块光斑必须在画面里相遇，并且她就站在相遇处**。相遇处要写成一条可见的线：`the two patches overlap along a band that runs across the floor at two thirds of the way up the frame, and she is sitting on that band`。

一句话自查：**把每个「被 X 光打到」的句子拿出来，问它的 bbox 和 X 的 bbox 有没有重叠**。没有重叠，这句话就是模型自由创作的地方，它一定不会按你想的画。

## G19 补充：光环第二次失败，只写尺寸不够（83 号，2026-11-06）

81 号之后我以为「no wider than her head」就够了。83 号出图给她加了一个**比头大三倍的白色发光线圈**，像浮在头顶的闪电符号，而且是全图最亮的东西之一。

尺寸形容词对这种装饰件完全无效，它需要的是**形状 + 画法 + 三连否认**，三样都要：

- 形状：`a single thin pale ring drawn in one continuous line, smaller than the width between her ears`。
- 画法：`it sits flat in the air like a piece of wire, and it is drawn with one line and not filled`。
- 否认：`it is not white, it does not glow, it is not a ring of light, there is no halo of light around her head, and it casts no light on her hair or her shoulders`。

漏掉任何一样，它就会变成发光装饰。

## G25 修订 + G26 无人图的尺度锚（91/92 实测，2026-11-06）

**先改正 G25 的结论。** 91 号特意去掉了角色名（`original character`），写 1/12 高，出图仍是 36%（4.3 倍）。所以**「角色名」不是真凶**。四张的实测倍数：86 号 1/5→1.8×、87 号 1/12→45%、90 号 1/4→45%、91 号 1/12→36%。真正规律是：**画面里只要有一个人，MOSS 就把她排到至少 1/3 画面高；小于 1/3 的比例句基本无效**。要小人物只剩两条路——① 按 1/3 设计构图，把「她很大」当既定条件用；② 不画人，只画人的痕迹。角色名与光环仍然要删（它们另有一个坏处：会召唤发光光环）。

**G26 无人图必须有尺度锚，否则每件道具都按「道具特写」尺寸画（92 号实测，用户原话「东西还是很大」）。**
- 92 号 bbox 尺寸其实被严格遵守了（鞋渲染出的宽度正好等于 bbox 给的 190px），但整张仍读成「大东西近景」。**真因不是 bbox，是画面里没有任何「人尽皆知尺寸」的参照物**，观者无从判断这堆东西是 2 米外还是 20 米外，模型于是给每件道具「英雄道具」体量：鞋成 30 厘米、脚印成脸盆大的坑。
- 修法（93 号）：在画面里放**一把尺子**——一件尺寸人人都知道的小物（塑料瓶 20cm / 易拉罐 / 一次性打火机），并在 summary 里明写「它是全图唯一量具」+ 逐件换算（`the shoe is shorter than the bottle`、`the open canopy is about two and a half bottles across`、`each footprint is one bottle long`）。
- 同时给每件道具一个**真实厘米数**（`twenty-five centimetres heel to toe at the most, no bigger`），并显式否认（`not a big umbrella: it is a small folding one`）。只写「比瓶子短」不够，模型会把瓶子一起放大。
- 脚印写成坑的真因：`a shallow depression holding a thin film of water` 会被画成水洼/坑。正解 `no deeper than a finger … never a pool, never a hole and never a crater` + `one bottle long and no wider`。

## G25 人物画太大，真凶是「角色名」（90 号实测 + 用户判断，2026-11-06）

90 号写 `her head reaches a quarter of the way up the frame`、character bbox 只给画面高 12%，出图她仍占了约 45%（用户 m05100 原话：「人对比起来还是大了，也许你按之前极简版那样写就不会有这种问题了」）。

对照同期所有条目：**凡是 character caption 以 `hoshino (blue archive), takanashi hoshino` 开头的（82/83/87/89/90），实测放大 1.8–3.6 倍；不带角色名、只写 `a girl in …` 的（73 号等），偏差小得多。** 机制：角色名让模型把这张当成「角色立绘」任务，按主体排版；场景照里的远景人物，比例句才生效。

规则：要小人物就三件事同时做——① **不写角色名、不写作品名、不写光环**；② 一分钱外观细节都不给（删发色、瞳色、服装细节），只写 `a young woman in a long dark coat, seen from behind, too far away to be more than a small dark shape`（G22：整段不出现 face/jaw/cheek/eyes）；③ bbox 压到目标的一半。

## G24 构图：前景道具抢主体、bbox 偏了人物还是居中（89 号实测，2026-11-06）

89 号光感过关（dark .503 / 唯一暖色成立 / 闪光照到顶），但用户一眼判「构图差点意思」。逐项对账：

- **前景大道具抢主体**：洗衣篮 bbox `[700,770,1000,950]` 在画面下缘正中、离镜头最近，出图它成了巨大前景主角，把她的脚整个挡住，整张读成「拍篮子」。规则：前景道具**不得压在中轴线**、**不得低于主体的脚踝线**、**不得比主体更靠近镜头**；真要前景道具就写「只在画面一角、只露出一部分、被画框裁掉一半」。
- **bbox 偏了，人物还是居中**：character bbox 中心 x=600（离中线 11%），关 10 通过，出图她仍被摆在正中、与身后洗衣机阵列对称。模型对 bbox 的中轴偏移几乎无感。要真正偏，必须让两侧的**满/空不对称**：一侧道具阵列铺满、另一侧显式写成空的（`the whole left third of the picture holds nothing but wall and floor`），并且 bbox 再偏一档（0.28 而不是 0.39）。
- **两条横贯全幅的灯管 = 水平分割线**（与 47 号绳子同一个错）：顶灯不要写「横贯画面」，写成「只在左上一段、到墙就断」。
- **亚像素细节写在 character caption 里画不出来**：瞳孔里的两个红点、额头上的针尖反光，全部没出现。这类细节要单独给一个极小 item，bbox 只框那一处（眼睛那块 60×30 像素），caption 只写那一个东西。

### 光环第三次失败的定稿写法
出图成了**三圈同心发光弧**＋在墙上投影。要写死三件事：`exactly one ring and no second one`、`no inner ring and no concentric arcs`、`it casts no shadow on the wall behind her`。

## G65 人物默认不居中——这是默认值，不是可选项（用户 m04130 / m09552 定，2026-11-08）

用户原话（m09552）：「人都在正中间，把人默认不在正中间写进规则，除非特意要求的人物居中」。

**为什么 144/145 会被指出来**：两条的 character bbox 中心分别在 0.58 与 0.59，等于中线；caption 里我写的是 `turned a little towards us and a little to our left`——**这是形容词，模型不执行**。人一旦居中、两侧又对称排满道具，整张就读成「陈列」。

**落位三件套，缺一件就会回中**：
1. **bbox 中心**：横图落在 0.33 或 0.66；竖图落在 0.30–0.35 或 0.65–0.70。**0.42–0.58 是禁区**。（关 10 只拦 6%，比这宽得多，所以还是靠自觉。）
2. **caption 写死相对位置**：`she stands a third of the way in from the left edge`，不放 `a little to our left` 这种模糊词。
3. **另一侧显式写成空的**：`the whole right third of the picture holds nothing but pavement`。空侧不点名，模型会拿道具把它填满，然后重新读成对称（G24 同一条）。

**允许正中的三种情况**：对称建筑/仪式的正面像、证件式肖像、用户明确说要居中。其余一律偏；**偏了就把留白交给对角**——人在右，空留给左上。

## 默认不写任何文字（m04470 用户定，2026-11-06）

用户原话：「我没叫你写字你就别写」。

- 默认合同：**画面里不出现任何文字**——不写招牌、不写标签、不写门牌、不写书名、不写涂鸦、不写海报字样，也不要为了「氛围」塞一块 paper with words on it。
- 只有用户点名要文字（贴参考图上有字要复刻、明确说要招牌/书名/标语）时，才用 text 块，并且要按「文字块的透视」写共面与收敛。
- 动画模型出拉丁字母极容易糊成乱码或拼错，一旦糊掉整张图就废；而大部分场景没有文字也完全成立，所以默认给零文字。
- 自助检查：交付前 grep 草稿里的 text 块与引号内的全大写词，无一例外全删（除用户点名）。

## 第 4.5 步：交付前过十二道自检（lint）

写完草稿、编译之前，先跑一遍自检。这一步是**强制**的，不许跳过。

```
python scripts/lint.py <草稿.json> --ref <参考图>
```

`--ref` 可选；给了就能把提示词里的声明与参考图实测值做对照（关 2）。

| 关 | 查什么 | 典型 FAIL |
|---|---|---|
| 1 结构 | 宽高 16 倍数、bbox 在画布内且左上<右下、label 合法、text item 必须带 text、summary.caption 非空 | bbox 越界 / text 缺内容 |
| 2 数值 | 声明的明度档 = 参考主导档？饱和方向 = 实测方向？近白/真黑/亮场位置/柔化程度是否与实测矛盾 | 参考暗部更饱和却写「亮部更艳」 |
| 3 矛盾 | 暗调词与亮调词并存、饱和方向自相矛盾、硬边与 bloom 并存、强触发 tag 组合 | `full body` + 机位词 / `from below` + `foreshortening` / `directly overhead` / 裸 `dutch angle` |
| 4 覆盖 | 明度档、光源出处、衰减、材质反应、空间层次五项有没有写 | 缺「衰减」 |
| 5 禁用 | 质量词、器材/引擎名、版权大词、负面词、cosplay、中文标点 | 出现 `masterpiece` |
| 6 机位 | 俯仰 / 距离 / 倾斜 / 视平线 四要素；平面海报式构图可豁免 | 四项缺两项以上 |
| 7 世界逻辑 | G 组：统一色与唯一色并存、高调无黑锚点、硬光没写边缘、有方向性场景没写朝向、只有人没有证据物、表情没写肌肉、地点与行为不符 | 「全图统一漂白」+「蓝是唯一冷色」 |
| 8 曝光 | 有没有把亮部写成「烧成纯白」（无保色句兜底即 FAIL）；前 80 词有没有明度定调句 | `overexposed to within a hair of pure white` 单独出现 |
| 9 色彩落点 | 色相词够不够；中性色词是不是比色相词多；最亮处有没有颜色 | 大面积写 `pale grey` + 颜色只在红杯套/蓝托盘上 |
| 10 构图落位 | 人物 bbox 中心离画布中线多远（横图 0.33/0.66、竖图 0.30–0.35/0.65–0.70）；0.42–0.58 是禁区 | 人物居中（G65）；横竖同时居中再加一条「正中靶心」 |

退出码 0 = 全过，1 = 有 FAIL。**FAIL 必须改完再交付**；WARN 按情况决定，但要在回复里说明为什么保留。

**否定句不算声明。** `not blown out` / `no ceiling` / `never becomes` / `without haze` 这类反着说的约束句，lint 会跳过（`NEG_BEFORE` 检测 `not|no|never|without|nothing|none of|nor` + 三词内）。
写反制句时不用怕被误报成自相矛盾——这正是 B9–B12 的写法所依赖的。

---

## 第 4.6 步：明度头（关 8 的正解，18 张实测换来的一条）

### 事故记录

2026-11-05 用户一次跑了 18 张，逐张实测（`scripts/probe.py` 量数值）：

| 病 | 张数 | 实测证据 |
|---|---|---|
| **亮部无色** | 15 / 18 | 亮部饱和度 0.014–0.119，暗部 0.092–0.652，比值 0.02–0.44 |
| **整体埋黑** | 5 / 18（全是竖图） | mean 0.250–0.285、dark 39–49%、med 0.153–0.210 |
| **挤在中调** | 3 / 18 | mid 0.771–0.875，几乎没有暗也没有亮 |
| **没有真黑** | 4 / 18 | p1 0.106–0.196，全图无一处真黑 |
| 全部通过 | 1 / 18 | 只有 00512 |

真凶不是缺规则，是**同一个写法用了 43 次**：把「硬光」写成「烧成纯白」。
统计 43 份草稿：`pure white` 13 份、`overexposed` 4 份、`blown to` 2 份、`flat sheet of warm white` 2 份。
模型照做，亮面颜色就没了——照片因此像过曝的手机照，而不是硬光。

### 规则

**明暗是关系，不是数量。** 写 `overexposed` / `pure white` / `near black` 是在给模型一个绝对值，
它会把这个值铺满整片区域；写「比谁亮一档 / 谁没被照到」才是在给关系。

**禁用词**（关 8 会 FAIL）：`overexposed`、`blown out`、`blown to`、`pure white`、`white out`、
`burns out to white`、`within a hair of white`、`flat sheet of white`、`bleached`。
海报/平面（`flat_intent`）豁免——纸白是材料，不是高光。

**替换句**（任选，必须与「亮部保色」同时出现）：
- `the lit side is one step lighter than the shade and keeps every bit of its colour`
- `the light does not wash the colour out of anything it touches`
- `nothing in the picture reaches white and nothing reaches black`

### 明度头模板（放在 summary.caption 最前面，60–80 词）

模型对 summary 前段的注意力最高，明度定调写在中段等于没写。**每条提示词开头都套这一段**，只换方括号里的四个槽位：

```
[VALUE] The picture sits in the [MID / LOW / HIGH] range of the grey scale and never at either end of it:
nothing in it reaches pure white and nothing in it reaches pure black. The light comes from [SIDE] and it is
the only light there is. Whatever it reaches turns one step lighter and keeps every bit of its colour;
whatever it misses keeps its colour and loses only brightness. [SURFACE A] and [SURFACE B] are the two
brightest things in the frame, and both of them are still clearly coloured, not white.
```

槽位填法：
- `[MID/LOW/HIGH]`：与 probe 实测的主导档一致（中调 = mid > 0.5）。
- `[SIDE]`：单一方向，写死（`the left`、`behind her`、`the far end of the room`）。
- `[SURFACE A/B]`：两个**具体**的高光载体（不是「亮部」，是「她脸朝光的那半张」「柜台前缘」）。

### 出图后的数值目标（`scripts/probe.py` 出数，`scripts/verify.py` 判）

| 指标 | 目标 | 含义 |
|---|---|---|
| `mean` | 0.38–0.55 | 中调为主；<0.30 是埋黑，>0.60 是漂白 |
| `nw`（L>0.95） | < 0.03 | 近白成片就是过曝；海报纸白可到 0.35 |
| `dark`（L<0.15） | ≥ 0.08 | 少于 8% 说明「近黑锚点」没落地 |
| `p1` | < 0.10 | >0.10 = 全图没有一处真黑，画面会发灰发飘 |
| `lit / shadow` 饱和度比 | ≥ 0.45 | <0.45 = 亮部褪色，这是最伤气氛的一项 |
| `mid` | < 0.75 | >0.75 = 全图挤在中调，这就是「单调」的数学定义 |
| `soft` | < 0.65，即 `strong` > 0.35 | 两者同时不满足 = 雾化成软光，硬光没落地 |

---

## 第 5 步：出图之后要验（不只是写的时候用）

同一套指标既是**写词前的测量**，也是**出图后的验收**。用户贴回一张"不对"的图时，不要凭感觉猜哪里错，跑对比：

```
python scripts/verify.py <参考图> <出图> --out-dir . --tag 名字
```

输出四块：

1. **逐项对照表**（参考 / 出图 / 差值）：mean、med、dark/mid/bright、nw、p1、p99、sat、lit、shadow、soft、strong、hue、rgb、主色
2. **6×6 明度矩阵三张并排**（参考 | 出图 | 差值）——直接看出"光跑到哪去了"
3. **诊断清单**，按 `[严重]/[明显]/[轻微]/[定位]` 排序，**每条都带"该改哪句话"**
4. **三联对比图** `_verify_<tag>.jpg`（参考 | 出图 | 色差热图，越红差越多）

### 它会替你抓的六类错误

| 判据 | 结论 |
|---|---|
| 主导明度档不同（dark/mid/bright 谁最大） | 气质级错误，先改这句 |
| `lit > shadow` 方向反转 | 亮部/暗部谁更饱和写反了，最伤气氛 |
| `\|Δmean\| > 0.05` | 整体偏亮/偏暗 |
| `\|Δsoft\| > 0.10` | 该糊的硬了，或该硬的糊了 |
| `ref nw < 0.01` 而 `out nw > 0.03` | 出图过曝出纯白 |
| `ref p1 > 0.13` 而 `out p1 < 0.08` | 出图出现真黑 |
| 最亮格行列差 ≥ 2 | 光源位置偏了 |
| 色相差 > 30° | 主色跑偏，回去用单色系钉住 |
| 16×11 色差最大格 | 直接指出"哪一块最不像" |

### 用法上的两条

- **翻车图优先看"最亮区位置"和"明度档主导"**。绝大多数"机位/光不对"的投诉，本质是光落错了格（例：黑翼少女那次参考最亮在右下、出图在左上）。
- **别只看数字**。数字告诉你"哪一块偏了"，但"为什么偏"要回到 B 组（机位写法）和 C 组（光五物质性）去找原因。数字是路标，不是答案。

---

## 参数与文件约定

- 采样：CFG 3.0（带颗粒 3.1）/ Steps 50 / Shift 5.0 / Euler + sgm_uniform / SLG 跳第 22 层。
- 分辨率：总像素 1–2M，宽高必须是 **16 的正整数倍**。横 1536×1024、竖 1024×1536、方 1024×1024、宽银幕 1536×640。
- 文件四件套：`moss-prompts/NN-英文名.json`（草稿）+ `.txt`（编译产物）+ `NN-notes.json`（中文参考）+ `NN-英文名-canvas.html`（画布预览）。
- 交付前顺序**固定**：`preview.py` 预览 → 调 y → `lint.py` → `compile_prompt.py`。顺序换了就会返工。
- 默认零文字、零质量词、零画师串、只给正向；默认叠加颗粒层（见 `references/entry.md`）。

---

## 规则实录在哪

G21–G98 的实测证据、翻车现象、正解句式全部在 **`references/casebook.md`**。
G1–G20、G24–G26、G65、G83 的正文小节就在本文档里。
本文只留流程、A–G 核心组、以及末尾那张索引表。

> 本文约 1000 行是「字典」不是「教程」。第一次写请从 `references/entry.md` 填空开始，
> 卡住了用 `references/symptoms.md` 按症状查，需要某条规则的判据再按索引跳 casebook。


---

## 规则索引（G1–G98）

编号按实测时间排，**不是逻辑顺序**——用这张表跳，不要顺着读。
带「补」「补二」「补三」的行是同一编号下的追加条款，紧跟在主条后面。
标题就是规则的一句话版本；要判据与实测数值，去右列那个文件。

| 编号 | 一句话规则 | 详见 |
|---|---|---|
| G1 | 先过一遍常识，再动笔 | 本文正文 |
| G2 | 先写故事，再从故事里挑那一瞬间（一张图只讲一件事） | 本文正文 |
| G3 | 补：模型的默认脸是微笑，「没有表情」不能靠否定词写（45 号实测，m03083） | 本文正文 |
| G4 | 高调必须有黑锚点 | 本文正文 |
| G5 | 「统一」与「唯一」不能并存 | 本文正文 |
| G6 | 硬光写边缘，不只写长短 | 本文正文 |
| G7 | 饱和度低不等于"高级"，先看它是不是事故 | 本文正文 |
| G8 | 人物永远会自动撑满画面——必须给比例尺 | 本文正文 |
| G9 | 颜色必须落在被照亮的大面积上，否则图一定发灰 | 本文正文 |
| G10 | 全图只允许一个视点，每一句都要服从它 | 本文正文 |
| G11 | 灯不要画进画面，写「光从哪来、打到哪、哪没打到」 | 本文正文 |
| G12 | 补：人物的姿态和道具的支撑不能互相矛盾（47 号实测，m03177） | 本文正文 |
| G13 | 注意力预算：不写毫米级的细枝末节（51 号实测，m03494） | 本文正文 |
| G14 | 名画融合：点名作品 > 描述结构（64 号 v4 实测通过，m04292 用户判「这回还原了」） | 本文正文 |
| G15 | 倒影与镜像：只说「这是倒影」不算数，要有只能倒置的证据（77 号实测，m04697） | 本文正文 |
| G16 | 介质照明的第二件：擦痕必须和她手上的湿痕连在一起（79 号实测通过，m04789） | 本文正文 |
| G17 | 独立小道具必须自己「站在一个面上」，否则会被就近吸附（80 号实测） | 本文正文 |
| G18 | 双人图：四只手要逐只点名，身高差要用画面坐标写（81 号实测失败） | 本文正文 |
| G19 | 光环、发光件与小道具的尺度三分钟（81 号实测） | 本文正文 |
| G20 | 每一处光照都要能在 bbox 几何上兑现（83 号实测，2026-11-06） | 本文正文 |
| G21 | 人物尺寸的实测偏差：写多少它画多大，但 bbox 会被放大（86 号实测，2026-11-06） | casebook.md |
| G22 | 要背影/侧背，一个 face 都不要提（86 号实测） | casebook.md |
| G23 | 大气透视是往亮里退，不是往灰里退（86 号实测） | casebook.md |
| G24 | 构图：前景道具抢主体、bbox 偏了人物还是居中（89 号实测，2026-11-06） | 本文正文 |
| G25 | 修订 + G26 无人图的尺度锚（91/92 实测，2026-11-06） | 本文正文 |
| G26 | 无人物的空景也要尺度锚：给真实厘米数 + 一件公认尺寸的相对物（91/92 实测；无独立标题，寄生在「G25 修订」节内） | 本文正文 |
| G27 | 水面反光 ≠ 天光柱；否定句管不住「场景必然后果」（95 号实测） | casebook.md |
| G28 | 命名即放大：凡是被叫出名字的工业制品，都会长到主体尺寸（96 号实测） | casebook.md |
| G29 | 角色锁定块换一致性，代价是尺寸必然放大（97A/97B 实测） | casebook.md |
| G30 | 纸/留白不是一个物体，模型没有「不画」的概念（98 号 riso 实测） | casebook.md |
| G31 | 亚像素纹理写不出来：网点、错版、颗粒、反光点（98 号 / 89 号同源；113 号二次确认 → 印刷网点族判死） | casebook.md |
| G32 | 只能有一个最亮，而且不能「先写 A 比 B 亮，再写 B 其实最亮」（99 号实测） | casebook.md |
| G33 | 出稿前先定「y 梯子」，再放东西（100 号实测 + preview.py 上线） | casebook.md |
| G34 | 「移动的某物」必须写成「它留下的痕迹」，否则画出整只东西（101 号实测） | casebook.md |
| G35 | 长曝光里的水面，写「没有波纹」一定失败——要写波纹被压成了什么形状（101 号实测） | casebook.md |
| G36 | 「层」必须满幅，并且要在主体块里重写一遍（102 v1 事故） | casebook.md |
| G37 | 有 bbox 就别再写厘米数；表情只写看得见的（102 v3，用户 m05852 定） | casebook.md |
| G38 | 思考别写进提示词（103 号，用户 m05898 定） | casebook.md |
| G39 | 强光源写「数值化克制」（103 号出图 nw .0592 得出） | casebook.md |
| G40 | 「只画到腰」= 亲口允许她悬空（110 号实测，最刺眼的一处错） | casebook.md |
| G41 | 光源不许给名词：写了 tube / lamp，它就把灯画进画面（G11 加强，110 号重犯） | casebook.md |
| G42 | 夜街、路面、水面自带画线：写「毫无细节」一定失败，要写成什么样的线（110 号 + G28 补） | casebook.md |
| G43 | 写 `Mid tone overall` 会把整张图压进中调：必须同时给「暗部面积」和「亮部色相」（110 v2 实测） | casebook.md |
| G44 | 写「里面什么都没有」会失败：要写「里面是什么颜色的东西」（111 号实测） | casebook.md |
| G45 | 画布基底不能作为 item：写「The paper itself」会被场景化成画面里的一堵墙（113 号实测） | casebook.md |
| G46 | 尺寸标定：bbox 管形状与位置，「距离 + 公认尺」管大小；同时给「离镜头多远 + 场景公认尺」时，1/3 的下限可被压到 25–28%（115 号三张实测，2026-11-07） | casebook.md |
| G47 | 物体的尺寸几乎完全由「名字先验」决定，bbox 只管位置不管大小（116 号实测，2026-11-07） | casebook.md |
| G48 | 标尺物必须和主体在同一个深度平面上；嵌进构图槽位的人物会被构图吞掉 bbox（117 号实测，2026-11-07） | casebook.md |
| G49 | 不要在别的 item 里提到人物，否则人物会被并进那一块、整块消失（117v2 实测，2026-11-07） | casebook.md |
| G50 | 官方口径：普通场景用 caption，Layout 只留给「必须精确」的东西（2026-11-07 查官方仓库后定） | casebook.md |
| G51 | 人物必须给「画内定位三句」，缺一句人物就消失（117v2/v3/v4 三连实测，2026-11-07） | casebook.md |
| G52 | 暗背景前的主体必须比背景亮一档，否则被背景吸收（117v4 实测，2026-11-07） | casebook.md |
| G53 | 不许用数值断言「画面里有没有某物」（117v4 判读事故，2026-11-07） | casebook.md |
| G54 | bbox 会被「头顶对齐同深度物体的哪条边」压住，不再按 1.5 倍放大（119 号实测，2026-11-07） | casebook.md |
| G55 | 漏光、光晕、眩光这类「没有物体的东西」必须逐项否认它是物体（121 号实测，2026-11-07） | casebook.md |
| G56 | 当标尺的物体，它的 bbox 必须和它所在的深度自洽（122 号实测，2026-11-07） | casebook.md |
| G57 | 画面的「地面强度」决定人物能被压多小（122 号两版实测，2026-11-07） | casebook.md |
| G58 | 光环必须逐项否认「辐条 / 射线 / 断弧」，只说「无内圈无同心弧」压不住（126、127 两次实测，2026-11-07） | casebook.md |
| G59 | 侧向朝向在「坐着的人」身上仍然失效，必须用「看不见哪只眼」的否定句（126 实测，2026-11-07） | casebook.md |
| G60 | 带印刷的道具会自己长出文字，要么换成无字材质，要么就当文字图设计（126 实测，2026-11-07） | casebook.md |
| G61 | 光环画不对不是写法的错，是角色名自带的官方设计（126、127 第三次实测，2026-11-07） | casebook.md |
| G62 | 明度的上限写在 summary 就压住全图，改 character 块无效（127v2 实测，2026-11-07） | casebook.md |
| G63 | 给「一群人」名词组，模型会先把人排好再上色；要无脸就写「背对我们」（129 号实测，2026-11-07） | casebook.md |
| G64 | 提示词太长，本身就会把人物画大（用户判断，2026-11-08；131 号做对照实验） | casebook.md |
| G65 | 人物默认不居中——这是默认值，不是可选项（用户 m04130 / m09552 定，2026-11-08） | 本文正文 |
| G66 | 角色不带光环就不要写光环；角色自带的部件先查设定再落笔（用户 2026-11-08 指出） | casebook.md |
| G67 | 细小的东西不给 bbox，只写进它所在那块的 caption（用户 2026-11-08 指出） | casebook.md |
| G68 | 剪影图不要写「几成近黑」，要写「天空占多少」+「暗部里多少真的到黑」；暗部极饱和是正解，写「最饱和的是那块暗的天」 | casebook.md |
| G69 | low key 图里「亮」等于中灰，必须点名一处「到白前一步」的锚并给比例；p99 < 0.70 等于没有高光锚 | casebook.md |
| G70 | 无人静物：影子会画但画成软浅影，要写「硬边、无半影、木质掉两档」；「暖蜜色木」=高饱和橙红会抢掉唯一饱和色；纹理越细尺度越读成特写 | casebook.md |
| G71 | 「cut like a blade」治不了投影：影子要写「边缘在哪突然停」+绝对明度对照（影内是画面最暗，比墙之亮更暗）+影子形状对得上投射物 | casebook.md |
| G72 | 删纹理不能删到零：「no visible grain」会变成无质感平板、sat 掉一半；正解是把纹理尺度改大（手宽的大片而非细线）+给饱和下限 | casebook.md |
| G73 | 参照物自己也会被放大成英雄道具（茶杯 11%→25%）；选结构构件（踢脚线/地砖格/桌沿厚度）做尺子，不选能单独成物的东西 | casebook.md |
| G74 | 满幅大面积块的明度要写在它自己的 caption 里，summary 的 Mid tone 只是总闸门；`tan` 就是浅色，要暗得明说 | casebook.md |
| G75 | 纹理先验绑在名词上：写 grain 就是细平行线，形容词改不动；换尺度要换名词（改成板条拼接） | casebook.md |
| G76 | 结构构件当尺子必须带可数重复单元（一排等距的钉头/三条等宽板），「一条边的粗细」不可数 | casebook.md |
| G77 | 正俯视配方三件：画框四边全交给地面 + 否认地平线/墙/天花板 + 光只以「地上的亮平行四边形」出现；人物沿对角线躺 | casebook.md |
| G78 | 布边/饰条类名词自带宽度先验，写「细」改不动；改写成「缝」或给指尖宽的可比物；细黑线当黑锚与 sat 下限冲突，要让受光大面本身带色 | casebook.md |
| G79 | 当尺子的物体必须自己拥有 bbox（167 号写「比一张席短」但席无独立 item → 1.22×/1.69×） | casebook.md |
| G80 | 地面光斑默认来自带窗棂的窗，会画成一格格分离矩形；必须显式否认窗棂、第二块光斑、任何网格 | casebook.md |
| G81 | 「不超过拇指宽」这类身体部位比对物对水花/烟/雾无效；改用画面内已有物的尺寸、或「数量+同尺寸」 | casebook.md |
| G82 | 每条交付第一行必须写「建议尺寸：W×H 横/竖图」；JSON 里的 width/height 不能替代这句话 | casebook.md |
| G83 | 可坐物比姿势词强势：画面里只要有台子/箱子/台阶沿，人就会被放上去坐或靠；要么删掉它，要么逐项否认（`this is only a step, too low to sit on`）——这是 B11 的独立编号版 | 本文正文 |
| G84 | 大面积水面自带俯视先验，写「低机位贴水」会被翻成俯拍；把水面压成高度不到 1/3 的横带，或把机位锚在「倒影的立面」上 | casebook.md |
| G84 补三 | 全幅路面要掠射，画框顶部必须有「被切掉的远处结构」（3–5% 高的一条暗边），整面墙会翻成俯视 | casebook.md |
| G84 补二 | 掠射机位必须有一条会汇聚的线；写成「平行于底边」＝取消透视，整张变正对平面。远处变暗给纵深，不用立面 | casebook.md |
| G84 补 | 低机位水面图不要写建筑/马路牙/台阶——任何「立着的立面」都会把机位拉高；不写 kerb 这个词就不会触发 lint 关 7 | casebook.md |
| G85 | 景别不是靠形容词，是靠两个数：机位距离 + 主体占画面高的分数；两者同时给且必须写余量句，否则必裁头（由 120 号特写与 115 号标定推出） | 本文正文 |
| G86 | 极低 key 有下限：dark >0.70 变成「黑屏里一束光」；要写「暗部里有多少不是纯黑」，目标 0.42–0.65 | casebook.md |
| G86 补 | dark 百分比不是判据，暗部里「有几层可辨识结构 + 值域有没有被拉开」才是；只写「暗部占几成」会画出平黑 | casebook.md |
| G87 | 倒影必须被水面事件打断（涟漪穿过时抖、边缘是撕开的、水花站在它前面），否则读成躺在水上的实物 | casebook.md |
| G88 | 「湿柏油」写 greenish 会勾来植物绿；改写成 `a desaturated blue black with no green in it at all` | casebook.md |
| G89 | 水面涟漪要疏密不均，全铺满会读成装饰图案；写「聚集在近半、中间留出光水面」+ `Nothing about the pattern is even` | casebook.md |
| G90 | 说「招牌」就会画字，`nothing reads as a letter` 拦不住；要零文字就先别叫它招牌，写成「只有光」 | casebook.md |
| G91 | 玻璃的透射层与反射层各占一块 item（透射满幅、反射只占上部横带），必须写「两层相加永不到白」；倒影写 soft/thin/half looked through | casebook.md |
| G92 | 逆光图里暖色不能落在逆光勾出的轮廓上（会是冷白）；必须落在「被主光正面照到的那块地上」，只写一处并写死面积 | casebook.md |
| G93 | 背人：被背者 bbox 上边要比背者高一个头（≥画高 6%），并写「头垂过哪侧肩、垂到哪」；两者都写「看不见哪半边脸」 | casebook.md |
| G94 | 彩色印刷题材（三色错位/riso）本身没有暗：必须加一版「只印阴影」的副墨并写死暗值，否则 dark<.05、p1>.13 | casebook.md |
| G95 | 人物 bbox 必须包住头顶到脚，且不许与她站立的地面/台面 bbox 交叠（交叠会让人物被旋转塞进去） | casebook.md |
| G96 | 介质指令（平色/无描边/无渐变）会被人物先验碾压：必须把人物本身也写进介质语言（脸=色块边界、眼=深色横带、发=单一平色块） | casebook.md |
| G97 | 像素画判死：「细小且全局统一的重复单元」（halftone/pixel/dither）画不出来，与 113 网点同族；soft>.9 且 strong<.01 即介质未生效 | casebook.md |
| G98 | 线稿成立：`no filled area` + 明暗全由排线疏密产生；高光锚写在纸白上（`within one step of the bare buff of the sheet`） | casebook.md |
