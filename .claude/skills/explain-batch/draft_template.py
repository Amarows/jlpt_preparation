"""Copy to the scratchpad as draftNN.py, fill D, run: python draftNN.py data/explain_drafts/<batch>/drafts-NN.json"""
import json, sys
from pathlib import Path

def O(*pairs): return [{"ruby": r, "en": e} for r, e in pairs]          # one (ruby, meaning) per option, in order
def W(*t): return [{"w": w, "r": r, "en": e} for w, r, e in t]          # (word, hiragana reading, meaning)
def E(*t): return [{"text": a, "ruby": b, "en": c} for a, b, c in t]    # (exact quote, quote with furigana, translation)
def X(sentence, tr, options, words, steps, evidence=None):
    d = {"sentence": sentence, "translation_en": tr, "options": options, "words": words, "steps": steps}
    if evidence: d["evidence"] = evidence
    return d
S = "　"  # full-width space: passages use it between words; quotes must keep it (f"道が{S}こむ")

D = {
"gr-noni-001": X("たくさん{勉強|べんきょう}したのに、テストはよくなかったです。", "Even though I studied a lot, the test did not go well.",
  O(("ので", "because: studying is not a reason for a bad test"), ("から", "because: same problem as ので"), ("と", "when/if: a natural result, does not fit"), ("のに", "even though: the result is unexpected")),
  W(("勉強する", "べんきょうする", "to study")),
  ["Studied a lot, but the test went badly: unexpected → のに."]),
}

Path(sys.argv[1]).write_text(json.dumps(D, ensure_ascii=False, indent=1), encoding="utf-8")
print(len(D), "entries →", sys.argv[1])
