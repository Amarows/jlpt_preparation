# Migration: the portal moves entirely to the Pi

Status: proposed on 2026-11-08 and awaiting Alex's yes.
Context: [online-portal.md](online-portal.md). The Tailscale demo on the Pi worked on 2026-11-08.

## Target

| What | Source of truth after migration | Copy |
|---|---|---|
| Code | GitHub `main`, developed on the PC | Deployed to the Pi at a tag |
| Content: `data/bank`, `data/tracks`, `data/explain.json`, `tracks/` | PC (OneDrive), where the Content session writes it | Pushed to the Pi by `pi.py push-content` |
| Audio: `audio/`, 301 MB, 161 files | PC (OneDrive); Alex owns the originals | Pushed to the Pi `/media/jlpt/audio` once, then only changed files |
| Learner data: attempts, runs, model state, open runs, logs | **Pi** (`/app_configs/local_jlpt_portal`) | Pulled to the PC nightly, plus Home Assistant backups |
| `materials/` (845 MB) | PC | Not copied: only the import tools read it, and the portal never serves it |

The PC becomes a development machine and the backup target. Nothing on the PC serves learners any more.

Data flows in one direction per kind of data: content goes PC → Pi, learner data goes Pi → PC. Nothing is edited on both sides.

Visibility: Alex accepts that learners may reach the shared files, meaning the bank and the audio. The code still shows each learner only their own progress, and only the admin sees every learner.

## Phase 0: tooling (Developer, on `multi-learner`, before cutover)

| # | Change | Done when |
|---|---|---|
| M1 | `tools/pi.py` over SSH (key `~/.ssh/jlpt_pi_ed25519`, host `homeassistant.local`, `tar` over `ssh`). One tool, four commands: `deploy <tag>`, `push-content`, `push-audio`, `pull`. | Each command has a dry-run mode, and a test runs it against a temporary folder |
| M2 | `deploy <tag>`: builds the app folder from `git archive <tag>`, normalises text files to LF, copies it to `/local_apps/jlpt_portal`, runs `ha apps rebuild local_jlpt_portal`, waits until `ha apps info` reports `state: started`, and checks the log for the server start line. If any step fails, it redeploys the previous tag, which is kept in `/local_apps/jlpt_portal/.tag`. | A deliberately broken tag rolls back by itself |
| M3 | `push-content` copies `data/bank`, `data/tracks`, `data/explain.json` and `data/vocabulary.csv`. It **never** touches `learners/` or `learners.json`. | A test proves `learners/` on the target is unchanged |
| M4 | `push-audio` compares the file lists by name and size, and sends only new or changed files to `/media/jlpt/audio`. | A second run sends 0 files |
| M5 | `pull` copies `learners.json`, `learners/` and `logs/` from the Pi to `backup/pi/<YYYY-MM-DD>/` on the PC (git-ignored, inside OneDrive), keeping 30 days. | `tools/golden_real.py`, pointed at the pulled copy, produces Anna's snapshot |
| M6 | Speed: cache the result of `simulate()` per learner, keyed by the attempts file's size and modification time. `/api/status` currently takes 1.5 s on the Pi. | A second `/api/status` call is under 100 ms on the Pi |
| M7 | Add `backup/` to `.gitignore` and to the push gate's confidential list. | The gate rejects a commit containing `backup/` |

## Phase 1: Alex, before cutover

