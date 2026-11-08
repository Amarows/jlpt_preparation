import argparse
import io
import json
import os
import py_compile
import re
import secrets
import shlex
import shutil
import subprocess
import sys
import tarfile
import tempfile
import time
from datetime import date, timedelta
from pathlib import Path, PurePosixPath

REPO = Path(__file__).resolve().parents[1]
sys.path[:0] = [str(REPO / "tools"), str(REPO)]
from export_app import export, resolve
from server import START

SLUG = "local_jlpt_portal"
APP = PurePosixPath("/local_apps/jlpt_portal")
CONFIG = PurePosixPath("/app_configs/local_jlpt_portal")
AUDIO = PurePosixPath("/media/jlpt/audio")
CONTENT = ("data/bank", "data/tracks", "data/explain.json", "data/vocabulary.csv")
PULLED = ("learners.json", "learners", "logs")
FORBIDDEN = ("learners", "learners.json", "logs")
KEEP_DAYS = 30
BACKUP = REPO / "backup" / "pi"


def say(*parts):
    print(*parts, flush=True)


def tar_of(root: Path, names: list[str], extra: dict | None = None) -> bytes:
    buf = io.BytesIO()
    with tarfile.open(fileobj=buf, mode="w") as tar:
        for name in names:
            tar.add(root / name, arcname=name)
        for name, text in (extra or {}).items():
            raw = text.encode("utf-8")
            info = tarfile.TarInfo(name)
            info.size = len(raw)
            tar.addfile(info, io.BytesIO(raw))
    return buf.getvalue()


def untar(data: bytes, dest: Path) -> list[str]:
    dest.mkdir(parents=True, exist_ok=True)
    if not data:
        return []
    with tarfile.open(fileobj=io.BytesIO(data)) as tar:
        names = tar.getnames()
        tar.extractall(dest, filter="data")
    return names


def member(data: bytes, name: str) -> str | None:
    with tarfile.open(fileobj=io.BytesIO(data)) as tar:
        try:
            return tar.extractfile(name).read().decode("utf-8")
        except (KeyError, AttributeError):
            return None


def version_of(config_yaml: str | None) -> str | None:
    m = re.search(r'^version:\s*"?([^"\n]+?)"?\s*$', config_yaml or "", re.M)
    return m.group(1) if m else None


def content_names(home: Path) -> list[str]:
    names = [n for n in CONTENT if (home / n).exists()]
    for n in names:
        parts = PurePosixPath(n).parts
        if parts[0] != "data" or ".." in parts or parts[0] in FORBIDDEN:
            raise SystemExit(f"refusing to push {n}: only data/ content is pushed")
    return names


class Folder:
    def __init__(self, root: Path):
        self.root = Path(root)

    def local(self, path: PurePosixPath) -> Path:
        return self.root / str(path).lstrip("/")

    def read(self, path):
        f = self.local(path)
        return f.read_text(encoding="utf-8") if f.is_file() else None

    def write(self, path, text):
        self.local(path).parent.mkdir(parents=True, exist_ok=True)
        self.local(path).write_text(text, encoding="utf-8")

    def put(self, data: bytes, dest, clear=()):
        for name in clear:
            target = self.local(dest / name)
            shutil.rmtree(target) if target.is_dir() else target.unlink(missing_ok=True)
        untar(data, self.local(dest))

    def replace_dir(self, data: bytes, dest):
        shutil.rmtree(self.local(dest), ignore_errors=True)
        untar(data, self.local(dest))

    def get(self, src, names) -> bytes:
        root = self.local(src)
        present = [n for n in names if (root / n).exists()]
        return tar_of(root, present) if present else b""

    def sizes(self, src) -> dict:
        root = self.local(src)
        return {f.relative_to(root).as_posix(): f.stat().st_size for f in root.rglob("*") if f.is_file()} if root.is_dir() else {}

    def _state(self) -> dict:
        f = self.local(PurePosixPath("/fake_ha/state.json"))
        return json.loads(f.read_text(encoding="utf-8")) if f.is_file() else {"state": "unknown", "version": None, "log": "", "store": None, "auto_start": True}

    def _save(self, state):
        self.write(PurePosixPath("/fake_ha/state.json"), json.dumps(state))

    def ha(self, *args) -> str:
        app, s = self.local(APP), self._state()
        if args == ("store", "reload"):
            s["store"] = version_of(self.read(APP / "config.yaml"))
        elif args[:2] in (("apps", "rebuild"), ("apps", "update")):
            if args[1] == "rebuild" and s["store"] != s["version"]:
                raise SystemExit("remote command failed (1): ha …")
            try:
                py_compile.compile(str(app / "server.py"), doraise=True)
                ok = (app / "Dockerfile").is_file()
            except (py_compile.PyCompileError, FileNotFoundError):
                ok = False
            build = (app / "BUILD").read_text(encoding="utf-8").strip() if (app / "BUILD").is_file() else "dev"
            s.update(version=s["store"], state=("started" if s["auto_start"] else "stopped") if ok else "error",
                     log=s["log"] + (f"{START} 127.0.0.1:8080 as tailscale build {build}\n" if ok and s["auto_start"] else "" if ok else "Traceback: SyntaxError\n"), ok=ok, build=build)
        elif args[:2] == ("apps", "start"):
            if s.get("ok"):
                s.update(state="started", log=s["log"] + f"{START} 127.0.0.1:8080 as tailscale build {s['build']}\n")
        elif args[:2] == ("apps", "info"):
            return json.dumps({"result": "ok", "data": {"state": s["state"], "version": s["version"]}})
        elif args[:2] == ("apps", "logs"):
            return s["log"]
        else:
            raise ValueError(args)
        self._save(s)
        return ""


