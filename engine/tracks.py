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


def training() -> list[dict]:
    return current().get("training", [])


def item_sections() -> list[str]:
    return sections() + [s["id"] for s in training()]


def item_mondai() -> list[str]:
    return list(blueprint()) + [m for s in training() for m in s["mondai"]]


def _section(section: str) -> dict:
    return next((s for s in exam()["sections"] + training() if s["id"] == section), {})


def prior(section: str) -> float:
    return _section(section).get("prior", .5)


def prior_sd(section: str) -> float:
    return _section(section).get("prior_sd", 1.0)


def summary() -> dict:
    t = current()
    e = t["exam"]
    return {"id": t["id"], "title": t["title"], "lang": t["lang"], "date": e["date"], "mocks": bool(e["parts"]), "explain": sorted(t.get("explain", {})), "features": t.get("features", []),
            "sections": [{"id": s["id"], "name": s.get("name", {})} for s in e["sections"]],
            **({"training": [{"id": s["id"], "name": s.get("name", {})} for s in training()]} if training() else {}),
            **({"exam_title": e["title"]} if e.get("title") else {})}
