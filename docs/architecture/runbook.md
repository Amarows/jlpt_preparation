# Runbook: put the portal online with Cloudflare Tunnel + Access

Use this runbook only after Alex has approved [online-portal.md](online-portal.md), decisions D1–D8.

Each step is marked with who does it:

- **[ALEX]** – only Alex can do this. These steps involve accounts, money, DNS or sharing data, and Claude must not do them.
- **[CLAUDE]** – a Claude session can do this on Alex's yes. These are code or local configuration changes and are reversible.
- **[CHECK]** – a pass/fail check. Stop if it fails.

Placeholders: `<domain>` is the bought domain, `<host>` is `study.<domain>`, and `<team>` is the Zero Trust team name.

## 0. Before anything is exposed

1. **[CLAUDE]** Implement hardening items H1–H10 from the ADR, each with failing-first tests, and merge them to `main`.
2. **[CHECK]** The suite is green.
3. **[CHECK]** `curl --path-as-is http://127.0.0.1:8080/audio/../confidential/attempts.jsonl` → 404.
4. **[CHECK]** `netstat -ano | findstr :8080` shows `127.0.0.1:8080` only, not `0.0.0.0`.
5. **[CLAUDE]** Add `PyJWT[crypto]` to `requirements.txt`, pinned, then install it into `.venv`.
6. **[CLAUDE]** Write `tools/backup.ps1`.
7. **[CHECK]** Run one backup, then restore it into a temporary `JLPT_HOME`. The golden snapshot of the restored copy matches the live one.

## 1. Domain and Cloudflare account

1. **[ALEX]** Create a Cloudflare account, or use an existing one. Turn on 2FA with an authenticator app or security key.
2. **[ALEX]** Get the domain (D2) onto Cloudflare, either way:
   - buy it in Cloudflare Registrar, or
   - add an existing domain and change its nameservers at the current registrar to the two Cloudflare gives. Then wait until the dashboard shows "Active".
3. **[ALEX]** Zero Trust → choose the team name `<team>` → choose the **Free** plan.
   - **[CHECK]** The plan is Free with 50 seats.
   - **[CHECK]** Read the checkout screen: if it asks for a payment method or overage consent, stop and tell Claude before accepting.

## 2. Tunnel

1. **[ALEX]** Zero Trust → Networks → Tunnels → Create a tunnel, type **Cloudflared**, name `jlpt-portal`, environment **Windows**.
2. **[ALEX]** Run the install command shown, `cloudflared.exe service install <token>`, in an **admin** PowerShell.
   - It installs `cloudflared` as a Windows service.
   - The token is a secret: don't paste it into chat, a file in the repo, or OneDrive.
3. **[CHECK]** The tunnel shows **Healthy** in the dashboard. The `cloudflared` service shows "Running" with startup type "Automatic" in `services.msc`.
4. **[ALEX]** Tunnel → Published application routes → add:
   - Hostname `<host>`
   - Service `HTTP` → `127.0.0.1:8080`
   - **Do this only after step 3.1 below is saved in the same sitting.** Until Access protects the hostname, keep the portal stopped.

## 3. Access application

1. **[ALEX]** Zero Trust → Access → Applications → Add → **Self-hosted**:
   - Name `JLPT portal`, domain `<host>`, path empty.
   - Session duration: 1 month (D4).
   - Identity provider: **One-time PIN** only.
   - Policy `learners`: Action **Allow**, Include → Emails → the D3 addresses, Alex's included.
2. **[ALEX]** Copy the app's **Application Audience (AUD) tag** and give it to Claude together with `<team>` and `<host>`. None of these three values is secret.
3. **[ALEX]** Optional, for D7: add a second self-hosted app at `<host>/healthz` with one policy, Action **Bypass**, Include **Everyone**.
4. **[ALEX]** Domain → Caching → Cache Rules → rule "no cache for portal":
   - When hostname equals `<host>`, then **Bypass cache**.
5. **[ALEX]** Domain → SSL/TLS:
   - Edge certificates: **Always Use HTTPS** on.
   - HSTS: enable, max-age 6 months, no preload.

## 4. Portal configuration and service

