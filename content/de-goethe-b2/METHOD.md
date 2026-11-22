# de-goethe-b2 content method

How the Goethe-Zertifikat B2 content for Yoko is planned and made. Every future step adds a note here: what was done, how, with which model or prompt, what was decided, and why. Item sets will also carry a `method` field, as the de-work units do.

## 1. Content plan (2026-11-08, PLAN.md)
- **Structure check:** Claude Opus 5.5 searched the web (WebSearch, standard mode) and downloaded [S1] and [S2] from goethe.de. It extracted the text locally with pypdf and read the overview table, the task pages and the scoring sections. [S4] could not be fetched (HTTP 403). The overview table in [S1] came out jumbled; it was rebuilt from the task pages (item numbers 1–30 in Lesen and in Hören, number of options, heard once or twice).
- **Item counts:** these are statistical estimates (binomial standard error), not official figures. 120 practice items plus 60 mock items per module is a planning number, to be revisited once real error rates exist.
- **B2 word list:** no official list was found. This is reported as "not found", not as "does not exist".
- **Bridge:** Claude matched each unit's language functions to the aims of each part [S1 p. 7]. It is a judgement and has not been tested.
- **Not done:** no items, no audio and no grading prompts. The Modellsatz and Durchführungsbestimmungen PDFs were kept only in the session scratchpad and were not committed.

## 2. Rules carried over from de-work (see ../de-work/METHOD.md)
- House style: Swiss spelling (ss, never ß) applies to Yoko's own items and explanations. Exam texts copied from official or book material keep their original spelling.
- `explanation_ja` and Japanese `distractor_notes`; `source.author`, `source.batch` and `verified: false` until approval.
- Blind check by a second model (Codex, or Claude Sonnet when Codex is out of quota) before approval. For copyrighted source material, the check runs only after Alex agrees to send that material to an external model.
