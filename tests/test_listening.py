import pytest
from engine.bank import validate_item

def item(mondai, options, answer=1):
    return {"id": "ls-x", "section": "listening", "mondai": mondai, "tier_prior": "medium", "level": "N4-core", "stem": "S",
            "options": options, "answer": answer, "tags": [], "explanation_en": "", "source": {}, "verified": True}

def test_spoken_reply_items_have_three_options():
    validate_item(item("quick_response", ["a", "b", "c"], 3))
    validate_item(item("verbal_expression", ["a", "b", "c"], 2))
    validate_item(item("verbal_expression", ["a", "b", "c", "d"], 4))
    with pytest.raises(ValueError): validate_item(item("quick_response", ["a", "b"]))
    with pytest.raises(ValueError): validate_item(item("quick_response", ["a", "b", "c"], 4))

def test_task_items_keep_four_options():
    validate_item(item("task_based", ["a", "b", "c", "d"], 4))
    with pytest.raises(ValueError): validate_item(item("key_points", ["a", "b", "c"]))
