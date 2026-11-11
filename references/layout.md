# MOSS-Image Layout 官方规范手册

> 本规范对齐 MOSS-Image 官方 `skills/moss-image-prompt-enhancer/references/layout.md`。
> 在起草空间布局草稿（Layout Draft）前，必须通读本规范。

---

## 一、何时使用 Layout（选型铁律）

* **默认使用 Caption（纯文本段落）**：普通场景、单人/双人写真、复杂插画、风景与概念图。**“画面细节丰富并不自动需要 Layout”**。
* **使用 Layout 的严格场景**：
  1. **明确的文字排版（Text Placement）**：海报、杂志封面、带有标语/路牌/排版字块的画面；
  2. **分镜与多格（Multi-panel / Collage）**：四格漫画、双格对比、画中画卡牌；
  3. **严格的物体空间互锁（Strict Spatial Relationships）**：多物体/多角色有明确的左右、上下遮挡与边界对应关系。

---

## 二、Layout 草稿结构（严格 6 个顶层字段）

草稿 JSON 必须且只能包含以下 6 个根字段：

```json
{
  "width": 1536,
  "height": 1024,
  "bbox_coord_space": "abs",
  "bbox_format": "xyxy",
  "summary": {
    "canvas": "single",
    "caption": "全局画面描述，包含整体影调、色彩、光影衰减与风格定调..."
  },
  "items": [
    {
      "label": "character",
      "caption": "角色的微观动作、神态、服装与材质受光描述...",
      "bbox": [150, 160, 680, 940]
    },
    {
      "label": "object",
      "caption": "环境物体的结构与光影描述...",
      "bbox": [700, 0, 1536, 1024]
    }
  ]
}
```

### 1. 字段约束表

| 字段 | 类型 | 规范要求 |
|---|---|---|
| `width` | 正整数 | 必须是 **16 的倍数**（如 1024, 1536, 1792） |
| `height` | 正整数 | 必须是 **16 的倍数**（如 768, 1024, 1536） |
| `bbox_coord_space` | 字符串 | 草稿阶段固定为 `"abs"`（绝对像素坐标） |
| `bbox_format` | 字符串 | 草稿阶段固定为 `"xyxy"` |
| `summary` | 对象 | 必含 `caption`；可选 `canvas` (`"single"`, `"multi_panel"`, `"collage"`), `meta`, `palette` |
| `items` | 扁平数组 | 必须是非空数组，不能嵌套 |

### 2. Item 字段约束

| 字段 | 类型 | 规范要求 |
|---|---|---|
| `label` | 枚举字符串 | 只能是 `"character"` / `"object"` / `"text"` 三者之一 |
| `caption` | 字符串 | 该局部区域的具象英文描写，符合七维与微观物理规范 |
| `bbox` | 4元整型数组 | `[x_min, y_min, x_max, y_max]`，以画布左上角为原点 `(0, 0)`。要求 `0 <= x_min < x_max <= width`，`0 <= y_min < y_max <= height`。禁止手写居中或归一化坐标！ |
| `text` | 字符串 | **当且仅当 `label == "text"` 时必填**。必须是实际需要渲染的字串，严禁占位符。保持原始语言与标点。 |
| `palette` | 字符串数组 | 可选，该区域包含的 HEX 颜色数组（如 `["#FFFFFF", "#1A1A1A"]`） |
| `tags` | 字符串数组 | 可选，辅助分类标签 |

---

## 三、编译产物与交付规范（Compile & Deliver）

### 1. 编译命令
必须使用随技能附带的编译器执行编译，严禁手写居中坐标：

```bash
python3 scripts/compile_prompt.py draft.json --output prompt.txt
```

### 2. 编译产物形态
* **对 Caption 草稿**：
  * 输出为**纯文本段落（Plain Text）**。
  * 交付给用户的正是这一段纯英文文本，可直接粘贴进 MOSS-Image 正向输入框。
* **对 Layout 草稿**：
  * 输出为**单行压缩 JSON（One physical line of JSON）**。
  * 编译器会自动执行以下转换：
    1. 剥离 `width` 与 `height`（MOSS-Image prompt 框不接受顶层尺寸元数据）；
    2. 将 `bbox` 转换为中心原点坐标系 `abs_centralized`，格式重写为 `yxyx`；
    3. 压缩空白，输出紧凑单行 JSON。
  * **交付给用户时的铁律**：
    * 必须提供编译后的单行 JSON（或保留单行格式）；
    * **必须在 prompt 外部单独显式注明画幅尺寸**（例如：`推荐分辨率：1536×1024`），因为 MOSS 的宽高是在模型界面的分辨率滑块/设置中配置的，提示词本身不带尺寸！

---

## 四、自检核对清单（Layout Checklist）

- [ ] 画布宽高是否均为 16 的倍数？
- [ ] 草稿 `bbox_coord_space` 是 `"abs"`，`bbox_format` 是 `"xyxy"` 吗？
- [ ] 每个 `bbox` 是否都在 `[0, width]` 与 `[0, height]` 范围内，且宽高为正？
- [ ] `summary.canvas` 是否为合法字符串（`single`/`multi_panel`/`collage`），没有写成对象？
- [ ] 所有 `items[].label` 是否都在 `character` / `object` / `text` 三者之中？
- [ ] 若有文字项，是否携带了真实的 `text` 内容而非占位符？
- [ ] 人物是否避开了中线死区（X 中心在 0.42–0.58 之外）？
- [ ] 是否在 prompt 外部单独标明了所需的 `width × height`？
