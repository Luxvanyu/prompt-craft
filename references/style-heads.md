# 风格头开关表（style heads）

「头」＝提示词最前面那句定调。**一张图只开一个主头**，质感层最多再叠两层。

头写对了，后面写得糙一点也像作品；头写错了，后面每句都对也像随机图。

---

## 怎么选（三问，十秒）

1. **这张图最亮的是什么？** → 决定明度档（高调 / 中调 / 低调）
2. **光有多硬？** → 硬光（边缘像刀切）／散光（没有边）／混合（一硬一软各管地盘）
3. **画面里有没有「介质」？** → 有雾、有水、有雨、有玻璃、有胶片颗粒 → 先定介质，再定头

答完这三个，下表里只剩一到两行。

---

## 主头

### 1. 自然光写实（默认头）

- **什么时候**：白天、户外、室内窗光，不想让人看出是「风格」
- **定调句**：`The whole picture sits in the middle of the value range, and the light comes from one direction only.`
- **必带**：一个主光 + 一个暗锚 + 一句话说清最亮处占多少
- **必禁**：`cinematic` / `dramatic lighting`（会直接跳到电影感）
- **数值目标**：mean 0.40–0.52 / dark ≥0.10 / sat ≥0.20
- **失败长相**：发灰、整张挤在中调、亮部没颜色

### 2. 电影感低调

- **什么时候**：室内、夜、只有一个光源、要压
- **定调句**：`Low key: everything is either in the one light or in a dark that has no light of its own.`
- **必带**：光路三落点 + 衰减方向 + 未照亮区逐项点名 + 暗面积写数字
- **必禁**：多个光源（会互相抵消成灰）
- **数值目标**：mean 0.18–0.30 / dark 0.30–0.55 / nw <0.02
- **失败长相**：暗到看不出东西（dark >0.65）、或者暗块加起来超过半幅
- **代表**：107 屏幕光照脸（mean .189 / dark .683）

### 3. 硬光高调

- **什么时候**：正午、白墙、雪、棚拍、要「亮得有形状」
- **定调句**：`High key: the lit surfaces are the subject and the shadow does the drawing.`
- **必带**：边缘硬度 `cut like a blade, with no gradient at all` + 三个黑锚点（G4）
- **必禁**：`overexposed` / `pure white`（亮部会失去全部颜色）
- **数值目标**：mean 0.50–0.62 / nw <0.03 / sat ≥0.18
- **失败长相**：整张飘、亮部像纸、没有一处接近黑

### 4. 胶片 / 廉价相机

- **什么时候**：要「不完美」、要私人感、要年代感
- **定调句**：`A badly exposed frame from a cheap camera, and the picture is the better for its mistakes.`
- **必带**：颗粒层 + 一两种可控缺陷（歪 / 失焦 / 漏光 / 色差）+ 三处色相幸存
- **必禁**：把缺陷写成实体（见 G55）、负面里写 `grainy / noise / blurry`（会把颗粒一起抹掉）
- **lint**：`--intent blown,leak,soft,tilt`
- **数值目标**：mean 0.40–0.50 / sat ≥0.25 / nw 可放宽到 0.09
- **代表**：121 廉价相机（mean .445 / sat .288）

### 5. 家庭录像 / 8mm

- **什么时候**：要怀旧、要「被拍下来」而不是「被摆好」
- **定调句**：`One frame from a home video camera: soft, slightly underexposed, with the colour drifting warm.`
- **必带**：黑位被抬起（这个风格**允许** dark 极低）+ 边缘轻微色散 + 运动物写成痕迹（G34）
- **数值目标**：mean 0.40–0.45 / nw 0.01–0.02 / dark 可以低到 0.04（合法例外）
- **代表**：112（mean .423 / nw .0146 / dark .037）

### 6. 黑白

- **什么时候**：要把注意力全放在形、光、质感上
- **定调句**：`Black and white only: no colour anywhere, and the whole picture is built from four values.`
- **必带**：四档明度各写名字与面积 + 一个真正的黑 + 一个真正的白
- **必禁**：任何色相词（模型会偷偷加一点颜色）
- **数值目标**：mean 0.35–0.50 / dark ≥0.15
- **代表**：95 黑白泳池

### 7. 长曝光

- **什么时候**：夜街、车流、水面、人群
- **定调句**：`A long exposure: everything that moved has left a smear and everything that stood still is sharp.`
- **必带**：静止物必须真的静止 + 移动物写成痕迹（无名 + 否认部件 + 轨迹理由，G34）+ 水面写成「被压平成了什么」（G35）
- **必禁**：`no ripple` / `no blur`（否定必失败）
- **数值目标**：mean 0.25–0.35 / dark 0.20–0.35
- **代表**：101 石拱桥（dark .211 / mid .771）

### 8. 古典绘画（梵高 / 莫奈 / 北斋 / 千里江山）

- **什么时候**：要「像一幅画」而不是「像一张照片」
- **定调句**：`painted the way <作者> painted <具体作品>` —— 点名，不描述
- **必带**：点名后删掉自己的细节（不然会变成大杂烩）+ 竖幅就裁原画一段 + 给纵向行程
- **必禁**：自己描述笔触（`swirling brushstrokes`）
- **代表**：63 莫奈睡莲桥 / 64 梵高（点名翻盘）/ 65 北斋冲浪 / 66 千里江山

### 9. 木刻版画

