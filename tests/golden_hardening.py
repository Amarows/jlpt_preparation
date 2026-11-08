import http.client
import json
import os
import threading
from contextlib import contextmanager
from http.server import ThreadingHTTPServer

from tests.golden_learners import two_learners

HEADERS = ("Cache-Control", "Content-Type", "Content-Range", "Set-Cookie")


@contextmanager
def env(**values):
    saved = {k: os.environ.get(k) for k in values}
    os.environ.update({k: v for k, v in values.items() if v is not None})
    for k, v in values.items():
        if v is None:
            os.environ.pop(k, None)
    try:
        yield
    finally:
        for k, v in saved.items():
            if v is None:
                os.environ.pop(k, None)
            else:
                os.environ[k] = v


@contextmanager
def server():
    import server as portal
    portal.BANKS.clear()
    portal.RUNS.clear()
    srv = ThreadingHTTPServer(("127.0.0.1", 0), portal.Handler)
    threading.Thread(target=srv.serve_forever, daemon=True).start()
    try:
        yield srv.server_port
    finally:
        srv.shutdown()
        srv.server_close()


def _call(port, method, path, body=None, headers=None, learner=None):
    c = http.client.HTTPConnection("127.0.0.1", port, timeout=10)
    hs = {**({"Cookie": f"learner={learner}"} if learner else {}), **(headers or {})}
    c.putrequest(method, path, skip_accept_encoding=True)
    for k, v in hs.items():
        c.putheader(k, v)
    c.endheaders(body)
    r = c.getresponse()
    raw = r.read()
    kind = r.getheader("Content-Type") or ""
    content = json.loads(raw) if kind.startswith("application/json") else raw.decode("utf-8") if kind.startswith("text/plain") else {"bytes": len(raw)}
    if isinstance(content, dict) and "id" in content:
        content = {**content, "id": "<random>"}
    c.close()
    return {"request": f"{method} {path}", "sent": {k: v.replace(str(port), "<port>") for k, v in (headers or {}).items()}, "as": learner, "status": r.status,
            "headers": {k: r.getheader(k) for k in HEADERS if r.getheader(k)}, "body": content}


def _post(port, path, obj, learner=None, **headers):
    raw = json.dumps(obj).encode()
    return _call(port, "POST", path, raw, {"Content-Type": "application/json", "Content-Length": str(len(raw)), **headers}, learner)


def api():
    import server as portal
    log = []
    with two_learners() as home, env(JLPT_AUDIO=None, JLPT_ORIGIN=None, JLPT_AUTH=None), server() as port:
        get = lambda path, learner="yoko", **h: log.append(_call(port, "GET", path, None, h, learner))
        get("/healthz", None)
        get("/api/me", None)
        get("/api/me")
        get("/web/index.html", None)
        get("/audio/clip.mp3")
        for path in ("/audio/../learners.json", "/audio/%2e%2e/learners.json", "/audio/..%2flearners.json", "/audio/..%5clearners.json",
                     "/audio/../confidential/attempts.jsonl", "/audio/%2e%2e/%2e%2e/server.py", "/audio/"):
            get(path)
        for rng in ("bytes=0-9", "bytes=-5", "bytes=5-", "bytes=abc", "bytes=99999999-", "bytes=9-2"):
            get("/audio/clip.mp3", Range=rng)
        get("/api/run?mode=practice&section=mixed&n=abc")
        log.append(_call(port, "POST", "/api/logout", None, {"Content-Type": "application/json"}))
        log.append(_call(port, "POST", "/api/logout", b"{}", {"Content-Type": "application/json", "Content-Length": "x"}))
        log.append(_call(port, "POST", "/api/logout", None, {"Content-Type": "application/json", "Content-Length": str(70000)}))
        log.append(_call(port, "POST", "/api/logout", b"{}", {"Content-Type": "text/plain", "Content-Length": "2"}))
        log.append(_post(port, "/api/logout", {}, Origin="https://evil.example"))
        log.append(_post(port, "/api/logout", {}, Origin=f"http://127.0.0.1:{port}"))
        log.append(_call(port, "POST", "/api/logout", b"{nope", {"Content-Type": "application/json", "Content-Length": "5"}))
        run = _call(port, "GET", "/api/run?mode=practice&section=mixed&n=2", None, None, "yoko")["body"]
        stored = sorted(p.name for p in (home / "learners" / "yoko" / "open_runs").glob("*.json"))
        portal.RUNS.clear()
        log.append(_post(port, "/api/answer", {"run_id": run["run_id"], "item_id": run["items"][0]["id"], "choice": 1, "ms": 1000}, "yoko"))
        portal.RUNS.clear()
        log.append(_post(port, "/api/answer", {"run_id": run["run_id"], "item_id": run["items"][0]["id"], "choice": 1, "ms": 1000}, "anna"))
        finished = _post(port, "/api/finish", {"run_id": run["run_id"]}, "yoko")
        log.append({**finished, "body": {"score": finished["body"]["score"], "answered": [x["choice"] for x in finished["body"]["items"]]}})
        left = sorted(p.name for p in (home / "learners" / "yoko" / "open_runs").glob("*.json"))
        (home / "learners.json").write_text("{broken", encoding="utf-8")
        get("/api/me")
        access_log = [json.loads(x) for f in sorted((home / "logs").glob("access-*.jsonl")) for x in f.read_text(encoding="utf-8").splitlines()]
        errors = (home / "logs" / "errors.log").read_text(encoding="utf-8")
    return {"calls": log, "open_runs": {"after_start": stored, "after_finish": left},
            "access_log": {"lines": len(access_log), "fields": sorted(access_log[0]), "sample": {k: access_log[2][k] for k in ("email", "as_learner", "method", "path", "status")}},
            "errors_log": {"tracebacks": errors.count("Traceback"), "mentions_json": "JSONDecodeError" in errors}}


def audio_root():
    log = []
    with two_learners() as home:
        outside = home.parent / "media" / "jlpt" / "audio"
        outside.mkdir(parents=True)
        (outside / "elsewhere.mp3").write_bytes(b"ID3-outside")
        with env(JLPT_AUDIO=str(outside), JLPT_ORIGIN=None, JLPT_AUTH=None), server() as port:
            for path in ("/audio/elsewhere.mp3", "/audio/clip.mp3", "/audio/../learners.json", "/audio/../../home/learners.json", "/audio/%2e%2e/audio/elsewhere.mp3"):
                log.append(_call(port, "GET", path, None, None, "yoko"))
    return {"calls": log}


def startup():
    from engine import access
    out = {}
    for name, values in {"default": {}, "local_lan": {"JLPT_BIND": "0.0.0.0"}, "tailscale": {"JLPT_AUTH": "tailscale"},
                         "tailscale_lan": {"JLPT_AUTH": "tailscale", "JLPT_BIND": "0.0.0.0"}, "tailscale_localhost_name": {"JLPT_AUTH": "tailscale", "JLPT_BIND": "localhost"},
                         "cloudflare_access_gone": {"JLPT_AUTH": "access"}, "unknown_mode": {"JLPT_AUTH": "open"}}.items():
        with env(**{"JLPT_AUTH": None, "JLPT_BIND": None, **values}):
            try:
                access.check_startup()
                out[name] = {"starts": True, "bind": access.bind()}
            except SystemExit as e:
                out[name] = {"starts": False, "message": str(e)}
    return out
