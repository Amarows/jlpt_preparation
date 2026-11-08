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
    assert options and all(f'options.get("{o}")' in start for o in options)
