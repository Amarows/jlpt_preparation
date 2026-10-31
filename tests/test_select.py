from engine import paths
from engine.select import build_run

def test_run_has_no_duplicate_items():
    run=build_run("practice","mixed",20,seed=5)
    ids=[x["id"] for x in run["items"]]
    assert len(ids)==len(set(ids))
    assert all(x.get("verified") for x in run["items"])

def test_right_answers_rest_and_mix_follows_blueprint(monkeypatch):
    from datetime import datetime,timedelta,timezone
    from engine import select
    item=lambda i,m,s="vocab":{"id":i,"section":s,"mondai":m,"tier_prior":"medium","level":"N4-core","stem":i,"options":["a","b","c","d"],"answer":1,"tags":[],"verified":True}
    items={f"k{n}":item(f"k{n}","kanji_reading") for n in range(40)}
    items.update({f"c{n}":item(f"c{n}","contextual") for n in range(40)})
    yesterday=(datetime.now(timezone.utc)-timedelta(days=1)).isoformat()
    rows=[{"ts":yesterday,"item_id":"c0","choice":1,"correct":True,"ms":1000},{"ts":yesterday,"item_id":"c1","choice":2,"correct":False,"ms":1000}]
    monkeypatch.setattr(select,"load_bank",lambda:(items,{})); monkeypatch.setattr(select,"read_attempts",lambda:rows)
    ids=[x["id"] for x in select.build_run("practice","vocab",20,seed=2)["items"]]
    assert "c0" not in ids and "c1" in ids
    # The blueprint has 7 kanji_reading to 8 contextual questions, so a run is about half and half, not mostly kanji.
    assert 8<=sum(i.startswith("k") for i in ids)<=11
