import json,threading,urllib.request,tempfile
from pathlib import Path
from http.server import ThreadingHTTPServer
from server import Handler,RUNS

def test_server_run_answer_finish(monkeypatch):
    from engine import paths
    tmp_path=Path(tempfile.mkdtemp(dir=Path(__file__).resolve().parents[1]))
    monkeypatch.setenv("JLPT_HOME",str(tmp_path))
    monkeypatch.setattr(paths,"HOME",tmp_path); monkeypatch.setattr(paths,"BANK",tmp_path/"data"/"bank"); monkeypatch.setattr(paths,"CONFIDENTIAL",tmp_path/"confidential"); monkeypatch.setattr(paths,"ATTEMPTS",tmp_path/"confidential"/"attempts.jsonl"); monkeypatch.setattr(paths,"RUNS",tmp_path/"confidential"/"runs.jsonl"); monkeypatch.setattr(paths,"MODEL_STATE",tmp_path/"confidential"/"model_state.json")
    folder=paths.BANK/"vocab"; folder.mkdir(parents=True)
    items=[]
    for n in range(3): items.append({"id":f"a{n}","section":"vocab","mondai":"kanji_reading","tier_prior":"easy","level":"N4-core","stem":f"【猫{n}】","options":["ねこ","いぬ","とり","うま"],"answer":1,"tags":[f"word:猫{n}"],"explanation_en":"cat","distractor_notes":{},"script":"M：ねこ","source":{"kind":"generated","ref":"test"},"verified":True})
    (folder/"tiny.json").write_text(json.dumps(items),encoding="utf-8")
    import server
    srv=ThreadingHTTPServer(("127.0.0.1",0),Handler); threading.Thread(target=srv.serve_forever,daemon=True).start()
    try:
        base=f"http://127.0.0.1:{srv.server_port}"
        with urllib.request.urlopen(base+"/api/status") as r: status=json.loads(r.read())
        with urllib.request.urlopen(base+"/api/run?section=vocab&n=3") as r: run=json.loads(r.read())
        assert len(run["items"])==3
        # The transcript is held back until the question is answered
        assert all("script" not in item for item in run["items"])
        for item in run["items"]:
            req=urllib.request.Request(base+"/api/answer",data=json.dumps({"run_id":run["run_id"],"item_id":item["id"],"choice":1,"ms":2000,"flag":"none","timed_out":False}).encode(),headers={"Content-Type":"application/json"})
            assert json.loads(urllib.request.urlopen(req).read())["script"]=="M：ねこ"
        req=urllib.request.Request(base+"/api/finish",data=json.dumps({"run_id":run["run_id"]}).encode(),headers={"Content-Type":"application/json"})
        result=json.loads(urllib.request.urlopen(req).read())
        assert result["score"]==3
        assert result["p_pass_before"]==status["p_pass"]
        assert len(paths.ATTEMPTS.read_text().splitlines())==3
        with urllib.request.urlopen(base+"/api/report") as r: report=json.loads(r.read())
        assert len(report["progress"])==1 and report["mistakes"]==[]
        assert {"section":"vocab","correct":3,"total":3} in report["sections"]
    finally: srv.shutdown()

def test_report_lists_open_mistakes_latest_first(monkeypatch,tmp_path):
    from engine import paths
    from engine.report import build_report
    monkeypatch.setattr(paths,"ATTEMPTS",tmp_path/"attempts.jsonl"); monkeypatch.setattr(paths,"RUNS",tmp_path/"runs.jsonl")
    item=lambda i:{"id":i,"section":"grammar","stem":i,"options":["a","b","c","d"],"answer":2}
    items={i:item(i) for i in ("g1","g2","g3")}; items["g3"]["revised"]="2026-10-24"
    rows=[("g1",21,1),("g2",22,3),("g1",23,2),("g3",23,1),("g2",24,None)]
    paths.ATTEMPTS.write_text("\n".join(json.dumps({"ts":f"2026-10-{d}T10:00:00+00:00","item_id":i,"choice":c,"correct":c==2}) for i,d,c in rows),encoding="utf-8")
    from datetime import datetime,timezone
    report=build_report(items,days=3,now=datetime(2026,10,25,tzinfo=timezone.utc))
    # g1 was corrected later; g3's attempt predates its revision
    assert [(m["stem"],m["choice"],m["answer"]) for m in report["mistakes"]]==[("g2",None,"b")]
    assert {"section":"grammar","correct":1,"total":3} in report["sections"]

def test_mistakes_run_and_review_attempts(monkeypatch,tmp_path):
    from engine import paths, select
    from engine.model import fit
    items={f"g{n}":{"id":f"g{n}","section":"grammar","mondai":"grammar_form","tier_prior":"easy","level":"N4-core","stem":"S","options":["a","b","c","d"],"answer":1,"tags":["grammar:x"],"verified":True} for n in range(4)}
    rows=[{"ts":"2026-10-20T10:00:00+00:00","item_id":i,"choice":2,"correct":False} for i in items]+[{"ts":"2026-10-21T10:00:00+00:00","item_id":"g0","choice":1,"correct":True,"review":True}]
    monkeypatch.setattr(select,"load_bank",lambda:(items,{})); monkeypatch.setattr(select,"read_attempts",lambda:rows)
    run=select.build_run("practice","mistakes",10,seed=3)
    assert sorted(x["id"] for x in run["items"])==["g1","g2","g3"]
    assert fit(rows,items)["sections"]["sec:grammar"]["n"]==4
