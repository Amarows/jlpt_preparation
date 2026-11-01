# Write wrong-answer explanations for JLPT N4 items

The learner, Anna, studies for JLPT N4 in English. When she answers a question wrong it is usually because she does not
know what the words mean, or does not understand the whole sentence. For reading and listening she needs to see the exact
lines that give the answer and how the answer follows from them. Your explanation is shown right after her wrong answer.

Read the brief file named in the task. It is a JSON array of items. Each item has `id`, `section`, `mondai`, `stem`,
`options`, `answer` (1-based), `explanation_en` (an old one-line note), and where relevant `passage` (reading text) or
`script` (listening transcript). Write one JSON object to the output file named in the task: `{"<id>": {...}, ...}`,
with one entry per item, UTF-8, no comments. Write nothing else.
If an item has `previous_errors`, an earlier draft for it failed these automatic checks: fix every one of them.

## Fields of each entry

- `sentence`: the key Japanese sentence with furigana (format below).
  - Blank items (`grammar_form`, `contextual`): the stem with the correct option written into the （　） blank.
  - `kanji_reading`, `paraphrase`: the stem as it is, without the 【 】 marks.
  - `orthography`: the stem with the underlined 【かな】 replaced by the correct option.
  - `usage`: the correct option sentence.
  - `sentence_composition`: the complete correct sentence, all four options in their right order.
  - `text_grammar`: the sentence from the passage that holds the blank, with the correct option written in, without the （14） number.
  - Reading and listening: the question (the stem) as it is.
  Keep the text identical to the source apart from the furigana, the filled blank and the removed 【 】; spaces may be dropped.
- `translation_en`: natural English translation of `sentence`.
- `options`: one entry per option, in order: `{"ruby": "<the option text with furigana>", "en": "<its meaning>"}`.
  `ruby` must be the option text exactly, plus furigana. For a kanji reading item, `en` of a wrong reading says what it is,
  e.g. "not a word" or "reading of 新聞 (newspaper), not of this word". For a grammar item, `en` says what the form means
  and, for wrong options, in a few words why it does not fit here. For reading and listening, translate the option.
- `words`: 2 to 8 key words from the sentence, passage lines or options that the learner may not know, especially in the
  correct answer: `{"w": "dictionary form as written", "r": "reading in hiragana", "en": "short meaning"}`.
- `evidence` (reading, listening and `text_grammar` only, otherwise leave it out): 1 to 3 lines from the passage or script
  that give the answer: `{"text": "<exact copy>", "ruby": "<the same with furigana>", "en": "<translation>"}`. `text` must
  be copied character for character from the passage or script, within one line (no line breaks), so it can be found and
  highlighted. Keep each quote short: the clause that matters, not a whole paragraph.
- `steps`: 1 to 3 short English sentences on how to get from the sentence or the evidence to the correct option, e.g.
  "She could not find the platform for her transfer → that is option 3". Japanese words in steps may carry furigana.
  Do not repeat the translation.

## Furigana format

Write `{漢字|かんじ}` around every kanji, with the reading in hiragana. Put okurigana outside the braces:
`{上|あ}がる`, `{食|た}べました`, `{来週|らいしゅう}`, `{大|おお}きい`. A whole word may share one brace when its kanji
are read together (`{今日|きょう}`, `{一人|ひとり}`). Every kanji in `sentence`, `options[].ruby` and `evidence[].ruby`
must be inside braces; kana, numbers and punctuation stay outside. Use the reading the word has in this sentence.
Never put furigana inside `text`, `w` or `en`.

## Quality

Be correct above all. If unsure about a reading or meaning, choose the standard dictionary reading. English must be
short and plain (N4 learner, B2 English). Do not invent facts that are not in the passage or script.

## Example

```json
{"gr-noni-001": {
  "sentence": "たくさん べんきょうしたのに、テストは よく なかったです。",
  "translation_en": "Even though I studied a lot, the test did not go well.",
  "options": [{"ruby": "ので", "en": "because: gives a reason, but studying is not a reason for a bad test"},
              {"ruby": "から", "en": "because: same problem as ので"},
              {"ruby": "と", "en": "when/if: a natural consequence, does not fit"},
              {"ruby": "のに", "en": "even though: the result is the opposite of what you expect"}],
  "words": [{"w": "勉強する", "r": "べんきょうする", "en": "to study"}],
  "steps": ["Studied a lot, but the test went badly: the result is unexpected, so のに."]
}}
```
