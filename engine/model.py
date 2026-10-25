"""Bayesian section abilities and Elo-style tag skills."""
import json
import math
from collections import defaultdict
from datetime import date, datetime, timezone
import numpy as np

from . import paths
from .bank import load_bank
from .leitner import boxes, target_ms


def sigmoid(x: float) -> float:
    return 1 / (1 + math.exp(-max(-30, min(30, x))))


def read_attempts() -> list[dict]:
    out = []
    if paths.ATTEMPTS.exists():
        for line in paths.ATTEMPTS.read_text(encoding="utf-8").splitlines():
            try:
                out.append(json.loads(line))
            except json.JSONDecodeError:
                pass
    return out


def _timestamp(value):
    try:
        parsed = datetime.fromisoformat(str(value).replace("Z", "+00:00"))
        return parsed.replace(tzinfo=timezone.utc) if parsed.tzinfo is None else parsed.astimezone(timezone.utc)
    except (TypeError, ValueError):
        return None


def _difficulty(item: dict) -> float:
    value = {"easy": -1.5, "medium": 0.0, "hard": 1.5}.get(item.get("tier_prior"), 0.0)
    if item.get("level") == "N5":
        value -= .5
    elif item.get("level") == "N4-hard":
        value += .5
    return value


def _posterior(rows: list[tuple[float, float, bool]], prior: float) -> tuple[float, float]:
    """Return logistic posterior MAP and Laplace standard deviation."""
    difficulties = np.asarray([row[0] for row in rows], dtype=float)
    weights = np.asarray([row[1] for row in rows], dtype=float)
    outcomes = np.asarray([row[2] for row in rows], dtype=float)
    theta = prior
    prior_precision = 1.0  # prior variance is 1
    for _ in range(20):
        probabilities = 1 / (1 + np.exp(-np.clip(theta - difficulties, -30, 30)))
        grad = -(theta - prior) * prior_precision + np.sum(weights * (outcomes - probabilities))
        precision = prior_precision + np.sum(weights * probabilities * (1 - probabilities))
        step = grad / precision
        theta += step
        if abs(step) < 1e-7:
            break
    probabilities = 1 / (1 + np.exp(-np.clip(theta - difficulties, -30, 30)))
    precision = prior_precision + np.sum(weights * probabilities * (1 - probabilities))
    return theta, 1 / math.sqrt(precision)


def fit(attempts: list[dict], items: dict | None = None, current_run_id: str | None = None) -> dict:
    """Recompute section posteriors from attempts; replay tag skills and item offsets."""
    items = items if items is not None else load_bank()[0]
    ordered = sorted(attempts, key=lambda x: x.get("ts", ""))
    section_rows = defaultdict(list)
    tag = defaultdict(float)
    tag_n = defaultdict(int)
    offsets = defaultdict(float)
    ns = defaultdict(int)
    nt = defaultdict(int)
    speeds = defaultdict(list)
    parsed_times = [_timestamp(a.get("ts")) for a in ordered]
    newest = max((t for t in parsed_times if t), default=None)

    # Cap only recent evidence, preserving older evidence and its recency decay.
    recent_totals = defaultdict(float)
    raw_weights = []
    for a, timestamp in zip(ordered, parsed_times):
        age_days = max(0.0, (newest - timestamp).total_seconds() / 86400) if newest and timestamp else 0.0
        weight = .5 ** (age_days / 14)
        if a.get("flag") == "guess":
            weight *= .5
        raw_weights.append(weight)
        item = items.get(a.get("item_id"), a.get("item", {}))
        section = item.get("section", a.get("section", "vocab"))
        if newest and timestamp and (newest - timestamp).total_seconds() <= 86400:
            recent_totals[section] += weight
    caps = {section: min(1.0, 40.0 / total) if total else 1.0 for section, total in recent_totals.items()}

    for a, raw_weight in zip(ordered, raw_weights):
        item_id = a.get("item_id", "")
        item = items.get(item_id, a.get("item", {}))
        section = item.get("section", a.get("section", "vocab"))
        prior = .4 if section == "listening" else .5
        base = _difficulty(item)
        difficulty = max(-1.0, min(1.0, base + offsets[item_id]))
        weight = raw_weight * caps.get(section, 1.0)
        correct = bool(a.get("correct")) and not a.get("timed_out")
        section_rows[section].append((difficulty, weight, correct))
        ns[section] += 1

        tags = item.get("tags", [])
        primary = next((t for t in tags if t.startswith(("grammar:", "word:", "kanji:", "skill:"))), None)
        q = primary or "tag:general"
        p = sigmoid(prior + tag[q] - difficulty)
        delta = (1 if correct else 0) - p
        if a.get("flag") == "guess":
            delta *= .5
        nt[q] += 1
        tag[q] += .5 / (1 + tag_n[q] / 5) * delta
        tag_n[q] += 1

        # A run's own outcomes cannot update the difficulty used to explain them.
        if not current_run_id or a.get("run_id") != current_run_id:
            offsets[item_id] = max(-1.0, min(1.0, offsets[item_id] - .15 * delta))
        if a.get("ms") is not None and item.get("mondai"):
            speeds[item["mondai"]].append(a["ms"])

    sections = {}
    for section in set(section_rows) | {"vocab", "grammar", "reading", "listening"}:
        prior = .4 if section == "listening" else .5
        theta, sd = _posterior(section_rows[section], prior)
        sections["sec:" + section] = {"theta": theta, "sd": sd, "n": ns[section]}
    skills = {k: data.copy() for k, data in sections.items()}
    skills.update({k: {"theta": v, "sd": 1 / math.sqrt(1 + nt[k] / 4), "n": nt[k]} for k, v in tag.items()})
    return {
        "skills": skills,
        "sections": sections,
        "item_b": {k: max(-1.0, min(1.0, _difficulty(items.get(k, {})) + v)) for k, v in offsets.items()},
        "speed": {k: {"median_ms": sorted(v[-50:])[len(v[-50:]) // 2], "target_ms": target_ms({"mondai": k, "tier_prior": "medium"})} for k, v in speeds.items()},
        "boxes": boxes(attempts, items),
    }


def get_theta(model: dict, section: str) -> float:
    return model.get("sections", {}).get("sec:" + section, {}).get("theta", .4 if section == "listening" else .5)
