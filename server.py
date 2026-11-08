"""Small stdlib HTTP portal server."""
import json, os, sys, threading, time, traceback, uuid, mimetypes, secrets
from datetime import datetime, timezone
from http.server import ThreadingHTTPServer, BaseHTTPRequestHandler
from http.cookies import CookieError, SimpleCookie
from urllib.parse import urlparse, parse_qs, unquote
from engine import access, openruns, paths, tracks
from engine.bank import load_bank
from engine.explain import explanations, for_item
from engine.leitner import target_ms
from engine.mock import assemble, mark_taken, mocks, score
from engine.simulate import simulate, status as cached_status
from engine.units import units

LOCK=threading.Lock(); RUNS={}; BANKS={}
OPEN={"/api/learners","/api/login","/api/logout"}
HIDDEN={"answer","distractor_notes","script"}
MAX_BODY=65536
DENIED="Not registered for this portal – ask Alex"
def cookie(value,age): return f"learner={value}; Path=/; Max-Age={age}; SameSite=Lax; HttpOnly"+("; Secure" if access.mode()!="local" else "")
def bank():
    if paths.BANK not in BANKS: BANKS[paths.BANK]=load_bank()
    return BANKS[paths.BANK]
def chosen(handler):
    try: jar=SimpleCookie(handler.headers.get("Cookie",""))
    except CookieError: return None
    return jar["learner"].value if "learner" in jar else None
def who(handler):
    rows=paths.learners(); pick=chosen(handler); picked=pick if any(r["id"]==pick for r in rows) else None
    if access.mode()=="local": return {"email":None,"learner_id":picked or (rows[0]["id"] if len(rows)==1 else None),"admin":False}
    email=access.login(handler.headers.get(access.HEADER))
    if email is None: return None
    row=paths.by_email(email); admin=email in paths.admins()
    if not row and not admin: return None
    return {"email":email,"learner_id":picked if admin and picked else row["id"] if row else None,"admin":admin}
def note(item,choice):
    own=item.get(f"distractor_notes_{paths.learner()['explain']}") or {}
    return own.get(str(choice)) or item.get("distractor_notes",{}).get(str(choice))
def profile(row): return {k:row[k] for k in ("id","name","track","ui","explain")}
def mine(rid):
    run=RUNS.get(rid)
    if run is None and (run:=openruns.load(rid)) is not None: RUNS[rid]=run
    return run if run and run["learner"]==paths.learner()["id"] else None
def append(path,obj):
    path.parent.mkdir(parents=True,exist_ok=True)
    with LOCK, path.open("a",encoding="utf-8") as f: f.write(json.dumps(obj,ensure_ascii=False)+"\n")
def attempts():
    if not paths.ATTEMPTS.exists(): return []
    return [json.loads(x) for x in paths.ATTEMPTS.read_text(encoding="utf-8").splitlines() if x.strip()]
REFUSED={}; REFUSED_EVERY_S=3600
def clock(): return time.monotonic()
def refused_login(h):
    if access.mode()!="tailscale" or h.status!=403 or h.ident is not None: return None
    login=access.login(h.headers.get(access.HEADER))
    if login is None: return None
    now=clock()
    with LOCK:
        if login in REFUSED and now-REFUSED[login]<REFUSED_EVERY_S: return None
        REFUSED[login]=now
    return login
def log_access(h):
    ident=h.ident or {}; ts=datetime.now(timezone.utc).isoformat(timespec="seconds"); login=refused_login(h)
    try: append(paths.HOME/"logs"/f"access-{ts[:7]}.jsonl",{"ts":ts,"email":ident.get("email"),"as_learner":ident.get("learner_id"),"method":h.command,"path":urlparse(h.path).path,"status":h.status,"ms":round((time.monotonic()-h.started)*1000),**({"refused_login":login} if login else {})})
    except OSError: pass
def log_error(eid):
    text=f"{datetime.now(timezone.utc).isoformat(timespec='seconds')} {eid}\n{traceback.format_exc()}"
    try:
        (paths.HOME/"logs").mkdir(parents=True,exist_ok=True)
        with LOCK, (paths.HOME/"logs"/"errors.log").open("a",encoding="utf-8") as f: f.write(text)
    except OSError: pass
    if sys.stderr: print(text,file=sys.stderr,flush=True)
def origins(handler):
    configured=[o.strip() for o in os.environ.get("JLPT_ORIGIN","").split(",") if o.strip()]
    host=handler.headers.get("Host","")
    return set(configured) if configured else {f"http://{host}",f"https://{host}"}
def byte_range(header,size):
    if not header.startswith("bytes="): return 0,size-1,200
    try:
        a,_,b=header[6:].split(",")[0].strip().partition("-")
        first,last=(max(0,size-int(b)),size-1) if not a else (int(a),min(int(b),size-1) if b else size-1)
    except ValueError: return None
    return (first,last,206) if 0<=first<=last<size else None
