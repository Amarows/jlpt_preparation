import importlib
import json
import os
import pkgutil
import shutil
import sys
import tempfile
import threading
import urllib.error
import urllib.request
import uuid
from contextlib import contextmanager
from datetime import date, datetime, timedelta, timezone
from http.server import ThreadingHTTPServer
from pathlib import Path

FIXTURE = Path(__file__).with_name("golden_n4_fixture")
NOW = datetime(2026, 11, 8, 12, 0, tzinfo=timezone.utc)


class FixedDate(date):
    @classmethod
    def today(cls):
        return cls(NOW.year, NOW.month, NOW.day)


class FixedDatetime(datetime):
    @classmethod
    def now(cls, tz=None):
        return NOW.astimezone(tz) if tz else NOW.astimezone().replace(tzinfo=None)


def _source():
    real = os.environ.get("N4_REAL_HOME")
    if not real:
        return {"bank": FIXTURE / "bank", "explain": FIXTURE / "explain.json", "confidential": FIXTURE, "audio": FIXTURE / "audio", "link_audio": False}
    real = Path(real)
    return {"bank": real / "data" / "bank", "explain": real / "data" / "explain.json", "confidential": real / "confidential", "audio": real / "audio", "link_audio": True}


def _build(home):
    src = _source()
    shutil.copytree(src["bank"], home / "data" / "bank")
    if src["explain"].exists():
        shutil.copy(src["explain"], home / "data" / "explain.json")
    (home / "confidential").mkdir()
    for name in ("attempts.jsonl", "runs.jsonl", "focus.json", "model_state.json"):
        if (src["confidential"] / name).exists():
            shutil.copy(src["confidential"] / name, home / "confidential" / name)
    if src["link_audio"]:
        for f in src["audio"].rglob("*"):
            if f.is_file():
                (home / "audio" / f.relative_to(src["audio"])).parent.mkdir(parents=True, exist_ok=True)
                (home / "audio" / f.relative_to(src["audio"])).touch()
    else:
        shutil.copytree(src["audio"], home / "audio")


def shifted_real_clock():
    days = int(os.environ.get("GOLDEN_CLOCK_SHIFT_DAYS") or 0)
    if not days:
        return []
    shift = timedelta(days=days)
    later_dt = type("LaterDatetime", (datetime,), {"now": classmethod(lambda cls, tz=None: datetime.now(tz) + shift)})
    later_d = type("LaterDate", (date,), {"today": classmethod(lambda cls: date.today() + shift)})
    import engine
    import server
    for info in pkgutil.iter_modules(engine.__path__):
        importlib.import_module(f"engine.{info.name}")
    mods = [m for name, m in list(sys.modules.items()) if name == "server" or name.startswith("engine.")]
    return [(m, "datetime", later_dt) for m in mods if getattr(m, "datetime", None) is datetime] + [(m, "date", later_d) for m in mods if getattr(m, "date", None) is date]


@contextmanager
def _patched(pairs):
    saved = [(obj, name, getattr(obj, name)) for obj, name, _ in pairs]
    for obj, name, value in pairs:
        setattr(obj, name, value)
    try:
        yield
    finally:
        for obj, name, value in reversed(saved):
            setattr(obj, name, value)


@contextmanager
def portal():
    from engine import explain, leitner, mock, paths, report, select, simulate
    import server
    tmp = Path(tempfile.mkdtemp()).resolve()
    home = tmp / "home"
    home.mkdir()
    _build(home)
    counter = iter(range(1, 10 ** 6))
    pairs = shifted_real_clock() + [(paths, "HOME", home), (simulate, "date", FixedDate), (mock, "date", FixedDate), (select, "datetime", FixedDatetime),
             (leitner, "datetime", FixedDatetime), (report, "datetime", FixedDatetime), (server, "datetime", FixedDatetime),
             (server.uuid, "uuid4", lambda: uuid.UUID(int=next(counter)))]
    explain._cache.clear()
    try:
        with _patched(pairs):
            yield home
    finally:
        explain._cache.clear()
        shutil.rmtree(tmp, ignore_errors=True)


def _open_mock():
    from engine.mock import mocks
    return next((m["id"] for m in mocks() if m["open"] and not m.get("taken")), None)


def bank():
    from engine.bank import load_bank, validate_item
    with portal():
        items, passages = load_bank()
        bad = {}
        sample = next(iter(items.values()))
        for name, change in {"three_options": {"options": ["a", "b", "c"], "answer": 1}, "answer_out_of_range": {"answer": 5},
                             "unknown_mondai": {"mondai": "essay"}, "duplicate_options": {"options": ["a", "a", "b", "c"]}}.items():
            try:
                validate_item({**sample, **change})
                bad[name] = "accepted"
            except ValueError as e:
                bad[name] = f"ValueError: {e}"
        return {"items": sorted(items), "passages": sorted(passages), "invalid": bad}


