"""Write and check wrong-answer explanations (data/explain.json, see docs/SCHEMA.md).

    python tools/explain_items.py brief NAME --mistakes      # items Anna has answered wrong, without an explanation
    python tools/explain_items.py brief NAME --all [--section reading]
    python tools/explain_items.py brief NAME --next 25        # new mistakes first, then the bank in ORDER
    python tools/explain_items.py status                      # what is explained, what is next
    python tools/explain_items.py steps NAME                  # the merged steps' furigana, to read through
    python tools/explain_items.py gen NAME [--jobs 3]        # Codex writes drafts-XX.json for each brief-XX.json
    python tools/explain_items.py check NAME [--accept ID ...]
    python tools/explain_items.py gen NAME --retry           # rewrite the items that failed the check

Work files go to data/explain_drafts/NAME/. `check` merges only drafts that pass every check into data/explain.json:
hard errors (text not matching the item, a quote not found in the passage, kanji without furigana) are never merged;
soft flags (a reading that differs from the dictionary analyser or the N4 word list) wait for a look and --accept.
"""
import argparse, csv, json, re, shutil, subprocess, sys
from concurrent.futures import ThreadPoolExecutor
from datetime import date
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from engine import paths
from engine.bank import load_bank
from engine.explain import RUBY, fingerprint, plain
from engine.model import read_attempts

KANJI = re.compile(r"[㐀-鿿豈-﫿々〆ヶ]")
KANA = re.compile(r"^[ぁ-ゟ゠-ヿー]+$")
BLANK = re.compile(r"[（(][\s　]*[）)]")
PASSAGE_TYPES = {"short_passage", "mid_passage", "info_retrieval", "text_grammar"}
CHUNK = 20
# Question types in the order they get explanations: most mistakes and longest stems first, short vocabulary last.
ORDER = ["grammar_form", "text_grammar", "short_passage", "mid_passage", "info_retrieval", "sentence_composition", "quick_response",
         "verbal_expression", "key_points", "task_based", "usage", "paraphrase", "contextual", "kanji_reading", "orthography"]
# Fixed readings for steps where the analyser is often wrong.
FIXED = {"何か": "なにか"}
# Words the analyser reads one way where both readings are standard: (kanji, its reading, the other reading).
VARIANTS = [("日本", "にっぽん", "にほん"), ("私", "わたくし", "わたし"), ("何", "なん", "なに"), ("何", "なに", "なん"), ("開", "ひら", "あ"), ("開", "あ", "ひら"), ("間", "ま", "あいだ"), ("人", "にん", "じん"), ("母", "はは", "かあ"), ("父", "ちち", "とう"), ("富士山", "ふじやま", "ふじさん"), ("明日", "あす", "あした")]


def work(name): return paths.DATA / "explain_drafts" / name
def norm(s):
    import unicodedata  # full- and half-width digits and letters compare equal (１枚 = 1枚)
    return re.sub(r"[\s　【】]", "", unicodedata.normalize("NFKC", s or ""))
def hira(s): return "".join(chr(ord(c) - 0x60) if "ァ" <= c <= "ヶ" else c for c in s)
# The analyser misses sound changes in compounds (曜日 → び, 40分 → ぷん), so readings are compared without dakuten.
def plain_sound(s):
    import unicodedata
    return unicodedata.normalize("NFC", "".join(c for c in unicodedata.normalize("NFD", hira(s)) if c not in "゙゚"))
def read_json(f, default): return json.loads(f.read_text(encoding="utf-8")) if f.exists() else default
def write_json(f, x): f.parent.mkdir(parents=True, exist_ok=True); f.write_text(json.dumps(x, ensure_ascii=False, indent=1), encoding="utf-8")


def explained(items):
    done = read_json(paths.DATA / "explain.json", {})
    return {i for i, x in done.items() if i in items and x.get("for") == fingerprint(items[i])}


def brief_row(x, passages):
    row = {k: x[k] for k in ("id", "section", "mondai", "stem", "options", "answer")}
    row["explanation_en"] = x.get("explanation_en")
    if x.get("passage_id") in passages: row["passage"] = passages[x["passage_id"]]["text"]
    if x.get("script"): row["script"] = x["script"]
    return row


