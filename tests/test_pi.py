import hashlib
import io
import json
import os
import shutil
import subprocess
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


def app(server_source: str, marker: str | None, version: str = "0.2.0") -> bytes:
    files = {"server.py": server_source, "Dockerfile": "FROM python:3.13-slim\n", "config.yaml": f'name: x\nversion: "{version}"\nslug: jlpt_portal\n'}
    files.update({"BUILD": marker + "\n"} if marker else {})
    with io.BytesIO() as buf:
        with tarfile.open(fileobj=buf, mode="w") as tar:
            for name, text in files.items():
                raw = text.encode()
                info = tarfile.TarInfo(name)
                info.size = len(raw)
                tar.addfile(info, io.BytesIO(raw))
        return buf.getvalue()


V1, V2, BROKEN = (pi.resolve(r) for r in ("HEAD~2", "HEAD~1", "HEAD"))
OLD = pi.resolve("0867b65")


def is_modern(sha):
    return sha != OLD


def source(versions=None):
    code = {V1: "print('v1')\n", V2: "print('v2')\n", BROKEN: "def broken(:\n", OLD: "print('old')\n"}
    return lambda sha, marker: app(code[sha], marker if is_modern(sha) else None, (versions or {}).get(sha, "0.2.0"))


def fast(**kw):
    return {"wait_s": 0, "poll_s": 0, "pull_into": None, "is_modern": is_modern, **kw}


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


def test_deploy_needs_first_on_a_target_without_tag(pi_dir):
    target = pi.Folder(pi_dir)
    assert not pi.deploy(target, V1, source(), **fast())
    assert not (pi_dir / "local_apps").exists()
    assert pi.deploy(target, V1, source(), **fast(first=True))
    assert target.read(pi.APP / ".tag").strip() == V1


def test_tag_stores_the_full_commit_not_the_ref(pi_dir):
    target = pi.Folder(pi_dir)
    assert pi.deploy(target, "HEAD~2", source(), **fast(first=True))
    assert target.read(pi.APP / ".tag").strip() == V1 and len(V1) == 40


def test_deploy_rolls_back_a_broken_commit_and_ignores_old_start_lines(pi_dir):
    target = pi.Folder(pi_dir)
    assert pi.deploy(target, V1, source(), **fast(first=True))
    assert pi.deploy(target, V2, source(), **fast())
    assert pi.START in target.ha("apps", "logs", pi.SLUG)
    assert not pi.deploy(target, BROKEN, source(), **fast())
    assert target.read(pi.APP / ".tag").strip() == V2
    assert (pi_dir / "local_apps" / "jlpt_portal" / "server.py").read_text(encoding="utf-8") == "print('v2')\n"
    assert json.loads(target.ha("apps", "info", pi.SLUG))["data"]["state"] == "started"


def test_a_start_line_from_an_earlier_container_does_not_count(pi_dir):
    target = pi.Folder(pi_dir)
    assert pi.deploy(target, V1, source(), **fast(first=True))
    marker = target.ha("apps", "logs", pi.SLUG).rsplit("build ", 1)[1].strip()
    assert pi.started(target, marker, 0, 0)
    assert not pi.started(target, marker[:-1] + ("0" if marker[-1] != "0" else "1"), 0, 0)


def test_version_bump_updates_and_same_version_rebuilds(pi_dir):
    target = pi.Folder(pi_dir)
    versions = {V1: "0.2.0", V2: "0.3.0"}
    assert pi.deploy(target, V1, source(versions), **fast(first=True))
    assert pi.deploy(target, V2, source(versions), **fast())
    assert json.loads(target.ha("apps", "info", pi.SLUG))["data"]["version"] == "0.3.0"
    assert pi.deploy(target, V2, source(versions), **fast())


def test_a_stopped_app_is_started_after_the_build(pi_dir):
    target = pi.Folder(pi_dir)
    target._save({**target._state(), "auto_start": False})
    assert pi.deploy(target, V1, source(), **fast(first=True))
    assert json.loads(target.ha("apps", "info", pi.SLUG))["data"]["state"] == "started"


def test_deploy_pulls_learner_data_first_unless_told_not_to(tmp_path, pi_dir):
    into = tmp_path / "backup"
    assert pi.deploy(pi.Folder(pi_dir), V1, source(), **fast(first=True, pull_into=into))
    assert (into / date.today().isoformat() / "learners" / "anna" / "attempts.jsonl").is_file()
    assert pi.deploy(pi.Folder(pi_dir), V2, source(), **fast(pull_into=None))
    assert len(list(into.iterdir())) == 1


