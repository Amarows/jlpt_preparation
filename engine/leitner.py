"""Leitner review state derived from the attempt log."""
from datetime import datetime, timedelta, timezone

INTERVALS = [0, 1, 2, 4, 7, 14]
GROUPS = {"kanji_reading":(10,20),"orthography":(10,20),"quick_response":(10,20),"instruction_phrase":(10,20),"contextual":(15,30),"paraphrase":(15,30),"grammar_form":(15,30),"usage":(30,60),"sentence_composition":(30,60),"text_grammar":(30,60),"short_passage":(60,120),"mid_passage":(60,120),"info_retrieval":(60,120),"task_based":(15,25),"key_points":(15,25),"verbal_expression":(15,25)}

def target_ms(item: dict) -> int:
    """Target response time in milliseconds."""
    easy, medium = GROUPS.get(item.get("mondai", "grammar_form"), (15,30))
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
