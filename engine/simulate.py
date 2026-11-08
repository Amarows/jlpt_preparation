import json, math, random
from datetime import date
from . import paths, tracks
from .model import fit, read_attempts, get_theta
from .bank import load_bank
from .leitner import target_ms


def simulate(attempts=None, seed=13, draws=10000, write=True, current_run_id=None, record_run=False):
    exam=tracks.exam(); blueprint=tracks.blueprint(); names=tracks.sections(); mondai=tracks.section_mondai()
    attempts=read_attempts() if attempts is None else attempts; model=fit(attempts,current_run_id=current_run_id); rng=random.Random(seed)
    means={s:get_theta(model,s) for s in names}; sds={s:model.get("sections",{}).get("sec:"+s,{}).get("sd",1.0) for s in means}
    items,_=load_bank(); speed=model["speed"]
    over={}
    for part in exam["parts"]:
        if part.get("pressure"):
            t=sum(speed.get(m,{}).get("median_ms",target_ms({"mondai":m,"tier_prior":"medium"}))*blueprint[m] for s in part["sections"] for m in mondai[s])
            over.update({s:max(0,min(1,(t-part["minutes"]*60000)/max(1,t))) for s in part["sections"]})
    gap=exam.get("gap_sd",.6); mu,sd=exam.get("item_difficulty",[.3,1]); guess=exam["guess"]; total_min=exam.get("total_min")
    sizes={s["id"]:sum(blueprint[m] for x in s["sections"] for m in mondai[x]) for s in exam["scores"]}
    outcomes=[]; dist={s["id"]:[] for s in exam["scores"]}; totals=[]
    for _ in range(draws):
        theta={s:rng.gauss(means[s],sds[s])-rng.gauss(0,gap) for s in means}; correct={s:0 for s in names}
        for section in names:
            for m in mondai[section]:
                for _j in range(blueprint[m]):
                    p=guess if section in over and rng.random()<over[section] else 1/(1+math.exp(-max(-30,min(30,theta[section]-rng.gauss(mu,sd)))))
                    correct[section]+=rng.random()<p
        scores={s["id"]:sum(correct[x] for x in s["sections"])/sizes[s["id"]]*s["max"] for s in exam["scores"]}; total=sum(scores.values())
        outcomes.append(all(scores[s["id"]]>=s["min"] for s in exam["scores"]) and (total_min is None or total>=total_min))
        for k,v in scores.items(): dist[k].append(v)
        totals.append(total)
    p=sum(outcomes)/draws
    batches=[sum(outcomes[i:i+500])/len(outcomes[i:i+500]) for i in range(0,draws,500)]
    prior={}
    if paths.MODEL_STATE.exists():
        try: prior=json.loads(paths.MODEL_STATE.read_text(encoding="utf-8"))
        except Exception: pass
    ema=.3*p+.7*prior.get("p_pass_ema",p) if record_run or "p_pass_ema" not in prior else prior["p_pass_ema"]
    past=prior.get("history",[]); ema_history=prior.get("ema_history",[])
    if record_run:
        trend="up" if len(ema_history)>=3 and ema-ema_history[-3]>.01 else "down" if len(ema_history)>=3 and ema-ema_history[-3]<-.01 else "flat"
        past=(past+[p])[-20:]; ema_history=(ema_history+[ema])[-20:]
    else:
        trend=prior.get("trend","flat") if len(ema_history)>=3 else "flat"
    mastered=model["boxes"]; by={}
    for i,box in mastered.items():
        if box>=3:
            sec=items.get(i,{}).get("section","unknown"); by[sec]=by.get(sec,0)+1
    state={"updated":date.today().isoformat(),"p_pass":p,"p_pass_ema":ema,"band80":[sorted(batches)[int(.1*len(batches))],sorted(batches)[min(len(batches)-1,int(.9*len(batches)))]],"trend":trend}
    state.update({f"p_{s['id']}_section":sum(x>=s["min"] for x in dist[s["id"]])/draws for s in exam["scores"]})
    if total_min is not None: state["p_total"]=sum(x>=total_min for x in totals)/draws
    state.update({"exp_score":{k:sum(v)/draws for k,v in dist.items()},"skills":model["skills"],"speed":model["speed"],"mastered":{"count":sum(v>=3 for v in mastered.values()),"by_section":by},"days_left":(date.fromisoformat(exam["date"])-date.today()).days,"history":past,"ema_history":ema_history})
    if write:
        paths.CONFIDENTIAL.mkdir(parents=True,exist_ok=True); paths.MODEL_STATE.write_text(json.dumps(state,ensure_ascii=False,indent=2),encoding="utf-8")
    return state
