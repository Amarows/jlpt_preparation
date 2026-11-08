import json,threading,urllib.request,urllib.error
from http.server import ThreadingHTTPServer
from server import Handler

def _item(i,section,mondai):
    return {"id":i,"section":section,"mondai":mondai,"tier_prior":"medium","level":"N4-core","stem":i,"options":["a","b","c"] if mondai=="quick_response" else ["a","b","c","d"],"answer":1,"tags":[],"explanation_en":"x","source":{"kind":"book","ref":"t","author":"t","batch":"t"},"verified":True}

def _post(url,obj):
    return json.loads(urllib.request.urlopen(urllib.request.Request(url,data=json.dumps(obj).encode(),headers={"Content-Type":"application/json"})).read())

def test_mock_runs_in_parts_scores_and_joins_practice(monkeypatch,tmp_path):
    from engine import paths
    from engine.bank import load_bank
    import server
    monkeypatch.setattr(server,"BANKS",{})
    monkeypatch.setattr(paths,"HOME",tmp_path)
    (paths.BANK/"vocab").mkdir(parents=True)
    (paths.BANK/"vocab"/"practice.json").write_text(json.dumps([_item("p1","vocab","kanji_reading")]),encoding="utf-8")
    m=paths.BANK/"mocks"/"m1"; m.mkdir(parents=True)
    # Files are read alphabetically; the mock must still come out in exam order.
    (m/"listening.json").write_text(json.dumps([_item("l1","listening","quick_response")]),encoding="utf-8")
    (m/"grammar.json").write_text(json.dumps([_item("g1","grammar","sentence_composition"),_item("g0","grammar","grammar_form")]),encoding="utf-8")
    (m/"vocab.json").write_text(json.dumps([_item("v2","vocab","contextual"),_item("v1","vocab","kanji_reading")]),encoding="utf-8")
    (m/"mock.json").write_text(json.dumps({"id":"m1","title":"Mock 1","opens":"2026-01-01"}),encoding="utf-8")
    later=paths.BANK/"mocks"/"m2"; later.mkdir(); (later/"mock.json").write_text(json.dumps({"id":"m2","title":"Mock 2","opens":"2999-01-01"}),encoding="utf-8")
    assert set(load_bank()[0])=={"p1"}
    srv=ThreadingHTTPServer(("127.0.0.1",0),Handler); threading.Thread(target=srv.serve_forever,daemon=True).start()
    try:
        base=f"http://127.0.0.1:{srv.server_port}"
        listed={x["id"]:x["open"] for x in json.loads(urllib.request.urlopen(base+"/api/mocks").read())}
        assert listed=={"m1":True,"m2":False}
        try: urllib.request.urlopen(base+"/api/run?mode=mock&mock=m2"); assert False
        except urllib.error.HTTPError as e: assert e.code==403
        run=json.loads(urllib.request.urlopen(base+"/api/run?mode=mock&mock=m1").read())
        assert [x["id"] for x in run["items"]]==["v1","v2","g0","g1","l1"]
        assert [(p["part"],p["minutes"],p["count"]) for p in run["parts"]]==[("vocab",25,2),("grammar_reading",55,2),("listening",35,1)]
        for item in run["items"]:
            out=_post(base+"/api/answer",{"run_id":run["run_id"],"item_id":item["id"],"choice":1 if item["id"]!="g1" else 2,"ms":1000})
            assert "answer" not in out  # no feedback during a mock
        result=_post(base+"/api/finish",{"run_id":run["run_id"]})
        assert result["mock"]=={"lk":90,"listening":60,"total":150,"passed":True}
        assert json.loads((m/"mock.json").read_text(encoding="utf-8"))["taken"]
        assert {"v1","v2","g0","g1","l1"}<=set(load_bank()[0])
    finally: srv.shutdown()
