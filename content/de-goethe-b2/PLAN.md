# Goethe-Zertifikat B2 – content plan for Yoko

Target chosen by Alex on 2026-11-08: Goethe-Zertifikat B2 (adult version). The exam date and test centre are still open. This is a plan only; no items have been written yet.

## Sources (checked 2026-11-08)
- [S1] Goethe-Institut, *Goethe-Zertifikat B2 – Modellsatz Erwachsene*, 2nd edition, August 2025 (document version Vs1.5_160426). https://www.goethe.de/pro/relaunch/prf/materialien/B2/b2_modellsatz_erwachsene.pdf. Foreword p. 6, overview table p. 7, task pages pp. 8–27, rating criteria and Leistungsbeispiele pp. 47–50. It states that it matches the real exam in task types, number of items and timings.
- [S2] Goethe-Institut, *Goethe-Zertifikat B2 – Durchführungsbestimmungen*, version of 1 September 2023. https://www.goethe.de/resources/files/pdf325/durchfuehrungsbestimmungen_b2-v1.pdf. Scoring is in § 4.1–4.4, the pass rule in § 6.3.
- [S3] Goethe-Institut, *Prüfungsziele und Testbeschreibung B2*. https://www.goethe.de/pro/relaunch/prf/de/Pruefungsziele_Testbeschreibung_B2.pdf. Cited for the exam's aims; not read in full.
- [S4] Goethe-Institut, *Prüfungstraining Goethe-Zertifikat B2*, with the free practice materials. https://www.goethe.de/de/spr/prf/ueb/pb2.html. The page returned HTTP 403 to the fetch tool; the link comes from search results.

## Exam rules that drive the model
- There are four modules: Lesen, Hören, Schreiben and Sprechen. Each can be taken on its own or all four together [S1 p. 6].
- Each module is scored out of 100 points and is passed at 60 or more [S1 p. 6; S2 § 6.3]. Grades: 90–100 sehr gut, 80–89 gut, 70–79 befriedigend, 60–69 ausreichend [S2 § 6.2].
- Lesen and Hören each have 30 items scored 1 or 0. The raw score is multiplied by 3.33 and rounded, so 18/30 = 60 is the pass mark [S2 § 4.1, § 4.2].
- Schreiben and Sprechen are each scored by two raters, out of 100, using the average of the two. A third rater decides borderline cases [S2 § 4.3, § 4.4].
- P(pass) is therefore computed **per module**, the way the N4 track computes it per section. Because modules can be retaken separately, the dashboard should show four P(pass) values, not one combined value.

## Modules and task types [S1 p. 7 and task pages]

### Lesen – 65 min, 30 items
| Part | Task | Items | Answer format | Suggested time | Portal? |
|---|---|---|---|---|---|
| L1 | Forum posts by 4 people: "Who says / thinks …?" A person can be the answer more than once. | 9 | 4 options (a–d), shared by all items | 18 min | yes: 4-option item tied to a passage |
| L2 | A magazine article with 6 gaps; choose the sentence for each gap from 8 (2 are not used). | 6 | 8 options shared by the set | 12 min | yes, needs an 8-option set item |
| L3 | A longer article, multiple choice | 6 | 3 options a/b/c | 12 min | yes: 3-option item |
| L4 | 8 short opinion statements (a–h; a is the example) matched to 6 headlines; one statement is left over | 6 | 7 options shared by the set | 12 min | yes, needs a set item |
| L5 | Regulations or instructions: match headings to 3 paragraphs; 4 headings are not used | 3 | 7 options shared by the set | 6 min | yes, needs a set item |

### Hören – about 40 min, 30 items
| Part | Task | Items | Answer format | Heard | Portal? |
|---|---|---|---|---|---|
| H1 | 5 short everyday conversations or statements, 2 tasks each | 10 | 1 richtig/falsch + 1 three-option MC per text | once | yes: 2-option and 3-option items with audio |
| H2 | Radio interview with an expert | 6 | 3 options a/b/c | twice | yes: 3-option item with audio |
| H3 | Radio discussion with several people: "Who says this?" | 6 | 3 speakers (moderator plus 2 guests) | once | yes: 3-option item with audio |
| H4 | Short lecture | 8 | 3 options a/b/c | twice | yes: 3-option item with audio |

