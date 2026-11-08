import json
import shutil
import threading
import urllib.error
import urllib.request
import uuid
from contextlib import contextmanager
from http.server import ThreadingHTTPServer
from pathlib import Path

from tests.golden_n4 import portal

FIXTURE = Path(__file__).with_name("golden_learners_fixture")
LEARNERS = [{"id": "anna", "name": "Anna", "track": "jlpt-n4", "data": "confidential"},
            {"id": "yoko", "name": "Yoko", "track": "de-work", "ui": "ja", "explain": "ja"}]
INVALID = {
    "empty": [],
    "no_track": [{"id": "anna"}],
    "duplicate_id": [LEARNERS[0], {**LEARNERS[1], "id": "anna"}],
    "id_with_slash": [{**LEARNERS[0], "id": "../anna"}],
    "id_uppercase": [{**LEARNERS[0], "id": "Anna"}],
    "unknown_track": [{**LEARNERS[0], "track": "jlpt-n1"}],
    "track_traversal": [{**LEARNERS[0], "track": "../jlpt-n4"}],
    "ui_unknown": [{**LEARNERS[0], "ui": "fr"}],
    "explain_missing": [{**LEARNERS[1], "explain": "en"}],
    "shared_data": [LEARNERS[0], {**LEARNERS[1], "data": "confidential"}],
    "data_escapes_home": [{**LEARNERS[0], "data": "../elsewhere"}],
}


@contextmanager
def two_learners(rows=LEARNERS):
    with portal() as home:
        (home / "learners.json").write_text(json.dumps({"learners": rows}), encoding="utf-8")
        shutil.copytree(FIXTURE / "de_bank", home / "data" / "tracks" / "de-work" / "bank")
        yield home


@contextmanager
def _uuids(server, counter):
    saved = server.uuid.uuid4
    server.uuid.uuid4 = lambda: uuid.UUID(int=next(counter) << 100)
    try:
        yield
    finally:
        server.uuid.uuid4 = saved


def validation():
    from engine import paths
    out = {}
    with two_learners() as home:
        out["valid"] = paths.learners()
        for name, rows in INVALID.items():
            (home / "learners.json").write_text(json.dumps({"learners": rows}), encoding="utf-8")
            try:
                out[name] = paths.learners()
            except ValueError as e:
                out[name] = f"ValueError: {e}"
    return out


def api():
    import server
    counter = iter(range(1, 10 ** 6))
    with two_learners() as home, _uuids(server, counter):
        server.BANKS.clear()
        server.RUNS.clear()
        srv = ThreadingHTTPServer(("127.0.0.1", 0), server.Handler)
        threading.Thread(target=srv.serve_forever, daemon=True).start()
        base = f"http://127.0.0.1:{srv.server_port}"
        log = []

        def call(path, body=None, learner=None):
            headers = {"Content-Type": "application/json", **({"Cookie": f"learner={learner}"} if learner else {})}
            req = urllib.request.Request(base + path, data=None if body is None else json.dumps(body).encode(), headers=headers)
            try:
                with urllib.request.urlopen(req) as r:
                    out = {"status": r.status, "body": json.loads(r.read()), "cookie": r.headers.get("Set-Cookie")}
            except urllib.error.HTTPError as e:
                out = {"status": e.code, "body": json.loads(e.read())}
            log.append({"request": path, "as": learner, "sent": body, **{k: v for k, v in out.items() if v is not None}})
            return out["body"]

        def practice(learner, query):
            r = call("/api/run?" + query, learner=learner)
            for k, item in enumerate(r["items"]):
                call("/api/answer", {"run_id": r["run_id"], "item_id": item["id"], "choice": 1 + k % 2, "ms": 4000 + 500 * k, "flag": "none"}, learner)
            return r["run_id"]

        try:
            call("/api/learners")
            call("/api/status")
            call("/api/me")
            call("/api/me", learner="nobody")
            call("/api/login", {"learner": "nobody"})
            call("/api/login", {"learner": "yoko"})
            call("/api/me", learner="yoko")
            call("/api/status", learner="yoko")
            call("/api/mocks", learner="yoko")
            yoko_run = practice("yoko", "mode=practice&section=mixed&n=6")
            call("/api/answer", {"run_id": yoko_run, "item_id": "dw-meaning-1", "choice": 1}, "anna")
            call("/api/finish", {"run_id": yoko_run}, "anna")
            call("/api/finish", {"run_id": yoko_run}, "yoko")
            call("/api/report", learner="yoko")
            call("/api/explain_feedback", {"item_id": "dw-cloze-1", "choice": 2}, "yoko")
            call("/api/me", learner="anna")
            call("/api/status", learner="anna")
            anna_run = practice("anna", "mode=drill&section=vocab&n=3")
            call("/api/finish", {"run_id": anna_run}, "yoko")
            call("/api/finish", {"run_id": anna_run}, "anna")
            call("/api/logout", {})
        finally:
            srv.shutdown()
            srv.server_close()
        files = {str(f.relative_to(home)).replace("\\", "/"): len(f.read_text(encoding="utf-8").splitlines())
                 for d in ("confidential", "learners") if (home / d).exists() for f in sorted((home / d).rglob("*.json*"))}
        return {"calls": log, "files": files}