1. **[CLAUDE]** Create the deploy checkout `C:\portal\app` (outside OneDrive) at the release tag, with its own `.venv`.
2. **[CLAUDE]** Write `C:\portal\portal.env`, which is not in any repo:

   ```
   JLPT_HOME=<path to the OneDrive repo data folder>
   JLPT_AUTH=access
   JLPT_ACCESS_TEAM=<team>
   JLPT_ACCESS_AUD=<AUD tag>
   JLPT_ORIGIN=https://<host>
   ```

3. **[CLAUDE]** Add the emails to `learners.json`: Anna's and Yoko's under their learner rows, and Alex's under `admins`.
4. **[CHECK]** `learners.json` emails equal the Access policy emails.
5. **[ALEX]** Approve a Task Scheduler task `JLPT portal`:
   - Trigger **At startup**.
   - Run whether the user is logged on or not.
   - Action: `C:\portal\app\.venv\Scripts\pythonw.exe C:\portal\app\server.py`, start in `C:\portal\app`.
   - Restart on failure every 1 minute, 3 times.

   Claude can prepare the XML for this task. Importing it needs Alex's admin password, so Alex does it.
6. **[ALEX]** Retire the old autostart: remove `start_portal.bat` from Startup, if it is there.
7. **[ALEX]** Approve the power settings (D5), in an admin PowerShell:
   - `powercfg /change standby-timeout-ac 0`
   - `powercfg /change hibernate-timeout-ac 0`
   - Or set wake and sleep tasks for the agreed hours.

## 5. Go-live checks (all must pass)

1. **[CHECK]** In a private browser window, `https://<host>` shows the Cloudflare login page, not the portal.
2. **[CHECK]** Alex signs in with his email code and sees the learner picker as admin.
3. **[CHECK]** In a second private window, an email **not** on the list gets no code. The page still says "sent", which is expected.
4. **[CHECK]** `curl -i https://<host>/audio/<a real clip>` without a cookie returns a redirect to `<team>.cloudflareaccess.com`, not audio bytes.
5. **[CHECK]** Signed in, a listening clip plays and seeks. The response headers show `Cache-Control: private, no-store` and `cf-cache-status: BYPASS` or `DYNAMIC`.
6. **[CHECK]** On the PC, `curl -H "Cf-Access-Jwt-Assertion: x" http://127.0.0.1:8080/` returns 403. This proves the header is verified, not trusted.
7. **[CHECK]** Restart the PC. Both services come back without a login, and `https://<host>` works within 2 minutes.
8. **[CHECK]** Anna runs one practice set. Then check two things:
   - `attempts.jsonl` gains her lines under her learner folder.
   - `logs/access-*.jsonl` shows her email.

## 6. Learner onboarding

1. **[ALEX]** Send each learner the link `https://<host>` with these instructions:
   1. Enter your email.
   2. Open the code email and type the code. It expires after 10 minutes.
   3. You stay signed in for a month.
   4. If you see "This One-Time PIN has already been used", request a new code. Your mail app opened the link first.
2. **[ALEX]** Yoko: add the page to her home screen.

## 7. Routine

- **Updates.** Run `tools/deploy.ps1 <tag>`, before 07:00 or after Anna's evening session. No deploys between 2026-11-29 and 2026-12-06 except fixes Anna asks for.
- **Weekly [ALEX].** Copy the newest backup zip off the PC (D6).
- **Adding a learner [ALEX + CLAUDE].** Alex adds the email to the Access policy, and Claude adds the row to `learners.json`. Then run `tools/access_check.py`; it reports no drift.
- **Removing a learner [ALEX].**
  1. Remove the email from the Access policy.
  2. Zero Trust → Users → revoke the user's session.
  3. Claude removes the email from `learners.json`; the learner's data folder is kept unless Alex says otherwise.

## Rollback

Do these in order, and stop when the problem is gone:

1. **[ALEX]** Zero Trust → Tunnels → `jlpt-portal` → delete the published route.
   - The portal is offline from the internet within seconds.
   - Local use at `127.0.0.1:8080` keeps working.
2. **[ALEX]** `sc stop cloudflared`, to stop all tunnel traffic.
3. **[CLAUDE]** `tools/deploy.ps1 <previous tag>`.
