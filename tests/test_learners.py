import json
from pathlib import Path

import pytest

from tests import golden_learners as g

FIXTURE_ATTEMPTS = len(Path(__file__).with_name("golden_n4_fixture").joinpath("attempts.jsonl").read_text(encoding="utf-8").splitlines())


@pytest.fixture(scope="module")
def flow():
    return g.api()


def _calls(flow, path, learner):
    return [c for c in flow["calls"] if c["request"].startswith(path) and c["as"] == learner]


def test_attempts_stay_with_their_learner(flow):
    assert flow["files"]["learners/yoko/attempts.jsonl"] == 6
    assert flow["files"]["confidential/attempts.jsonl"] == FIXTURE_ATTEMPTS + 3


def test_runs_of_another_learner_are_rejected(flow):
    assert [c["status"] for c in _calls(flow, "/api/finish", "anna")] == [404, 200]
    assert [c["status"] for c in _calls(flow, "/api/finish", "yoko")] == [200, 404]
    assert [c["status"] for c in _calls(flow, "/api/answer", "anna")][0] == 404


def test_each_learner_sees_only_their_track(flow):
    yoko = _calls(flow, "/api/run", "yoko")[0]["body"]["items"]
    anna = _calls(flow, "/api/run", "anna")[0]["body"]["items"]
    assert {x["section"] for x in yoko} <= {"words", "phrases"}
    assert {x["section"] for x in anna} == {"vocab"}


def test_explanations_only_after_answering(flow):
    for c in _calls(flow, "/api/run", "yoko") + _calls(flow, "/api/run", "anna"):
        assert not any(k.startswith("explanation_") or k == "answer" for x in c["body"]["items"] for k in x)
    assert all(c["body"]["explanation_ja"] for c in _calls(flow, "/api/answer", "yoko"))


def test_without_a_chosen_learner_the_api_answers_401(flow):
    assert [c["status"] for c in flow["calls"] if c["as"] in (None, "nobody") and c["request"] in ("/api/status", "/api/me")] == [401, 401, 401]


def test_a_single_learner_needs_no_login():
    import server
    with g.two_learners(g.LEARNERS[1:]):
        handler = type("H", (), {"headers": {}})()
        assert server.learner_id(handler) == "yoko"


@pytest.mark.parametrize("name", sorted(g.INVALID))
def test_invalid_learners_json_is_rejected(name):
    from engine import paths
    with g.two_learners(g.INVALID[name]):
        with pytest.raises(ValueError):
            paths.learners()


@pytest.mark.parametrize("path", ["/audio/../confidential/attempts.jsonl", "/audio/%2e%2e/confidential/attempts.jsonl", "/audio/..%2flearners.json"])
def test_audio_cannot_reach_outside_the_audio_folder(path):
    import http.client
    import threading
    from http.server import ThreadingHTTPServer
    import server
    with g.two_learners():
        srv = ThreadingHTTPServer(("127.0.0.1", 0), server.Handler)
        threading.Thread(target=srv.serve_forever, daemon=True).start()
        try:
            def get(p):
                c = http.client.HTTPConnection("127.0.0.1", srv.server_port)
                c.request("GET", p, headers={"Cookie": "learner=yoko"})
                return c.getresponse().status
            assert get("/audio/clip.mp3") == 200
            assert get(path) == 404
        finally:
            srv.shutdown()
            srv.server_close()


def test_example_config_is_valid():
    from engine import paths
    rows = json.loads((Path(__file__).resolve().parents[1] / "learners.example.json").read_text(encoding="utf-8"))["learners"]
    with g.two_learners(rows):
        assert [r["id"] for r in paths.learners()] == ["anna", "yoko"]
