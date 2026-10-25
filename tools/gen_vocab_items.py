"""Generate vocabulary recognition items with plausible distractors."""
import csv
import hashlib
import json
import random
import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from engine import paths

KANJI = re.compile(r"[一-龯々〆ヵヶ]")
KANA = re.compile(r"[ぁ-ゖァ-ヺー]")
LONG = (("ゅう", "ゅ"), ("ょう", "ょ"), ("おう", "お"), ("えい", "え"), ("ゆう", "ゆ"))
VOICE = dict(zip("かきくけこさしすせそたちつてとはひふへほ", "がぎぐげござじずぜぞだぢづでどばびぶべぼ"))
UNVOICE = {v: k for k, v in VOICE.items()}
SMALL_TSU_BEFORE = set("かきくけこさしすせそたちつてとはひふへほカキクケコサシスセソタチツテトハヒフヘホ")
SAFE_LOOKALIKE_KANJI = set("一二三四五六七八九十百千万円日月火水木金土年上下左右中大小山川田人口目耳手足力気雨天空花草竹木林森本休体休学校先生学生友男女子父母兄姉弟妹私今時分半毎週先生話語読書聞見行来帰出入食飲買売安新古高多少白黒赤青早長明夜朝昼夕午前後内外東西南北国町村店会社員仕事物車電道駅社名字方会家室道理同別元多少数万点体不心思知教習使作持待借貸会回台太犬猫鳥魚肉米茶酒牛馬足立住所通着始終歩走待特間問聞買貸質末未土士午牛右石見貝人入日目鳥島京東洗先漢館員開閉会合理里白百田由申甲王玉主住門口回白目自貝負貨力刀方万千干于夕外名各友反有左斤月用由甲申早草田里大太犬天夫王玉")
SAFE_LOOKALIKE_KANJI.update("生牛午年王主正玉先失物勿易下上不止味未末朱昧出山事吏以似代所斤斥近長張帳帯道首通習羽痛用恋赤引弓行街急忘思息付府附汽業葉藥空穴突最取量予矛坊防房放集隹住文交父法去泊地池他理埋注電申動重働遠運音暗意冷光元送色角免命令故古分切社仕柔矢彼皮破画由經軽径験駅済齊研硯究決快君群着著看講構工港江争無舞治冶慣貫眠眼")

