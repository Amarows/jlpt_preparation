from engine.health import item_health

def _item(i, batch="b1"):
    return {"id":i,"section":"grammar","mondai":"grammar_form","tier_prior":"easy","level":"N4-core","stem":f"stem {i}","options":["a","b","c","d"],"answer":1,"tags":[],"source":{"kind":"generated","author":"claude-opus-5-5","batch":batch}}

def test_wrong_key_and_unclear_items_are_flagged():
    items={f"g{n}":_item(f"g{n}") for n in range(20)}; items["bad"]=_item("bad","b2"); items["vague"]=_item("vague","b2")
    attempts=[]
    for n in range(20):
        for d in range(3): attempts.append({"ts":f"2026-10-{d+1:02d}T10:{n:02d}:00+00:00","item_id":f"g{n}","choice":1,"correct":True,"ms":5000})
    # A wrong key: the learner keeps picking the same "wrong" option.
    for d in range(3): attempts.append({"ts":f"2026-10-{d+1:02d}T11:00:00+00:00","item_id":"bad","choice":3,"correct":False,"ms":5000})
    for d in range(2): attempts.append({"ts":f"2026-10-{d+1:02d}T12:00:00+00:00","item_id":"vague","choice":1,"correct":True,"ms":5000,"flag":"unclear"})
    health=item_health(items,attempts)
    flagged={s["id"]:s["reasons"] for s in health["suspects"]}
    assert set(flagged)=={"bad","vague"}
    assert any("same wrong option 3" in r for r in flagged["bad"]) and any("missed 3/3" in r for r in flagged["bad"])
    b2=[b for b in health["batches"] if b["batch"].endswith("/b2")][0]
    assert b2["accuracy"]<b2["expected_accuracy"]
