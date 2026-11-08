import json

from tests.golden_hardening import env
from tests.golden_learners import LEARNERS, two_learners

ROWS = [{**LEARNERS[0], "emails": ["Anna@example.ch"]}, {**LEARNERS[1], "emails": ["yoko@example.ch"]}]
CASES = {
    "learner": ({"Tailscale-User-Login": "anna@example.ch"}, None),
    "learner_upper_case": ({"Tailscale-User-Login": "ANNA@Example.CH"}, None),
    "learner_rfc2047": ({"Tailscale-User-Login": "=?utf-8?q?yoko=40example=2Ech?="}, None),
    "admin": ({"Tailscale-User-Login": "alex@example.ch"}, None),
    "admin_chose_yoko": ({"Tailscale-User-Login": "alex@example.ch"}, "yoko"),
    "learner_cookie_ignored": ({"Tailscale-User-Login": "anna@example.ch"}, "yoko"),
    "unknown": ({"Tailscale-User-Login": "eve@example.ch"}, None),
    "not_an_email": ({"Tailscale-User-Login": "tagged-devices"}, None),
    "missing": ({}, None),
    "missing_with_cookie": ({}, "anna"),
}


def who():
    import server
    out = {}
    with two_learners(ROWS) as home:
        data = json.loads((home / "learners.json").read_text(encoding="utf-8"))
        (home / "learners.json").write_text(json.dumps({**data, "admins": ["alex@example.ch"]}), encoding="utf-8")
        for auth in ("tailscale", None):
            with env(JLPT_AUTH=auth):
                for name, (headers, cookie) in CASES.items():
                    h = {**headers, **({"Cookie": f"learner={cookie}"} if cookie else {})}
                    out[f"{auth or 'local'}:{name}"] = server.who(type("H", (), {"headers": h})())
    return out
