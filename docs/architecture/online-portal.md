# ADR: Putting the study portal online

Status: accepted 2026-11-08. Alex chose the Raspberry Pi 5 as origin; see "Origin: Raspberry Pi 5 with Home Assistant OS". Other open decisions are listed at the end of this file.
Setup steps: [runbook.md](runbook.md).

## Context

- `server.py` is a stdlib `ThreadingHTTPServer` on `0.0.0.0:8080`. It runs on Alex's Windows 11 home PC, from the repo folder inside OneDrive, started by `start_portal.bat` → `start_portal.vbs` → `pythonw server.py`.
- It has no login and no TLS. Open runs live in the in-memory dict `RUNS`, and answers are appended to JSONL under `confidential/` (per learner on branch `multi-learner`).
- `audio/` holds copyrighted listening MP3s and booklet images, for private study only. They must never be publicly reachable.
- `data/`, `confidential/`, `audio/`, `materials/` and `learners/` are git-ignored and synced by OneDrive.
- Learners:
  - Anna, JLPT N4 on 2026-12-06, mostly on a laptop or desktop.
  - Yoko, workplace German, mostly on her phone, possibly a work phone.
  - Alex is the admin. More learners may come, but always fewer than ten.

**Finding while reviewing (2026-11-08):** `GET /audio/../confidential/attempts.jsonl` returns the confidential file with status 200. I reproduced it against a throwaway server. `under_home` only checks that the path stays under `JLPT_HOME`, and `confidential/` is under `JLPT_HOME`. Since the server binds `0.0.0.0`, anyone on the home Wi-Fi can do this today. Fix H1 below closes it.

## Options

### A. Cloudflare Tunnel + Cloudflare Access (home PC as origin)

How it works: `cloudflared` on the PC opens an outbound-only connection to Cloudflare. A hostname on Alex's domain, such as `study.example.ch`, routes through the tunnel to `http://127.0.0.1:8080`. An Access application on that hostname lets in only listed emails, which sign in with a one-time code sent by email.

### B. Tailscale

- **B1. Private tailnet or node sharing.** The portal is reachable only from devices running Tailscale. Alex shares the PC node, or invites the learners to his tailnet.
- **B2. Funnel.** Tailscale publishes the service on a public `*.ts.net` URL without any authentication.

### C. Small VPS

The portal and its data move to a rented Linux server, for example Hetzner in Germany. The VPS needs its own login in front: either Cloudflare Tunnel + Access as in A, or Caddy plus an auth proxy.

### Comparison

| Criterion | A. CF Tunnel + Access | B1. Tailscale private | B2. Tailscale Funnel | C. VPS (+ CF Access) |
|---|---|---|---|---|
| Security | Strong: no open port, origin on 127.0.0.1, auth at the edge before any byte reaches the PC, no passwords stored. Cloudflare terminates TLS and sees the traffic. | Strongest: nothing public, end-to-end WireGuard. | **Fails the requirement**: public URL with no auth. The app would need its own login with stored passwords. | Like A, plus a public server Alex must patch. |
| Effort for Alex | Medium, once: domain on Cloudflare, tunnel, Access app, Windows service. About 1–2 h. | Low: install Tailscale and share the node. | Low, but writing app login is extra work. | High: server administration, deployments, data sync. |
| Effort for learners (Yoko on a phone) | Lowest: open a link, type the email, paste the code. Sessions last up to one month. No app needed. | Highest: install the Tailscale app, create an account, keep the VPN on. A work phone's MDM may forbid it. | Low | Lowest, as A |
| Cost | Free plan (up to 50 seats). One domain, about USD 10–11 a year for a .com at Cloudflare Registrar, or a .ch domain at its own price. | Free Personal plan (6 users). | Free | Roughly €4–7 a month for the server, plus the domain. |
| Uptime (the home PC sleeps) | Only while the PC is awake. | Only while the PC is awake. | Only while the PC is awake. | Always on. |
| Where confidential data and audio live | On Alex's PC; only in transit through Cloudflare. | On Alex's PC; nothing passes through a third party in plaintext. | On Alex's PC. | Copied to a rented server in a data centre. Copyrighted audio is stored on third-party infrastructure. |
| Fit with OneDrive | Unchanged: the server reads and writes the OneDrive folder, as today. | Unchanged | Unchanged | Poor: OneDrive has no Linux client, so data needs a sync or backup path back home. |

