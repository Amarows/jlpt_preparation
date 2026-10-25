import json

from engine import paths
from tools.gen_vocab_items import shuffle_options


def test_per_item_seed_distributes_correct_answer_positions():
    ids = [f"vocab-kr-{i:05d}" for i in range(1, 1001)]
    counts = [0, 0, 0, 0]
    for item_id in ids:
        options = shuffle_options(["correct", "wrong-a", "wrong-b", "wrong-c"], item_id)
        counts[options.index("correct")] += 1
    assert all(20 <= count / len(ids) * 100 <= 30 for count in counts), counts

    generated = paths.BANK / "vocab" / "generated_kanji.json"
    if generated.is_file():
        items = json.loads(generated.read_text(encoding="utf-8"))
        actual = [sum(item["answer"] == position for item in items) for position in range(1, 5)]
        assert all(20 <= count / len(items) * 100 <= 30 for count in actual), actual
