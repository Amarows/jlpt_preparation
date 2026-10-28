"""Small stdlib HTTP portal server."""
import json, os, threading, uuid, mimetypes
from datetime import datetime, timezone
from http.server import ThreadingHTTPServer, BaseHTTPRequestHandler
from urllib.parse import urlparse, parse_qs, unquote
from engine import paths
from engine.bank import load_bank
from engine.leitner import target_ms
from engine.simulate import simulate

LOCK=threading.Lock(); RUNS={}; ITEMS={}; PASSAGES={}
def append(path,obj):
    path.parent.mkdir(parents=True,exist_ok=True)
    with LOCK, path.open("a",encoding="utf-8") as f: f.write(json.dumps(obj,ensure_ascii=False)+"\n")
def attempts():
    if not paths.ATTEMPTS.exists(): return []
    return [json.loads(x) for x in paths.ATTEMPTS.read_text(encoding="utf-8").splitlines() if x.strip()]
class Handler(BaseHTTPRequestHandler):
    def log_message(self,*args): pass
    def send_json(self,obj,status=200):
        raw=json.dumps(obj,ensure_ascii=False).encode(); self.send_response(status); self.send_header("Content-Type","application/json; charset=utf-8"); self.send_header("Content-Length",str(len(raw))); self.end_headers(); self.wfile.write(raw)
    def body(self): return json.loads(self.rfile.read(int(self.headers.get("Content-Length",0)) or 0))
    def do_GET(self):
        u=urlparse(self.path); q=parse_qs(u.query)
        if u.path=="/api/status": return self.send_json(simulate())
        if u.path=="/api/report":
            from engine.report import build_report
            return self.send_json(build_report(ITEMS or load_bank()[0]))
        if u.path=="/api/run":
            from engine.select import build_run
            mode=q.get("mode",["practice"])[0]; section=q.get("section",["mixed"])[0]; n=max(1,min(100,int(q.get("n",[20])[0])))
            data=build_run(mode,section,n,seed=uuid.uuid4().int); rid="r-"+uuid.uuid4().hex[:12]; originals=data["items"]
            public=[]
            for item in originals: public.append({**{k:v for k,v in item.items() if k not in {"answer","explanation_en","distractor_notes"}},"target_ms":target_ms(item)})
            try: baseline=json.loads(paths.MODEL_STATE.read_text(encoding="utf-8"))["p_pass"]
            except (OSError, ValueError, KeyError): baseline=simulate(write=False)["p_pass"]
            RUNS[rid]={"start":datetime.now(timezone.utc).isoformat(),"mode":mode,"section":section,"items":{x["id"]:x for x in originals},"answers":{},"time_limit_ms":data["time_limit_ms"],"p_pass_before":baseline}
            return self.send_json({"run_id":rid,"mode":mode,"time_limit_ms":data["time_limit_ms"],"items":public,"passages":data["passages"]})
        if u.path=="/" or u.path.startswith("/web/"):
            rel="index.html" if u.path=="/" else unquote(u.path[5:]); path=(paths.REPO/"web"/rel).resolve()
            if paths.REPO/"web" not in path.parents and path!=paths.REPO/"web": return self.send_error(403)
        elif u.path.startswith("/audio/"): path=paths.under_home(u.path.lstrip("/"))
        else: return self.send_error(404)
        if not path.is_file(): return self.send_error(404)
        raw=path.read_bytes(); self.send_response(200); self.send_header("Content-Type",mimetypes.guess_type(path.name)[0] or "application/octet-stream"); self.send_header("Content-Length",str(len(raw))); self.end_headers(); self.wfile.write(raw)
    def do_POST(self):
        try: data=self.body()
        except Exception: return self.send_json({"error":"invalid JSON"},400)
        if self.path=="/api/answer":
            run=RUNS.get(data.get("run_id")); item=run and run["items"].get(data.get("item_id"))
            if not item: return self.send_json({"error":"unknown run/item"},404)
            if item["id"] in run["answers"]: return self.send_json({"ok":True})
            choice=data.get("choice"); correct=choice==item["answer"] and not data.get("timed_out")
            a={"ts":datetime.now().astimezone().isoformat(),"run_id":data["run_id"],"item_id":item["id"],"choice":choice,"correct":correct,"ms":data.get("ms"),"flag":data.get("flag") or "none","mode":run["mode"],"timed_out":bool(data.get("timed_out"))}
            if run["section"]=="mistakes": a["review"]=True
            append(paths.ATTEMPTS,a); run["answers"][item["id"]]={**a,"item":item}; out={"ok":True}
            if run["mode"]=="practice": out.update({"answer":item["answer"],"explanation_en":item.get("explanation_en"),"distractor_note":item.get("distractor_notes",{}).get(str(choice))})
            return self.send_json(out)
        if self.path=="/api/finish":
            rid=data.get("run_id"); run=RUNS.get(rid)
            if not run: return self.send_json({"error":"unknown run"},404)
            before=run["p_pass_before"]; rows=list(run["answers"].values()); correct=sum(bool(x["correct"]) for x in rows); total_ms=sum(x.get("ms") or 0 for x in rows)
            after=simulate(write=True,current_run_id=rid,record_run=True)["p_pass"]; end=datetime.now().astimezone().isoformat()
            append(paths.RUNS,{"run_id":rid,"start":run["start"],"end":end,"mode":run["mode"],"section":run["section"],"n":len(run["items"]),"correct":correct,"total_ms":total_ms,"p_pass_before":before,"p_pass_after":after})
            result=[]
            for item in run["items"].values():
                a=run["answers"].get(item["id"],{}); choice=a.get("choice"); result.append({"stem":item["stem"],"options":item["options"],"choice":choice,"answer":item["answer"],"correct":a.get("correct",False),"ms":a.get("ms"),"slow":bool(a.get("ms") and a["ms"]>target_ms(item)),"flag":a.get("flag","none"),"explanation_en":item.get("explanation_en"),"distractor_note":item.get("distractor_notes",{}).get(str(choice))})
            return self.send_json({"score":correct,"total_ms":total_ms,"p_pass_before":before,"p_pass_after":after,"items":result})
        self.send_error(404)

def serve(port=None):
    global ITEMS,PASSAGES
    ITEMS,PASSAGES=load_bank(); ThreadingHTTPServer(("0.0.0.0",int(port or os.getenv("JLPT_PORT",8080))),Handler).serve_forever()
if __name__=="__main__": serve()