def test_deploy_builds_the_app_from_git_with_lf(pi_dir):
    assert pi.deploy(pi.Folder(pi_dir), "HEAD", **fast(first=True))
    folder = pi_dir / "local_apps" / "jlpt_portal"
    assert (folder / "run.sh").read_bytes().startswith(b"#!/bin/sh\n") and b"\r" not in (folder / "run.sh").read_bytes()
    assert {"Dockerfile", "config.yaml", "server.py", "engine", "web", "tracks", "BUILD", ".tag"} <= {p.name for p in folder.iterdir()}


def test_dry_run_changes_nothing(tmp_path, pi_dir):
    target = pi.Folder(pi_dir)
    assert pi.deploy(target, V1, source(), **fast(first=True))
    before = tree(pi_dir)
    home = write(tmp_path / "home", {"data/bank/a.json": "[9]"})
    audio = write(tmp_path / "audio", {"new.mp3": "n"})
    dry = pi.DryRun(target)
    pi.push_content(dry, home)
    pi.push_audio(dry, audio)
    assert pi.deploy(dry, V2, source(), **fast(pull_into=tmp_path / "backup", dry=True))
    assert tree(pi_dir) == before and not (tmp_path / "backup").exists()


def test_pull_works_with_missing_entries_and_drops_files_deleted_on_the_pi(tmp_path, pi_dir):
    config = pi_dir / "app_configs" / "local_jlpt_portal"
    into = tmp_path / "backup"
    target = pi.Folder(pi_dir)
    first = pi.pull(target, into, today=date(2026, 11, 8))
    assert (first / "logs" / "access-2026-11.jsonl").is_file()
    shutil.rmtree(config / "logs")
    (config / "learners" / "yoko" / "runs.jsonl").unlink()
    again = pi.pull(target, into, today=date(2026, 11, 8))
    assert sorted(tree(again)) == ["learners.json", "learners/anna/attempts.jsonl"]
    shutil.rmtree(config / "learners")
    (config / "learners.json").unlink()
    empty = pi.pull(target, into, today=date(2026, 11, 9))
    assert tree(empty) == {} and sorted(p.name for p in into.iterdir()) == ["2026-11-08", "2026-11-09"]


def test_golden_real_reads_a_pulled_copy_like_the_original(tmp_path, pi_dir):
    fixture = Path(__file__).with_name("golden_n4_fixture")
    real = tmp_path / "real"
    shutil.copytree(fixture / "bank", real / "data" / "bank")
    shutil.copy(fixture / "explain.json", real / "data" / "explain.json")
    shutil.copytree(fixture / "audio", real / "audio")
    for name in ("attempts.jsonl", "runs.jsonl", "focus.json", "model_state.json"):
        text = (fixture / name).read_text(encoding="utf-8")
        write(real / "confidential", {name: text})
        write(pi_dir / "app_configs" / "local_jlpt_portal" / "learners" / "anna", {name: text})
    pulled = pi.pull(pi.Folder(pi_dir), tmp_path / "backup") / "learners" / "anna"
    repo = Path(__file__).resolve().parents[1]
    runs = {}
    for label, extra in (("original", None), ("pulled", str(pulled))):
        env = {k: v for k, v in os.environ.items() if k != "N4_REAL_DATA"}
        env.update({"N4_REAL_HOME": str(real), **({"N4_REAL_DATA": extra} if extra else {})})
        subprocess.run([sys.executable, str(repo / "tools" / "golden_real.py"), "--snapshot", str(tmp_path / f"{label}.json")], cwd=repo, env=env, check=True, capture_output=True)
        runs[label] = (tmp_path / f"{label}.json").read_bytes()
    assert runs["original"] == runs["pulled"]
    assert [k for k, v in json.loads(runs["original"]).items() if isinstance(v, dict) and set(v) == {"error"}] == []


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


def test_cli_against_a_target_folder(tmp_path, pi_dir, capsys, monkeypatch):
    monkeypatch.setattr(pi, "dirty", lambda repo=pi.REPO: [])
    audio = write(tmp_path / "audio", {"a.mp3": "a"})
    assert pi.main(["--target-dir", str(pi_dir), "push-audio", "--audio", str(audio)]) == 0
    assert pi.main(["--target-dir", str(pi_dir), "push-audio", "--audio", str(audio)]) == 0
    assert capsys.readouterr().out.splitlines()[-1] == "audio: 0 of 1 files sent"


