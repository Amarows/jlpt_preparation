"""Write confidential/analysis/mistakes_to_generate.md: open mistakes that have no follow-up items yet.

This is the input for a generation pass: for each mistake, write 3-5 new items aimed at the same error, with
source.parent_item / source.parent_attempt set, then check them blind before setting verified.
"""
import sys
from collections import Counter
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from engine import paths
from engine.bank import load_bank
from engine.model import open_mistakes, read_attempts


def main():
    items, passages = load_bank()
    children = Counter(x["source"].get("parent_item") for x in items.values() if x["source"].get("parent_item"))
    todo = [(i, a) for i, a in open_mistakes(read_attempts(), items).items() if children[i] < 3]
    lines = ["# Mistakes to generate from", "", f"{len(todo)} open mistakes without follow-up items.", ""]
    for i, a in todo:
        x = items[i]
        chosen = x["options"][a["choice"] - 1] if isinstance(a.get("choice"), int) and 0 < a["choice"] <= len(x["options"]) else "no answer"
        lines += [f"## {i} ({x['section']}/{x['mondai']})", "",
                  f"- Attempt: {a.get('ts')}" + (f", flagged {a['flag']}" if a.get("flag") not in (None, "none") else ""),
                  f"- Stem: {x['stem']}"]
        if x.get("passage_id") in passages:
            lines.append(f"- Passage: {passages[x['passage_id']]['text'][:300]}")
        lines += [f"- Options: {' / '.join(f'{n}. {o}' for n, o in enumerate(x['options'], 1))}",
                  f"- Correct: {x['options'][x['answer'] - 1]} · Chosen: {chosen}",
                  f"- Tags: {', '.join(x.get('tags', []))}", f"- Note: {x.get('explanation_en', '')}", ""]
    out = paths.CONFIDENTIAL / "analysis" / "mistakes_to_generate.md"
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text("\n".join(lines), encoding="utf-8")
    print(f"{len(todo)} mistakes; wrote {out}")


if __name__ == "__main__":
    main()
