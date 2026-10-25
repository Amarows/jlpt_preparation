"""Elo/Rasch-lite learner model."""
import json, math
from collections import defaultdict
from datetime import date
from . import paths
from .bank import load_bank
from .leitner import boxes, target_ms

def sigmoid(x: float) -> float: return 1 / (1 + math.exp(-max(-30, min(30, x))))
def read_attempts() -> list[dict]:
    out=[]
    if paths.ATTEMPTS.exists():
        for line in paths.ATTEMPTS.read_text(encoding="utf-8").splitlines():
            try: out.append(json.loads(line))
            except json.JSONDecodeError: pass
    return out

def fit(attempts: list[dict], items: dict | None = None) -> dict:
    """Replay attempts chronologically and return skill, item, and speed estimates."""
    items = items if items is not None else load_bank()[0]
    sec=defaultdict(lambda:.5); tag=defaultdict(float); b=defaultdict(float); ns=defaultdict(int); nt=defaultdict(int); speeds=defaultdict(list)
    for a in sorted(attempts,key=lambda x:x.get("ts", "")):
        item=items.get(a.get("item_id"), a.get("item",{})); section=item.get("section", a.get("section","vocab")); s="sec:"+section
        if s not in sec: sec[s]=.4 if section=="listening" else .5
        tags=item.get("tags",[]); primary=next((t for t in tags if t.startswith(("grammar:","word:","kanji:","skill:"))),None)
        q=primary or "tag:general"; tier=item.get("tier_prior","medium"); difficulty={"easy":-1.5,"medium":0,"hard":1.5}.get(tier,0)
        if item.get("level")=="N5": difficulty-=.5
        if item.get("level")=="N4-hard": difficulty+=.5
        difficulty=b[a.get("item_id","")] if a.get("item_id") in b else difficulty
        p=sigmoid(sec[s]+tag[q]-difficulty); y=1 if a.get("correct") and not a.get("timed_out") else 0; delta=y-p
        if a.get("flag")=="guess": delta*=.5
        sec[s]+=0.3/(1+ns[s]/20)*delta; tag[q]+=.5/(1+nt[q]/5)*delta; b[a.get("item_id","")]=difficulty-.15*delta; ns[s]+=1; nt[q]+=1
        if a.get("ms") is not None and item.get("mondai"): speeds[item["mondai"]].append(a["ms"])
    skills={}
    for k,n in ns.items(): skills[k]={"theta":sec[k],"sd":1/math.sqrt(1+n/4),"n":n}
    for k,n in nt.items(): skills[k]={"theta":tag[k],"sd":1/math.sqrt(1+n/4),"n":n}
    return {"skills":skills,"sections":{k:{"theta":v,"sd":1/math.sqrt(1+ns[k]/4),"n":ns[k]} for k,v in sec.items()},"item_b":dict(b),"speed":{k:{"median_ms":sorted(v[-50:])[len(v[-50:])//2],"target_ms":target_ms({"mondai":k,"tier_prior":"medium"})} for k,v in speeds.items()},"boxes":boxes(attempts,items)}

def get_theta(model: dict, section: str) -> float: return model.get("sections",{}).get("sec:"+section,{}).get("theta",.4 if section=="listening" else .5)
