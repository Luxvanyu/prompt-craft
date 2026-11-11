#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""MOSS-Image Universal Multi-Engine Prompt Transpiler v2.

Upgraded to natively support:
1. MOSS-Image (Official JSON prose & centralized yxyx Layout)
2. NovelAI v5 (Official 3-Tier Split: Base Prompt, Character 1, UC, 1.2::tag:: weighting, high complexity, and Single Global Integration for complex composition)
3. Anima3 (Strict 9-Slot sequential pipeline without 'camera' keyword, ending natural language interaction clause, single-line text output)
4. Krea 2 (Visual-LLM 600-800 word cinematic prose + 8-slot breakdown + 28-char Chinese 7-word poem + HTML output)
"""

import argparse
import json
import re
import sys
from pathlib import Path

TAG_MAP = [
    # Character & Gender
    (r'\b1girl\b|\ba girl\b|\ba young woman\b', '1girl, solo'),
    (r'\bpink hair\b', 'pink hair'),
    (r'\bmedium hair\b|\bmedium length\b', 'medium hair'),
    (r'\bhair intakes\b|\brounded hair intakes\b', 'hair intakes'),
    (r'\bhair ornament\b|\bhair clip\b|\bgold clip\b', 'hair ornament, hair clip'),
    (r'\bhairband\b|\bheadband\b', 'hairband'),
    (r'\bpink eyes\b', 'pink eyes'),
    (r'\blarge breasts\b|\bbosom\b', 'large breasts'),
    (r'\bfeathered wings\b|\bwhite feathered wings\b|\bwings\b', 'wings, feathered wings'),
    # Clothing
    (r'\bwhite dress\b', 'white dress'),
    (r'\bdetached sleeves\b', 'detached sleeves'),
    (r'\blong sleeves\b', 'long sleeves'),
    (r'\bwhite sleeves\b', 'white sleeves'),
    (r'\bthighhighs\b|\bwhite thighhighs\b', 'thighhighs, white thighhighs'),
    (r'\bsailor uniform\b|\bserafuku\b|\bsailor collar\b', 'sailor uniform, serafuku, sailor collar'),
    (r'\bpleated skirt\b', 'pleated skirt'),
    (r'\bribbon tie\b|\bcrimson ribbon\b|\bnecktie\b', 'ribbon, red ribbon, bow tie'),
    (r'\bsweater\b|\bcable-knit\b', 'sweater, knit sweater'),
    (r'\bhoodie\b|\bhooded sweatshirt\b', 'hoodie'),
    (r'\bjeans\b|\bdenim\b', 'jeans, denim'),
    (r'\bleather jacket\b', 'leather jacket'),
    (r'\btrench coat\b', 'trench coat'),
    (r'\bapron\b', 'apron'),
        (r'\bboots\b', 'boots'),
    (r'\bloafers\b', 'loafers'),
    (r'\bshoes\b', 'shoes'),
    # Actions & Poses
    (r'\b(she sits|girl sits|is sitting|sitting on|seated on|seated at)\b', 'sitting'),
    (r'\bstands\b|\bstanding\b', 'standing'),
    (r'\bwalks\b|\bwalking\b|\bstride\b', 'walking'),
    (r'\bcrouch\b|\bcrouches\b|\bcrouching\b', 'crouching'),
    (r'\brecline\b|\breclines\b|\blying\b', 'lying, reclining'),
    (r'\bholding\b|\bholds\b', 'holding'),
    (r'\bdrinking\b|\bsipping\b', 'drinking, sipping, straw'),
    (r'\blooking at viewer\b|\btoward the viewer\b|\btoward us\b|\btoward camera\b', 'looking at viewer'),
    (r'\blooking away\b|\blooking out\b', 'looking away'),
    (r'\bsmile\b|\bsmiling\b', 'smile'),
    (r'\bblush\b|\bflushed\b', 'blush'),
    # Environment
    (r'\bclassroom\b', 'classroom, school desk, indoors'),
    (r'\bcafe\b|\bcoffee shop\b', 'cafe, coffee cup, indoors'),
    (r'\bstation\b|\btrain platform\b', 'train station, platform, railway'),
    (r'\borchard\b|\bapple tree\b', 'orchard, apple, tree, outdoors'),
    (r'\blake\b|\bpond\b|\bwater lilies\b', 'lake, water lily, nature, outdoors'),
    (r'\bcathedral\b|\bgothic\b|\bruins\b', 'ruins, gothic, cathedral, architecture'),
    (r'\blibrary\b|\bbookshelves\b', 'library, bookshelf, book'),
    (r'\bterrace\b|\bbalcony\b', 'terrace, balcony, outdoors'),
    (r'\bstreet\b|\balley\b|\bcity\b', 'city, street, urban, outdoors'),
    (r'\bnight\b|\bmidnight\b', 'night'),
    (r'\brain\b|\brainy\b|\bdrizzle\b', 'rain, wet'),
    (r'\bsunlight\b|\bsunny\b|\bdaylight\b', 'sunlight, day'),
    (r'\bdusk\b|\bsunset\b', 'sunset, twilight'),
    (r'\bmotorcycle\b|\bbike\b', 'motorcycle'),
    (r'\brabbit\b|\bbunny\b', 'rabbit'),
    (r'\bsword\b|\brapier\b', 'sword, weapon'),
    (r'\bclarinet\b', 'clarinet, musical instrument'),
    (r'\bboba\b|\bmilk tea\b', 'bubble tea'),
    # Combat & Action Tags (Phase 2 Action Library)
    (r'\bthrust\b|\bthrusting\b|\bpierce\b|\bpiercing\b', 'thrusting, 1.2::slender rapier::, thrust'),
    (r'\bslash\b|\bslashing\b|\bswing\b|\bswinging\b', 'slashing, sword swing, 1.2::curved blade::'),
    (r'\brapier\b|\bslender sword\b', 'rapier, slender blade, holding sword'),
    (r'\bcurved blade\b|\bkatana\b|\bsaber\b', 'curved blade, single sword, sword swing'),
    (r'\bdive\b|\bdiving\b|\baerial dive\b', 'dive, 1.2::aerial falcon dive::, aerial, flying'),
    (r'\baerial\b|\bairborne\b|\bmidair\b|\bmid-air\b', 'aerial, airborne, in midair'),
    (r'\bshockwave\b|\bair ripples\b|\bdistortion\b', 'shockwave, conical air distortion, wind'),
    (r'\bspeed lines\b|\bmotion lines\b|\bmotion blur\b', 'speed lines, motion lines, motion blur'),
    (r'\bcrescent\b|\blight arc\b|\blight trail\b|\bsword trail\b', 'sword trail, crescent light arc'),
    (r'\bcounterbalance\b|\bguard\b|\bdefensive\b', 'defensive stance, combat stance'),
    (r'\bspin\b|\bspinning\b|\bpivot\b', 'spin, spinning, ground skim spin slash'),
    (r'\bfolded wings\b|\bswept tightly back\b', 'folded wings, 1.2::folded wings swept back::'),
    (r'\basymmetric wings\b|\bbraking\b|\bair-brake\b', 'asymmetrical wings, braking wing, wide wings'),

]


def extract_text(draft):
    if isinstance(draft, dict):
        if "caption" in draft and not draft.get("items"):
            return draft["caption"]
        parts = [draft.get("summary", {}).get("caption", "")]
        for item in draft.get("items", []):
            parts.append(item.get("caption", ""))
        return "\n".join(p for p in parts if p)
    return str(draft)


def to_moss(draft):
    txt = extract_text(draft)
    return json.dumps({"caption": txt}, ensure_ascii=False)


def to_nai_v5(draft, mode="single_global"):
    """NovelAI V5 Official Standard format:
    Base Prompt (Camera, action, scene, lighting, spatial sentences, complexity, quality)
    Character 1 (Physical traits, hair, eyes, clothes) [if not single_global]
    UC (Negative prompt)
    """
    txt = extract_text(draft)
    low = txt.lower()
    
    # 1. Base tags
    base_tags = ["1girl", "solo"]
    action_scene_tags = []
    char_tags = []
    
    # Check character traits
    # 不写角色名：G25/G22 — 带名字会触发整套角色先验并被放大 1.8-3.6 倍
    # 注意：下面这些「特征」直接进 char_tags；TAG_MAP 里含 hair/eyes/dress 等词条的
    # 命中会在 154 行被主动跳过（避免与这里重复），所以特征必须在这里单独兜住。
    if "medium hair" in low:
        char_tags.append("medium hair")
    if "long hair" in low:
        char_tags.append("long hair")
    if "short hair" in low:
        char_tags.append("short hair")
    if "pink hair" in low:
        char_tags.append("pink hair")
    if "blonde hair" in low or "blond hair" in low:
        char_tags.append("blonde hair")
    if "black hair" in low:
        char_tags.append("black hair")
    if "white hair" in low or "silver hair" in low:
        char_tags.append("white hair")
    if "blue hair" in low:
        char_tags.append("blue hair")
    if "red hair" in low:
        char_tags.append("red hair")
    if "twintails" in low or "twin tails" in low:
        char_tags.append("twintails")
    if "ponytail" in low:
        char_tags.append("ponytail")
    if "hair intakes" in low:
        char_tags.append("hair intakes")
    if "ahoge" in low:
        char_tags.append("ahoge")
    if "hairband" in low:
        char_tags.append("hairband")
    if "hair ornament" in low or "hair clip" in low:
        char_tags.append("hair ornament")
    if "pink eyes" in low:
        char_tags.append("pink eyes")
    if "blue eyes" in low:
        char_tags.append("blue eyes")
    if "red eyes" in low:
        char_tags.append("red eyes")
    if "green eyes" in low:
        char_tags.append("green eyes")
    if "black eyes" in low or "dark black irises" in low:
        char_tags.append("black eyes")
    if "glasses" in low:
        char_tags.append("glasses")
    if "large breasts" in low:
        char_tags.append("large breasts")
    if "wings" in low or "feathered wings" in low:
        for _w in ("wings", "feathered wings"):
            if _w not in char_tags:
                char_tags.append(_w)
    if "white dress" in low:
        char_tags.append("white dress")
    if "detached sleeves" in low:
        char_tags.append("detached sleeves")
    if "thighhighs" in low:
        for _t in ("thighhighs", "white thighhighs"):
            if _t not in char_tags:
                char_tags.append(_t)

    for pattern, matched_tag in TAG_MAP:
        if re.search(pattern, low):
            for t in matched_tag.split(','):
                t_clean = t.strip()
                if t_clean and t_clean not in base_tags and t_clean not in char_tags and t_clean not in action_scene_tags:
                    if any(c in t_clean for c in ["hair", "eyes", "breasts", "dress", "sleeves", "thighhighs"]):
                        continue
                    action_scene_tags.append(t_clean)
                    
    # Clean natural sentence for NAI V5 spatial guidance
    spatial_sentences = []
    for s in re.split(r'(?<!\d)\.(?!\d)', txt):
        s_clean = s.strip()
        if not s_clean or "The whole picture sits" in s_clean or "One coarse visible grain" in s_clean:
            continue
        if any(w in s_clean.lower() for w in ["stands", "sits", "walks", "crouch", "recline", "behind", "left", "right", "light", "shadow", "bench", "table", "window", "street"]):
            spatial_sentences.append(s_clean)
            
    spatial_prose = ". ".join(spatial_sentences[:3]) + "." if spatial_sentences else ""
    
    # Complexity and quality
    # 零质量词纪律：质量由明度/光/材质句承担，不靠形容词串堆权重
    v5_quality = ""
    
    # UC (Negative)
    uc_str = (
        "lowres, {bad}, error, fewer digits, extra digit, missing fingers, "
        "worst quality, low quality, normal quality, jpeg artifacts, "
        "signature, watermark, username, blurry, artist name, "
        "-2::halo::, -2::head halo::, -2::floating halo::"
    )
    
    if mode == "single_global":
        # NAI V5 Complex Composition: Single Global Integration (Base Prompt only)
        all_tags = base_tags + char_tags + action_scene_tags
        prompt_block = (
            f"{', '.join(all_tags)},\n"
            f"{spatial_prose}\n"
            f"{v5_quality}"
        )
        return (
            f"Prompt:\n{prompt_block}\n\n"
            f"Character 1:\n\n"
            f"UC:\n{uc_str}"
        )
    else:
        # Standard Multi-Slot NAI V5
        base_block = (
            f"{', '.join(base_tags + action_scene_tags)},\n"
            f"{spatial_prose}\n"
            f"{v5_quality}"
        )
        char_block = f"{', '.join(char_tags)}"
        return (
            f"Prompt:\n{base_block}\n\n"
            f"Character 1:\n{char_block}\n\n"
            f"UC:\n{uc_str}"
        )


def to_anima(draft, artist=""):
    """Anima3 Prompt Engineer Standard:
    人数 → 角色 → 作品 → 画师串 → 特征/场景/镜头顺排 + 结尾自然语言描述 (严格禁止出现 'camera')
    Exactly one single-line text string!
    """
    txt = extract_text(draft)
    low = txt.lower()
    
    tags = ["1girl", "solo"]
    if artist:
        tags.append(artist)
        
    for pattern, matched_tag in TAG_MAP:
        if re.search(pattern, low):
            for t in matched_tag.split(','):
                # 剥离 TAG_MAP 中专供 NAI 的 1.2::tag:: 权重壳，保持 Anima 裸 tag 纯净
                t_clean = re.sub(r'^[\d\.]+::(.*?)::$', r'\1', t.strip())
                if t_clean and t_clean not in tags:
                    tags.append(t_clean)
                    
    # 零质量词：masterpiece / very aesthetic 一律不加
    
    # Clean natural language sentence (strictly strip 'camera', technical stops, and MOSS exposure headers)
    clean_desc = re.sub(r'\bcamera\b', 'view', txt, flags=re.I)
    clean_desc = re.sub(r'[\d\.]+::(.*?)::', r'\1', clean_desc)
    clean_desc = re.sub(r'The (whole )?picture sits in the[^\.]*\.', '', clean_desc, flags=re.I)
    clean_desc = re.sub(r'The view is positioned[^\.]*\.', '', clean_desc, flags=re.I)
    clean_desc = re.sub(r'One coarse visible grain[^\.]*\.', '', clean_desc, flags=re.I)
    clean_desc = re.sub(r'stopping one step short of blowing out', '', clean_desc, flags=re.I)
    
    # 用 (?<!\d)\.(?!\d) 切句，防止小数点（如 0.3s / 1.5m）被误切
    sentences = [s.strip() for s in re.split(r'(?<!\d)\.(?!\d)', clean_desc) if s.strip()]
    short_narrative = ". ".join(sentences[:2]) + "."
    
    return f"{', '.join(tags)}, {short_narrative}"


def to_krea2(draft, title_cn="", include_poem=False):
    """Krea 2 Prompt Artisan Standard:
    Continuous natural language prose (500-800 words) + 8-slot breakdown rationale.
    Poem is optional (defaults to False per user instruction).
    """
    txt = extract_text(draft)
    
    clean = re.sub(r'One coarse visible grain layer[^\.]*\.', '', txt, flags=re.I)
    clean = re.sub(r'The (whole )?picture sits in the[^\.]*\.', '', clean, flags=re.I)
    clean = re.sub(r'stopping one step short of blowing out', '', clean, flags=re.I)
    clean = re.sub(r'The camera is positioned[^\.]*\.', '', clean, flags=re.I)
    # Anima 的 1.2::phrase:: 权重壳在 Krea 2 里没有意义，剥成普通词组
    clean = re.sub(r'[\d\.]+::(.*?)::', r'\1', clean)
    
    sentences = [s.strip() for s in re.split(r'(?<!\d)\.(?!\d)', clean) if s.strip()]
    narrative_prose = ". ".join(sentences) + "."
    
    krea_english = (
        f"{narrative_prose}"
    )
    
    if not title_cn:
        # 从草稿现有键里取标题，取不到就用文案首句前半，绝不硬编码具体题目
        title_cn = (draft.get("title") or draft.get("title_cn") or "").strip()
        if not title_cn:
            first = sentences[0] if sentences else "untitled"
            title_cn = (first[:18] + "…") if len(first) > 18 else first
    res = {
        "title_cn": "Krea 2 prompt - " + title_cn,
        "prompt_en": krea_english,
    }
    if include_poem:
        res["poem"] = ""
        res["signature"] = ""
    return res


def translate_all(draft, include_poem=False):
    return {
        "moss": to_moss(draft),
        "nai_v5": to_nai_v5(draft),
        "anima": to_anima(draft),
        "krea2": to_krea2(draft, include_poem=include_poem)
    }


def _safe_stdout():
    try:
        sys.stdout.reconfigure(encoding='utf-8', errors='replace')
    except Exception:
        pass


def main():
    _safe_stdout()
    parser = argparse.ArgumentParser(description="Multi-engine prompt transpiler v2")
    parser.add_argument("input", help="Path to input draft JSON or text file")
    parser.add_argument("--target", choices=["moss", "nai", "anima", "krea2", "all"], default="all",
                        help="Target engine format (default: all)")
    parser.add_argument("--poem", action="store_true", help="Include 28-character Chinese poem in Krea 2 output (default: False)")
    args = parser.parse_args()

    p = Path(args.input)
    if not p.exists():
        print(f"Error: {args.input} not found", file=sys.stderr)
        sys.exit(1)

    try:
        with open(p, "r", encoding="utf-8") as f:
            data = json.load(f)
    except Exception:
        with open(p, "r", encoding="utf-8") as f:
            data = {"caption": f.read()}

    if args.target == "moss":
        print(to_moss(data))
    elif args.target == "nai":
        print(to_nai_v5(data))
    elif args.target == "anima":
        print(to_anima(data))
    elif args.target == "krea2":
        res = to_krea2(data, include_poem=args.poem)
        print(f"=== {res['title_cn']} ===\n")
        print(res["prompt_en"])
        if "poem" in res:
            print(f"\n{res['poem']}\n{res['signature']}")
    else:
        all_res = translate_all(data, include_poem=args.poem)
        print("="*60)
        print("1. [MOSS-Image] (Official Single-Key JSON)")
        print("="*60)
        print(all_res["moss"])
        print("\n" + "="*60)
        print("2. [NovelAI v5] (Official 3-Tier Split & Base Prompt Integration)")
        print("="*60)
        print(all_res["nai_v5"])
        print("\n" + "="*60)
        print("3. [Anima3] (Strict 1-Line Slot Sequence without Camera)")
        print("="*60)
        print(all_res["anima"])
        print("\n" + "="*60)
        print("4. [Krea 2] (Visual-LLM 600-800 Word Cinematic Prose)")
        print("="*60)
        k = all_res["krea2"]
        print(f"{k['title_cn']}\n\n{k['prompt_en']}")
        if "poem" in k:
            print(f"\n{k['poem']}\n{k['signature']}")


if __name__ == "__main__":
    main()
