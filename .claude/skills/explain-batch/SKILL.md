---
name: explain-batch
description: Write and check wrong-answer explanations (furigana, translation, option meanings, evidence, steps) for the JLPT N4 question bank, batch after batch, until the session's quota runs low. Use when Alex says "explain batch", "write explanations", "Sunday explanations", or runs /explain-batch.
---

# Explanation batches

Anna (the learner) mostly gets questions wrong because she doesn't know the words or can't parse the whole sentence, so every question in the bank gets an explanation that she sees right after a wrong answer. You write them yourself in this session (Codex is not used here), and `tools/explain_items.py` checks them before they go live. Alex runs this on Sunday evenings to use up quota before the weekly reset. Keep going batch after batch until he stops you or the quota runs low; a half-finished batch costs nothing, because only checked entries are merged.

Read first: `tools/explain_prompt.md` (the rules for every field) and the "Explanation" section of `docs/SCHEMA.md`.

## Each batch

1. `python tools/explain_items.py status` shows progress and what is next. Questions Anna got wrong always come first.
2. `python tools/explain_items.py brief sun-YYYY-MM-DD-NN --next 25` writes `data/explain_drafts/<batch>/brief-01.json`. Use about 15 for reading, because the passages are long. The tool doesn't split a passage's questions across batches.
3. Read the brief. Copy `.claude/skills/explain-batch/draft_template.py` to the scratchpad and fill `D` with one entry per item, following `tools/explain_prompt.md`. Then run it with the output path `data/explain_drafts/<batch>/drafts-01.json`.
4. `python tools/explain_items.py check <batch>`, then read `data/explain_drafts/<batch>/report.md`:
   - **FAILED**: fix the draft and run the check again. Common causes: an evidence quote that is not copied exactly (full-width spaces `\u3000`, line breaks, or a `|` from a table row); a kanji left without furigana; sentence text that doesn't equal the stem with the answer filled in.
   - **needs a look**: the dictionary analyser or the N4 word list reads something differently. Decide which reading is right. Fix the draft if it is wrong, otherwise rerun with `--accept <id> ...`. Known false alarms: made-up kanji pairs in wrong orthography options, 開く あく/ひらく, readings of a kanji quoted on its own.
5. Steps get their furigana automatically when merged. Read them with `python tools/explain_items.py steps <batch>` and fix any wrong reading by hand in `data/explain.json`.
6. Tell Alex in one line, e.g. "batch 3: 25 merged, 412 / 1320 explained", and start the next batch.

## Rules

- Correctness comes before speed. If you are unsure of a reading, use the standard dictionary reading. Never invent facts that aren't in the passage or script.
- Don't change items. If a question looks wrong (two defensible answers, a wrong key, broken text), still explain the keyed answer honestly, e.g. "やすい: also correct Japanese, but this item wants にくい". Then add the item to `data/explain_drafts/item_problems.md` with one line on why, for Alex to decide on. If an item is broken so badly it can't be explained (options that don't belong to the stem), don't explain it: add its id to `data/explain_drafts/skip.txt` too, which keeps it out of `--next`. Changing an item means marking it `revised`, which drops Anna's earlier answers on it.
- Never point the live portal at test data and never write to `confidential/`. To try the page, use a copy under the scratchpad with `JLPT_HOME` set.
- `data/` is git-ignored, so the explanations are not committed. Commit only changes to tools or the prompt, and only when Alex asks.

## At the end

Run `status` once more and give Alex: how many items were explained this session, the overall count, what is next, and any new lines in `item_problems.md`.
