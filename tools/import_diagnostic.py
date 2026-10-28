"""Import placement diagnostic items and seed attempts."""
import json,re,sys
from pathlib import Path
from datetime import datetime
sys.path.insert(0,str(Path(__file__).resolve().parents[1]))
from engine import paths

def main():
    d=paths.BANK/"diagnostic"; test=d/"2026-10-25_placement_test.md"; keyfile=d/"2026-10-25_placement_key.json"
    text=test.read_text(encoding="utf-8"); key={x["q"]:x for x in json.loads(keyfile.read_text(encoding="utf-8"))}
    blocks={int(m.group(1)):m.group(2) for m in re.finditer(r"(?ms)^\*\*(\d+)\.\*\*\s*(.*?)(?=^\*\*\d+\.\*\*|^---|\Z)",text)}
    items=[]; passages=[]
    # Passage text stops at its first question; blockquote markers are dropped, line structure (tables) is kept.
    unquote=lambda s:"\n".join(re.sub(r"^>[ \t]?","",l.strip()) for l in s.strip().splitlines()).strip()
    pm=re.search(r"(?s)\*\*Read the (?:text|passage) and answer questions 19–20\.\*\*(.*?)(?=^\*\*\d+\.\*\*)",text,re.M)
    if pm: passages.append({"id":"placement-passage-19","text":unquote(pm.group(1))})
    nm=re.search(r"(?s)\*\*Read the notice and answer questions 21–22\.\*\*(.*?)(?=^\*\*\d+\.\*\*)",text,re.M)
    if nm: passages.append({"id":"placement-notice-21","text":unquote(nm.group(1))})
    for q,entry in key.items():
        block=blocks.get(q,""); stem=re.split(r"(?m)^\s*1\.",block,maxsplit=1)[0].strip()
        stem=re.sub(r"\s+", " ",stem)
        opts=[]
        for line in block.splitlines():
            opts += [(n, value.strip()) for n, value in re.findall(r"(?:^|\s)([1-4])\.\s*(.*?)(?=\s+[1-4]\.\s*|$)",line)]
        options=[v for _,v in opts]
        if len(options)!=4: options=[x.strip() for x in re.findall(r"[1-4]\.\s*([^\s　]+)",block)][:4]
        if len(options)!=4: raise ValueError(f"could not parse options for question {q}: {options}")
        sec="listening" if entry["section"]=="listening_proxy" else entry["section"]
        tags=[]
        topic=entry.get("topic","")
        if "のに" in topic: tags=["grammar:のに","grammar:contrast"]
        elif sec=="vocab": tags=["word:"+re.sub(r"[^一-龯々ぁ-んァ-ン]","",topic)[:12] or "placement"]
        elif sec=="grammar": tags=["grammar:"+topic[:32]]
        else: tags=["skill:"+entry["mondai"]]
        pid="placement-passage-19" if q in (19,20) else "placement-notice-21" if q in (21,22) else None
        items.append({"id":f"placement-{q:02d}","section":sec,"mondai":entry["mondai"],"tier_prior":"hard" if entry["level"]=="N4-hard" else "medium","level":entry["level"],"stem":stem,"options":options,"answer":entry["answer"],"tags":tags,"confusion_pair":None,"passage_id":pid,"audio":None,"image":None,"explanation_en":topic,"distractor_notes":entry.get("distractors",{}),"source":{"kind":"official","ref":f"2026-10-25 placement question {q}"},"verified":True})
    out=d/"placement_items.json"; out.write_text(json.dumps(items,ensure_ascii=False,indent=2),encoding="utf-8")
    pf=paths.BANK/"reading"/"passages.json"; pf.parent.mkdir(parents=True,exist_ok=True); existing=[]
    if pf.exists(): existing=json.loads(pf.read_text(encoding="utf-8"))
    by={x["id"]:x for x in existing}; by.update({x["id"]:x for x in passages}); pf.write_text(json.dumps(list(by.values()),ensure_ascii=False,indent=2),encoding="utf-8")
    summary=json.loads((paths.CONFIDENTIAL/"attempts/2026-10-25_placement.json").read_text(encoding="utf-8")); log=paths.ATTEMPTS; log.parent.mkdir(parents=True,exist_ok=True)
    existing_ids=set()
    if log.exists():
        for line in log.read_text(encoding="utf-8").splitlines():
            try:
                a=json.loads(line)
                if a.get("run_id")=="r-20261025-placement": existing_ids.add(a.get("item_id"))
            except json.JSONDecodeError: pass
    with log.open("a",encoding="utf-8") as f:
        for item in items:
            if item["id"] in existing_ids: continue
            q=int(item["id"].split("-")[1]); choice=summary["answers"][str(q)]
            flag="guess" if q==9 else "unclear" if q==20 else "none"
            a={"ts":"2026-10-25T12:00:00+02:00","run_id":"r-20261025-placement","item_id":item["id"],"choice":choice,"correct":choice==item["answer"],"ms":None,"flag":flag,"mode":"diagnostic","timed_out":False}
            f.write(json.dumps(a,ensure_ascii=False)+"\n")
    print(f"Imported {len(items)} diagnostic items; placement attempts are idempotent")
if __name__=="__main__": main()
