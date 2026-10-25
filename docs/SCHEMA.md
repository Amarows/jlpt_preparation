# Data contract — JLPT N4 portal

This file is the contract between the engine, the server, the runner UI, the dashboard and every agent.
Change it only on purpose, and update all consumers in the same commit.

All files are UTF-8 JSON / JSONL. Paths are relative to the repo root and git-ignored (see `.gitignore`).
Set the env var `JLPT_HOME` to point the server, engine and dashboard at a different root (default: the repo root).

## Folders
| Path | Content | Writer |
|---|---|---|
| `data/bank/<section>/*.json` | Item files, each holding a JSON array of items | tools/, Codex, Claude |
| `data/bank/mocks/<mock_id>/` | Reserved full mock exams (never drawn in drills) | tools/ |
| `audio/` | MP3 files referenced by items | Alex, tools/split_audio.py |
| `materials/` | Source books and PDFs | Alex |
| `confidential/attempts.jsonl` | One line per answer | server |
| `confidential/runs.jsonl` | One line per finished run | server |
| `confidential/model_state.json` | Latest model output (recomputed from logs) | engine |
| `confidential/focus.json` | Tag boosts written by Claude's analysis | Claude |
| `confidential/analysis/YYYY-MM-DD.md` | Claude's qualitative gap analysis | Claude |

## Item
```json
{
  "id": "gr-noni-001",
  "section": "vocab | grammar | reading | listening",
  "mondai": "kanji_reading | orthography | contextual | paraphrase | usage | grammar_form | sentence_composition | text_grammar | short_passage | mid_passage | info_retrieval | task_based | key_points | verbal_expression | quick_response | instruction_phrase",
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
  "source": {"kind": "generated | book | web | official", "ref": "free text, e.g. jlptpracticetest.com/n4/3 q12"},
  "verified": true
}
```
- `answer` is 1-based. `options` always has exactly 4 entries.
- `stem` marks the underlined word with 【 】 and the ★ slot with ★.
- `passage_id` points to `data/bank/reading/passages.json` → `{"id", "text", "image"?}`; listening items use `audio: {"file": "audio/x.mp3", "start": 12.5, "end": 48.0}` (seconds).
- `tags` use prefixes: `grammar:`, `word:`, `kanji:`, `skill:` (e.g. `skill:long_vowel`), `phrase:`.
- Only items with `verified: true` are served.

## Attempt (`confidential/attempts.jsonl`)
```json
{"ts": "2026-10-30T19:02:11+01:00", "run_id": "r-20261030-190000", "item_id": "gr-noni-001",
 "choice": 1, "correct": false, "ms": 14230, "flag": "none | unclear | guess", "mode": "drill | timed | practice | mock", "timed_out": false}
```
`ms` is measured in the browser (`performance.now()`), from the moment the item is shown to the moment it is answered. For a reading passage, the time spent reading the passage goes to the first question of that passage.

## Run (`confidential/runs.jsonl`)
```json
{"run_id": "r-20261030-190000", "start": "...", "end": "...", "mode": "timed", "section": "grammar | mixed | ...",
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
