"""Resolve portal data paths."""
import os
from pathlib import Path

REPO = Path(__file__).resolve().parents[1]
HOME = Path(os.environ.get("JLPT_HOME", REPO)).expanduser().resolve()
DATA = HOME / "data"
BANK = DATA / "bank"
CONFIDENTIAL = HOME / "confidential"
ATTEMPTS = CONFIDENTIAL / "attempts.jsonl"
RUNS = CONFIDENTIAL / "runs.jsonl"
MODEL_STATE = CONFIDENTIAL / "model_state.json"

def under_home(path: str | Path) -> Path:
    """Resolve a path under JLPT_HOME and reject escapes."""
    p = (HOME / path).resolve()
    if p != HOME and HOME not in p.parents:
        raise ValueError("path escapes JLPT_HOME")
    return p
