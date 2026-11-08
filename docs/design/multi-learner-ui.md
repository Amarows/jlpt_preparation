# Multi-learner interface

Status: design proposal, 8 Nov 2026. Strings live in `web/i18n/strings.json`; the clickable mockup is `docs/design/mockup.html` (published privately: https://claude.ai/artifact/1oNiLmr4ezMENch9Z5LxW9).

## Ground rules

- **Anna's screens stay pixel-identical until 7 Dec 2026.** Every new rule in `style.css` is scoped to a new class or to `body:not([data-track="n4"])`. Her `en` strings are today's text, character for character.
- One look: the existing `style.css` tokens. No new colours except the four unit-state chips below, built from existing tokens.
- The interface language comes from the learner (`ui_lang`), the explanation language from the track (`explanation_lang`). Yoko: `ja` / `ja`. Anna: `en` / `en`.
- Dates use the interface language: `Intl.DateTimeFormat(ui_lang)` (`ja` → 「11月8日」), replacing `toLocaleDateString(undefined, …)`.
- `<html lang>` is set to `ui_lang`; German stems and options get `lang="de"` so phones pick a correct hyphenation and voice.

## 1. Learner picker

Shown at `/` only when there are two or more learners **and** this device has no remembered learner (`localStorage.learner`). With one learner it never appears.

- Title: `picker.title` (「どなたが学習しますか？」 / "Who is studying?"). Shown in the language of the device (`navigator.language` starts with `ja` → `ja`, else `en`), because nobody is chosen yet.
- One full-width card per learner, min-height 72 px: name (large), then `picker.learner_track` in the learner's own `ui_lang` (Anna's card in English, Yoko's in Japanese).
- Tapping a card stores the learner id and opens their home. Line under the cards: `picker.remember`.
- Later, with internet access, the picker becomes the login screen: same cards, then a password field. Nothing else changes.

## 2. Header

Left: track title (`track.<id>.title`). Right: P(pass) badge as today.

- **Non-N4 tracks**: a learner chip sits between title and badge: `header.learner` (「ヨウコさん」) with a ▾ marker; tapping it opens a small menu with one item, `header.switch`. Switching clears `localStorage.learner` and returns to the picker. Chip and menu item are at least 44 px high.
- **N4 track (Anna)**: no chip before 7 Dec, so her header does not change. Switching from her device is done by opening `/?pick` (clears the remembered learner). **Decision for Alex**, see the end.
- At ≤ 560 px the header wraps to two rows: row 1 title + chip, row 2 badge at full width, left-aligned. Today the badge is capped at 50 % width; on non-N4 tracks the cap is removed so 「目標：2027年6月30日までにB1（職場）」 does not wrap into four lines.

## 3. Yoko's home

Replaces the Mode / Section / Length form on non-N4 tracks. Order, top to bottom:

1. **Today** panel (`home.today_title`): target `home.today_target` (default: 10 questions/day), a progress bar, `home.today_left` or `home.today_done`. One primary button, full width on phone: `home.continue_unit` with the active unit's name. It starts a practice run on that unit (all its items, 5–10).
2. **Topics** list (`home.topics_title`): one row per topic unit in the order Alex/the content session defines. Each row: unit name in Japanese, German name underneath in small muted text, `home.topic_items`, a state chip, `home.topic_known` with a thin bar, and one action button whose label depends on state: not started → `home.topic_start`, learning/practised → `home.topic_practise`, done → `home.topic_review`. The whole row is the tap target.
3. **Review my mistakes** (`home.mistakes`), secondary button, hidden when the count is 0.
4. The existing report panels (P(pass) chart, latest mistakes) below; "Accuracy by section" is replaced by the topic list and hidden.

Unit states (chip colour → token):

| State | Key | Rule (proposal) | Chip |
|---|---|---|---|
| Not started | `unit.not_started` | no answers on any item of the unit | `--paper` / `--muted` |
| Learning | `unit.learning` | some answers, not every item correct yet | `--accent-soft` / `--accent` |
| Practised | `unit.practised` | every item answered correctly at least once | `--good-soft` / `--good` |
| Done | `unit.done` | every item correct on two different days, latest answer correct | `--good` / white |

`home.topic_known` counts items whose latest answer is correct. Only 1–2 units are "active" at a time: the Today button always picks the first unit in Learning, else the first Not started.

P(pass) on Yoko's badge reads `badge.p_pass` + `badge.target` instead of the 80 % band line; the band stays in the chart tooltip. What "pass" means for her (target and date) is a **decision for Alex**.

## 4. Run and result for German items

Same `run.html`, same card. Differences on non-N4 tracks:

- Stem and options are German (`lang="de"`); the stem uses `--stem-size` but capped at 1.6 rem, because German sentences are long.
- Mode is always Practice (feedback after every answer). No run clock; the per-question timer stays (it feeds the model) but is shown only as the thin bar, without seconds, so it does not pressure her.
- Feedback box: `run.correct` / `run.not_quite`, then the explanation in Japanese (item field `explanation_ja`; the server sends `explanation` in the track's `explanation_lang`), then the distractor note in Japanese. A wrong answer waits for `run.next`; a correct one flashes green and moves on after 700 ms, as today.
- Answer-note toggles (`run.unclear`, `run.guess`) stay; on phone they are 44 px high and split the row 50/50. The keyboard hints (`kbd`) are hidden on touch devices (`@media (hover: none)`).
- Result screen: `result.title`, `result.score`, `result.p_pass`, plus one line per unit that changed state (`result.unit_now`, e.g. 「不良の報告：練習済みになりました」). The four-column table becomes stacked cards at ≤ 560 px on non-N4 tracks: German question in bold, then 「あなたの回答」 and 「正解」 rows, explanation in muted text, wrong cards first with the `--bad-soft` background. Button `result.back_to_topics` at the bottom, full width.

## 5. N4-only parts

Driven by a track feature list (`track.features`), not by `if track == n4` checks spread through the code:

| Feature | N4 | German workplace |
|---|---|---|
| Mode / Section / Length form | yes | no (topic list instead) |
| Timed mode, run clock, mock exams | yes | no |
| Furigana, `【 】` underline, `★` slot | yes | no |
| Listening clip rules (stem hidden until answered, single play in timed mode) | yes | no; future listening (incl. Swiss German) allows replays and shows the question first |
| Reading passages | yes | not now; same component when needed |
| Accuracy by section | yes | no (topic progress instead) |

Hidden means not rendered, not `display:none` over loaded data.

## 6. Phone width (375 px)

- No horizontal page scroll on any screen. The only element allowed to scroll sideways is an N4 reading table inside `.passage-table`.
- Every tap target ≥ 44 × 44 px: answer buttons (already 64 px), toggles (raise `min-height` to 44 px on non-N4 tracks), learner chip, topic rows, Next, result links.
- Primary actions are full width at ≤ 560 px and sit within thumb reach: the Today button is the first control on the home screen; Next follows the feedback directly.
- Body text ≥ 16 px for Japanese explanations (Japanese at 14 px is hard to read on a phone).
- Header is not sticky; the run card's progress bar already shows position.

## Decisions for Alex

1. **Anna's switch action before 7 Dec**: (a) no visible change, switch via `/?pick` — recommended; (b) a small name chip in her header too.
2. **Yoko's P(pass)**: what target and date? Proposal: "all planned units Done by 30 Jun 2027", shown as 「目標：2027年6月30日までに全トピック習得」.
3. **Unit-state rules** in the table above (two different days for Done).
4. **Today's target** for Yoko: 10 questions a day, or one full unit run a day?
