import random
from engine.model import fit
from engine.simulate import simulate

def test_model_returns_section_priors_and_updates():
    attempts=[]
    for n in range(30): attempts.append({"ts":f"2026-01-{n%28+1:02d}","item_id":"a","correct":True,"ms":1000,"item":{"section":"vocab","tier_prior":"easy","level":"N4-core","tags":["word:猫"]}})
    model=fit(attempts,{})
    assert model["sections"]["sec:vocab"]["theta"]>.5
    assert "word:猫" in model["skills"]

def test_theta_recovery_and_pass_probability_extremes():
    rng=random.Random(4); attempts=[]; items={}; theta={"vocab":1.1,"grammar":.8,"reading":.4,"listening":.7}
    for n in range(2000):
        section=("vocab","grammar","reading","listening")[n%4]; tier=("easy","medium","hard")[n%3]; diff={"easy":-1.5,"medium":0,"hard":1.5}[tier]
        iid=f"i{n}"; item={"section":section,"mondai":"grammar_form","tier_prior":tier,"level":"N4-core","tags":[f"skill:{section}:{n}"]}; items[iid]=item
        p=1/(1+__import__("math").exp(-(theta[section]-diff)))
        attempts.append({"ts":f"2026-01-01T00:{n//60:02d}:{n%60:02d}+00:00","item_id":iid,"correct":rng.random()<p,"ms":12000})
    fitted=fit(attempts,items)
    for sec,value in theta.items(): assert abs(fitted["sections"]["sec:"+sec]["theta"]-value)<.3
    for level,expected in ((4,True),(-4,False)):
        evidence=[]
        for sec in ("vocab","grammar","reading","listening"):
            for n in range(100): evidence.append({"ts":f"2026-02-{n%28+1:02d}T{n%24:02d}:00:00+00:00","item_id":f"{sec}{n}","section":sec,"correct":level>0,"ms":10000,"tier_prior":"medium","mondai":"grammar_form"})
        prob=simulate(evidence,draws=1000,write=False)["p_pass"]
        assert (prob>.95)==expected if expected else prob<.2

def test_section_posterior_is_stable_after_large_evidence():
    rng=random.Random(27)
    items={"medium":{"section":"vocab","tier_prior":"medium","level":"N4-core"}}
    attempts=[{"ts":f"2026-10-{n//24+1:02d}T{n%24:02d}:00:00+00:00","item_id":"medium","correct":rng.random()<.8} for n in range(200)]
    before=simulate(attempts,draws=1000,write=False)["p_pass"]
    extra=[{"ts":f"2026-10-25T12:{n:02d}:00+00:00","item_id":"medium","correct":rng.random()<.5,"run_id":"new"} for n in range(10)]
    after=simulate(attempts+extra,draws=1000,write=False)["p_pass"]
    assert abs(after-before)<.08

def test_consistent_medium_evidence_moves_theta_from_prior():
    attempts=[{"ts":f"2026-10-{n//24+1:02d}T{n%24:02d}:00:00+00:00","item_id":"medium","correct":n%20!=0,"item":{"section":"grammar","tier_prior":"medium","level":"N4-core"}} for n in range(100)]
    fitted=fit(attempts,{})
    assert fitted["sections"]["sec:grammar"]["theta"]>=1.0