def test_deploy_over_ssh_reloads_the_store_updates_on_a_new_version_and_starts(tmp_path):
    scripts, uploaded = [], {}

    def runner(cmd, input=None, capture_output=True):
        script = cmd[-1]
        scripts.append(script)
        if "tar -xf - -C /local_apps/jlpt_portal.new" in script:
            uploaded["build"] = pi.member(input, "BUILD").strip()
        out = b""
        if script.startswith("cat /local_apps/jlpt_portal/.tag"):
            out = (V1 + "\n").encode()
        elif script.startswith("ha apps info"):
            out = json.dumps({"data": {"state": "stopped" if not any(s.startswith("ha apps start") for s in scripts) else "started", "version": "0.1.0"}}).encode()
        elif script.startswith("ha apps logs"):
            out = f"{pi.START} 127.0.0.1:8080 as tailscale build {uploaded.get('build')}\n".encode()
        return type("Done", (), {"returncode": 0, "stdout": out})()

    ssh = pi.Ssh("homeassistant.local", "root", tmp_path / "key", runner)
    assert pi.deploy(ssh, V2, source({V2: "0.2.0"}), **fast())
    ha = [s for s in scripts if s.startswith("ha ")]
    assert ha == ["ha apps info local_jlpt_portal --raw-json", "ha store reload", "ha apps update local_jlpt_portal",
                  "ha apps info local_jlpt_portal --raw-json", "ha apps start local_jlpt_portal",
                  "ha apps info local_jlpt_portal --raw-json", "ha apps logs local_jlpt_portal"]
    assert any(s.startswith(f"mkdir -p /local_apps/jlpt_portal && cat > /local_apps/jlpt_portal/.tag") for s in scripts)


def test_the_build_line_is_detected_from_the_commit_itself():
    assert not pi.modern("0867b65")
    assert pi.modern("42a02ff")


def test_rollback_to_a_commit_without_the_build_line_passes(pi_dir):
    target = pi.Folder(pi_dir)
    assert pi.deploy(target, OLD, source(), **fast(first=True, allow_old=True))
    assert pi.START in target.ha("apps", "logs", pi.SLUG) and "build" not in target.ha("apps", "logs", pi.SLUG)
    assert not pi.deploy(target, BROKEN, source(), **fast())
    assert target.read(pi.APP / ".tag").strip() == OLD
    assert (pi_dir / "local_apps" / "jlpt_portal" / "server.py").read_text(encoding="utf-8") == "print('old')\n"


def test_an_old_build_still_needs_healthz(pi_dir, monkeypatch):
    target = pi.Folder(pi_dir)
    monkeypatch.setattr(pi.Folder, "health", lambda self: False)
    assert not pi.deploy(target, OLD, source(), **fast(first=True, allow_old=True))


def test_a_forward_deploy_of_an_old_commit_is_refused(pi_dir):
    target = pi.Folder(pi_dir)
    assert pi.deploy(target, V1, source(), **fast(first=True))
    before = tree(pi_dir)
    assert not pi.deploy(target, OLD, source(), **fast())
    assert tree(pi_dir) == before


def test_a_dirty_tree_is_refused(tmp_path, pi_dir, monkeypatch, capsys):
    repo = tmp_path / "repo"
    write(repo, {"tools/pi.py": "x\n", "server.py": "y\n", "deploy/ha-app/run.sh": "z\n", "notes.txt": "n\n"})
    git = lambda *a: subprocess.run(["git", "-C", str(repo), *a], check=True, capture_output=True)
    git("init", "-q")
    git("add", "-A")
    git("-c", "user.name=t", "-c", "user.email=t@example.ch", "commit", "-q", "-m", "init")
    assert pi.dirty(repo) == []
    (repo / "notes.txt").write_text("changed", encoding="utf-8")
    assert pi.dirty(repo) == []
    (repo / "deploy" / "ha-app" / "run.sh").write_text("changed", encoding="utf-8")
    (repo / "tools" / "pi.py").write_text("changed", encoding="utf-8")
    assert sorted(pi.dirty(repo)) == ["deploy/ha-app/run.sh", "tools/pi.py"]
    monkeypatch.setattr(pi, "dirty", lambda repo=pi.REPO: ["tools/pi.py"])
    before = tree(pi_dir)
    assert pi.main(["--target-dir", str(pi_dir), "pull", "--into", str(tmp_path / "b")]) == 2
    assert "refusing to run" in capsys.readouterr().out and tree(pi_dir) == before and not (tmp_path / "b").exists()
