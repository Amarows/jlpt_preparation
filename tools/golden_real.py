import json, sys, time
sys.path.insert(0, ".")
from tests import golden_n4 as g
cases = {"bank": (g.bank, []), "model": (g.model, []), "state": (g.state, []), "mocks": (g.mocks, []), "report": (g.report, []),
         "explanations": (g.explanations, []), "health": (g.health, []), "api": (g.api, []),
         "run_practice_mixed": (g.run, ["practice", "mixed", 20, 7]), "run_timed_mixed": (g.run, ["timed", "mixed", 30, 11]),
         "run_mistakes": (g.run, ["practice", "mistakes", 10, 4]), "run_listening": (g.run, ["practice", "listening", 10, 5]),
         "run_reading": (g.run, ["drill", "reading", 6, 2])}
out = {}
for k, (f, a) in cases.items():
    t = time.time()
    try: out[k] = f(*a)
    except Exception as e: out[k] = {"error": f"{type(e).__name__}: {e}"}
    print(k, round(time.time() - t, 1), file=sys.stderr)
open(sys.argv[1], "w", encoding="utf-8").write(json.dumps(out, ensure_ascii=False, sort_keys=True, default=str))
