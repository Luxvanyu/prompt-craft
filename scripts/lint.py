#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""MOSS 提示词交付前自检（lint）：把草稿 JSON 和参考图实测值做对照，抓自相矛盾与漏项。

用法:
    python lint.py <草稿.json> [--ref 参考图] [--strict]

十道关:
    关 1  结构     width/height 16 倍数、bbox 在画布内、label 合法、text item 带 text
    关 2  数值     提示词里声明的明度/比例 与 参考图实测 是否一致
    关 3  矛盾     明度词冲突、饱和方向冲突、机位词互斥、强触发 tag 组合
    关 4  覆盖     参考图的 6 个关键特征在提示词里有没有对应描述
    关 5  禁用     质量词、器材名、版权大词、负面词混入、中文标点
    关 6  机位     俯仰 / 距离 / 倾斜 / 视平线 四要素是否写全
    关 7  世界逻辑 场景方向性、一张图一件事、表情写肌肉、高调黑锚点、
                  统一色与唯一色并存、硬光边缘、人物比例尺、道具支撑
    关 8  曝光     明度定调句、暗部面积、烧白词、nw 红线
    关 9  色彩落点 色相词是否落在被照亮的大面积上
    关 10 构图落位 人物是否落在中线禁区（G65）

选项:
    --ref 参考图.png      对参考图实测值做关 2 / 关 4 对照
    --intent blown,leak,tilt,soft
                          声明这些是「有意的」：blown=故意过曝、leak=漏光、
                          tilt=故意歪、soft=故意失焦（放行关 3 / 关 8）

