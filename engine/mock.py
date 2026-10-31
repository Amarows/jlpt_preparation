"""Reserved full mock exams: listing, exam-order assembly, scoring and release into practice."""
import json
from datetime import date

from . import paths
from .bank import validate_item
from .simulate import BLUEPRINT

# The real N4 timetable: (part, title, minutes, sections).
PARTS = [("vocab", "言語知識（文字・語彙）", 25, {"vocab"}),
         ("grammar_reading", "言語知識（文法）・読解", 55, {"grammar", "reading"}),
         ("listening", "聴解", 35, {"listening"})]
ORDER = list(BLUEPRINT)


def _meta_path(mock_id: str):
    return paths.BANK / "mocks" / mock_id / "mock.json"


def mocks() -> list[dict]:
    """Every mock with its opening date, whether it is open today, and its result once taken."""
    out = []
    for f in sorted((paths.BANK / "mocks").glob("*/mock.json")):
        try:
            meta = json.loads(f.read_text(encoding="utf-8"))
        except (OSError, json.JSONDecodeError):
            continue
        out.append({**meta, "open": date.today().isoformat() >= meta.get("opens", "9999")})
    return sorted(out, key=lambda m: m.get("opens", ""))


def load_mock(mock_id: str) -> tuple[list[dict], dict[str, dict]]:
    """Return the mock's items in exam order and its passages."""
    if mock_id not in {m["id"] for m in mocks()}:
        raise KeyError(mock_id)
    items, passages = [], {}
    for f in sorted(_meta_path(mock_id).parent.glob("*.json")):
        data = json.loads(f.read_text(encoding="utf-8"))
        if f.name == "passages.json":
            passages.update({p["id"]: p for p in data})
        elif isinstance(data, list):
            for x in data:
                validate_item(x)
                items.append(x)
    # Stable sort keeps the booklet order within each mondai.
    items.sort(key=lambda x: ORDER.index(x["mondai"]))
    return items, passages


def assemble(mock_id: str) -> dict:
    """Items in exam order plus the timed parts they fall into."""
    items, passages = load_mock(mock_id)
    ordered, parts = [], []
    for part, title, minutes, sections in PARTS:
        chunk = [x for x in items if x["section"] in sections]
        if chunk:
            ordered += chunk
            parts.append({"part": part, "title": title, "minutes": minutes, "count": len(chunk)})
    used = {x.get("passage_id") for x in ordered}
    return {"items": ordered, "parts": parts, "passages": {k: v["text"] for k, v in passages.items() if k in used}}


def score(items: list[dict], correct: set[str]) -> dict:
    """Section scores on the JLPT scale (raw share of the section's points) against the N4 pass lines."""
    lk = [x for x in items if x["section"] != "listening"]
    ls = [x for x in items if x["section"] == "listening"]
    lk_score = round(sum(x["id"] in correct for x in lk) / len(lk) * 120) if lk else 0
    l_score = round(sum(x["id"] in correct for x in ls) / len(ls) * 60) if ls else 0
    return {"lk": lk_score, "listening": l_score, "total": lk_score + l_score,
            "passed": lk_score >= 38 and l_score >= 19 and lk_score + l_score >= 90}


def mark_taken(mock_id: str, result: dict) -> None:
    """Record the result; the bank then serves this mock's items in practice."""
    f = _meta_path(mock_id)
    meta = json.loads(f.read_text(encoding="utf-8"))
    meta.update({"taken": date.today().isoformat(), "result": result})
    f.write_text(json.dumps(meta, ensure_ascii=False, indent=2), encoding="utf-8")
