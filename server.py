"""Small stdlib HTTP portal server."""
import json, os, threading, uuid, mimetypes
from datetime import datetime, timezone
from http.server import ThreadingHTTPServer, BaseHTTPRequestHandler
from http.cookies import CookieError, SimpleCookie
from urllib.parse import urlparse, parse_qs, unquote
from engine import paths, tracks
from engine.bank import load_bank
from engine.explain import explanations, for_item
from engine.leitner import target_ms
from engine.mock import assemble, mark_taken, mocks, score
from engine.simulate import simulate

LOCK=threading.Lock(); RUNS={}; BANKS={}
OPEN={"/api/learners","/api/login","/api/logout"}
HIDDEN={"answer","distractor_notes","script"}
COOKIE="learner={}; Path=/; Max-Age={}; SameSite=Lax; HttpOnly"
def bank():
    if paths.BANK not in BANKS: BANKS[paths.BANK]=load_bank()
    return BANKS[paths.BANK]
def who(handler):
    try: jar=SimpleCookie(handler.headers.get("Cookie",""))
    except CookieError: return None
    return jar["learner"].value if "learner" in jar else None
def learner_id(handler):
    rows=paths.learners(); chosen=who(handler)
    if any(r["id"]==chosen for r in rows): return chosen
    return rows[0]["id"] if len(rows)==1 else None
def profile(row): return {k:row[k] for k in ("id","name","track","ui","explain")}
def mine(rid):
    run=RUNS.get(rid)
    return run if run and run["learner"]==paths.learner()["id"] else None
def append(path,obj):
    path.parent.mkdir(parents=True,exist_ok=True)
    with LOCK, path.open("a",encoding="utf-8") as f: f.write(json.dumps(obj,ensure_ascii=False)+"\n")
def attempts():
    if not paths.ATTEMPTS.exists(): return []
    return [json.loads(x) for x in paths.ATTEMPTS.read_text(encoding="utf-8").splitlines() if x.strip()]
