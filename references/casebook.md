# 规则实录 G21–G98（casebook）

> 这里是**证据层**：每条规则当时的实测数值、翻车现象、正解句式。
>
> **G21–G98** 的主条在本文件里，按编号顺序往下翻。
> **G1–G20、G24–G26、G65、G83、G85** 的正文小节在 `references/moss-rules.md`（同一份文件里的
> 「世界逻辑与故事」「尺寸四把尺」等节），本文件只保留它们的实测痕迹。

> 编号不连续是历史原因（按实测时间编号）。同一编号出现多次＝同一机制后来的补充实测。

### G21 人物尺寸的实测偏差：写多少它画多大，但 bbox 会被放大（86 号实测，2026-11-06）

86 号写 `she is two fifths of the height of the picture`、character bbox 高度 430px（42%），出图实测她占据画面 90–870px ＝ **76% 高，比 bbox 放大约 1.8 倍**。

三条对策：
1. **人一多、场景元素一挤，模型就以「完整入画」为优先，比例退到第二**。要小人物，就得同时给三样：分数（`one twelfth of the height of the picture`）+ 一个**尺寸对照**（`her whole body is shorter than the width of one of these footprints`）+ 一个**否定**（`she is a small figure in a large empty place, and the snow around her is much more of the picture than she is`）。
2. **bbox 要给得比目标再小一档**（目标 2/5 就给 1/4，目标 1/12 就给 1/16）。
3. **不要用「某物到她腰」来标定她身高**。86 号写了 `the railing comes to her hip`，栏杆的 bbox 与她的 bbox 互相拉扯，最后两边都放大。要标定就用**远景里的东西**（船、桩、山），别用紧贴她的道具。

### G22 要背影/侧背，一个 face 都不要提（86 号实测）

86 号写 `three-quarter view from behind: we see the back of her left shoulder, the left side of her jaw, and the left edge of her cheek`，出图是**正脸略微朝左**。只要句子里出现 `face` / `jaw` / `cheek` / `eyes`，模型就转向正面。

正解：用**体积**说背面，整段不提脸。
- `we are looking at her back: the shoulder blades of her coat and the upturned collar are what fills the space between us and her, and her head is a dark shape on top of that collar`
- 要看侧脸就另起一句、并且写清「只有这些，没有更多」：`only the edge of her jaw is visible past the collar, and there is no eye, no nose and no mouth in the picture at all`
- 想让她转向，用**她身体朝哪 + 头偏多少度**，不用「view」这种词。

### G23 大气透视是往亮里退，不是往灰里退（86 号实测）

86 号写了 `every eight metres back costs one step of contrast`，只写了对比衰减，没写亮度抬升。出图 `mid 0.926`——**92.6% 的像素挤在中调**，远处没有变亮，整张图平了。

正解：雾/霾的每一层都要**同时**降对比、**升亮度**、**丢色相**：
`the railing is dark and sharp; eight metres back the bollard is lighter by one step and flatter; eighteen metres back the boat is lighter again and has lost its colour; and at thirty metres everything is the same pale value as the sky and has no colour at all.`

自查一句话：把远处那一层单独看，它**是不是比近处更亮**。如果只是「更淡」，实测会变成一片中灰。
### G21 补充：MOSS 有人物最小尺寸，低于它就一定被放大（87 号实测）

87 号写 `she is one twelfth of the height of the picture`、bbox 高度 94px（9%），出图实测她 **45% 高**——放大 3.6 倍。加上 86 号的 1.8 倍，两次实测说明：**只要写了角色名 + 服装 + 姿态，模型就按"主体"来排版，比例句几乎无效。**

实测阈值（暂定）：**人物要小到 1/6 以下就会被拉回 1/3–1/2**。三个可用做法：
1. **要人物在 1/6 到 1/4 之间**：可以写，但 bbox 给 1/8，并且不写"某物到她腰"。
2. **要"人在大景里极小"**：放弃角色细节——不写名字、不写服装、不写姿态，只写 `a single small figure in a red coat, too far away to have a face, no bigger than a thumbnail in the frame, and nothing about her can be made out except the colour of her coat`。painted 成"一个红点"。
3. **最稳的做法是不画人**：画空景 + 人的痕迹（脚印、晾着的衣服、没关的灯、留下的杯子）。87 号的脚印串就是这个思路，成立。


**G26 实测成立（93 号，2026-11-06，用户 m05169「这次差不多」）**：在画面里放一瓶 20cm 矿泉水并逐件换算后，鞋立刻缩到比瓶短、脚印变成浅印、伞读成小折叠伞。所以「无人图的尺度问题」的解法是：**放一件人尽皆知尺寸的小物 + 给每件道具真实厘米数 + 逐件换算**，三者缺一不可。瓶子的位置要选在道具群中间、离镜头不远（放在画面最深处会失去参照作用）。

**G26 补：无定形物的厘米数无效（94 号实测，2026-11-06）**。94 号写水洼「三十厘米宽」，出图它占了画面宽度的四分之一（约两米三），放大八倍；同一张图里斑马线（45cm）和井盖（60cm）却都准。原因：斑马线和井盖有硬边、有固定形状，水洼是**无定形物**，厘米数对它不生效——它只听 bbox。规则：水洼、雾、烟、影、泼溅这类无定形物，尺寸只能用 bbox 控制，或写「不比某件已知物大」。

**方形画幅 + 正俯视成立（94 号，用户 m05185「我觉得还行」）**：方图配十字结构（南北一条、东西一条、四条斑马线两两成直角）效果最好；正俯视要让「斑马线的边平行于画框、完全没有透视收敛」写进画面事实，只写 `directly above` 会被画成斜俯拍。breaking symmetry 要写成四件具体的、分属不同象限的小事，否则方图会退化成图案。

### G27 水面反光 ≠ 天光柱；否定句管不住「场景必然后果」（95 号实测）

95 号（黑白泳池）用户 m05204「还不错」，但三条承诺没兑现，全是写法问题：

1. **「水面上一道灯影」被画成从天而降的体积光柱**。我写 `the reflection of a lamp above and behind us` + `a long smear of light on the water`，模型把两者合成了一束天花板射下来的光。正解：反射只写**水面上的那条横带本身**——`one long band lying flat on the water, running parallel to the top and bottom edges of the frame, found nowhere above the waterline`，并补一句 `there is no beam of light coming down from the ceiling and no shaft of light in the air`。
2. **`no ripple drawn on it, no splash` 无效**。头部浮在水面 → 同心涟漪是场景必然后果，模型一定补。否定句只能管住**措辞**，管不住**物理**。正解：主动写形状——`three rings spread out from her chin, wider and flatter the further they go, and they die out within two metres of her`。
3. **「镜头前的水近黑」被画成画面下缘的一道黑边**。一片没有形状的暗，模型会把它排成边框（等于给图加了 border，即便我明写 no border）。正解：近黑端要落在**有形状的物体**上（池底排水口、暗色瓷砖带、她脑后那片湿发），不要用「镜头前的水」这种无定形区域承载最暗端。

数值印证：dark 只有 .098、p1 .114（承诺的三处近黑全没出现）、mid .819（两端被冲淡挤进中调）、p99 .992（天花板光柱成为最亮）。

**通用条款**：凡是「场景自带的必然后果」（水面必有涟漪、有光必有影、雪上必有落痕、玻璃必有反光），只能写成它**是什么形状**，写成「没有」一定失败。

### G28 命名即放大：凡是被叫出名字的工业制品，都会长到主体尺寸（96 号实测）

96 号（2.4:1 沙漠公路）用户 m05230「我觉得还行」，四条承诺里有两条没兑现，都是同一类问题：

- **车放大 2.6 倍**：我写 `one car, its width about a fortieth of the frame`，实测红点簇跨 100px / 1536 = 6.5%（1/15），车身高度 70px = 11% 画面高。同一张图里那根 2.5 米导标桩反而画准了（1/12 高）。
- **结论**：尺寸误差不来自「有没有尺子」，而来自**有没有名字**。「车」是一个有几万个先验的形状（车窗、车牌、后视镜、轮胎），模型会把它画成一辆完整的车，完整就需要面积；而「导标桩」先验很少，所以能保持小。
- **正解**：要它小，就别叫它名字，只写它在画面上是什么——`two small red points at the end of the road, and behind them one shape a little darker than the road, with no window, no wheel and no plate in it`。名字一旦出现，比例句与 bbox 都会失效。

**另一半：场景自带先验只能「纳入设计」，不能否认（96 号同批实测）**：

- 我写 `no painted line on it anywhere`，出图公路两侧有两条干净的白边线。
- 我写 `no detail in the hills at all`，出图山脊里全是沟壑与岩层。
- 规律：**公路必有画线、远山必有沟壑、水面必有涟漪、玻璃必有反光**——这四类否认句的成功率接近于零。
- 正解只有两条路：① **纳入设计**——承认它存在，然后指定它的样子（`two white edge lines, unbroken, running to the vanishing point`：它从失控细节变成构图线）；② **换掉物体类别**——不画柏油路画砂石路、不画远山画树线、不画水面画湿沙。

### G29 角色锁定块换一致性，代价是尺寸必然放大（97A/97B 实测）

97 号是一对（同一角色、同一地点、同一机位、只换时间，见 `moss-prompts/97a-roof-dawn.json` 与 `97b-roof-midnight.json`）。用户 m05259「我觉得还行」。

**成立的部分（这是可封装的机制）**：把外观写成一段**逐字相同**的 `[CHARACTER LOCK]`（发色长度 + 刘海 + 光环三句定形 + 大衣颜色/长度/袖口 + 衬衫 + 裙 + 鞋 + 包）放进两张图的 character caption，出图两张**确实是同一个人**：发色、刘海横线、光环细空心圈带十字、大衣黄、藏青百褶裙、深棕系带鞋、帆布包位置全部一致。
- 附带印证：我写「包在左肩」，两张都画在右肩——**成组一致地放错＝惯例，不算错误**（同一角色不同图放反才叫错）。

**代价（必须写进封装说明）**：LOCK 块越详细，人物越被当成立绘。
- A 写「她占画面高三分之一」，实测 **93%**（头顶 y≈40 到鞋底 y≈990）；
- B 写「坐姿占三分之一」，实测 **55%**。
- 结论：**角色锁定块与「小人物」互斥**。要跨图一致就得接受人物占 1/2 以上；要小人物就不能用 LOCK，改用 86/87 号那条路（只写小点/痕迹/不画人）。

**另外两条数值事故（97A/97B 同批）**：
1. A 承诺「最暗＝罐子投在水泥上的长影」，实测 `dark .026`、`p1 .109`——影几乎不存在。原因：我同时写了「整张图高调、冷、upper middle」+ 大面积浅灰水泥 + 浅绿白天光，模型把地面也一并提亮，我那条「影只覆盖三分之一」被淹没。**高调图要留暗部，暗部必须写成「占多大面积」而不是「有一个影」**：`the shadow covers rather less than a third of the platform` → 改成 `the shadow covers two of the three slabs, and it is the darkest thing in the frame by five steps`。
2. B 承诺「almost all of it is near black」，实测 `dark .759`——过暗，中间调只剩 19.8%，人物和罐壁糊在一起。**低长调图的暗部上限约 60–65%**，写 `almost all` 会一路压到 76%。要写 `about two thirds of the frame is dark and the remaining third carries the light`。

### G29 补：LOCK 在场时，人物的比例句一律失效，bbox 也会被超画 1.2–1.4 倍（114 三张实测）

114 是一组三张序列（同一角色、同一套衣服、同一天三个时段，`114a-sequence-classroom-dawn` / `114b-sequence-rooftop-dusk` / `114c-sequence-store-night`，均在 `moss-prompts/`）。**身份一致性成立**：黑短波波头长度、齐眉刘海横线、呆毛存在、细框圆眼镜、黑瞳、白水手服红领巾、藏青百褶裙、白过膝袜、黑皮鞋、深棕书包，三张全部一致。这是 LOCK 机制第二次独立验证（97 号是一对，114 是三张）。

**但比例句全线阵亡，三张实测**：

| 图 | 写的比例 | bbox 高 | 出图实测 |
|---|---|---|---|
| 114a | three fifths（60%） | 62% | **约 75%** |
| 114b | two fifths（40%） | 53% | **约 69%** |
| 114c | two fifths（40%） | 53% | **约 76%** |

1. **LOCK 在场时，`about two fifths of the frame height` 这类比例句可以删掉**——写了也白写，模型一律按立绘体量画（G29 主条已记 97A 写 1/3 出 93%）。省下来的字数给别处。
2. **bbox 也压不住**：给 53% 画出 69–76%，超画约 **1.2–1.4 倍**。要人物真的小，只能**不用 LOCK**（走 86/87 那条「只画小点/痕迹/不画人」的路），没有第三种办法。
3. **书包肩带**：我写 `hangs from her left shoulder`，三张**全部画在右肩**。按 G29 主条「成组一致地放错＝惯例」，这不算错；但下次要么直接把 LOCK 改成 right（顺从惯例，最省事），要么写死 `the strap runs over her LEFT shoulder and the bag hangs at her left hip` 并接受它可能还是反。
4. **朝向三句在「人物占画幅过半」时会输给正面站姿先验**：114a 写「她面朝窗、我们只看见远颊和眼镜边」，出图是**几乎正脸看向我们**（B、C 两张的朝向都对）。规律：朝向三句在**中远景/小人物**时稳，在**近景大立绘**时容易退化成「站着看镜头」。近景要侧脸，就得把「我们看见的是哪一侧、看不见哪只眼」写成否定句，光写「她面朝窗」不够。
5. 另记：三张里只有 114c 的裙下多出一条棕色内衬褶（LOCK 未写内衬，模型自由发挥）；不影响身份判定，但说明 **LOCK 只锁到「写了的那几件」，没写的部件会各自长**。

### G29 补二：LOCK 在场时人物比写的比例大 1.2–1.5 倍，比例句基本失效（114 三张实测，2026-11-07）

114 三张（同一 LOCK、同一套衣服、三个时段）出图实测，**身份一致性成立**——波波头长度、齐眉刘海、呆毛、细框圆眼镜、黑瞳、白水手服红领巾、藏青百褶裙、白过膝袜、黑皮鞋、深棕书包，三张全部对得上。LOCK 机制第二次验证成功（97 号一对 → 114 三张）。

但**比例句全线失效**，三张都画大了：

| 图 | 写的比例 | 实测占画高 | 倍数 |
|---|---|---|---|
| 114a 教室 | 五分之三（60%） | 约 70% | 1.17× |
| 114b 天台 | 五分之二（40%） | 约 58% | 1.45× |
| 114c 便利店 | 五分之二（40%） | 约 70% | 1.75× |

1. **LOCK 在场时，想要多大就写「目标尺寸 ÷ 1.4」**；写 40% 会出 58–70%。这条与 G21（有人就至少 1/3）叠加，实际下限更高。
2. **朝向三句在 LOCK 场景里也会被稀释**：114a 写「她面朝窗、侧身四分之一背离我们、只看见远颊」，出图是**正面偏四分之一朝我们**——脸转向镜头了。要她真的背离，得把「看不见她的哪只眼/哪半边脸」写成否定句，而不是只写「她面朝窗」。
3. **一致性的副产品**：三张都在藏青百褶裙下多出一层棕黄褶边（LOCK 里没写这一层）。因为**三张一致**，按「成组一致地放错＝惯例」不算错——这再次说明 LOCK 场景里**跨图一致性比单图准确性更值钱**。
4. 数值：114a mean .492 / nw .0264 / **lit .121 < shadow .201（方向反转，高调冷光场景的通病）**；114b mean .503 / nw .0029 / lit .178 > shadow .146（唯一方向正确的一张）；114c mean .406 / mid .750（**顶到 .75 上限**）/ dark .155。夜景那张偏亮一档，是「窗光写成满幅大白」的代价。

### G30 纸/留白不是一个物体，模型没有「不画」的概念（98 号 riso 实测）

