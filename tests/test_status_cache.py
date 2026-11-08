import json
import os
import time

from tests import golden_n4 as g


def test_status_is_cached_until_attempts_bank_state_or_day_change(monkeypatch):
    from engine import simulate as sim
    from engine import paths
    sim._status.clear()
    with g.portal():
        calls = []
        real = sim.simulate
        monkeypatch.setattr(sim, "simulate", lambda *a, **k: calls.append(k) or real(*a, **k))
        first = sim.status()
        assert sim.status() is first and len(calls) == 1
        assert first == real(write=False)
        with paths.ATTEMPTS.open("a", encoding="utf-8") as f:
            f.write(json.dumps({"ts": g.NOW.isoformat(), "item_id": "nope", "correct": True}) + "\n")
        sim.status()
        assert len(calls) == 2
        bank = next(paths.BANK.rglob("*.json"))
        os.utime(bank, ns=(time.time_ns(), time.time_ns() + 10 ** 9))
        sim.status()
        assert len(calls) == 3
        real(write=True, record_run=True)
        sim.status()
        assert len(calls) == 4
        with monkeypatch.context() as m:
            m.setattr(sim, "date", type("Later", (g.FixedDate,), {"today": classmethod(lambda c: g.FixedDate(2026, 11, 9))}))
            sim.status()
            assert len(calls) == 5
            assert sim.status() is sim.status() and len(calls) == 5