def queue(items):
    """Items still without an explanation: ones Anna got wrong first, then by ORDER, a passage's questions together."""
    done, wrong = explained(items), {t["item_id"] for t in read_attempts() if not t.get("correct")}
    skip = paths.DATA / "explain_drafts" / "skip.txt"  # broken items listed in item_problems.md, one id per line
    done |= set(skip.read_text(encoding="utf-8").split()) if skip.exists() else set()
    rank = lambda i: (i not in wrong, ORDER.index(items[i]["mondai"]), items[i].get("passage_id") or "", i)
    return sorted((i for i, x in items.items() if x.get("verified") and i not in done), key=rank)


def cmd_brief(a):
    items, passages = load_bank()
    if a.next: ids = queue(items)[:a.next]
    else:
        if a.mistakes: ids = list(dict.fromkeys(t["item_id"] for t in read_attempts() if not t.get("correct") and t.get("item_id") in items))
        else: ids = sorted(i for i, x in items.items() if x.get("verified") and (not a.section or x["section"] == a.section))
        ids = [i for i in ids if i not in explained(items)]
    # Keep a passage's questions together, so one writer reads each passage once.
    if not a.next: ids.sort(key=lambda i: (items[i]["section"], items[i].get("passage_id") or "", i))
    if a.next and ids and items[ids[-1]].get("passage_id"):  # finish the last passage rather than split it across batches
        rest = queue(items)[a.next:]; pid = items[ids[-1]]["passage_id"]
        ids += [i for i in rest if items[i].get("passage_id") == pid]
    d = work(a.name)
    if a.next: a.chunk = len(ids) or 1  # one brief per batch: the writer is this session, not parallel Codex calls
    for n in range(0, len(ids), a.chunk):
        write_json(d / f"brief-{n // a.chunk + 1:02d}.json", [brief_row(items[i], passages) for i in ids[n:n + a.chunk]])
    print(f"{len(ids)} items in {-(-len(ids) // a.chunk)} briefs → {d}")


def codex(brief, out):
    exe = shutil.which("codex") or "codex"
    task = (f"Follow the instructions in tools/explain_prompt.md. Brief: {brief.relative_to(paths.HOME).as_posix()}. "
            f"Output file: {out.relative_to(paths.HOME).as_posix()}.")
    r = subprocess.run([exe, "exec", "--skip-git-repo-check", "-s", "workspace-write", "-m", "gpt-6-luna", task],
                       cwd=paths.HOME, capture_output=True, text=True, encoding="utf-8", errors="replace")
    return f"{brief.name}: {'ok' if out.exists() else 'NO OUTPUT, exit ' + str(r.returncode)}"


def cmd_gen(a):
    d = work(a.name)
    if a.retry:
        failed = read_json(d / "failed.json", {})
        if not failed: return print("nothing to retry")
        items, passages = load_bank()
        k = len(list(d.glob("brief-retry-*.json"))) + 1
        write_json(d / f"brief-retry-{k}.json", [{**brief_row(items[i], passages), "previous_errors": e} for i, e in failed.items() if i in items])
    todo = [b for b in sorted(d.glob("brief-*.json")) if not (d / b.name.replace("brief-", "drafts-")).exists()]
    with ThreadPoolExecutor(a.jobs) as pool:
        for line in pool.map(lambda b: codex(b, d / b.name.replace("brief-", "drafts-")), todo): print(line)


