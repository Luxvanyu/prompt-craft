# 附录 H：风格提取

<!-- back -->
返回：`references/aesthetic.md`（审美内核正文）｜总入口 `SKILL.md`

用户给图说"学这个风格"时，不要用形容词模仿（"类似那种复古电影感"），走提取流程。

本文件是 `ajinnaaa/extract-visual-style-2` 方法论的精简操作版。

---

## 一、四类信息必须分离

看到一张图，先把它拆成四类，混在一起就会把场景规则当全局规则。

| 类别 | 内容 | 归属 |
|---|---|---|
| **Content** | 身份、物体、地点、动作、服装、logo、文字 | 只属于这张图，不进风格 |
| **Transferable style** | 形状语法、边缘行为、色彩角色、灯光逻辑、质感、空间、构图、运动、finishing | 可迁移，这才是"风格" |
| **Production locks** | 画幅、分辨率、媒介、合成目的、模型约束 | 全局约束 |
| **Scene locks** | 只在这个场景成立的东西（雨、雪、特定建筑） | 场景级，不能全局化 |

**最常见的错误**：把场景锁当全局规则。参考图是"雨夜霓虹"，提取出的风格就变成"必须有霓虹和雨"——那不是风格，是内容。

---

## 二、三层规则架构

| 层 | 说明 | 例子 |
|---|---|---|
| **Stable core** | 每张图都成立的 | "阴影偏青，高光偏暖" |
| **Conditional variants** | 特定条件下才用 | "夜景时背景落 3 stops；日景落 1 stop" |
| **Scene-specific locks** | 只对这一张/这一组 | "这个场景有一盏钨丝吊灯" |

写规则时必须标层，否则下一张图就会误用。

---

## 三、证据充分度

| 样本数 | 标签 | 能下什么结论 |
|---|---|---|
| 1 张 | provisional single-sample | 只能提"观察"，不能称"风格" |
| 2–5 张 | tentative shared style | 可以提共性，但要标 tentative |
| 6+ 张，覆盖不同主体/环境/光照/景别 | stronger series-level evidence | 可以定 stable core |

**判据**：如果 6 张图里光照条件全一样，证据强度仍等于 1 张。

---

## 四、每条规则的记录格式

```
[规则] location/owner + direction/behavior + relative strength + visual purpose + condition/exception + failure mode
[证据] 可见证据（具体到画面位置）
[覆盖] 样本数 / 覆盖了哪些变量
[层级] stable core / conditional / scene lock
[状态] observed / inferred / proposed / unknown
[置信度] high / medium / low
```

**禁止**：只凭画面断言具体摄影机、镜头型号、胶片、LUT、软件。可以说"看起来像高感负片的行为"，不能说"这是 Portra 400"。

---

## 五、十二个视觉系统（互不越界）

提取时逐项过，每项只写属于它的东西：

1. **Project identity** — 这个项目的不可变量（画幅、视角习惯、主题）
2. **Rendering & shape** — 边缘行为、形状语法、线条 vs 块面
3. **Color** — 角色分配、面积比、阴影/高光色相
4. **Lighting** — 光源类型、方向、质量、比例、衰减
5. **Space** — 透视类型、层数、空气透视
6. **Composition & lens** — 焦段、机位、构图习惯
7. **Material** — 粗糙度、光泽、半透、湿润、磨损
8. **Character** — 剪影、比例、脸部构造、身份差异手段
9. **Background** — 细节密度、边缘锐度、与主体的分离手段
10. **Coexistence & compositing** — 角色与背景的相对锐度/对比/明度/饱和度分离、共享光向
11. **Effects physics** — 源、附着、传播、衰减、残留
12. **Motion & time** — 静止/运动、模糊类型、时间点

---

## 六、提示词模块顺序（12 块）

提取完成后，按这个顺序组装（内容无关的模板）：

```
1  global style core
2  color
3  lighting preset
4  space / composition / lens
5  material
6  character
7  background
8  coexistence / compositing
9  effects physics
10 motion / temporal
11 negatives（只针对已证实的失效模式）
12 production / scene locks
```

内容无关的提示词以 `【在这里填写人物或场景内容】` 开头，内容插在 6–7 之间。

---

## 七、十二项冲突检查（交付前必过）

1. 场景规则被当成全局规则了吗？
2. "提议"被写成"事实"了吗？（proposed vs observed）
3. 两套 lighting preset 互斥吗？（一个说顶光，一个说侧窗）
4. 调色覆盖了材质固有色吗？（把木头调成蓝的）
5. 雾/虚化破坏了主体可读性吗？
6. 角色与背景的光向一致吗？
7. 角色与背景的色温兼容吗？
8. 颗粒在角色与背景上是同一个参数吗？
9. 透视在角色与背景上一致吗？
10. 特效发光了，但不影响邻近表面吗？（发光物必须照亮周围）
11. 负面压制了想要的材质吗？（例如负面写 `grain` 却要胶片感）
12. 内容泄漏进 content-free prompt 了吗？
13. 每个数字都有依据吗？（stops、焦段、面积比）

---

## 八、校准模式（用户给结果图说"不对"）

不要堆负面。流程是：

1. 让用户指出"哪里不对"（或自己诊断，见 09）
2. 定位到**哪个视觉系统**出错
3. **替换那条规则**，而不是加一条负面
4. 只改一处，重跑
5. 保留改动前后的对照

**为什么替换优于负面**：负面是"不要 X"，模型仍不知道要什么，容易把 X 旁边的正确东西一起压掉（最典型：负面写 `grain` 会把颗粒和细节一起抹平）。

---

## 九、提取检查表

- [ ] 四类信息分离了吗？内容有没有混进风格？
- [ ] 每条规则标了层级（stable / conditional / scene lock）？
- [ ] 证据充分度标了吗？1 张就别说"风格"？
- [ ] 有没有断言具体器材/胶片/LUT？
- [ ] 十二个系统逐项过了吗？
- [ ] 冲突检查 13 项过了吗？
- [ ] 数字（stops、焦段、面积）都有依据吗？
