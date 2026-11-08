import json
import shutil
import tempfile
from contextlib import contextmanager
from datetime import timedelta
from pathlib import Path

from tests.golden_n4 import NOW, FixedDate, _patched


def _item(i, section, mondai, level="B2"):
    return {"id": i, "section": section, "mondai": mondai, "tier_prior": "medium", "level": level, "stem": i, "options": ["a", "b", "c", "d"],
            "answer": 1, "tags": [], "explanation_ja": "x", "source": {"kind": "book", "ref": "fixture"}, "verified": True}


ITEMS = ([_item(f"le-{k}", "lesen", "lesen") for k in range(6)] + [_item(f"ho-{k}", "hoeren", "hoeren") for k in range(6)]
         + [_item(f"wo-{k}", "words", "meaning_choice", "B1") for k in range(4)])
SCENARIOS = {
    "prior": [],
    "training_only": [(f"wo-{k % 4}", True) for k in range(40)],
    "receptive_strong": [(f"le-{k % 6}", k % 6 != 0) for k in range(30)] + [(f"ho-{k % 6}", k % 3 != 0) for k in range(30)],
    "receptive_weak": [(f"le-{k % 6}", k % 3 == 0) for k in range(30)] + [(f"ho-{k % 6}", k % 4 == 0) for k in range(30)],
}


@contextmanager
def yoko():
    from engine import paths, simulate
    tmp = Path(tempfile.mkdtemp()).resolve()
    try:
        (tmp / "learners.json").write_text(json.dumps({"learners": [{"id": "yoko", "track": "de-work", "ui": "ja", "explain": "ja"}]}), encoding="utf-8")
        bank = tmp / "data" / "tracks" / "de-work" / "bank"
        bank.mkdir(parents=True)
        (bank / "fixture.json").write_text(json.dumps(ITEMS), encoding="utf-8")
        with _patched([(paths, "HOME", tmp), (simulate, "date", FixedDate)]), paths.as_learner("yoko"):
            yield tmp
    finally:
        shutil.rmtree(tmp, ignore_errors=True)


def b2(scenario):
    from engine import paths
    from engine.simulate import simulate
    with yoko():
        rows = [{"ts": (NOW - timedelta(minutes=len(SCENARIOS[scenario]) - k)).isoformat(), "item_id": i, "correct": ok, "ms": 20000, "run_id": "r-1"}
                for k, (i, ok) in enumerate(SCENARIOS[scenario])]
        paths.ATTEMPTS.parent.mkdir(parents=True, exist_ok=True)
        paths.ATTEMPTS.write_text("".join(json.dumps(r) + "\n" for r in rows), encoding="utf-8")
        s = simulate(write=False)
        return {"p_pass": s["p_pass"], "modules": {k[2:-8]: v for k, v in s.items() if k.endswith("_section")}, "exp_score": s["exp_score"],
                "sections": {k: v for k, v in s["skills"].items() if k.startswith("sec:")}, "days_left": s["days_left"]}
