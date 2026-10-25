# Spec 03 — Item quality fixes

Read `docs/SCHEMA.md`. Data lives under `JLPT_HOME` (env var). Three fixes, all in one pass.

## A. Vocabulary generator (`tools/gen_vocab_items.py`), then regenerate
Problems found in review: the correct answer is almost always option 1 or 4, and many distractors are obviously fake (`い階建て`, `くく`, `おくじょうう`, `おうもいだす`, or unrelated words like `あがる` offered for 汽車).
1. **Shuffle option order** with a per-item seed (hash of the id), so answer positions are uniform over 1–4. Apply the same shuffle helper in every generator, and add a test that checks the distribution (each position 20–30% over the generated set).
2. **Reading distractors must look like plausible real readings.** Allowed transformations: long vowel dropped or added at a mora that can carry one (ゅう↔ゅ, ょう↔ょ, おう↔お, えい↔え, ゆう↔ゆ); dakuten toggled on a kana that can carry it (か↔が, し↔じ, …); small っ added before a k/s/t/p-row kana or removed; ん removed or added before a consonant; the on'yomi of one kanji swapped for another common on'yomi of the same kanji, taken from other vocabulary words containing it. **Forbidden:** prefixing お/う to the word, doubling a final vowel (おくじょうう), and readings of unrelated words. If fewer than 3 valid distractors exist, skip the word.
3. **Orthography distractors must be the same shape as the answer:** the same okurigana and the same number of kanji, all kanji (no kana fragments where the answer has kanji). Replace one kanji with (a) a kanji sharing the same reading in the vocabulary list, or (b) a visually similar kanji from a hard-coded look-alike table (at least 60 pairs for N5/N4, e.g. 体/休, 待/持/特, 間/問/聞, 買/貸/質, 末/未, 土/士, 午/牛, 右/石, 見/貝, 人/入, 日/目, 鳥/島, 借/貸, 京/東, 洗/先, 漢/館, 員/貝, 開/閉, 会/合, 理/里). If fewer than 3 valid distractors exist, skip the word.
4. Add an exam-style sentence where possible: stem = a short sentence with the word in 【 】, using a template by part of speech (noun: 「【X】を見ました。」-style is acceptable but must be grammatical; skip when no template fits). If this is too unreliable, keep the bare `【X】` stem.
5. Regenerate `data/bank/vocab/generated_kanji.json` with **new ids** (the old ones were shown to nobody, so overwrite them). Print counts and 15 random samples.

## B. Regenerate the 30 sentence-composition items (`data/bank/grammar/generated_composition.json`)
The current ones are broken: the stem is only `＿＿ ＿＿ ★ ＿＿` with no surrounding sentence, the options are already in sentence order, and most keys are wrong. Rewrite all 30, in real N4 format:
- The stem is a full sentence with fixed words before and/or after the four blanks, e.g. `この 本は ＿＿ ＿＿ ★ ＿＿ です。`
- The options are the 4 pieces in **shuffled** order (not sentence order).
- `answer` = the option number of the piece that lands in the ★ slot in the only grammatical order. Check this for every item, and make sure no second grammatical order puts a different piece at ★.
- Keep the SCHEMA fields, primary tag `grammar:<point>`, explanation_en (≤140 chars, with the full correct sentence), `verified: false`, ids `gr-comp-NNN`.

## C. Replace defective grammar_form items
In `data/bank/grammar/generated_form.json`, the items with `"verified": false` have a `review_note` explaining the defect (options built on the wrong verb, or several acceptable answers). Rewrite each of them in place (same grammar point, new id with suffix `-r`), so the item has one unambiguous answer, then set `verified: false` and delete the `review_note`. Leave verified items untouched.

General: only N5/N4 kanji in new text (write harder words in kana). Do not commit. Run `tools/verify_items.py` and the tests at the end, and report counts.