98 号（`moss-prompts/98-riso-rain-window-cat.json`，riso 双套色，1024×1536）三档明度写得很清楚：纸的奶油色=最亮、靛蓝=最暗、荧光橙=唯一暖色只准两处。出图实测 `bright .004`、`p99 .730`、`dark .479`。

**成立的两件事**：① **色数纪律落地了**——橙色真的只出现在两处（窗框左侧一条竖带 + 窗台一片），其余全是靛蓝；② 硬边平涂、无渐变、猫偏右不居中、窗框十字结构全部到位。

**失败的一件（关键）**：**整张「纸」被染成了靛蓝**。我把「未印刷的奶油纸占左上四分之一」写成了一个 bbox `[-768,-512,-148,48]` 的 item，出图那一块是深蓝，纸从来没有出现。
- 真因：**paper 不是物体**。模型对「这一块什么都不画」没有概念——bbox 里必须画点东西，它就按 summary 的主色填了进去。
- 正解只有两条：① 把纸写成**被某物占据的反面**（`the cream is only ever seen as the sliver of untouched paper between two passes of ink`），让它的形状由别的东西界定；② 或者干脆承认背景必须有色，改成「浅色底」并给底色指定一个明确的浅色名（`the ground is not white paper, it is pale celadon, and it is the lightest tone in the picture`）——给它一个颜色，而不是给它「什么都没有」。

### G31 亚像素纹理写不出来：网点、错版、颗粒、反光点（98 号 / 89 号同源；113 号二次确认 → 印刷网点族判死）

98 号 riso 写 65 lpi 网点全灭；113 号 halftone 把点写到最粗（`each dot is a distinct round speck, rows of them running at one angle across every tone`）+ 纸满幅 + 「点相触成中调、点稀疏成高调」逐档写明，**出图仍是平滑绘画，零网点**，整体退化成柔和的水彩风旧插画。两次独立失败，结论升级：**印刷网点族（halftone / riso 网点 / 报纸网点 / 错版）在 MOSS 上不可实现，配方表移除**。

98 号还想要三种印刷语汇，一个都没出现，出图是平滑的平涂插画（`soft .620`、`strong .063`）：
- **65 lpi 网点**：1024px 宽的画面上一行约 15 像素，模型不会画，直接给平涂。
- **两版错位 2mm**：2 像素级的月牙露纸，同上。
- **纸纹透出来**：亚像素级颗粒。

89 号当年要的「瞳孔里成对的红色反光点」也是同一类失败。**结论：小于约 1/100 画面宽的细节，写在 caption 里一律不生效。** 想要质感，只有两条路：
1. **给它一个自己的 bbox（局部放大）**——把「网点」写成画面里的一块 60×60 像素的放大区域，它会画；但这就变成「画中画的印刷样本」，是另一张图。
2. **换成可见尺寸的对应物**——木刻用刀痕（88 号成立，因为刀痕是 3–5px 的**线条**且方向统一）、胶片用颗粒（要写 `grain you can count`）、报纸用半调大点到 8–10px。**质感必须是「可数的单元」，不能是「均匀的场」。**

### 不够显式否认的「不要第二件东西」= 一定出现（98 号）

98 号写了 `There is nothing else on it: no pot, no book, no cup, no cloth, and no second object of any kind`，出图上窗台仍然多出一个橙褐色小物件（贴着猫尾巴）。同 95 号、88 号的旧账。要空，就必须**把台面本身写成空的理由**（`the sill is empty because the shop closed and everything was taken in`），而不是列举不要什么。

### G32 只能有一个最亮，而且不能「先写 A 比 B 亮，再写 B 其实最亮」（99 号实测）

99 号（单色绿调旧书店）整体成立：`rgb 0.172/0.231/0.153` 绿占绝对主导、`sat 0.376`、灯锥一米内收住、远处走道退黑、书脊全部不可读、椅子+外套+捆书+梯凳四件证据物全在。

但有两处自负盈亏的错：
1. **焦点被灯罩抢走**（`p99 .920`）。台灯 item 里我写了 `the glass glows a green that is brighter than the paper under it`，书页 item 里又写 `its two pages are the brightest thing in the whole picture, brighter than the lamp glass`。**两句互相矛盾**，模型选了先出现、更具体、更靠近光源的那句，于是绿玻璃罩成了全图最亮最饱和的一块。
   - 规则：**亮度排序全文只能声明一次，单向。** 不要先给 A 一个「比 B 亮」的具体句，再在 B 的块里宣布「B 才是最亮」。正确的是先定 B 为最亮，然后所有别的物体只写「比它暗几档」，不再出现任何「比 X 亮」的句子。
2. **台灯比书和椅子都大**。我写「四十厘米高」，但 bbox 给了 `[600,840,900,1120]`＝300×280px（画幅宽的 29%）——**模型听 bbox 不听厘米数**。道具的 bbox 宽度不得超过主体，工业制品（台灯/椅子/桌/车）先验极强，bbox 一大就必然按实物尺寸放大成前景。
   - 规则：写尺寸的物体，bbox 必须与那句尺寸自洽：40cm 的东西在 1536 高的画里、离镜头两米，bbox 高不过 200px。

### 单色处理的三个条件（99 号成立的部分）

1. **单色要有物理理由且在画面里**（绿玻璃灯罩是唯一光源 → 照到哪染到哪），不能是「加了个滤镜」。
2. **单色靠明度分档**：近黑墨绿 / 中瓶中绿 / 浅薄荷，三档同一色相，不许偷偷给木头加棕、给书脊加红。
3. **最亮的东西要小**：灯下书页只有一巴掌大，图才暗得下去。最亮面积一放大，整张图就被提亮成灰。

### G33 出稿前先定「y 梯子」，再放东西（100 号实测 + preview.py 上线）

100 号（对称站台，`moss-prompts/100-symmetric-platform.json`）构图成立：镜像对称、左右柱列收敛到轴上同一灭点、湿地面倒影光带从尽头淌到脚下、单支冷灰绿 + 一点深红。实测 mean .250 / dark .314 / p99 .968。

但 bbox 有两处系统性偏低：**长凳给到 y=980（64%），实际该在 55%**；**远端灭点给到 31%，实际 27%**。后果不只是位置歪一点——**写在该 bbox 里的附属物会被钉错地方**：那把深红折伞只写在长凳 caption 里、没有自己的 item，结果被塞进那个下缘 bbox，成了躺在前景地板上的一件巨大红物，「放在长凳上」完全没实现。

**规则一：先写 y 梯子，再放东西。** 动笔前把画面分成三条水平带并写死 y（按画面高百分比）：
- 背景带（天空 / 墙 / 远处）：0 – 0.30H
- 中景带（主体所在、地平线附近）：0.30 – 0.55H
- 前景带（脚下、近处地面）：0.55 – 1.00H
所有 item 的 bbox 必须落在其中一条带内；跨界要有理由（贯穿画面的长物件、贴地延伸的地面）。**地平线落在 0.52–0.58H，灭点落在 0.24–0.30H。**
自检：随便挑一个 item 问「它在哪条带」，答不出来就是梯子还没定。

**规则二：小道具不许寄生在别的道具的 caption 里。** 「放在长凳上的伞」「桌上的杯子」必须各自有 item 和 bbox，哪怕只占 2–3%。寄生 = 它被钉在宿主 bbox 的几何中心，然后被放大成主角。

**工具（新）：`scripts/preview.py`**
- `python preview.py draft.json`：把每个 bbox 画在灰底上，标「序号 / 标签 / 面积占比 / 像素尺寸 / 中心偏离中线比例」，附中线与三分线。
- `python preview.py draft.json --img 出图.png`：把 bbox 叠在真实出图上，直接读偏差。
**交付前顺序固定**：预览 → 调 y → lint → 编译。

### G34 「移动的某物」必须写成「它留下的痕迹」，否则画出整只东西（101 号实测）

101 号（长曝光石拱桥）里我写 `anything that moved during the exposure is a smear and not an object: a bird that crossed the frame is one thin grey arc`，出图给的是一只**模糊的、有翅膀有身体的鸟**——不是一条弧。

原因不是「模糊不够」，而是**先说了一次 `a bird`**：名字一出现，几万个先验形状被调用，模糊只能把它涂糊，不能把它变没。这与 G28「命名即放大」是同一条，但换了战场：不是尺寸，是**存在形态**。

正解三条，缺一条都不成：
1. **不出现名字**：整段不写 `bird`，只写 `one thin grey arc, faint at both ends and solid in the middle`。
2. **逐项否认部件**：`it has no head, no wings, no body and no eye in it`。
3. **给轨迹的理由**：`it is where something flew through the frame while the shutter was open, and the thing itself is not in this picture at all`。
同理适用于：长曝光的人（不写 `a walking person`，写 `a vertical grey smear at knee height`）、烟花（不写 `fireworks`，写 `a bundle of thin bright lines falling out of one point`）、雨（不写 `rain`，写 `the diagonal streaks the rain left`）。

**106 号补充两条（图内多个拖影人物的实测）**：
- **「抹痕/实像」要逐件分配，不能靠远近默认**。106 写第二个行人「nearer the signs, smeared even harder」，出图里它反而是**全图最清晰的一个**（站着、有腿、有兜帽）——因为把它放在「实像区」（店招）旁边 + 没有像第一个那样逐项否认部件，模型就近了实像先验。修法：每个拖影块独立写全套三件（无名/否认部件/轨迹理由），并且**逐件声明谁是糊的**：`both walkers are smeared; neither one stands still in this picture`。
- **「痕迹里的附属物」也会被画成实物**。写 `two darker vertical smears where the umbrella and the bag were`，出图是一个人**手里提着**真包真桶。修法：附属物也走否认——`it holds nothing; there are no hands in it`，附属物只以「更深的一道」存在，不给名字。

### G35 长曝光里的水面，写「没有波纹」一定失败——要写波纹被压成了什么形状（101 号实测）

101 号原文 `no ripple, no wavelet, no foam and no texture of any kind, because thirty seconds have averaged all of it away`，出图水面上是**一整排清晰的等距横波纹**。实测 mean .277 / dark .211 / mid .771 —— 中间调占七成七，`low key` 没落地。

两条结论：
1. **水面必有波纹**（与 G28 的「水面必有涟漪」同源）。三十秒曝光不会把波纹抹掉，只会把它**压平、压成等距条纹**。正解：`the ripples have been flattened into a row of level lines lying parallel to the waterline, and the spacing between them gets narrower and narrower as they go away from us`——把先验纳入设计并指定它长什么样。
2. **`low key` 是个词，不是数量**。要低长调必须写暗部**面积**：`about two thirds of the bottom half of the frame is dark`。只写 low key + 一个黑点（桥洞）→ dark 只到 .211。

顺带一条：**远岸树/屋顶写 `no detail inside it` 也无效**（树自带树叶先验），要么给形状（`a flat silhouette with a jagged top edge and nothing inside it`），要么换成先验更弱的替代物（仓库屋面、围墙）。

### 交付四件套（2026-11-06 起固定）

每条提示词交付 = `NN-名字.json`（草稿）+ `NN-名字.txt`（编译产物）+ `NN-notes.json`（中文参考）+ `NN-名字-canvas.html`（可拖画布）。

生成画布（**外部技能** `json-prompt-visualizer`，已装在本机；本包只依赖、不分发）：
```
python "C:/Users/Administrator/.dsh/skills/json-prompt-visualizer/scripts/canvas.py" NN.json --notes NN-notes.json --image 出图.png -o NN-canvas.html
# 注意：canvas.py 不在本 skill 的 scripts/ 里，属于外部技能 json-prompt-visualizer；
# 本包只依赖、不分发。缺这个技能时交付四件套降级为三件（json/txt/notes.json）。
```

**`notes.json` 的第一个分句就是框头显示的名字。**格式 `{"summary_zh": "...", "items":[{"caption_zh": "石拱桥——一座横跨……"}]}`，`caption_zh` 用 `——` 隔开「短名」与「描述」。**上面的绝对路径是本机写法**，换机器时改成你自己 skills 目录下的对应路径。另外这个 `shortName()` 补丁只打在本机那份 canvas.py 上，**没有跟着本包分发**——别人 clone 拿到的是原版，框头会退化成统一的「物体」，不影响出图，只影响画布可读性。
- 短名要能一眼认出是画面里哪一块（天空 / 远岸 / 石拱桥 / 桥栏钠灯 / 河面与倒影），不要写「物体1」。
- `notes.json` 不参与编译（官方编译器不认），纯给自己看和给画布显示。
- 改 canvas.py 前先跑 `python -c` 查 `\x08`：`cat -A | grep "^H"` 会给假阳性，别信它。

### G36 「层」必须满幅，并且要在主体块里重写一遍（102 v1 事故）

**症状**：写「一块玻璃，上面映着街」，出图反光只在上半幅，人物与桌子完全没有玻璃覆盖，于是人物从画面里跳出来、显得特别突出。

**根因**：模型是按 item 分块作画的，**层的 bbox 就是层的范围**。我写了 `the glass`（一整块平面）却给了 `[0,40,1536,560]`（上半幅）的框 —— 等于告诉模型「玻璃只存在于上半幅」。同一件事在 22 号 `fills the top quarter` 上已经犯过一次（出成隧道天花板）。

**正解三件，缺一件就漏**：

1. **层满幅**：玻璃 / 雾 / 纱 / 雨幕 / 水幕 / 投影 / 反光层，bbox 一律 `[0,0,W,H]`，并在 caption 里写死 `covers every pixel of the frame, edge to edge and top to bottom` + `there is no part of this image that is not seen through it`。
2. **在主体块里重写一遍**：只写在层里不够，模型会把它当背景。必须在人物 caption 里再写「它压在我身上」并给**具体后果**——哪一道痕从哪穿到哪（`one streak comes down through her left eyebrow and splits it in two`）、她的边断成几段（`her edges break into segments`）。
3. **主体不许有干净轮廓**：`her grey jumper sits at the same value as the wall behind her, so she has no clean outline at all` + `lifted by less than the highlight on the tumbler`（提亮程度低于某件小物）。光靠「压了一层」还不够，得同时**取消她与背景的明度差**，否则她照样跳出来。

配套：层的 caption 里要写「这块面上只有两样东西」并逐项点数，否则模型会往玻璃上加指纹、贴纸、广告字。

### G37 有 bbox 就别再写厘米数；表情只写看得见的（102 v3，用户 m05852 定）

用户原话：「有bbox了你就不用去描写物体的尺寸了」「人物表情不需要那么细致」「用自然语言描述就行」。

1. **删掉所有厘米/米级的物体尺寸**。bbox 已经把尺寸说死了，再写一遍是冗余，而且两句不一致时模型听 bbox、白写。**只保留 bbox 表达不了的两种量**：① 占画面几分之几（`two fifths of the height of the frame`）；② 纵深距离（`the table sits one metre behind the glass, and we stand four metres back`）——bbox 是二维的，进深只能靠句子。
2. **表情只写看得见的物理事实**：眼睛朝哪、嘴闭没闭、眉平不平、脸静不静。**删掉 `the face of someone who...` 这类心理推断**（G3 旧写法已被用户否掉）——「忙了一天、正在看杯底的那张脸」模型读不出来，只会稀释注意力。G3 只保留「视线落点」这一半。
3. 一条 caption 里只留一个主轴。102 v2 的人物块把雨痕、明度、提亮、光向、比例尺、距离全塞在一起，用户判为「太混乱」——**能删的删，能挪进别的块的挪出去**。

### G38 思考别写进提示词（103 号，用户 m05898 定）

用户原话：「你这最后一句是什么鬼，你思考的东西不要输入到提示词里面去」——指 caption 里 `It is the only thing in the picture that is not fixed to the building, and it is the only evidence that someone was here.` 这类句子。

