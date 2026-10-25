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
    for n in range(3): items.append({"id":f"a{n}","section":"vocab","mondai":"kanji_reading","tier_prior":"easy","level":"N4-core","stem":f"【猫{n}】","options":["ねこ","いぬ","とり","うま"],"answer":1,"tags":[f"word:猫{n}"],"explanation_en":"cat","distractor_notes":{},"source":{"kind":"generated","ref":"test"},"verified":True})
    (folder/"tiny.json").write_text(json.dumps(items),encoding="utf-8")
    import server
    srv=ThreadingHTTPServer(("127.0.0.1",0),Handler); threading.Thread(target=srv.serve_forever,daemon=True).start()
    try:
        base=f"http://127.0.0.1:{srv.server_port}"
        with urllib.request.urlopen(base+"/api/status") as r: status=json.loads(r.read())
        with urllib.request.urlopen(base+"/api/run?section=vocab&n=3") as r: run=json.loads(r.read())
        assert len(run["items"])==3
        for item in run["items"]:
            req=urllib.request.Request(base+"/api/answer",data=json.dumps({"run_id":run["run_id"],"item_id":item["id"],"choice":1,"ms":2000,"flag":"none","timed_out":False}).encode(),headers={"Content-Type":"application/json"})
            urllib.request.urlopen(req).read()
        req=urllib.request.Request(base+"/api/finish",data=json.dumps({"run_id":run["run_id"]}).encode(),headers={"Content-Type":"application/json"})
        result=json.loads(urllib.request.urlopen(req).read())
        assert result["score"]==3
        assert result["p_pass_before"]==status["p_pass"]
        assert len(paths.ATTEMPTS.read_text().splitlines())==3
    finally: srv.shutdown()
