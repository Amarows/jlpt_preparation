"""Batch 1 of generated vocab 問題3 (contextual) items for N4 words that had no item. Correct option first; shuffled below."""
import hashlib, json, random, sys
from pathlib import Path

B = [
 ("案内", "駅から ホテルまで 友だちが（　　）して くれました。", ["あんない", "しょうかい", "よやく", "けんぶつ"], "案内する = to show someone the way."),
 ("アルバイト", "大学に 行きながら、コンビニで（　　）を して います。", ["アルバイト", "けんがく", "けんきゅう", "よやく"], "アルバイト = part-time job, done at a shop."),
 ("浅い", "この 川は（　　）ので、子どもでも あんぜんです。", ["あさい", "ふかい", "はやい", "うすい"], "あさい = shallow, so safe for children."),
 ("集まる", "あしたの 朝 9時に 駅の 前に（　　）ください。", ["あつまって", "あつめて", "ならべて", "まぜて"], "あつまる (intransitive) = people gather; あつめる needs an object."),
 ("集める", "わたしの しゅみは 古い 切手を（　　）ことです。", ["あつめる", "あつまる", "つつむ", "おとす"], "切手を あつめる = collect stamps (transitive, with を)."),
 ("謝る", "約束の 時間に おくれて しまったので、友だちに（　　）。", ["あやまりました", "ほめました", "いのりました", "かまいました"], "Late for a meeting, so you apologise: あやまる."),
 ("倍", "この 店の ケーキは、ほかの 店の 二（　　）の 大きさです。", ["ばい", "かい", "ど", "だい"], "二倍 (にばい) = twice as big."),
 ("びっくり", "後ろから 大きな 声で 名前を 呼ばれて、（　　）しました。", ["びっくり", "はっきり", "しっかり", "ゆっくり"], "びっくりする = to be startled."),
 ("チェック", "しゅくだいを 出す 前に、まちがいが ないか もう一度（　　）して ください。", ["チェック", "ノック", "セット", "サイン"], "チェックする = check for mistakes."),
 ("できるだけ", "あしたは しけんなので、今日は（　　）早く ねて ください。", ["できるだけ", "なかなか", "ちっとも", "ずいぶん"], "できるだけ早く = as early as possible."),
 ("どんどん", "春に なって、木の 葉が 毎日（　　）大きく なって います。", ["どんどん", "そろそろ", "まだまだ", "ぜんぜん"], "どんどん = steadily, more and more."),
 ("泥棒", "夜、（　　）が 入って、お金を とられました。", ["どろぼう", "けいかん", "おまわりさん", "おきゃくさん"], "どろぼう = thief, who took the money."),
 ("選ぶ", "赤と 青の セーター、どちらが いいか（　　）ください。", ["えらんで", "ひろって", "かざって", "はらって"], "どちらが いいか えらぶ = choose which one."),
 ("増える", "日本に 来る 外国人が 毎年（　　）います。", ["ふえて", "ふやして", "まけて", "こわれて"], "ふえる (intransitive) = increase; ふやす needs an object."),
 ("踏む", "電車の 中で、となりの 人に 足を（　　）。", ["ふまれました", "ひかれました", "かまれました", "ほめられました"], "足を ふまれる = have one's foot stepped on."),
 ("原因", "火事の（　　）は たばこだそうです。", ["げんいん", "けいかく", "きかい", "しゅみ"], "げんいん = cause."),
 ("ごちそう", "先生の お宅で、おいしい 料理を（　　）に なりました。", ["ごちそう", "おみまい", "おじゃま", "おせわ"], "料理を ごちそうに なる = be treated to a meal."),
 ("ごみ", "もえる（　　）は 月曜日と 木曜日の 朝に 出して ください。", ["ごみ", "おみやげ", "しゅくだい", "てがみ"], "ごみを 出す = put out the rubbish, on collection days."),
 ("ご覧になる", "先生、この 写真を もう（　　）か。", ["ごらんに なりました", "はいけんしました", "まいりました", "いただきました"], "ごらんに なる: respectful 'see' for the teacher; はいけんする is humble."),
 ("はっきり", "声が 小さくて 聞こえません。もう 少し（　　）話して ください。", ["はっきり", "そっと", "びっくり", "すっかり"], "はっきり 話す = speak clearly."),
 ("払う", "レストランで、お金は わたしが（　　）。", ["はらいます", "ひろいます", "おとします", "かえします"], "お金を はらう = pay."),
 ("変", "この 牛乳、（　　）においが します。飲まない ほうが いいですよ。", ["へんな", "ていねいな", "ねっしんな", "じゆうな"], "へんな におい = a strange smell."),
 ("冷える", "ビールは れいぞうこで よく（　　）います。", ["ひえて", "さめて", "かわいて", "やけて"], "ひえる = get cold; さめる is for hot things cooling down."),
 ("拾う", "道で さいふを（　　）ので、交番に とどけました。", ["ひろった", "おとした", "なくした", "ぬすんだ"], "Found a wallet and took it to the police box: ひろう."),
 ("褒める", "テストで 100点を とったので、先生に（　　）。", ["ほめられました", "しかられました", "わらわれました", "いじめられました"], "100 points, so the teacher praised her: ほめられる."),
 ("ほとんど", "宿題は（　　）終わりました。あと 少しです。", ["ほとんど", "ちっとも", "ぜひ", "きっと"], "ほとんど 終わった = almost finished."),
 ("以内", "この 本は 二週間（　　）に 返して ください。", ["いない", "いじょう", "いがい", "いか"], "二週間いない = within two weeks."),
 ("いっぱい", "たくさん 食べたので、おなかが（　　）です。", ["いっぱい", "ぺこぺこ", "じゅうぶん", "たいへん"], "おなかが いっぱい = full; ぺこぺこ = hungry."),
 ("帰り", "会社の（　　）に、スーパーで 買い物を しました。", ["かえり", "もどり", "ゆき", "あいだ"], "会社の かえりに = on the way home from work."),
 ("変える", "この へやは 暗いので、カーテンの 色を（　　）つもりです。", ["かえる", "かわる", "かざる", "かぞえる"], "色を かえる (transitive) = change the colour; かわる has no object."),
 ("構う", "ここで たばこを すっても（　　）か。", ["かまいません", "しかたありません", "ちがいません", "こまりません"], "～ても かまいませんか = is it all right if...?"),
 ("噛む", "この 肉は かたくて、なかなか（　　）ません。", ["かめ", "のめ", "ふめ", "ぬげ"], "かたい 肉は かめない = can't chew."),
 ("必ず", "あしたの 会議には（　　）来て ください。", ["かならず", "たぶん", "なかなか", "めったに"], "かならず 来て ください = be sure to come."),
 ("代わり", "父が いそがしいので、わたしが 父の（　　）に 会議に 出ました。", ["かわり", "まま", "ばかり", "ころ"], "父の かわりに = in place of my father."),
 ("飾る", "たんじょうびの パーティーの ために、へやに 花を（　　）。", ["かざりました", "かぞえました", "かけました", "つつみました"], "花を かざる = decorate with flowers."),
 ("怪我", "自転車で ころんで、足に（　　）を しました。", ["けが", "びょうき", "かじ", "けんか"], "けがを する = get hurt."),
 ("経済", "大学で 日本の（　　）を べんきょうして、銀行に しゅうしょくしたいです。", ["けいざい", "けしき", "けいかく", "けんぶつ"], "けいざい = economics, fits a bank job."),
 ("鏡", "出かける 前に、（　　）で かみを 見ました。", ["かがみ", "まど", "かべ", "しゃしん"], "かがみで 見る = look in the mirror."),
 ("火事", "となりの 家が（　　）に なって、消防車が 来ました。", ["かじ", "じこ", "けが", "じしん"], "家が かじに なる = the house caught fire."),
 ("いじめる", "弱い 動物を（　　）のは よくないです。", ["いじめる", "ほめる", "さわぐ", "あやまる"], "いじめる = to bully, which is not good."),
]

out = []
for n, (word, stem, opts, expl) in enumerate(B, 1):
    iid = f"vc-gen-ctx-{n:03d}"
    order = list(range(4)); random.Random(int(hashlib.md5(iid.encode()).hexdigest(), 16)).shuffle(order)
    out.append({"id": iid, "section": "vocab", "mondai": "contextual", "tier_prior": "medium", "level": "N4-core",
                "stem": stem, "options": [opts[i] for i in order], "answer": order.index(0) + 1, "tags": [f"word:{word}"],
                "confusion_pair": None, "passage_id": None, "audio": None, "image": None, "explanation_en": expl, "distractor_notes": {},
                "source": {"kind": "generated", "ref": "N4 word without an item (data/vocabulary.csv)", "author": "claude-opus-5-5",
                           "batch": "vocab/gen_contextual_2026-10-31", "created": "2026-10-31"},
                "verified": True})
Path(sys.argv[1]).write_text(json.dumps(out, ensure_ascii=False, indent=2), encoding="utf-8")
print(len(out), sorted(x["answer"] for x in out).count(1), [x["answer"] for x in out])
