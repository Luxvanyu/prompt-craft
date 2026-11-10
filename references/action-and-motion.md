<!-- P2 · 大动态格斗 -->
# 大动态与动作格斗库（Phase 2: Dynamic Action & Combat Motion Library）

本参考手册规范了 `prompt-craft` 体系在大动态、高张力动作及空中/冷兵器格斗场景中的核心物理法则、解剖防崩约束、羽翼气动力学及四模型（MOSS-Image、NovelAI v5、Anima3、Krea 2）转译标准。

---

## 1. 核心物理缺陷与对抗哲学

在扩散模型（Diffusion Models）中，动作与打斗出图经常出现三大崩溃现象：
1. **多肢体与幽灵残影（Multi-Limb & Phantom Hands）**：描述“快速挥剑”、“连续刺击”时，注意力机制会在运动残影路径上误算出手臂，导致画面出现 3 条手臂、双右手或悬空断剑。
2. **透视气球效应（Foreshortening Ballooning / B3 陷阱）**：盲目使用 `foreshortening` 或裸写 `from below`，导致近景脚底板或拳头体积畸变成 5 倍，遮挡并拉扯五官。
3. **羽翼物理脱节（Stiff Wallpaper Wings）**：绝大多数模型将翅膀视为静止贴纸，在激烈打斗时翅膀依然僵直站立，或直接与武器发生穿模撕裂。

**对抗哲学**：
* **定格 0.3 秒运动中段（In-Motion Keyframe）**：严禁描述连续过程，严禁描述“劈完收刀”的死姿态；必须定格在力道贯穿、斩切至一半、脚刚离地的爆发瞬间。
* **双手解剖闭环（Anatomical Lock）**：持械手动作确立的同时，**必须强制明确非持械手位置**。封死自由手的注意力盲区，从根源消除多臂。
* **羽翼升格为气动控制面（Aerodynamic Flight Surfaces）**：翅膀必须具备因果受力（折叠减阻、前张刹车、侧倾差动、扫地荡尘）。
* **透视安全笼（Foreshortening Safety Cage）**：废除裸透视词，改用“沿刃面三七开跟拍，面部比例严格保全”的机位几何约束。

---

## 2. 四大动作相位与关键帧定义（The 4 Action Phases）

打斗动作必须明确所处相位，不同相位对应不同的肢体与羽翼状态：

| 相位 | 动作时序 | 核心视觉特征 | 羽翼状态 | 典型描述片段 |
| :--- | :--- | :--- | :--- | :--- |
| **Phase A: 蓄势 (Anticipation / Coil)** | 动作发动前夕 (-0.2s) | 重心极度压低，蓄力未发，肌肉紧绷，眼神锁定目标 | 双翼后收蓄风，羽梢内敛，降低受风截面 | `crouches low in an aerial coil, right hand gripping the sheathed hilt, wings pulled back` |
| **Phase B: 击发 (Impact / Mid-Arc)** | 威力爆发中段 (0.0s) | 刃尖向前突刺或横斩至中段，带出音障激波或月牙光弧 | 隼式折翼紧贴背脊，羽毛压平顺风减阻 | `swept tightly back along her spine like a falcon in a dive, conical air ripples` |
| **Phase C: 滞空 (Airborne / Apex)** | 顶点失重瞬间 (+0.2s) | 身体处于滞空最高点，衣摆发丝全向上翻卷，速度线放射 | 双翼大幅度向上完全展开，张满受风提供升力 | `flared wide and high to catch the thermal updraft, feathers spreading air resistance` |
| **Phase D: 收势 (Recovery / Landing)** | 落地滑行制动 (+0.4s) | 单膝触地滑行，反向发力减速，地面碎石气浪飞溅 | 双翼向前强力反张包覆，充当空气阻力刹车 | `left wing flares aggressively forward as an air-brake, right wing skimming stones` |

---

## 3. 双手解剖闭环法则（Anatomical Lock Protocol）

**铁律**：只要画面中存在持械、出拳或单手动作，必须**在同一主句或紧邻从句中同时定义非持械手的解剖安置**。

### 常用闭环配对表：
1. **直线突刺（Thrust / Pierce）**：
   * 持械手：`right hand firmly grips the silver rapier extended forward in a piercing thrust`
   * 非持械手：`while her left hand is pulled tight against her left hip in a clenched counterbalance fist`
2. **水平回旋横斩（Horizontal Slash / Cleave）**：
   * 持械手：`right arm sweeps the curved blade horizontally through a 180-degree crescent arc`
   * 非持械手：`while her left hand is raised beside her collarbone in an open-palm deflection guard`
3. **拔刀居合蓄势（Iaijutsu / Quick Draw）**：
   * 持械手：`right hand rests on the hilt ready to draw`
   * 非持械手：`while her left hand firmly grips and steadies the scabbard at her hip`
