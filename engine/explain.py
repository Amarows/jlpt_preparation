"""Wrong-answer explanations: sentence with furigana, translation, option meanings, evidence and steps.

They live in data/explain.json ({item_id: explain}), apart from the item files, so importers can rewrite items
without losing them and adding one never changes an item or its attempt history. Each entry stores `for`, a
fingerprint of the item's stem, options and answer; an entry whose item has changed since is not served.
"""
import csv, hashlib, json, re
from . import paths

RUBY = re.compile(r"\{([^{}|]+)\|([^{}|]+)\}")
_cache = {"mtime": None, "data": {}}
_vocab = {}


def fingerprint(item: dict) -> str:
    raw = json.dumps([item["stem"], item["options"], item["answer"]], ensure_ascii=False)
    return hashlib.sha256(raw.encode("utf-8")).hexdigest()[:12]


def plain(s: str) -> str:
    """Text without furigana: {漢字|かんじ} → 漢字."""
    return RUBY.sub(r"\1", s)


def kana(s: str) -> str:
    """Text read aloud: {漢字|かんじ} → かんじ."""
    return RUBY.sub(r"\2", s)


def file():
    return paths.DATA / "explain.json"


def load() -> dict[str, dict]:
    f = file()
    try: mtime = f.stat().st_mtime
    except OSError: return {}
    if _cache["mtime"] != mtime:
        try: _cache.update(mtime=mtime, data=json.loads(f.read_text(encoding="utf-8")))
        except (OSError, ValueError): return _cache["data"]
    return _cache["data"]


def vocab() -> dict[str, tuple[str, str]]:
    """N4 word list: kanji or kana spelling → (reading, meaning)."""
    if not _vocab:
        with (paths.REPO / "data" / "vocabulary.csv").open(encoding="utf-8") as f:
            for row in csv.DictReader(f):
                for key in (row["kanji"], row["reading"]):
                    _vocab.setdefault(key, (row["reading"], row["meaning"]))
    return _vocab


def for_item(item: dict) -> dict | None:
    """The checked explanation for this item, or else option meanings from the word list, or None."""
    x = load().get(item["id"])
    if x and x.get("for") == fingerprint(item): return x
    words = vocab()
    options = []
    for o in item["options"]:
        key = re.sub(r"[\s　【】]", "", o)
        r, en = words.get(key, (None, None))
        options.append({"ruby": o, "en": en, **({"r": r} if r and r != key else {})} if en else None)
    return {"fallback": True, "options": options} if any(options) else None