# Confusable N5/N4 characters, including frequent near-shapes in common fonts.
LOOKALIKE_PAIRS = """
体 休 待 持 待 特 持 特 間 問 間 聞 問 聞 買 貸 買 質 貸 質
末 未 土 士 午 牛 右 石 見 貝 人 入 日 目 白 百 鳥 島 京 東
洗 先 漢 館 員 貝 開 閉 会 合 理 里 木 本 木 米 木 休 休 体
大 太 大 犬 天 夫 王 玉 主 住 待 持 早 草 口 日 田 由 申 甲
力 刀 力 九 力 万 千 干 午 千 于 土 工 士 干 于 夕 外 夕 多
名 各 休 体 友 反 友 有 左 右 石 右 斤 白 自 白 百 目 日
口 回 口 日 目 自 目 貝 月 用 月 肉 田 由 田 甲 田 申 田 里
人 入 人 八 入 力 方 万 方 放 方 旅 牛 午 牛 生 牛 年 干 千
末 未 末 本 未 朱 朱 株 林 森 林 村 村 材 村 寸 材 才 在
門 間 門 問 門 聞 門 開 門 閉 門 関 門 閣 国 因 国 困 国 園
語 話 言 信 言 記 言 計 言 訓 言 試 言 読 言 説 言 語 言 話
買 貝 員 見 貝 負 貝 貨 貝 貸 貝 質 貝 賞 貝 貯 貝 財
者 都 者 暑 者 諸 昼 夜 昼 書 者 着 目 着 看 目 相 木 相 想
時 持 時 待 時 特 寺 持 寺 待 寺 詩 住 柱 主 王 往 主 注
泳 永 永 求 水 氷 水 永 氵 氺 広 店 庄 広 庁 天 店 占
車 東 里 重 里 理 里 埋 田 由 田 申 由 甲 申 甲 里

日 目 白 百 白 自 白 百 百 貝 自 目 貝 貝 負 負 貨 負 員 見 貝 見 頁
口 囗 口 日 口 中 口 古 口 石 口 田 田 由 田 申 田 甲 田 里 田 男
大 天 大 夫 天 矢 太 犬 太 夫 犬 状 犬 状 王 玉 王 主 玉 宝 王 皇
生 牛 生 年 牛 午 牛 半 牛 件 手 毛 手 才 手 千 才 材 才 在 木 本
木 末 木 未 木 朱 木 休 木 体 林 木 森 木 村 木 材 本 体 本 休
山 出 山 仙 山 岩 川 州 川 巛 水 氷 水 永 水 求 火 災 火 灯 火 秋
土 士 土 工 士 干 干 于 千 干 千 午 午 牛 午 半 十 千 十 升 十 千
人 入 人 八 入 力 人 大 人 天 人 介 入 力 力 九 力 万 力 方 力 刀
右 石 右 友 左 右 左 佐 左 右 斤 斥 斤 折 斤 近 月 用 月 肉 月 明
日 目 日 白 目 貝 見 貝 見 覚 見 規 見 観 貝 財 貝 貞 貝 質
東 車 東 束 東 重 西 酉 西 要 南 商 北 比 北 背 上 止 上 正 下 卞
中 仲 中 沖 千 干 千 于 午 干 今 金 令 冷 令 命 金 全 金 会 金 針
口 回 回 困 囗 国 門 問 門 間 門 聞 門 開 門 閉 門 関 間 聞 問 間
言 話 言 信 言 記 言 計 言 語 言 読 言 説 言 試 言 訓 言 許 言 認
糸 系 糸 級 糸 給 糸 終 糸 絵 糸 紙 糸 線 糸 組 糸 細 糸 緑 糸 結
車 軍 車 庫 車 転 車 輪 車 軽 車 東 車 連 車 運 車 軌 車 転 車 軽
魚 鳥 鳥 島 魚 漁 魚 鮮 魚 鯨 馬 駅 馬 鳴 馬 駆 馬 駐 馬 験 馬 騎
雨 雲 雨 電 雨 雪 雨 雷 雨 零 雨 霜 雨 霧 雨 曇 竹 笑 竹 第 竹 箱
草 花 草 茶 花 化 花 貨 花 苗 花 芽 艸 草 艹 花 良 食 良 浪 良 娘
石 右 石 研 石 砂 石 破 石 確 石 岩 貝 見 貝 負 貝 貨 貝 貸 貝 買
虫 風 虫 蚊 虫 蝶 虫 蛇 虫 蛍 心 忘 心 思 心 急 心 息 心 悪 心 必
足 走 足 路 足 踏 足 踊 足 跳 足 跡 足 輪 辶 道 辶 通 辶 近 辶 返
犬 太 犬 状 犬 猫 犬 献 犬 獣 王 主 王 往 王 皇 王 玉 王 現 王 球
女 好 女 姉 女 妹 女 始 女 安 女 妻 子 字 子 学 子 存 子 季 子 孫
父 交 父 斧 母 毎 母 海 母 毎 母 毎 母 梅 母 毎 母 敏 母 毎 母 毎
力 男 力 協 力 努 力 勉 力 勝 力 助 力 動 力 労 力 効果 刀 刃 刀 切
建 健 建 延 建 廷 建 鍵 健 康 倉 創 倉 庫 米 来 米 料 米 粉 米 迷
店 点 店 占 店 広 店 庄 庄 広 庄 天 天 夫 天 太 天 矢 天 失 天 鉄
休 體 体 待 侍 持 時 持 特 待 後 待 詩 持 寺 特 等 特 時 寺 詩 寺
学 覚 学 挙 学 字 学 校 校 木 校 交 校 効 教 孝 教 救 教 数 教 文
会社 会 合 会 今 会 絵 社 礼 社 神 社 土 社 者 都 都 暑 者 諸 都 緒
道 首 道 遠 道 運 道 通 通 痛 通 勇 通 踊 通 用 用 田 用 甩 用 由
明 朋 明 盟 明 鳴 明 名 朝 潮 朝 期 朝 月 昼 書 書 者 書 聿 昼 夜
早 草 早 卓 早 旬 早 章 田 由 田 申 田 甲 里 理 里 埋 里 黒 里 量
町 略 町 男 町 田 村 材 村 寸 材 才 村 木 市 巾 市 布 市 巾 師 師 帥
駅 験 駅 駅 駅 駅 館 管 館 官 館 店 員 貝 員 損 員 賞 員 負 員 貨
新 親 新 薪 親 立 親 童 新 斤 新 斬 新 断 新 斯 方 旅 方 族 方 放
買 置 買 具 買 貝 売 士 売 買 売 売 質 斤 質 貝 質 斦 貸 責 貸 借
借 惜 借 昔 借 錯 近 斤 近 折 近 祈 近 斥 近 斬 近 断 走 起 走 越
駅 馬 駅 尺 駅 駅 館 食 館 官 漢 難 漢 嘆 漢 韓 漢 漢 洗 先 洗 洒
病 痛 病 丙 病 柄 病 疲 病 疫 医 区 医 匠 医 医 医 矢 医 医 病 医
終 糸 終 冬 終 冬 終 系 終 紙 終 級 終 級 終 糸 終 糸 終 糸 終 糸
"""

