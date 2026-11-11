# 我是什么 / 怎么用我

一句话：**把「想画什么」变成一份能直接编译的提示词，并且能在出图后判断它错在哪一句。**

---

## 三十秒版

1. 读 `references/entry.md`，填十一个槽位 → 得到一份 `draft.json`
2. `python scripts/preview.py draft.json --out layout.png` → 看人物有没有压中线
3. `python scripts/lint.py draft.json` → 十道关，退出码 1 就是有 FAIL
4. 编译出图
5. 出图不对：`probe.py` 量数值 → `references/symptoms.md` 找症状 → 只改那一句

普通场景默认写**纯 caption**（`{"caption": "..."}`，200–320 词），不要一上来就 Layout。

---

## 我信什么

| 信条 | 意思 |
|---|---|
| 关系 > 形容词 | 写「她比身后的墙亮一档」而不是「她站在柔和的光里」 |
| 数量 > 程度 | 写「暗部占一半」而不是「画面很暗」 |
| 画面事实 > 意图 | 写「鞋底平放在地上」而不是「她蹲着」 |
| 一图一主张 | 每件道具都要是那件事的证据 |
| 先写故事再挑瞬间 | 故事定了，图里该有什么自己会浮出来 |
| 规则是诊断工具 | 每条规则都有适用边界，边界写在它自己的段落里 |

**不写**：质量词、画师串、器材名、`full body`、厘米数、给设计文档看的元话语。

---

## 我会犯的错（已记录在案）

- 无端把人物画大 —— 先量，别猜（`probe.py` + `lint.py` 关 8）
- 用数值断言「画面里有没有某物」 —— **不许**，数值只能答「在哪 / 多大 / 多亮」（G53）
- 把规则当模板套 —— 每条规则都有适用边界
- 看到「没有」两个字就以为能压住模型 —— 否定句经常变成点名（G90/G96 补）

---

## 打包内容

```
SKILL.md                  入口（七维决策 + 反默认 + 模型翻译 + 自检）
references/entry.md       从零起草（推荐入口，十一槽）
references/aesthetic.md   审美内核（为什么不好看 + 12 配方 + 风格提取 + 批评法）
references/style-heads.md 12 个风格主头 + 6 层质感
references/word-budget.md 字数预算
references/composition.md 景别 / 视角 / 构图
references/symptoms.md    症状 → 改哪句
references/moss-rules.md  MOSS 实测规则正文 + 索引 G1–G98
references/casebook.md    G1–G98 实测证据
references/gap-audit.md   缺口台账
scripts/probe.py          单张实测
scripts/lint.py           十道关自检
scripts/preview.py        布局预览
scripts/compile_prompt.py 编译成官方格式
```

完整说明见 `README.md`。

---

## 和另外两个包的关系

`prompt-craft` 是 `moss-replica`（MOSS 实测规则）与 `aesthetic-core`（审美方法）的**合并入口**。
两个源包还在，规则有更新时在源包里改，再同步过来；新任务一律从 `prompt-craft` 进，不必分别加载。
