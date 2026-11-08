import io
import json
import os
import subprocess
import sys
import tempfile
import time
import zipfile
from pathlib import Path

REPO = Path(__file__).resolve().parents[1]
HARNESS = "1da3c74"
CLOCK_FIX = [("    from engine import explain, leitner, mock, paths, select, simulate\n",
              "    from engine import explain, leitner, mock, paths, report, select, simulate\n"),
             ('(leitner, "datetime", FixedDatetime), (server, "datetime", FixedDatetime),',
              '(leitner, "datetime", FixedDatetime), (report, "datetime", FixedDatetime), (server, "datetime", FixedDatetime),')]


def snapshot(out: str) -> None:
    sys.path.insert(0, os.getcwd())
    from tests import golden_n4 as g
    cases = {"bank": (g.bank, []), "model": (g.model, []), "state": (g.state, []), "mocks": (g.mocks, []), "report": (g.report, []),
             "explanations": (g.explanations, []), "health": (g.health, []), "api": (g.api, []),
             "run_practice_mixed": (g.run, ["practice", "mixed", 20, 7]), "run_timed_mixed": (g.run, ["timed", "mixed", 30, 11]),
             "run_mistakes": (g.run, ["practice", "mistakes", 10, 4]), "run_listening": (g.run, ["practice", "listening", 10, 5]),
             "run_reading": (g.run, ["drill", "reading", 6, 2])}
    result = {}
    for k, (f, a) in cases.items():
        t = time.time()
        try:
            result[k] = f(*a)
        except Exception as e:
            result[k] = {"error": f"{type(e).__name__}: {e}"}
        print(k, round(time.time() - t, 1), file=sys.stderr)
    Path(out).write_text(json.dumps(result, ensure_ascii=False, sort_keys=True, default=str), encoding="utf-8")


def git(*args: str) -> bytes:
    return subprocess.run(["git", "-C", str(REPO), *args], capture_output=True, check=True).stdout


def export(ref: str, dest: Path) -> None:
    zipfile.ZipFile(io.BytesIO(git("archive", "--format=zip", ref))).extractall(dest)
    harness = git("show", f"{HARNESS}:tests/golden_n4.py").decode("utf-8")
    for old, new in CLOCK_FIX:
        if harness.count(old) != 1:
            raise SystemExit(f"harness {HARNESS} no longer matches the clock fix: {old!r}")
        harness = harness.replace(old, new)
    (dest / "tests").mkdir(exist_ok=True)
    (dest / "tests" / "golden_n4.py").write_text(harness, encoding="utf-8")


def run(cwd: Path, out: Path) -> None:
    subprocess.run([sys.executable, str(Path(__file__).resolve()), "--snapshot", str(out)], cwd=cwd, check=True, env={**os.environ, "N4_REAL_HOME": os.environ["N4_REAL_HOME"]})


def differences(a, b, path="$"):
    if type(a) is not type(b):
        return [path]
    if isinstance(a, dict):
        return [p for k in sorted(set(a) | set(b)) for p in (differences(a[k], b[k], f"{path}.{k}") if k in a and k in b else [f"{path}.{k}"])]
    if isinstance(a, list):
        return ([f"{path}[len]"] if len(a) != len(b) else []) + [p for i, (x, y) in enumerate(zip(a, b)) for p in differences(x, y, f"{path}[{i}]")]
    return [] if a == b else [path]


def compare(ref: str) -> int:
    if not os.environ.get("N4_REAL_HOME"):
        raise SystemExit("set N4_REAL_HOME to the folder with Anna's real data")
    with tempfile.TemporaryDirectory() as tmp:
        tmp = Path(tmp)
        export(ref, tmp / "base")
        run(tmp / "base", tmp / "base.json")
        run(REPO, tmp / "branch.json")
        base, branch = (tmp / "base.json").read_bytes(), (tmp / "branch.json").read_bytes()
    if base == branch:
        print(f"identical: {ref} and the working tree give byte-identical outputs on the real data")
        return 0
    diff = differences(json.loads(base), json.loads(branch))
    print(f"DIFFERENT: {len(diff)} values differ between {ref} and the working tree", *diff[:40], sep="\n")
    return 1


if __name__ == "__main__":
    if len(sys.argv) == 3 and sys.argv[1] == "--snapshot":
        snapshot(sys.argv[2])
    elif len(sys.argv) in (2, 3) and sys.argv[1] == "--compare":
        sys.exit(compare(sys.argv[2] if len(sys.argv) == 3 else "main"))
    else:
        raise SystemExit("usage: N4_REAL_HOME=<data> python tools/golden_real.py --compare [ref, default main]\n"
                         "       N4_REAL_HOME=<data> [N4_REAL_DATA=<learner data, e.g. backup/pi/<date>/learners/anna>] python tools/golden_real.py --snapshot <out.json>")