1. **caption 只写画面事实，不写设计意图/叙事解释/元评论**。「它是唯一不属于建筑的东西」「这是有人来过的唯一证据」「这负责让画面不闷」全是给设计文档看的，不是给模型看的。模型不会因此多画任何东西，只会稀释句子。要讲证据物，就写**物本身的样子**（漂着、倾着、半桶水），证据关系留给自己。
2. summary 里的 [MEDIUM]/[SCALE] 等头是写给自己排布用的，**item caption 里不出现任何「为什么」**。每句自问：删掉这句，画面上会少什么？答案是「不会少」就删。
3. 同理适用 notes：框头短名后面的描述也不放设计意图。

### G39 强光源写「数值化克制」（103 号出图 nw .0592 得出）

「warm white, not white」挡不住光斑过曝（p99 .985，光斑内部瓷砖格完全烧掉）。正解三句：
- `the brightest patch of wall sits just under the point where the tiles would burn to white; the grout lines inside the light block stay readable`；
- 面积上限：`the light block covers less than a tenth of the frame`；
- 高光周围写衰减：`around the block the wall falls away fast, two full steps darker at the block's own edge`。
nw 实测红线仍是 0.03，超出即返工。

### G40 「只画到腰」= 亲口允许她悬空（110 号实测，最刺眼的一处错）

110 号人物块写 `her whole figure filling the frame from the top of her head to below her waist`，bbox 给到 `[30,0,780,1320]`（占画面 86% 高）。出图结果：**只有上半截，衬衫下摆凭空吊在半空，下面什么也没有，还从下摆滴着水落到地上留了水圈**——整张图读成「一个人悬浮在玻璃前面」。数值还全在区（sat .253 / nw .0167），所以数值验收救不了这种错。

根因：`to below her waist` 不是「取景到腰」，模型读成「她的身体到腰为止」。**取景裁切和身体存在是两件事，必须分开写。**

1. **人要站在地上，就写脚和地面**：`both shoes flat on the concrete, her weight evenly on both feet`，并且**必须给一个支撑物**（长凳、立柱、台阶）——空地上凭空站人，模型会把她画成贴上去的剪纸。
2. **真要裁在腰上，就明写「她身体在这条线以下不存在，而且没有人会因此觉得她缺了腿」**：`the frame cuts her at the waist; there is nothing of her below that line, and the picture does not read as a person missing her legs, because the hem of her shirt hangs the whole way down to the crop`。含糊的 `below her waist` 永远不要用。
3. 自查：**凡人物 bbox 下缘没到画框底边，就要有一个「为什么下面没有了」的物理交代**（裁切句 / 地面 / 支撑物），三者至少给一个。

### G41 光源不许给名词：写了 tube / lamp，它就把灯画进画面（G11 加强，110 号重犯）

110 号 summary 写 `One cold white tube above and behind the camera, out of frame`，出图**画面顶部横着一条发白的灯管**——`out of frame` 完全无效，因为 `tube` 是一个有形状的名词。

1. **光源描述里不出现任何实体名词**：tube / lamp / bulb / fixture / strip light / diffuser 全部禁用，连着 `out of frame` 一起删。只写光的后果：`the light comes from high behind us and dies within arm's reach`。
2. 光只以三种东西存在：**落点（写成物：`the top of her shoulder` / `the rim of the cup`）+ 衰减（`two steps darker at her knees`）+ 未被照亮的区域逐项点名**。
3. 自查：全文搜 `tube|bulb|lamp|fixture|strip|diffuser`，**任何命中都必须是「没有这个东西」的否认句**，不能是描述句——哪怕后面跟了 `out of frame`。

### G42 夜街、路面、水面自带画线：写「毫无细节」一定失败，要写成什么样的线（110 号 + G28 补）

110 号写玻璃外是 `an unlit dark that holds no detail at all`，出图那面玻璃后面出现了**一条完整的路面加一条黄色分道线**。

- 与 G28 后半条同源：**场景自带的先验只能纳入设计，不能否认**。公路必有画线、街道必有路缘、水面必有涟漪、玻璃必有反光。
- 正解写法：给它一个形状，然后**指定它是什么样**——`one horizontal band of dark grey road lies beyond the glass, with a single dull yellow line running level across it`。写清楚了，它就不会自己加第二条、第三条、加路牌、加车灯。
- 顺序：**先认下这个先验，再规定它的样子**。反着来（先说「没有」，再想「其实有一条」）一定翻车。

### G43 写 `Mid tone overall` 会把整张图压进中调：必须同时给「暗部面积」和「亮部色相」（110 v2 实测）

110 v2 summary 第一句就是 `[VALUE] Mid tone overall.`，出图实测 **dark .062 / mid .924 / lit .080 / sat .143**——**92% 的画面挤在中调，几乎没有暗部，亮部一点颜色都没有**，整体发灰。数值判读：mean .288 偏暗、dark 远低于 0.08 下限、mid 冲破 0.75 上限、sat 远低于 0.16。

根因：`Mid tone overall` 是一句**总指令**，模型执行成「所有东西都画成中间灰」，于是我把每件东西都写成湿的、灰的、中等明度（湿玻璃、湿水泥、湿皮肤、拉丝钢），**没有任何一件东西被指定为「暗」**，也没有任何东西被指定为「带色」。这与 G4（高调要有黑锚点）是同一族，但触发条件相反：不是高调，是**中调**，一样要锚。

1. **「Mid tone overall」后面必须紧跟一句黑锚点**，并给**面积**：`two thirds of the frame is this middle grey, and the darkest thing in it is the shadow under the bench, which covers the whole strip along the bottom and holds no detail`。不写面积，模型不给暗部。
2. **亮部必须点名带色**：`the brightest thing is the lit drum window, and it is a cold blue white`——只写「最亮」不写颜色，出来就是没有色相的白（sat .143 的直接来源）。
3. 三种调子各给一个**数量**：暗部面积、中调面积、亮部面积，三者相加占满。只写形容词（`mid tone` / `low key`）永远不算数（同 G35 末尾）。
4. 自查顺序：先定「谁最暗、占多少」，再定「谁最亮、什么颜色」，最后剩下的才是中调。

### G44 写「里面什么都没有」会失败：要写「里面是什么颜色的东西」（111 号实测）

111 号机器排写 `Four of the doors are dark and show nothing inside them`，出图**最左边那台圆窗里清清楚楚塞着一堆白衣物**——洗衣机的默认先验就是「里面有衣服」，一句「什么都没有」压不住。

1. **否定内容要改成肯定另一种内容**：`the other four hold a dark load of laundry, and their drums read as one flat dark mass with no pale shape anywhere in it`。给一个东西，然后规定它的颜色和形状；不要给「空」。
2. 同族规则汇总（都是「先认先验再规定样子」）：G28 尺寸/命名、G42 路面必有画线、G27 水面必有涟漪、G44 容器必有内容。
3. 111 号另两处：**暗锚点被别的光洗亮**（写「椅下是最暗的地方」，但椅下露出被同一盏灯照亮的墙裙，最暗跑到画框最下缘）；**第二亮抢戏**（她绒毛衣的亮面比圆窗还亮，撞 G32）。所以暗锚点必须落在**有实体遮挡**的地方（椅下有背板、或改成机器与地面之间的那条缝），第二亮必须显式压一档：`her sleeve is the brightest thing on her, and it is still a full step darker than the drum window`。

### G45 画布基底不能作为 item：写「The paper itself」会被场景化成画面里的一堵墙（113 号实测）

113 号把新闻纸写成满幅 item（`The paper itself, covering every part of the picture: a warm cream ground with a faint grain`），出图里**它变成了一堵上下包住窗户的石膏墙**（石纹颗粒、深灰、占约四成画幅）——「纸」这个字被读成「房间里的纸/墙面材质」，不是「这张图印在纸上」。这比 G30（纸/留白不是物体）更极端一步：**连画布本身这个层都不能给 item**。

1. 画布/纸/印刷基底只能写在 **summary 的 [STOCK] 与 [FINISH] 头**里（`One old press photograph … printed in a single black ink`），**绝不给 item、绝不给 bbox**。凡是「这张图本身是什么材质」的陈述，一律进 summary；凡是「画面里的一件东西」，才进 items。
2. 同一实测还确认：**窗框 bbox 给 78% 高、模型就自动把剩下的 22% 画成墙**。要「窗几乎满幅」就把窗框 bbox 直接给满幅 `[0,0,W,H]`，用 caption 写「内缘贴近四边」，不要留缝再否认（`only a finger of wall` 挡不住）。
3. 顺手的 lint 事实：`high-key`（连字符）不被关 8 的明度正则识别，**必须写 `high key`（空格分开）**。

### G46 尺寸标定：bbox 管形状与位置，「距离 + 公认尺」管大小；1/3 下限可被打穿（115 号三张实测，2026-11-07）

**实验设计**（`（实验脚本）_mk115.py`）：同一走廊、同一机位高度与朝向、同一光、同一描述结构，**只改「她离镜头多远」**（四步 / 八步 / 十二步），场景给三个公认尺（30cm 地砖网格、2m 门 + 1m 门把手、10cm 踢脚线）。三张 bbox 高度分别 845px / 460px / 276px（55% / 30% / 18%）。

**实测结果**（1024×1536，量头顶到鞋底的像素）：

| 张 | 距离 | bbox 高度 | 实测占比 | 放大系数 |
|---|---|---|---|---|
| 115a | 四步 | 55% | **54.3%** | 0.99（精确执行） |
| 115b | 八步 | 30% | **43.6%** | 1.45 |
| 115c | 十二步 | 18% | **28.3%** | 1.58 |
| **115d 对照** | **度量句全删** | 18% | **43.6%** | 1.58 |

**115d 是关键对照**：构图、bbox（18%，276px）、场景全部与 115c 相同，只把「两米门 / 一米把手 / 三十厘米砖 / 十二步」这些数字删干净。结果**弹回 43.6%**——和 115c 的 28.3% 差 1.5 倍。所以「不写度量、只用 bbox」在小尺寸区**不成立**：度量句不是 bbox 的尺子，是「这个空间有多大」的声明；删了它，bbox 立刻退回名字先验。

四条结论：

1. **bbox 在「大尺寸区」（≥50%）几乎被像素级执行**（54.3 vs 55）。用户 m06987 问「不要写度量尺寸、直接用 bbox 行不行」——**行，但只在 ≥50% 的区间行。**
2. **bbox 在「小尺寸区」（<50%）被放大 1.45–1.58 倍**，而且越小说得越狠。补偿：**目标 × 0.6 才是该写的数**（想要 30% 写 18–20%，想要 18% 写 10–12%）。
3. **G21 的 1/3 下限被打穿**：115c 实测 28.3% < 33%，这是第一次有角色低于 1/3。条件不是「写了更小的数字」（那从来无效），而是**同时给了「离镜头多远」+「场景公认尺」**。所以 G21 要改写：**1/3 下限只在「没有距离参照物」时成立**；给了距离 + 门/砖/台阶这类公认尺，下限降到约 25–28%。
4. **度量句不是给 bbox 用的，是给「这个空间多大」的锚**，它决定 bbox 被遵守的程度。可以砍到最少：**一个门高 + 一个地砖格**就够（115 写了三个尺，起作用的主要是门）。别写自己的厘米数（99 号台灯已证）。

**配套 lint 修正**：G8 的「可量距离」词表原来只认 `metres away` / `metres from`，**不认 steps**，导致「四步远」被判「没有比例尺」→ 已扩为追加 `'steps from us'`, `'steps away'`, `'steps from'`, `'paces from us'`, `'paces away'`（改完 `\x08` 计数 0）。

**走廊题材的副作用（记录，不是错）**：三张 dark 只有 .033 / .009 / .005、sat .11–.14、nw .028–.034（略破 .03 红线）。浅色走廊 + 尽头窗光天然高调低饱和，**这类题材必须额外指定一个暗锚**（例：把左侧一个门洞写成全暗、或换到侧光时段），否则暗部面积归零。

### G47 物体的尺寸几乎完全由「名字先验」决定，bbox 只管位置不管大小（116 号实测，2026-11-07）

**实验设计**（`（实验脚本）_mk116.py` → `moss-prompts/116-object-size-conflict.json`）：四件东西站在同一面灰绿墙前的地板上，**bbox 高度故意和常识反着来**——白瓷马克杯 59%（巨型）、锈红木椅 24%、奶白冰箱 19%（矮柜）、硬币 4%。若 bbox 赢，杯子该是巨物、冰箱该是矮柜。

**实测（1536×1024 出图，量物体自身高度）**：

| 物件 | 名字先验 | 我给的 bbox | 出图实测 | 偏差 |
|---|---|---|---|---|
| 白瓷马克杯 | 小 | **59%** | **约 20%** | **缩小 0.34×** |
| 锈红木椅 | 中 | 24% | **约 50%** | 放大 2.1× |
| 奶白冰箱 | 大 | **19%** | **约 35%** | 放大 1.8× |
| 硬币 | 极小 | 4% | 约 1–2% | 接近（先验本来就极小） |

**结论：物体与人物是两套完全不同的规则。**

1. **人物**：bbox 在 ≥50% 区间被像素级执行（115a 写 55% 出 54.3%），只在 <50% 区间被放大 1.45–1.58×。
2. **物体**：**bbox 几乎完全不被当尺寸用**，它只定位置和大致占位；尺寸由名字自带的标准大小决定，而且**反着写也没用**（把杯子框给 59%，它照样画成一只正常杯子）。所以「把框画大点让它变大」这条路对物体是死的。
3. **物体的四把尺**（按有效性排序）：
   - **去名尺（最有效）**：不叫「马克杯」，写 `a white glazed cylinder with one loop handle on its right side`——名字一拿掉，先验就没有了，bbox 才开始被当尺寸用。同理：不写「冰箱」写「一台奶白搪瓷矮柜，一扇平门占满正面」。
   - **公认尺 + 距离**（G46 已证，对物体同样成立）：`it stands on the floor four steps away, and its rim comes up to a third of the height of the door behind it`。
   - **相对物**：`its rim reaches exactly the height of the chair's seat`——和一个已知尺寸的邻居直接比高低。
   - **裁切尺**（唯一能可靠做出「巨大」的手法）：`its rim is out of frame above; we only see the lower part of it`——把物体切出画框。这跟人物的「让画框把她切掉」是同一条路。
4. **摆拍题材的连带副作用（116 实测）**：mean .588（过高）/ dark **.006**（几乎没有暗部）/ sat **.062**（四件东西的色相全被洗掉）/ lit .016 << shadow .128。原因是「一面浅灰绿墙 + 一片软日光 + 四件浅色东西」本身没有任何暗锚，也没有任何大面积饱和色。**静物摆拍必须先指定一个暗锚（一道深色的墙脚阴影带、一块深色台面）和一个饱和色落点（让它落在一件被照亮的大东西上），否则整张发白。**

### G48 标尺物必须和主体在同一个深度平面上；嵌进构图槽位的人物会被构图吞掉 bbox（117 号实测，2026-11-07）

**117 号**（`moss-prompts/117-weaving-shed-girl.json`，旧纺织车间，1536×1024）把 G46/G47 全套都用上了：她 bbox 17%（= 目标 28% × 0.6）、`she is eight steps from us`、公认尺（窗高两米 / 地面一米方板）、相对物（`her head comes up to the bottom rail of the lowest window`）。出图实测 **她占画高 41.5%**（目标 26–28%），**放大约 1.5 倍**；而且位置也没守住——bbox 给 x 880–1000（中线右侧），她被画在 x 500–660（中线左侧）。

**失效的两个原因，都是「深度平面」问题**：

1. **标尺物在另一个深度平面上**。窗在远处墙上，她站在中景通道里；「头顶到窗下槛」是一句跨深度的相对物，模型用不上，于是退回名字先验（girl = 立绘级大人物）。对照 **115c 为什么成功（28.3%）**：门、地砖网格、踢脚线全部**贴在她同一个深度平面上**，标尺就长在她脚边。
   → **规则：给人物定标，标尺物必须和她同深度、最好贴着她**。可用：她身侧一步的立柱/门框/桌沿/机器顶横梁/墙裙线。禁止：远处墙上的窗、远处的地面线、画框外的任何东西。