# Dense groups make the hard-coded confusable inventory useful in practice:
# each common N5/N4 kanji has several alternatives while every replacement
# still occupies exactly one kanji slot.
LOOKALIKE_GROUPS = """
人 入 八 大 天 太 犬 夫
日 目 白 百 自 貝 見
木 本 末 未 朱 休 体
土 士 干 于 千 午 牛
右 石 左 友 斤 斥
口 回 中 田 由 申 甲
月 用 肉 明 朋
山 出 川 州
東 束 車 里 重
門 間 問 聞 開 閉
言 話 信 記 計 語 読
買 貝 負 貨 貸 質 員
王 玉 主 住 往 注
力 刀 九 万 方 努
早 草 卓 章 旬
会 合 今 絵 全 金
店 点 占 広 庄
社 礼 神 土 者
新 親 斤 斬 断
鳥 島 馬 駅 鳴
魚 鮮 漁 鳥
雨 雲 電 雪 雷
草 花 茶 苗 芽
足 走 路 起 越
子 字 学 存 季
女 好 姉 妹 始 安
食 良 飲 飯 館
米 来 料 粉 迷
病 痛 疲 疫
校 木 交 効 教
昼 書 者 夜 朝
町 男 村 材
力 男 協 助 勝
車 軍 庫 転 輪 軽
石 研 砂 破 確 岩
心 必 思 忘 急 悪
手 才 毛 千
父 交 斧 母 毎 海
名 各 多 夕
本 体 休 待 持 特
生 牛 午 年 王 主 正 玉 先 失
物 勿 易 場 楊 場
下 上 不 止 土 士
味 未 末 朱 昧
出 山 仙 击
以 似 代 仏
所 斤 斥 近
長 張 帳 帯
道 首 通 導 遠 運
習 羽 翅
変 恋 赤 亦
引 弓 弔
行 術 街 衍
急 忘 思 息
付 府 附
気 汽
業 葉 薬
空 穴 突
最 取 量
予 子 矛
坊 防 房 放
集 隹 住
文 交 父
法 去 泊
地 池 他
理 里 埋
注 主 住
電 申 由
動 重 働
音 暗 意
冷 凉 冫
光 先 元
色 角 免
命 令 乞
分 刀 切
社 土 仕
柔 矛 矢
彼 皮 破
経 軽 径
験 駅 験
済 斉 齊
研 硯
決 快
君 群
着 著 看
講 構
工 王
港 江
無 舞
治 冶
慣 貫
眠 眼
"""


def shuffle_options(options, item_id):
    """Stable, per-item shuffle shared by all generated choice sets."""
    result = list(options)
    seed = int.from_bytes(hashlib.sha256(item_id.encode("utf-8")).digest()[:8], "big")
    random.Random(seed).shuffle(result)
    return result


def kanji_count(word):
    return sum(bool(KANJI.fullmatch(c)) for c in word)


def shape(word):
    """Keep kana positions/okurigana fixed and count kanji slots."""
    return tuple("K" if KANJI.fullmatch(c) else c for c in word)


def reading_distractors(reading, same_kanji_words):
    found = set()
    for long, short in LONG:
        start = 0
        while True:
            index = reading.find(long, start)
            if index < 0:
                break
            found.add(reading[:index] + short + reading[index + len(long):])
            start = index + len(long)
        start = 0
        while True:
            index = reading.find(short, start)
            if index < 0:
                break
            if not reading.startswith(long, index):
                found.add(reading[:index] + long + reading[index + len(short):])
            start = index + len(short)
    for i, char in enumerate(reading):
        if char in VOICE:
            found.add(reading[:i] + VOICE[char] + reading[i + 1:])
        elif char in UNVOICE:
            found.add(reading[:i] + UNVOICE[char] + reading[i + 1:])
    for i, char in enumerate(reading):
        if i > 0 and char in SMALL_TSU_BEFORE and reading[i - 1] != "っ":
            found.add(reading[:i] + "っ" + reading[i:])
        if char == "っ":
            found.add(reading[:i] + reading[i + 1:])
    if "ん" in reading:
        found.add(reading.replace("ん", "", 1))
    # Adding ん inside arbitrary words creates non-words (e.g. ちかんら).
    found.update(same_kanji_words)
    return sorted(x for x in found if x and x != reading and all(KANA.fullmatch(c) for c in x))


def orthography_distractors(word, row_candidates, lookalikes, same_on_reading):
    result = set()
    target_shape = shape(word)
    for candidate in row_candidates:
        if candidate != word and shape(candidate) == target_shape:
            result.add(candidate)
    for pos, char in enumerate(word):
        if not KANJI.fullmatch(char):
            continue
        replacements = (lookalikes.get(char, set()) & SAFE_LOOKALIKE_KANJI) | same_on_reading.get(char, set())
        for replacement in replacements:
            candidate = word[:pos] + replacement + word[pos + 1:]
            if candidate != word and shape(candidate) == target_shape:
                result.add(candidate)
    return sorted(result)


