import subprocess
import sys
from pathlib import Path

REPO = Path(__file__).resolve().parents[1]
APP = "deploy/ha-app"
CODE = ["server.py", "engine", "web", "tracks", "data/vocabulary.csv", "requirements-server.txt"]
BINARY = {".png", ".jpg", ".jpeg", ".gif", ".ico", ".woff", ".woff2", ".mp3"}


def git(*args: str) -> bytes:
    return subprocess.run(["git", "-C", str(REPO), *args], capture_output=True, check=True).stdout


def resolve(ref: str) -> str:
    return git("rev-parse", "--verify", f"{ref}^{{commit}}").decode("ascii").strip()


def export(dest: Path, ref: str = "HEAD") -> list[str]:
    if dest.exists() and any(dest.iterdir()):
        raise SystemExit(f"{dest} must be empty")
    ref = resolve(ref)
    names = git("ls-tree", "-r", "--name-only", ref, "--", APP, *CODE).decode("utf-8").splitlines()
    for name in names:
        data = git("cat-file", "blob", f"{ref}:{name}")
        if Path(name).suffix.lower() not in BINARY:
            data = data.replace(b"\r\n", b"\n")
        target = dest / (name[len(APP) + 1:] if name.startswith(APP + "/") else name)
        target.parent.mkdir(parents=True, exist_ok=True)
        target.write_bytes(data)
    (dest / "BUILD").write_bytes(ref.encode("ascii") + b"\n")
    return names


if __name__ == "__main__":
    if len(sys.argv) not in (2, 3):
        raise SystemExit("usage: python tools/export_app.py <empty folder> [git ref]  ->  copy the folder to /local_apps/jlpt_portal on the Pi")
    done = export(Path(sys.argv[1]), *sys.argv[2:])
    print(f"{len(done)} files exported with LF line endings to {sys.argv[1]}")
