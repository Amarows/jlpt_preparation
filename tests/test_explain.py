import json,sys,threading,urllib.request
from pathlib import Path
from http.server import ThreadingHTTPServer
sys.path.insert(0,str(Path(__file__).resolve().parents[1]/"tools"))
from engine import explain, paths
from engine.explain import fingerprint, for_item, kana, plain
import explain_items

ITEM={"id":"g1","section":"grammar","mondai":"grammar_form","tier_prior":"easy","level":"N4-core","stem":"たくさん 勉強した（　　）、テストは よく なかったです。","options":["ので","から","と","のに"],"answer":4,"tags":["grammar:のに"],"explanation_en":"のに","distractor_notes":{},"source":{"kind":"generated","ref":"test"},"verified":True}
GOOD={"sentence":"たくさん {勉強|べんきょう}したのに、テストは よく なかったです。","translation_en":"Even though I studied a lot, the test went badly.",
      "options":[{"ruby":o,"en":"x"} for o in ITEM["options"]],"words":[{"w":"勉強する","r":"べんきょうする","en":"to study"}],"steps":["Unexpected result → のに."]}

class FakeReader:
    words={"勉強":{"べんきょう"}}
    def disagreements(self,ruby): return []

def test_ruby_helpers():
    s="{来週|らいしゅう}、{海|うみ}へ {行|い}きます"
    assert plain(s)=="来週、海へ 行きます" and kana(s)=="らいしゅう、うみへ いきます"

def test_check_accepts_a_good_entry():
    assert explain_items.check_one(ITEM,GOOD,"",FakeReader())==([],[])

def test_check_rejects_missing_furigana_wrong_text_and_made_up_quotes():
    bad={**GOOD,"sentence":"たくさん 勉強したので、テストは よく なかったです。"}
    hard,_=explain_items.check_one(ITEM,bad,"",FakeReader())
    assert any("kanji without furigana" in h for h in hard) and any("should be" in h for h in hard)
    reading={**ITEM,"section":"reading","mondai":"short_passage","stem":"どうしますか。","options":["a","b","c","d"],"answer":1}
    e={**GOOD,"sentence":"どうしますか。","options":[{"ruby":o,"en":"x"} for o in "abcd"],"evidence":[{"text":"学生課に 持って いく","ruby":"{学生課|がくせいか}に {持|も}って いく","en":"take it"}]}
    assert explain_items.check_one(reading,e,"レポートは 学生課に 持って いく こと。",FakeReader())[0]==[]
    hard,_=explain_items.check_one(reading,e,"レポートは 研究室に 持って いく こと。",FakeReader())
    assert any("exact one-line quote" in h for h in hard)

def test_served_only_for_the_item_version_it_was_written_for(monkeypatch,tmp_path):
    monkeypatch.setattr(paths,"HOME",tmp_path); explain._cache.clear(); (tmp_path/"data").mkdir()
    (tmp_path/"data"/"explain.json").write_text(json.dumps({"g1":{**GOOD,"for":fingerprint(ITEM)}},ensure_ascii=False),encoding="utf-8")
    assert for_item(ITEM)["sentence"]==GOOD["sentence"]
    changed={**ITEM,"answer":1}
    assert (for_item(changed) or {}).get("sentence") is None

def test_server_sends_explanation_only_after_the_answer(monkeypatch,tmp_path):
    monkeypatch.setattr(paths,"HOME",tmp_path)
    monkeypatch.setenv("JLPT_HOME",str(tmp_path)); explain._cache.clear()
    (paths.BANK/"grammar").mkdir(parents=True); (paths.BANK/"grammar"/"t.json").write_text(json.dumps([ITEM],ensure_ascii=False),encoding="utf-8")
    (paths.DATA/"explain.json").write_text(json.dumps({"g1":{**GOOD,"for":fingerprint(ITEM)}},ensure_ascii=False),encoding="utf-8")
    from server import Handler
    srv=ThreadingHTTPServer(("127.0.0.1",0),Handler); threading.Thread(target=srv.serve_forever,daemon=True).start()
    post=lambda path,body:json.loads(urllib.request.urlopen(urllib.request.Request(base+path,data=json.dumps(body).encode(),headers={"Content-Type":"application/json"})).read())
    try:
        base=f"http://127.0.0.1:{srv.server_port}"
        run=json.loads(urllib.request.urlopen(base+"/api/run?section=grammar&n=1").read())
        assert "explain" not in json.dumps(run,ensure_ascii=False) and "べんきょう" not in json.dumps(run,ensure_ascii=False)
        out=post("/api/answer",{"run_id":run["run_id"],"item_id":"g1","choice":1,"ms":1000})
        assert out["explain"]["translation_en"]==GOOD["translation_en"]
        assert post("/api/explain_feedback",{"item_id":"g1","choice":1})=={"ok":True}
        # "Still unclear" is kept apart from the answer log
        assert len(paths.ATTEMPTS.read_text(encoding="utf-8").splitlines())==1
        assert (paths.CONFIDENTIAL/"explain_feedback.jsonl").exists()
        assert post("/api/finish",{"run_id":run["run_id"]})["items"][0]["explain"]["sentence"]==GOOD["sentence"]
    finally: srv.shutdown()

def test_step_furigana_reuses_the_entry_readings():
    reader=explain_items.Reader()
    rubies=["{金曜日|きんようび}までに","{窓|まど}が{開|あ}いています"]
    assert reader.furigana("金曜日 + までに; 窓が 開いて",rubies)=="{金曜日|きんようび} + までに; {窓|まど}が {開|あ}いて"
    assert reader.furigana("{何|なに}か and 何か",[])=="{何|なに}か and {何|なに}か"
