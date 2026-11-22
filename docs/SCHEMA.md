# Data contract — JLPT N4 portal

This file is the contract between the engine, the server, the runner UI, the dashboard and every agent.
Change it only on purpose, and update all consumers in the same commit.

All files are UTF-8 JSON / JSONL. Paths are relative to the repo root and git-ignored (see `.gitignore`).
Set the env var `JLPT_HOME` to point the server, engine and dashboard at a different root (default: the repo root).

## Folders
| Path | Content | Writer |
|---|---|---|
| `data/bank/<section>/*.json` | Item files, each holding a JSON array of items | tools/, Codex, Claude |
| `data/bank/mocks/<mock_id>/` | Reserved full mock exams: `mock.json` (`id`, `title`, `opens`, `seen_before_mock`; the server adds `taken` and `result`), item files and `passages.json`. Kept out of practice until taken, then served like any other bank file | tools/, server |
| `audio/` | MP3 files and cropped booklet pictures referenced by items | tools/import_listening.py |
| `materials/` | Source books and PDFs | Alex |
| `data/explain.json` | Wrong-answer explanations, `{item_id: explain}` (see below) | tools/explain_items.py |
| `data/explain_drafts/<batch>/` | Briefs, drafts and the check report of one explanation batch | tools/explain_items.py |
| `confidential/attempts.jsonl` | One line per answer | server |
| `confidential/runs.jsonl` | One line per finished run | server |
| `confidential/model_state.json` | Latest model output (recomputed from logs) | engine |
| `confidential/explain_feedback.jsonl` | One line per "Still unclear" click on an explanation: `ts`, `item_id`, `choice` | server |
| `confidential/focus.json` | Tag boosts written by Claude's analysis | Claude |
| `confidential/analysis/YYYY-MM-DD.md` | Claude's qualitative gap analysis | Claude |

## Item
```json
{
  "id": "gr-noni-001",
  "section": "vocab | grammar | reading | listening",
  "mondai": "kanji_reading | orthography | contextual | paraphrase | usage | grammar_form | sentence_composition | text_grammar | short_passage | mid_passage | info_retrieval | task_based | key_points | verbal_expression | quick_response",
  "tier_prior": "easy | medium | hard",
  "level": "N5 | N4-core | N4-hard",
  "stem": "たくさん べんきょうした (　　)、テストは よく なかったです。",
  "options": ["ので", "から", "と", "のに"],
  "answer": 4,
  "tags": ["grammar:のに", "contrast"],
  "confusion_pair": "のに/ので",
  "passage_id": null,
  "audio": null,
  "image": null,
  "explanation_en": "のに = 'even though' (unexpected result); ので/から give a reason.",
  "distractor_notes": {"1": "reason instead of contrast"},
  "source": {"kind": "generated | book | web | official", "ref": "free text, e.g. jlptpracticetest.com/n4/3 q12",
             "author": "codex | claude-opus-5-5 | Japan Times | JLPT | ...", "batch": "grammar/generated_form",
             "created": "2026-11-01", "page": 42, "parent_item": "gr-noni-001", "parent_attempt": "2026-10-30T19:02:11+01:00"},
  "verified": true
}
```
- `answer` is 1-based. `options` has exactly 4 entries, except listening `verbal_expression` and `quick_response` items, which may have 3 (the spoken replies of 問題3 and 問題4).
- `stem` marks the underlined word with 【 】 and the ★ slot with ★.
- `passage_id` points to `data/bank/reading/passages.json` → `{"id", "text", "image"?}`; listening items use `audio: {"file": "audio/x.mp3", "start": 12.5, "end": 48.0}` (seconds; `start`/`end` are left out when the file holds one question; `duration` is the clip length, added to timed-run limits).
- Listening items also carry `script` (the transcript, sent to the browser only after the answer), `hide_options: true` when the options are spoken or drawn rather than printed (the buttons show only numbers until the answer), and `image` (a booklet picture, e.g. `audio/bpt1/img/1-1.png`). The question text (`stem`) is shown only after answering, as in the real test where it is spoken.
- `tags` use prefixes: `grammar:`, `word:`, `kanji:`, `skill:` (e.g. `skill:long_vowel`), `phrase:`.
- `source.author` and `source.batch` are required for new items: the batch groups items made together (a bank file, one generation run), so `tools/item_health.py` can compare batches and pull a bad one. `page` is the book page; `parent_item`/`parent_attempt` name the mistake a generated item was written for. `created` is the date the item was written.
- `distractor_notes` is in the track's original explanation language (English for N4, Japanese for de-work). Optional `distractor_notes_<lang>` (e.g. `distractor_notes_en`) has the same shape and gives the notes in another explanation language; when it is missing, `distractor_notes` is used. Likewise `explanation_<lang>` (`explanation_en`, `explanation_ja`). Optional `options_lang` / `stem_lang` mark options or a stem written in another language than the track's (e.g. `"ja"`).
- Only items with `verified: true` are served.
- Optional `revised: "YYYY-MM-DD"`: set when an item's stem, options or answer change. Attempts made before that date answered the old version, so the engine, the selection and the report ignore them.

