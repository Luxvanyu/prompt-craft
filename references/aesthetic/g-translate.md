# 附录 G：翻译

<!-- back -->
返回：`references/aesthetic.md`（审美内核正文）｜总入口 `SKILL.md`

七维决策是思考层。真正决定出图的是**三个槽位**，每个槽位能承载的信息类型不同。

---

## 一、三个槽位，各装什么

| 槽位 | 能装 | 不能装 | 注意力权重 |
|---|---|---|---|
| **平铺 tag 串** | 模型认识的**名词/状态/已知概念** | 比例、衰减、因果关系、空间关系 | 中（会被稀释） |
| **结尾英文描述句** | **设计决策**：光的方向与比例、衰减、不对称、瞬间、材质行为 | 大量并列名词（会互相抵消） | **最高** |
| **JSON 分块（bbox）** | 精确位置、文字内容、多主体归属 | 全局氛围 | 高（但会锁死构图） |

**结论**：审美决策主要靠**描述句**承载，tag 只负责"有哪些东西"。把比例、衰减、瞬间写进 tag 串是无效的——模型不解析那些。

---

## 二、tag 预算（35 个标签的分配）

按用户既有密度规则（约 35 个平铺标签 + 一句英文描述）：

| 类别 | 数量 | 说明 |
|---|---|---|
| 人数 / 角色 / 作品 / 画师串 | 4–6 | 固定项，不动 |
| 身份锚（外观固定特征） | 6–8 | 眼镜娘那套固定设定 |
| 服装 | 3–5 | 只写能看见的 |
| 动作 / 姿态 | 2–3 | **只留一个主轴**（堆多了必变形） |
| 场景 / 环境 | 3–4 | 少而准 |
| **光** | **3–4** | 见下方词表 |
| **构图 / 镜头** | **3–4** | 见下方词表 |
| 材质状态 | 2–3 | 湿/旧/汗/皱 |
| finishing | 2–3 | 颗粒/光晕/景深 |

**光 + 构图合计 6–8 个标签**，这是审美的骨架。少于 4 个 = 模型回到默认均光居中。

---

## 三、光与构图的可用标签词表

这些是 danbooru 系模型真正认识的词，不是自造词。

### 光

`backlighting` `rim light` `contre-jour` `hard lighting` `soft lighting` `dappled sunlight` `god rays` `volumetric lighting` `chiaroscuro` `low key` `high key` `silhouette` `split lighting` `light from above` `candlelight` `moonlight` `neon lights` `light rays` `bloom` `halation` `lens flare` `window light` `sunbeam`

**不要用**：`cinematic lighting` `dramatic lighting` `beautiful lighting` `professional lighting`——这些是空转，模型给你平均值。

### 构图 / 镜头

`from side` `from above` `from below` `dutch angle` `close-up` `upper body` `cowboy shot` `full body` `wide shot` `negative space` `off-center` `foreshortening` `depth of field` `blurry background` `bokeh` `foreground blur` `profile` `three-quarter view` `looking away` `looking to the side`

**破对称专用**：`off-center` + `negative space`（这两个词是模型唯一稳定响应的构图标签）

### 材质状态

`wet hair` `wet clothes` `sweat` `glossy skin` `worn` `wrinkles` `dust` `steam` `smoke` `fog` `rain` `crumpled`

### finishing

`film grain` `35mm film` `kodak portra 400` `cinestill 800t` `expired film` `vignette` `chromatic aberration` `soft focus`

（用户已有粗颗粒层的既定写法，MOSS 里写在 summary.caption 最前面。）

---

## 四、描述句模板（一句，必须含五件事）

```
[瞬间/未完成动作] + [光源物件 + 方向 + 质量] + [比例或衰减] + [不对称/留白] + [一个材质可见行为]
```

**一句话，不要分号堆叠。** 五个成分里缺任何一个，模型就往默认值回退。

### 模板实例

**室内窗光（配方 2）**
> She has just set the cup down and her hand is still open above it, the only light a north window on camera left, half-hard and eight to one, dying within arm's reach so the far wall is already gone, and she sits on the left third with the right side of the frame held as empty wall.

**夜景（配方 1）**
> The bulb above the table is the hottest thing in the frame and everything else falls away from it — her skin at key, the room three stops under, nothing behind her brighter than the lamp — and she is caught mid-turn, not yet facing the lens.

**逆光（配方 4）**
> Low sun directly behind her, hard and warm, her body one and a half stops under the sky so she reads as a silhouette, every loose hair at the edge of her head lit and separated, and she is off-center with the empty bright sky filling the upper right.