2. **人物被钉进构图槽位时，bbox 的位置和大小一起作废**。117 的构图是「两排织机之间的通道中央」，这个槽位比 bbox 强势：她自动站到通道正中、自动放大到与通道相称。
   → **规则：如果要她小、要她偏，就必须明写「她不在通道正中」**，例如 `she does not stand in the middle of the aisle; she stands close to the left row, and the aisle opens up wide to her right`。只给 bbox 不给这句，通道会把她拉回正中。

**117 号成立的部分（同一张图里的正面对照）**：
- **G47 去名尺 + 相对物对物体完全有效**：红容器写成 `a red moulded plastic vessel, wider across its open top than at its base, with a thin wire loop handle fallen over to one side`，出图就是一只正常大小的红桶（画高 19%，前景四步处），没有变英雄道具；钢纱管 `a small hollow steel spool, smaller than the palm of a hand` 也画准了（两片平法兰 + 窄筒身，躺在地上）。**同一条规则在人物身上失效、在物体身上成立——差别就在「有没有名字」。**
- 暗锚（织机剪影约占三分之一）、唯一饱和色（红桶）、最亮（最近光斑暖金、停在纯白之前）三件全部兑现；实测 nw **.0070**（极干净）、sat **.236**（红桶站住，116 只有 .062）、strong .102（光斑硬边成立）、dark .308（低 key 生效）。
- 代价：mean .268 偏暗一档（低于 .38 目标），因为全图只有光斑是亮的、其余都在暗里。**低 key 室内题材要把「亮部面积」也写成数量**，否则亮部只剩几块光斑、mean 掉到 .27。

**另一处：朝向句 `from the front, a little to her left` 出成了背右三分之三。** 与 114a 同一个坑（G29 补二）。要正面就写死可见部位 + 否定：`we see her face and both her eyes; she is turned towards us, and we are not behind her`。

### G49 不要在别的 item 里提到人物，否则人物会被并进那一块、整块消失（117v2 实测，2026-11-07）

**117v2** 为了给 G48 提供同深度标尺，新增了一个铸铁立柱 item，caption 里三次提到她：

- `A cast iron column standing one step to the left of the girl`
- `it rises from the floor at her feet straight up out of the top of the frame`
- `the girl's head reaches exactly that joint`

立柱 bbox `[340,0,412,632]`（72×632，一根通到画框外的细长条），她的 bbox `[432,455,552,632]` 紧贴它右边。

**出图结果：画面里没有人物。** 判据（不是"看着像没有"，是量出来的）：

- 她 bbox 那片区域（x 432–552, y 455–632）实测 mean **0.131** / sd **0.070**——一片平坦暗墙，没有任何轮廓。
- 全图扫一遍：皮肤掩膜只在窗户（y 88–280）和地面光斑（y 484–824）里有大片命中，**没有任何脸大小的孤立色块**；局部对比度热图里除了四扇窗、x≈500 那根竖线、地面光斑，**没有人体轮廓**。
- 对照 117v1（同样 6 items、她的 caption 与 v2 几乎一样）：她出图占画高 41.5%，清清楚楚。**差别只在 v2 多了一个提到她三次的立柱块。**

**结论（机制假设，v3 验证中）**：别的 item 的 caption 里只要反复点名人物，模型会把人物理解成**那一块的组成部分**，然后在生成该块时把"人"消化掉；人物自己的 character 块反而变成重复信息被丢弃。**同一现象的近亲**：G12 的道具归属、106 号"附属物给了名字就变实物"——都是"名字把人/物拽到别的块里去"。

**规则**：

1. **人物只在 character 块里被描述**。其他任何 item 的 caption 里不出现 `the girl` / `she` / `her`，一句都不行。
2. 需要标尺就写在**她自己的 caption 里**，用同深度的邻居做参照，且邻居**不需要在那张图里有独立 item**：`The machine frame at her right hand stands in the same plane as she does, and its top beam comes level with her chin`。
3. 需要交代人物与场景的关系时，改写场景块本身：不写 `the aisle she stands in`，写 `the two rows leave a wide empty aisle between them, and that aisle runs up the left third of the frame`——把关系交给构图，不交给代词。
4. **交付前搜一遍**：除 character 块外，全文 `grep -i "the girl\|she \|her "`，命中即改。

**附带一条位置发现（117v1/v2 两次一致）**：bbox 的 x 在"有明确通道/纵深"的构图里会被构图槽位覆盖，而且**覆盖的结果往往比我给的更好**——v1 我给 x 880–1000（57–65%），出图在 x 500–660（33–43%），正好压在左三分之一线上。**遇到这类构图，直接把 bbox 放到槽位的实际落点，不要跟它较劲。**


---

## G50 官方口径：普通场景用 caption，Layout 只留给「必须精确」的东西（2026-11-07 查官方仓库后定）

**来源**：`https://github.com/OpenMOSS/MOSS-Image` 的 `skills/moss-image-prompt-enhancer/SKILL.md` 原文：

> Use a caption for ordinary scenes, photographs and illustrations. Use Layout when specific text placement, a poster, several panels, or controlled object relationships would benefit from bounding boxes. **A detailed image does not automatically need Layout.**

**这条推翻了我们 01–117 号的做法**：那张图再复杂，也不代表需要 Layout。Layout（bbox）是为四件事设计的——**文字排版、海报、多格、受控物体关系**；普通场景 / 照片 / 插画一律用 caption。

**为什么要改**：

- 官方把 Layout 明确标为**实验性功能（experimental）**。
- 我们自己的实测已经把 bbox 的三个失效面全撞过一遍：G21（人物下限 1/3）、G46（<50% 时放大 1.45–1.58×）、G47（物体尺寸由名字先验决定、bbox 只管位置）、G49（人物被别的块消化掉）。
- 结论一致：**bbox 只在"落位"上可靠，在"多大"和"出不出现"上都不可靠**。而"多大、出不出现"正是 caption 最擅长的。

**新的分工（写作前先选，不许默认 Layout）**：

| 画面里有 | 用什么 |
|---|---|
| 只有场景 / 人物 / 物品，无文字，位置不需要精确到像素 | **caption**（`{"caption": "..."}`） |
| 有需要精确落字的文字（招牌、海报、书页、标签） | **Layout**，且文字必须单独 text item |
| 多格 / 拼贴 / 分镜 | **Layout** |
| 两件东西必须严格不重叠、或有精确的上下/左右关系 | **Layout**，只给这两件东西 bbox |
| 以上混合 | **混合输入**——官方明说模型「支持自然语言和结构化语言的混合输入」：summary 用自然语言写全场景，只给必须精确的块加 bbox，**人物永远不给 bbox** |

**caption 草稿的 schema（与我们 Layout 草稿不同，别混）**：

```json
{"caption": "整段连贯散文，空间关系全部用文字写，可见文字原样引号"}
```

- 只有 `caption` 一个键，**不能有 width/height / summary / items / bbox**（编译器会拒）。
- 编译产物是**纯文本**，不是 JSON。
- 分辨率不在 prompt 里，出图时在工作流里设（1536×1024 / 1024×1536 / 1536×1344）。
- 允许分段（用空行），**不要**为了显得结构化而塞坐标。

**caption 的写法纪律（与 Layout 版共享的部分照旧，这段是 caption 特有）**：

1. **空间关系只能靠文字**：用「离画面左缘多远 / 在谁的手边 / 在哪个边缘之外」这类**相对位置**，而不是「占画高 28%」。没有 bbox 就没有坐标系，写百分比只能当建议。
2. **先写视点段，再写光，再写暗，再写人，再写前景物**——单向注意力，顺序就是重要性。
3. **人物的出现靠"她在做什么 + 她站在什么上面"**保证，不靠表情词：`both her shoes flat on the ground and her weight even on both feet`。
4. **不要把人放在最亮的区域**（117v2/v3 两连败的机制）：caption 里写 `she stands just outside the near edge of the second patch of sunlight, on the dark side of that edge` —— 用"光的边缘"给她定位，既定了位置又定了明度关系。
5. 字数 **600–800 词**是实测舒服区（117v4 是 775 词）；低于 120 词 lint 会 WARN。

**lint.py 已支持 caption 草稿**（2026-11-07 改）：识别 `{"caption": ...}` 无 items 的草稿，跳过关 1 的 width/height 与关 10 的 bbox 检查，其余八关照跑。`all_text()` 现在同时读 `summary.caption` 和顶层 `caption`。

**踩坑**：`looking straight down its length`（英文里"沿着它的长度看过去"）会被关 3 的 `OVERHEAD_CAM = ['looking straight down', ...]` 判成俯拍，因为前面 60 字符里没有 sun/light 可豁免。**写"沿纵深看"用 `looking along its length`**，别用 `straight down`。


---

## G51 人物必须给「画内定位三句」，缺一句人物就消失（117v2/v3/v4 三连实测，2026-11-07）

**症状**：同一个场景、同一段人物描述，v1 画出了人，v2/v3/v4 三版人都不在画面里。v2 用了 bbox，v3 删了 bbox，v4 干脆不用 Layout 只用纯 caption —— 三次都没有人。

**判据是量出来的，不是看出来的**（本轮无图像通道）：
- 她 bbox 区 mean .131 / sd **.070**，对照 v1 她实际所在处 sd **.183**（平坦墙 vs 有人）；
- 皮肤掩膜在窗和地面光斑上大片命中，**没有脸大小的孤立色块**；
- 滑窗人形检测（宽=高×0.34、高 16–28% 画高）最高分候选 inside .176 / ring .463，看着像"亮地面上的一个暗块"——但**逐行剖面证伪**：该暗块右缘稳定在 x≈575–580、从 y460 一直连到 y655，左边一直顶出裁切框外，y658 之后环自身掉到 .123 → 那是**左侧大片暗区的右边缘**，不是人。

**根因 = v1 有、v2–v4 全丢的三句「画内定位」**：

| v1（有人） | v2–v4（没有人） |
|---|---|
| `a girl standing still **among the loom frames**` | `in the aisle between the two rows` / `on the concrete in that aisle`（空处） |
| **`All of her is inside the frame, with the dark of the machines above her head and the lit concrete below her feet.`** | 整句丢失 |
| `her head comes up to the bottom rail of the lowest window` | 换成远处物件当标尺（跨深度，无效） |

**三句缺一不可**：
1. **`All of her is inside the frame, ...`** —— 显式声明整个人在画框内。不写这句，模型有权把她理解成画外/极小/不存在。
2. **头顶对齐一个画内物体**：`The bottom rail of the lowest window sits level with the top of her head` —— 让她有一个必须成立的高度，模型就得画出一个那个高度的人。
3. **脚踩在有名字的地面 + 上下明度不同**：`the dark of the machines above her head and the lit concrete below her feet` —— 夹层锚。上下都是同一个明度时她没有边界。

**附加**：她要在**有实体的区域**里（`among the loom frames`），不要在"两排之间的通道中央"这种纯空间描述里。空间描述是空的，模型不会往空处放人。

---

## G52 暗背景前的主体必须比背景亮一档，否则被背景吸收（117v4 实测，2026-11-07）

**错的写法**（v4）：`She stands in the shadow between two of the light patches, so she is **a full two steps darker than the concrete at her feet**, and only the edge of her right sleeve catches any of the warm light.`

这句话在三处同时把人抹掉：① 她整身暗；② 她背后的机器也是暗；③ 唯一的亮只有"右袖的一条边"。结果 = 暗块里的暗块，没有轮廓。

**对的写法**（v5，已入库）：
```
The floor she stands on is in shadow, and she reads one step lighter than the dark behind her
and one step darker than the concrete she stands on: her shoulders, the top of her head and the
outer edge of her left arm are the lightest part of her, the far side of her body and the space
under her chin fall away dark, and the edge of her right sleeve catches the warm gold.
```
三个要点：① **比背景亮一档、比脚下地面暗一档**（夹在两者之间才有轮廓）；② **点名她身上最亮的部位**（肩 / 头顶 / 外侧手臂）；③ 背光面单独说"掉进暗里"，不要整身一起暗。

**同族禁令：不要在人要占的位置上写"空"。** v3/v4 的机器块写了 `leave a wide empty aisle between them` —— `empty` / `nothing stands here` / `clear` 这类词会把那块真的清空，包括你要放的人。要描述宽度就写尺寸（`the rows stand three metres apart`），不写空。

**通用推论**：任何主体（人 / 物 / 动物）在暗区里，都要单独声明「它比身后的东西亮几档」。只写"它在暗处"等于说"它不存在"。

---

### G53 不许用数值断言「画面里有没有某物」（117v4 判读事故，2026-11-07）

**事故经过**：117v4 出图后，我（助手）用 probe 数值 + ASCII 明度图 + 皮肤掩膜 + 滑窗人形检测，连续三次向用户断言「人物不在画面里」，并据此写了 v5 的五处「修正」。用户回原话：**「你自己看图，这不是一直有人吗」**——人一直在，判读全错，v5 的动机根本不成立。

**错的机制**（三条判据全部失效，且失效方向一致）：

| 判据 | 我用的阈值 | 为什么必然假阴性 |
|---|---|---|
| 区域明度 sd | 她 bbox sd .070 < v1 有人处 sd .183 | 暗部里的人本来就是一片均匀暗块，**sd 低是「她在暗处」的证据，不是「她不在」的证据** |
| 皮肤色掩膜 | 无脸大小孤立块 | 暖金地面 / 暖木墙 / 暖光斑会把掩膜大面积污染，把真正的脸淹掉 |
| 滑窗人形检测 | 最高候选 inside .176 / ring .463 | 在暗区边缘，窗框的「暗块 + 外侧稍亮」几何与人形几乎同构，**误报不可避免** |

**结论（硬规则）**：

1. **没有图像通道时，不要对「画面里有没有某物」下断言。** 可以说「我量到这块区域是平的」，不能说「这里没有人」。
2. **数值能回答的问题只有三个**：这东西在哪、多大、多亮。它回答不了「这是不是一个我以为的东西」。
3. 交付话术：老实写「我这边看不到图，只能给你量出来的数」，比编一个结论安全一百倍。
4. **绝不因为「量的结果不对」就去改 prompt**——改 prompt 的动机只能来自用户的话或明确的数值失控（过曝、饱和、明度档）。
5. 反向也成立：用户说「这里有人」就是有人，不要用数值去反驳用户对画面的观察。**用户有眼睛，我没有。**


---

## G54 bbox 会被「头顶对齐同深度物体的哪条边」压住，不再按 1.5 倍放大（119 号实测，2026-11-07）

### 实测对照表（五组，同一个人物、同一个 1024 高的画布）

| 号 | 场景里有什么参照 | bbox 给的高度 | 实际高度 | 放大倍数 |
|---|---|---|---|---|
| 115b | 走廊：门、门把手、踢脚线、地砖 | 30% | 43.6% | **1.45×** |
| 115c | 同上 | 18% | 28.3% | **1.58×** |
| 118v4 | 雪原 + 同深度篮架（但只写了「她身高＝篮板宽」） | 13.7% | 21.5% | **1.57×** |
| 117 | 车间，标尺物在**另一个深度** | 17% | 41.5% | **2.40×** |
| 118v3 | 雪原，什么都没有 | 16.6% | 43.0% | **2.60×** |
| **119** | **更衣室 + 同深度储物柜 + 明写头顶对齐柜顶** | **28.6%** | **31.1%** | **1.09×** |

### 结论

放大幅度不是由「场景里有没有参照物」决定的，走廊明明有门有地砖照样 1.5 倍。
决定它的是这一句：**「她的头顶比某件同深度物体的某条边低多少」是否被明写出来。**

- 不写 → 模型按「这个空间里人应该多大」自己估，1.45–1.6×。
- 写了但对齐的是**另一个深度**的东西 → 更糟，2.4–2.6×（117 号，标尺在远处墙上）。
- **写了、同深度、而且那条边在画面上是水平贯穿的** → 1.09×，几乎照抄 bbox。

### 可用句式（119 号一次通过的那句）

