"""Leitner review state derived from the attempt log."""
from datetime import datetime, timedelta, timezone
from . import tracks

INTERVALS = [0, 1, 2, 4, 7, 14]

def target_ms(item: dict) -> int:
    """Target response time in milliseconds."""
    easy, medium = tracks.exam()["target_s"].get(item.get("mondai", "grammar_form"), (15,30))
    sec = easy if item.get("tier_prior") == "easy" else medium * (2 if item.get("tier_prior") == "hard" else 1)
    return sec * 1000

def boxes(attempts: list[dict], items: dict[str, dict] | None = None) -> dict[str, int]:
    """Replay attempts and return each item's current box."""
    state = {}; items = items or {}
    for a in sorted(attempts, key=lambda x: x.get("ts", "")):
        i = a["item_id"]; old = state.get(i, 0)
        if a.get("flag") == "unclear" or a.get("timed_out") or not a.get("correct"):
            state[i] = 0
        elif a.get("ms") is not None and a["ms"] <= target_ms(a.get("item") or items.get(i) or {"mondai":a.get("mondai", "grammar_form"), "tier_prior":a.get("tier_prior", "medium")}):
            state[i] = min(5, old + 1)
        else: state[i] = old
    return state

def due(box: int, last_ts: str | None, now: datetime | None = None) -> bool:
    if box == 0 or not last_ts: return box == 0
    now = now or datetime.now(timezone.utc)
    try: then = datetime.fromisoformat(last_ts)
    except ValueError: return True
    return now.date() >= (then.date() + timedelta(days=INTERVALS[box]))
