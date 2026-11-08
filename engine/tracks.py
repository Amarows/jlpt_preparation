import json
from functools import lru_cache
from pathlib import Path

from . import paths

ROOT = Path(__file__).resolve().parents[1] / "tracks"


@lru_cache(maxsize=None)
def load(track_id: str) -> dict:
    return {**json.loads((ROOT / track_id / "track.json").read_text(encoding="utf-8")), "id": track_id}


def current() -> dict:
    return load(paths.learner()["track"])


def exam() -> dict:
    return current()["exam"]


def sections() -> list[str]:
    return [s["id"] for s in exam()["sections"]]


def section_mondai() -> dict[str, list[str]]:
    return {s["id"]: list(s["mondai"]) for s in exam()["sections"]}


def blueprint() -> dict[str, int]:
    return {m: n for s in exam()["sections"] for m, n in s["mondai"].items()}


def prior(section: str) -> float:
    return next((s["prior"] for s in exam()["sections"] if s["id"] == section), .5)


def summary() -> dict:
    t = current()
    e = t["exam"]
    return {"id": t["id"], "title": t["title"], "lang": t["lang"], "date": e["date"], "mocks": bool(e["parts"]), "explain": sorted(t.get("explain", {})),
            "sections": [{"id": s["id"], "name": s.get("name", {})} for s in e["sections"]]}
