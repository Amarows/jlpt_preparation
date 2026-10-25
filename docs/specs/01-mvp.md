# Spec 01 — Portal MVP (engine, server, runner, vocab generator, tests)

Read `docs/SCHEMA.md` first; it is binding. Context: a training portal for one learner (Anna) preparing for JLPT N4 on 2026-12-06.
Pass rule: language knowledge (vocab+grammar+reading) ≥38/120 AND listening ≥19/60 AND total ≥90/180.

## Constraints
- Python 3.13. Use **stdlib only** for server and engine, plus `numpy`. No Flask/FastAPI/SQL. Tests use `pytest`.
- Root for data = env `JLPT_HOME` (default: repo root). Never write outside `JLPT_HOME`. Tests must use a temp `JLPT_HOME`.
- Web UI: plain HTML/CSS/JS, no build step, no CDN. Put all colours/spacing in CSS variables in `web/style.css`, because a designer will restyle it later.
- Code style: small modules, type hints, short docstrings. Match the existing repo's simplicity.

## Files to create
```
engine/__init__.py
engine/paths.py      JLPT_HOME resolution, file paths
engine/bank.py       load all data/bank/**/*.json except data/bank/mocks/ and data/bank/diagnostic/*.md; validate; index by id; passages
engine/leitner.py    per-item box state derived from attempts
engine/model.py      skill ratings from attempts
engine/simulate.py   P(pass) Monte Carlo -> model_state.json
engine/select.py     adaptive run builder
server.py            HTTP server + API
web/index.html  web/run.html  web/app.js  web/style.css
tools/gen_vocab_items.py
tools/verify_items.py
tools/import_diagnostic.py
tests/test_model.py tests/test_select.py tests/test_leitner.py tests/test_server.py
start_portal.bat     runs `.venv\Scripts\python server.py` from the repo root
```

## Engine
**Leitner** (`leitner.py`): boxes 0–5, review intervals in days [0,1,2,4,7,14]. Correct and `ms <= target_ms(item)` → box+1. Correct but slow → box unchanged. Wrong, timed out or flagged `unclear` → box 0. Mastered = box ≥ 3. `target_ms` by mondai and tier, per the table below (use the upper bound of "medium" when tier is medium, etc.; hard = 2× medium):

| mondai | easy | medium |
|---|---|---|
| kanji_reading, orthography, quick_response, instruction_phrase | 10s | 20s |
| contextual, paraphrase, grammar_form | 15s | 30s |
| usage, sentence_composition, text_grammar | 30s | 60s |
| short_passage, mid_passage, info_retrieval | 60s | 120s |
| task_based, key_points, verbal_expression | 15s | 25s (measured after the audio clip ends) |

**Model** (`model.py`), Elo/Rasch-lite, replayed over all attempts in time order:
- Skills: one per section (`sec:vocab`, …) plus one per primary tag (the first tag with prefix `grammar:`, `word:`, `kanji:` or `skill:`).
- P(correct) = σ(θ_sec + θ_tag − b_item). Initial b by tier: easy −1.5, medium 0, hard +1.5; shift N5 −0.5, N4-hard +0.5.
- Update with y∈{0,1}: θ_sec += k_sec·(y−p) with k_sec = 0.3/(1+n_sec/20); θ_tag += 0.5/(1+n_tag/5)·(y−p); b_item −= 0.15·(y−p). Timed-out = wrong. A `guess` flag halves the update.
- sd per skill = 1/sqrt(1 + n/4). Section priors: θ=0.5, sd=1.0. Listening prior θ=0.4, sd=1.0.
- Speed: median `ms` per mondai over the last 50 attempts of that mondai.

**Simulation** (`simulate.py`): 10,000 draws.
- Blueprint: vocab kanji_reading 7, orthography 5, contextual 8, paraphrase 4, usage 4; grammar_form 13, sentence_composition 4, text_grammar 4; short_passage 3, mid_passage 3, info_retrieval 2; listening task_based 8, key_points 7, verbal_expression 5, quick_response 8.
- Per draw: θ_sec ~ N(mean, sd); exam item b ~ N(0.3, 1.0); p = σ(θ_sec − b).
- Time: if Σ(median_ms × count) for vocab > 25 min, or for grammar+reading > 55 min, the overflow fraction of items is answered at p=0.25. No time model for listening.
- LK = correct_lk/57·120, L = correct_l/28·60. Report p_pass, p_lk_section, p_listening_section, p_total, exp_score, band80 (10th–90th percentile of P(pass) over 20 bootstrap batches of 500), p_pass_ema (α=0.3 over runs), trend (EMA vs EMA 3 runs ago, ±0.01 → up/down/flat), mastered counts, days_left to 2026-12-06. Write `confidential/model_state.json`.

**Selection** (`select.py`) `build_run(mode, section, n)`:
- Pool = verified items in the section (`mixed` = all sections except listening when audio is missing).
- Buckets: weak (primary-tag θ below section θ, or wrong/unclear in the last 14 days, or tag boosted in `confidential/focus.json` `{"boost": {"grammar:のに": 2.0}}`), due (Leitner due today), new (never attempted), maintenance (mastered).
- Mix: 50% weak+due, 30% new, 20% maintenance. Refill from the other buckets when one is short. Weak items prefer **different items with the same tag or confusion_pair** over repeating the exact item answered in the last 24 h.
- No duplicates in a run. Reading items sharing a `passage_id` stay together and in order. Deterministic given a seed.
- `practice` and `drill` modes use the same selection; `timed` adds a time limit = Σ target_ms(medium) of the run's items.

