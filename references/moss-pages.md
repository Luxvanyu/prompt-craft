# MOSS 分格页 · 版面引擎（从 moss-manga v1.1 并入）

> 前面各篇管「一张图长什么样」。这一篇管**一页里有多个框、框里有坐标**的那一类任务：
> 分格漫画页、连续页、同一角色跨页不换脸、按语料抽真实体位。
>
> **本文是操作脊柱，不是全量词表**。13,488 条实测语料、十二篇兜底词表、五个脚本仍在
> `C:/Users/Administrator/.dsh/skills/moss-manga/`（绝对路径，可直接 `node` / `open`）。
> 需要抄整串、查频次、跑校验时才去那边，日常写页看这里就够。

---

## 一、先选引擎（选错，后面全白做）

| 你要的 | 引擎 | 写法 |
|---|---|---|
| 一页多格、每格独立机位、要控制格与格的位置 | **MOSS** | page JSON + bbox，`compile` 出提示词 |
| 连续几十页、人物必须一模一样 | **MOSS** | 角色卡 base + variants（机制级一致） |
| 单张图要成片感、画风稳定、脸好看 | **NAI5** | 你说过默认走 NAI5，写法见本文第九节 |
| 单张图里要中文台词/旁白 | **NAI5** 最快（`text"…"`）；MOSS 也能（bubble item） | — |
| 已有 MOSS 分镜，想用 NAI5 重画 | 搬 `moss-manga/references/nai5.md` 第 9 节 | 版面→版式句，格内→槽位 |
| 反推参考图 | 都能；规则在 `moss-manga/references/nai5/图片反推.md` | 屏蔽发色/瞳色/发型/胸围 |

**两个引擎的分工轴不一样，这是最容易踩的坑：**

- **MOSS 按「格」分工**——一人只在一处描述，写了格就只属于那格。
- **NAI5 按「属性类型」分工**——外貌进 Character 槽位，动作与环境进主串。

所以 MOSS 的 `character.desc` 整段贴进 NAI 槽位会双输：姿势跑去管外貌的地方，外貌又被主串重复一遍。

> **色图默认口径（用户 2026-11-20 定，优先于本文其它尺寸建议）**
>
> - 色图一律**走平铺 tag 串**；**人物 ≤2 时不要 Layout**（Layout 是为分格、多人、画面文字存在的）。
> - **默认引擎 MOSS**（用户 2026-11-22 定）：写提示词不再默认 NAI5，只有当次明说要 NAI5 / Anima / 要画师串时才换引擎。
> - 尺寸 **832×1216**（竖）／**1216×832**（横），不再用 1536×1344 / 1344×1536 / 1024×1536。
> - **不写渲染与氛围层**：粗颗粒胶片段、35mm / ISO1600 / halation / 化学偏色、蒸汽、光柱、烛光之类一律不进色图（用户 2026-11-20 定，除非当次明确要求）。
> - **只写动作、位置、接触关系、可见部位**；部位必须显式点名——`nipples` / `pussy` / `penis` / `testicles` / `ass` / `thighs`，漏写模型就不画。
> - ≥3 人、要分格、要画面文字时才回到页面 JSON + `compile`。

> **手部几何必须写死四件事（2026-11-22 反手事故后补）**：只写 `holding X` / `holding dildo` 会出「反手」——模型只画手指正面、不画掌心平面，读起来就像手背朝外攥着。四件事缺一即错：
> 1. **哪只手、几只**——`her right hand alone`；`both hands` 在平铺串里会让两手互相吞并，指头归属直接乱。
> 2. **掌心朝哪**——`with the palm turned toward her own belly`（朝自己身体永远比「朝镜头」好读）。
> 3. **拇指在哪侧、指尖落在哪侧**——`her thumb laid up along the near side of the shaft and her four fingertips curling around the far side and showing at its edge`；拇指与指尖不同侧才成立。
> 4. **腕子从哪来、手背朝哪**——`the wrist coming up from below with the back of the hand facing out`。
>
> 另加一条几何锚：道具**必须有接触点**（`the base of the toy pressed down against her mound`），悬空的手一定读错方向。

