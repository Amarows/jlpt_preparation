"""Wrong-answer explanations: sentence with furigana, translation, option meanings, evidence and steps.

They live in data/explain.json ({item_id: explain}), apart from the item files, so importers can rewrite items
without losing them and adding one never changes an item or its attempt history. Each entry stores `for`, a
fingerprint of the item's stem, options and answer; an entry whose item has changed since is not served.
"""
import csv, hashlib, json, re
from . import paths, tracks

RUBY = re.compile(r"\{([^{}|]+)\|([^{}|]+)\}")
_cache = {}
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
    files = tracks.current().get("explain", {})
    rel = files.get(paths.learner()["explain"]) or next(iter(files.values()), None)
    return paths.HOME / rel if rel else None


def load() -> dict[str, dict]:
    f = file()
    if f is None: return {}
    try: mtime = f.stat().st_mtime
    except OSError: return {}
    hit = _cache.get(f)
    if not hit or hit[0] != mtime:
        try: hit = _cache[f] = (mtime, json.loads(f.read_text(encoding="utf-8")))
        except (OSError, ValueError): return hit[1] if hit else {}
    return hit[1]


def vocab() -> dict[str, tuple[str, str]]:
    rel = tracks.current().get("word_list")
    if not rel: return {}
    if rel not in _vocab:
        words = _vocab[rel] = {}
        with (paths.REPO / rel).open(encoding="utf-8") as f:
            for row in csv.DictReader(f):
                for key in (row["kanji"], row["reading"]):
                    words.setdefault(key, (row["reading"], row["meaning"]))
    return _vocab[rel]


def explanations(item: dict) -> dict:
    return {k: v for k, v in item.items() if k.startswith("explanation_")}


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
