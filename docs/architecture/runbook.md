# Runbook: put the portal online (Raspberry Pi 5 + Tailscale)

This runbook implements [online-portal.md](online-portal.md) as decided on 2026-11-08:

- The portal runs on the Raspberry Pi 5 as a local Home Assistant app.
- Learners reach it through Tailscale node sharing.
- There is no domain, no static IP, and no port forwarding.

Each step is marked with who does it:

- **[ALEX]** – only Alex can do this. These steps involve accounts, secrets, sharing, or installs on the Pi, and Claude must not do them.
- **[CLAUDE]** – a Claude session can do this on Alex's yes. These are code or local file changes and are reversible.
- **[CHECK]** – a pass/fail check. Stop if it fails.

Placeholders:

- `<tailnet>` – the tailnet's DNS name, for example `tail1234.ts.net`
- `<pi>` – `homeassistant.local`

## 0. Code ready

1. **[CLAUDE]** Implement and merge the following to `main` on `multi-learner`, each with failing-first tests:
   - hardening H1–H11,
   - Pi changes P1–P7 in their Tailscale form (ADR "Changes against the Cloudflare plan"),
   - the `tailscale` backend of `who()`.
2. **[CHECK]** The full suite is green.
3. **[CHECK]** Each of these returns 404:
   - `curl --path-as-is http://127.0.0.1:8080/audio/../learners.json`
   - `curl --path-as-is http://127.0.0.1:8080/audio/../learners/anna/attempts.jsonl`
4. **[CHECK]** With `JLPT_AUTH=tailscale` and no `Tailscale-User-Login` header, every route except `/healthz` returns 403.
5. **[CHECK]** With `JLPT_AUTH=tailscale` and `JLPT_BIND=0.0.0.0`, the server refuses to start.

## 1. Tailscale account

1. **[ALEX]** Create a Tailscale account on the free Personal plan. Sign in with the identity Alex wants as admin, and turn on two-factor authentication at that provider.
2. **[ALEX]** Admin console → DNS:
   - turn on **MagicDNS**;
   - turn on **HTTPS certificates**.
   - Note `<tailnet>`.
3. **[ALEX]** Admin console → Settings → Keys → Generate auth key:
   - **not** reusable;
   - **not** ephemeral;
   - **no tags**;
   - expiry 1 day.

   Copy it. It is a secret: it goes only into the app option in step 2.6, never into chat, the repo or OneDrive.

## 2. Pi preparation

1. **[ALEX]** Home Assistant → Settings → Apps:
   - Update the apps that show an update.
   - Start **Terminal & SSH** with Alex's public SSH key. Password login stays off.
2. **[ALEX]** Settings → System → Backups. Check every location; no cloud may appear that Alex has not chosen. Add the PC network share (D10).
3. **[CLAUDE]** On the Pi through SSH, create:
   - `/media/jlpt/audio/`
   - `/addons/jlpt_portal/`
4. **[ALEX]** Copy the audio. Claude gives the command, and Alex runs it because it copies copyrighted files:

   ```bash
   scp -r audio/* root@<pi>:/media/jlpt/audio/
   ```

5. **[CLAUDE]** `tools/deploy.ps1 <tag>`, first run. It copies the app, the code, `data/bank/`, and a `learners.json` with Alex as admin and **no learner emails yet**.
6. **[ALEX]** Settings → Apps → ⋮ → Check for updates.
   - Install **JLPT portal** from Local apps.
   - Paste the auth key into the option `ts_authkey`.
   - Turn on "Start on boot" and "Watchdog".
   - Start it.
7. **[CHECK]** The app log shows `tailscale up` succeeded, then `serve` on `https://jlpt.<tailnet>`, then the server listening on `127.0.0.1:8080`. The log does not print the key.
8. **[CHECK]** The app's Info tab shows:
   - no network ports;
   - "Home Assistant API: no";
   - "Supervisor API: no".
9. **[ALEX]** Admin console → Machines → `jlpt` → ⋯ → **Disable key expiry**.
10. **[ALEX]** Clear the `ts_authkey` option. The node's state is kept in the app's `/data`.
11. **[CHECK]** Restart the app. It comes back online in the tailnet without the key.