---

## 二、页面是什么形状

一页 = `summary` + `items[]`。

- `summary.caption` 是**整页总述**，必须含三段，缺一段就散架：
  1. `<|background_setting|>…<|/background_setting|>` 场景一句
  2. `<|layout|>LAYOUT AND STORY: PANEL ONE is …<|/layout|>` 一格一句，只写位置和内容
  3. `<|character_list|>…<|/character_list|>` 角色表（引擎自动注入，别手写）
- `items[]` 三类 item：`panel`（框）/ `bubble`（气泡）/ `character`（人物）。**没有 native，没有 text 类型**。
- 每个 item 都有 `bbox: [x1, y1, x2, y2]`——**x 在前**，不是 yxyx。搞反整页错位。
- 画布默认 1024×1536（竖）。

字段级细节、shape/frame/camera/kind 全表 → `moss-manga/references/page-json.md`。

---

## 三、七条铁律（违反任一条，图就会崩）

1. **一人只在一处描述**。`panel.desc` 写场景/机位/道具/光，不写长相与衣服；`character.desc` 写「编号 + 位置 + 姿势 + 表情 + 手」。同一件事写两遍 → 重影、错肢。
2. **手必须给「拇指锚」**。只写 `both hands lifted` 等于没写，模型把掌外旋 180° 画成反手。写法：掌心朝哪 + 拇指在哪 + 手指怎么放；双手对称高举最危险（没有参照物），要么给接触物，要么明写 `palms turned inward`。
3. **朝向四词与动作绑定**：`from the side` / `from behind` / `from above` / `from the front`。改了体位不换这四个词，手腿就朝反方向长。
4. **结合点不能落在水线以下**——否则下半身整个泡掉，不画生殖器、不画插入。把结合点抬到水面以上，男性站浅水。
5. **匿名男也要建角色卡**。只在 panel 写 `a nude man`，模型不画阴茎；给他一个 character 项（look 含 `erect penis`）立刻正确。无脸要逐个否掉五官（`no eyes and no nose and no mouth`），不能只写 `faceless male`。
6. **变种名里绝不能带姿势词**。`(NUDE STANDING)` 会跟着角色出现在每一格。改中性编号 `(NUDE ONE)`。
7. **base + variant 合并时要去重**。两边都写了 `completely nude, erect penis` 等于喂三遍，权重翻三倍。

---

## 四、一页一件事

- 一页只推进一个动作节点。想塞两件事，拆页。
- 一页只留**一格**画完整环境，其余格写 `PLAIN WHITE BACKGROUND with no background detail at all`。每格都画背景，人物会被稀释成小人。
- 人物顶满画面 70–90%。小格用 `waist-up medium shot`。
- 嵌格（inset）只讲**别的时空**（结合点特写、前一刻、旁观视角），2–4 个，每个 ≥256×350，写 `its own scene, with a thick white border and a soft drop shadow`。
- `xclose`（大特写）一格最多一个，且不小于 376px。
- **不要指望角色卡的默认表情**：base look 里那句 `confident tired smile` 每格都生效，主角就全程一个表情。每格单独写脸（眉/眼/嘴/下颌/汗/视线）与身体（重心/手在哪/躯干扭转/惯性）。

---

## 五、文字怎么进画面

- **气泡**：`bubble` item，`kind` + `text`。kind 全集：`speech` / `speech-notail` / `shout` / `whisper` / `tremble` / `thought` / `heart` / `narration` / `narration-bare` / `sfx`。
- **画面内文字**（招牌/门牌/手机屏/封面）：`item.caption` 会**整段覆盖**编译结果，必须手写完整串；只写 desc 不会把字写进去。
- 三条纪律：说话人不在画面 → `speech-notail`；同格双人 → 写几何约束（`in the TOP RIGHT of PANEL ONE, tail pointing LEFT toward her own face, SPOKEN BY CHARACTER TWO`）；thought 气泡补 `The tails of thought bubbles point at nobody.`
- 竖排气泡宽 80–130、高 300–400；一页 3–5 条，单条 15–25 字。

