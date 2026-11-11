<!-- P1 · 先验解绑 -->
# 强先验解绑协议（Anti-Prior De-Coupling Protocol）

> 解决模型「擅自多画、顽固脑补」的终极手段：从语义隐空间、物理几何占位到负向抑制的三重切断法。

> **适用引擎**（先读这条再往下）：
> - **MOSS-Image / Krea 2 / Midjourney / SD / Flux**：一律**只给正向**。先验要在画面里被别的实体「占位」掉——
>   直接正常描写角色的头发、发饰与头顶上方的真实环境背景（如树冠、天空、天花板），**绝不要写 `no halo` 或 `empty air with nothing hovering`**，避免欲盖弥彰激活光环先验。
> - **NAI / Anima**：负向串是合法工具，`-2::halo::` 这类加权负向才有意义。
> 下文的 `{halo}` / `{head halo}` / `{floating halo}` 模板**只用于负向栏**，不要混进正向 caption。


---

## 一、为什么模型会「擅自脑补」？（先验耦合机制）

扩散模型（Diffusion Models）本质上是基于概率分布的关联引擎。在数以亿计的图文对训练中，某些概念被极度强绑定：
* `羽翼（wings）` 90% 以上伴随 `光环（halo）` 出现（天使先验）；
* `杯子/饮品（cup/drink）` 95% 伴随 `手持（holding cup）` 出现；
* `华丽白裙（ornate white dress）` 极易诱发 `头纱（veil）` 与 `捧花（bouquet）`（新娘婚纱先验）；
* `铠甲（armor）` 容易自动带出 `头盔（helmet）`；
* `兽耳（animal ears）` 容易自动长出 `尾巴（tail）`。

**传统单纯写「no halo」为什么会失败？**
模型在去噪过程中，`halo` 这个词本身的嵌入向量（Embedding）会激活相关神经元，甚至导致“越否定反而越注意”。

> **注意适用范围**：这条说的是**首轮预防**。如果出图已经长出光环，正面描写就来不及了，必须用「形状 + 画法 + 三连否认」硬压（`moss-rules.md` G19 补充）——那是修复轮的做法，与这里的纪律不冲突。

---

## 二、三重解绑协议（Three-Step Protocol）

彻底解绑必须遵循以下三步，缺一不可：

```
步骤一：语义降级（切断上游诱发词）
   ↓
步骤二：物理占位（给被侵占的空间/肢体安排别的任务）
   ↓
步骤三：负向拦截（引擎级硬性抑制）
```

### 步骤一：语义降级（Semantic De-amplification）
* **原则**：绝对不要在提示词中出现该种族的“高阶统称词”。
* **操作**：
  * ❌ 不要写：`angelic, angel, seraph, divine maiden`（天使统称必附赠光环）；
  * ✅ 改写为：`a young woman with white feathered wings`（纯几何与解剖学描述）；
  * ❌ 不要写：`bride, bridal, wedding gown`；
  * ✅ 改写为：`white summer dress, white silk gown`。

### 步骤二：物理占位与动作指派（Physical Space Occupancy）
* **原则**：模型不会让空间或肢体处于“待定”状态。如果你不主动规定它是什么，模型就会按先验自动填上。
* **操作**：
  * **头部自然描写（防光环/防头纱 · 严禁欲盖弥彰）**：  
    不要写 `no halo` 或 `nothing hovering`，而是直接写发丝与背景物体的自然衔接（如 `her wind-ruffled hair frames her face against the clear oak bookshelves behind her`）。
  * **双手动作重定向（防手拿杯子/防乱摸）**：  
    `her hands swing freely at her sides with her walking motion, leaving her hands completely off the cup`
  * **发饰贴头锁定（防悬浮环状发饰）**：  
    `a flat gold hair clip pinned flush against the side of her hair, not floating`

### 步骤三：引擎级负向拦截（Engine-Specific Interception）
不同引擎的负向机制不同，按目标引擎精准投放：
* **NAI v5 / v4.5**：加入带权重的括号组：  
  `{halo}, {head halo}, {floating halo}, {glowing ring}, {nimbus}`
* **MOSS / Krea 2**：在正向描述中写入空间排除句（如步骤二），负向若支持则补短语。
* **Anima**：前置画师串对冲 + 负向置入标签。

---

## 三、五大高频解绑实战配方

### 1. 羽翼去光环（Wings without Halo）
* **诱发源**：`angel`, `angelic`, `holy glow`, `golden rim light around head`
* **首轮写法（推荐，不否定、只正面描写）**：
  `A young woman with long pale hair and feathered wings, the wind lifting the strands so they break against the dark oak leaves behind her; the crown of her head is framed by two branches and a strip of overcast sky.`
  要点：把「头顶上方是什么」写成一个**具体的实物**（树枝、天花板、云层、墙面），发丝与它有自然遮挡关系。正向锁定比任何否定句都稳。
* **修复轮（首轮已经出光环了才用，见 `moss-rules.md` G19 补充）**：
  `Above and behind her head there is no halo and no floating ring, the space over her hair is completely empty air with nothing hovering or glowing.`
  这一句会吃 lint 关 11 的 WARN —— 那是**故意**的。首轮写了是欲盖弥彰，修复轮不写压不回去，两者取舍见 SKILL.md「光环设定规范」。
* **负向补充**：
  `halo, head halo, floating halo, glowing ring, nimbus, ring of light`

### 2. 饮品去手拿 / 双手放开（Hands-Free Beverage Challenge）
* **诱发源**：`cup`, `drink`, `straw`, `boba`
* **正向解绑句**：
  `She drinks hands-free from a plastic cup resting supported and wedged firmly on top of her chest, while her hands remain completely off the cup, her arms swinging naturally at her sides.`
* **负向补充**：
  `holding cup, holding, hand on cup, grabbing cup`

### 3. 白裙去婚纱/头纱（White Dress without Veil/Bride）
* **诱发源**：`white gown`, `wedding`, `veil`, `ceremony`
* **正向解绑句**：
  `She wears an elegant casual white summer dress with a clean neckline. Her hair is uncovered and bare, with no veil and no fabric draped over her head.`
* **负向补充**：
  `veil, bridal veil, wedding dress, bride, bouquet, bridal`

### 4. 铠甲去头盔（Armor without Helmet）
* **诱发源**：`knight`, `full armor`, `paladin`
* **正向解绑句**：
  `She wears polished plate armor covering her torso and limbs. Her head is completely unarmored and bare, with her hair flowing freely in the wind, wearing no helmet and no visor.`
* **负向补充**：
  `helmet, visor, headgear, faceplate, armored helmet`

### 5. 兽耳去尾巴 / 尾巴去兽耳（Independent Animal Features）
* **诱发源**：`kitsune`, `catgirl`, `furry`
* **正向解绑句**：
  `She has cat ears on her head, but has no tail, her lower back completely smooth and human.`
* **负向补充**：
  `tail, animal tail, cat tail, fox tail`
