# de-work content method

How Yoko's German work content is made. The general method is described here. What was done for each unit is in the `method` field of `topics.json` and of each `units/*.json` file. Every new unit fills the same fields: `entries`, `cefr`, `house_style`, `items`, `blind_check`, `approval`, `open`.

## 1. Topics: choice and ranking
- Input: Yoko's profile from the PO brief. She leads the method and process for powder-metal mixes in Winterthur. Her goals are work vocabulary, more correct Standard German, and understanding Swiss German.
- Each candidate unit is one work situation she meets at least weekly.
- Ranking: first the units that serve a goal she named, then the units she uses most often, then the units that need materials we do not have yet (Swiss German audio).
- Alex's limit: 1–2 units at a time, 5–10 entries each.
- Yoko confirms or reorders the units. She has not done so yet.

## 2. Entries per unit
- The words and phrases needed to act in that situation: name the problem, say what happened, compare with the limit, then propose or ask.
- Sources so far: the PO brief and Claude's knowledge of powder metallurgy. No company documents were used.
- Company documents may be used only with Yoko's OK and her employer's. They stay in the git-ignored `materials/` folder and are never sent to an external model (see `materials.json`).
- Each entry has the German form, plus article and plural for nouns and the principal parts for verbs. It also has an example sentence from her work, the Japanese and English meanings, and a CEFR level.

## 3. CEFR level
- Claude judges each level against the Goethe/telc B1 scope. Everyday words are A2 or B1. Words beyond B1 and technical words are B2.
- The levels are still to be checked against the official Goethe B1 Wortliste once Alex has it.

## 4. House style (approved by Alex, 2026-11-08)
- Swiss Standard German: always ss, never ß (Massnahme, ausserhalb, Grüsse).
- Swiss workplace words where they differ from Germany's (Sitzung, Absenz, parkieren).
- du with colleagues, Sie with the boss.
- Swiss German (dialect) appears only in listening material. Yoko is taught to answer in Standard German.

## 5. Item generation
- Claude Opus 5.5 writes each item from an approved entry. A small script adds the ids, the `source` fields, the answer position and `verified: false`.
- `source.author` is `claude-opus-5-5`. `source.batch` is `de-work/unit-<X>-v<n>`. `source.ref` is `content/de-work/units/<file>#<entry id>`.
- Mondai types:
  - Word entries get `meaning_choice` (the word is marked 【 】 in a work sentence; 4 Japanese meanings) and `cloze` (a gap (　　) in a work sentence; 4 German options in the same grammatical form).
  - Phrase entries get `phrase_choice` (a situation in German; 4 utterances) and, where a natural colleague line exists, `reply_choice` (the colleague's line and the speaker's intention; 4 replies).
- Distractor rules:
  - There is exactly one acceptable answer.
  - Every distractor is a real word or phrase from the same setting.
  - No distractor is a second meaning of the target word.
  - Grammar distractors test only frequent learner errors: the verb in second position, the verb at the end of dass/weil clauses, ob vs wenn, and sein vs haben.
  - Answer positions are spread over 1–4.
- `explanation_ja` is 1–2 sentences: the meaning, then the key collocation or rule, with German forms in Latin script. `distractor_notes` says in Japanese what each wrong option means or what error it contains.

## 6. Blind check
- A second model answers every item without the key, explanations or notes. It also flags an item if more than one option is acceptable, if no option is correct, if the German is unnatural, or if a Japanese option is mistranslated.
- The default checker is the Codex CLI: `codex exec --skip-git-repo-check -s read-only -m gpt-6-luna "<task>"`.
- If Codex is unavailable, a fresh Claude Sonnet subagent that reads only the blind file takes its place. The unit's `method.blind_check` records which model was used.
- Every disagreement or flag is either fixed or the item is dropped. Defect rate = flagged or mismatched items ÷ items.
- Units B and C: Sonnet did the check, because Codex was out of quota until 2026-11-18. 33/33 answers matched the key. One item was flagged: `dw-c-pc-ansicht`, whose distractor "Ich habe die Ansicht" was judged acceptable German. That distractor was replaced. Defect rate: 3 %.

## 7. Approval
- Alex (or Yoko) approves the unit's entry list as a plain data file. The approval is recorded in the unit file as `status`, `approved_by`, `approved_on` and `approval_note`.
- After approval, that unit's items are set to `verified: true` and the portal serves them.
- Units B and C were approved by Alex on 2026-11-08, relayed by the PO.

## Open
- Run the blind solve again with Codex after 2026-11-18, for units B and C.
- Check the CEFR levels against the Goethe B1 Wortliste.
- Yoko's review of the topics and the entry lists.
- The exam benchmark (P(pass) of a real exam at her next level, e.g. Goethe B1) is not chosen yet. Once it is, the exam's own task types, such as Lesen and Hören, need their own item set. The work units stay as practice content.
