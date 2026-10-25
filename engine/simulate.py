"""Monte Carlo JLPT pass-probability simulation."""
import json, math, random
from datetime import date
from . import paths
from .model import fit, read_attempts, get_theta
from .bank import load_bank
from .leitner import target_ms

BLUEPRINT={"kanji_reading":7,"orthography":5,"contextual":8,"paraphrase":4,"usage":4,"grammar_form":13,"sentence_composition":4,"text_grammar":4,"short_passage":3,"mid_passage":3,"info_retrieval":2,"task_based":8,"key_points":7,"verbal_expression":5,"quick_response":8}
def simulate(attempts=None, seed=13, draws=10000, write=True, current_run_id=None, record_run=False):
    """Compute pass probability, score estimates, confidence band and trends."""
    attempts=read_attempts() if attempts is None else attempts; model=fit(attempts,current_run_id=current_run_id); rng=random.Random(seed)
    means={s:get_theta(model,s) for s in ("vocab","grammar","reading","listening")}; sds={s:model.get("sections",{}).get("sec:"+s,{}).get("sd",1.0) for s in means}
    items,_=load_bank(); speed=model["speed"]
    vtime=sum(speed.get(m,{}).get("median_ms",target_ms({"mondai":m,"tier_prior":"medium"}))*n for m,n in BLUEPRINT.items() if m in {"kanji_reading","orthography","contextual","paraphrase","usage"})
    grtime=sum(speed.get(m,{}).get("median_ms",target_ms({"mondai":m,"tier_prior":"medium"}))*n for m,n in BLUEPRINT.items() if m in {"grammar_form","sentence_composition","text_grammar","short_passage","mid_passage","info_retrieval"})
    vover=max(0,min(1,(vtime-25*60000)/max(1,vtime))); gover=max(0,min(1,(grtime-55*60000)/max(1,grtime)))
    outcomes=[]; lks=[]; ls=[]
    for _ in range(draws):
        theta={s:rng.gauss(means[s],sds[s]) for s in means}; correct={"vocab":0,"grammar":0,"reading":0,"listening":0}
        groups={"vocab":["kanji_reading","orthography","contextual","paraphrase","usage"],"grammar":["grammar_form","sentence_composition","text_grammar"],"reading":["short_passage","mid_passage","info_retrieval"],"listening":["task_based","key_points","verbal_expression","quick_response"]}
        for section,mondais in groups.items():
            for m in mondais:
                for _j in range(BLUEPRINT[m]):
                    p=.25 if section=="vocab" and rng.random()<vover or section in ("grammar","reading") and rng.random()<gover else 1/(1+math.exp(-max(-30,min(30,theta[section]-rng.gauss(.3,1)))))
                    correct[section]+=rng.random()<p
        lk=correct["vocab"]+correct["grammar"]+correct["reading"]; l=correct["listening"]; lk_score=lk/57*120; l_score=l/28*60
        outcomes.append(lk_score>=38 and l_score>=19 and lk_score+l_score>=90); lks.append(lk_score); ls.append(l_score)
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
    state={"updated":date.today().isoformat(),"p_pass":p,"p_pass_ema":ema,"band80":[sorted(batches)[int(.1*len(batches))],sorted(batches)[min(len(batches)-1,int(.9*len(batches)))]],"trend":trend,"p_lk_section":sum(x>=38 for x in lks)/draws,"p_listening_section":sum(x>=19 for x in ls)/draws,"p_total":sum(x+y>=90 for x,y in zip(lks,ls))/draws,"exp_score":{"lk":sum(lks)/draws,"listening":sum(ls)/draws},"skills":model["skills"],"speed":model["speed"],"mastered":{"count":sum(v>=3 for v in mastered.values()),"by_section":by},"days_left":(date(2026,12,6)-date.today()).days,"history":past,"ema_history":ema_history}
    if write:
        paths.CONFIDENTIAL.mkdir(parents=True,exist_ok=True); paths.MODEL_STATE.write_text(json.dumps(state,ensure_ascii=False,indent=2),encoding="utf-8")
    return state