---

## 六、角色卡

```json
{
  "id": "hanheeah",
  "name": "CHARACTER SEVEN - HAN HEEAH",
  "look": "Han Heeah, young woman, snow-white silver hair …",
  "variants": [{ "id": "incognito", "name": "INCOGNITO", "look": "oversized sunglasses and a black face mask …" }]
}
```

- `id` 全小写，只留 `[a-z0-9_-]`，页面靠它引用。
- `name` 固定格式 `CHARACTER <序号> - <罗马音名>`——引擎靠这个格式塞进 `<|character_list|>`。
- **罗马音，不写汉字**：汉字会被当要画的字画到画面上；中文名放 `note`（只给人看）。
- base 只写不变（脸型/眼/发/肤色/体型基准）；variants 写会变的（年龄阶段/服装/裸体/道具/状态）。
- 变种默认项**不要是 nude**——默认项是该角色的标志性出场状态。

---

## 七、出图前自检（跑脚本，不要凭眼睛）

```bash
D=C:/Users/Administrator/.dsh/skills/moss-manga/scripts
node $D/check-pages.mjs <导出后的 pages.json>     # 单页内部：bbox/气泡/手势/朝向/变种名/三段
node $D/scene-consistency.mjs <project目录>        # 跨页：同一房间有没有画成两个房间
node $D/anchor-scenes.mjs <project目录> --dry -v   # 房间锚定修复，先看对照再落盘（自动备份）
```

- 第一个查六项：bbox 是否越出所在框、气泡尺寸、角色是否有手势朝向、panel 与 character 方位词是否互斥、变种名是否含姿势词、summary 三段是否齐全。写了性行为却没记 `src:` 的页会被点名。
- 第二个查**跨页场景漂移**：相邻两页 `<|background_setting|>` 词重合度 <50% 就是同一处没接上（会先按地点词排除「本来就该换场」）。

---

## 八、用户说「来个这个角色的性爱」——一条命令，不要反问

**不要问「想在哪儿」「什么姿势」「白天还是晚上」**——这些正是该随机定的。`scene-roll.mjs` 一次全定，并把体位接到语料里的真实条目上：

```bash
S=C:/Users/Administrator/.dsh/skills/moss-manga/scripts/scene-roll.mjs
node $S --char "koharu (blue archive), pink hair, halo"      # 全随机：时间/场所/家具/光线/镜头
node $S --char "sensei, koharu" --people 3                    # 三人行
node $S --char "neru (blue archive)" --taste 触手 --place 浴室  # 限定题材与场所
node $S --char "koharu" --seed 31337                          # 复现刚才那张
```

输出就是成品，直接照着写：场景卡（时间/场所/光/镜头/氛围）→ 体位 + 出处 → 骨架 + 差分 → 直抄整串 → `src:` 记录。

**硬规矩**：定了就写，不许把随机推回给用户；整串里的人数/场所/时间已互相对齐；姿势**必须**来自语料条目；一页多格时同一 seed 固定场所/时间/光/镜头，姿势各格各抽一次（`--taste` 收窄到同一族，避免两种物理规则打架）；`src:` 写进页 note，`check-pages.mjs` 会核。

### 「定了就写」之后还要人做的事

语料条目是**别人的**场景，落地时要删掉与本页冲突的部分（多出来的 `1boy` / `bed` / `bedroom` / `outdoor` / `sofa`），以及与本页角色体型冲突的（给萝莉体型抽到 `sagging breasts` 就删）。删是删冲突项，不是重写姿势。

### 语料库在哪、怎么查

13,488 条实测条目 / 45,256 个标签，索引 `E:/dow/gongzuo/tag-lexicon/index.json`（`TAG_LEXICON` 可覆盖）。

