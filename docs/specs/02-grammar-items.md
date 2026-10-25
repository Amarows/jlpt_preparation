# Spec 02 — Generated grammar and instruction-phrase items

Read `docs/SCHEMA.md`; every item must match it exactly. Write UTF-8 JSON arrays to:
- `data/bank/grammar/generated_form.json`: **100 `grammar_form` items**
- `data/bank/grammar/generated_composition.json`: **30 `sentence_composition` items**
- `data/bank/vocab/instruction_phrases.json`: **15 `instruction_phrase` items** (section `vocab`)

## Coverage
Cover the standard JLPT N4 grammar list (~130 points), with the high-yield points getting 2–3 items each: potential, passive (direct and suffering), causative, causative-passive, ～ば / ～たら / ～と / ～なら, ～そうだ (appearance vs hearsay), ～ようだ / ～らしい / ～みたい, ～ようにする / ～ようになる, ～ことにする / ～ことになる, あげる / くれる / もらう and their ～て forms, ～てしまう, ～ておく, ～てある vs ～ている, ～ながら, ～のに vs ～ので, ～し, ～たがる, ～ばかり, ～はずだ, ～かもしれない, ～つもり, ～予定, ～始める / ～終わる / ～続ける, ～やすい / ～にくい, ～すぎる, ～ずに / ～ないで, ～まま, ～場合, keigo (honorific/humble basics: いらっしゃる, おっしゃる, 召し上がる, 申す, 参る, お～になる, お～する), transitive/intransitive pairs (開ける/開く etc.), ～かどうか, question word + か, ～ところ, ～間 / ～間に, ～までに vs ～まで.

## Rules
- Mirror real N4 sentential-grammar items: one natural sentence, a single blank `(　　)`, 4 options of the same grammatical kind.
- **Exactly one defensible answer.** Avoid options that are acceptable in casual speech. Prefer distractors that expose a known confusion; record that confusion in `confusion_pair` (e.g. `"のに/ので"`) and in `distractor_notes`.
- Sentence composition: 4 pieces in the options, stem with `＿＿ ＿＿ ★ ＿＿`; `answer` = the number of the piece in the ★ slot. Make sure every grammatical ordering puts the same piece at ★.
- Only N5/N4 kanji; write anything harder in kana.
- Tier mix: 40% easy, 40% medium, 20% hard. Level mix: 20% N5, 60% N4-core, 20% N4-hard.
- Tags: the primary tag first (`grammar:<point>`), e.g. `["grammar:のに", "skill:contrast"]`.
- `explanation_en`: one line, ≤140 characters, why the answer is right.
- `distractor_notes`: one note per wrong option.
- ids: `gr-<romaji-point>-NNN`; instruction phrases `ip-NNN`.
- `source: {"kind":"generated","ref":"codex spec 02"}`, `verified: false` (a separate blind check sets it to true).
- Instruction phrases: exam question stems Anna must parse instantly (e.g. 文章の内容と合っているものはどれですか, ＿＿の　ことばは　どう　よみますか, ★に　入る　ものは　どれですか, 正しい　ものを　一つ　えらんで　ください, 何を　しなければ　なりませんか). Stem = the Japanese phrase; options = 4 English meanings; tier easy; tag `phrase:<short>`.

When done, run `python -c` to check that each file loads as JSON with the right counts and unique ids, then print counts by tier, level and primary tag.
