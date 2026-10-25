"""Validate bank JSON files against docs/SCHEMA.md."""
import json,sys
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parents[1]))
from engine import paths
from engine.bank import validate_item
def main():
    errors=[]; ids={}; seen=set(); passages=set()
    files=list(paths.BANK.rglob("*.json"))
    for f in files:
        if f.name=="passages.json":
            try: passages.update(x["id"] for x in json.loads(f.read_text(encoding="utf-8")))
            except Exception as e: errors.append(f"{f}: {e}")
    for f in files:
        if "mocks" in f.parts: continue
        try: data=json.loads(f.read_text(encoding="utf-8"))
        except Exception as e: errors.append(f"{f}: {e}"); continue
        if f.name=="passages.json": continue
        if f.name.endswith("_key.json"): continue
        if not isinstance(data,list): errors.append(f"{f}: expected array"); continue
        for x in data:
            try:
                validate_item(x)
                if x["id"] in ids: errors.append(f"duplicate id {x['id']}")
                ids[x["id"]]=f
                sig=(x["stem"],tuple(x["options"]))
                if sig in seen: errors.append(f"duplicate stem/options {x['id']}")
                seen.add(sig)
                for tag in x["tags"]:
                    if not tag.startswith(("grammar:","word:","kanji:","skill:","phrase:")) and tag.split(":")[0] in {"grammar","word","kanji","skill","phrase"}: errors.append(f"bad tag {tag}")
                if x.get("passage_id") and x["passage_id"] not in passages: errors.append(f"missing passage {x['id']}")
                aud=x.get("audio")
                if aud and not paths.under_home(aud["file"]).is_file(): errors.append(f"missing audio {x['id']}")
            except Exception as e: errors.append(f"{f}: {e}")
    if errors: print("\n".join(errors)); return 1
    print(f"Verified {len(ids)} items"); return 0
if __name__=="__main__": raise SystemExit(main())
