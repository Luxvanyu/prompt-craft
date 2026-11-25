# 反推特种构图配方库与角色替换

> 这里只放 `reverse-engineer.md` 装不下的两类东西：换角色时会变的东西、容易退化的特殊构图。
> 每条标证据等级：**【代码】**= 本包脚本会这么判、【实测】**= 返图量过、【外部】**= 来自外部目录或他人经验，本包未实测。

---

## 一、换角色与文本本地化

### 1. 角色识别度
写法用 Danbooru tag 格式 `<name> (<ip>)`，两个词之间不要漏括号——`lint.py` 的 `NAME_START` 只认「单词名」或「单词名 (ip)」，`hatsune miku,` 这种双词无括号写法不会被识别成角色名。

- 【外部】高识别度：《蔚蓝档案》主力学生（`hoshino`、`shiroko`、`hina`、`yuuka`、`noa`、`mika`、`aru`、`mutsuki`、`kayoko`、`momoi`、`midori`、`neru`、`aris`、`kazusa`、`rio`、`koyuki`、`wakamo`）。
- 【外部】中高识别度：《明日方舟》经典干员（`amiya`、`texas`、`lappland`、`exusiai`、`skadi`、`surtr`、`kal'tsit`、`ch'en`、`w`、`mostima`、`suzuran`、`specter`、`blaze`、`nian`、`dusk`、`ling`、`bagpipe`、`reed`）。
- 【外部】这份分级来自 [MOSS-Image Character Catalog](https://huggingface.co/spaces/hide1/MOSS-Image-Character-Catalog) 的收录情况，**不是本包的返图实测**。近期新角色的训练样本少，脸型和发色容易漂；发现还原不上去，就退回高识别度 IP，或者不写名字、改用具象描写（发色 + 瞳色 + 标志配饰）。
- 【实测】带名字的 character 会被放大 1.8–3.6 倍，并把整套角色先验（光环 / 画风 / 服装）一起拽进来。所以「必须长得像」和「位置尺寸对」经常互相打架——先确定要哪一头。

### 2. 清理与替换
1. 【代码】版权大词（`blue archive`、`arknights`）只写在 `character` 项的 caption 里。写进 `summary.caption` 或 `object` 框会被关 5 判为版权词污染，同时把全局画风带跑。
2. 【实测】光环只属于《蔚蓝档案》角色与《明日方舟》萨科塔（`exusiai`、`mostima`）；其余角色不写光环，也不写 `no halo` 这类否定句。
3. 【实测】参考图里的画师签名、平台水印（小红书角标）、人体辅助红线，反推时直接不写进任何框。
4. 【实测】换角色时一并替换招牌、衣领标、游戏 UI、海报卡司、涂鸦文字；不涉 IP 的功能文案（`REC`、`TIME`、`GET WELL SOON!`、`LOOK RIGHT`）保持原样。

---

## 二、五类特殊构图

### 配方 1：反重力 / 水平悬空（防「站地弯腰」退化）
【实测，单样本返图对照】只写 `floating horizontally`，模型会顺着重力先验把人画成站在地上弯腰。两条锁死：

1. **净空带**：角色 `bbox` 底边与地面 `bbox` 顶边之间留 ≥8% 画高的纯空隙——这是可量的，别靠形容词。
2. **解剖四事实**：躯干水平俯卧（`torso lies horizontal and prone, belly facing downward`）、小腿与鞋在身后 90° 弯曲悬空（`lower legs and shoes float horizontally in mid-air well above the ground`）、双臂垂直下垂（`both arms dangling straight down vertically perpendicular to her torso`）、受力点被拉成形（衬衫背面被拉成尖顶 `pulled taut upward into a sharp pointed conical tent peak`）。

### 配方 2：UI / 录像机 / 猫眼取景框套壳
【实测】适用手游育成界面、3D RPG 对话框、夜视 `REC` 录像机、门镜鱼眼走廊。`summary` 写清扫描线、暗角或界面高光质感；主画面按「道具/场景 → 角色」分层。HUD 文字拆框规则见 `reverse-engineer.md` §十（每处文字单独一个 `text` 框，合并会掉字），本文件不重复。

### 配方 3：多槽位群像矩阵
【实测】适用洗衣房 2×4 烘干机群像、双格对比、仰拍五人围圈、港风霓虹街。先跑 `align_bboxes.py grid` 逐格读边界，每个槽位独立成框；排序按「远景小框 → 前景大框」，避免近景被远景盖住。背景墙体字与招牌的层级处理见 `reverse-engineer.md` §3.1 第 5 步。

### 配方 4：实景照片 / 像素道具混二次元
【实测，单样本】适用实景走廊叠罗汉壁咚、电车吊环手办实拍、雪地像素道具雪天使。`summary` 里声明混合媒介（`mixed-media illustration pairing anime characters over a real photograph`），并把真实环境的光色、接触面投影、反光落到二次元人物身上——贴纸浮空感的来源不是画风差异，是投影和反光没跟上。

### 配方 5：水中仰浮 & 极限低机位广角
- 【实测】**水中仰浮**（睡莲 / 花海 / 泳池）：写 `overhead` 或 `looking straight down` 之后，**必须紧跟一句只有这个角度才看得见的画面事实**（头顶、双肩、被压缩的肢体都行），否则模型会退化成平视站姿。配 `horizon line above the top edge` 与焦散光斑、水波高光锚点。（`reverse-engineer.md` §十 也是这条：视角词本身不锁机位，证据句才锁。）
- 【代码】**极限低机位广角**（高架桥倒立街舞 / 仰拍围圈）：`from below` 与 `foreshortening` / `wide angle distortion` 同写会被关 3 判互斥——不是玄学，脚本会拦。改用 `low-angle shot from ground level looking up`，再给具体近大远小落点（鞋底贴右上前景、支撑手压实地面）。
