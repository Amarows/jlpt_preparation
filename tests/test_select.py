from engine import paths
from engine.select import build_run

def test_run_has_no_duplicate_items():
    run=build_run("practice","mixed",20,seed=5)
    ids=[x["id"] for x in run["items"]]
    assert len(ids)==len(set(ids))
    assert all(x.get("verified") for x in run["items"])
