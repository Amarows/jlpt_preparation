import os
from email.header import decode_header, make_header

MODES = ("local", "tailscale")
HEADER = "Tailscale-User-Login"


def mode() -> str:
    return os.environ.get("JLPT_AUTH") or "local"


def bind() -> str:
    return os.environ.get("JLPT_BIND") or "127.0.0.1"


def check_startup() -> None:
    if mode() not in MODES:
        raise SystemExit(f"JLPT_AUTH must be one of {', '.join(MODES)}, not {mode()!r}")
    if mode() == "tailscale" and bind() != "127.0.0.1":
        raise SystemExit(f"JLPT_AUTH=tailscale trusts {HEADER} only behind tailscale serve: JLPT_BIND must be 127.0.0.1, not {bind()!r}")


def login(value: str | None) -> str | None:
    if not value:
        return None
    try:
        text = str(make_header(decode_header(value))) if "=?" in value else value
    except Exception:
        return None
    text = text.strip().lower()
    return text if "@" in text else None