### Schreiben – 75 min, graded later by Claude
| Part | Task | Length | Time |
|---|---|---|---|
| S1 | Forum post giving an opinion: take a position, give reasons, make suggestions, discuss pros and cons; needs an introduction and a conclusion | about 150 words | 50 min |
| S2 | Message to a superior or an institution: explain, describe, propose, ask politely; needs a greeting and sign-off | about 100 words | 25 min |

The criteria are how fully the content points are covered, correctness, and cohesion [S1 p. 25].

### Sprechen – about 15 min, paired exam, graded later by Claude
| Part | Task | Time |
|---|---|---|
| Sp1 | Short presentation on one of two topics, then answering the partner's questions | about 4 min per candidate |
| Sp2 | Discussion of a controversial question: exchange positions and arguments, reach a conclusion | about 5 min in total |

Preparation time is 15 minutes, and notes are allowed [S1 p. 26].

## How many items are needed

1. **Lesen and Hören.**
   - A single 30-item mock measures the score with a standard error of about ±2.6 raw points, which is about ±9 exam points. One mock is therefore not enough for a reliable P(pass).
   - To estimate accuracy per module to within ±0.05 at the pass level (p ≈ 0.6–0.7), she needs about 90–100 answered items per module.
   - Plan per module: **4 practice sets of the full module (120 items)** plus **2 sets kept back as full mocks (60 items)**.
   - Lesen: 4 × (L1 + L2 + L3 + L4 + L5) = 20 passage sets, 120 items.
   - Hören: 4 × (H1 + H2 + H3 + H4) = 16 audio sets, 120 items.
   - The engine's prior and tier calibration can reuse the N4 approach, with section = module and mondai = part.
2. **Matching parts (L1, L2, L4, L5, H3)** share one option pool, so their items are not independent. A wrong match often costs two items. The engine should treat each set as a unit for selection, and its variance is somewhat larger than for independent items.
3. **Schreiben.**
   - Aim for 6 graded texts (3 × S1, 3 × S2) before the first estimate, then one per week.
   - P(pass) comes from Claude's score on the official criteria, with the rater's spread included.
   - Calibrate first against [S1] pp. 47–50: the official rating criteria and the Leistungsbeispiele (authentic B2 learner texts). The extracted text does not show official scores for those samples, so scored samples must also come from a practice book that publishes rated answers. Claude must reproduce the published scores within ±5 points; those samples become the golden cases.
4. **Sprechen.**
   - Aim for 4 recorded attempts at Sp1 and 4 at Sp2.
   - Grading needs a recording, a transcript (speech-to-text) and Claude's score on the criteria.
   - Calibrate first on scored speaking samples, either official Goethe videos or a practice book with rated answers.
   - This is the last module to build.
5. **Order of work:** Lesen first (text only, no audio needed), then Hören (needs audio, see Materials), then Schreiben grading, then Sprechen.

### Developer needs (for the PO)
- Option counts of 2, 3, 4, 7 and 8 per mondai. The N4 rule fixes most mondai at 4 options.
- Set items: one passage or audio clip, a shared option pool, and several gaps or statements.
- Audio with "heard once" or "heard twice" playback.
- Modules scored separately, with P(pass) per module.
- A text and audio input path for Schreiben and Sprechen later.
- Suggested mondai ids: `lesen_1` … `lesen_5`, `hoeren_1` … `hoeren_4`, `schreiben_1`, `schreiben_2`, `sprechen_1`, `sprechen_2`.

