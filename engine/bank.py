"""Bank loading and lightweight schema validation."""
import json
from pathlib import Path
from . import paths, tracks

TIERS = {"easy", "medium", "hard"}

def load_bank(root: Path | None = None) -> tuple[dict[str, dict], dict[str, dict]]:
    """Load valid item objects and passages, keyed by id."""
    root = root or paths.BANK
    items: dict[str, dict] = {}
    passages: dict[str, dict] = {}
    # A mock stays out of practice until it has been taken.
    taken = set()
    for meta in root.glob("mocks/*/mock.json"):
        try:
            if json.loads(meta.read_text(encoding="utf-8")).get("taken"): taken.add(meta.parent.name)
        except (OSError, json.JSONDecodeError): pass
    for f in root.rglob("*.json"):
        rel = f.relative_to(root).parts
        if rel[0] == "mocks" and (len(rel) < 3 or rel[1] not in taken) or f.name == "mock.json" or f.name.endswith("_key.json"): continue
        try: data = json.loads(f.read_text(encoding="utf-8"))
        except (OSError, json.JSONDecodeError): continue
        if f.name == "passages.json":
            for p in data: passages[p["id"]] = p
            continue
        if isinstance(data, list):
            for item in data:
                validate_item(item)
                items[item["id"]] = item
    return items, passages

def validate_item(x: dict) -> None:
    """Raise ValueError if an item violates the data contract."""
    exam = tracks.exam()
    required = {"id", "section", "mondai", "tier_prior", "level", "stem", "options", "answer", "tags", "source", "verified"}
    if not isinstance(x, dict) or not required <= x.keys() or not any(k.startswith("explanation_") for k in x): raise ValueError("missing item fields")
    if x["section"] not in tracks.sections() or x["mondai"] not in tracks.blueprint() or x["tier_prior"] not in TIERS or x["level"] not in exam["levels"]: raise ValueError(f"invalid item dimensions: {x.get('id')}")
    n = len(x["options"])
    if n not in exam["options"].get(x["mondai"], exam["options"]["default"]) or len(set(x["options"])) != n or x["answer"] not in range(1, n + 1): raise ValueError(f"invalid options/answer: {x['id']}")
    if not isinstance(x["tags"], list): raise ValueError(f"invalid tags: {x['id']}")
