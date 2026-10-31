"""Item health: flag items whose answers look wrong statistically, and compare source batches."""
import math
from collections import Counter, defaultdict

from .model import _difficulty, current_attempts, fit, get_theta, sigmoid


def _tail(k: int, n: int, p: float) -> float:
    """P(X >= k) for X ~ Binomial(n, p)."""
    return sum(math.comb(n, j) * p ** j * (1 - p) ** (n - j) for j in range(k, n + 1))


def batch_key(item: dict) -> str:
    src = item.get("source", {})
    return f"{src.get('kind', '?')}/{src.get('author', '?')}/{src.get('batch') or src.get('ref', '?')}"


def item_health(items: dict[str, dict], attempts: list[dict], alpha: float = .05) -> dict:
    """Return suspect items and per-batch accuracy against what the learner's level predicts."""
    attempts = [a for a in current_attempts(attempts, items) if a.get("item_id") in items and not a.get("review")]
    model = fit(attempts, items)
    by_item = defaultdict(list)
    for a in attempts:
        by_item[a["item_id"]].append(a)
    suspects = []
    batches = defaultdict(lambda: {"n": 0, "correct": 0, "expected": 0.0})
    for item_id, rows in by_item.items():
        item = items[item_id]
        # Expected accuracy uses the label prior only, so a bad item cannot explain itself away through its offset.
        p = sigmoid(get_theta(model, item["section"]) - _difficulty(item))
        correct = [bool(a.get("correct")) and not a.get("timed_out") for a in rows]
        wrong = len(rows) - sum(correct)
        b = batches[(batch_key(item), item["mondai"])]
        b["n"] += len(rows); b["correct"] += sum(correct); b["expected"] += p * len(rows)
        reasons = []
        if wrong >= 2 and _tail(wrong, len(rows), 1 - p) < alpha:
            reasons.append(f"missed {wrong}/{len(rows)}, expected {1 - p:.0%} misses")
        picks = Counter(a.get("choice") for a, ok in zip(rows, correct) if not ok and a.get("choice") is not None)
        if picks and picks.most_common(1)[0][1] >= 2:
            choice, times = picks.most_common(1)[0]
            reasons.append(f"same wrong option {choice} picked {times} times")
        unclear = sum(a.get("flag") == "unclear" for a in rows)
        if unclear >= 2:
            reasons.append(f"marked unclear {unclear} times")
        if reasons:
            suspects.append({"id": item_id, "batch": batch_key(item), "stem": item["stem"], "reasons": reasons})
    return {
        "suspects": sorted(suspects, key=lambda s: (-len(s["reasons"]), s["id"])),
        "batches": [{"batch": k, "mondai": m, **v, "accuracy": v["correct"] / v["n"], "expected_accuracy": v["expected"] / v["n"]}
                    for (k, m), v in sorted(batches.items())],
    }


def to_markdown(health: dict) -> str:
    lines = ["# Item health", "", "## Suspect items", ""]
    lines += [f"- `{s['id']}` ({s['batch']}): {s['stem'][:60]} — {'; '.join(s['reasons'])}" for s in health["suspects"]] or ["None."]
    lines += ["", "## Batches", "", "| Batch | Mondai | Answers | Accuracy | Expected |", "|---|---|---|---|---|"]
    lines += [f"| {b['batch']} | {b['mondai']} | {b['n']} | {b['accuracy']:.0%} | {b['expected_accuracy']:.0%} |" for b in health["batches"]]
    return "\n".join(lines) + "\n"
