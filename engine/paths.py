import json
import os
import re
from contextlib import contextmanager
from contextvars import ContextVar
from pathlib import Path

REPO = Path(__file__).resolve().parents[1]
HOME = Path(os.environ.get("JLPT_HOME", REPO)).expanduser().resolve()
DEFAULT = {"id": "default", "name": "Learner", "track": "jlpt-n4", "ui": "en", "explain": "en", "data": "confidential"}
FILES = {"ATTEMPTS": "attempts.jsonl", "RUNS": "runs.jsonl", "MODEL_STATE": "model_state.json"}
_current = ContextVar("learner", default=None)
ID = re.compile(r"[a-z0-9][a-z0-9_-]{0,31}")
UI = {"en", "ja"}


def learners() -> list[dict]:
    f = HOME / "learners.json"
    if not f.exists():
        return [DEFAULT]
    rows = json.loads(f.read_text(encoding="utf-8"))["learners"]
    if not isinstance(rows, list) or not rows or not all(isinstance(r, dict) and {"id", "track"} <= r.keys() for r in rows):
        raise ValueError("learners.json: learners must be a non-empty list, each with id and track")
    out = [{"ui": "en", "explain": "en", "data": f"learners/{r['id']}", "name": r["id"], **r} for r in rows]
    validate(out)
    return out


def validate(rows: list[dict]) -> None:
    from . import tracks
    for r in rows:
        for k in ("id", "track"):
            if not isinstance(r[k], str) or not ID.fullmatch(r[k]):
                raise ValueError(f"learners.json: {k} must match {ID.pattern}: {r[k]!r}")
        if r["ui"] not in UI:
            raise ValueError(f"learners.json: ui must be one of {sorted(UI)}: {r['id']}")
        try:
            track = tracks.load(r["track"])
        except FileNotFoundError:
            raise ValueError(f"learners.json: unknown track {r['track']!r}: {r['id']}") from None
        if track.get("explain") and r["explain"] not in track["explain"]:
            raise ValueError(f"learners.json: track {r['track']} has no {r['explain']!r} explanations: {r['id']}")
    ids = [r["id"] for r in rows]
    data = [under_home(r["data"]) for r in rows]
    if len(set(ids)) != len(ids) or len(set(data)) != len(data):
        raise ValueError("learners.json: ids and data folders must be unique")


def find(learner_id) -> dict | None:
    return next((r for r in learners() if r["id"] == learner_id), None)


def learner() -> dict:
    return _current.get() or learners()[0]


@contextmanager
def as_learner(learner_id: str):
    row = find(learner_id)
    if row is None:
        raise KeyError(learner_id)
    token = _current.set(row)
    try:
        yield row
    finally:
        _current.reset(token)


def __getattr__(name):
    if name == "DATA":
        return HOME / "data"
    if name == "BANK":
        from . import tracks
        return HOME / tracks.current()["bank"]
    if name == "CONFIDENTIAL":
        return HOME / learner()["data"]
    if name in FILES:
        return HOME / learner()["data"] / FILES[name]
    raise AttributeError(name)


def under_home(path: str | Path) -> Path:
    p = (HOME / path).resolve()
    if p != HOME and HOME not in p.parents:
        raise ValueError("path escapes JLPT_HOME")
    return p