class Reader:
    """Readings from the dictionary analyser (fugashi + unidic-lite) and the N4 word list, for soft checks."""
    def __init__(self):
        import fugashi
        self.tagger = fugashi.Tagger()
        self.words = {}
        with (paths.REPO / "data" / "vocabulary.csv").open(encoding="utf-8") as f:
            for row in csv.DictReader(f): self.words.setdefault(row["kanji"], set()).add(hira(row["reading"]))

    def tokens(self, text):
        out, at = [], 0
        for w in self.tagger(text):
            s = text.find(w.surface, at)
            if s < 0: continue
            k = getattr(w.feature, "kana", None)
            out.append((s, s + len(w.surface), hira(k) if k and k != "*" else w.surface)); at = s + len(w.surface)
        return out

    def furigana(self, text, rubies):
        """Add furigana to kanji outside braces, preferring readings from this entry's checked furigana (`rubies`):
        compounds as they are; a single kanji when the kana after it match, when it stands alone, or when the analyser
        often picks the other of two readings (VARIANTS). Anything else gets the analyser's reading."""
        compounds, single = dict(FIXED), {}
        for r in rubies:
            for m in RUBY.finditer(r):
                if len(m.group(1)) > 1: compounds.setdefault(m.group(1), m.group(2))
                else: single.setdefault(m.group(1), []).append((m.group(2), re.match("[ぁ-ゖ]*", r[m.end():]).group(0)))
        if compounds: text = re.sub("|".join(map(re.escape, sorted(compounds, key=len, reverse=True))), lambda m: self._ruby(m.group(0), compounds[m.group(0)]), text)
        ambiguous = {k for k, _, _ in VARIANTS}
        out, i = [], 0
        for m in list(RUBY.finditer(text)) + [None]:
            seg = text[i:m.start() if m else len(text)]; at = 0
            for s, e, r in self.tokens(seg):
                surf = seg[s:e]; out.append(seg[at:s]); at = e
                core = re.sub("[ぁ-ゖ]+$", "", surf); tail = surf[len(core):]; reading = r[:len(r) - len(tail)] if tail and r.endswith(hira(tail)) else r
                if not KANJI.search(core) or KANJI.sub("", core): out.append(surf); continue
                seen = single.get(core, []) if len(core) == 1 else []
                match = [x for x, after in seen if tail and after.startswith(tail)]
                if match or seen and (not tail or core in ambiguous): reading = (match or [seen[0][0]])[0]
                elif reading == surf: out.append(surf); continue
                out.append(f"{{{core}|{reading}}}{tail}")
            out.append(seg[at:])
            if m: out.append(m.group(0)); i = m.end()
        return "".join(out)

    @staticmethod
    def _ruby(surface, reading):
        """{base|reading} for a kanji word with kana after it: 何か + なにか → {何|なに}か."""
        core = re.sub("[ぁ-ゖ]+$", "", surface); tail = surface[len(core):]
        return f"{{{core}|{reading[:len(reading) - len(tail)]}}}{tail}"

    def disagreements(self, ruby):
        """Spans where the furigana reading differs from the analyser's reading."""
        text, segs, at, i = [], [], 0, 0
        for m in RUBY.finditer(ruby):
            text.append(ruby[i:m.start()]); at += m.start() - i
            segs.append((at, at + len(m.group(1)), hira(m.group(2)))); text.append(m.group(1)); at += len(m.group(1)); i = m.end()
        text.append(ruby[i:]); text = "".join(text)
        toks = self.tokens(text); out = []; seen = set()
        for t in toks:
            if not KANJI.search(text[t[0]:t[1]]) or t in seen: continue
            s, e = t[0], t[1]
            while True:  # grow the span until no furigana or token crosses its edge
                s2 = min([s] + [a for a, b, _ in segs if a < e and b > s] + [a for a, b, _ in toks if a < e and b > s])
                e2 = max([e] + [b for a, b, _ in segs if a < e and b > s] + [b for a, b, _ in toks if a < e and b > s])
                if (s2, e2) == (s, e): break
                s, e = s2, e2
            span = [x for x in toks if s <= x[0] and x[1] <= e]; seen.update(span)
            mine, p = "", s
            for a, b, r in sorted(x for x in segs if s <= x[0] and x[1] <= e):
                mine += hira(text[p:a]) + r; p = b
            mine += hira(text[p:e])
            theirs = "".join(r for _, _, r in span)
            alts = [theirs] + [theirs.replace(d, f, 1) for k, d, f in VARIANTS if k in text[s:e] and d in theirs]
            if all(plain_sound(mine) != plain_sound(t) for t in alts): out.append(f"{text[s:e]}: furigana {mine}, dictionary {theirs}")
        return out


