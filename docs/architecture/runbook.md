# Runbook: put the portal online (Raspberry Pi 5 + Cloudflare Tunnel + Access)

Use this runbook for the design in [online-portal.md](online-portal.md): origin decided on 2026-11-08, with decisions D2–D10 still open.

Each step is marked with who does it:

- **[ALEX]** – only Alex can do this. These steps involve accounts, money, DNS, secrets, or installs on the Pi, and Claude must not do them.
- **[CLAUDE]** – a Claude session can do this on Alex's yes. These are code or local file changes and are reversible.
- **[CHECK]** – a pass/fail check. Stop if it fails.

Placeholders:

- `<domain>` – the bought domain
- `<host>` – `study.<domain>`
- `<team>` – the Zero Trust team name
- `<pi>` – `homeassistant.local`

## 0. Before anything is exposed

1. **[CLAUDE]** Implement the ADR changes on `multi-learner`, each with failing-first tests, and merge them to `main`:
   - hardening H1–H11,
   - the Pi changes P1–P7.
2. **[CHECK]** The full suite is green.
3. **[CHECK]** Each of these returns 404:
   - `curl --path-as-is http://127.0.0.1:8080/audio/../learners.json`
   - `curl --path-as-is http://127.0.0.1:8080/audio/../learners/anna/attempts.jsonl`
4. **[CHECK]** With `JLPT_AUTH=access` and no header, every route except `/healthz` returns 403.

## 1. Pi preparation

1. **[ALEX]** Home Assistant → Settings → Apps:
   - Update Studio Code Server, Music Assistant and Claude Terminal Pro, which have updates waiting.
   - Start **Terminal & SSH** and add Alex's public SSH key in its configuration. Password login stays off.
2. **[ALEX]** Settings → System → Backups:
   - Check every configured backup location. **No cloud location Alex has not chosen.**
   - Add the PC network share as a location (D10).
3. **[CLAUDE]** On the Pi through SSH, create:
   - `/media/jlpt/audio/`
   - `/addons/jlpt_portal/`
4. **[ALEX]** Copy the audio from the PC to `/media/jlpt/audio/`. This is a copy of copyrighted files, so Alex runs it himself; Claude gives the command.

   ```bash
   scp -r audio/* root@<pi>:/media/jlpt/audio/
   ```

5. **[CLAUDE]** `tools/deploy.ps1 <tag>`, first run:
   - copies `deploy/ha-app/` and the code to `/addons/jlpt_portal/`;
   - copies `data/bank/` and a `learners.json` that contains **Yoko only** to `/addon_configs/local_jlpt_portal/`.
6. **[ALEX]** Settings → Apps → ⋮ → Check for updates.
   - "JLPT portal" appears under Local apps. Install it.
   - Options: `access_team=<team>`, `access_aud=` empty for now, `origin=https://<host>`.
   - Do **not** start it yet.
7. **[CHECK]** The app's Info tab shows:
   - no network ports;
   - "Home Assistant API: no";
   - "Supervisor API: no".

## 2. Domain and Cloudflare account

1. **[ALEX]** Create a Cloudflare account, or use an existing one. Turn on 2FA with an authenticator app or a security key.
2. **[ALEX]** Get the domain (D2) onto Cloudflare: buy it in Cloudflare Registrar, or move the nameservers of a domain Alex already owns. Then wait for "Active".
3. **[ALEX]** Zero Trust → choose the team name `<team>` → **Free** plan.
   - **[CHECK]** If the checkout asks for a payment method or overage consent, stop and ask Claude before accepting.

## 3. Access application (before any route exists)

1. **[ALEX]** Zero Trust → Access → Applications → Add → **Self-hosted**, with these settings:
   - Name `JLPT portal`, domain `<host>`.
   - Session 1 month (D4).
   - Identity provider: **One-time PIN** only.
   - Policy `learners`: Allow, Emails = the D3 addresses. Yoko and Alex go in now; Anna is added when she moves.
2. **[ALEX]** Copy the **AUD tag** into the portal app's option `access_aud`.
3. **[ALEX]** Optional (D7): add a second app at `<host>/healthz` with a single policy, **Bypass**, **Everyone**.
4. **[ALEX]** On the domain:
   - Caching → Cache Rules → hostname `<host>` → **Bypass cache**.
   - SSL/TLS → **Always Use HTTPS** on.
   - SSL/TLS → HSTS: 6 months, no preload.

## 4. Tunnel through the Cloudflared app

