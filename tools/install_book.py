"""Normalise a transcribed book test and install it into the bank, as practice or as a mock.

Usage: python tools/install_book.py <transcription folder> <JLPT_HOME> <test id, e.g. bpt1> practice|mock
The folder holds vocab.json, grammar.json, reading.json and passages.json written by a transcription pass.
"""
import json, re, sys
from pathlib import Path
src, home, test, dest = Path(sys.argv[1]), Path(sys.argv[2]), sys.argv[3], sys.argv[4]  # dest: "practice" or "mock"
def clean(t):
    t = re.sub(r"<u>(.*?)</u>", r"【\1】", t)          # SCHEMA: underline = 【 】
    t = t.replace("<br>", " ／ ")
    t = re.sub(r"(?m)^#+\s*(.+)$", r"**\1**", t)
    t = re.sub(r"(?m)^>\s?", "", t)                    # blockquotes are not rendered
    t = re.sub(r"(?m)^-{3,}\s*$", "", t)               # nor horizontal rules
    t = re.sub(r" {2,}$", "", t, flags=re.M)
    return t
bank = home / "data" / "bank"
passages = [{**p, "text": clean(p["text"])} for p in json.loads((src / "passages.json").read_text(encoding="utf-8"))]
for f in ("vocab", "grammar", "reading"):
    items = json.loads((src / f"{f}.json").read_text(encoding="utf-8"))
    for x in items:
        x["stem"] = clean(x["stem"]); x["options"] = [clean(o) for o in x["options"]]
        assert "<" not in x["stem"] + "".join(x["options"]), x["id"]
        x["source"]["batch"] = f"{f}/{test}_written" if dest == "practice" else f"mocks/{test}/{f}"
    out = bank / f / f"{test}_written.json" if dest == "practice" else bank / "mocks" / test / f"{f}.json"
    out.write_text(json.dumps(items, ensure_ascii=False, indent=2), encoding="utf-8"); print(out, len(items))
if dest == "practice":
    pf = bank / "reading" / "passages.json"; old = [p for p in json.loads(pf.read_text(encoding="utf-8")) if not p["id"].startswith(f"psg-{test}-")]
    pf.write_text(json.dumps(old + passages, ensure_ascii=False, indent=2), encoding="utf-8")
else:
    (bank / "mocks" / test / "passages.json").write_text(json.dumps(passages, ensure_ascii=False, indent=2), encoding="utf-8")
print("passages", len(passages))
