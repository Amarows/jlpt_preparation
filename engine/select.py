"""Deterministic adaptive practice run selection."""
import json, random
from collections import Counter, defaultdict
from datetime import datetime, timedelta, timezone
from . import paths
from .bank import load_bank
from .model import fit, read_attempts, get_theta, current_attempts, open_mistakes, _timestamp
from .leitner import target_ms, due as is_due
from .simulate import BLUEPRINT

REST_DAYS = 3

def blend(xs, n=None):
    """Reorder items so question types follow the exam blueprint: always take the type furthest below its share."""
    pools = defaultdict(list)
    for x in xs: pools[x["mondai"]].append(x)
    counts = Counter(); out = []
    while any(pools.values()) and (n is None or len(out) < n):
        m = min((m for m in pools if pools[m]), key=lambda m: counts[m] / BLUEPRINT.get(m, 1))
        out.append(pools[m].pop(0)); counts[m] += 1
    return out

def has_audio(x):
    return bool(x.get("audio")) and paths.under_home(x["audio"]["file"]).is_file()

def build_run(mode="practice", section="mixed", n=20, seed=1):
    """Choose a no-duplicate run with adaptive bucket proportions."""
    items,passages=load_bank(); attempts=current_attempts(read_attempts(),items)
    if section=="mistakes":
        # Every item whose latest answer was wrong; it leaves the pool once answered correctly.
        wrong=open_mistakes(attempts,items)
        pool=[items[i] for i in wrong if items[i].get("verified") and (items[i]["section"]!="listening" or has_audio(items[i]))]
        selected=list(pool); random.Random(seed).shuffle(selected); selected=selected[:n]
        return _assemble(mode,selected,pool,n,items,passages)
    model=fit(attempts,items)
    pool=[x for x in items.values() if x.get("verified") and (section=="mixed" or x["section"]==section) and (section!="mixed" or x.get("section")!="listening" or has_audio(x))]
    focus={}
    try: focus=json.loads((paths.CONFIDENTIAL/"focus.json").read_text(encoding="utf-8")).get("boost",{})
    except (OSError,json.JSONDecodeError): pass
    buckets={k:[] for k in ("weak","due","new","maintenance","rest")}; cutoff=(datetime.now(timezone.utc)-timedelta(days=14)).isoformat()
    rest_cut=datetime.now(timezone.utc)-timedelta(days=REST_DAYS); by_item=defaultdict(list)
    for a in attempts: by_item[a.get("item_id")].append(a)
    for x in pool:
        at=by_item[x["id"]]; last=at[-1] if at else None
        primary=next((t for t in x.get("tags",[]) if t.startswith(("grammar:","word:","kanji:","skill:"))),None)
        weak=(primary and model["skills"].get(primary,{}).get("theta",0)<get_theta(model,x["section"])) or bool(focus.get(primary)) or any((a.get("ts","")>=cutoff and (not a.get("correct") or a.get("flag")=="unclear")) for a in at)
        box=model["boxes"].get(x["id"],0)
        # An item answered right comes back only once it is due, and never within REST_DAYS; mistakes come back any time.
        missed=last and (not last.get("correct") or last.get("timed_out") or last.get("flag")=="unclear")
        if last and not missed and ((_timestamp(last.get("ts")) or rest_cut)>rest_cut or not is_due(box,last.get("ts"))):
            buckets["rest"].append(x); continue
        if weak: buckets["weak"].append(x)
        elif not at: buckets["new"].append(x)
        elif box>=3: buckets["maintenance"].append(x)
        elif is_due(box,last.get("ts") if last else None): buckets["due"].append(x)
        else: buckets["due"].append(x)
    recent_cut=(datetime.now(timezone.utc)-timedelta(hours=24)).isoformat()
    buckets["weak"].sort(key=lambda x:any(a.get("item_id")==x["id"] and a.get("ts","")>=recent_cut for a in attempts))
    rng=random.Random(seed)
    for k,v in buckets.items():
        rng.shuffle(v); buckets[k]=blend(v)
    # Resting items only fill a run when nothing else is left, least recently seen first.
    buckets["rest"].sort(key=lambda x:by_item[x["id"]][-1].get("ts",""))
    # weak includes due work in the high-priority half
    quotas={"weak":round(n*.25),"due":n//2-round(n*.25),"new":round(n*.3),"maintenance":n-round(n*.25)-(n//2-round(n*.25))-round(n*.3)}
    selected=[]
    for key in ("weak","due","new","maintenance"):
        for x in buckets[key][:quotas[key]]:
            if x not in selected: selected.append(x)
    for key in ("weak","due","new","maintenance","rest"):
        for x in buckets[key]:
            if len(selected)>=n: break
            if x not in selected: selected.append(x)
    return _assemble(mode,selected,pool,n,items,passages)

def _assemble(mode,selected,pool,n,items,passages):
    """Complete passage bundles, order the run and set the time limit."""
    # Keep every selected passage as a complete, ordered bundle when it fits.
    complete=[]; seen_ids=set()
    for x in selected:
        pid=x.get("passage_id")
        bundle=[y for y in pool if pid and y.get("passage_id")==pid] if pid else [x]
        missing=[y for y in bundle if y["id"] not in seen_ids]
        if len(complete)+len(missing)>n: continue
        complete.extend(missing); seen_ids.update(y["id"] for y in missing)
    for x in pool:
        if len(complete)>=n: break
        if not x.get("passage_id") and x["id"] not in seen_ids:
            complete.append(x); seen_ids.add(x["id"])
    selected=complete; porder=[]; grouped={}
    for x in selected:
        pid=x.get("passage_id")
        if pid: grouped.setdefault(pid,[]).append(x)
        else: porder.append((None,[x]))
    # Restore question order within passages based on bank file order as loaded.
    for pid,xs in grouped.items(): porder.append((pid,sorted(xs,key=lambda x:list(items).index(x["id"]))))
    runitems=[x for _,xs in porder for x in xs]
    excerpt={pid:passages[pid]["text"] for pid,_ in porder if pid in passages}
    # Listening answer time starts when the clip ends, so the clip itself is added to the limit.
    limit=sum(target_ms({**x,"tier_prior":"medium"})+round((x.get("audio") or {}).get("duration",0)*1000) for x in runitems) if mode=="timed" else None
    return {"mode":mode,"time_limit_ms":limit,"items":runitems,"passages":excerpt}