class Ssh:
    def __init__(self, host: str, user: str, key: Path, runner=subprocess.run):
        self.base = ["ssh", "-i", str(key), "-o", "IdentitiesOnly=yes", "-o", "BatchMode=yes", f"{user}@{host}"]
        self.runner = runner

    def sh(self, script: str, data: bytes | None = None) -> bytes:
        done = self.runner(self.base + [script], input=data, capture_output=True)
        if done.returncode:
            raise SystemExit(f"remote command failed ({done.returncode}): {script.split()[0]} …")
        return done.stdout

    def read(self, path):
        out = self.sh(f"cat {shlex.quote(str(path))} 2>/dev/null || true").decode("utf-8")
        return out or None

    def write(self, path, text):
        self.sh(f"mkdir -p {shlex.quote(str(path.parent))} && cat > {shlex.quote(str(path))}", text.encode("utf-8"))

    def put(self, data, dest, clear=()):
        q = shlex.quote(str(dest))
        wipe = "".join(f"rm -rf {shlex.quote(str(dest / n))} && " for n in clear)
        self.sh(f"mkdir -p {q} && {wipe}tar -xf - -C {q}", data)

    def replace_dir(self, data, dest):
        q, new = shlex.quote(str(dest)), shlex.quote(f"{dest}.new")
        self.sh(f"rm -rf {new} && mkdir -p {new} && tar -xf - -C {new} && rm -rf {q} && mv {new} {q}", data)

    def get(self, src, names) -> bytes:
        q = shlex.quote(str(src))
        listed = " ".join(shlex.quote(n) for n in names)
        return self.sh(f"cd {q} && set -- && for n in {listed}; do [ -e \"$n\" ] && set -- \"$@\" \"$n\"; done; [ $# -gt 0 ] && tar -cf - \"$@\" || true")

    def sizes(self, src) -> dict:
        q = shlex.quote(str(src))
        out = self.sh(f"[ -d {q} ] && cd {q} && find . -type f -exec stat -c '%n\t%s' {{}} + || true").decode("utf-8")
        return {line.split("\t")[0][2:]: int(line.split("\t")[1]) for line in out.splitlines() if "\t" in line}

    def ha(self, *args) -> str:
        return self.sh("ha " + " ".join(shlex.quote(a) for a in args)).decode("utf-8")


class DryRun:
    def __init__(self, target):
        self.target = target

    def __getattr__(self, name):
        if name in ("read", "sizes", "get"):
            return getattr(self.target, name)
        if name == "ha":
            return self._ha
        return lambda *args, **kw: say(f"dry-run: {name}", *[a for a in args if not isinstance(a, bytes)], *(f"({len(a)} bytes)" for a in args if isinstance(a, bytes)))

    def _ha(self, *args):
        if args[:2] in (("apps", "info"), ("apps", "logs")):
            return self.target.ha(*args)
        say("dry-run: ha", *args)
        return ""


def build(sha: str, marker: str) -> bytes:
    with tempfile.TemporaryDirectory() as tmp:
        export(Path(tmp), sha)
        (Path(tmp) / "BUILD").write_bytes(marker.encode("ascii") + b"\n")
        return tar_of(Path(tmp), sorted(p.name for p in Path(tmp).iterdir()))


def info(target) -> dict:
    try:
        return json.loads(target.ha("apps", "info", SLUG, "--raw-json") or "{}").get("data", {})
    except ValueError:
        return {}


def started(target, marker: str, wait_s: float, poll_s: float) -> bool:
    deadline = time.monotonic() + wait_s
    line = f"build {marker}"
    while True:
        state = info(target).get("state")
        if state == "started" and line in target.ha("apps", "logs", SLUG):
            return True
        if state == "error" or time.monotonic() >= deadline:
            return False
        time.sleep(poll_s)


def install(target, data: bytes, sha: str, marker: str, wait_s: float, poll_s: float, dry: bool) -> bool:
    installed = info(target).get("version")
    target.replace_dir(data, APP)
    target.write(APP / ".tag", sha + "\n")
    target.ha("store", "reload")
    new = version_of(member(data, "config.yaml"))
    target.ha("apps", "update" if new != installed else "rebuild", SLUG)
    if dry:
        say(f"dry-run: would wait for '{START} … build {marker}'")
        return True
    if info(target).get("state") != "started":
        target.ha("apps", "start", SLUG)
    return started(target, marker, wait_s, poll_s)


