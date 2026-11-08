import json
from datetime import datetime, timezone

from . import paths
from .model import _timestamp, current_attempts

STATES = ("not_started", "learning", "practised", "done")
_titles = {}


def unit_of(item: dict) -> str | None:
    return (item.get("source") or {}).get("batch")


def title(item: dict) -> dict:
    ref = str((item.get("source") or {}).get("ref", "")).split("#")[0]
    if not ref:
        return {}
    f = (paths.REPO / ref).resolve()
    if paths.REPO not in f.parents:
        return {}
    if f not in _titles:
        try:
            data = json.loads(f.read_text(encoding="utf-8"))
            _titles[f] = {k[6:]: v for k, v in data.items() if k.startswith("title_")}
        except (OSError, ValueError, AttributeError):
            _titles[f] = {}
    return _titles[f]


def state(rows: list[list[dict]]) -> str:
    if not any(rows):
        return "not_started"
    if not all(any(a.get("correct") for a in r) for r in rows):
        return "learning"
    days = lambda r: {_timestamp(a["ts"]).astimezone().date() for a in r if a.get("correct") and _timestamp(a.get("ts"))}
    if all(len(days(r)) >= 2 and r[-1].get("correct") for r in rows):
        return "done"
    return "practised"


def units(items: dict[str, dict], attempts: list[dict]) -> list[dict]:
    served = {i: x for i, x in items.items() if x.get("verified") and unit_of(x)}
    when = lambda a: _timestamp(a.get("ts")) or datetime.min.replace(tzinfo=timezone.utc)
    by_item = {i: [] for i in served}
    for a in sorted(current_attempts(attempts, items), key=when):
        if a.get("item_id") in by_item:
            by_item[a["item_id"]].append(a)
    out = {}
    for i, x in served.items():
        out.setdefault(unit_of(x), {"id": unit_of(x), "title": title(x), "ids": []})["ids"].append(i)
    return [{"id": u["id"], "title": u["title"], "items": len(u["ids"]),
             "known": sum(bool(by_item[i]) and bool(by_item[i][-1].get("correct")) for i in u["ids"]),
             "state": state([by_item[i] for i in u["ids"]])} for u in sorted(out.values(), key=lambda u: u["id"])]
