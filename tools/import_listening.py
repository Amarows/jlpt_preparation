"""Build listening items from hand-checked source files.

Each source file in materials/listening_src/*.json describes one set:
{"set", "ref", "kind", "audio_dir", "pdf"?, "items": [
  {"n": "<mondai>-<question>", "track" | "file", "start"?, "end"?, "q", "opts", "ans",
   "img": [pdf_page, "top" | "bottom"] | null, "hide", "script", "note"}]}

Audio is copied to audio/<set>/, booklet pictures are cropped from the PDF to audio/<set>/img/,
and the items go to data/bank/listening/<set>.json. Needs PyMuPDF and mutagen (pip install pymupdf mutagen).
"""
import json, shutil, sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from engine import paths
from engine.bank import validate_item

MONDAI = {"1": "task_based", "2": "key_points", "3": "verbal_expression", "4": "quick_response"}
HALVES = {"top": (0.03, 0.03, 0.97, 0.51), "bottom": (0.03, 0.49, 0.97, 0.97)}

def crop(pdf, page, half, out):
    import pymupdf
    doc = pymupdf.open(pdf); r = doc[page].rect
    x0, y0, x1, y1 = HALVES[half] if isinstance(half, str) else half
    clip = pymupdf.Rect(r.width * x0, r.height * y0, r.width * x1, r.height * y1)
    out.parent.mkdir(parents=True, exist_ok=True)
    doc[page].get_pixmap(dpi=110, clip=clip).save(out)

def build(src: Path, materials: Path) -> list[dict]:
    s = json.loads(src.read_text(encoding="utf-8")); name = s["set"]; items = []
    for x in s["items"]:
        m, q = x["n"].split("-")
        audio_src = materials / s["audio_dir"] / (x["track"] + ".mp3" if "track" in x else x["file"])
        audio = paths.HOME / "audio" / name / audio_src.name
        audio.parent.mkdir(parents=True, exist_ok=True)
        if not audio.exists(): shutil.copyfile(audio_src, audio)
        clip = {"file": audio.relative_to(paths.HOME).as_posix()}
        if "start" in x: clip.update(start=x["start"], end=x["end"], duration=round(x["end"] - x["start"], 1))
        else:
            from mutagen.mp3 import MP3
            clip["duration"] = round(MP3(audio).info.length, 1)
        image = None
        if x.get("img"):
            out = paths.HOME / "audio" / name / "img" / f"{m}-{q}.png"
            crop(materials / s["pdf"], x["img"][0], x["img"][1], out)
            image = out.relative_to(paths.HOME).as_posix()
        item = {"id": f"ls-{name}-{m}-{int(q):02d}", "section": "listening", "mondai": MONDAI[m], "tier_prior": "medium", "level": "N4-core",
                "stem": x["q"], "options": x["opts"], "answer": x["ans"], "tags": [f"skill:listening_{MONDAI[m]}"], "confusion_pair": None,
                "passage_id": None, "audio": clip, "image": image, "hide_options": bool(x.get("hide")), "script": x["script"],
                "explanation_en": x.get("note", ""), "distractor_notes": {}, "source": {"kind": s.get("kind", "book"), "ref": f"{s['ref']} 問題{m} {q}番"}, "verified": True}
        validate_item(item); items.append(item)
    return items

def main():
    materials = paths.HOME / "materials"; out_dir = paths.BANK / "listening"; out_dir.mkdir(parents=True, exist_ok=True)
    for src in sorted((materials / "listening_src").glob("*.json")):
        items = build(src, materials)
        (out_dir / f"{src.stem}.json").write_text(json.dumps(items, ensure_ascii=False, indent=1), encoding="utf-8")
        print(f"{src.stem}: {len(items)} items")
if __name__ == "__main__": main()