## 3. Alex's own test

1. **[CHECK]** On Alex's phone or laptop with Tailscale on, `https://jlpt.<tailnet>` opens with a valid certificate and shows the admin learner picker.
2. **[CHECK]** On the same device with Tailscale **off**, the address does not resolve.
3. **[CHECK]** From a LAN computer without Tailscale, `http://<pi>:8080` does not answer.
4. **[CHECK]** From Alex's laptop through Tailscale, run:

   ```bash
   curl -H "Tailscale-User-Login: anna@x" https://jlpt.<tailnet>/api/status
   ```

   The access log must show Alex's own login, not `anna@x`. That proves Serve replaces a forged header.

## 4. Yoko (D11 first: is her phone personal or managed by her work?)

1. **[ALEX]** Admin console → Machines → `jlpt` → Share → create an invite link and send it to Yoko with these steps:
   1. Install **Tailscale** from the App Store or Play Store.
   2. Sign in with your Google, Apple or Microsoft account.
   3. Open the invite link and accept it.
   4. Open `https://jlpt.<tailnet>` and add it to your home screen.
   5. Tailscale has to be switched on while you practise.
2. **[ALEX]** After she accepts, read her **login name** under Machines → `jlpt` → Sharing. It may be an Apple relay address.
3. **[CLAUDE]** Add that login to Yoko's `emails` in `learners.json` on the Pi.
4. **[CHECK]** Yoko opens the portal and sees her own track. The access log shows her login.

## 5. Go-live checks

1. **[CHECK]** A listening clip plays and seeks on Yoko's or Alex's phone.
2. **[CHECK]** Restart the Pi. The app comes back, and `https://jlpt.<tailnet>` works within 3 minutes.
3. **[CHECK]** Restart the portal app during a timed run. The run continues (P7).
4. **[CHECK]** A manual backup:
   - contains the JLPT portal app;
   - reaches the PC share;
   - passes the restore test (ADR O1).

## 6. Anna's move (D9: after one clean week, by 2026-11-22, else after 2026-12-06)

1. **[ALEX]** Stop the PC portal.
2. **[CLAUDE]** Copy Anna's learner folder and her `learners.json` row to the Pi.
3. **[CHECK]** The golden snapshot of Anna's data on the Pi equals the PC's.
4. **[ALEX]** Share `jlpt` with Anna, as in step 4.1. Anna installs Tailscale on the device she practises on.
5. **[CLAUDE]** Add her login to `learners.json`.
6. **[CHECK]** Anna runs one practice set. Her `attempts.jsonl` on the Pi grows.
7. **[CLAUDE]** Keep the PC copy of Anna's data read-only for one month as the fallback.

## 7. Routine

- **Deploys:** `tools/deploy.ps1 <tag>`, before 07:00 or in the evening. No deploys between 2026-11-29 and 2026-12-06 except fixes Anna asks for.
- **Weekly [ALEX]:** copy the newest Home Assistant backup from the PC share to USB.
- **Adding a learner:** **[ALEX]** shares `jlpt` with the learner; **[CLAUDE]** adds their login to `learners.json`.
- **Removing a learner:**
  - **[ALEX]** revokes the share under Machines → `jlpt` → Sharing.
  - **[CLAUDE]** removes the login from `learners.json`. The learner's data is kept unless Alex says otherwise.

## Rollback

1. **[ALEX]** Stop the JLPT portal app, or revoke the shares. Learners lose access immediately.
2. **[CLAUDE]** `tools/deploy.ps1 <previous tag>`.
3. **[ALEX + CLAUDE]** Last resort before the exam: copy `/addon_configs/local_jlpt_portal/learners/anna/` back to the PC, and Anna practises on the PC portal locally.

## Later: a domain and Cloudflare

If Alex buys a domain, follow the Cloudflare design in the ADR:

- set `JLPT_AUTH=access` in the app;
- install the Cloudflared app;
- create the Access app.

Learners then use an email code instead of the Tailscale app.