## Explanation (`data/explain.json`)
Shown after a wrong answer (in practice, on the results page and in the mistakes list), never before. Kept apart from the
item files, so it never changes an item or its attempt history.
```json
{"gr-noni-001": {
  "sentence": "たくさん {勉強|べんきょう}したのに、テストは よく なかったです。",
  "translation_en": "Even though I studied a lot, the test did not go well.",
  "options": [{"ruby": "ので", "en": "because: …"}, {"ruby": "から", "en": "…"}, {"ruby": "と", "en": "…"}, {"ruby": "のに", "en": "even though"}],
  "words": [{"w": "勉強する", "r": "べんきょうする", "en": "to study"}],
  "evidence": [{"text": "exact one-line quote from the passage or script", "ruby": "the same with furigana", "en": "translation"}],
  "steps": ["How the answer follows, with {漢字|かんじ} furigana."],
  "for": "3f1c0a9b2d4e", "checked": "2026-11-01", "batch": "mistakes-2026-11-01"}}
```
- Furigana is written `{漢字|かんじ}`; every kanji in `sentence`, `options[].ruby` and `evidence[].ruby` has it, and without it the text equals the item's (`sentence`: the stem with the answer filled in, see `tools/explain_prompt.md`).
- `evidence` is required for reading, listening and `text_grammar`; each `text` appears verbatim in the passage or script, so the runner can highlight it.
- `for` is a fingerprint of the item's stem, options and answer. When the item changes, its explanation stops being served until it is rewritten.
- Items without an explanation get `{"fallback": true, "options": [...]}`: option meanings looked up in `data/vocabulary.csv`.

## Attempt (`confidential/attempts.jsonl`)
```json
{"ts": "2026-10-30T19:02:11+01:00", "run_id": "r-20261030-190000", "item_id": "gr-noni-001",
 "choice": 1, "correct": false, "ms": 14230, "flag": "none | unclear | guess", "mode": "drill | timed | practice | mock", "timed_out": false}
```
Optional `"review": true` marks an answer given in a "My mistakes" run (run `section: "mistakes"`, items whose latest answer was wrong). Review answers move Leitner boxes and can clear a mistake, but do not update section or tag abilities, P(pass) or the accuracy report, because the learner has already seen these items with feedback.

`ms` is measured in the browser (`performance.now()`), from the moment the item is shown to the moment it is answered. For a reading passage, the time spent reading the passage goes to the first question of that passage.

## Run (`confidential/runs.jsonl`)
```json
{"run_id": "r-20261030-190000", "start": "...", "end": "...", "mode": "timed", "section": "grammar | mixed | mistakes | ...",
 "n": 20, "correct": 16, "total_ms": 412000, "p_pass_before": 0.88, "p_pass_after": 0.89}
```

## Model state (`confidential/model_state.json`)
```json
{"updated": "...", "p_pass": 0.89, "p_pass_ema": 0.89, "band80": [0.81, 0.95], "trend": "up | flat | down",
 "p_lk_section": 0.99, "p_listening_section": 0.92, "p_total": 0.94,
 "exp_score": {"lk": 84, "listening": 36},
 "skills": {"grammar:のに": {"theta": 0.2, "sd": 0.8, "n": 3}},
 "speed": {"grammar_form": {"median_ms": 18000, "target_ms": 30000}},
 "mastered": {"count": 0, "by_section": {}},
 "days_left": 42}
```

## Placement diagnostic (seed data)
- Test and key: `data/bank/diagnostic/2026-10-25_placement_{test.md,key.json}`
- Attempt record: `confidential/attempts/2026-10-25_placement.json` (summary format, older than this schema; the engine imports it as prior evidence)
