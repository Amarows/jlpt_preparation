# jlpt_preparation

A small training portal for one learner preparing for JLPT N4 (2026-12-06). It runs adaptive drills and timed practice across vocabulary, grammar, reading and listening, tracks every answer, and estimates the chance of passing.

## Running

Double-click `start_portal.bat` (it starts `server.py` without a console window), then open http://localhost:8080. Set `JLPT_PORT` to use another port.

## Layout

- `server.py` — stdlib HTTP server and JSON API.
- `engine/` — question bank loading, Leitner boxes, ability model, P(pass) simulation, run selection, report.
- `web/` — plain HTML/CSS/JS front end, no build step.
- `tools/` — item generation, import (diagnostic, listening) and verification scripts.
- `docs/SCHEMA.md` — item and attempt formats; `docs/specs/` — design specs.
- `tests/` — pytest suite (`.venv\Scripts\python -m pytest tests`).

Not in git (synced through OneDrive): `data/bank/` (question bank), `audio/` and `materials/` (copyrighted source material), `confidential/` (the learner's attempts and model state).

## Legacy

`index.html`, `kanji_learn.html`, `kanji_test.html`, `parse_vocabulary.py` and `raw_data/` are the original vocabulary and kanji quiz from May 2026. `data/vocabulary.csv` is still used by `tools/gen_vocab_items.py`.
