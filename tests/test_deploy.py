import re
from pathlib import Path

REPO = Path(__file__).resolve().parents[1]
APP = REPO / "deploy" / "ha-app"


def test_the_image_copies_files_that_exist():
    sources = [s for line in (APP / "Dockerfile").read_text(encoding="utf-8").splitlines() if line.startswith("COPY ") for s in line.split()[1:-1]]
    missing = [s for s in sources if not (APP / s).exists() and not (REPO / s).exists()]
    assert sources and missing == []


def test_the_image_installs_only_the_server_requirements():
    assert re.findall(r"pip install .*-r (\S+)", (APP / "Dockerfile").read_text(encoding="utf-8")) == ["requirements-server.txt"]
    assert (REPO / "requirements.txt").read_text(encoding="utf-8").splitlines()[0] == "-r requirements-server.txt"


def test_every_app_option_reaches_the_server():
    config = (APP / "config.yaml").read_text(encoding="utf-8")
    options = re.findall(r"^  (\w+): \"\"$", config, re.M)
    start = (APP / "start.py").read_text(encoding="utf-8")
    run = (APP / "run.sh").read_text(encoding="utf-8")
    assert options and all(f'options.get("{o}")' in start or f"options.py {o}" in run for o in options)


def test_the_auth_key_never_reaches_the_server_or_the_log():
    run = (APP / "run.sh").read_text(encoding="utf-8")
    assert "ts_authkey" not in (APP / "start.py").read_text(encoding="utf-8")
    assert "--auth-key=file:" in run and "set -x" not in run and "cat /tmp/ts_authkey" not in run


def test_the_portal_binds_loopback_behind_tailscale_serve():
    start = (APP / "start.py").read_text(encoding="utf-8")
    assert '"JLPT_AUTH": "tailscale"' in start and '"JLPT_BIND": "127.0.0.1"' in start
    assert "serve --bg 8080" in (APP / "run.sh").read_text(encoding="utf-8")