Facts checked on 2026-11-08. The pricing sources are partly secondary, so recheck when buying:

- **Cloudflare Access JWT.** The header is `Cf-Access-Jwt-Assertion`, which Cloudflare recommends over the `CF_Authorization` cookie. Tokens are RS256. Keys are published at `https://<team>.cloudflareaccess.com/cdn-cgi/access/certs`. Keys rotate every 6 weeks, and the old key stays valid for 7 more days. Validation must check signature, `aud` (the app's AUD tag) and `iss` (the team domain). Source: developers.cloudflare.com, "Validate JWTs".
- **One-time PIN.** The code is sent only to emails that the policy allows. It expires after 10 minutes and works once. Session length can be set from immediate timeout up to one month (default 24 h). Sources: Cloudflare One docs, "One-time PIN" and "Session management".
- **Zero Trust Free.** Up to 50 seats; adding more requires upgrading to a paid plan. Reports differ on whether the free checkout now asks for overage consent, so Alex should check at signup that no payment method is required. Sources: Cloudflare blog "Zero Trust for everyone" and Cloudflare Community threads.
- **Tunnel and media.** Public-hostname tunnel traffic falls under the CDN terms, which restrict serving "a disproportionate amount of large files". Video is the main target, and audio is not named. A few MP3 clips for two learners is not disproportionate, but the risk is non-zero. Source: developers.cloudflare.com, "Delivering videos with Cloudflare".
- **Tailscale.**
  - Personal plan: free, 6 users, non-commercial.
  - Node sharing and invites: available on all plans.
  - Funnel: available on all plans; serves the public internet on ports 443, 8443 and 10000 under `*.ts.net`, with no visitor authentication.
  - Source: tailscale.com, Pricing and "Funnel" KB.
- **Hetzner.** Prices rose in 2026. The smallest shared VPS (CX22/CX23 class, 2 vCPU, 4 GB) is roughly €4–5 a month according to secondary sources. Check hetzner.com before deciding.

## Decision (recommended)

**Option A: Cloudflare Tunnel + Access, with the home PC as origin bound to `127.0.0.1`. The server validates the Access JWT itself.**

Why:

- Yoko needs nothing installed.
- No port is opened on the router.
- No passwords are stored anywhere.
- The data and the copyrighted audio stay on Alex's PC.
- It costs one domain.
- Nothing about OneDrive changes.

Trade-offs accepted:

1. **Cloudflare is a man-in-the-middle by design.** It terminates TLS and sees answers and audio in transit. This is acceptable for study data; it would not be for health or financial data.
2. **Uptime equals the PC's uptime.** Mitigation: power plan "never sleep on AC" during agreed hours (see Operations). If learners hit a dead portal more than occasionally, move the origin to a VPS. `cloudflared`, Access and `who()` stay identical; only the origin host changes. This makes the decision reversible.
3. **A domain is needed, and its DNS must be on Cloudflare.**
4. **The audio is served through Cloudflare's CDN terms.** Mitigations: `Cache-Control: private, no-store` on `/audio/` (H5), and stay on low volume.

Rejected:

- **B2 (Funnel).** It is public with no auth.
- **B1 (private tailnet).** It is the right answer if Yoko cannot or will not use Cloudflare's email codes, or if Alex refuses the Cloudflare MITM. It keeps the same server changes, except that `who()` would read Tailscale identity headers from `tailscale serve` instead of the JWT.
- **C (VPS).** It is the fallback for uptime, not the start: it moves confidential data and copyrighted audio off Alex's PC and breaks the OneDrive model.

## Origin: Raspberry Pi 5 with Home Assistant OS (decided 2026-11-08)

Alex rejected two other first steps:
- **Sharing the portal through OneDrive.** Yoko would get files, not a portal: Python on a computer, nothing on her phone. It would also need a second copy of the code without Anna's folders.
- **Using the home PC as the origin.** The PC sleeps.

### The Pi as seen on 2026-11-08

- Raspberry Pi 5 with 16 GB RAM. Home Assistant uses about 5.6 GB.
- NVMe SSD of 117 GB with 83 GB free, so SD-card wear does not apply.
- Home Assistant OS 17.3, Core 2026.7.1.
- Apps running: Whisper, Piper, Music Assistant, Studio Code Server, File editor, Claude Terminal Pro. Terminal & SSH is installed but stopped.
- No external URL and no Home Assistant Cloud: nothing on it is reachable from the internet.

### Shape

Option A stays unchanged except for the origin host. Access, the JWT check in `who()` and the hardening list are the same. Two Home Assistant apps run on the Pi.

```
phone / laptop ──HTTPS──► Cloudflare Access (email code) ──► Tunnel
        ──► app "Cloudflared" (tunnel token, outbound only)
        ──► http://local-jlpt-portal:8080  (internal app network, no host port)
        ──► app "JLPT portal" (local app, Python 3.13 + numpy + PyJWT)
              /config  = JLPT_HOME  (app_config, rw): learners.json, learners/<id>/, data/bank/, logs/
              /media/jlpt/audio     (media, read-only): listening MP3s and booklet images
```

- **JLPT portal app.** A local app in `/addons/jlpt_portal`, built on the Pi from a `Dockerfile` that uses a Python 3.13 slim image for aarch64.
  - It gets no `ports:` entry, `hassio_api: false`, `homeassistant_api: false`, no `host_network`, and no maps beyond `app_config:rw` and `media:ro`.
  - Only other apps on the internal network can reach it. They include Studio Code Server and Claude Terminal Pro, which is why `who()` verifies the JWT instead of trusting the header.
  - The portal cannot reach Home Assistant's API, so a portal bug cannot touch heating or lights.
- **Cloudflared app.** Community app `brenner-tobias/ha-addons`, in `tunnel_token` mode.
  - Routes are managed in the Zero Trust dashboard, and only `<host>` → `http://local-jlpt-portal:8080` is published.
  - `external_hostname` stays empty, so Home Assistant itself is not exposed.
  - Verify the internal hostname in the portal app's info page; local apps are named `local-<slug>`.
- **Data location.**
  - `JLPT_HOME=/config` is visible to Alex through Studio Code Server and the SSH app as `/addon_configs/local_jlpt_portal`.
  - It is included in the app's Home Assistant backups.
  - Audio stays out of the app's backups; Alex keeps the originals.
- **OneDrive.** The Pi becomes the master copy of learner data. OneDrive keeps the code and the content work. A nightly copy of the Home Assistant backup to the PC is O1 below.
- **Resources.** The portal is tiny next to Whisper. `simulate()` with 10 000 draws takes well under a second on a Pi 5. 16 GB leaves ample headroom.

### Fallback

If the app packaging fights us, Alex is willing to replace Home Assistant OS with plain 64-bit Raspberry Pi OS. Home Assistant would then run in Docker, and the portal would run as a systemd service with `cloudflared` as a Debian package. Cost: Home Assistant "Container" has no Supervisor and no apps, so Whisper, Piper, Music Assistant and Studio Code Server would have to become separate containers set up by hand. Use this only if the app route fails a concrete check in the runbook.

### Rollout

Anna's exam is on 2026-12-06. Recommendation:
- **Yoko goes live on the Pi first.**
- **Anna stays on the PC portal, local only on `127.0.0.1`,** until the Pi has run one clean week. Anna moves no later than 2026-11-22. If any check fails, she moves after the exam.
- Learner data is separate per learner, so the two portals never write the same file.

### Developer changes this needs (branch `multi-learner`)

| # | Change |
|---|---|
| P1 | `paths.AUDIO` from env `JLPT_AUDIO`, default `HOME/"audio"`, resolved. `/audio/` serves only under it. The Pi keeps audio in `/media/jlpt/audio`, outside `JLPT_HOME`. The traversal fix in `35ee427` must hold against the new root: golden case `/audio/../learners.json` → 404. |
| P2 | Bind address from env `JLPT_BIND`: `0.0.0.0` inside the container, `127.0.0.1` everywhere else. This replaces H2's "tests only" wording. |
| P3 | Split dependencies: `requirements-server.txt` with numpy and `PyJWT[crypto]`, pinned. `requirements.txt` keeps the tools (fugashi, unidic-lite, pytest, PyYAML) and includes the server file. The image installs only the server file. |
| P4 | `deploy/ha-app/`: `config.yaml`, `Dockerfile` and `run.sh` for the local app, as described above. `run.sh` exports `JLPT_HOME=/config`, `JLPT_AUDIO=/media/jlpt/audio`, `JLPT_BIND=0.0.0.0` and the Access settings, which come from app options. |
| P5 | `GET /healthz` → `ok`, with no identity required and nothing else on that route. |
| P6 | Logs go to `JLPT_HOME/logs/` (O4). Unhandled errors also go to stdout, so they appear in the app's log tab. |
| P7 | H11 (persisted open runs) moves up to **must**. Home Assistant restarts apps on updates and backups, which would lose a timed run in progress. |

## Identity: `who(handler)` under option A

### Verify the JWT, not just trust the header

Trusting `Cf-Access-Jwt-Assertion` or `Cf-Access-Authenticated-User-Email` unchecked is safe only while every route to the origin passes Access. That fails silently in two cases:

- the bind address goes back to `0.0.0.0`, which is the current code, or
- a tunnel hostname is added without an Access policy.

In either case anyone could send the header. Verification costs about 30 lines, so `who()` verifies.

### Algorithm

1. Read the `Cf-Access-Jwt-Assertion` header. If it is missing, return `None`.
2. Decode the header and take `kid`. Look up the key in a JWKS cache from `https://<team>.cloudflareaccess.com/cdn-cgi/access/certs`, refreshed every hour and immediately on an unknown `kid`. That covers the 6-week rotation.
3. Verify RS256 with leeway 60 s: `aud` must contain `JLPT_ACCESS_AUD`, `iss` must equal `https://<team>.cloudflareaccess.com`, and `exp`, `nbf` and `iat` are checked.
4. Take `email`, lowercased. Look it up in `learners.json`. Unknown email → `None`.
5. Any request without an identity gets 403. The page says only "Not registered for this portal – ask Alex", with no detail.

### Dependency

`PyJWT[crypto]`, which pulls in `cryptography`. Pin both in `requirements.txt` at the versions current on install day. `jwt.PyJWKClient(certs_url, cache_keys=True, lifespan=3600)` does steps 2 and 3.

A stdlib-only RS256 check is possible in about 20 lines: `pow(sig, e, n)` plus a comparison against the PKCS#1 v1.5 encoding. It is rejected: hand-written signature checks are where auth bugs live, and the dependency is small and widely audited.

### Configuration

- Environment variables, set in `start_portal.vbs` or a git-ignored `portal.env`:
  - `JLPT_AUTH=access|local`
  - `JLPT_ACCESS_TEAM` (the team name)
  - `JLPT_ACCESS_AUD` (the AUD tag)
- Neither the team name nor the AUD tag is secret. There are no secrets on the PC at all; the tunnel token is held by the `cloudflared` service.
- `JLPT_AUTH=local` keeps today's cookie learner picker. It is only allowed when the server binds `127.0.0.1` and `JLPT_AUTH` is not `access`, so tests and offline use still work.
- At startup, `JLPT_AUTH=access` without team or AUD refuses to start.

### `learners.json`

The file is in `JLPT_HOME` and synced by OneDrive. It must be git-ignored (H9) because it now holds emails.

```json
{
  "admins": ["alex@…"],
  "learners": [
    {"id": "anna", "name": "Anna", "track": "jlpt-n4", "emails": ["anna@…"]},
    {"id": "yoko", "name": "Yoko", "track": "de-work", "ui": "de", "emails": ["yoko@…"]}
  ]
}
```

- `who()` returns `{"email", "learner_id", "admin"}`.
- A learner's email maps to exactly one learner. Startup rejects an email listed twice.
- An admin email may also be a learner's email.
- An admin who is not a learner gets the learner picker, today's local cookie, and can act as any learner. Every request an admin makes as someone else is logged with the admin's email (O4).
- The same email list is the **Access policy**: "Emails: anna@…, yoko@…, alex@…". The one fact lives in two places, because Access must stop strangers before they reach the PC. Mitigation: `tools/access_check.py` (should, S5) compares the Access policy emails with `learners.json` through the Cloudflare API with a read-only token. It reports drift and changes nothing.

The Developer session owns `who()` on `multi-learner`. This section is its spec. Golden cases to add:

| Input | Expected `who()` |
|---|---|
| Valid JWT, email in `learners.json` | `{"email": "anna@…", "learner_id": "anna", "admin": false}` |
| Valid JWT, admin email | `{"email": "alex@…", "learner_id": null, "admin": true}` |
| Valid JWT, unknown email | `None` |
| Wrong `aud` or wrong `iss` | `None` |
| Expired token | `None` |
| Bad signature | `None` |
| Header missing | `None` |

## Server hardening

Priority: **M** = must before going online · **S** = should, within weeks · **L** = later.

| # | Pri | Issue (location) | Concrete change |
|---|---|---|---|
| H1 | **M** | Path traversal in `/audio/` (`server.py`, `elif u.path.startswith("/audio/")`). `under_home` allows anything under `JLPT_HOME`, so `/audio/../confidential/…`, `learners.json` and `.venv/` are all readable. Reproduced. | Resolve against `HOME/"audio"` and require `AUDIO in path.parents`. Apply `unquote` before resolving, as `/web/` does. Return 404, not an exception. Add golden cases: `/audio/../confidential/attempts.jsonl` → 404, `/audio/%2e%2e/…` → 404, a real clip → 200. |
| H2 | **M** | Bind address `0.0.0.0` (`serve()`). | Default to `127.0.0.1`. Allow `JLPT_BIND` only for tests. |
| H3 | **M** | No authentication. | `who()` as specified above, on every route, including `/web/` and `/audio/`. Fail closed with 403. |
| H4 | **M** | `RUNS` is not bound to a learner. Anyone holding a `run_id` can answer or finish another learner's run. | Store `learner_id` in the run. `/api/answer` and `/api/finish` return 404 when `run["learner_id"] != who().learner_id`. |
| H5 | **M** | Copyrighted audio could be cached by the Cloudflare edge: MP3 is a default-cached extension. API JSON is cacheable too. | `Cache-Control: private, no-store` on `/audio/` and `/api/`. Also add the Cloudflare Cache Rule "bypass cache for the hostname" (runbook step). |
| H6 | **M** | Unbounded request body (`body()`): `Content-Length` is trusted, so a large value allocates and blocks a thread. | Reject `Content-Length` above 64 KB with 413. Reject a missing or non-integer value with 400. |
| H7 | **M** | CSRF on POST. Today's local cookie and Access's `CF_Authorization` cookie ride on cross-site requests, and `body()` parses any content type, so a `text/plain` form can post JSON. | Require `Content-Type: application/json`. Require `Origin` to equal the portal origin (configured `JLPT_ORIGIN`) when it is present. Reject both failures with 403. No token is needed: a JSON content type forces a CORS preflight, which the server never answers. |
| H8 | **M** | Malformed input crashes the handler thread: `int(q["n"])` in `/api/run`, and `int()` in `Range` parsing. The client gets a dropped connection, and the traceback goes to stderr (dropped under `pythonw`). | Parse with fallbacks and return 400 or 416. A top-level `try` in `do_GET`/`do_POST` returns `{"error": "server error", "id": <short id>}` with 500 and logs the traceback with that id (O4). No exception text in responses. |
| H9 | **M** | `learners.json` and `learners/` are not in `.gitignore` on `multi-learner`; only the pre-push gate covers them. | Add both to `.gitignore`. |
| H10 | **M** | Cookie flags for the local learner cookie, if it stays in `local` mode. | `HttpOnly; SameSite=Lax; Path=/`, plus `Secure` when `JLPT_AUTH=access`. Under Access the cookie does not decide identity: `who()` ignores it except for an admin's chosen learner. |
| H11 | S | In-memory `RUNS` is lost on restart, which loses a mid-run timed test. Answers already survive in `attempts.jsonl`. | On `/api/run`, write the run to `<learner>/open_runs/<rid>.json`. Delete it on `/api/finish`. Load files younger than 24 h at startup, and drop older ones on startup. This also caps memory: H12. |
| H12 | S | `GET /api/run` creates state on every call, with no cap, and GET has side effects. `GET /api/status` also writes `model_state.json`. | Cap at 5 open runs per learner (oldest evicted). Leave the method change for later (L3); it is safe behind Access + H7. |
| H13 | S | Security headers are missing. | `X-Content-Type-Options: nosniff`, `Referrer-Policy: same-origin`, `X-Frame-Options: DENY`, and a CSP of `default-src 'self'; media-src 'self'; img-src 'self' data:` (to be checked against `web/`). HSTS is set at Cloudflare. |
| H14 | S | Audio is served with `read_bytes()`, loading the whole file per Range request. | Seek and read only `first..last`. |
| H15 | L | Rate limits. Access lets only about 3 authenticated people through, and Cloudflare absorbs the rest. Not needed now. | Revisit only for a public page or more than 10 learners. |
| L3 | L | `/api/run` and `/api/status` use GET but change state. | Move them to POST when the frontend is next reworked. |

Every M item ships with a failing-first test in `tests/test_server.py` or golden cases. The Developer session implements them on its branch, one intent per change: H1+H2 together (exposure), H3+H4+H10 (identity), H5–H8 (requests), H9 (repo).

## Operations

### O1. Backups beyond OneDrive

OneDrive is sync, not backup. A corrupted `attempts.jsonl` or a deletion syncs everywhere within seconds, and version history is limited.

- **Daily.** A Windows Task Scheduler job at 03:00 zips `confidential/`, `learners/` and `learners.json` into `D:\portal-backup\YYYY-MM-DD.zip`, or any folder **outside OneDrive** on another physical disk. It keeps 30 dailies and 12 monthlies. The script is `tools/backup.ps1`, and it is tested by restoring into a temporary `JLPT_HOME` and running the golden snapshot tool (`tools/golden_real.py`) on it.
- **Weekly.** Alex copies the latest zip to a USB stick, or turns on encrypted off-site storage. This is decision D6.
- The audio is not backed up by this job: Alex has the original MP3s.

### O1 on the Pi (replaces the PC job above for learner data)

- Home Assistant → Settings → System → Backups. A daily automatic backup that includes the JLPT portal app; keep 14.
- Backup location: a network share on Alex's PC, outside OneDrive. The weekly USB copy stays as above.
- **Check before turning this on:** confirm no backup location points to a cloud Alex has not chosen, such as Home Assistant Cloud or Google Drive. These backups contain learner data.
- Restore test: unpack one backup on the PC and run `tools/golden_real.py` with `JLPT_HOME` set to the unpacked `/config`.

### O2. Keeping the PC awake

This no longer applies: the Pi runs all the time. It is kept only for the fallback of running from the PC.

Measure the PC's idle draw with a smart plug before deciding.

- Power plan, plugged in:
  - Sleep never: `powercfg /change standby-timeout-ac 0`.
  - Hibernate never: `powercfg /change hibernate-timeout-ac 0`.
  - The display may sleep.
  - "Allow wake timers: enabled".
- `cloudflared` and the portal run as services (runbook), so they start at boot without a login. That also covers Windows Update reboots.
- Rough cost: a desktop idles at 30–60 W, about 260–520 kWh a year, about CHF 80–160 a year at 0.30 CHF/kWh. A €5-a-month VPS is about €60 a year. **So a VPS is cheaper than an always-on desktop.** The case for staying home is data location and simplicity, not money.
- If Alex will not leave the PC on, agree on hours instead, e.g. 06:00–23:00. Schedule a wake at 06:00 and sleep at 23:00. Tell the learners these hours.

### O3. Updating without breaking Anna before 2026-12-06

On the Pi, `tools/deploy.ps1 <tag>` does the following:

1. Runs the tests on the PC.
2. Copies `deploy/ha-app/` and the code at the tag to `/addons/jlpt_portal` through the SSH app.
3. Copies `data/bank/` to `/addon_configs/local_jlpt_portal/data/bank/`.
4. Runs `ha apps rebuild local_jlpt_portal`; on older releases the command is `ha addons rebuild`.
5. Polls `/healthz`.
6. On failure, it redeploys the previous tag.

The PC-only procedure below stays valid for the fallback.

- The PC runs a **separate deploy checkout**, e.g. `C:\portal\app`, on a tag. The service never runs from the OneDrive working copy that sessions edit. Data stays in OneDrive through `JLPT_HOME`.
- Update procedure: `tools/deploy.ps1 <tag>`.
  1. Fetch the tag.
  2. Run the tests against the golden cases on a copy of the data.
  3. Stop the service, check out the tag, start the service.
  4. Smoke check: `/api/status` returns 200 for Anna's identity through a local header, in test mode only.
  5. On failure, return to the previous tag automatically.
- **Freeze from 2026-11-29 to 2026-12-06.** Only fixes for something Anna reports as broken.
- Deploy only when Anna is not practising: before 07:00 or after an evening session.

### O4. Logging and monitoring for a small portal

- **Access log.** One JSONL line per request to `logs/access-YYYY-MM.jsonl`: `ts`, `email`, `as_learner`, `method`, `path` (no query string, no body), `status`, `ms`. The log rolls monthly; keep 6 months. Status 500 lines include the error id; the traceback goes to `logs/errors.log`.
- **Cloudflare Access logs.** Logins appear in the Zero Trust dashboard; the free plan keeps them for 24 h. They are enough to see "Yoko could not log in today".
- **Monitoring.** A free external uptime check (UptimeRobot or Healthchecks.io) on `https://<host>/healthz`, the only route that Access bypasses. It returns `ok` and nothing else, and the check emails Alex if the portal is down for more than 10 minutes during agreed hours. This is optional; decision D7.
- No dashboards, no metrics stack.

## Decisions Alex needs to make

| # | Decision | Recommendation | Cost |
|---|---|---|---|
| D1 | Hosting | **Decided 2026-11-08:** Cloudflare Tunnel + Access, with the Raspberry Pi 5 running Home Assistant OS as origin | Free plan, a few watts |
| D9 | Rollout order | Yoko on the Pi first; Anna after one clean week, by 2026-11-22 at the latest, otherwise after the exam | — |
| D10 | Home Assistant backup location | A network share on the PC, not a cloud | — |
| D2 | Domain: buy a new one, or use one Alex already owns (its DNS must move to Cloudflare) | A cheap new domain at Cloudflare Registrar, used only for this | About USD 10–11 a year (.com) |
| D3 | Learners' login emails: Anna, Yoko, and Alex's admin email | Personal addresses they can read on their phones | — |
| D4 | Session length | 30 days, so Yoko types a code about once a month | — |
| D5 | PC availability | No longer needed: the Pi is always on | — |
| D6 | Off-site backup target | A USB stick weekly, or encrypted cloud | — |
| D7 | External uptime check | Yes, free tier | Free |
| D8 | New Python dependency `PyJWT[crypto]` | Yes | — |