1. Tailscale admin console → Machines → `jlpt` → **Disable key expiry**. Then clear `ts_authkey` in the app's options.
2. Install Tailscale on the **PC** with the same account. Development checks then reach `https://jlpt.<tailnet>` from the PC as well.
3. Choose **Anna's device(s)**. Anna installs Tailscale and signs in with her Google, Apple or Microsoft account. Alex shares `jlpt` with her and reads her login name under Machines → `jlpt` → Sharing.
4. Home Assistant → Backups: schedule a daily backup that includes the JLPT portal app, kept for 14 days. Set the location to a network share on the PC. Check that no cloud location is configured that Alex did not choose.
5. Pick the cutover evening (proposed: **Tue 2026-11-10, after Anna's practice**) and tell Anna. The portal is down for about 30 minutes.

## Phase 2: cutover, one evening, about 30 minutes

| # | Who | Step | Check |
|---|---|---|---|
| C1 | Claude | `pi.py push-audio` (301 MB over the LAN, a few minutes). This can run the day before. | 161 files, sizes equal |
| C2 | Claude | `pi.py deploy <release tag>`, then `pi.py push-content` | App started, `/healthz` ok through Tailscale |
| C3 | Alex | Stop the PC portal: end `pythonw.exe`, and remove the autostart if there is one | `netstat` shows nothing on 8080 |
| C4 | Claude | Freeze the PC copy: snapshot `confidential/` → `backup/pc-final-2026-11-10/`, and run `golden_real.py` on it → `before.json` | — |
| C5 | Claude | Copy `confidential/` to the Pi as `learners/anna/`. Write the real `learners.json`: Alex as admin; Anna with her Tailscale login and `"data": "learners/anna"`; Yoko with her login if known, otherwise without. The demo data is replaced. | — |
| C6 | Claude | `pi.py pull`, then `golden_real.py` on the pulled copy → `after.json` | `before.json` and `after.json` are identical |
| C7 | Alex | Restart the app | `state: started` |
| C8 | Alex | On the phone, as admin, open Anna's page | P(pass) equals the PC's last value, and today's count is correct |
| C9 | Anna | Opens `https://jlpt.<tailnet>` on her device and answers 3 questions, including one listening question | The audio plays, and `pi.py pull` shows 3 new lines in her attempts |

If C6, C8 or C9 fails, roll back (below) and try again on another evening.

## Phase 3: the PC as development machine and backup

1. Rename `confidential/` on the PC to `confidential.migrated-2026-11-10/` and make it read-only. Delete it after the exam, and only on Alex's yes.
2. Use a Windows Task Scheduler job at 03:30 for `pi.py pull`. Before it, the Home Assistant backup at 03:00 lands on the PC share. Two independent copies then exist on the PC, and the weekly USB copy remains (D6).
3. Local development uses the test fixtures or a pulled copy, with `JLPT_HOME` pointing at a temporary folder. The PC never writes to the Pi's learner data.
4. Retire `start_portal.bat` and `start_portal.vbs`, or point them at fixture data for development. The Developer decides which and tells Alex.
5. Remove the SSH key from the Pi only if deployment moves to another method. `pi.py` needs it.

## Anna's exam (2026-12-06)

- After the cutover, deploy only in the evening, and run `pi.py pull` before each deploy.
- From 2026-11-29 to 2026-12-06 there are no deploys, except fixes Anna asks for.
- Fallback if the Pi or Tailscale fails during the exam weeks:
  1. Copy the newest `backup/pi/<date>/learners/anna/` back to `confidential/`.
  2. Start the PC portal locally.
  3. Anna practises on the PC.

  At most one day of attempts is lost. If the Pi is still reachable, nothing is lost: run `pull` first.

## Rollback during cutover

1. Stop the app on the Pi.
2. Restore `confidential/` on the PC from `backup/pc-final-2026-11-10/`. It is unchanged unless Anna practised on the Pi; in that case, `pull` first and append her new attempts.
3. Start the PC portal. Anna keeps using it until the next attempt.

## Decisions for Alex

| # | Decision | Proposal |
|---|---|---|
| G1 | Cutover evening | Tue 2026-11-10 |
| G2 | Anna's device(s) for Tailscale | Ask Anna |
| G3 | Copy the audio to the Pi | Yes. It is private study use on Alex's own device, behind Tailscale |
| G4 | `materials/` stays on the PC only | Yes |
| G5 | Delete the frozen PC copy of Anna's data after the exam | Decide after 2026-12-06 |