def item(item_id, mondai, stem, choices, answer, word, reading, meaning, skill):
    return {
        "id": item_id, "section": "vocab", "mondai": mondai,
        "tier_prior": "easy", "level": "N4-core", "stem": stem,
        "options": choices, "answer": answer,
        "tags": ["word:" + word, "skill:" + skill],
        "confusion_pair": None, "passage_id": None, "audio": None, "image": None,
        "explanation_en": f"{word} = {reading} ({meaning})",
        "distractor_notes": {},
        "source": {"kind": "generated", "ref": "data/vocabulary.csv"},
        "verified": True,
    }


def main():
    with (paths.DATA / "vocabulary.csv").open(encoding="utf-8-sig", newline="") as f:
        rows = list(csv.DictReader(f))
    rows = [r for r in rows if KANJI.search(r["kanji"]) and not any(c in r["reading"] for c in ";、/")]
    by_reading = {}
    by_kanji = {}
    kanji_on_readings = {}
    for row in rows:
        by_reading.setdefault(row["reading"], set()).add(row["kanji"])
        for char in set(row["kanji"]):
            if KANJI.fullmatch(char):
                by_kanji.setdefault(char, set()).add(row["reading"])
        # Single-kanji vocabulary entries give direct reading evidence. Use
        # shared readings to find replacement characters in the same slots.
        if len(row["kanji"]) == 1 and KANJI.fullmatch(row["kanji"]):
            kanji_on_readings.setdefault(row["kanji"], set()).add(row["reading"])
    reading_to_kanji = {}
    for char, readings in kanji_on_readings.items():
        for reading in readings:
            reading_to_kanji.setdefault(reading, set()).add(char)
    same_on_reading = {
        char: set().union(*(reading_to_kanji.get(reading, set()) for reading in readings)) - {char}
        for char, readings in kanji_on_readings.items()
    }
    lookalikes = {}
    pairs = LOOKALIKE_PAIRS.split()
    for a, b in zip(pairs[::2], pairs[1::2]):
        lookalikes.setdefault(a, set()).add(b)
        lookalikes.setdefault(b, set()).add(a)
    for group in LOOKALIKE_GROUPS.splitlines():
        chars = [char for char in group.split() if char in SAFE_LOOKALIKE_KANJI]
        for i, a in enumerate(chars):
            for b in chars[i + 1:]:
                lookalikes.setdefault(a, set()).add(b)
                lookalikes.setdefault(b, set()).add(a)

    out = []
    skipped_reading = skipped_orthography = 0
    for row in rows:
        word, reading = row["kanji"], row["reading"]
        shared_readings = set()
        for char in set(word):
            if not KANJI.fullmatch(char):
                continue
            direct = kanji_on_readings.get(char, set())
            for source_reading in direct:
                start = 0
                while source_reading and (index := reading.find(source_reading, start)) >= 0:
                    for alternate in direct - {source_reading}:
                        variant = reading[:index] + alternate + reading[index + len(source_reading):]
                        if variant != reading:
                            shared_readings.add(variant)
                    start = index + 1
        read_candidates = reading_distractors(reading, shared_readings)
        variants = (
            ("kanji_reading", reading, read_candidates, "long_vowel", f"【{word}】"),
            ("orthography", word, orthography_distractors(word, by_reading.get(reading, ()), lookalikes, same_on_reading), "orthography", f"【{reading}】"),
        )
        for mondai, key, candidates, skill, stem in variants:
            if len(candidates) < 3:
                if mondai == "kanji_reading":
                    skipped_reading += 1
                else:
                    skipped_orthography += 1
                continue
            item_id = f"vocab-{'kr' if mondai == 'kanji_reading' else 'or'}-20261025-{int(row['index']):05d}"
            selected = [key] + candidates[:3]
            choices = shuffle_options(selected, item_id)
            out.append(item(item_id, mondai, stem, choices, choices.index(key) + 1,
                            word, reading, row["meaning"], skill))

    dest = paths.BANK / "vocab" / "generated_kanji.json"
    dest.parent.mkdir(parents=True, exist_ok=True)
    dest.write_text(json.dumps(out, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(f"Wrote {len(out)} items ({len(out)//2} words); skipped {skipped_reading} for reading distractors and {skipped_orthography} for orthography distractors")
    print("Answer positions:", {i: sum(x["answer"] == i for x in out) for i in range(1, 5)})
    if hasattr(sys.stdout, "reconfigure"):
        sys.stdout.reconfigure(encoding="utf-8")
    print("15 random samples:")
    for sample in random.Random(20261025).sample(out, min(15, len(out))):
        print(json.dumps(sample, ensure_ascii=False))


if __name__ == "__main__":
    main()