1. **[ALEX]** Zero Trust → Networks → Tunnels → Create a tunnel:
   - Type **Cloudflared**, name `jlpt-pi`, environment Docker.
   - Copy only the **token**. It is a secret: it goes into the app option and nowhere else (no chat, repo or OneDrive).
2. **[ALEX]** Home Assistant → Settings → Apps → Install app → ⋮ Repositories → add `https://github.com/brenner-tobias/ha-addons`.
3. **[ALEX]** Install **Cloudflared** and set the option `tunnel_token` to the token. Leave `external_hostname` and `additional_hosts` **empty**. Start the app.
4. **[CHECK]** The tunnel shows **Healthy** in the dashboard. The app log has no errors.
5. **[ALEX]** Start the **JLPT portal** app.
6. **[CHECK]** The portal app log shows it listening on `0.0.0.0:8080`. Its Info tab shows the hostname, expected `local-jlpt-portal`.
7. **[ALEX]** Tunnel `jlpt-pi` → Published application routes → add:
   - hostname `<host>`;
   - service `HTTP` → `local-jlpt-portal:8080`, using the hostname from step 6.

   Step 3.1 must already be saved.

## 5. Go-live checks (all must pass)

1. **[CHECK]** In a private window, `https://<host>` shows the Cloudflare login page.
2. **[CHECK]** Alex signs in with an email code and sees the admin learner picker.
3. **[CHECK]** An email not on the list receives no code.
4. **[CHECK]** `curl -i https://<host>/audio/<clip>` returns a redirect to `<team>.cloudflareaccess.com`, not audio.
5. **[CHECK]** Signed in, a clip plays and seeks, with `Cache-Control: private, no-store` and `cf-cache-status` not `HIT`.
6. **[CHECK]** From the Studio Code Server terminal on the Pi, `curl -H "Cf-Access-Jwt-Assertion: x" http://local-jlpt-portal:8080/` returns 403, which proves the JWT is verified.
7. **[CHECK]** `https://homeassistant.<domain>` and any other name do not resolve to the tunnel; only `<host>` does.
8. **[CHECK]** Restart the Pi. Both apps come back with "Start on boot" on, and `https://<host>` works within 3 minutes.
9. **[CHECK]** Restart the portal app in the middle of a timed run. The run continues afterwards (P7).
10. **[CHECK]** After a manual backup:
    - it contains the JLPT portal app;
    - it reached the PC share;
    - the restore test (ADR O1) gives the same golden snapshot.

## 6. Learner onboarding

1. **[ALEX]** Send Yoko `https://<host>` with these instructions:
   1. Enter your email.
   2. Type the code from the email. It expires after 10 minutes.
   3. You stay signed in for a month.
   4. If you see "already used", request a new code.
2. **[ALEX]** Yoko adds the page to her phone's home screen.

## 7. Anna's move (D9: after one clean week, by 2026-11-22, else after 2026-12-06)

1. **[ALEX]** Stop the PC portal.
2. **[CLAUDE]** Copy Anna's learner folder and her `learners.json` row to the Pi.
3. **[CHECK]** The golden snapshot of Anna's data on the Pi equals the one on the PC.
4. **[ALEX]** Add Anna's email to the Access policy.
5. **[CHECK]** Anna signs in and runs one practice set. Her `attempts.jsonl` on the Pi grows.
6. **[CLAUDE]** Mark the PC copy of Anna's data read-only in place. It is kept as the fallback for one month.

## 8. Routine

- **Deploys.** `tools/deploy.ps1 <tag>`, before 07:00 or in the evening. No deploys between 2026-11-29 and 2026-12-06 except fixes Anna asks for.
- **Weekly [ALEX].** Copy the newest Home Assistant backup from the PC share to USB.
- **Add a learner.** **[ALEX]** adds the email to the Access policy. **[CLAUDE]** adds the row to `learners.json` on the Pi. Then run `tools/access_check.py`; it should report no drift.
- **Remove a learner [ALEX].**
  1. Remove the email from the policy.
  2. Zero Trust → Users → revoke the user.
  3. **[CLAUDE]** removes the row from `learners.json`. The data is kept unless Alex says otherwise.

## Rollback

Do these in order, and stop when the problem is gone:

1. **[ALEX]** Delete the published route `<host>`. The portal is offline from the internet within seconds.
2. **[ALEX]** Stop the Cloudflared app.
3. **[CLAUDE]** `tools/deploy.ps1 <previous tag>`.
4. **[ALEX + CLAUDE]** Last resort before the exam: copy `/addon_configs/local_jlpt_portal/learners/anna/` back to the PC, and Anna practises on the PC portal locally.
