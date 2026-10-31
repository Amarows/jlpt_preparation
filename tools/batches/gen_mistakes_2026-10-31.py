"""Batch 1 of mistake-driven items (2026-10-31). Correct option first; shuffled below. Each row names its parent mistake."""
import hashlib, json, random, sys
from pathlib import Path

G = "grammar_form"
ROWS = [
 # (parent item, mondai, tag, stem, options, explanation)
 ("placement-10", G, "grammar:のに", "薬を 飲んだ（　　）、熱が 下がりません。", ["のに", "ので", "から", "ために"], "のに = even though: the result is not what you expect."),
 ("placement-10", G, "grammar:のに", "この レストランは 高い（　　）、あまり おいしくないです。", ["のに", "ので", "から", "と"], "Expensive yet not tasty: unexpected, so のに."),
 ("placement-10", G, "grammar:のに", "あした テストが ある（　　）、弟は ゲームばかり して います。", ["のに", "ので", "から", "ために"], "A test tomorrow, yet he only plays games: のに."),
 ("gr-hajimeru-075", G, "grammar:始める", "赤ちゃんが 急に 泣き（　　）ました。", ["始め", "続け", "すぎ", "終わり"], "急に + ～始める = suddenly started crying."),
 ("gr-tsuzukeru-080", G, "grammar:続ける", "三時間 歩き（　　）、足が いたく なりました。", ["続けて", "始めて", "出して", "終わって"], "～続ける = keep doing: walked for three hours straight."),
 ("gr-tsuzukeru-080", G, "grammar:すぎる", "ケーキを 食べ（　　）、おなかが いたいです。", ["すぎて", "始めて", "やすくて", "終わって"], "～すぎる = too much: ate too much cake."),
 ("gr-hajimeru-075", G, "grammar:終わる", "この 本は とても 長いので、まだ 読み（　　）いません。", ["終わって", "始めて", "すぎて", "やすくて"], "まだ 読み終わって いない = haven't finished reading yet."),
 ("gr-tearu-052", G, "grammar:てある", "つくえの 上に 花が かざって（　　）。", ["あります", "います", "おきます", "みます"], "Transitive かざる + てある = someone put the flowers there."),
 ("gr-teiru-054", G, "grammar:ている", "電気が ついて（　　）。だれか いるのでしょう。", ["います", "あります", "おきます", "しまいます"], "Intransitive つく + ている = the light is on."),
 ("gr-tearu-052", G, "grammar:てある", "パーティーの 飲み物は もう 買って（　　）から、だいじょうぶです。", ["あります", "います", "みます", "いきます"], "買って ある = already bought, ready for later."),
 ("gr-teiru-054", G, "grammar:ている", "ドアが しまって（　　）から、ノックして ください。", ["います", "あります", "おきます", "みます"], "Intransitive しまる + ている = the door is shut."),
 ("gr-transitive-092", G, "grammar:transitive", "寒いので、窓を（　　）ください。", ["しめて", "しまって", "ついて", "きえて"], "窓を しめる (transitive, with を); しまる has no object."),
 ("gr-transitive-092", G, "grammar:intransitive", "風で ドアが 急に（　　）。", ["あきました", "あけました", "つけました", "けしました"], "ドアが あく (intransitive, with が): nobody opened it."),
 ("gr-transitive-092", G, "grammar:transitive", "へやが 暗いですね。電気を（　　）か。", ["つけましょう", "つきましょう", "きえましょう", "あきましょう"], "電気を つける (transitive, with を)."),
 ("gr-questionka-095", G, "grammar:question word + か", "さっき だれ（　　）から 電話が ありましたよ。", ["か", "も", "でも", "が"], "だれか = someone."),
 ("gr-questionka-095", G, "grammar:question word + か", "夏休みは どこ（　　）行きたいですね。", ["かへ", "もへ", "でも", "が"], "どこかへ 行きたい = want to go somewhere."),
 ("gr-questionka-095", G, "grammar:question word + か", "のどが かわきましたね。何（　　）飲みましょう。", ["か", "も", "が", "まで"], "何か 飲みましょう = let's drink something."),
 ("gr-passive-003", G, "grammar:passive", "電車の 中で だれかに さいふを（　　）。", ["とられました", "とらせました", "とりました", "とれました"], "Passive: someone stole my wallet (I was affected)."),
 ("gr-passive-003", G, "grammar:passive", "きのう 雨に（　　）、かぜを ひきました。", ["ふられて", "ふらせて", "ふって", "ふれて"], "雨に ふられる = get caught in the rain (passive of trouble)."),
 ("gr-passive-003", G, "grammar:passive", "先生に 名前を（　　）、大きな 声で 返事を しました。", ["よばれて", "よばせて", "よんで", "よべて"], "My name was called by the teacher: passive よばれる."),
 ("gr-zuni-086", G, "grammar:ずに", "かさを 持た（　　）出かけたので、雨に ぬれました。", ["ずに", "なくて", "なければ", "ないと"], "持たずに = without taking (an umbrella)."),
 ("gr-zuni-086", G, "grammar:ずに", "よく 考え（　　）答えを 書いて しまいました。", ["ずに", "なくて", "ないと", "なければ"], "考えずに = without thinking."),
 ("gr-zuni-086", G, "grammar:ずに", "ゆうべは ね（　　）宿題を しました。", ["ずに", "なくて", "ないと", "ても"], "ねずに = without sleeping."),
 ("gr-tara-011", G, "grammar:たら", "家に（　　）、メールを ください。", ["帰ったら", "帰ると", "帰るなら", "帰れば"], "～たら + request: once you get home."),
 ("placement-14", G, "grammar:たら", "仕事が（　　）、いっしょに 食事に 行きましょう。", ["終わったら", "終わると", "終わるなら", "終われば"], "～たら + invitation: when work is over."),
 ("placement-14", G, "grammar:たら", "わからない ことが（　　）、いつでも 聞いて ください。", ["あったら", "あると", "あって", "あるのに"], "～たら + request: if there is something."),
 ("gr-tagaru-064", G, "grammar:たがる", "妹は 新しい ゲームを（　　）います。", ["ほしがって", "ほしくて", "ほしいで", "ほしかって"], "Someone else's wish: ほしがって いる."),
 ("gr-tagaru-064", G, "grammar:たがる", "弟は 毎日 公園へ 行き（　　）。", ["たがります", "たいです", "たかったです", "たくて"], "Third person's wish: ～たがる, not ～たい."),
 ("gr-tagaru-064", G, "grammar:たがる", "むすこは 医者に なり（　　）いるようです。", ["たがって", "たくて", "たいで", "たかって"], "～たがって いる for another person's wish."),
 ("gr-hearsay-019", G, "grammar:そうだ (hearsay)", "テレビの ニュースに よると、あしたは 雨が（　　）そうです。", ["ふる", "ふり", "ふって", "ふった"], "Hearsay: plain form + そうです (によると)."),
 ("gr-hearsay-019", G, "grammar:そうだ (looks like)", "空が 暗く なって きました。雨が（　　）そうです。", ["ふり", "ふる", "ふった", "ふって"], "Looks about to: stem + そう (ふりそう)."),
 ("gr-hearsay-019", G, "grammar:そうだ (hearsay)", "田中さんの 話では、あの 店の ラーメンは とても（　　）そうです。", ["おいしい", "おいし", "おいしく", "おいしいの"], "Hearsay keeps the full い-adjective: おいしいそうです."),
 ("gr-hearsay-019", G, "grammar:そうだ (looks like)", "この ケーキ、（　　）そうですね。一つ ください。", ["おいし", "おいしい", "おいしく", "おいしいの"], "Looks tasty: drop い → おいしそう."),
 ("gr-comp-029", G, "grammar:までに", "レポートは 金曜日（　　）出して ください。", ["までに", "まで", "までで", "ごろに"], "までに = by (a deadline); まで = until."),
 ("gr-comp-029", G, "grammar:まで", "きのうは 夜 11時（　　）べんきょうしました。", ["まで", "までに", "からに", "のに"], "まで = until: studied continuously until 11."),
 ("gr-comp-029", G, "grammar:までに", "5時（　　）帰らなければ なりません。", ["までに", "まで", "ので", "から"], "Must be back by 5: までに."),
 ("placement-09", "usage", "word:ていねい", "ていねい", ["先生は いつも ていねいに 教えて くれます。", "きょうは ていねいな 雨が ふって います。", "この 部屋は ていねいで、とても 広いです。", "ていねいが あるので、病院へ 行きます。"], "ていねい = careful/polite, about how people do things."),
 ("placement-09", "usage", "word:ねっしん", "ねっしん", ["兄は しごとに ねっしんで、毎日 おそくまで はたらいて います。", "この スープは ねっしんなので、気を つけて ください。", "ねっしんが 出たので、学校を 休みました。", "ねっしんな 日が つづいて、つかれました。"], "ねっしん = keen, hard-working; only about people's attitude."),
 ("vocab-or-20261025-00158", "usage", "word:十分", "じゅうぶん", ["時間は じゅうぶん ありますから、ゆっくり 行きましょう。", "あの 人は とても じゅうぶんな 人です。", "じゅうぶん ねて いないので、元気です。", "毎日 じゅうぶんを 食べて います。"], "じゅうぶん = enough: there is enough time."),
 ("placement-01", "kanji_reading", "word:空港", "【空港】まで バスで 行きます。", ["くうこう", "くこう", "くうこ", "くこ"], "空港 = くうこう: both syllables are long."),
 ("placement-01", "kanji_reading", "word:教室", "【教室】で 待って います。", ["きょうしつ", "きょしつ", "ぎょうしつ", "きょうしち"], "教室 = きょうしつ, with a long きょう."),
 ("vocab-kr-20261025-00299", "kanji_reading", "word:昔", "【昔】は この あたりに 川が ありました。", ["むかし", "むがし", "むかじ", "むっかし"], "昔 = むかし, no dakuten."),
 ("vocab-kr-20261025-00240", "kanji_reading", "word:答え", "テストの【答え】を 書いて ください。", ["こたえ", "こだえ", "こたい", "ことえ"], "答え = こたえ."),
]

