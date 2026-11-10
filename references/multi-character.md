<!-- P3 · 双人战术对峙 -->
# 双人互动与战术对峙系统（Phase 3: Multi-Character Interaction & Combat Staging）

本参考手册规范了 `prompt-craft` 体系在多人物、双人对打交锋、并肩作战及紧密接触互动场景下的防崩准则、空间隔离规范与 MOSS-Image 物理级提示词编写标准。

---

## 1. 核心痛点与物理防御哲学

在扩散模型中，画面中一旦出现两个或多个人物，崩溃概率呈指数级上升。主要集中在三大致命问题：
1. **特征串色与属性污染（Trait Bleeding / Cross-Contamination）**：
   * 现象：角色 A 的发色、羽翼、金色发夹，会随机长到对手 B 身上；或者对手 B 的黑皮衣穿到了 A 身上。
   * 根源：CLIP / T5 文本编码器对长句中形容词与名词的归属缺乏硬隔离，“pink hair”与“wings”的注意力权重漂移到了临近的角色名词上。
2. **肢体融合与连体畸变（Fused Limbs & Phantom Arms）**：
   * 现象：两人兵刃交锋或接触（拥抱、牵手、推搡）时，交界处长出 3~5 条手臂，或者手掌融合在一柄剑上分不清谁在持剑。
   * 根源：模型在两人接触的密集注意力区域无法区分身体边界，且常有“未被提及的手臂”被注意力机制随意填充。
3. **动作主客体颠倒（Subject-Object Inversion）**：
   * 现象：描述“A 砍向 B，B 举盾格挡”，模型经常画成 B 拿刀砍 A，或者两人同时拿刀砍空。

**防御哲学**：
* **四手解剖全清点（The Quad-Hand Accountability Protocol）**：双人同框时，必须清点并明确安排 **2 + 2 = 4 只手** 的绝对位置。严禁留空任何一只手！
* **空间物理防火墙（Spatial Partitioning & Trait Firewall）**：通过“左三开 / 右三开”显式划分地盘，并对客体人物使用**排他性否定声明（Exclusionary Assertions）**，直接切断主体的特征渗透。
* **接触点物理能量锚（Kinetic Contact Anchor）**：在两人交汇的正中区域安插高亮、物理形态具体的能量事件（如火花迸射、刀刃咬合线、碰撞风压），作为身体分界的“物理隔离带”。

---

## 2. 三大多人防崩硬法则（Safety Protocols）

### 2.1 法则一：四手解剖全清点（The 4-Hand Quad-Lock Protocol）
双人互动时，必须在文本中按顺序逐一核定 4 只手的解剖归属与受力：
* **主体右手（A-Right）**：明确持握/出招动作（如 `Her right hand drives the silver rapier upward...`）。
* **主体左手（A-Left）**：明确副手平衡或辅助防御（如 `while her left hand is pulled tight at her hip in a clenched counterbalance fist`）。
* **客体右手（B-Right）**：明确对手持械手或受击防御（如 `The rival's right hand grips the dark steel broadsword locked against the rapier`）。
* **客体左手（B-Left）**：明确对手副手动作（如 `while her left hand presses flat against the spine of her own blade to reinforce the parry`）。

### 2.2 法则二：空间分栏与属性防火墙（Trait Firewall）
1. **禁止模糊代词统括**：严禁写 `They are fighting`、`The two girls slash at each other`。必须自始至终用同一组具象称呼：`the white-winged woman` 与 `the rival female swordsman`（或 `the dark-robed warrior`），不写角色名（G25：名字会触发整套先验并被放大 1.8–3.6 倍）。
2. **严格空间划分（Left vs Right）**：
   * `On camera left, the white-winged figure occupies two fifths of the picture width...`
   * `On camera right, facing her, the rival swordsman occupies two fifths of the picture width...`
3. **排他性否定声明（Exclusionary Negative Anchoring）**：
   * 为防止 A 的标志性先验（羽翼、发色、发夹）污染对手，必须在对手描写中显式写入**排他性阻断词**：
   * 范例：`She has straight jet-black hair tied low, wearing a fitted charcoal leather doublet without wings, without halo, and without any hair ornaments.`

### 2.3 法则三：接触点物理能量锚（The Kinetic Contact Anchor）
兵刃碰撞或肢体对抗的中心点，不能写抽象的“they clash”，必须写成具象的物理交互介质：
* **冷兵器交锋**：`where the polished silver edge grinds fiercely against the notched black fuller, an erupting burst of bright orange sparks and curling white friction smoke marks the exact point of impact`。
* **拳脚肉搏**：`her heel slams against the rival's raised forearm guard, displacing air in a visible circular shockwave`。
* **背靠背并肩**：`their shoulder blades press firmly against each other, creating distinct folds and tension lines across their contrasting white and black tunics`。

---

## 3. MOSS-Image 双人提示词标准化工程模板

在 MOSS 单键 JSON 架构中，双人对打或互动 prompt 严格按照以下五段式组织：

```text
第 1 段：全画明度基调与单向强光源声明（G1/G6/G8）。
第 2 段：世界环境与机位（平视、零倾斜、景深基准点）。
第 3 段：左侧主体（the white-winged woman）外貌、站位宽度（two fifths）、主攻手持械、副手安置、羽翼展开形态。
第 4 段：右侧客体（Rival）外貌对比、站位宽度、排他性否定（no wings）、格挡手、副手安置、视线死斗。
第 5 段：中心接触点物理锚（火花/气流/光轨）、光影落点（受光面与最暗面归属）、主色彩分布与全图统一颗粒胶片层。
```

---

## 4. 三大经典实战对峙套路（Combat Staging Archetypes）

### 套路 1：【双刃近身死斗·火花交锋】（Blade Clash & Cross-Parry）
* **战术态势**：近身格挡僵持，双方力量爆发对抗，眼神近距离对视。
* **视觉核心**：左白右黑高反差，刀刃在正中交叉，橘红火花飞溅成为画面最高对比处。
* **解剖锁定**：双人四手全部可见——A 单手前顶/反向收拳；对手双手握柄（或单手握柄+一手推剑背）。

### 套路 2：【掠空背靠背·联袂御敌】（Airborne Back-to-Back Standoff）
* **战术态势**：被群敌合围或高空滞空，两人背靠背互为后盾。
* **视觉核心**：A 的大羽翼向前微曲环护两侧，对手持长兵刃或双刀向画外戒备。
* **解剖锁定**：背脊与肩胛骨接触面衣料拉扯，两对双臂分别朝向左右画外。

### 套路 3：【瞬身错刃·低伏回马斩】（Cross-Pass Evade & Counter-Slash）
* **战术态势**：高速交错而过（交手完成 0.1 秒前夕），一高一低。
* **视觉核心**：一人低空掠地扫击，一人空中翻跃反切，两道不同颜色的刀光在中间交织错开。
* **解剖锁定**：低桩者单膝触地单臂横斩，高位者折翼俯冲反手格挡。
