import hashlib
import io
import json
import sys
import tarfile
from datetime import date
from pathlib import Path, PurePosixPath

import pytest

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "tools"))
import pi


def tree(root: Path) -> dict:
    return {f.relative_to(root).as_posix(): hashlib.sha256(f.read_bytes()).hexdigest() for f in sorted(root.rglob("*")) if f.is_file()} if root.exists() else {}


def write(root: Path, files: dict) -> Path:
    for name, text in files.items():
        (root / name).parent.mkdir(parents=True, exist_ok=True)
        (root / name).write_text(text, encoding="utf-8")
    return root


@pytest.fixture
def pi_dir(tmp_path):
    config = tmp_path / "pi" / "app_configs" / "local_jlpt_portal"
    write(config, {"learners.json": '{"learners": []}', "learners/anna/attempts.jsonl": "{}\n", "learners/yoko/runs.jsonl": "{}\n",
                   "logs/access-2026-11.jsonl": "{}\n", "data/bank/old.json": "[]", "data/tracks/de-work/bank/words/u.json": "[1]"})
    return tmp_path / "pi"


def app(server_source: str) -> bytes:
    with io.BytesIO() as buf:
        with tarfile.open(fileobj=buf, mode="w") as tar:
            for name, text in {"server.py": server_source, "Dockerfile": "FROM python:3.13-slim\n"}.items():
                raw = text.encode()
                info = tarfile.TarInfo(name)
                info.size = len(raw)
                tar.addfile(info, io.BytesIO(raw))
        return buf.getvalue()


SOURCES = {"v1": app("print('v1')\n"), "v2": app("print('v2')\n"), "broken": app("def broken(:\n")}


def test_push_content_never_touches_learner_data(tmp_path, pi_dir):
    home = write(tmp_path / "home", {"data/bank/vocab/a.json": "[2]", "data/tracks/de-work/bank/words/u.json": "[3]", "data/explain.json": "{}",
                                     "learners/anna/attempts.jsonl": "FROM THE PC\n", "learners.json": '{"evil": true}', "logs/x.jsonl": "pc\n"})
    config = pi_dir / "app_configs" / "local_jlpt_portal"
    learner_data = lambda: {k: v for k, v in tree(config).items() if k.startswith(("learners", "logs"))}
    before = learner_data()
    pushed = pi.push_content(pi.Folder(pi_dir), home)
    assert learner_data() == before
    assert pushed == ["data/bank", "data/tracks", "data/explain.json"]
    assert tree(config / "data") == tree(home / "data")


@pytest.mark.parametrize("bad", [("learners",), ("learners.json",), ("data/../learners",), ("logs",)])
def test_content_list_cannot_name_learner_data(tmp_path, monkeypatch, bad):
    monkeypatch.setattr(pi, "CONTENT", bad)
    write(tmp_path, {"learners/a.txt": "x", "learners.json": "{}", "logs/a": "x", "data/x": "x"})
    with pytest.raises(SystemExit):
        pi.content_names(tmp_path)


def test_push_audio_sends_only_new_or_changed_files(tmp_path, pi_dir):
    audio = write(tmp_path / "audio", {"a.mp3": "aaaa", "sub/b.mp3": "bb"})
    target = pi.Folder(pi_dir)
    assert pi.push_audio(target, audio) == ["a.mp3", "sub/b.mp3"]
    assert pi.push_audio(target, audio) == []
    (audio / "sub" / "b.mp3").write_text("bbb", encoding="utf-8")
    write(audio, {"c.mp3": "c"})
    assert pi.push_audio(target, audio) == ["c.mp3", "sub/b.mp3"]
    assert tree(pi_dir / "media" / "jlpt" / "audio") == tree(audio)


def test_pull_copies_learner_data_and_keeps_30_days(tmp_path, pi_dir):
    into = tmp_path / "backup" / "pi"
    write(into, {"2026-10-08/old.txt": "x", "2026-10-09/keep.txt": "x", "notes/keep.txt": "x"})
    dest = pi.pull(pi.Folder(pi_dir), into, today=date(2026, 11, 8))
    assert sorted(tree(dest)) == ["learners.json", "learners/anna/attempts.jsonl", "learners/yoko/runs.jsonl", "logs/access-2026-11.jsonl"]
    assert sorted(p.name for p in into.iterdir()) == ["2026-10-09", "2026-11-08", "notes"]


