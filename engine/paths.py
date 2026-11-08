import json
import os
from contextlib import contextmanager
from contextvars import ContextVar
from pathlib import Path

REPO = Path(__file__).resolve().parents[1]
HOME = Path(os.environ.get("JLPT_HOME", REPO)).expanduser().resolve()
DEFAULT = {"id": "default", "name": "Learner", "track": "jlpt-n4", "ui": "en", "explain": "en", "data": "confidential"}
FILES = {"ATTEMPTS": "attempts.jsonl", "RUNS": "runs.jsonl", "MODEL_STATE": "model_state.json"}
_current = ContextVar("learner", default=None)


def learners() -> list[dict]:
    f = HOME / "learners.json"
    if not f.exists():
        return [DEFAULT]
    rows = json.loads(f.read_text(encoding="utf-8"))["learners"]
    out = [{"ui": "en", "explain": "en", "data": f"learners/{r['id']}", "name": r["id"], **r} for r in rows]
    ids = [r["id"] for r in out]
    if not out or len(set(ids)) != len(ids):
        raise ValueError("learners.json needs at least one learner and unique ids")
    for r in out:
        under_home(r["data"])
    return out


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
