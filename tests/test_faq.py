import inspect
import json
import re
from pathlib import Path

REPO = Path(__file__).resolve().parents[1]
PAGE = (REPO / "web" / "faq.html").read_text(encoding="utf-8")


def section(track: str) -> str:
    return re.search(rf'<section class="panel" data-track="{track}">(.*?)</section>', PAGE, re.S).group(1)


def track(track_id: str) -> dict:
    return json.loads((REPO / "tracks" / track_id / "track.json").read_text(encoding="utf-8"))


def test_every_track_has_a_section():
    assert sorted(re.findall(r'data-track="([\w-]+)"', PAGE)) == sorted(p.name for p in (REPO / "tracks").iterdir() if (p / "track.json").is_file())


def test_simulation_numbers_match_the_engine():
    from engine import simulate
    source = inspect.getsource(simulate.simulate)
    assert inspect.signature(simulate.simulate).parameters["draws"].default == 10000
    assert "range(0,draws,500)" in source and "int(.1*len(batches))" in source and "int(.9*len(batches))" in source
    assert "ema_history[-3]>.01" in source and "ema_history[-3]<-.01" in source
    for t in ("de-work", "jlpt-n4"):
        text = section(t)
        assert "10,000" in text and "500" in text and "three runs earlier" in text and "1 point" in text


def test_goethe_b2_rules_match_the_track():
    t, text = track("de-work"), section("de-work")
    exam = t["exam"]
    assert [s["id"] for s in exam["sections"]] == ["lesen", "hoeren", "schreiben", "sprechen"]
    assert "Lesen, Hören, Schreiben and Sprechen" in text
    assert {(s["max"], s["min"]) for s in exam["scores"]} == {(100, 60)} and exam["total_min"] is None
    assert "0–100 and needs at least 60" in text and "there is no total" in text
    priors = {s["id"]: (s["prior"], s["prior_sd"]) for s in exam["sections"]}
    assert priors["schreiben"][0] < exam["levels"]["B1"] < exam["levels"]["B2"] and priors["schreiben"][1] > priors["lesen"][1]
    assert "a little below B1 and with wide uncertainty" in text
    assert {s["id"] for s in t["training"]} == {"words", "phrases"} and "does not change P(pass)" in text
    assert f'{t["daily_target"]} a day' in text and f'compares with {t["daily_target"]} for each weekday' in text
    assert t["features"] == [] and "Drill and Timed runs exist only on the JLPT track" in text
    assert exam["title"] == "Goethe-Zertifikat B2" and '<span data-fill="exam">Goethe-Zertifikat B2</span>' in text


def test_unit_states_match_the_engine():
    from engine import units
    text = section("de-work")
    assert units.STATES == ("not_started", "learning", "practised", "done")
    for name in ("Not started", "Learning", "Practised", "Done"):
        assert f"<strong>{name}</strong>" in text
    assert "on two different days, and your latest answer to each is correct" in text


def test_jlpt_rules_match_the_track():
    t, text = track("jlpt-n4"), section("jlpt-n4")
    scores = {s["id"]: (s["min"], s["max"]) for s in t["exam"]["scores"]}
    assert scores == {"lk": (38, 120), "listening": (19, 60)} and t["exam"]["total_min"] == 90
    assert "38/120" in text and "19/60" in text and "90/180" in text
    assert [p["minutes"] for p in t["exam"]["parts"]] == [25, 55, 35] and "(25, 55 and 35 minutes)" in text
    assert f'{t["daily_target"]} questions a day' in text
    assert t["features"] == ["drill", "timed"]


def test_flags_match_the_model():
    from engine import model, select
    assert 'a.get("flag") == "guess"' in inspect.getsource(model.fit) and "weight *= .5" in inspect.getsource(model.fit)
    assert 'last.get("flag")=="unclear"' in inspect.getsource(select.build_run)
    assert "unclear >= 2" in (REPO / "engine" / "health.py").read_text(encoding="utf-8")
    for t in ("de-work", "jlpt-n4"):
        assert "half as much" in section(t) and "Unclear twice is flagged for Alex" in section(t)