def test_pull_refuses_paths_outside_the_backup(tmp_path):
    buf = io.BytesIO()
    with tarfile.open(fileobj=buf, mode="w") as tar:
        info = tarfile.TarInfo("../escape.txt")
        info.size = 1
        tar.addfile(info, io.BytesIO(b"x"))
    with pytest.raises(tarfile.FilterError):
        pi.untar(buf.getvalue(), tmp_path / "dest")
    assert not (tmp_path / "escape.txt").exists()


def test_deploy_rolls_back_a_broken_tag(pi_dir):
    target = pi.Folder(pi_dir)
    source = SOURCES.__getitem__
    assert pi.deploy(target, "v1", source, wait_s=0, poll_s=0)
    assert pi.deploy(target, "v2", source, wait_s=0, poll_s=0)
    assert not pi.deploy(target, "broken", source, wait_s=0, poll_s=0)
    assert target.read(pi.APP / ".tag").strip() == "v2"
    assert (pi_dir / "local_apps" / "jlpt_portal" / "server.py").read_text(encoding="utf-8") == "print('v2')\n"
    assert json.loads(target.ha("apps", "info", pi.SLUG))["data"]["state"] == "started"


def test_deploy_builds_the_app_from_git_with_lf(pi_dir):
    assert pi.deploy(pi.Folder(pi_dir), "HEAD", wait_s=0, poll_s=0)
    folder = pi_dir / "local_apps" / "jlpt_portal"
    assert (folder / "run.sh").read_bytes().startswith(b"#!/bin/sh\n") and b"\r" not in (folder / "run.sh").read_bytes()
    assert {"Dockerfile", "config.yaml", "server.py", "engine", "web", "tracks", ".tag"} <= {p.name for p in folder.iterdir()}


def test_dry_run_changes_nothing(tmp_path, pi_dir):
    before = tree(pi_dir)
    home = write(tmp_path / "home", {"data/bank/a.json": "[9]"})
    audio = write(tmp_path / "audio", {"new.mp3": "n"})
    target = pi.DryRun(pi.Folder(pi_dir))
    pi.push_content(target, home)
    pi.push_audio(target, audio)
    pi.deploy(target, "v1", SOURCES.__getitem__, wait_s=0, poll_s=0)
    assert tree(pi_dir) == before


def test_ssh_uses_the_key_by_path_and_scoped_commands(tmp_path):
    calls = []

    def runner(cmd, input=None, capture_output=True):
        calls.append(cmd)
        return type("Done", (), {"returncode": 0, "stdout": b""})()

    key = tmp_path / "jlpt_pi_ed25519"
    key.write_text("PRIVATE KEY MATERIAL", encoding="utf-8")
    ssh = pi.Ssh("homeassistant.local", "root", key, runner)
    home = write(tmp_path / "home", {"data/bank/a.json": "[1]", "data/explain.json": "{}"})
    pi.push_content(ssh, home)
    assert calls[0][:8] == ["ssh", "-i", str(key), "-o", "IdentitiesOnly=yes", "-o", "BatchMode=yes", "root@homeassistant.local"]
    script = calls[0][-1]
    assert "PRIVATE KEY" not in " ".join(calls[0])
    assert script == "mkdir -p /app_configs/local_jlpt_portal && rm -rf /app_configs/local_jlpt_portal/data/bank && tar -xf - -C /app_configs/local_jlpt_portal"


def test_cli_against_a_target_folder(tmp_path, pi_dir, capsys):
    audio = write(tmp_path / "audio", {"a.mp3": "a"})
    assert pi.main(["--target-dir", str(pi_dir), "push-audio", "--audio", str(audio)]) == 0
    assert pi.main(["--target-dir", str(pi_dir), "push-audio", "--audio", str(audio)]) == 0
    assert capsys.readouterr().out.splitlines()[-1] == "audio: 0 of 1 files sent"