```bash
T=C:/Users/Administrator/.dsh/skills/moss-manga/scripts/tag-search.mjs
node $T --pose 骑乘位          # 整族骨架：半数以上条目共有的标签，整段照抄
node $T --pose 各种体位/后入    # 按分类路径匹配，附各条差分
node $T --random 各种体位 -n 3  # 随机抽 3 条真实整串
node $T stomach                # 模糊查标签 + 频次（stomach bulge 最多）
node $T --diff 爬行试图逃走      # 差分族：同族重合度 + 共享前缀（跨帧该复制的那段）
node $T --dict 泳装             # 中文 → tag（图鉴 7,526 条）
```

三套法典：`suozhang_r18`（11,990，覆盖面最广）/ `suozhang_nai5_r18`（1,147，词最干净，同题材优先）/ `mengshen_r18`（351，按人数×部位编排，口交最细）。

**不要凭印象造标签**：`stomach bulge`（151）、`body in water` 这类具体词都在库里；自造词模型多半当噪声。查不到再自己写，而且要写成英文句子而不是生造 tag。

**四条用法纪律**：①数字是「多少条串用过它」，常规图挑大数字，特定效果才挑小数字；②同一维度只取一个词（体位/机位/绳种/服装各一个，两个 = 两套物理规则打架）；③优先抄结构不抄内容（长串的价值在排列顺序：构图→光→道具→液体）；④词表是补洞的，不是堆料的——写完自检，只有「这一格明显缺东西」才回来补 2–3 个词。

---

## 九、同一页的 NAI5 写法（用户默认引擎）

MOSS 定的是**版面**，NAI5 定的是**成片**。同一段戏要 NAI5 版时：

- 五字段分工：主体身份 / 动作 / 环境 / 画风串 / 质量词（质量词单独落最后一行）。
- 权重只用 `::`；画师串靠前（前四分之一即可，不必打头）。
- 单张图 = 平铺 tag 串 + 一句英文锚点；**不做分格**就别带 `-1::multiple_views::`（会和分格打对打）。
- 详细写法与 MOSS→NAI5 搬运表 → `moss-manga/references/nai5.md`。

---

## 十、文件地图（都在 `C:/Users/Administrator/.dsh/skills/moss-manga/`）

| 文件 | 什么时候翻 |
|---|---|
| `references/page-json.md` | 页面 JSON 全字段、shape/frame/camera/kind 全表、bbox 坐标体系、嵌格与出血 |
| `references/body-anatomy.md` | 手、朝向、水位、接触点、多人同格、无脸替身——人体不崩的全部硬约束（最贵的一课） |
| `references/r18-vocabulary.md` | R18 九槽位 + 三套法典频次 + 人数×部位矩阵 + 口交细分 + MOSS 禁忌 |
| `references/symptoms.md` | 症状 → 改哪一句（反手、断肢、穿模、糊水、气泡错位、表情僵） |
| `references/tag-strings.md` | 1,202 条成串提炼：差分=变种、共享前缀=跨帧一致、按题材抄现成串 |
| `references/pipeline.md` | moss-manga-studio 命令行、编译校验、渲染、页序、批量与坑 |
| `references/nai5.md` | NAI5 写法入口 + MOSS→NAI5 搬运表 |
| `references/lexicon/*.md` | 十二篇兜底词表（positions/acts/cameras/outfits/restraint/monsters/partners/strings/sets/dict/params） |

**常见误解（都被实测否掉）**：「框会裁切画面」（不会，框只是方位句，框对不上图是正常的）；「多写形容词人物更准」（反过来，同义堆叠互相稀释）；「回合多了模型会记住上一格」（不会，每页独立编译）；「加 NSFW 标签更容易出」（MOSS 不需要，和 `censoring` 类词同现还互相打）；「人物多要堆人数锚点」（靠蒸汽/遮挡/剪影就够）。