- **什么时候**：要硬、要图形化、要老印刷物
- **定调句**：`A woodcut: flat black shapes cut by hand, with a knife mark wherever a line changes direction.`
- **必带**：刀痕是**可数的单元**（3–5px 有方向的线条），不是均匀的场
- **必禁**：网点 / 半调（G31 判死）；但**刀痕可以**——刀痕是可数的方向线条，不是重复单元
- **代表**：88 木刻版画

### 10. 水墨

- **什么时候**：要留白、要气韵
- **定调句**：`Ink on paper: the picture is mostly empty paper, and the ink only does the work it has to.`
- **必带**：空白是主体之一（占三到四成）+ 墨分五色（写「淡墨/焦墨」对应的具体面积）
- **必禁**：把纸写成 item（G45）
- **代表**：62 水墨海报

### 11. 极简平面 / 海报

- **什么时候**：要设计感、要留白、要有文字
- **定调句**：`A flat printed rectangle: no perspective, no camera, no depth.`
- **必带**：大留白区占三到四成且里面有内容 + 全图只允许一条非水平线 + 颜色写死数量 `exactly two things and nothing else is allowed any`
- **格式**：用 Layout（这是官方唯一推荐的 Layout 场景）
- **失败长相**：纸被当成物体画成墙（G45）、网点出不来（G31）

### 12. 建筑 / 空间

- **什么时候**：要「地方」而不是「人」
- **定调句**：`The room is the subject; the light is what describes it.`
- **必带**：三条同深度的水平线（地脚线 / 台沿 / 梁）+ 一个公认尺（地砖、门、把手）+ 一个暗锚
- **必禁**：`full body`（会吞掉机位词）
- **代表**：46 走廊 / 115 走廊标定 / 119 更衣室（mean .259 / nw .0035）

---

## 质感层（可叠，最多两层）

| 层 | 一句话 | 什么时候加 | 代价 |
|---|---|---|---|
| **粗颗粒** | `one single coarse visible grain layer covers the whole picture, each clump two to three pixels across, and the grain sits over everything including the darkest part of the frame` | 几乎总是（默认叠） | CFG 要降 0.1–0.2，否则当瑕疵抹平 |
| **色差** | `a thin fringe of colour on every high-contrast edge` | 胶片、老镜头、要「不完美」 | 容易变成彩虹边，写「thin」写死 |
| **暗角** | `the corners fall off about one stop` | 要把视线压回中间 | 会和「暗部面积」打架，二选一 |
| **漏光** | 走 G55 三件套 | 一次性相机、夏天 | 写错就变实体 |
| **失焦** | `nothing in the frame is sharp, and the softness is even from edge to edge` | 私摄影、做梦 | 会和细节要求冲突，别同时要「清晰」 |
| **halation** | `a wide soft halation bleeds six to eight pixels around every high-contrast edge` | 夜景、霓虹 | 会吃掉小字和小结构 |

---

## 组合纪律

1. **一个主头，两层质感，到此为止。** 三个头叠上去＝没有头。
2. **主头之间互斥的组合**：高调 + 低调（取平均变灰）、黑白 + 任何色相词、长曝光 + `no blur`、极简平面 + 透视句。
3. **禁用清单**（本模型实测不可做）：印刷**网点** / 半调 / 报纸网点 / 像素格 / dither（G31、G97 判死，同一族：要求整幅遵守一个「细小且全局统一的重复单元」）；亚像素纹理（<1/100 画面宽）；多指独立手势（69 号）。
   **但「错版/套印错位」是活的**（172/172v3 实测，G96）：它是**轮廓级位移**，不是单元级重复。riso 三色套印错位可以放心用，只在写法上要求「残影是平色月牙，不是模糊重影」。
4. **第一句的归属**：第一句同时承担「明度定调」和「风格头」，两件事**合成一句**写，例如 `Low key: everything is either in the one light or in a dark that has no light of its own.`——前半是明度档，后半是风格。**不要**先写明度头模板再另起一句写风格头（会互相抢权重）；明度头的数值细化（各档面积、高光载体）放在第二、三句。

---

## 参数

| 项 | 值 | 备注 |
|---|---|---|
| CFG | 3.0（带颗粒 3.1 起、不带 3.2） | 官方推荐 3.0–6.0；CFG 高会把颗粒当瑕疵抹平 |
| Steps | 50 | 官方「≥50 最佳」 |
| Shift | 5.0 | 官方默认 |
| 采样器 | Euler + sgm_uniform | 官方工作流 |
| SLG | 负向跳过第 22 层 | 二次采样 SLG |
| 分辨率 | 1–2MP，16 的倍数 | 1536×1024 / 1024×1536 / 1024×1024 / 1536×640 |

---

## 对照：一个题材换六个头

同一个「天台的女孩」，头不同，出来的东西完全不同：

| 头 | 你大概会得到 |
|---|---|
| 自然光写实 | 下午四点的天台，什么都在，什么都不突出 |
| 电影感低调 | 只有一盏灯照着她的侧脸，其余全黑 |
| 硬光高调 | 白到发亮的水泥和她的影子，像时装片 |
| 胶片廉价相机 | 歪的、过曝的、有一道漏光的私人照片 |
| 黑白 | 只有形和光，脸不重要 |
| 极简平面 | 一块色 + 一行字，她可能只是个剪影 |

**选头就是在选「这张图要说什么」。** 内容一样而头不同，是六张不同的作品，不是六个版本。