**时装硬闪（配方 5）**
> Direct on-camera flash, hard, almost no modelling on the face but the shadow under the jaw a crisp cut line, everything it touches sharp — pores, the weave of the collar, the scratches on the buckle — and she is pushed to the right edge, half out of frame.

**阴天（配方 3）**
> Overcast with no direction to the light at all, so the structure comes from mass instead: her dark coat the heaviest shape at the bottom, the wall a mid grey, the pale sky the only light area, everything slightly wet and a shade darker where the water sits.

---

## 五、三个模型的落地写法

### MOSS（平铺 tag + 结尾句；含文字时改 JSON）

顺序：**人数 → 内容标签顺排 → 光 → 构图 → 材质 → finishing → 结尾英文句**

```
1girl, solo, [角色锚点...], [服装...], [动作主轴], [场景...], backlighting, rim light, hard lighting, off-center, negative space, depth of field, wet hair, film grain, 35mm film, <结尾英文描述句>
```

要点：
- 不带 LoRA 触发词、不带质量词（用户既定）
- 颗粒层写在 caption 最前面
- 需要精确文字/多主体归属 → 改 JSON，把文字内容单列 object 块

### Anima（平铺 danbooru tag + 一句英文）

顺序：**人数 → 角色名 → 作品 → 画师串 → 特征/场景/镜头标签顺排 + 一句英文描述**

要点：
- 不用 `角色名:` `scene:` `camera:` 这类行前缀
- 描述句里**绝不出现 camera 一词**（会被画成相机），改说 `the viewer` / `the foreground`

### NAI（权重语法 + 画师串置顶）

- 画师串按既定置顶（SFW / NSFW 两套）
- 光与构图的标签给 1.1–1.3 的轻权重，不要顶格
- 比例/衰减仍写在句子里，NAI 对自然语言的响应比 MOSS 强

---

## 六、标签稀释：最常见的失败模式

**现象**：加了 8 个美学标签，出图反而更平。

**原因**：并列的形容词在注意力里互相抵消。`soft lighting, hard lighting, dramatic lighting, moody lighting` 四个一起写 = 模型取平均 = 无光。

**规则**：
1. **一组只留一个**：光只留 3–4 个且互相兼容（`backlighting` + `rim light` + `hard lighting` 兼容；`backlighting` + `window light` 不兼容）
2. **宁可少一个，不要多一个**：删掉最不确定的那个标签，通常更好
3. **用句子补，不用标签补**：想说"衰减"就写进句子，不要找标签

---

## 七、从"单调提示词"升级的实操流程

给一段现有的提示词，按这五步改：

1. **删**：所有质量词、空转形容词（cinematic / beautiful / masterpiece / dramatic）
2. **定**：挑一个配方（06），把它的明度分布和比例记住
3. **加**：光 3–4 个 + 构图 3–4 个标签（从词表里挑，兼容的）
4. **写**：一句英文描述句，五个成分齐全
5. **减**：如果标签总数超过 40，从"场景/环境"里删（环境最不承担设计）

---

## 八、对照示例（同一内容，两版）

### 单调版

```
1girl, solo, glasses, black hair, school uniform, classroom, window, sitting, smile, soft lighting, depth of field, masterpiece, best quality, cinematic
```

问题：居中、均光、无比例、无衰减、摆拍、质量词空转。

### 审美版（配方 2 单窗光 + 眼镜娘固定设定）

```
1girl, solo, short black bob, blunt fringe, ahoge, round glasses, black eyes, white sailor uniform, red sailor collar, navy pleated skirt, white thigh-highs, sitting, classroom, desk, window light, hard lighting, from side, off-center, negative space, depth of field, dust, worn, film grain, 35mm film, she has just set the cup down and her hand is still open above it, the only light a north window on camera left, half-hard and eight to one, dying within arm's reach so the far wall is already gone, and she sits on the left third with the right side of the frame held as empty wall
```

改动清单：
- 删了 3 个质量词 + `cinematic`
- 删了 `smile`（改成瞬间）
- 加了光 2 个、构图 3 个、材质 2 个、finishing 2 个
- 加了五成分描述句
- 身份锚点保留不动

---

## 九、翻译检查表

- [ ] 描述句五成分齐全？（瞬间/光源+方向+质量/比例或衰减/不对称/材质行为）
- [ ] 光标签 3–4 个，且互相兼容？
- [ ] 构图标签里有 `off-center` 或 `negative space` 吗？
- [ ] 质量词全删了吗？
- [ ] 标签总数 ≤40？
- [ ] 动作标签只有一个主轴？
- [ ] 比例/衰减写进了句子而不是标签？
- [ ] Anima 描述句里没有 `camera` 一词？
- [ ] MOSS 里没有 LoRA 触发词、没有质量词？