## Server (`server.py`)
`ThreadingHTTPServer` on `0.0.0.0:8080` (env `JLPT_PORT`). Static: `/` → `web/`, `/audio/*` → `JLPT_HOME/audio`. Write all JSONL appends under one `threading.Lock`.
- `GET /api/status` → model_state.json (compute it if missing).
- `GET /api/run?mode=drill|timed|practice&section=vocab|grammar|reading|listening|mixed&n=20` → `{run_id, mode, time_limit_ms|null, items:[item without answer/explanation_en/distractor_notes], passages:{id:text}}`. Keep the run in memory.
- `POST /api/answer` `{run_id,item_id,choice|null,ms,flag,timed_out}` → append an attempt (server computes `correct`) → `{ok:true}`. In practice mode the reply also includes `answer, explanation_en, distractor_note`. Idempotent per (run_id,item_id).
- `POST /api/finish` `{run_id}` → append run line, recompute the model → `{score, total_ms, p_pass_before, p_pass_after, items:[{stem, options, choice, answer, correct, ms, slow:bool, flag, explanation_en, distractor_note}]}`.

## Web
- Every page shows a top-right badge: P(pass) as a %, a trend arrow and the 80% band in small text, plus days left. It polls `/api/status` on load and after each run.
- `index.html`: choose mode (Drill / Timed / Practice) × section (Vocabulary, Grammar, Reading, Listening, Mixed) × length (10/20/40). Show mastered count.
- `run.html?mode=..&section=..&n=..`: one item at a time; large Japanese text (font stack incl. "Noto Sans JP", "Yu Gothic", "Meiryo"). Keys **1–4** answer; key **?** or a button toggles flag `unclear`; key **G** marks `guess`. `ms` via `performance.now()` from render to answer. Passage shown above its questions. Timed mode: countdown; at 0, remaining items are sent with `choice:null, timed_out:true`. Practice mode: after answering show correct/incorrect + explanation; Enter → next. Listening: `<audio>` plays `audio.start`–`audio.end`, once in timed mode, replay allowed in practice; time starts when the clip ends.
- Queue answers in `localStorage` and retry until acknowledged; never lose an answer on a network blip.
- Summary screen: score, time, then wrong, flagged and slow items first (stem, her choice, the correct answer, explanation_en, the distractor note for her choice); others collapsed.
- Must work in Chrome on a laptop and on a narrow phone width.

## Tools
- `gen_vocab_items.py`: read `data/vocabulary.csv` (columns index,kanji,reading,romaji,type,meaning). Skip rows whose `kanji` has no kanji characters or whose reading contains `;`, `、` or `/`. Create **kanji_reading** items (stem `【<kanji>】`, options = the reading + 3 distractors) and **orthography** items (stem `【<reading>】`, options = the kanji spelling + 3 distractors). Reading distractors, in priority order: drop/add a long vowel (ゅう↔ゅ, ょう↔ょ, おう↔お, えい↔え, うう↔う), toggle dakuten/handakuten on a kana, add/remove small っ, then another vocabulary word's reading of the same length. Orthography distractors: swap one kanji for a kanji from another vocabulary word that shares a reading fragment, else a random kanji from the list. Never emit a distractor equal to any valid reading/spelling of that word in the csv. Tier easy, level N4-core (N5 if the word is in a common-N5 list you can hard-code of ~80 words), tags `word:<kanji>` and `skill:long_vowel` etc. for the rule used, explanation_en = "<kanji> = <reading> (<meaning>)". `source.kind="generated"`, `verified=true`. Write `data/bank/vocab/generated_kanji.json`. Print counts.
- `verify_items.py`: validate every bank file against SCHEMA (required fields, 4 unique options, answer 1–4, known mondai/section/tier/level, tag prefixes, audio file exists if set, passage exists if set), duplicate ids, duplicate (stem, options) sets, and no mock item id appearing in the drill pool. Non-zero exit on errors. `--fix-ids` is not needed.
- `import_diagnostic.py`: parse `data/bank/diagnostic/2026-10-25_placement_test.md` with its `_key.json` into items in `data/bank/diagnostic/placement_items.json` (mondai/level/tags from the key; explanation_en from the key's topic; verified true). Write Anna's placement answers (in `confidential/attempts/2026-10-25_placement.json`, field `answers`) as attempts with `ts` 2026-10-25T12:00:00+02:00, `run_id` `r-20261025-placement`, `ms` null, mode `diagnostic`, and flags: q9 `guess`, q20 `unclear`. Make it safe to run more than once (no duplicate lines). The engine must handle `ms: null` (ignore for speed).

## Tests (must pass with `.venv\Scripts\python -m pytest -q`)
- model: generate 2,000 synthetic attempts from a known θ per section on random items; the recovered θ is within 0.3, and P(pass) is >0.95 for a strong learner and <0.2 for a weak one.
- select: mix ratios within ±1 item for n=20; no duplicates; passages stay grouped; mock items excluded.
- leitner: box transitions and mastery.
- server: start on a random port with a temp JLPT_HOME holding a tiny bank; run → answer ×3 → finish; attempts.jsonl has 3 lines; status returns p_pass.

## Done when
Tests pass; `python tools/gen_vocab_items.py && python tools/import_diagnostic.py && python tools/verify_items.py` succeed against `JLPT_HOME`; and the server starts and serves a 10-item vocab drill. Finally, print a short report of what was built and any deviations from this spec.