class Handler(BaseHTTPRequestHandler):
    def log_message(self,*args): pass
    def send_json(self,obj,status=200,cookie=None):
        raw=json.dumps(obj,ensure_ascii=False).encode(); self.send_response(status); self.send_header("Content-Type","application/json; charset=utf-8"); self.send_header("Content-Length",str(len(raw)))
        if cookie: self.send_header("Set-Cookie",cookie)
        self.end_headers(); self.wfile.write(raw)
    def body(self): return json.loads(self.rfile.read(int(self.headers.get("Content-Length",0)) or 0))
    def route(self,fn):
        path=urlparse(self.path).path
        if path in OPEN or not path.startswith(("/api/","/audio/")): return fn()
        lid=learner_id(self)
        if lid is None: return self.send_json({"error":"login required"},401)
        with paths.as_learner(lid): return fn()
    def do_GET(self): self.route(self.get)
    def get(self):
        u=urlparse(self.path); q=parse_qs(u.query)
        if u.path=="/api/learners": return self.send_json([{k:r[k] for k in ("id","name","ui")} for r in paths.learners()])
        if u.path=="/api/me": return self.send_json({"learner":profile(paths.learner()),"track":tracks.summary()})
        if u.path=="/api/status": return self.send_json(simulate())
        if u.path=="/api/report":
            from engine.report import build_report
            return self.send_json(build_report(bank()[0]))
        if u.path=="/api/mocks": return self.send_json(mocks())
        if u.path=="/api/run":
            from engine.select import build_run
            mode=q.get("mode",["practice"])[0]; section=q.get("section",["mixed"])[0]; n=max(1,min(100,int(q.get("n",[20])[0]))); mock_id=None
            if mode=="mock":
                mock_id=q.get("mock",[""])[0]; meta=next((m for m in mocks() if m["id"]==mock_id),None)
                if not meta or not meta["open"]: return self.send_json({"error":"This mock is not open yet."},403)
                data={**assemble(mock_id),"mode":mode,"time_limit_ms":None}; section="mock"
            else: data=build_run(mode,section,n,seed=uuid.uuid4().int)
            rid="r-"+uuid.uuid4().hex[:12]; originals=data["items"]
            public=[]
            for item in originals: public.append({**{k:v for k,v in item.items() if k not in HIDDEN and not k.startswith("explanation_")},"target_ms":target_ms(item)})
            try: baseline=json.loads(paths.MODEL_STATE.read_text(encoding="utf-8"))["p_pass"]
            except (OSError, ValueError, KeyError): baseline=simulate(write=False)["p_pass"]
            RUNS[rid]={"start":datetime.now(timezone.utc).isoformat(),"mode":mode,"section":section,"items":{x["id"]:x for x in originals},"answers":{},"time_limit_ms":data["time_limit_ms"],"p_pass_before":baseline,"mock_id":mock_id,"learner":paths.learner()["id"]}
            return self.send_json({"run_id":rid,"mode":mode,"time_limit_ms":data["time_limit_ms"],"parts":data.get("parts"),"items":public,"passages":data["passages"]})
        if u.path=="/" or u.path.startswith("/web/"):
            rel="index.html" if u.path=="/" else unquote(u.path[5:]); path=(paths.REPO/"web"/rel).resolve()
            if paths.REPO/"web" not in path.parents and path!=paths.REPO/"web": return self.send_error(403)
        elif u.path.startswith("/audio/"):
            root=paths.HOME/"audio"; path=(root/unquote(u.path[7:])).resolve()
            if root not in path.parents: return self.send_error(404)
        else: return self.send_error(404)
        if not path.is_file(): return self.send_error(404)
        raw=path.read_bytes(); status=200; first,last=0,len(raw)-1
        # Browsers can only seek inside an MP3 (listening clips start mid-file) when byte ranges are served.
        rng=self.headers.get("Range","")
        if rng.startswith("bytes="):
            a,_,b=rng[6:].split(",")[0].partition("-")
            first,last=(len(raw)-int(b),len(raw)-1) if not a else (int(a),min(int(b),len(raw)-1) if b else len(raw)-1)
            if first>last or first>=len(raw): self.send_response(416); self.send_header("Content-Range",f"bytes */{len(raw)}"); self.end_headers(); return
            status=206
        self.send_response(status); self.send_header("Content-Type",mimetypes.guess_type(path.name)[0] or "application/octet-stream"); self.send_header("Accept-Ranges","bytes")
        if status==206: self.send_header("Content-Range",f"bytes {first}-{last}/{len(raw)}")
        self.send_header("Content-Length",str(last-first+1)); self.end_headers(); self.wfile.write(raw[first:last+1])
    def do_POST(self):
        try: data=self.body()
        except Exception: return self.send_json({"error":"invalid JSON"},400)
        self.route(lambda: self.post(data if isinstance(data,dict) else {}))
    def post(self,data):
        if self.path=="/api/login":
            row=paths.find(data.get("learner"))
            if not row: return self.send_json({"error":"unknown learner"},404)
            return self.send_json({"ok":True,"learner":profile(row)},cookie=COOKIE.format(row["id"],31536000))
        if self.path=="/api/logout": return self.send_json({"ok":True},cookie=COOKIE.format("",0))
        if self.path=="/api/answer":
            run=mine(data.get("run_id")); item=run and run["items"].get(data.get("item_id"))
            if not item: return self.send_json({"error":"unknown run/item"},404)
            if item["id"] in run["answers"]: return self.send_json({"ok":True})
            choice=data.get("choice"); correct=choice==item["answer"] and not data.get("timed_out")
            a={"ts":datetime.now().astimezone().isoformat(),"run_id":data["run_id"],"item_id":item["id"],"choice":choice,"correct":correct,"ms":data.get("ms"),"flag":data.get("flag") or "none","mode":run["mode"],"timed_out":bool(data.get("timed_out"))}
            if run["section"]=="mistakes": a["review"]=True
            append(paths.ATTEMPTS,a); run["answers"][item["id"]]={**a,"item":item}; out={"ok":True}
            if run["mode"]=="practice": out.update({"answer":item["answer"],"explanation_en":item.get("explanation_en"),**explanations(item),"distractor_note":item.get("distractor_notes",{}).get(str(choice)),"script":item.get("script"),"explain":for_item(item)})
            return self.send_json(out)
        if self.path=="/api/finish":
            rid=data.get("run_id"); run=mine(rid)
            if not run: return self.send_json({"error":"unknown run"},404)
            before=run["p_pass_before"]; rows=list(run["answers"].values()); correct=sum(bool(x["correct"]) for x in rows); total_ms=sum(x.get("ms") or 0 for x in rows)
            mock=None
            if run.get("mock_id"):
                # Score first: marking the mock taken releases its items into the bank the model reads.
                mock=score(list(run["items"].values()),{i for i,x in run["answers"].items() if x["correct"]}); mark_taken(run["mock_id"],mock)
                BANKS.pop(paths.BANK,None)
            after=simulate(write=True,current_run_id=rid,record_run=True)["p_pass"]; end=datetime.now().astimezone().isoformat()
            append(paths.RUNS,{"run_id":rid,"start":run["start"],"end":end,"mode":run["mode"],"section":run["section"],"n":len(run["items"]),"correct":correct,"total_ms":total_ms,"p_pass_before":before,"p_pass_after":after,**({"mock_id":run["mock_id"],"mock":mock} if mock else {})})
            result=[]
            for item in run["items"].values():
                a=run["answers"].get(item["id"],{}); choice=a.get("choice"); result.append({"stem":item["stem"],"options":item["options"],"choice":choice,"answer":item["answer"],"correct":a.get("correct",False),"ms":a.get("ms"),"slow":bool(a.get("ms") and a["ms"]>target_ms(item)),"flag":a.get("flag","none"),"explanation_en":item.get("explanation_en"),**explanations(item),"distractor_note":item.get("distractor_notes",{}).get(str(choice)),"script":item.get("script"),"explain":for_item(item),"item_id":item["id"],"section":item["section"]})
            return self.send_json({"score":correct,"total_ms":total_ms,"p_pass_before":before,"p_pass_after":after,"mock":mock,"items":result})
        if self.path=="/api/explain_feedback":
            # "Still unclear" on an explanation: kept apart from attempts, so it never touches scores.
            if not isinstance(data.get("item_id"),str): return self.send_json({"error":"item_id required"},400)
            append(paths.CONFIDENTIAL/"explain_feedback.jsonl",{"ts":datetime.now().astimezone().isoformat(),"item_id":data["item_id"],"run_id":data.get("run_id"),"choice":data.get("choice")})
            return self.send_json({"ok":True})
        self.send_error(404)

def serve(port=None):
    ThreadingHTTPServer(("0.0.0.0",int(port or os.getenv("JLPT_PORT",8080))),Handler).serve_forever()
if __name__=="__main__": serve()