def main(home):
    import sys as _s; _s.path.insert(0, str(Path(__file__).resolve().parent))
    attempts = [json.loads(l) for l in (Path(home) / "confidential" / "attempts.jsonl").read_text(encoding="utf-8").splitlines() if l.strip()]
    last_ts = {}
    for a in attempts:
        if not a.get("correct"): last_ts[a["item_id"]] = a["ts"]
    out = {"grammar": [], "vocab": []}
    for n, (parent, mondai, tag, stem, opts, expl) in enumerate(ROWS, 1):
        section = "grammar" if mondai == G else "vocab"
        iid = f"{'gr' if section == 'grammar' else 'vc'}-gen-mis-{n:03d}"
        order = list(range(4)); random.Random(int(hashlib.md5(iid.encode()).hexdigest(), 16)).shuffle(order)
        out[section].append({"id": iid, "section": section, "mondai": mondai, "tier_prior": "medium", "level": "N4-core",
            "stem": stem, "options": [opts[i] for i in order], "answer": order.index(0) + 1, "tags": [tag],
            "confusion_pair": None, "passage_id": None, "audio": None, "image": None, "explanation_en": expl, "distractor_notes": {},
            "source": {"kind": "generated", "ref": f"written for the mistake on {parent}", "author": "claude-opus-5-5",
                       "batch": f"{section}/gen_mistakes_2026-10-31", "created": "2026-10-31",
                       "parent_item": parent, "parent_attempt": last_ts.get(parent)},
            "verified": False})
    for section, items in out.items():
        f = Path(home) / "data" / "bank" / section / "gen_mistakes_2026-10-31.json"
        f.write_text(json.dumps(items, ensure_ascii=False, indent=2), encoding="utf-8"); print(f, len(items))

main(sys.argv[1])