> `Her size is fixed by the furniture beside her: she stands on the same floor line as the bank and the top of her head sits a little below the top edge of the lockers, so she is a little shorter than one locker door and her whole height is a little under a quarter of the height of the frame.`

四个要件缺一不可：

1. **`stands on the same floor line as X`** —— 先锁地面线，两个东西才在同一个透视平面上。
2. **`the top of her head sits a little below the top edge of X`** —— 说清头顶的对齐位置，不要写「她比柜子矮」这种没有具体对位的句子。
3. **X 的顶边在画面上是水平贯穿的**（一排柜子、一道墙裙、一条栏杆、一根横梁）。孤立的竖直物体（一根柱子、一个篮架）给出的对位信息弱，118v4 就只做到 1.57×。
4. **`her whole height is a little under a quarter of the height of the frame`** —— 分数仍然要写，它是安全带，不是主尺。

### 两个副作用（119 号实测）

- **参照物自己也会缩**：柜子 bbox 给了 310px，实测约 317px（1.02×），没缩；但 118v3 里没有对位句时柜类物体曾缩到 0.9× 以下。所以对位句是双向的，同时稳定了人和物体。
- **比值比绝对值更重要**：119 号最终 柜子高 / 她高 = 1.00（目标是 1.058，误差 6%）。判定几何锁定成不成立，看的是这个比值，不是她占画高的百分数。

### 判定口径

出图后量两个像素高度就行：

- 比值落在 **0.9–1.2** → 几何锁定成立，尺寸问题按这条路解。
- 比值 ≥ 1.5 → 对位句没生效，回查是不是犯了上面第 3 条（参照物不是水平贯穿）或第 1 条（不在同一地平面）。

---

---

---

## G57 画面的「地面强度」决定人物能被压多小（122 号两版实测，2026-11-07）

同一个 bbox 比例、同一套对位句，结果差 2.4 倍，差别只在画面下半部是什么。

| 号 | 下半部是什么 | 请求比例 | 实际比例 | 倍数 |
|---|---|---|---|---|
| 118v4 | 空旷雪原，前景是平暗的雪，没有任何线 | 13.7% | 21.5% | 1.57× |
| 119 | 一排柜子 + 平铺地砖，线条稀疏且不向灭点收 | 28.6% | 31.1% | 1.09× |
| 117 | 两排机器夹出的通道 | 17% | 41.5% | 2.40× |
| 122v1 | 石板坡道，横向石缝一级一级往上收 | 26.4% | 78% | 2.94× |
| 122v2 | 大石台阶，正面十来级，边缘线全部向灭点收 | 25.4% | 61% | 2.40× |

**机制**：模型读到一个强透视的地面，就先把「可站人的台阶」排好，再从最近的一级往上放人。地面上有越多横向线条往灭点收，可站的位置就越集中在近处，人被吸到近景、比例随之放大。对位句（G54/G56）管的是「她身旁那个东西多高」，管不了「她站在第几级」。

**结论**：想要 25–30% 的人，只能配**弱地面**——平原、雪地、水面、平铺地砖、地毯、没有任何横向线条的空地，而且前景要空、要暗。强透视地面（台阶、长廊、铁轨、坡道）的场景，把目标改成 **40–50%**，按「中景主体」去设计，别再去追那个数。

**未验证的对策**：有强地面又想要小人时，在前景放一件具体的东西把近景占住（一根斜出画面的枝、一盏石灯、一段栏杆），并明写「这是近处唯一的物体，它之后才是台阶」。这条还没实测过，用之前当假设。

## G56 当标尺的物体，它的 bbox 必须和它所在的深度自洽（122 号实测，2026-11-07）

119 号用「头顶对齐柜顶」把 bbox 放大从 2.4 倍压到 1.09 倍，122 号用同一句式却放大到 **2.94 倍**。差别不在句式，在**标尺物本身画在哪个深度**。

- 119 的标尺：一整排柜子，bbox `[240,320,1290,630]`——**一条横贯画面的、高度只有画高十分之三的水平带**，平贴在她身后的墙上，和她同一个深度。模型把它读成「背景平面上的重复构件」，于是「她头顶比柜顶低一点」这句话把它钉在了那个平面上。
- 122 的标尺：最近的樱树，bbox `[1130,0,1500,760]`——**一根从画框顶通到画高四分之三的竖直条**。模型把它读成「前景立着的一棵大树」；树是前景，站在树半步之内的人自然也是前景；前景的人就该画大。**对位句被深度判读覆盖了。**

**规则**：拿来做标尺的东西必须满足两条，缺一条就退回 1.5–3 倍放大。

1. **它的 bbox 必须是一条水平带**（高 ≤ 画高 40%、宽 ≥ 画宽 40%）。柜列、墙裙、栏杆、桌沿、货架横梁、一排窗台都行。**竖直物体（树、柱、路灯、门框）不能单独当标尺**——它们的 bbox 天生是细高的，模型只会把它读成「离镜头很近的东西」。
2. **它的 bbox 上下缘都要落在同一块地面上**。树从画顶开始＝有半截在画外＝它必然比画内所有东西都近。要用竖立物当尺，就把它整个画进来，而且底边落在她脚边那条地面线上。

**替代写法**（竖立物必须用时）：不要让它当尺，让**它脚下的地面**当尺。写 `the base of the trunk sits on the same line of paving stones that her shoes are standing on, and that line runs level across the frame`，再单独写她的分数。地面线是水平的，不会被读成前景。

**自查**：交付前看一遍标尺物的 bbox，问一句「如果我只看这个框的长宽比，我会不会认为它在镜头前两米」。会，就换。

## G55 漏光、光晕、眩光这类「没有物体的东西」必须逐项否认它是物体（121 号实测，2026-11-07）

121 号写的是「从左上角进来一道橙红楔形，占约四分之一画幅，向右下边缘渐变消失，没有任何硬边」。出图把这个楔形画成了**一块有清晰边缘的实心红色形状**——像挂在楼顶的横幅或另一栋楼的红色屋顶，不像光。整张图因此读作「天台旁边有块红色建筑」，而不是「相机漏光」。

原因和 G34（移动物要写成痕迹）同族：**只要一个东西被写成「在画面里占一块面积、有边界」，模型就给它实体**。光和实体在提示词层面没有区别，除非你明说。

### 写法三件

1. **先否认它是任何东西**：`it is not a banner, not a roof, not any surface, not any object at all; it is light and it has no body of its own`
2. **写它跨深度而值不变**（这是光独有的物理指纹）：`it lies over the sky, over the far buildings and over the railing at exactly the same strength, so it does not sit behind anything and does not sit in front of anything`
3. **写它的边界是值的变化而不是线**：`its edge is only a change in brightness, and if you follow that edge with your eye you find no line anywhere, only a place where the warm colour has thinned out`

### 反例（全部实测失败或半失败）

- `fades out gradually`（121，出成实心块）——「渐变」不足以取消边界
- `no hard boundary anywhere on it`（121，同上）——否定「硬边」不等于否定「边」
- 只写位置和面积（`covers roughly a quarter of the frame`）——面积词在 B9 里是几何指令，会直接生成一块实体

### 同族清单

凡是「有面积但没有实体」的现象都走这一套：漏光、眩光、鬼影、镜头雾、暗角、反光、彩虹耀斑。反过来，**有实体但面积不定**的现象（影子、雾、水汽）走 G27/G31 那一套（写它被压成了什么形状）。

## G58 光环必须逐项否认「辐条 / 射线 / 断弧」，只说「无内圈无同心弧」压不住（126、127 两次实测，2026-11-07）

两次都写了 `there is no second one, there is no inner ring and no concentric arcs inside it`，出图两次都是**带辐条、断弧、外扩射线的齿轮环**。模型对 `ring` 的先验是「发光环 = 带光芒的装饰环」，只否认同心结构不够。

可用写法（四段，缺一段就长刺）：

1. **形态**：`a single thin smooth circle drawn in one stroke, the thickness of a pencil line`
2. **内部与外部都是空**：`completely empty inside, with nothing drawn within it and nothing outside it either`
3. **逐项点名八样**：`no second ring, no arcs, no spokes, no rays, no spikes, no notches, no broken segments, and no glow spreading away from it`
4. **不投影**：`it casts no shadow on anything behind her`

判定：出图里出现任何一条从环上伸出去的短线 = 第 3 段没生效。同族：光晕、魔法阵、召唤阵、装饰性边框。

## G59 侧向朝向在「坐着的人」身上仍然失效，必须用「看不见哪只眼」的否定句（126 实测，2026-11-07）

126 写 `turned towards the window, so we see her right side ... and we do not see her left eye`，出图**正面朝我们、双眼可见**。117 也栽过一次（`from the front, a little to her left` 出成背右三分之三）。

原因：坐姿 + 面向窗户是「人在看风景」的强先验，模型默认给你一张脸，因为脸是画面里最有信息的部分。

可用写法（三件一起给）：

1. 先否整体：`turned away from us towards the window, and her whole body is side on to us`
2. 再给一个**方向可验证的锚**：`the tip of her nose points at the right edge of the picture`（不给角度黑话）
3. 最后连否：`we do not see her mouth from the front, we do not see her left eye, and her face is never turned towards us`

判定：出图里能同时看到两只眼 = 失效。

## G60 带印刷的道具会自己长出文字，要么换成无字材质，要么就当文字图设计（126 实测，2026-11-07）

126 写 `wrapped in newspaper ... has no writing on it that can be read`，出图报纸上**满版假字**。否定句对「报纸」这个名字无效——名字自带的先验太强。

两条出路：

- **换材质**：`wrapped in plain brown kraft paper ... a flat warm brown with no printing and no writing of any kind on it`（本次采用，一次成功）
- **当文字图设计**：真要文字，就按 G13 给独立 text item + 共面句 + 行跟随表面，不要指望 caption 里顺手一提能出干净的字

同族：书页、信件、海报、票据、招牌、罐头标签、路牌。

## G61 光环画不对不是写法的错，是角色名自带的官方设计（126、127 第三次实测，2026-11-07）

连续三版写了「一个细单圈、内部全空、无第二圈/无弧/无辐条/无射线/无尖刺/无缺口」，出图三次都是**同一个带箭头与同心弧的环**。原因不是词表不够狠，是 `aru (blue archive)` 这个角色名把她的官方光环一起带进来了——模型画的是设定稿，不是我的描述。

三条出路，按代价排：

1. **接受它**：官方光环本身是成立的图形语言，画面不吃亏（本次两条最终都留着）。
2. **改名淡化先验**：只写 `rikuhachima aru` 不带作品名，光环会退化成普通圆环（未实测）。
3. **显式否认官方形**：`not the ring with arrows she usually wears; this one is a plain thin circle`（未实测，风险是模型两个都画）。

同一族：角色自带的角、兽耳、尾巴、眼睛纹样、校服徽章、领结形状——**凡是角色名带得动的东西，caption 里写得再细也只是「补充」不是「覆盖」**。想改，先降角色名的权重，或者干脆不用角色名。

## G62 明度的上限写在 summary 就压住全图，改 character 块无效（127v2 实测，2026-11-07）

127v1 太暗（mean .209 / p99 .716 / bright .008）。v2 我把「脸是最亮、比布高两档、布永不超过她脸颊」写进了 character 块，出图几乎一模一样（mean .222 / p99 .767 / bright .011）——因为 summary 里那句 `the remaining thirty, and none of it reaches white` 是**全图的闸门**，它先定了顶。

v3 改法（四处，全在 summary 与场景块）：

1. 删掉「none of it reaches white」，换成**点名两个面**：`Two things in the picture are the lightest values in it and they come within one step of white and stop there: the flat of her cheek facing the flash, and the front of her white collar.`
2. 三档重新分配（暗 50 / 中 20 / 亮 30）
3. 顶棚写「全图最暗且不借光」（暗锚要有具体物）
4. character 块只补一句「比布高三档」，不再承担曝光职责

规则：**曝光与明度分档只写在 summary**；character / object 块里写的是「这块比周围亮几档」这种局部关系。写反了就是白改。

**G62 补｜分档百分比会被精确执行，但「亮」不等于「接近白」（127v3 实测，2026-11-07）**

v3 写了「暗 50 / 中 20 / 亮 30」，实测 dark **.500**（一分不差）、mid .486、bright .015。也就是说：**三档的百分比是硬指令，会被照做；但模型把「亮」理解成 .45 上下就算交差**，因为中调值域本身很宽（.25–.75）。整图因此仍然偏暗（mean .215），只有脸和领口两个被点名的小面摸到 .96。

规则：想让画面真的亮起来，光分配面积不够，必须再写一句「**这一块里有多少比例是接近白的**」——例如 `a fifth of her lit cheek is within one step of white, and nowhere else in the picture is`。否则「亮部 30%」会老老实实变成「中调 30%」。

反过来：只要写了这句，面积就必须小（点名到「一个面 / 一条边」），否则整图会过曝。

## G63 给「一群人」名词组，模型会先把人排好再上色；要无脸就写「背对我们」（129 号实测，2026-11-07）

**现象**：129 号写「三个男人站在她身后，每个人的脸都读不出来，没有一只眼睛、没有一只手能指认，他们就是一整块平黑」，出图是**三张清清楚楚的脸**，中间那位还抱着胳膊、整条前臂被光照亮，抢走了她的位置。同一种失败在 121（漏光被画成实体）、113（洗衣机里的衣服）上都出现过：**先验一旦被名词组激活，否定句只是补充，不是覆盖。**

**机制**：`three men standing in the dark` 是一个**会召唤人脸的名词组**。模型先按「人」的图式排好三个人（头、肩、脸），再按光照上色；「没有脸」这句只作用在最后的细节层，压不过图式。

**正解 —— 换结构，不是加否定词**：让那个人**背对我们**。背对的人从构造上就没有脸，不需要任何否定句：

```
One man stands behind her and to her right, turned away from us: we see his back and the back of his head,
and his face is on the far side of his head, where it cannot be seen from here at all.
```

实测 129v2：**一张脸都没出来**，只有背影与肩线，其余全是黑。这句话一次就成立，不依赖任何 no face / no eyes / not readable。

**配套三件**：
1. 人数写成一个，不写「三个人」——数量是图式的一部分，写三个就排三个。
2. 附属物要一起清掉：原文「前臂与刀柄」在改成人背后仍会召出武器，必须同步删掉，并把那处光改落到**没有器官的物体**上（墙边矮石台、地上一级台阶、桌沿）。
3. 用「他是唯一另一个人」收口：`He is the only other person in the picture and there is nobody standing beside him.`

**同族清单**（都改成「结构上没有」而不是「写了没有」）：人群 / 围观者 / 士兵 / 舞者 / 观众 —— 一律写背对、侧背影、或被物体挡住整个上半身；要留多人就必须接受他们会有脸。

## G64 提示词太长，本身就会把人物画大（用户判断，2026-11-08；131 号做对照实验）

用户原话：「其实我告诉你是因为什么，还是因为你的提示词太长了」，以及更早的「也许你按之前极简版那样写就不会有这种问题了」。

**这是对 115–130 全部尺寸实验的另一种解释，而且比我的解释更可能对。** 我的解释是「她站在谁旁边就按谁画」（G47/G54/G57）；用户的解释是「描述越多，模型越把她当主体画」。两者不冲突，但后者解释力更强，因为它同时解释了另外三件我一直归因于别的规则的事：

- 130 写 19.5% 出 48%、129 写 36% 出 52.7%、128 写三分之一出 44%——三张的提示词都在 1200–1500 词；
- 115 的走廊是唯一压到 28% 的，而它的 caption 只有一段；
- 118v1（857 词）出 46.4%，118v4（970 词 + Layout）出 21.5%——同一题材，词数降下来、人也就小了。

**机制假设**：Layout 里 character 块的 caption 越长，模型越把它当成「这张画的主题」，于是按「主体该占多大」的图式去画，bbox 退化为位置标注。反之 caption 短，它只读到「一个人在雪里」，就按「远景里的一个人」去画。