def deploy(target, ref: str, source=build, wait_s=180.0, poll_s=3.0, first=False, pull_into: Path | None = BACKUP, dry=False) -> bool:
    sha = resolve(ref)
    previous = (target.read(APP / ".tag") or "").strip() or None
    if previous is None and not first:
        say("no .tag on the target: run the first deploy with --first")
        return False
    if pull_into is not None:
        pull(target, pull_into) if not dry else say("dry-run: pull before deploy")
    say(f"deploy {ref} = {sha} (previous: {previous or 'none'})")
    marker = f"{sha[:12]}-{secrets.token_hex(4)}"
    if install(target, source(sha, marker), sha, marker, wait_s, poll_s, dry):
        say(f"deployed {sha}: app started")
        return True
    say(f"deploy {sha} FAILED: the app did not start with build {marker}")
    if previous and previous != sha:
        say(f"rolling back to {previous}")
        back = f"{previous[:12]}-{secrets.token_hex(4)}"
        say("rolled back" if install(target, source(previous, back), previous, back, wait_s, poll_s, dry) else "ROLLBACK FAILED as well")
    return False


def push_content(target, home: Path) -> list[str]:
    names = content_names(home)
    target.put(tar_of(home, names), CONFIG, clear=[n for n in names if (home / n).is_dir()])
    say(f"pushed content: {', '.join(names)}")
    return names


def push_audio(target, audio: Path) -> list[str]:
    have = target.sizes(AUDIO)
    local = {f.relative_to(audio).as_posix(): f.stat().st_size for f in audio.rglob("*") if f.is_file()}
    send = sorted(n for n, size in local.items() if have.get(n) != size)
    if send:
        target.put(tar_of(audio, send), AUDIO)
    say(f"audio: {len(send)} of {len(local)} files sent")
    return send


def pull(target, into: Path, today: date | None = None) -> Path:
    today = today or date.today()
    into.mkdir(parents=True, exist_ok=True)
    dest = into / today.isoformat()
    fresh = into / f".incoming-{today.isoformat()}-{secrets.token_hex(4)}"
    names = untar(target.get(CONFIG, list(PULLED)), fresh)
    old = into / f".replaced-{today.isoformat()}-{secrets.token_hex(4)}"
    if dest.exists():
        dest.rename(old)
    fresh.rename(dest)
    shutil.rmtree(old, ignore_errors=True)
    cutoff = today - timedelta(days=KEEP_DAYS)
    for folder in into.iterdir():
        try:
            day = date.fromisoformat(folder.name)
        except ValueError:
            continue
        if day < cutoff and folder.is_dir():
            shutil.rmtree(folder)
    say(f"pulled {len(names)} entries to {dest}")
    return dest


def main(argv=None) -> int:
    p = argparse.ArgumentParser(prog="pi.py", description="Deploy the portal to the Pi and move content and learner data.")
    p.add_argument("--host", default="homeassistant.local")
    p.add_argument("--user", default="root")
    p.add_argument("--key", default=str(Path.home() / ".ssh" / "jlpt_pi_ed25519"))
    p.add_argument("--target-dir", help="a local folder standing in for the Pi (tests and rehearsals)")
    p.add_argument("--dry-run", action="store_true", help="read from the target but change nothing")
    sub = p.add_subparsers(dest="command", required=True)
    d = sub.add_parser("deploy")
    d.add_argument("ref")
    d.add_argument("--first", action="store_true", help="the target has no .tag yet: deploy without a rollback target")
    d.add_argument("--no-pull", action="store_true", help="skip the pull of learner data before deploying")
    d.add_argument("--into", default=str(BACKUP))
    sub.add_parser("push-content").add_argument("--home", default=os.environ.get("JLPT_HOME") or str(REPO))
    sub.add_parser("push-audio").add_argument("--audio", default=os.environ.get("JLPT_AUDIO") or str(Path(os.environ.get("JLPT_HOME") or REPO) / "audio"))
    sub.add_parser("pull").add_argument("--into", default=str(BACKUP))
    a = p.parse_args(argv)
    target = Folder(Path(a.target_dir)) if a.target_dir else Ssh(a.host, a.user, Path(a.key))
    target = DryRun(target) if a.dry_run else target
    if a.command == "deploy":
        return 0 if deploy(target, a.ref, first=a.first, pull_into=None if a.no_pull else Path(a.into), dry=a.dry_run) else 1
    if a.command == "push-content":
        push_content(target, Path(a.home))
    elif a.command == "push-audio":
        push_audio(target, Path(a.audio))
    elif a.command == "pull" and not a.dry_run:
        pull(target, Path(a.into))
    else:
        say("dry-run: pull", CONFIG, "->", Path(a.into) / date.today().isoformat())
    return 0


if __name__ == "__main__":
    sys.exit(main())
