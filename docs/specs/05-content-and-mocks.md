# Spec 05 — More real items, two mocks, honest P(pass)

Agreed with Alex on 2026-10-31. Branch `content-and-mocks`; code in the worktree, bank changes go straight into the live `data/bank`.

## Why
P(pass) showed 99.8% on ~116 distinct items (30 official). The bank is thin outside kanji (about 150 grammar/reading items), vocab meaning questions (contextual, paraphrase, usage: 16 of 28 exam vocab questions) are almost untested, and the model has no uncertainty about how hard the real exam is compared with our items.

## Phases (in priority order)
0. **Mocks set aside.** Japan Times Best Practice Tests 2 and 3 become mocks in `data/bank/mocks/bpt2|bpt3/` (listening moved out of practice; `mock.json` lists the items Anna had already seen). Test 1 is practice.
1. **Provenance and item health.** `source.author`, `source.batch` (+ `page`, `created`, `parent_item`, `parent_attempt`) on every item. `tools/item_health.py` flags items missed more than her level predicts, the same wrong option picked repeatedly, or two Unclear flags, and compares batches.
2. **Book import.** Render the scanned PDF pages, transcribe vocab/grammar/reading of tests 1–3, take answers from the book's key, then a blind solve by a second model; disagreements are rechecked against the page.
3. **Mock mode.** Full mock in exam order, three timed parts (vocab 25 min, grammar+reading 55 min, listening ~35 min), each clip once, no feedback until the end, then section scores against the pass lines (38/120, 19/60, 90) and a full review. The mock is also training: answers count at full weight, wrong answers go to My mistakes, and the items join practice once the mock is taken. A front-page card announces Mock 1 (from 15 Nov) and Mock 2 (from 29 Nov).
4. **Model.** Remove the ±1 difficulty clip, recalibrate tier labels against book items, add exam-vs-bank difficulty uncertainty, count generated items less until item health shows they behave like book items. Repeats keep full weight.
5. **Generation.** Vocab meaning questions for the N4 words without items; a light N5 check; 3–5 items per mistake, aimed at the error type (Jev classifies). Each batch: write → blind solve by a different model → Jev check → `verify_items.py`.
6. **Daily target.** 100 questions a day on the front page, a run mix that follows the exam blueprint, repeats only for mistakes or due reviews and never within 3 days otherwise; lighter last week.
7. **More sources.** Kana-only 2012 official book (grammar, reading), the 3anet mock 2 booklet, more books from Alex.