**做法（暂定纪律）**：
1. 先按 200–300 词写，出图看尺寸；尺寸对了就不要再加字。
2. 加字只允许加在**明度三档的数量**和**光的落点**上；人物块永远保持最短。
3. 人物块优先级：名字 → 朝向一句 → 位置一句 → 比例一句 → 收工。外观细节只在「换了角色认不出来」时才补。
4. 判断依据不再是「规则有没有写全」，而是「这句话删掉画面会少什么」（G38 同族）。

**131 号是对照实验**：与 130v2 同场景、同 5 个 item、同 bbox（她 16.9%、机器 27.3%），只把提示词从 1406 词砍到 **214 词**。若出图她仍在 20% 上下，则词数为主因；若又回到 45% 以上，则主因仍是参照物吸附。
### G64 结论（131 号实测，2026-11-08）：用户判断成立，词数是尺寸的主因

131 与 130v2 同场景、同 5 个 item、同 bbox（她 16.9%），只把提示词从 **1406 词砍到 214 词**。出图实测：她头顶 y≈465、鞋底 y≈640 → 高 175px = **17.1%**，即 **1.01×**，几乎逐像素执行。

| 编号 | 词数 | bbox 写 | 实际 | 放大 |
|---|---|---|---|---|
| 118v1 | 857 | — | 46.4% | — |
| 118v3 | 700 | 16.6% | 43.0% | 2.60× |
| 118v4 | 970 | 13.7% | 21.5% | 1.57× |
| 117 | 1152 | 17% | 41.5% | 2.40× |
| 122v1 | 1219 | 26.4% | 78% | 2.94× |
| 128 | 1516 | 33% | 44% | 1.33× |
| 129v2 | 1309 | 36.1% | 52.7% | 1.46× |
| 130 | 1424 | 19.5% | 48% | 2.40× |
| 130v2 | 1406 | 16.9% | 48% | 2.40× |
| **131** | **214** | **16.9%** | **17.1%** | **1.01×** |

**所以 G46/G47/G54/G57 那些「放大倍数」现象，主因不是场景地面强度、也不是参照物吸附，而是词数**：1000 词以上一律放大 1.3–2.9 倍，200–300 词落在 1.0×。地面强度与参照物只是叠加项。


## G66 角色不带光环就不要写光环；角色自带的部件先查设定再落笔（用户 2026-11-08 指出）

**G61 讲的是「角色名带得动的部件改不掉」，G66 讲的是反面：角色本来没有的东西，不要因为同厂牌别的角色有就顺手写上。**

用户原话：「灵梦脑后是没有光环的，不像蔚蓝档案角色」。我在 148 号（悲悯碎镜）里写了「头顶一个比胸口光更弱的细环」——那是把蔚蓝档案（Blue Archive）角色的标配（每人头顶一个光环）当成了通用习惯，套到了东方 Project 的角色上。同类错误：给没有兽耳的角色写耳朵、给没有角的角色写角、给普通制服写校徽。

规则：

1. **落笔前分两步查**：① 这个角色属于哪个作品；② 那个作品里「人人都有」的部件是什么（蔚蓝档案＝光环，东方 Project＝无光环、无兽耳、无尾巴）。
2. **不确定就不写**。少写一个部件只是画面朴素，写错一个部件是**角色错**，而且它会被画在最容易被看见的位置（头顶）。
3. **`original character` 或者自己设计的角色可以任意加**，一旦写了具体角色名，就按该角色设定走。
4. 同族禁忌：不要把 A 作品的通用设定当 B 作品的默认值——光环（BA）、兽耳（兽娘系）、吉祥纹样、校服襟章都属于「作品级的通用件」，跨作品一律不继承。

自查：写完 character 块，把**所有不在该角色设定里的部件**逐个数一遍，全部删掉。

## G67 细小的东西不给 bbox，只写进它所在那块的 caption（用户 2026-11-08 指出）

用户原话：「不用给硬币那种东西写 bbox，他会变得很大，一些细小的东西也是一样，不要给 bbox，有这个意思就可以了」。

153 号我给了一枚掉在碎石上的硬币、给签子、给纸扇，全是独立 item。**bbox 是「这块区域要画成这个东西」的强指令**——它同时规定了位置和范围，模型会把整块 bbox 填满这个物体，于是硬币被画成一块巴掌大的金属片，签子被画成一根棍。

规则：

1. **判据用面积**：占画面 **2% 以下**的东西一律不给 bbox，写进它所在的地面/台面/桌面的 caption 里，一句话带过（`one dropped coin lies on the gravel, throwing a small hard shadow`）。
2. **必须独立成 item 的情况只有三种**：① 它是故事证据物（她要捡的东西、她手里的东西）；② 它要被单独打光（一束光落在它上面）；③ 它和主体有接触（手扶、脚踩）。这时它不是「细小物」，是道具。
3. **同族清单**：硬币、签子、笔、钥匙、纽扣、耳环、水滴、烟头、纸片、花瓣、米粒、螺丝、气泡——全部只写进所属物体的 caption。
4. 需要它「有存在感」时，改用**相对尺度**：`a coin the size of a fingernail, lost among gravel the size of beans`，写在碎石块里，不给框。

与 G31（亚像素纹理写不出来）、G47（名字即放大）同族：**bbox 只管位置不管大小，但它会强制「把这块画满」**，所以小块 + 小物件 = 放大事故。

**新纪律（取代之前的加法式写法）**：
1. 默认按 **200–320 词** 写。尺寸对了不加字。
2. 加字只准加在**明度三档的数量**和**光的落点**上；character 块永远最短。
3. character 块五句封顶：名字 → 外观两个特征 → 朝向 → 位置与距离 → 比例一句。
4. 只有「含文字的海报 / 多格 / 需要精确物件关系」才允许上千词（官方 Layout 的本意场景）。

---

### G68 剪影图不要写「几成近黑」，要写「天空占多少」+「暗部里多少真的到黑」（164 号实测，2026-11-08）

164 号写「roughly six tenths of the picture is one flat near black」，出图实测：

| 指标 | 实测 | 说明 |
|---|---|---|
| 真正 <0.10 的面积 | **35.9%** | 写了六成，只出三成六 |
| 天空 | 只占顶部 **1/8** | 写「四成天空」，被压成 12% |
| 暗部 20% 里的 sat | **0.374** | 暗部确实饱和，这句成立 |
| lit / shadow | .311 / .376 | 暗部比亮部更饱和，方向正确 |
| p99 | **.994**（>0.90 占 3.5%） | 太阳光斑打满，写「停在白前一步」没做到 |

结论两条：

1. **「几成近黑」会被当成「几成暗」执行，而暗可以是饱和的深蓝，不一定是黑。** 想要真黑面积 X%，要写 X ÷ 0.6。或者更稳：直接写「天空占画面顶部多少」——这个数字被遵守得更好。
2. **剪影图的暗部饱和是成立的，且这是这类图的正解**（`lit < shadow` 是合法结果，不是事故）。参考图暗部 sat 0.619、早期出图只有 0.264，这次 0.534 / 暗部 0.374。**要写的是「全图最饱和的东西是那块暗的天」**，一句就够。

同族：任何「大面积单一色」的图，不要用比例形容暗部，要形容**那块暗是什么颜色、饱和到什么程度**。

---

### G69 low key 图里「亮」等于中灰，必须给一处「接近白」的锚并写明比例（165 号实测，2026-11-08）

165 号雨窗写「the only genuinely bright points are the wet highlights inside the raindrops」，出图实测：

| 指标 | 实测 | 判据 |
|---|---|---|
| mean | .167 | 低长调成立 |
| dark | .513 | 暗部过半 |
| **p99** | **.484** | **全图最亮处只有中灰** |
| **>0.90 的面积** | **0.00%** | **一处接近白都没有** |
| bright | .001 | 无高光 |
| sat | .423 / 暗部 .429 | 统一蓝灰，尚可 |

**这是 G62 补的反面案例**：写了「唯一亮源是雨滴高光」，但整张图被压成中灰，雨滴的硬亮点一个都没出现。low key 图里模型把「bright」理解成 .45 上下就算交差，跟 G62 补说的一样——但这次连 .45 都没到，因为它同时被「low key overall」压住了。

修法三件：

1. **点名到具体物体 + 给比例**：`the single wet highlight on each drop, and together they cover less than one percent of the frame, is the only thing in the picture that comes within one step of white`
2. **给一个绝对锚**：`one small hard white point, no bigger than a pinhead, on the nearest drop`——比「bright」有效得多。
3. **红线**：low key 图的 **p99 低于 0.70 就等于没有高光锚**，这张图会读成「阴天中灰」而不是「夜晚」。0.70–0.85 是安全区。

---

### G70 无人静物：影子会画，但画成软浅影；木纹细度会改写尺度（166 号看图修正，2026-11-08）

**先记一次误判**：只看数值（dark .003 / <0.10 面积 0%）时我判定「影子一个都没画」，换到多模态模型看图后确认——**影子是画了的**（杯子朝右拖影、火柴盒朝右拖影），只是软、浅、面积小。**数值能证明「暗部总量不足」，不能证明「某个东西没有」。** 与 G53 同族。

166 号实测 + 看图：

| 指标 | 实测 | 看图核对 |
|---|---|---|
| mean / dark | .618 / .003 | 整张高调，没有一个真正的暗锚 |
| 红分量面积 | 59.8% | 桌面被画成暖橙棕，抢掉了火柴盒红面的「唯一饱和色」地位 |
| 影子 | 有，但软浅 | 杯子与火柴盒各朝右拖一条浅影，没有硬度也没有纵深 |
| 主体尺寸 | — | **木纹太细，整张读成特写**，于是火柴盒看起来是「正常大小的火柴盒」，不是「极小主体」 |

三条真规则：

1. **「极小主体」靠的不是小数字，是周围的参照物里有没有一件「正常大小」的东西。** 166 号给了白瓷杯当参照，结果两个都读成正常大小。想要「小」，要么**只给一件东西 + 一片没有任何纹理的空面**（纹理越细，尺度越读成特写），要么用**裁切尺**反向（G22 同族）。
2. **影子的硬度要写，不能只写「影子是最暗的」。** 正解：`each object lays a shadow with a hard edge and no penumbra to speak of, twice as long as the object is wide, and the wood inside that shadow keeps its grain but drops two full steps in value`。
3. **中性大面要写低饱和 + 不许有暖色倾向。** `a low saturation greyish brown, closer to dust than to orange, with no red in it anywhere`。**「暖蜜色木」= 高饱和橙红**，这条已两次实测（116 号 sat .062 发白、166 号 59.8% 橙红）。

**无人图的必写四项**：① 一个硬边暗锚（点名形状与面积）；② 一个高光锚（点名物体 + 到白前一步）；③ 中性大面写低饱和且点名「里面没有红」；④ 一件公认尺（G26）。

---

### G71 「cut like a blade」治不了投影；影子要写「边缘在哪突然停」+ 绝对明度对照（166 v2 实测，2026-11-09）

166 v2 写了 `each cut like a blade, with no gradient at all and no penumbra to speak of`——这是 G6 的标准措辞，lint 也认。看图结果：**杯子后面是一大片柔和的椭圆渐变影，边缘完全虚掉**；火柴盒的影稍硬一点，也远不到刀切。实测 dark 只有 .021（目标 ≥0.08），<0.10 面积 0.1%。

**结论：`cut like a blade` 只对「光落在物体上的明暗交界」有效，对「物体投在地上的影子」无效。** 影子是另一套机制，要三件事：

1. **写边缘在哪突然停，不写边缘硬**：`the edge of that shadow stops dead in a straight line halfway across the table, and on the far side of that line the surface is back to its full value in the space of a single finger's width`。
2. **给绝对明度对照，不给相对档位**：`inside the shadow the surface is the darkest value anywhere in the picture, darker than the wall is light`——「掉两整档」没有基准，模型不知道从哪掉。这跟 G32「只能有一个最亮」是同一套机制：**暗端也要有一个唯一的「最暗」。**
3. **影子的形状要能对上投射物**：写 `the shadow is the same shape as the cup and its handle, lying flat`——不写形状，模型给一坨椭圆。

### G72 删纹理不能删到零：「no visible grain」会变成没有质感的平板（166 v2 实测，2026-11-09）

166 v2 为了治「木纹太细导致整张读成微距」，写成 `matte, low saturation greyish brown, closer to the colour of dust than to wood, with no visible grain, no ring marks, no gloss`。看图：**桌面变成一块均匀的灰色纸板**，既不像木桌也不像水泥台，材质信息归零。同时 sat 从 .288 掉到 **.105**（目标 ≥0.16）。

正确做法：**不是删掉纹理，是把纹理的尺度改大**。`a fine matte texture that only shows where the light skims across it, in wide soft patches about the width of a hand rather than fine lines`——**「手宽的大片」而不是「细线」**，尺度一变，整张就不读成微距了。同时给饱和一个下限：`a warm grey that is still recognisably wood, only its saturation pushed almost all the way down`。

### G73 当参照物的东西自己也会被放大成英雄道具（166 v2 实测，2026-11-09）

166 v2 给茶杯 bbox 11%W × 15.6%H，出图实测约 **25% × 25%**（放大约 2.3×）。它一放大，整张图的「极小主体」就垮了——因为观众先看见一个巨大的杯子。

**参照物要选「不会被放大」的东西**：墙面的踢脚线高度、地砖格数、门框宽度、桌沿厚度——这些是**结构构件**，模型不会把它们当英雄道具。**任何可以单独成物的东西（杯子、瓶子、椅子）一旦写进提示词就会被放大。**

166 v2 里同时成立的：桌面暖橙被彻底压掉（红分量 59.8% → 0.59%）、火柴盒相对杯子约 1/3 高（尺度比值对）、红面是唯一饱和色、墙桌交线正好在上三分之一。

---

### G74 满幅大面积块的明度必须写在它自己的 caption 里，不能只靠 summary 的「Mid tone」（166 v3 实测，2026-11-09）

166 v3 删掉杯子后，桌面块 bbox 占了 71% 画幅，caption 只写了颜色（pale tan grey）和纹理，没写「它有多暗」；summary 里写了 `Mid tone overall`。出图：**桌面成了一张近乎白的浅木纹板**（hex `#fbede5`–`#fcf1e8`），mean **.657**、dark **.002**、p99 .973、nw .0497。比 v2（.491 / .021）更亮。

**结论：summary 的 `Mid tone` 是总闸门（G62），不是分块指令。一块占画幅七成以上的面，必须在它自己的 caption 里给出值。** 写法：`this surface sits at the value a middle grey sits at, and it does not lift anywhere: in the brightest part of it the wood is still clearly darker than the wall above`。

**同族陷阱**：`tan` 是浅黄褐，写 `pale tan grey` 等于点了一份浅色。要暗就得明说「比中灰暗一档的褐」，不要靠 `tan` 自己变暗。

### G75 纹理的先验绑在名词上，不与形容词合作（166 v2 + v3 两次实测，2026-11-09）

v2 写 `no visible grain` → 变成无质感平板。v3 改写成 `The grain only shows where the light skims across it, in wide soft patches about the width of a hand rather than fine lines` → **出图仍是密集的横向细纹**，读起来像木纹贴图或印刷板。

**两次都失败，说明 `grain` / `wood` 这两个词自带「细平行线」的先验，形容词改不动它。** 同族 G28（命名即放大）——这里是「命名即定形」。

要真的换尺度必须**换名词**：不说 grain，说**拼接**——
`the top is made of broad planks of unequal width, and the joins between them are the only lines on it; there is no fine texture anywhere on the surface`。

**「线」的数量越少、越粗，整张越不读成微距。**

### G76 结构构件当尺子，必须带一个可数的重复单元（166 v3 实测，2026-11-09）

G73 说用桌沿厚度当尺子（结构构件不会被放大）。v3 照做：`its thickness is exactly the height of the matchbox standing on it`。出图：盒高约 130px，桌沿厚度约 60px，**差 2 倍，对位句完全没执行**。火柴盒实际占 22% 宽 × 13% 高（bbox 给的是 7.2% × 7.8%，放大 3×）。

