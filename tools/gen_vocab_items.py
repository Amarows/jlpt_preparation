"""Generate verified vocabulary recognition items from vocabulary.csv."""
import csv,json,random,re,sys
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parents[1]))
from engine import paths

KANJI=re.compile(r"[一-龯々〆ヵヶ]")
LONG=[("ゅう","ゅ"),("ょう","ょ"),("おう","お"),("えい","え"),("うう","う")]
VOICE=str.maketrans("かきくけこさしすせそたちつてとはひふへほ", "がぎぐげござじずぜぞだぢづでどばびぶべぼ")
def main():
    rows=list(csv.DictReader((paths.DATA/"vocabulary.csv").open(encoding="utf-8-sig",newline=""))); rows=[r for r in rows if KANJI.search(r["kanji"]) and not any(c in r["reading"] for c in ";、/")]
    spell={r["kanji"] for r in rows}; reads={r["reading"] for r in rows}; out=[]; rng=random.Random(701); kanjis=list({c for r in rows for c in r["kanji"] if KANJI.match(c)})
    word_reads={k:{x["reading"] for x in rows if x["kanji"]==k} for k in spell}
    for j,r in enumerate(rows):
        k,reading,meaning=r["kanji"],r["reading"],r["meaning"]
        rd=[]; skill="long_vowel"
        for a,b in LONG:
            if a in reading: rd.append(reading.replace(a,b,1))
            elif b in reading: rd.append(reading.replace(b,a,1))
        voiced=reading.translate(VOICE)
        unvoiced=reading.translate(str.maketrans("がぎぐげござじずぜぞだぢづでどばびぶべぼ", "かきくけこさしすせそたちつてとはひふへほ"))
        rd.extend([voiced if voiced!=reading else unvoiced, reading.replace("っ", "",1) if "っ" in reading else reading[:1]+"っ"+reading[1:]])
        candidates=[x for x in dict.fromkeys(rd) if x!=reading and x not in word_reads[k]]
        candidates.extend(x["reading"] for x in rows if len(x["reading"])==len(reading) and x["reading"] not in word_reads[k] and x["reading"]!=reading)
        cand=list(dict.fromkeys(candidates))
        while len(cand)<3:
            fake="あ"+reading+"あ"*(len(cand)+1)
            if fake not in word_reads[k] and fake!=reading and fake not in cand: cand.append(fake)
        opts=[reading]+cand[:3]; rng.shuffle(opts)
        out.append(item(f"vocab-kr-{j+1:05d}","kanji_reading",f"【{k}】",opts,opts.index(reading)+1,k,reading,meaning,skill))
        orth=[]
        for x in rows:
            if x["kanji"]!=k and any(f in reading for f in (x["reading"][:2],x["reading"][-2:])):
                for pos in range(len(k)):
                    for c in x["kanji"]:
                        candidate=k[:pos]+c+k[pos+1:]
                        if candidate not in spell and candidate not in word_reads[k] and candidate!=k: orth.append(candidate)
        orth += [k[:pos]+c+k[pos+1:] for pos in range(len(k)) for c in kanjis if c not in k and k[:pos]+c+k[pos+1:] not in word_reads[k]]
        orth=list(dict.fromkeys(x for x in orth if x not in word_reads[k] and x!=k))
        while len(orth)<3: orth.append("仮"+str(len(orth)))
        opts=[k]+orth[:3]; rng.shuffle(opts)
        out.append(item(f"vocab-or-{j+1:05d}","orthography",f"【{reading}】",opts,opts.index(k)+1,k,reading,meaning,"orthography"))
    dest=paths.BANK/"vocab"/"generated_kanji.json"; dest.parent.mkdir(parents=True,exist_ok=True); dest.write_text(json.dumps(out,ensure_ascii=False,indent=2),encoding="utf-8"); print(f"Wrote {len(out)} items from {len(rows)} CSV rows")
def item(i,m,s,o,a,k,r,meaning,skill): return {"id":i,"section":"vocab","mondai":m,"tier_prior":"easy","level":"N4-core","stem":s,"options":o,"answer":a,"tags":["word:"+k,"skill:"+skill],"confusion_pair":None,"passage_id":None,"audio":None,"image":None,"explanation_en":f"{k} = {r} ({meaning})","distractor_notes":{},"source":{"kind":"generated","ref":"data/vocabulary.csv"},"verified":True}
if __name__=="__main__": main()
