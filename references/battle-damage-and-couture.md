<!-- P5 · 战损物理与机能装束 -->
# 战损物理与机能幻想装束系统（Phase 5: Battle Damage & Tactical Couture）

本参考手册规范了 `prompt-craft` 体系在战斗损伤（Battle Damage）、破损物理学、机能幻想装束层级构建及羽翼受损真实感方面的标准与 MOSS-Image 物理级提示词编写规范。

---

## 1. 核心痛点与防崩准则

在扩散模型中，描写“战损”或“机能战术装备”时极易出现以下翻车现象：
1. **战损尺度失控与走光冲突**：
   * 盲目使用 `torn clothes` / `damaged`，模型容易将衣服撕成大面积不雅或触发审核过滤，失去战斗美感。
   * **破局法则**：严格规定破损发生在边缘与功能层（抽丝毛边、下摆撕裂、袖口破损），并引入**战术亚麻绷带（Linen Field Bandage）**作为专业战斗痕迹。
2. **羽翼战损的“拔毛鸡”畸变**：
   * 直接写 `broken wings`，模型容易把翅膀画成残疾肉瘤或无毛鸡翅。
   * **破局法则**：战损必须落在具体部位——“最外侧初级飞羽尖端焦黑断裂（scorch marks and frayed tips on the outermost primary feathers）”，并伴随“空中漂浮的脱落脱散羽毛”，主体羽翼骨架保持舒展坚毅。
3. **装备与身体先验粘连**：
   * 战术绑带、护甲皮带容易直接融进皮肤变成黑色条纹。
   * **破局法则**：必须采用**分层物理穿搭法（Layered Physical Dressing）**，明确写出内衬、硬质护胸甲与皮革扣带的层叠包裹关系。

---

## 2. 战损三级渐进体系（The 3-Tier Hierarchy）

| 战损级别 | 适用场景 | 衣物表现 | 羽翼表现 | 兵刃与身体 |
| :--- | :--- | :--- | :--- | :--- |
| **Level 1: 微损 (Light Dust)** | 战斗初结、清理战场 | 白裙下摆轻微沾染灰烬与泥渍，衣物整体完整无撕口 | 3–5 片零星白色绒羽在热气流中脱落飘零，羽梢轻微紊乱 | 剑刃寒光锋利无缺；脸颊与下颌有一两道浅灰炭黑蹭痕 |
| **Level 2: 中损 (Moderate Wear)** | 陷入鏖战、破甲硬拼 | 衣袖与裙摆边缘呈现细碎抽丝、裂口毛边与烟熏暗斑 | 外侧初级飞羽边缘焦黑断裂，羽毛受气流撕扯凌乱 | 单侧小臂缠绕紧绷的浅色亚麻战术绷带；剑刃出现微小崩口 |
| **Level 3: 重损 (Climax Limit)** | 绝境决胜、极限意志 | 战袍多处受力破损，战术绷带多处缠绕，布料在风中激烈抽动 | 局部羽毛剥落露出内部骨架阴影，多枚断羽悬空下落 | 剑身带有一道发丝般细微应力裂纹；眼神如电、屹立不倒 |

---

## 3. 高阶机能幻想装束分层法则（Layered Tactical Couture）

为了在画面中建立高级、严谨的战斗幻想设计感，角色装束按四层物理结构构建：

1. **第一层：贴身内衬（Under-Tunic / Silk Base）**
   * 柔软透气的白色丝质或机能纤维内衬，作为打底与高光衬托。
   * `tailored white silk under-tunic`
2. **第二层：硬质防护胸甲（Tactical Cuirass / Corset）**
   * 贴合身躯的哑光黑皮革或暗金附魔胸甲，提供力量感与结构轮廓。
   * `fitted matte-black and polished-gold articulated leather cuirass`
3. **第三层：模块化战术外挂（Modular Armored Sleeves & Harness）**
   * 十字交叉扣合在肋下的武装带，配金属搭扣；模块化分体式袖甲。
   * `cross-strapped leather utility harnesses buckled securely around her ribcage, modular white armored detached sleeves with gold-trimmed elbow cops`
4. **第四层：下肢防护与机能战靴（Reinforced Thighhighs & Greaves）**
   * 带战术护膝插板的过膝袜，配合防滑合金底战术战靴。
   * `reinforced white thighhighs with tactical knee plates, dark armored boots`

---

## 4. MOSS-Image 实战经典模板

### 模板 1：【Level 2 中度战损·硝烟残阳与断羽飘零】
* **核心意象**：战后硝烟残阳，白裙抽丝与焦黑羽尖，紧绷亚麻绷带与插地的崩口细剑。
* **光影配置**：低俯角黄昏强逆光，焦黑断羽与碎石高对比阴影。

### 模板 2：【机能黑金轻甲·暴风雪前哨决战】
* **核心意象**：暗金黑皮革组合轻甲、十字战术武装带、手持发光信标、对称展翼覆雪。
* **光影配置**：冷蓝冬日天光搭配金属搭扣与甲片的锐利冷金高光。
