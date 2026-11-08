import json
import time

import pytest

jwt = pytest.importorskip("jwt")
rsa = pytest.importorskip("cryptography.hazmat.primitives.asymmetric.rsa")

from tests.golden_learners import LEARNERS, two_learners

TEAM, AUD = "home", "aud-tag"
GOOD = rsa.generate_private_key(public_exponent=65537, key_size=2048)
OTHER = rsa.generate_private_key(public_exponent=65537, key_size=2048)


class Keys:
    def get_signing_key_from_jwt(self, token):
        return type("K", (), {"key": GOOD.public_key()})()


def token(email="anna@example.ch", key=GOOD, aud=AUD, iss=f"https://{TEAM}.cloudflareaccess.com", exp=3600):
    now = int(time.time())
    return jwt.encode({"email": email, "aud": [aud], "iss": iss, "iat": now, "nbf": now, "exp": now + exp}, key, algorithm="RS256")


@pytest.fixture
def portal(monkeypatch):
    from engine import access
    rows = [{**LEARNERS[0], "emails": ["Anna@example.ch"]}, {**LEARNERS[1], "emails": ["yoko@example.ch"]}]
    with two_learners(rows) as home:
        data = json.loads((home / "learners.json").read_text(encoding="utf-8"))
        (home / "learners.json").write_text(json.dumps({**data, "admins": ["alex@example.ch"]}), encoding="utf-8")
        monkeypatch.setenv("JLPT_AUTH", "access")
        monkeypatch.setenv("JLPT_ACCESS_TEAM", TEAM)
        monkeypatch.setenv("JLPT_ACCESS_AUD", AUD)
        monkeypatch.setattr(access, "_keys", lambda name: Keys())
        yield home


def who(jwt_value, cookie=None):
    import server
    headers = {**({"Cf-Access-Jwt-Assertion": jwt_value} if jwt_value else {}), **({"Cookie": f"learner={cookie}"} if cookie else {})}
    return server.who(type("H", (), {"headers": headers})())


@pytest.mark.parametrize("name,value,expected", [
    ("learner", token(), {"email": "anna@example.ch", "learner_id": "anna", "admin": False}),
    ("admin", token("alex@example.ch"), {"email": "alex@example.ch", "learner_id": None, "admin": True}),
    ("unknown email", token("eve@example.ch"), None),
    ("wrong aud", token(aud="other"), None),
    ("wrong iss", token(iss="https://evil.cloudflareaccess.com"), None),
    ("expired", token(exp=-120), None),
    ("bad signature", token(key=OTHER), None),
    ("header missing", None, None),
])
def test_who_under_access(portal, name, value, expected):
    assert who(value) == expected


def test_admin_acts_as_the_chosen_learner(portal):
    assert who(token("alex@example.ch"), cookie="yoko") == {"email": "alex@example.ch", "learner_id": "yoko", "admin": True}


def test_a_learner_cannot_switch_by_cookie(portal):
    assert who(token(), cookie="yoko")["learner_id"] == "anna"