**原因是「桌沿厚度」是一条边，模型没有长度信息，无法换算。** 尺子必须带**可数的重复单元**：
`the tabletop is made of three planks, each plank exactly as wide as the matchbox is long`、`along the front edge a row of nail heads sits one hand's width apart`。

「一条线的粗细」不可数，「一排等距的东西」才可数。

### G71 补 · 影子硬度写法有效，但明度锚不能写「全画最暗」（166 v3 实测，2026-11-09）

v3 用 G71 的写法（`stops dead in a straight line` + 形状对得上投射物），出图：**影子确实硬了**——一片带尖的清晰影子向右延伸，不再是大椭圆渐变。**方向正确。**

但它的颜色仍是浅灰紫，因为 `the darkest value anywhere in the picture` 是**相对量**：整张图都亮的时候，「最暗」也亮。

**修法：把暗端锚在一件确定深色的物体上。**
`inside the shadow the wood is the same value as the burnt black head of the match beside it`。

同族：亮端也一样，「唯一最亮」要靠一件确定亮色的物体，不能靠 `brightest` 这个说法。

### G77 正俯视成立的条件（167 号首次成功，2026-11-09）

B 组机位只到「俯拍 60 度」，正俯视此前从未成功。167 号一次做成，配方三件：

1. **一句话把画框的四个边都交给地面**：`The whole frame is tatami floor seen from straight above, and it runs past every edge of the picture`。
2. **三项否认缺一不可**：`no horizon anywhere in the frame` / `no wall` / `no ceiling and no furniture edge is visible anywhere`。少任何一项，模型都会补一面墙当地平线，机位立刻退回 60 度俯拍。
3. **光源不许以「灯」或「天」出现，只以「地面上的一块亮平行四边形」出现**：`a single bright parallelogram with four straight edges`。正俯视里没有天空可以给你放太阳，光只能落在地上。

附带两条：人物躺姿**必须沿对角线**（横图里竖直躺会顶天立地，斜躺才装得下）；影子在正俯视里是**贴着她的一圈硬边形状**，不是拖出去的长影，写「四周一圈硬边、轮廓就是她的身体和屈起的膝和裙摆」。

### G78 布边 / 饰条 / 镶边类名词自带宽度先验，写「细」改不动（167 号实测，2026-11-09）

我写 `a narrow band of dark cloth` + `thin, near black`，出图是一条 **15–20px 宽的蓝紫色粗条**（真实榻榻米 heri 约 3–4cm，在 90cm 席宽里应是 3–4%，画面上约 5px）。同族 G75：**宽度先验绑在名词上，形容词压不住。**

三条出路，按可靠度排序：

1. **不给名字，只写缝**：`the mats meet along straight seams, and each seam is a dark line no thicker than the straw beside it`——把「条」变成「缝」，宽度就没有独立体量了。
2. **给可比的细物**：`a line no wider than a fingernail`。
3. **接受它是条，改设计**：把布边当成构图元素（细黑网格），而不是当黑锚的细线。

顺带：**细黑线当黑锚和 sat 下限直接冲突**——167 号 sat 只有 .134（目标 ≥.16），因为全画唯一有色的东西就是那条细布边，面积太小。要同时满足，得让**受光的大面本身带色**：`the lit straw is a saturated yellow green, not a grey green`。

### G79 当尺子的物体必须自己拥有 bbox（167 号实测，2026-11-09）

我写 `She is a little shorter than one mat is long and she lies across two of them`——句子本身完全符合 G54/G76。但**席是地面块的一部分，没有独立 item、没有 bbox**，所以模型没有可换算的像素量。结果：她 bbox 给 60.5% 高 → 实际 73.8%（1.22×），宽 500px → 实际 845px（1.69×）。

规则：**任何要参与尺寸换算的物体，必须独立成 item 并给 bbox**，哪怕它只是地上的一块。反例的代价比「多一个 item」大得多。

---

### G80 地上的光斑默认来自「带窗棂的窗」，会画成一格格分离的矩形（168 号实测，2026-11-09）

168 号写 `an elongated shape with two long straight sides and two soft ends`（一条拉长的亮斑、两条长边笔直、两端渐虚），出图地面上是**一组排成网格的分离亮矩形**——模型把「笔直长边」读成了窗棂，把一块光斑拆成六七个格子。

规则：写地面光斑时，**必须显式否认窗棂与第二块光斑**：

> the light arrives through a single opening with nothing across it, so the patch on the floor is one continuous shape, with no bars running across it, no second patch beside it, and no grid of any kind.

同族先验（都在「否认具体结构」这一类）：G42 路面自带画线、G44 洗衣机里有衣服、G27 水面必有涟漪、G28 命名的东西会被放大。**凡是模型见过的「现实搭配」，都不能靠形容词否定，只能显式点名那个结构并说它不在。**

### G81 「不超过拇指宽」这类身体部位比对物对水花、烟、雾这类无定形物无效（169 号实测，2026-11-09）

169 号想控制砸地水花的大小，写了 `no crown is wider than a thumb`，出图最近的一个皇冠占画面宽度约 **16%**（应有 2–3%）。

原因同 G26：**比对物必须在画面里出现，或者必须是画面内某件东西的属性**。拇指不在画面里，就没有锚。

三条可行的替代：
1. **用画面内已有物的尺寸做锚**：`each crown is no wider than the painted line is thick`（画线在画面里，且它自己有条明确的宽度）。
2. **用「数量 + 分布」代替尺寸**：`there are about two dozen crowns scattered across the whole puddle, and they are all about the same size`——同尺寸的一群小东西比一个大东西更容易被画对。
3. **把最大的那个也压下去**：`the largest crown in the picture is still small enough that a row of eight of them would only just span the painted line`。

### G82 每条交付第一行必须写明尺寸，否则 bbox 全部错位（168 号实测，2026-11-09）

168 号的 JSON 写的是 1024×1536 竖图，但交付回复里没有把尺寸说清楚（那条回复中途断了），用户按默认的 1536×1024 横图渲染。结果：**bbox 是按竖图排的，人跑到最右边、光斑跑到画面中间偏右，整张构图和我设计的不一样。**

规则：交付的第一行固定写 `建议尺寸：W×H 横/竖图。` 并给一句理由。JSON 里的 `width`/`height` **不能替代**这句话——用户是照着回复里的那句话去设参数的。

---

### G80 补：地面光斑的四重否认全部失效——问题不是「没有窗」，是「这个形状没有出处」（168 号 v2 实测，2026-11-09）

168 号 v2 把 G80 的正解句全写上了：`no bars, no mullions, no pane edges, no grid of any kind, no second patch anywhere on this floor`，summary 里再写 `no window in this picture at any point, no pane and no bars`。出图地板上的光斑**仍然是一块 3×2 的窗格投影**，横缝竖缝一条不少。

原因：**否定句解释不了「光斑为什么是这个形状」。** 模型必须给光斑一个出处，而它默认的出处永远是「透过窗」。你说不是窗，它还是会画窗的形状，只是嘴上不承认。

正解：**给光一个能决定形状的具体来源，让形状从来源里推出来。** 屋顶塌了一条缝，缝是窄的、长的、直的，于是光柱窄而长，地面光斑自然是一条长条：

> the light comes through one long crack where the roof has split, and the crack is narrow and straight; it is the only break in the roof anywhere, and the light that comes through it is one narrow blade rather than a spread of separate rays.

同族：G42 路面画线、G44 洗衣机里有衣服、G27 水面必有涟漪、G28 命名的东西会被放大——**凡是模型见过的「现实搭配」，只能改它的出处，不能否认它的存在。** G80 原文的「显式否认」只够治「多出来的第二块」，不够治「形状」。

### G84 大面积水面自带俯视先验，写「低机位贴水看」会被翻成俯拍（169 号 v2 实测，2026-11-09）

169 号 v2 写 `The camera is low to the water, about a pace from the near edge of it`、`The camera is low, close to the water`，并且给水洼的 bbox 只占画面下 40%。出图是**斜俯视**：水洼横在画面中间，上下两边都是路面，等于人站在岸上往下看。

原因同 G28：**「水面」这个词自带「从上往下看才能看见水面」的先验**。你写「低机位」，模型听懂了机位，但它更相信「水要看得见」这件事，于是把机位抬高到能看见水为止。

三条出路：
1. **把水面压成一条横带**：占画面高度 **不到三分之一**，其余全是柏油或岸。它没法被读成俯视，因为没有足够的水面面积去「看」。
2. **把机位锚在倒影的立面上，而不是水面上**：`we are looking at the reflection almost edge on, so the reflected bars stand up in the frame rather than lying flat in it`——一旦倒影在画面里是「竖起来的」，机位就被钉死在低处。
3. **给一个只有低机位才看得见的东西当前景**：`the near kerb cuts across the bottom of the frame at the height of our knees, and it hides the first hand's width of the water`。

---

### G80 补二：给光一个「会产出正确形状」的出处，一次就成（168 号 v3 实测，2026-11-09）

168 号 v3 把「屋顶裂了一道缝」写进墙体块：`the roof has cracked apart along one line, and that split is the only break in the roof anywhere: it is narrow, it runs straight`，光柱写 `one narrow blade, not a fan`。出图：**屋顶正中真的裂开一道口子**（能看见破损的木板断口），光从那里落成一把窄刃，落到地面直接接上光斑，**窗格彻底消失**。

关键判据（这条决定「板缝」和「窗格」的区别）：出图的地面光斑里确实还有横向亮条，但那些条**和地板板缝同向、平行于光斑长轴**，所以读成「光落在有起伏的木板上」。真正的窗格一定是**垂直交叉的网格**。→ **同向条带合法，交叉网格非法。**

### G86 极低 key 有下限：dark 超过 70% 就变成「黑屏里一束光」（168 号 v3 实测，2026-11-09）

168 号 v3 实测 mean **.134** / dark **.759**，比 v2（mean .206 / dark .616）更黑。看图：暗部几乎吃掉整张，地板只剩贴着光斑的一小条，其余全是黑，画面读起来像「一块黑底上打了一束光」而不是一个房间。

原因：为了把光「衬出来」，我把墙、地板远端、屋顶全部写成 near black，三层叠加。

规则：**low key 图要写「暗部里有多少不是纯黑」**，而不是只写「多暗」。正解句：

> away from the light the room is dark but not empty: the wall behind her sits about three steps above black, the boards in the middle of the floor about two, and only the far corner goes all the way down.

对照：dark 目标区间 **0.42–0.65**；超过 0.70 就不是 low key，是 underexposed。

### G87 倒影必须被水面上发生的事打断，否则读成「躺在水上的实物」（169 号 v3 实测，2026-11-09）

169 号 v3 的琥珀反光按「断成六段短横条」写，出图确实是一叠错开的横条——但它**在水面上纹丝不动**：涟漪从它两侧绕过去，边缘干净利落，而且条里还长出了字，整块读起来像「一块发光的招牌掉在路上」，不是水里的倒影。

规则：倒影除了「形状」，还必须写它**被水破坏**：

> the bars are not clean: where each ripple ring crosses them the amber wavers and breaks, the edges of the bars are torn rather than ruled, and the whole stack sits one step behind the crowns that stand in front of it.

三件：① 涟漪穿过时它要抖、要断；② 边缘是「撕开的」不是「画出来的」；③ 水花要站在它前面（前后层次），它才算「在水里」。

### G88 「湿柏油」被写成墨绿时，是「湿」这个词在拉草地（169 号 v3 实测，2026-11-09）

169 号 v3 写 `a greenish black`，出图柏油绿得像深绿地毯。`greenish` 单写会勾来植物绿。

正解：把绿绑在**城市表面**上——`the colour wet tarmac goes at night, a desaturated blue black with no green in it at all`。宁可否认绿，也不要主动提绿。

---

### G84 补：低机位的水面场景里，「画面顶部的立面」会把机位整个拉高（169 号 v4 实测，2026-11-09）

169 号 v3 的机位是对的（贴水、水面压成下部三分之一）。v4 为了满足 lint 关 7 的「场景朝向」，加了一句 `the row of buildings runs along behind the road with its faces turned to the road`，并把 `the lower storeys of the buildings stand dark and empty` 写进柏油块——**机位立刻翻成站在路边往下看**：柏油占了中间 60%，水面退到下部 40%，v3 好不容易拿到的掠射角全丢了。

原因：**只要画面顶部出现一条「立着的立面」（楼房、马路牙、店面、石阶），模型就按「站在地上看这排立面」来定机位**，而那个机位必然是平的甚至俯的。低机位要的是「画框顶部什么都没有」——只剩柏油往远处走，走进黑里。

两条纪律：
1. **低机位水面图不要写建筑、不要写马路牙、不要写台阶。** 顶部就是路面本身，一直走到黑。lint 关 7 的 G1 只在出现 `kerb`/`bench`/`counter` 这类词时才触发——**不写那个词，就不会触发**，不需要为了过关硬加一句朝向。
2. **要交代「这条路在哪」就用画外句**：`the road runs on out of frame in both directions, and whatever stands at its far side is above the top edge and never in the picture.`

### G86 补：dark 的百分比不是判据，「暗部里有没有可辨识的结构」才是（168 号 v4 实测，2026-11-09）

168 号 v3 dark **.759**，看图是「黑底上一束光」；v4 dark **.668**（仍高于 G86 定的 0.65 上限），看图却完全不闷——因为暗部里屋顶的椽、板缝、地板木纹、远处墙的竖缝全都读得出来，是「一个暗房间」而不是「一块黑」。

规则修正：**dark 只用来发现「是不是全平」，不能反过来当目标值。** 真正的判据是这三条：
1. 暗部里至少有**两层可辨识的结构**（168 v4：屋顶椽 + 墙板竖缝 + 地板木纹，三层）；
2. 暗部内部有**值的变化**（v4 的暗部 .08–.19 之间浮动，v3 是 .07 一片平）；
3. summary 里写的是「**什么东西在哪个暗档上**」，不是「暗部占百分之几」。

对照表：v3 mean .134 / dark .759 / 暗部值域 .07–.10（平）→ 闷。v4 mean .169 / dark .668 / 暗部值域 .08–.19（有层次）→ 通。**mean 提了 .035 就够了，关键是值域被拉开了。**

---

### G84 补二：掠射机位要靠「汇聚线」活着，写成「平行于底边」就变成正对平面（169 号 v5 实测，2026-11-09）

169 号 v5 把建筑和马路牙全删了（v4 的教训），机位仍然没有变成掠射——出图读成「正对着一整片路面」，柏油完全不走透视，几条横向亮带彼此严格平行，整张像一张平面图案。

根因是我自己写的一句：`One painted line runs across it parallel to the bottom edge`。**「平行于底边」＝主动取消了唯一的透视线索。** 只要画面里没有任何一条会汇聚的线，模型就按「正对平面」渲染，机位高低完全失效。

规则：**掠射机位必须有一条会收的线**：

> a painted line running away from us towards the top of the frame, narrowing as it goes, so that the road is much wider at the bottom of the picture than it is where it disappears.

三件配套：① 线要**走向画框深处**（不是横过来）；② 远处要**变暗**（`the tarmac darkens as it recedes and goes black before it reaches the top edge`）——用明度给纵深，不用立面；③ 地面上的横向结构（斑马线、减速带、接缝）**要么删掉，要么也写成往远处收**。

对照：v3 有楼面但楼面被画框裁掉、且线不是平行写的 → 掠射成立。v4 楼面写成「面朝路」的立面 → 翻成俯视。v5 全删但线写成平行 → 翻成正对平面。**三个版本的机位分别由「有没有立面」「线收不收」决定，跟「低机位」这个词本身无关。**

### G89 同一片水面上，涟漪要疏密不均，全铺满会读成装饰图案（169 号 v5 实测，2026-11-09）

