"""Bank loading and lightweight schema validation."""
import json
from pathlib import Path
from . import paths

MONDAI = set("kanji_reading orthography contextual paraphrase usage grammar_form sentence_composition text_grammar short_passage mid_passage info_retrieval task_based key_points verbal_expression quick_response instruction_phrase".split())
SECTIONS = {"vocab", "grammar", "reading", "listening"}
TIERS = {"easy", "medium", "hard"}
LEVELS = {"N5", "N4-core", "N4-hard"}
THREE_OPTIONS = {"verbal_expression", "quick_response"}

def load_bank(root: Path | None = None) -> tuple[dict[str, dict], dict[str, dict]]:
    """Load valid item objects and passages, keyed by id."""
    root = root or paths.BANK
    items: dict[str, dict] = {}
    passages: dict[str, dict] = {}
    for f in root.rglob("*.json"):
        if "mocks" in f.parts or f.name.endswith("_key.json"): continue
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
    required = {"id", "section", "mondai", "tier_prior", "level", "stem", "options", "answer", "tags", "explanation_en", "source", "verified"}
    if not isinstance(x, dict) or not required <= x.keys(): raise ValueError("missing item fields")
    if x["section"] not in SECTIONS or x["mondai"] not in MONDAI or x["tier_prior"] not in TIERS or x["level"] not in LEVELS: raise ValueError(f"invalid item dimensions: {x.get('id')}")
    # Listening 問題3 and 問題4 offer three spoken replies (written placement versions have four); everything else has four options.
    n = len(x["options"])
    if n not in ((3, 4) if x["mondai"] in THREE_OPTIONS else (4,)) or len(set(x["options"])) != n or x["answer"] not in range(1, n + 1): raise ValueError(f"invalid options/answer: {x['id']}")
    if not isinstance(x["tags"], list): raise ValueError(f"invalid tags: {x['id']}")