4. **滞空俯冲平衡（Diving Balance）**：
   * 持械手：`right hand holds the blade extended downward`
   * 非持械手：`while her left arm extends backward parallel to her spine to stabilize her flight path`

---

## 4. 羽翼气动力学矩阵（Aerodynamic Wing Mechanics）

她的白色大羽翼在动态中遵循以下气动行为，严禁画成平面垂直贴纸：

* **高速突进 / 俯冲**：
  `massive white feathered wings swept tightly back along her spine like a falcon in a steep dive, primary feathers flattened against the gale`
* **急停制动 / 反向发力**：
  `her left wing flares aggressively forward and outward, acting as an aerodynamic air-brake that catches the turbulent headwind`
* **掠地低空滑翔**：
  `her right wing sweeps low, inches above the cracked paving, kicking up a rooster-tail spray of dust and gravel`
* **侧倾盘旋机动**：
  `wings banked at a sharp 45-degree angle, primary flight feathers parted to spill airflow during the high-g centrifugal turn`

---

## 5. 透视安全笼法则（Foreshortening Safety Cage）

为彻底根治 MOSS Rule B3 陷阱（`from below` + `foreshortening` 导致巨鞋遮脸或五官崩坏）：

1. **禁止裸写抽象透视词**：禁止出现孤立的 `extreme foreshortening`、`crazy perspective`。
2. **机位轴线引导（Camera Plane Alignment）**：机位必须沿着兵器平面的侧前方切入，保持景深落点。
   * 正确写法：`The camera tracks on a three-quarter angle along the flat plane of the blade, holding zero tilt, keeping facial proportions strictly intact.`
3. **头部与面部比例锁定**：必须显式声明面部五官不受透视扭曲拉扯。

---

## 6. 四模型动作转译矩阵

### 6.1 MOSS-Image
* **物理级摄影机文本**：遵循 11 关门禁，精确定义机位俯仰、距离、倾斜（zero tilt）、明暗落点。
* **单帧中段决断**：详细刻画剑刃激波、折翼羽流、非持械手位置与粗糙胶片颗粒（grain）。

### 6.2 NovelAI v5
* **Base Prompt**：放置全局战斗场景、光弧、气流、动态机位（`1.2::aerial falcon dive::`, `dynamic angle`, `motion lines`, `shockwave`）。
* **Character 1**：强化角色特征、武器与翅膀形态（`1.2::folded wings swept back::`, `slender silver rapier`, `holding sword`, `thrusting`）。
* **UC (负向)**：强力挂载 `-2::halo::`, `extra arms, multiple arms, 1.4::extra limbs::, extra weapons, floating sword, 1.3::broken spine::, deformed face`。

### 6.3 Anima3
* **9 槽位单行流**：严守质量、角色、服装、动作、环境槽位，**绝对不出现 camera/机位词**（如 tracking, low angle 等），防止机位词稀释画风。
* **末尾叙事动作驱动句**：在行末用一个精炼的英文叙事从句串联双手与翅膀状态（`She dives at extreme speed with her white wings folded tightly back...`）。

### 6.4 Krea 2
* **电影级视听长文本**：600~800 词，设定 120fps 高速快门冷光定格，细致描写金属反光、气流激波、肌肉重心与织物飞卷。
* **纯净版输出**：默认去除诗词尾巴，直接输出纯净影视级 Prompt。

---

## 7. 经典实战动作套路（Casebook Presets）

### 套路 1：【破空折翼·俯冲居合突刺】（Aerial Falcon-Dive Thrust）
* **定位**：高空高速击发（Phase B）。
* **机位**：三七开侧前跟拍，零倾斜，锁定五官端正。
* **双手**：右手持细剑前刺，左手腰际反向握拳。
* **羽翼**：隼式背向折叠，减阻流线。

### 套路 2：【掠地回旋·双翼急停反切斩】（Low-Skim Counter-Slash & Air-Brake）
* **定位**：贴地横斩与空气制动（Phase B & D 结合）。
* **机位**：贴地膝盖高度低机位，抓地表飞石与残影。
* **双手**：右手持刀大弧度横斩，左手胸前开掌防守。
* **羽翼**：非对称布局，一翼贴地荡尘，一翼向前反张抱风刹车。

### 套路 3：【破空后跃·滞空引弓拔剑】（Airborne Backstep Draw）
* **定位**：拉开距离与蓄势（Phase A & C 结合）。
* **机位**：仰角微俯拍，背景为宏大暮色或断壁残垣。
* **双手**：左手握紧鞘口，右手搭在剑柄准备抽刃。
* **羽翼**：向两侧完全张满形成浮力伞。