169 号 v5 写了 `Rain strikes it all over: about two dozen splash crowns stand up out of it`，出图水面被同心圆**均匀铺满**，密度高到像一层印上去的花纹，水本身读不出来了。

规则：给数量的同时要**给分布的偏斜**：

> Most of the crowns gather in the near half of the water, and there are stretches of bare water between them where the surface is smooth and only the rain streaks cross it. Nothing about the pattern is even.

一句 `Nothing about the pattern is even` 比任何数量词都管用。

---

### G90 说「招牌」就会画字，否认句拦不住——要文字自由就先把名字去掉（169 号 v6 实测，2026-11-09）

169 号 v6 的倒影块写了 `The amber of the shop sign coming back off the water`，并且明确加了 `Nothing in the stack reads as a letter or a word`。出图：水里是一整块琥珀色的**可读英文招牌**，`ODDS AND ENDS` 清清楚楚。否认句完全无效。

同族：G28（命名带来形态）、G42（路面自带画线）、G44（洗衣机里有衣服）、G80（光斑自带窗棂）。**`shop sign` 这个名词本身就把「有字」带进来了，`nothing reads as a letter` 是在跟这个名词打架，名词赢。**

规则：**要零文字，就先别叫它招牌**。改成描述光的形状而不描述它的来源：

> the amber that comes back off the water here belongs to nothing in the frame: it is only light, broken into about six separate bars stacked one above the other, each shifted sideways from the one below it.

三个配套：① 不出现 `sign` / `shop` / `store` / `neon` / `board` / `banner` 任何一个词；② 不写 `letter` / `word` / `text` / `character`（写这些词本身也会勾字）；③ 把它写成「光」而不是「物的像」——`only light`、`the amber`。

### G84 补三：全幅都是路面时，画框顶部必须有「被裁掉的远处结构」，否则没有纵深（169 号 v6 实测，2026-11-09）

169 号 v6 按 v5 的教训把建筑彻底删干净（`There is no kerb, no step and no building anywhere in this picture`），并把画线改成往深处收。出图：**仍然是两条平行的横带**（柏油在上、水在下），画线没有收，整张没有纵深。

对照三版：v3 顶部有一排楼面**被画框裁掉** → 掠射成立；v4 楼面写成**面朝路的立面** → 俯视；v5/v6 全删 → 正对平面。**差别不在「有没有远处的东西」，而在「那个东西是不是完整地立在画面里」。**

规则：**要的是「画面顶端留 3–5% 的一点点远处结构，被上边缘切掉」，不是一整面墙。** 正解句：

> Along the very top edge of the frame there is only the bottom step of something: a dark horizontal edge about a twentieth of the frame high, cut off by the top of the picture, with nothing above it and no face to it. It gives the road its far end without putting anything in the picture.

一句话记：**顶部要有个「看不见全貌的边」，画面才有里面和外面。**

---

### G91 玻璃的「透射层 + 反射层」要各占一块 item，并写死「两层互不加白」（170 号实测，2026-11-09）

170 号一次成了大半，机制四件：

1. **透射层独占一块 item，bbox 铺满整块玻璃**（`[0,40,1536,760]`），caption 只写「玻璃后面是什么」——远处一盏湿路灯化成光团（`no filament, no bracket and no arm of it readable`，去名去结构，防止画成实体路灯杆）、**第二盏更远更小给距离**、雨丝「在灯前又在灯后，因为它们哪一个都不是：它们在玻璃外面」。
2. **反射层单独一块 item，只占玻璃上部一条横带**（`[880,0,1536,300]`），caption 写 **doubled**：`one copy bright and one copy a step dimmer and shifted down by the thickness of the glass`。实测两重都画出来了，第二重更暗更错开。
3. **两层互不加白的显式禁令**（本图最关键的一句）：`where the street is bright the amber is fainter, where the street is dark the amber is at its strongest, so the two together never add up to white anywhere`。没有这句，两层一叠就是一片糊白。
4. **倒影层写「软、薄、被看穿」**：`soft, thin and half looked through`，并让透射层的东西穿过去——`one lamp inside her hair and one lamp across her jaw`。这句让两层发生物理交互，而不是各画各的。

实测已成立的判据：两盏灯给了距离、琥珀双带都在、雨丝有前后歧义、two layers 分离清楚、sat .262（暖琥珀+暖白，没灰）、p99 .890（灯头当高光锚）、mid .607 / dark .326 电影感比例。

**一处已知偏差（可接受，不必修）**：character 块写得太完整时，模型会**补画一个实体的人**站在玻璃旁，而不是只画倒影。但这张的实体侧脸旁边紧挨着那重半透明倒影头影，两层关系反而更读得出来（「她看着自己映在玻璃上」）。→ 想要纯倒影就把 character 块砍到只剩「玻璃上那些软薄的形状」，否则接受并存。

**附带：擦拭区在整幅玻璃图里读不出来**。掌形清亮区 + 四道指痕都画了，但「区内比区外锐利一档」的对比撑不住——因为整块玻璃本来就有雾，锐利度差不够大。要这个动作成为主角，得把擦拭区做成画面里唯一有细节的地方（其余全部糊到只剩明度），而不是在整体清晰的画面上加一块更清晰的。

---

### G92 逆光图里，暖色必须落在「被主光照到的那块地上」，不能落在被逆光勾出来的轮廓上（171 号实测，2026-11-09）

171 号写：`the sodium of the lamp gives the whole foreground its one warm amber cast where it lands: the amber lies across the snow on their near side and across the tops of their shoulders`。

出图：肩上只有一道**冷白**轮廓亮边，雪还是蓝的，全图**没有一处暖色**。实测 sat **.202**，`lit .089 < shadow .198`——被照亮的部分反而更不饱和，光把颜色洗掉了。

原因：主光在他们的**背后上方**（逆光）。逆光只会给轮廓一条细亮边，而那条边的颜色由「光源本体 + 空气」决定，不是你写的琥珀。琥珀真正能落的地方只有一个：**灯头正下方、被光锥完整打到的那块地**。

修法：

> the sodium shows up in exactly one place: the round patch of snow directly below the lamp head, where the ground goes a deep amber that is the only warm colour anywhere in the picture, and the patch is less than half the width of the frame.

三件：① 只说一处；② 面积写死；③ 明说「全图唯一的暖色」在那一处。
自检：**画面里有没有哪一块地面正在被主光正面照到？** 没有，就不要写暖色——先改光位。

---

### G93 背人：两个人的 bbox 上面必须各留一块空，而且被背者的头要比背者的头高一整个头高（171 v2 实测，2026-11-09）

171 v2 把两个 character 的 bbox 叠得太紧：背者 `[195,540,535,1040]`、被背者 `[225,520,615,900]`——上面只差 20px，出图两个人**头叠成一块**：被背者的脸整个压在背者的头顶上，读不出「一个趴在另一个背上」，读成「一个头两个身」。

原因：两个 character 有 bbox 交叠时（104 号多人物接触的正解），模型会把「上边界」当成「两个人的共同顶点」去凑，谁的头先到上边界就算谁的头。

修法三条，缺一不可：

1. **被背者的上边界要比背者高出一个头的高度**：背者头顶写 y=540，被背者的头就要到 y≈420（约 120px，占画高 8%）。
2. **被背者的头要写「垂过哪一侧肩、垂到背者的什么部位」**：`their head hangs past the carrier right shoulder and down to the level of the carrier chest`——给了落点，模型才不会把两个头叠一起。
3. **两个人的脸各写「看不见」的方式**：背者 `we see her left profile`，被背者 `the face turned down and away so that it cannot be seen`；两个都写「看不见哪半边」比写「朝哪边」有效。

自检：**两个 character 的 bbox 上边差 < 画高 6%，就一定叠头。**

---

### G94 三色错位版画成立，但「低 key」没有物质支撑；暗部必须给一版专门的墨（172 号实测，2026-11-09）

172 号写「三色丝网，普鲁士蓝 + 朱红 + 土黄，无黑墨，low key」。出图：**错位三重色边完全成立**（她轮廓上有真的一条纯红月牙 + 一条纯黄月牙），sat **.597** 是历史最高；但实测 **dark .001 / mid .969 / p1 .170**——整张没有一处暗，全浮在中调。

原因：三版彩色油墨本身都很亮，`no black ink at all` 等于把暗部彻底交出去。**「low key」在这种印刷语言里没有落点。**

修法：**加一版专门印暗的副墨**，只承担阴影：

> a fourth plate printed in a near-black prussian that carries every shadow in the picture and nothing else: wherever the picture is dark it is this plate alone, and it prints no colour of its own beyond the blue black.

配套：这一版的暗值写死（`it sits below a fifth of the way up the scale at its darkest`），否则它会被当成第四种装饰色。

判据：彩色印刷题材出图后先看 dark 与 p1。dark < .05 且 p1 > .13 = 没有暗，加副墨版。

### G95 人物 bbox 必须包住头顶到脚，且不许和她自己站立的台面 bbox 交叠（172 号实测，2026-11-09）

172 号人物 bbox `[700,150,1190,760]`（头顶到腰），台面 bbox `[0,640,1536,1024]`——两块在 y 640–760 交叠 120px。出图：**她整个人是倒着的**，脚朝上、头朝下，被塞进台面上方那块空间里。

原因：交叠区域让模型把人物当成「台面块里的一部分」，于是它能用的空间只有台面上那一条横带；横带太矮，模型就把人旋转 90° 塞进去。

规则三条：

1. **character 的 bbox 必须从头顶一直包到鞋底**（哪怕腿被前景挡住，bbox 也要含进去）。
2. **人物 bbox 与「她站的地面/台面/桌面」的 bbox 不许交叠**——台面要挡住她的膝以下，就把台面 bbox 下移到她膝盖线以下，让遮挡发生在**深度上**而不是 bbox 上。
3. 需要「她站在台后、只露上半身」这种构图时，写**裁切尺**而不是让两块 bbox 交叠：`the counter cuts across her at the waist, so we see her from the waist up only`，台面 bbox 单独占下部横带，人物 bbox 落在台面之上那片空间里，两者边界刚好相接。

自检：交付前把人物 bbox 和地面/台面 bbox 画在一张纸上，两块只要有重叠面积，就一定出翻转或截断。

---

### G96 介质指令会被人物先验碾压：脸永远按它见过的画法画（172 号 v2 实测，2026-11-09）

172 号 v2 全文明写丝网版画的介质语言（`flat opaque ink` / `no gradient and no mixing anywhere` / `separate flat shapes rather than blurred copies`），出图：三版错位完全成立（她左肩一条纯黄月牙、头右后侧一条纯红月牙），但**她是一张完整的动漫脸**——眼睛睫毛嘴全有、发丝有渐变高光、轮廓有描边。

对照 113 号：网点（细小重复单元）画不出来；172 号 v1/v2：错位（轮廓级位移）画得出来，但**无描边平色（介质级）画不出来——被脸碾压**。层级：轮廓级效果 > 介质级效果。

规则：**介质语言要成立，必须把人物本身也写进介质语言**，只写背景的介质没用。正解句（写进 character 块）：

> She is printed like everything else in the picture: she has no outlines and no drawn lines around any part of her, her face is only the edges where flat inks meet, her eyes are single dark bands with no iris drawn inside them, and her hair is one flat dark shape with no strands and no highlights.

配套：介质色要写死值域，否则被拉向常见色（普鲁士蓝被画成天空蓝）：`a prussian blue so deep it reads almost black at night`。高光锚（裸纸近白）也要点名：`the bare paper shows as the brightest thing, one step short of white`。

判据：p99 < .70 且主体脸上有渐变/描边 = 介质指令未生效，先改 character 块，不是先加更多介质词。

---

### G96 补：脸的先验是最高优先级，连 character 块里的介质句也只能拆掉一半（172 号 v3 实测，2026-11-09）

v3 把介质语言写进了 character 块（`no outlines` / `face is only the edges where flat inks meet` / `eyes are single dark bands with no iris` / `mouth is absent`）。出图：**衣身、头发真的成了平色块**（无描边、无渐变、无发丝），蓝色回到深普鲁士蓝，但**眼睛仍被画成完整的动漫眼（虹膜、双眼皮全在），嘴仍在**。「眼睛」「嘴」这两个部位无论怎么否认，都会被画——否认句反而起了点名作用。

推论三条：

1. **肢体与毛发可以按介质语言画，五官（眼/嘴）画不成平色**——五官先验高于一切介质指令。要介质语言彻底成立，唯一可靠的办法是**不给脸出现的机会**：让人物背对、低头到看不见脸、或在暗部里只剩剪影（与 G63「要无脸就写背对我们」同源）。
2. **否认五官的句子会变成五官的点名**——`her mouth is absent` 大概率反而保证画一张嘴。写介质句时不要列「没有 X」，只写「她由什么构成」（正解句式：`her head is one flat dark shape, and no feature of it is separately drawn`）。
3. 本条适用范围：**任何「把人物画成 X 质感」的题材**（版画/像素/剪纸/雕塑）都会在脸上撞这堵墙；测这格时把「脸部保留细节」算作合法残留，不算题材失败。

172 号判读结论：**色分离（错位）成立**——三版位移、纯红纯黄月牙、残影全部可读；介质平色在背景/物体/衣着上成立，五官是合法残留。**像素与线稿两个子项未测**，同族风险（细小重复单元/轮廓线提取）。

---

### G97 像素画判死：「细小重复单元」是 MOSS 的死角，第三次证实（173 号实测，2026-11-09）

173 号按十六色掌机调色板写：`the pixel grid is the finest thing in the picture and it never varies, so every edge is a staircase of steps one pixel wide`，人物背对（绕开 G96 补的五官坑）。出图：**一张普通的低清蓝色插画**——人物有渐变光影、雨是半透明细划、地面有柔光池，**像素格完全没有出现**。数值判据：soft **.943**（全糊）/ strong **.005**（零硬边）/ p99 **.514**（无高光锚）。

判死。族谱：113 报纸网点 ✘ → 173 像素格 ✘。共同点：**要求整幅画面遵守一个「细小且全局统一的重复单元」**，模型的渲染通路不经过这个约束——它只认「介质的样子」，不认「介质的构造规则」。错位（172 ✔）和排线（174 ✔）能活，因为它们是**轮廓级/走向级**的指令，不是单元级的。以后凡是「halftone / pixel / dither / 网点 / 拼布单元」一类题材，直接引用本条判死，不再消耗轮次。

### G98 线稿成立：明暗全部来自疏密，一句「no filled area」就能立住（174 号实测，2026-11-09）

174 号写 `there is no filled area anywhere, no shading, no wash and no grey, and every value in the picture is produced by how densely the lines are packed`，配三件套：① 最暗=两组交叉排线吃到纸面几乎消失；② 水=横线间留纸、越远越密；③ 唯一留白=桥洞那头（稀疏线 + 两条向上收的斜线）+ 四周排线最密。出图全部成立：dark .308 / p99 .780 / strong .375 / soft .288。

要点：① 高光锚落在**纸白**上而不是白颜料上，是线稿的物理本质，写「comes within one step of the bare buff of the sheet」即可；② 人物背对（G96 补）再次避开五官；③ G84 补二的「会收的线」在纯线稿里同样有效（运河向桥洞收窄）。

---

### G83 可坐物比姿势词强势（B11 的独立编号版，2026-11-09 归并）

画面里只要有台子、箱子、台阶、台阶沿，人就会被放上去坐或靠，**姿势词打不过它**。这不是「她没有要坐」，是模型看到可坐面就自动安排人坐下——因为「有人在可坐物旁边」这个先验比「她站着」强。

三种处置，按优先级：
1. **删掉它**（最有效）——画面里不需要的可坐面一律不写进 caption。
2. **逐项否认用途**：`it is only a step, too low to sit on` / `this ledge is narrower than her hand and there is nothing on it`。
3. **把它换成不可坐的形态**：台子改成窄沿（`no wider than her wrist`）、台阶改成坡道。

配套句（写人物时）：`her shoes are flat on the floor and her weight is on both of them`——脚底写平，人就不会被摆成坐姿。