class Handler(BaseHTTPRequestHandler):
    status=None; ident=None; started=0.0
    def log_message(self,*args): pass
    def send_response(self,code,message=None):
        self.status=code; super().send_response(code,message)
    def end_headers(self):
        if urlparse(self.path).path.startswith(("/api/","/audio/")): self.send_header("Cache-Control","private, no-store")
        super().end_headers()
    def send_json(self,obj,status=200,cookie=None):
        raw=json.dumps(obj,ensure_ascii=False).encode(); self.send_response(status); self.send_header("Content-Type","application/json; charset=utf-8"); self.send_header("Content-Length",str(len(raw)))
        if cookie: self.send_header("Set-Cookie",cookie)
        self.end_headers(); self.wfile.write(raw)
    def send_text(self,text,status=200):
        raw=text.encode(); self.send_response(status); self.send_header("Content-Type","text/plain; charset=utf-8"); self.send_header("Content-Length",str(len(raw))); self.end_headers(); self.wfile.write(raw)
    def refuse(self,obj,status):
        self.close_connection=True; return self.send_json(obj,status)
    def deny(self,path):
        return self.send_json({"error":DENIED},403) if path.startswith("/api/") else self.send_text(DENIED,403)
    def guarded(self,fn):
        self.started=time.monotonic(); self.status=None; self.ident=None
        try: fn()
        except (BrokenPipeError,ConnectionResetError): pass
        except Exception:
            eid=secrets.token_hex(4); log_error(eid)
            if self.status is None:
                try: self.refuse({"error":"server error","id":eid},500)
                except OSError: pass
        finally: log_access(self)
    def route(self,fn):
        path=urlparse(self.path).path; gated=access.mode()!="local"; private=path.startswith(("/api/","/audio/"))
        if gated or private: self.ident=who(self)
        if gated and self.ident is None: return self.deny(path)
        if path in OPEN or not private: return fn()
        lid=self.ident and self.ident["learner_id"]
        if lid is None: return self.send_json({"error":"login required"},401)
        with paths.as_learner(lid): return fn()
    def do_GET(self): self.guarded(lambda: self.send_text("ok") if urlparse(self.path).path=="/healthz" else self.route(self.get))
    def do_POST(self): self.guarded(self.receive)
    def receive(self):
        try: n=int(self.headers.get("Content-Length",""))
        except ValueError: return self.refuse({"error":"invalid length"},400)
        if n<0: return self.refuse({"error":"invalid length"},400)
        if n>MAX_BODY: return self.refuse({"error":"body too large"},413)
        if self.headers.get("Content-Type","").split(";")[0].strip().lower()!="application/json": return self.refuse({"error":"forbidden"},403)
        origin=self.headers.get("Origin")
        if origin and origin not in origins(self): return self.refuse({"error":"forbidden"},403)
        try: data=json.loads(self.rfile.read(n))
        except ValueError: return self.send_json({"error":"invalid JSON"},400)
        self.route(lambda: self.post(data if isinstance(data,dict) else {}))
    def get(self):
        u=urlparse(self.path); q=parse_qs(u.query)
        if u.path=="/api/learners":
            rows=paths.learners() if access.mode()=="local" or self.ident["admin"] else [r for r in paths.learners() if r["id"]==self.ident["learner_id"]]
            return self.send_json([{k:r[k] for k in ("id","name","ui","track")} for r in rows])
        if u.path=="/api/me": return self.send_json({"learner":profile(paths.learner()),"track":tracks.summary(),**({"admin":True} if self.ident and self.ident["admin"] else {})})
        if u.path=="/api/status": return self.send_json(cached_status())
        if u.path=="/api/report":
            from engine.report import build_report
            return self.send_json(build_report(bank()[0]))
        if u.path=="/api/mocks": return self.send_json(mocks())
        if u.path=="/api/units": return self.send_json(units(bank()[0],attempts()) if tracks.current().get("units") else [])
        if u.path=="/api/run":
            from engine.select import build_run
            mode=q.get("mode",["practice"])[0]; section=q.get("section",["mixed"])[0]; mock_id=None
            try: n=max(1,min(100,int(q.get("n",[20])[0])))
            except ValueError: return self.send_json({"error":"invalid n"},400)
            if mode=="mock":
                mock_id=q.get("mock",[""])[0]; meta=next((m for m in mocks() if m["id"]==mock_id),None)
                if not meta or not meta["open"]: return self.send_json({"error":"This mock is not open yet."},403)
                data={**assemble(mock_id),"mode":mode,"time_limit_ms":None}; section="mock"
            else: data=build_run(mode,section,n,seed=uuid.uuid4().int)
            rid="r-"+uuid.uuid4().hex[:12]; originals=data["items"]
            public=[]
            for item in originals: public.append({**{k:v for k,v in item.items() if k not in HIDDEN and not k.startswith(("explanation_","distractor_notes"))},"target_ms":target_ms(item)})
            try: baseline=json.loads(paths.MODEL_STATE.read_text(encoding="utf-8"))["p_pass"]
            except (OSError, ValueError, KeyError): baseline=simulate(write=False)["p_pass"]
            RUNS[rid]={"start":datetime.now(timezone.utc).isoformat(),"mode":mode,"section":section,"items":{x["id"]:x for x in originals},"answers":{},"time_limit_ms":data["time_limit_ms"],"p_pass_before":baseline,"mock_id":mock_id,"learner":paths.learner()["id"]}
            openruns.save(rid,RUNS[rid])
            return self.send_json({"run_id":rid,"mode":mode,"time_limit_ms":data["time_limit_ms"],"parts":data.get("parts"),"items":public,"passages":data["passages"]})
        if u.path=="/" or u.path.startswith("/web/"):
            rel="index.html" if u.path=="/" else unquote(u.path[5:]); path=(paths.REPO/"web"/rel).resolve()
            if paths.REPO/"web" not in path.parents and path!=paths.REPO/"web": return self.send_error(403)
        elif u.path.startswith("/audio/"):
            path=paths.audio_file("audio/"+unquote(u.path[7:]))
            if path is None: return self.send_error(404)
        else: return self.send_error(404)
        if not path.is_file(): return self.send_error(404)
        size=path.stat().st_size
        # Browsers can only seek inside an MP3 (listening clips start mid-file) when byte ranges are served.
        span=byte_range(self.headers.get("Range",""),size)
        if span is None: self.send_response(416); self.send_header("Content-Range",f"bytes */{size}"); self.send_header("Content-Length","0"); self.end_headers(); return
        first,last,status=span
        self.send_response(status); self.send_header("Content-Type",mimetypes.guess_type(path.name)[0] or "application/octet-stream"); self.send_header("Accept-Ranges","bytes")
        if status==206: self.send_header("Content-Range",f"bytes {first}-{last}/{size}")
        self.send_header("Content-Length",str(max(0,last-first+1))); self.end_headers()
        with path.open("rb") as f: f.seek(first); self.wfile.write(f.read(max(0,last-first+1)))
    def post(self,data):
        if self.path=="/api/login":
            if access.mode()!="local" and not self.ident["admin"]: return self.send_json({"error":"forbidden"},403)
            row=paths.find(data.get("learner"))
            if not row: return self.send_json({"error":"unknown learner"},404)
            return self.send_json({"ok":True,"learner":profile(row)},cookie=cookie(row["id"],31536000))
        if self.path=="/api/logout": return self.send_json({"ok":True},cookie=cookie("",0))
        if self.path=="/api/answer":
            run=mine(data.get("run_id")); item=run and run["items"].get(data.get("item_id"))
            if not item: return self.send_json({"error":"unknown run/item"},404)
            if item["id"] in run["answers"]: return self.send_json({"ok":True})
            choice=data.get("choice"); correct=choice==item["answer"] and not data.get("timed_out")
            a={"ts":datetime.now().astimezone().isoformat(),"run_id":data["run_id"],"item_id":item["id"],"choice":choice,"correct":correct,"ms":data.get("ms"),"flag":data.get("flag") or "none","mode":run["mode"],"timed_out":bool(data.get("timed_out"))}
            if run["section"]=="mistakes": a["review"]=True
            append(paths.ATTEMPTS,a); run["answers"][item["id"]]={**a,"item":item}; openruns.save(data["run_id"],run); out={"ok":True}
            if run["mode"]=="practice": out.update({"answer":item["answer"],"explanation_en":item.get("explanation_en"),**explanations(item),"distractor_note":note(item,choice),"script":item.get("script"),"explain":for_item(item)})
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
            openruns.drop(rid)
            result=[]
            for item in run["items"].values():
                a=run["answers"].get(item["id"],{}); choice=a.get("choice"); result.append({"stem":item["stem"],"options":item["options"],"choice":choice,"answer":item["answer"],"correct":a.get("correct",False),"ms":a.get("ms"),"slow":bool(a.get("ms") and a["ms"]>target_ms(item)),"flag":a.get("flag","none"),"explanation_en":item.get("explanation_en"),**explanations(item),"distractor_note":note(item,choice),"script":item.get("script"),"explain":for_item(item),"item_id":item["id"],"section":item["section"],**{k:item[k] for k in ("stem_lang","options_lang") if k in item}})
            return self.send_json({"score":correct,"total_ms":total_ms,"p_pass_before":before,"p_pass_after":after,"mock":mock,"items":result})
        if self.path=="/api/explain_feedback":
            # "Still unclear" on an explanation: kept apart from attempts, so it never touches scores.
            if not isinstance(data.get("item_id"),str): return self.send_json({"error":"item_id required"},400)
            append(paths.CONFIDENTIAL/"explain_feedback.jsonl",{"ts":datetime.now().astimezone().isoformat(),"item_id":data["item_id"],"run_id":data.get("run_id"),"choice":data.get("choice")})
            return self.send_json({"ok":True})
        self.send_error(404)

START="JLPT portal serving on"
def serve(port=None):
    access.check_startup(); openruns.prune()
    srv=ThreadingHTTPServer((access.bind(),int(port or os.getenv("JLPT_PORT",8080))),Handler)
    build=(paths.REPO/"BUILD").read_text(encoding="utf-8").strip() if (paths.REPO/"BUILD").is_file() else "dev"
    if sys.stderr: print(f"{START} {access.bind()}:{srv.server_port} as {access.mode()} build {build}",file=sys.stderr,flush=True)
    srv.serve_forever()
if __name__=="__main__": serve()
