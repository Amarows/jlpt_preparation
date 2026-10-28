"""Front-page progress report built from attempts and runs."""
import json
from datetime import datetime, timedelta, timezone

from . import paths
from .bank import SECTIONS
from .model import _timestamp, current_attempts, open_mistakes, read_attempts

ORDER = ["vocab", "grammar", "reading", "listening"]


def _runs() -> list[dict]:
    out = []
    if paths.RUNS.exists():
        for line in paths.RUNS.read_text(encoding="utf-8").splitlines():
            try:
                out.append(json.loads(line))
            except json.JSONDecodeError:
                pass
    return out


def _option(item: dict, n) -> str | None:
    return item["options"][n - 1] if isinstance(n, int) and 1 <= n <= len(item.get("options", [])) else None


def build_report(items: dict[str, dict], days: int = 14, mistakes: int = 5, now: datetime | None = None) -> dict:
    """Return P(pass) per run, section accuracy over `days`, and the latest open mistakes."""
    now = now or datetime.now(timezone.utc)
    progress = []
    runs = _runs()
    last = runs[-1] if runs else None
    for r in runs:
        ts = _timestamp(r.get("end"))
        if ts and r.get("p_pass_after") is not None:
            progress.append({"ts": ts.isoformat(), "p_pass": r["p_pass_after"], "section": r.get("section"), "correct": r.get("correct"), "n": r.get("n")})
    progress.sort(key=lambda x: x["ts"])

    attempts = current_attempts(read_attempts(), items)
    since = now - timedelta(days=days)
    counts = {s: [0, 0] for s in ORDER}
    for a in attempts:
        item = items.get(a.get("item_id"))
        ts = _timestamp(a.get("ts"))
        if item and ts and ts >= since and item["section"] in SECTIONS and not a.get("review"):
            counts[item["section"]][0] += bool(a.get("correct"))
            counts[item["section"]][1] += 1
    wrong = list(open_mistakes(attempts, items).values())[::-1]
    return {
        "days": days,
        "last_run": {k: last.get(k) for k in ("mode", "section", "n")} if last else None,
        "open_mistakes": len(wrong),
        "progress": progress,
        "sections": [{"section": s, "correct": c, "total": t} for s, (c, t) in counts.items()],
        "mistakes": [{
            "ts": _timestamp(a.get("ts")).isoformat(), "section": items[a["item_id"]]["section"], "stem": items[a["item_id"]]["stem"],
            "choice": _option(items[a["item_id"]], a.get("choice")), "answer": _option(items[a["item_id"]], items[a["item_id"]]["answer"]),
            "timed_out": bool(a.get("timed_out")), "explanation_en": items[a["item_id"]].get("explanation_en"),
        } for a in wrong[:mistakes]],
    }
