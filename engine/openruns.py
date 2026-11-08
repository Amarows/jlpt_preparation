import json
import re
import time

from . import paths

RID = re.compile(r"r-[0-9a-f]{12}")
MAX_AGE_S = 24 * 3600


def _file(rid: str):
    return paths.CONFIDENTIAL / "open_runs" / f"{rid}.json" if isinstance(rid, str) and RID.fullmatch(rid) else None


def save(rid: str, run: dict) -> None:
    f = _file(rid)
    if f is None:
        return
    f.parent.mkdir(parents=True, exist_ok=True)
    tmp = f.with_suffix(".tmp")
    tmp.write_text(json.dumps(run, ensure_ascii=False), encoding="utf-8")
    tmp.replace(f)


def load(rid: str) -> dict | None:
    f = _file(rid)
    try:
        if f is None or time.time() - f.stat().st_mtime > MAX_AGE_S:
            return None
        return json.loads(f.read_text(encoding="utf-8"))
    except (OSError, ValueError):
        return None


def drop(rid: str) -> None:
    f = _file(rid)
    if f is not None:
        f.unlink(missing_ok=True)


def prune() -> int:
    gone = 0
    for row in paths.learners():
        folder = paths.HOME / row["data"] / "open_runs"
        for f in folder.glob("*.json") if folder.is_dir() else []:
            if time.time() - f.stat().st_mtime > MAX_AGE_S:
                f.unlink(missing_ok=True)
                gone += 1
    return gone