退出码 0 = 全过；1 = 有 FAIL。
"""
import json
import os
import re
import sys

import numpy as np
from PIL import Image

for _s in (sys.stdout, sys.stderr):
    try:
        _s.reconfigure(encoding='utf-8')
    except Exception:
        pass

FAIL, WARN, OK = 'FAIL', 'WARN', 'ok'

QUALITY = ['masterpiece', 'best quality', 'very aesthetic', 'ultra-detailed',
           'highly detailed', 'high contrast', 'absurdres', '8k', '4k',
           'award winning', 'top quality', 'amazing quality']
GEAR = ['contax', 'portra', 'pro 400h', 'polaroid', 'leica', 'canon eos', 'nikon',
        'sony a7', 'unreal engine', 'octane', 'blender cycles', 'redshift',
        'subsurface scattering']
# 'iso 1600' / 'ilford' 已移除：颗粒层的定稿写法会用到感光度与胶片型号，
# 它们不是引擎名，MOSS 也不会因此变差；真正要禁的是 unreal/octane 这类渲染器。
COPYRIGHT = ['blue archive', 'genshin impact', 'pokemon', 'nintendo', 'naruto',
             'honkai', 'arknights', 'fate/grand order']
NEGATIVE = ['censored', 'mosaic censoring', 'bar censor', 'watermark', 'signature',
            'worst quality', 'bad anatomy', 'lowres', 'blurry']
COSPLAY = ['cosplay', 'cosplayer', 'コスプレ']

DARK_WORDS = ['low key', 'low-key', 'deep shadow', 'pitch-black', 'pitch black',
              'mostly dark', 'unlit', 'almost black', 'dark throughout']
LIGHT_WORDS = ['high key', 'high-key', 'mostly bright', 'washed out', 'blown out',
               'sunlit throughout', 'overexposed', 'bright throughout']
MID_WORDS = ['middle value', 'mid-tone', 'midtone', 'mid value', 'middle of the tonal',
             'lower middle', 'nothing is dark', 'no true darks', 'no real darks',
             'sits in the middle', 'held in the middle']

# 「暗部更饱和」：暗面承载颜色
SAT_SHADOW = ['saturated in the shadow', 'stronger in the shadow', 'richer in the shadow',
              'deeper and more saturated', 'shadows keep', 'shadows carry',
              'shadowed side keeps', 'shadowed side carries', 'dark side carries',
              'most saturated colour', 'most saturated color',
              'colours live in the shadow', 'colors live in the shadow']
# 「亮部更饱和」：亮面是艳的
SAT_LIGHT = ['saturated in the light', 'vivid in the light', 'richest in the highlight',
             'lights carry the colour', 'lights carry the color',
             'brighter and more saturated', 'the sun makes the colours hotter',
             'the sun makes the colors hotter']
# 「亮部被冲淡」——这是暗部更饱和的**证据**，不是反证
PALE_LIGHT = ['wash out', 'washes out', 'washed out', 'bleach', 'chalky', 'pale in the light',
              'sun-bleached', 'pale gold', 'chalky cream']


# 否定前缀：`not blown out`、`no ceiling`、`never becomes`、`without haze`
# 这些是「反着说」的约束句，不能当成正向声明，否则会误报成自相矛盾。
NEG_BEFORE = re.compile(
    r"(?:\bnot|\bno|\bnever|\bwithout|\bnothing|\bnone\s+of|\bnor)\s+"
    r"(?:\w+[\s,]+){0,3}$", re.I)


def has(txt, words):
    """词边界匹配，避免 sunlit 命中 unlit、a bloom（花）命中 bloom（光晕）；
    同时跳过被否定的出现（not blown out / no ceiling）。"""
    for w in words:
        for m in re.finditer(r'(?<![a-z])' + re.escape(w) + r'(?![a-z])', txt):
            pre = txt[max(0, m.start() - 48):m.start()]
            if NEG_BEFORE.search(pre):
                continue
            return True
    return False
HARD = ['hard edge', 'crisp', 'razor', 'sharp shadow', 'hard-edged', 'knife']
SOFTW = ['bloom', 'haze', 'humid', 'diffused', 'soft edge', 'glow', 'fog']

BAD_COMBO = [
    # (必须出现的词, 同时出现才算触发, 说明)
    (['full body'], ['from below', 'from above', 'overhead', 'dutch angle',
                     'fisheye', 'wide angle'],
     'full body 会吞掉机位词，复杂机位图里要删掉'),
    (['from below', 'low angle'], ['foreshortening', 'wide angle distortion'],
     'from below + foreshortening/wide angle distortion 会出脚底板视角'),
]

# 机位类的 overhead 才危险；写太阳/光「几乎正上方」是合法用法，不能误报
OVERHEAD_CAM = ['directly overhead', 'looking straight down',
                'shot from directly above', 'camera directly above']
OVERHEAD_LIGHT_CTX = re.compile(
    r'\b(sun|sunlight|light|noon|midday|lamp|bulb|neon|sky)\b', re.I)


def load_draft(p):
    with open(p, 'r', encoding='utf-8') as f:
        return json.load(f)


def all_text(d):
    parts = [d.get('summary', {}).get('caption', ''), d.get('caption', '')]
    for it in d.get('items', []):
        parts.append(it.get('caption', ''))
        if it.get('text'):
            parts.append(it['text'])
    return '\n'.join(parts)


def ref_profile(path):
    im = Image.open(path).convert('RGB')
    W, H = im.size
    a = np.asarray(im).astype(np.float32) / 255.
    lum = 0.2126 * a[..., 0] + 0.7152 * a[..., 1] + 0.0722 * a[..., 2]
    mx, mn = a.max(2), a.min(2)
    sat = np.where(mx > 0, (mx - mn) / np.maximum(mx, 1e-6), 0)
    gy, gx = np.gradient(lum)
    gm = np.hypot(gx, gy)
    grid = np.array([[lum[i * H // 6:(i + 1) * H // 6, j * W // 6:(j + 1) * W // 6].mean()
                      for j in range(6)] for i in range(6)])
    bi, bj = np.unravel_index(np.argmax(grid), grid.shape)
    return dict(W=W, H=H,
                dark=float((lum < .15).mean()), mid=float(((lum >= .15) & (lum <= .75)).mean()),
                bright=float((lum > .75).mean()), nw=float((lum > .95).mean()),
                p1=float(np.percentile(lum, 1)),
                sat=float(sat.mean()),
                lit=float(sat[lum > np.percentile(lum, 80)].mean()),
                shadow=float(sat[lum < np.percentile(lum, 25)].mean()),
                soft=float((gm < .02).mean()),
                brightest=(int(bi), int(bj)))



def gate10(draft, add):
    """关 10 构图落位：人物 bbox 中心不能压在画布中线上。"""
    try:
        W = float(draft.get('width') or 0)
        H = float(draft.get('height') or 0)
    except (TypeError, ValueError):
        return
    if W <= 0 or H <= 0:
        return
    chars = [it for it in draft.get('items', []) if it.get('label') == 'character']
    if not chars:
        return
    # 取面积最大的那个 character 当主体
    def area(it):
        b = it.get('bbox') or [0, 0, 0, 0]
        return abs(b[2] - b[0]) * abs(b[3] - b[1])
    main = max(chars, key=area)
    b = main.get('bbox') or [0, 0, 0, 0]
    cx = (b[0] + b[2]) / 2.0
    cy = (b[1] + b[3]) / 2.0
    off = abs(cx - W / 2.0) / W
    if off < 0.06:
        add(10, 'WARN', '人物 bbox 中心离画布中线不足 6%，实测就是居中生图',
            'm04882：要么把 bbox 整体平移，要么写清她站画面的哪三分之一；形容词说「不居中」模型不听，只听 bbox')
    elif off < 0.08:
        add(10, 'WARN', '人物 bbox 中心仍落在 0.42–0.58 禁区里（G65）',
            'm09552：横图放到 0.33 或 0.66，竖图放到 0.30–0.35 / 0.65–0.70')
    if off < 0.06 and cy > 0 and abs(cy - H / 2.0) / H < 0.05:
        add(10, 'WARN', '人物同时在横竖两个方向都居中（正中靶心）',
            '给一条三分线：横向放一侧三分之一，竖向让头顶或脚底压到三分线')


def lint(draft, ref=None, intents=()):
    intents = set(intents or ())
    res = []
    add = lambda gate, lvl, msg, fix='': res.append((gate, lvl, msg, fix))

    txt = all_text(draft).lower()
    W, H = draft.get('width'), draft.get('height')
    # 纯 caption 草稿（官方 schema：{"caption": "..."}，无 width/height/items）
    cap_only = bool(draft.get('caption')) and not draft.get('items')

    # ---------- 关 1 结构 ----------
    if cap_only:
        for k in ('children', 'parent', 'id', 'elements', 'items', 'summary'):
            if k in draft:
                add(1, FAIL, 'caption 草稿里不能出现字段 %r' % k,
                    'caption 草稿只有 {"caption": "..."} 一个键')
        if len(draft['caption'].split()) < 120:
            add(1, WARN, 'caption 只有 %d 词' % len(draft['caption'].split()),
                '纯 caption 靠自然语言承担全部信息，低于 120 词通常写不出空间关系')
    elif not W or not H:
        add(1, FAIL, '缺 width/height', '草稿必须带 width/height（16 的倍数），编译器要用来换算坐标')
    else:
        if W % 16 or H % 16:
            add(1, WARN, 'width/height 不是 16 的倍数（%d×%d）' % (W, H), '取最近的 16 倍数')
        if draft.get('bbox_coord_space') != 'abs' or draft.get('bbox_format') != 'xyxy':
            add(1, FAIL, 'bbox_coord_space / bbox_format 不是 abs / xyxy',
                '草稿固定用 abs + xyxy（左上原点），编译器负责转 centralized + yxyx')
        for k in ('children', 'parent', 'id', 'elements'):
            if k in draft:
                add(1, FAIL, '草稿里出现编译器不接受的字段 %r' % k, '删掉它')
        for i, it in enumerate(draft.get('items', [])):
            lab = it.get('label')
            if lab not in ('object', 'character', 'text'):
                add(1, FAIL, 'item %d 的 label=%r 非法' % (i, lab), '只能是 object / character / text')
            bb = it.get('bbox') or []
            if len(bb) != 4:
                add(1, FAIL, 'item %d 的 bbox 不是四个数' % i, '写成 [x_min, y_min, x_max, y_max]')
                continue
            x0, y0, x1, y1 = bb
            if not (x0 < x1 and y0 < y1):
                add(1, FAIL, 'item %d 的 bbox 宽或高为负/零' % i, '左上 < 右下')
            if x0 < 0 or y0 < 0 or x1 > W or y1 > H:
                add(1, WARN, 'item %d 的 bbox 越界 %s（画布 %d×%d）' % (i, bb, W, H),
                    '要贴边就正好贴到 0 或 W/H，不要超出')
            if lab == 'text' and not it.get('text'):
                add(1, FAIL, 'item %d 是 text 但没写 text 字段' % i, '补上字符串，换行用 \\n')
            if not it.get('caption'):
                add(1, FAIL, 'item %d 没有 caption' % i, '每个 item 都要有 caption')
        if not draft.get('summary', {}).get('caption'):
            add(1, FAIL, 'summary.caption 为空', 'summary.caption 是整体场景与风格，必须写')
        # 角色名 tag：character caption 必须以名字开头，否则模型认不出是谁
        NAME_START = re.compile(r'^(a|an|the|she|he|they|his|her|its|this|that)\b', re.I)
        for i, it in enumerate(draft.get('items', [])):
            if it.get('label') != 'character':
                continue
            cap = (it.get('caption') or '').strip()
            low = cap.lower()
            if 'original character' in low or 'oc character' in low:
                continue
            if NAME_START.match(cap):
                add(1, WARN,
                    'item %d 的角色 caption 以「%s」开头，没有角色名' % (i, cap.split()[0] if cap else ''),
                    'E6：改成「aru (blue archive), a girl sitting...」这种「名字, 外观」结构；'
                    '原创角色就在 caption 开头写 original character')


    # ---------- 关 2 数值 ----------
    if ref:
        band = max([('dark', ref['dark']), ('mid', ref['mid']), ('bright', ref['bright'])],
                   key=lambda x: x[1])
        name_cn = {'dark': '暗调', 'mid': '中调', 'bright': '亮调'}[band[0]]
        hit = {'dark': DARK_WORDS, 'mid': MID_WORDS, 'bright': LIGHT_WORDS}[band[0]]
        if not has(txt, hit):
            add(2, WARN, '参考图是「%s」主导（%.0f%%），但提示词里没有明确声明这一档'
                % (name_cn, band[1] * 100),
                '加一句「the picture sits in the middle values with nothing truly dark」' if band[0] == 'mid'
                else '加一句「%s takes up more than half the frame」' % name_cn)

        # 声明了相反的档（只有真的相反才算错，中调主导时两个极端都算相反）
        opp = {'dark': LIGHT_WORDS, 'bright': DARK_WORDS,
               'mid': DARK_WORDS + LIGHT_WORDS}[band[0]]
        if opp and has(txt, opp) and not has(txt, hit):
            add(2, FAIL, '提示词声明了与参考相反的明度档（参考是%s %.0f%%）'
                % (name_cn, band[1] * 100), '删掉相反的形容词')

        # 饱和度方向
        ref_lit_more = ref['lit'] > ref['shadow']
        says_shadow = has(txt, SAT_SHADOW) or has(txt, PALE_LIGHT)
        says_light = has(txt, SAT_LIGHT)
        if ref_lit_more and says_shadow and not says_light:
            add(2, FAIL, '参考是亮部更饱和（%.3f vs %.3f），提示词却写暗部更饱和/亮部被冲淡'
                % (ref['lit'], ref['shadow']),
                '改成「the sun keeps the colour hot in the lights and the shadows go grey-blue」')
        if (not ref_lit_more) and says_light and not says_shadow:
            add(2, FAIL, '参考是暗部更饱和（%.3f vs %.3f），提示词却写亮部更饱和'
                % (ref['shadow'], ref['lit']),
                '改成「the lights wash out pale and the shadows carry the deepest colour」')

        # 近白
        if ref['nw'] < 0.01 and re.search(r'\b(pure white|blown out|to white)\b', txt):
            add(2, WARN, '参考近白只有 %.1f%%，提示词却提到纯白' % (ref['nw'] * 100),
                '改成「nothing reaches pure white, the highest value is a pale cream」')
        # 真黑
        if ref['p1'] > 0.13 and re.search(r'\b(pure black|pitch black|black void)\b', txt):
            add(2, WARN, '参考 p1=%.3f（全图无真黑），提示词却提到纯黑' % ref['p1'],
                '改成「the deepest shadow stays a warm brown / cold blue」')

        # 亮场位置
        bi, bj = ref['brightest']
        row = ['upper', 'upper', 'upper middle', 'lower middle', 'lower', 'lower'][bi]
        col = ['left', 'left', 'left of centre', 'right of centre', 'right', 'right'][bj]
        want = (row, col)
        if not any(w in txt for w in [want[0], want[1]]) or not re.search(
                r'(brightest|highlight|sun|light)[^.]{0,80}(%s|%s)' % (want[0], want[1]), txt):
            add(2, WARN, '参考最亮格在第 %d 行第 %d 列（%s %s），提示词没把亮场位置写成坐标事实'
                % (bi + 1, bj + 1, want[0], want[1]),
                '加「the brightest patch sits in the %s %s」' % (want[0], want[1]))

        # soft
        if ref['soft'] > 0.55 and not has(txt, SOFTW):
            add(2, WARN, '参考柔化占比 %.2f（大范围 bloom/雾），提示词没写柔化' % ref['soft'],
                '加 bloom / haze / humid 类描述')
        if ref['soft'] < 0.35 and has(txt, ['bloom', 'haze', 'fog']):
            add(2, WARN, '参考柔化占比只有 %.2f（硬光），提示词却写了 bloom/haze' % ref['soft'],
                '删掉柔化词，改成 hard edge / crisp')

    # ---------- 关 3 矛盾 ----------
    if has(txt, DARK_WORDS) and has(txt, LIGHT_WORDS) and not (intents & {'blown', 'soft', 'leak'}):
        add(3, FAIL, '同时出现暗调词与亮调词，模型会取平均',
            '只保留一个，另一个删掉')
    if has(txt, SAT_SHADOW) and has(txt, SAT_LIGHT):
        add(3, FAIL, '同时声明「暗部更饱和」与「亮部更饱和」', '二选一')
    # bloom 有「花」和「光晕」两个意思，只有光晕义才与硬边冲突
    bloom_light = re.search(
        r'(soft |wide |faint |gentle |slight )?bloom(s|ing)? (bleed|around|out|into|over|the edge)|'
        r'(bleeds?|glows?|halation|halo)[^.]{0,40}(around|over|into)', txt) is not None
    if has(txt, HARD) and (bloom_light or has(txt, ['haze'])):
        add(3, WARN, '同时写硬边与 bloom/雾', '除非是「硬光 + 只在高光处 bloom」，否则会互相抵消')

    for need, forbid, why in BAD_COMBO:
        if any(n in txt for n in need):
            if not forbid or any(f in txt for f in forbid):
                if need == ['dutch angle']:
                    continue  # 单独处理
                add(3, FAIL, '强触发 tag 组合风险：%s' % why,
                    '按 B 组的正解改写（用画面事实代替机位形容词）')
    if 'dutch angle' in txt:
        if not has(txt, ['level edge', 'plumb line', 'rolled', 'rotated', 'degrees']):
            add(3, FAIL, 'dutch angle 单独出现会被摆正',
                '写「rolled about twenty degrees」+ 点名三条长线 + 连竖直物一起歪')

    # overhead：只有"机位在头顶"才危险，"太阳几乎正上方"是合法写法
    for m in re.finditer('|'.join(re.escape(k) for k in OVERHEAD_CAM), txt, re.I):
        pre = txt[max(0, m.start() - 60):m.start()]
        if OVERHEAD_LIGHT_CTX.search(pre):
            continue  # 在说光，不是在说机位
        add(3, FAIL, '机位写成 overhead 会退化成正常立姿',
            '改写成「前上方约 60 度」+ 四条只有这个角度才看得见的事实')
        break

    # ---------- 关 4 覆盖 ----------
    if ref:
        checks = [
            ('明度档', has(txt, DARK_WORDS + LIGHT_WORDS + MID_WORDS)),
            ('光源有画内出处', re.search(r'\b(sun|window|lamp|neon|screen|candle|fire|moon|sky)\b', txt) is not None),
            ('衰减', re.search(r'\b(dies|fades|falls off|within (a|an|arm|forearm|reach))\b', txt) is not None),
            ('材质反应', re.search(r'\b(matte|glossy|chalky|wet|dusty|worn|bleached|translucent)\b', txt) is not None),
            ('空间层次', re.search(r'\b(foreground|background|behind|in front of|nearest)\b', txt) is not None),
        ]
        for name, okk in checks:
            if not okk:
                add(4, WARN, '缺「%s」' % name, '补一句，否则模型自己填平均值')

    # ---------- 关 5 禁用 ----------
    for grp, words in (('质量词', QUALITY), ('器材/引擎名', GEAR),
                       ('负面词', NEGATIVE), ('cosplay', COSPLAY)):
        hit = [w for w in words if re.search(r'(?<![a-z])' + re.escape(w) + r'(?![a-z])', txt)]
        if hit:
            add(5, FAIL, '出现%s：%s' % (grp, ', '.join(hit)), '删掉，MOSS 对这些无效或有害')
    # 版权大词只查 summary 与非人物块：人物块里写角色 tag 是必须的
    non_char = [draft.get('summary', {}).get('caption', '')] + [
        it.get('caption', '') for it in draft.get('items', [])
        if it.get('label') != 'character']
    nc_txt = ' '.join(non_char)
    hit = [w for w in COPYRIGHT if re.search(r'(?<![a-z])' + re.escape(w) + r'(?![a-z])', nc_txt)]
    if hit:
        add(5, FAIL, '场景/风格里出现版权大词：%s' % ', '.join(hit),
            '作品名只留在人物块的 tag 里，summary 不写，否则会出真人假发感')

    if re.search(r'[\u3000-\u303f\uff00-\uffef]', nc_txt):
        add(5, WARN, '正文里出现中文标点', 'caption 用英文标点，中文只留在 text 字段里')

    # ---------- 关 6 机位 ----------
    has_pitch = re.search(
        r'(from below|from above|overhead|eye height|eye level|eye line|'
        r'looks? (slightly )?(up|down)|looking (slightly )?(up|down)|'
        r'height of|chest height|floor level|steep angle|tipped (down|up)|'
        r'above the height|below the level|low near|low to the)', txt) is not None
    has_dist = re.search(
        r'(close|closer|nearest|near the|distant|arm|step|metre|meter|far|'
        r'a few paces|right up against|at arm)', txt) is not None
    has_tilt = re.search(
        r'(lens level|level with|square to|tilted|rolled|rotated|degrees|'
        r'parallel to the sides|no tilt|zero tilt|camera level|'
        r'dead level|stays vertical|stays plumb|runs level|runs dead level|'
        r'does not lean|no lean|holds level|'
        r'nothing in the picture is level|nothing is level|no level line|'
        r'not one level edge|leans? in towards|leans? inward)', txt) is not None
    has_horizon = re.search(
        r'(horizon|bottom third|top third|lower third|upper third|'
        r'centre of the frame|center of the frame|middle of the frame|'
        r'eye line|eye level|takes the bottom|takes the top|'
        r'sits (just )?(above|below) the)', txt) is not None

    missing = [n for n, v in [('俯仰', has_pitch), ('距离', has_dist),
                              ('倾斜', has_tilt), ('视平线', has_horizon)] if not v]
    flat_intent = has(txt, ['flat plane', 'poster', 'no perspective', 'zero perspective',
                            'printed rectangle', 'no camera', 'no depth',
                            'flat graphic', 'collage', 'printed panel'])
    if len(missing) >= 2:
        if flat_intent:
            add(6, WARN, '机位四要素缺 %s，但这是平面/海报式构图，可视为有意省略' % '/'.join(missing),
                '若想更稳，补一句「the picture is a flat plane with no perspective and no camera」')
        else:
            add(6, FAIL, '机位四要素缺 %s' % '/'.join(missing),
                'B1：用可验证的画面事实写机位，四项至少各有一句')
    elif missing:
        add(6, WARN, '机位缺「%s」' % '/'.join(missing), '补一句，避免模型回落到默认平视')

    # ---------- 关 7 世界逻辑与故事（G 组） ----------
    # G5 「统一」与「唯一」并存 → 唯一色会被一起漂掉
    uniform = has(txt, ['every surface in the frame', 'everything in the frame',
                        'every white in the frame', 'the whole frame bleaches',
                        'all of it bleaches'])
    exclusive = has(txt, ['only cool', 'only saturated', 'the only colour',
                          'the only color', 'only colour in', 'only color in'])
    exception = has(txt, ['apart from', 'except for', 'other than', 'save for',
                          'with the one exception'])
    if uniform and exclusive and not exception:
        add(7, FAIL, '同时声明「全图统一成一支色」与「某物是唯一冷/饱和色」，后者会被一起漂掉',
            'G5：把例外显式排除——apart from X, every surface bleaches to ...')

    # G4 高调必须有黑锚点
    if has(txt, LIGHT_WORDS) and not has(
            txt, ['almost to black', 'near-black', 'near black', 'drops to black',
                  'the darkest part', 'deepest black', 'down to black',
                  'the darkest thing', 'the darkest notes', 'the darkest of the',
                  'three darks', 'two darks', 'darks in it']):
        add(7, WARN, '声明了高调但没有给「接近黑」的锚点，画面会整体飘',
            'G4：写「全图只有 N 处接近黑——具体是哪里」')

    # G6 硬光要写边缘（绘画性画面豁免：印象派/笔触/无硬轮廓本来就不要硬边）
    SOFT_INTENT = ['impressionist', 'brushstroke', 'brushstrokes', 'watercolour',
                   'watercolor', 'gouache', 'oil painting', 'no hard contour',
                   'no hard contours', 'no hard edge', 'no hard edges',
                   'all edges soft', 'soft focus', 'pastel']
    if has(txt, ['hard shadow', 'hard-edged', 'hard edge', 'hard light']) and not has(
            txt, ['blade', 'no gradient', 'no softness', 'razor', 'crisp edge']) \
            and not has(txt, SOFT_INTENT):
        add(7, WARN, '写了硬光但没写边缘硬度，实测会退化成阴天柔光',
            'G6：补 each shadow edge is cut like a blade, with no gradient at all')

    # G1 场景朝向
    scene = has(txt, ['bench', 'shelter', 'bus stop', 'platform', 'classroom',
                      'counter', 'kerb', 'curb', 'waiting room'])
    orient = has(txt, ['faces the road', 'facing the road', 'back against',
                       'facing out', 'turned to the road', 'open side toward',
                       'faces the street', 'faces the viewer', 'facing the viewer',
                       'faces the glass', 'faces the window', 'faces the table',
                       'faces the counter', 'faces the wall', 'faces away from',
                       'one place down the counter', 'same side of the counter',
                       'faces the camera', 'facing the camera',
                       'faces the aisle', 'facing the aisle', 'back to the wall',
                       'opposite the window', 'facing the opposite'])
    if scene and not orient:
        add(7, WARN, '有长凳/候车亭这类有方向性的场景，但没写朝向，容易背对车道',
            'G1：明写 the bench faces the road, her back is to the wall')

    # G2 故事道具
    props = ['footprint', 'ticket', 'bottle', 'notice', 'shoe', 'cup', 'letter',
             'suitcase', 'umbrella', 'cigarette', 'can ', 'newspaper', 'bucket',
             'hose', 'price card', 'boots', 'jar', 'apron', 'basket', 'crate',
             'tray', 'plate', 'basin', 'towell', 'sack', 'box', 'twine', 'shears',
             'lantern', 'lamp', 'branch', 'prints', 'print', 'boot print',
             'snowshoe', 'walking stick', 'rope', 'pail', 'mat', 'card', 'tag',
             'straw hat', 'sun hat', 'hat', 'ribbon', 'flower', 'stem', 'bunch']
    nprops = sum(1 for p in props if p in txt)
    if any(it.get('label') == 'character' for it in draft.get('items', [])) and nprops < 2:
        add(7, WARN, '画面里只有人，没有讲故事的证据物（脚印/票/空瓶/告示）',
            'G2：先写一句 story line，再给 3–6 件道具，每件都是那句话的证据')

    # G8 人物比例：只有人物没人比尺 → 一定会撑满画面
    if any(it.get('label') == 'character' for it in draft.get('items', [])):
        ratio = re.search(
            r'(her|she|he|his|him|they|figure|body|head|shoulders|boy|man|girl)[^.]{0,60}'
            r'(a quarter|a third|a fifth|a tenth|one fifth|'
            r'one quarter|one third|two thirds|two fifths|three fifths|'
            r'three quarters|a seventh|a sixth|a twelfth|a sixteenth|an eighth|a twentieth|'
            r'one twelfth|one sixteenth|one eighth|one twentieth|sixteen per cent|twelve per cent|'
            r'thirty per cent|forty per cent|half the height)[^.]{0,40}'
            r'(picture|frame|height|width)', txt, re.I)
        rel = has(txt, ['empty beside', 'wider than she is', 'twice her',
                        'taller than the bench', 'metres above her',
                        'meters above her', 'the whole width of the road',
                        'twice her seated height', 'above the top of her head',
                        'well clear above', 'empty air between',
                        'heads tall', 'her heads tall', 'to her chest',
                        'to her waist', 'to her shoulder'])
        dist = has(txt, ['metres away', 'meters away', 'metres from',
                         'meters from', 'opposite shoulder', 'from the far side',
                         'on the far shoulder', 'seven metres', 'ten metres',
                         'metre and a half', 'meters and a half',
                         'steps from us', 'steps away', 'steps from',
                         'paces from us', 'paces away'])
        if not (ratio or rel or dist):
            add(7, WARN, '人物没有任何比例尺，模型会把她放大到撑满画面',
                'G8：给分数 / 相对物 / 可量距离 至少两种，外加机位距离')

    # G3 表情：简单描写即可（2026-11-06 用户 m03593 改定，肌肉动向反而抢戏）
    # 只有完全没写表情（连 simple 描写都没有）才 WARN
    chars = [it for it in draft.get('items', []) if it.get('label') == 'character']
    if chars:
        ctxt = ' '.join(it.get('caption', '') for it in chars)
        simple = re.search(r'\b(expression|face|smiling|frowning|looking (down|up|at)|'
                           r'concentration|distracted|tired|sad|happy|calm|relaxed|'
                           r'mouth is (slightly )?open|mouth is closed)\b', ctxt, re.I)
        muscle = re.search(r'\b(brows?|eyebrows?|lids?|mouth corners?|jaw|cheeks?|lips?|'
                           r'forehead|chin|eyelid|eyes? (narrow|half|wide)|'
                           r'pupils?)\b', ctxt, re.I)
        if not (simple or muscle):
            add(7, WARN, '人物完全没写表情，会出默认脸',
                'G3：一句简单表情描写即可（looking down at her hands, mouth slightly open, not smiling）')

    # ── 关 8 曝光：亮部有没有被写死 ──────────────────────────────
    # 18 张实测：亮部饱和度 0.014–0.119、暗部 0.092–0.652，17/18 亮部比暗部淡
    # 3–50 倍。真凶是把「硬光」写成「烧成纯白」，亮面因此失去全部颜色。
    BLEACH = ['overexposed', 'blown out', 'blown to', 'pure white',
              'white out', 'burns out to white', 'within a hair of white',
              'flat sheet of white', 'bleached']
    KEEP_COLOUR = ['keeps its colour', 'keeps its color', 'still holds its colour',
                   'still holds its color', 'one step lighter',
                   'lighter but not paler', 'the colour survives',
                   'the color survives', 'holds its hue',
                   'saturated in the light', 'the lit side keeps',
                   'keeps every bit of its colour', 'keeps every bit of its color']
    def _bleach_hits(t, words):
        out = []
        for w in words:
            for m in re.finditer(r'(?<![a-z])' + re.escape(w) + r'(?![a-z])', t, re.I):
                pre = t[max(0, m.start() - 70):m.start()]
                if re.search(r'\b(not|no|never|without|nothing|none|nor|'
                             r'rather than|instead of|far from)\b', pre, re.I):
                    continue
                out.append(w)
                break
        return out

    hit = _bleach_hits(txt, BLEACH)
    blown_ok = bool(intents & {'blown', 'leak'})
    if hit and blown_ok:
        add(8, WARN, '有意过曝（%s）：已被 --intent 放行' % ' / '.join(hit),
            '仍要写清「哪里烧掉」和「哪里还留着颜色」，否则整张只剩暗部有色')
    if hit and not flat_intent and not blown_ok:
        if not has(txt, KEEP_COLOUR):
            add(8, FAIL,
                '亮部写成"烧成纯白"（%s）：实测会让亮面饱和度掉到 0.02–0.12，'
                '整张图只剩暗部有颜色，看上去像过曝的手机照' % ' / '.join(hit),
                '关 8：删掉 overexposed / pure white，改写成关系句——'
                '"the lit side is one step lighter than the shade and keeps every bit of its colour"')
        else:
            add(8, WARN,
                '仍有漂白措辞（%s），但有保色句兜底' % ' / '.join(hit),
                '关 8：整句删掉更稳，硬光靠边缘硬度写，不靠亮度写')

    # 明度指令必须在最前 80 词内出现一次（模型只看前段）
    head = txt[:520]
    if not re.search(r'\b(dark|dim|bright|lit|shadow|light|expos|contrast|'
                     r'high key|low key|mid tone)\b', head, re.I):
        add(8, WARN, '前 80 词里没有一句明度/光线的定调句，模型会退回平均亮度',
            '关 8：把"整张图的明度落在哪一档"提到 summary 开头第一句')

    gate9(txt, draft.get('summary', {}).get('caption', '') or draft.get('caption', ''), add)
    if not cap_only:
        gate10(draft, add)

    return res


# ---------- 关 9 色彩落点 ----------
CHROMA = ['ochre', 'amber', 'yellow', 'green', 'red', 'blue', 'pink', 'orange', 'brown',
          'gold', 'honey', 'butter', 'teal', 'olive', 'violet', 'purple', 'cyan',
          'magenta', 'rust', 'terracotta', 'mustard', 'lime', 'wine', 'copper',
          'turquoise', 'crimson', 'scarlet', 'indigo', 'maroon', 'beige', 'tan']
NEUTRAL = ['grey', 'gray', 'white', 'cream', 'silver', 'pale', 'off-white', 'ivory',
           'charcoal', 'ash']
MONO_OK = ['monochrome', 'one colour only', 'one color only', 'single colour',
           'single color', 'no colour at all', 'no color at all', 'black and white']


def gate9(txt, summary, add):
    low = summary.lower()
    if any(k in low for k in MONO_OK):
        return
    n_ch = sum(low.count(w) for w in CHROMA)
    n_ne = sum(low.count(w) for w in NEUTRAL)
    if n_ch < 3:
        add(9, WARN, 'summary 里的色相词只有 %d 个，色彩预算不足，模型会画出接近中性的图' % n_ch,
            '至少点名三个有色相的东西，并且写在被照亮的大面积上（台面、墙、地面），不要只写在小道具上')
    if n_ne > n_ch:
        add(9, WARN, '中性色词（%d）多于色相词（%d），大面积会被中性色占满' % (n_ne, n_ch),
            '把 grey / cream / white / pale 留给小物件，把 ochre / amber / green 这类色相词给最大块的面')
    # 最亮处必须有颜色
    m = None
    for kw in ('brightest thing', 'bright end', 'brightest note', 'the brightest'):
        i = low.find(kw)
        if i >= 0:
            m = i
            break
    if m is not None:
        win = low[max(0, m - 220):m + 260]
        OK_BRIGHT = ('glass', 'window', 'sky', 'sun', 'daylight', 'lamp', 'tube', 'bulb',
                 'paper', 'the white ground', 'bare white', 'mist', 'silk')
        if not any(w in win for w in CHROMA) and not any(w in win for w in OK_BRIGHT):
            add(9, WARN, '写了「最亮的东西」，但那句话附近没有任何色相词',
                '最亮处要写成有颜色的东西（ochre laminate / yellow-green paint），否则模型把它画成白')


def main():
    if len(sys.argv) < 2:
        print(__doc__)
        sys.exit(1)
    path = sys.argv[1]
    ref_p = None
    args = sys.argv[2:]
    intents = []
    for i, a in enumerate(args):
        if a == '--ref' and i + 1 < len(args):
            ref_p = args[i + 1]
        if a == '--intent' and i + 1 < len(args):
            intents = [x.strip().lower() for x in args[i + 1].split(',') if x.strip()]

    draft = load_draft(path)
    ref = ref_profile(ref_p) if ref_p else None
    res = lint(draft, ref, intents)

    print('检查 %s' % os.path.basename(path))
    if ref:
        print('参考图 %s  明度 暗%.1f%%/中%.1f%%/亮%.1f%%  饱和 亮%.3f/暗%.3f  soft %.2f  最亮格 %d行%d列'
              % (os.path.basename(ref_p), ref['dark'] * 100, ref['mid'] * 100,
                 ref['bright'] * 100, ref['lit'], ref['shadow'], ref['soft'],
                 ref['brightest'][0] + 1, ref['brightest'][1] + 1))
    print()

    gate_name = {1: '结构', 2: '数值', 3: '矛盾', 4: '覆盖', 5: '禁用', 6: '机位', 7: '世界逻辑', 8: '曝光', 9: '色彩落点', 10: '构图落位'}
    nfail = 0
    for g in range(1, 11):
        rows = [r for r in res if r[0] == g]
        if not rows:
            print('关 %d %s：通过' % (g, gate_name[g]))
            continue
        print('关 %d %s：' % (g, gate_name[g]))
        for _, lvl, msg, fix in rows:
            if lvl == FAIL:
                nfail += 1
            print('  [%s] %s' % (lvl, msg))
            if fix:
                print('         → %s' % fix)
    print()
    print('结论：%s（%d 项 FAIL）' % ('不通过' if nfail else '通过', nfail))
    sys.exit(1 if nfail else 0)


if __name__ == '__main__':
    main()
