from engine.leitner import boxes

def test_box_progress_and_failure_reset():
    item={"mondai":"grammar_form","tier_prior":"easy"}
    good=lambda n:{"item_id":"x","correct":True,"ms":1000,"item":item,"ts":str(n)}
    assert boxes([good(1),good(2),good(3)])["x"]==3
    assert boxes([good(1),{**good(2),"correct":False}])["x"]==0
    assert boxes([good(1),{**good(2),"ms":999999}])["x"]==1