def ruby_errors(label, ruby, expect=None):
    errs = []
    if not isinstance(ruby, str) or not ruby: return [f"{label}: missing"]
    for m in RUBY.finditer(ruby):
        if not KANJI.search(m.group(1)) or KANJI.sub("", m.group(1)): errs.append(f"{label}: furigana base {m.group(1)!r} is not only kanji")
        if not KANA.match(m.group(2)): errs.append(f"{label}: furigana {m.group(2)!r} is not kana")
    rest = RUBY.sub("", ruby)
    if re.search(r"[{}|]", rest): errs.append(f"{label}: broken furigana markup")
    if KANJI.search(rest): errs.append(f"{label}: kanji without furigana: {''.join(KANJI.findall(rest))}")
    if expect is not None and norm(plain(ruby)) != norm(expect): errs.append(f"{label}: text {norm(plain(ruby))!r} should be {norm(expect)!r}")
    return errs


def expected_sentence(x):
    """The sentence the furigana must spell, or None where only looser checks apply."""
    m, right = x["mondai"], x["options"][x["answer"] - 1]
    if m in ("grammar_form", "contextual") and BLANK.search(x["stem"]):
        parts = right.split("／") if len(BLANK.findall(x["stem"])) > 1 else [right]  # two blanks: option "A／B"
        stem = x["stem"]
        for part in parts: stem = BLANK.sub(part, stem, count=1)
        return stem
    if m == "orthography": return re.sub(r"【[^】]*】", right, x["stem"], count=1)
    if m == "usage": return right
    if m in ("sentence_composition", "text_grammar", "grammar_form", "contextual"): return None
    return x["stem"]


def check_one(x, e, source, reader):
    hard, soft = [], []
    if not isinstance(e, dict): return ["entry is not an object"], []
    want = expected_sentence(x)
    hard += ruby_errors("sentence", e.get("sentence"), want)
    if want is None and isinstance(e.get("sentence"), str):
        s = norm(plain(e["sentence"]))
        need = x["options"] if x["mondai"] == "sentence_composition" else [x["options"][x["answer"] - 1]]
        hard += [f"sentence: lacks {o!r}" for o in need if norm(o) not in s]
    if not str(e.get("translation_en") or "").strip(): hard.append("translation_en: missing")
    opts = e.get("options")
    if not isinstance(opts, list) or len(opts) != len(x["options"]): hard.append("options: need one entry per option")
    else:
        for n, (o, src) in enumerate(zip(opts, x["options"]), 1):
            if not isinstance(o, dict) or not str(o.get("en") or "").strip(): hard.append(f"option {n}: missing meaning"); continue
            hard += ruby_errors(f"option {n}", o.get("ruby"), src)
    words = e.get("words") or []
    if not isinstance(words, list) or not words: hard.append("words: missing")
    else:
        for w in words:
            if not isinstance(w, dict) or not w.get("w") or not w.get("en") or not KANA.match(hira(str(w.get("r") or ""))): hard.append(f"words: bad entry {w!r}"); continue
            known = reader.words.get(w["w"])
            if known and hira(w["r"]) not in known: soft.append(f"word {w['w']}: {w['r']}, word list says {'/'.join(sorted(known))}")
    ev = e.get("evidence") or []
    needs = x["section"] in ("reading", "listening") or x["mondai"] == "text_grammar"
    if needs and not ev: hard.append("evidence: missing")
    for n, q in enumerate(ev if isinstance(ev, list) else [], 1):
        t = q.get("text") if isinstance(q, dict) else None
        if not t or "\n" in t or t not in (source or ""): hard.append(f"evidence {n}: not an exact one-line quote from the passage/script: {t!r}"); continue
        hard += ruby_errors(f"evidence {n}", q.get("ruby"), t)
        if not str(q.get("en") or "").strip(): hard.append(f"evidence {n}: missing translation")
    if not isinstance(e.get("steps"), list) or not e["steps"]: hard.append("steps: missing")
    if not hard:
        for label, r in [("sentence", e["sentence"])] + [(f"option {n}", o["ruby"]) for n, o in enumerate(opts, 1)] + [(f"evidence {n}", q["ruby"]) for n, q in enumerate(ev, 1)]:
            soft += [f"{label}: {d}" for d in reader.disagreements(r)]
    return hard, soft