def model():
    from engine.bank import load_bank
    from engine.model import fit, read_attempts
    with portal():
        return fit(read_attempts(), load_bank()[0])


def state():
    from engine.simulate import simulate
    with portal() as home:
        before = simulate(write=False)
        after = simulate(write=True, record_run=True)
        return {"read_only": before, "after_run": after, "written": json.loads((home / "confidential" / "model_state.json").read_text(encoding="utf-8"))}


def run(mode, section, n, seed):
    from engine.select import build_run
    with portal():
        r = build_run(mode, section, n, seed=seed)
        return {"mode": r["mode"], "time_limit_ms": r["time_limit_ms"], "items": [x["id"] for x in r["items"]], "passages": r["passages"]}


def mocks():
    from engine.mock import assemble, mocks as listing, score
    with portal():
        mid = _open_mock()
        if not mid:
            return {"listing": listing()}
        a = assemble(mid)
        ids = [x["id"] for x in a["items"]]
        return {"listing": listing(), "open": {"id": mid, "items": ids, "parts": a["parts"], "passages": a["passages"]},
                "score_all": score(a["items"], set(ids)), "score_half": score(a["items"], set(ids[::2])), "score_none": score(a["items"], set())}


def report():
    from engine.bank import load_bank
    from engine.report import build_report
    with portal():
        return build_report(load_bank()[0], now=NOW)


def explanations():
    from engine.bank import load_bank
    from engine.explain import for_item
    with portal():
        return {i: for_item(x) for i, x in sorted(load_bank()[0].items())}


def health():
    from engine.bank import load_bank
    from engine.health import item_health
    from engine.model import read_attempts
    with portal():
        return item_health(load_bank()[0], read_attempts())


def api():
    import server
    with portal() as home:
        server.BANKS.clear()
        server.RUNS.clear()
        srv = ThreadingHTTPServer(("127.0.0.1", 0), server.Handler)
        threading.Thread(target=srv.serve_forever, daemon=True).start()
        base = f"http://127.0.0.1:{srv.server_port}"
        mid = _open_mock()
        log = []

        def call(path, body=None):
            req = urllib.request.Request(base + path, data=None if body is None else json.dumps(body).encode(), headers={"Content-Type": "application/json"})
            try:
                with urllib.request.urlopen(req) as r:
                    out = {"status": r.status, "body": json.loads(r.read())}
            except urllib.error.HTTPError as e:
                raw = e.read()
                try:
                    out = {"status": e.code, "body": json.loads(raw)}
                except ValueError:
                    out = {"status": e.code}
            log.append({"request": path, "sent": body, **out})
            return out.get("body")

        try:
            call("/api/status")
            call("/api/mocks")
            call("/api/report")
            for query in ("mode=practice&section=mixed&n=12", "mode=timed&section=vocab&n=5", "mode=drill&section=mistakes&n=6", f"mode=mock&mock={mid}", "mode=mock&mock=m3"):
                r = call("/api/run?" + query)
                if not r or "run_id" not in r:
                    continue
                for k, item in enumerate(r["items"]):
                    call("/api/answer", {"run_id": r["run_id"], "item_id": item["id"], "choice": 1 + k % len(item["options"]), "ms": 3000 + 1000 * k,
                                         "flag": ["none", "guess", "unclear"][k % 3], "timed_out": k == 4})
                call("/api/answer", {"run_id": r["run_id"], "item_id": r["items"][0]["id"], "choice": 2, "ms": 1})
                call("/api/finish", {"run_id": r["run_id"]})
            call("/api/answer", {"run_id": "r-unknown", "item_id": "x"})
            call("/api/finish", {"run_id": "r-unknown"})
            call("/api/explain_feedback", {"item_id": 7})
            call("/api/explain_feedback", {"item_id": "gr-grammar_form-0", "run_id": "r-x", "choice": 2})
            call("/api/nothing", {})
            call("/web/../server.py")
            call("/nothing")
        finally:
            srv.shutdown()
            srv.server_close()
        conf = home / "confidential"
        files = {name: [json.loads(x) for x in (conf / name).read_text(encoding="utf-8").splitlines()] for name in ("attempts.jsonl", "runs.jsonl", "explain_feedback.jsonl") if (conf / name).exists()}
        return {"calls": log, "files": files, "mock": json.loads((home / "data" / "bank" / "mocks" / mid / "mock.json").read_text(encoding="utf-8")) if mid else None}