## Materials for Alex
| What | Licence / handling | What it unlocks |
|---|---|---|
| Official Modellsatz Erwachsene, PDF and audio MP3s [S1, S4] | Free download from goethe.de, but **copyrighted**: private use only. Keep it in `materials/` (git-ignored), never commit it, never publish it. | 1 full mock (Lesen, Hören, Schreiben, Sprechen); the rating criteria and Leistungsbeispiele as the starting point for Claude's grading |
| Official Modellsatz Jugendliche plus the online Übungssatz [S4] | Same as above | A second full mock; the format is the same, only the topics are for teenagers |
| Durchführungsbestimmungen [S2], Prüfungsziele [S3] | Free official documents; cite them by link, do not commit them | Scoring rules (already used above) |
| 1–2 published practice books with audio, current edition (for example from Hueber, Klett or Cornelsen, titles like "Goethe-Zertifikat B2 – Prüfungstraining" or "Mit Erfolg zum Goethe-Zertifikat B2") | **Copyrighted**, bought copy, private use only. Scanned pages and audio go to `materials/`. Items made from them stay in the git-ignored bank and are tagged `source.kind: "book"`. | 4–8 more full sets, which covers most of the practice-bank target without writing everything ourselves |
| B2 word list | **I found no official Goethe B2 Wortliste.** Goethe publishes word lists for A1–B1; search results for "B2 Wortliste" were unofficial pages. Substitute: *Profile Deutsch* (Klett-Langenscheidt, commercial, lists words per level up to C2) or a B2 vocabulary trainer from one of the publishers. | B2 level checks for her work units; vocabulary drills beyond the exam tasks |
| Her answers to Schreiben tasks and recordings for Sprechen | Yoko's own data: stays in `confidential/` | Schreiben and Sprechen P(pass) |
| Exam date and test centre | Alex and Yoko decide. There is no Goethe-Institut in Switzerland; the exam is offered by licensed partner centres. | Days left and pacing |

**Rule for copyrighted material:** it must never go into git. Before any of it is sent to an external model (Codex blind solve, Jev), Alex has to decide whether that is allowed. Until he does, items made from book or Modellsatz material are checked locally by Claude only. Items we write ourselves are not affected by this rule.

**Hören audio for our own items:** B2 Hören is Standard German. For the practice sets we write ourselves, the options are text-to-speech with two or more distinct voices, or Alex recording them. Alex chooses; text-to-speech needs a service, so it is a gated decision.

## Bridge: work units A–G → B2
The work units stay practice content and do not count towards the B2 P(pass). Many of their phrases also serve the exam:

| Unit | Serves | Why |
|---|---|---|
| C – opinion in a meeting | Sprechen Sp2, Schreiben S1, Lesen L1/L4, Hören H3 | B2 opinion language is the same: Meiner Meinung nach, Ich bin der Ansicht, Da bin ich anderer Meinung, Bedenken, einverstanden. L1, L4 and H3 test who holds which opinion. |
| D – proposing a QA improvement | Schreiben S2 and S1 ("etwas vorschlagen"), Sprechen Sp2 | The Modellsatz S2 task is a message to a superior at a company that proposes something [S1 p. 25]. Massnahme, sinnvoll, wir könnten. |
| G – everyday work | Schreiben S2, Hören H1 | Moving an appointment, asking politely, greetings and sign-offs, short everyday conversations |
| B – reporting a problem | Hören H2/H4, Lesen L3 | Cause-and-effect words that run through B2 science interviews and lectures: Ursache, auftreten, Schwankung, Abweichung, festgestellt |
| A, F – mixing, pressing, sintering | Sprechen Sp1 (only if she may choose a technical angle) | Specialist words are rarely tested; their value is mainly for her job |
| E – Swiss German | not tested | B2 Hören is Standard German; the value is for her job only |

Suggested order if the exam has priority: C, D and G before A, F and E. Alex decides.

## Method notes
See [METHOD.md](METHOD.md).

## Open
- Exam date and test centre.
- Alex's decisions: which practice books to buy; whether copyrighted material may go to external models; how to make Hören audio for our own items.
- The Developer's set items, option counts and per-module P(pass) (see Developer needs).
- Calibrating Claude's grading against scored samples before any Schreiben or Sprechen P(pass) is computed. Whether Goethe publishes scores for its Leistungsbeispiele is still to be checked.