def with_furigana(e, reader):
    """Steps are free text, so their kanji get furigana here rather than from the writer."""
    rubies = [e["sentence"], *[o["ruby"] for o in e["options"]], *[q["ruby"] for q in e.get("evidence") or []]]
    return [reader.furigana(t, rubies) for t in e["steps"]]


def cmd_status(a):
    items, _ = load_bank(); done = explained(items); todo = queue(items)
    wrong = {t["item_id"] for t in read_attempts() if not t.get("correct") and t.get("item_id") in items}
    print(f"explained {len(done)} of {sum(1 for x in items.values() if x.get('verified'))}; wrong answers without one: {len(wrong - done)}")
    for m in ORDER:
        n = sum(1 for x in items.values() if x.get("verified") and x["mondai"] == m)
        if n: print(f"  {m:22} {sum(1 for i in done if items[i]['mondai'] == m):4} / {n}")
    if todo: print(f"next: {todo[0]} ({items[todo[0]]['mondai']})")
    drafts = sorted(p.parent.name for p in (paths.DATA / "explain_drafts").glob("*/brief-*.json") if not (p.parent / p.name.replace("brief-", "drafts-")).exists())
    if drafts: print("briefs without drafts:", ", ".join(sorted(set(drafts))))


def cmd_steps(a):
    for i, e in read_json(paths.DATA / "explain.json", {}).items():
        if e.get("batch") == a.name: print(i, *[s for s in e["steps"] if "{" in s], sep="\n  ")


def cmd_check(a):
    d = work(a.name); items, passages = load_bank(); reader = Reader()
    drafts = {}
    for f in sorted(d.glob("drafts-*.json")):  # later files (retries) replace earlier drafts
        try: drafts.update(read_json(f, {}))
        except ValueError as err: print(f"{f.name}: not valid JSON ({err})")
    store = read_json(paths.DATA / "explain.json", {}); done = explained(items)
    failed, merged, waiting, lines = {}, [], [], [f"# Explanation check: {a.name}", ""]
    for i, e in drafts.items():
        if i in done and i not in a.accept: continue
        x = items.get(i)
        if not x: lines.append(f"- {i}: not in the bank"); continue
        source = passages.get(x.get("passage_id"), {}).get("text", "") + "\n" + (x.get("script") or "")
        hard, soft = check_one(x, e, source, reader)
        if hard: failed[i] = hard; lines += [f"## {i} — FAILED", *[f"- {h}" for h in hard], ""]
        elif soft and i not in a.accept: waiting.append(i); lines += [f"## {i} — needs a look (--accept {i})", *[f"- {s}" for s in soft], ""]
        else:
            store[i] = {**e, "steps": with_furigana(e, reader), "for": fingerprint(x), "checked": date.today().isoformat(), "batch": a.name}; merged.append(i)
    write_json(paths.DATA / "explain.json", store); write_json(d / "failed.json", failed)
    (d / "report.md").write_text("\n".join(lines), encoding="utf-8")
    print(f"merged {len(merged)}, waiting for a look {len(waiting)}, failed {len(failed)} → {d / 'report.md'}")


def main():
    p = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter); sub = p.add_subparsers(dest="cmd", required=True)
    b = sub.add_parser("brief"); b.add_argument("name"); g = b.add_mutually_exclusive_group(required=True)
    g.add_argument("--mistakes", action="store_true"); g.add_argument("--all", action="store_true"); g.add_argument("--next", type=int)
    b.add_argument("--section"); b.add_argument("--chunk", type=int, default=CHUNK)
    g2 = sub.add_parser("gen"); g2.add_argument("name"); g2.add_argument("--jobs", type=int, default=3); g2.add_argument("--retry", action="store_true")
    c = sub.add_parser("check"); c.add_argument("name"); c.add_argument("--accept", nargs="*", default=[])
    sub.add_parser("status"); sub.add_parser("steps").add_argument("name")
    a = p.parse_args(); sys.stdout.reconfigure(encoding="utf-8")
    {"brief": cmd_brief, "gen": cmd_gen, "check": cmd_check, "status": cmd_status, "steps": cmd_steps}[a.cmd](a)


if __name__ == "__main__":
    main()
