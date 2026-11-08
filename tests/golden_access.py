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


def me():
    from tests.golden_hardening import _call, server
    out = {}
    with two_learners(ROWS) as home:
        data = json.loads((home / "learners.json").read_text(encoding="utf-8"))
        (home / "learners.json").write_text(json.dumps({**data, "admins": ["alex@example.ch"]}), encoding="utf-8")
        for auth, cases in (("tailscale", {"anna_herself": ("anna@example.ch", None), "admin_viewing_anna": ("alex@example.ch", "anna"),
                                           "admin_viewing_yoko": ("alex@example.ch", "yoko"), "admin_not_chosen": ("alex@example.ch", None),
                                           "yoko_herself": ("yoko@example.ch", None)}),
                            (None, {"cookie_anna": (None, "anna"), "cookie_yoko": (None, "yoko")})):
            with env(JLPT_AUTH=auth), server() as port:
                for name, (login, cookie) in cases.items():
                    r = _call(port, "GET", "/api/me", None, {"Tailscale-User-Login": login} if login else None, cookie)
                    body = r["body"]
                    out[f"{auth or 'local'}:{name}"] = {"status": r["status"], **({"learner": body["learner"]["id"], "track": body["track"]["id"],
                                                        "admin": body.get("admin", "<absent>")} if r["status"] == 200 else {"body": body})}
    return out
