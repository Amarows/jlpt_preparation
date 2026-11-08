import ipaddress
import os
from functools import lru_cache

LOOPBACK = {"localhost", "::1"}


def mode() -> str:
    return os.environ.get("JLPT_AUTH", "local")


def team() -> str:
    return os.environ.get("JLPT_ACCESS_TEAM", "")


def aud() -> str:
    return os.environ.get("JLPT_ACCESS_AUD", "")


def bind() -> str:
    return os.environ.get("JLPT_BIND", "127.0.0.1")


def issuer(name: str) -> str:
    return f"https://{name}.cloudflareaccess.com"


def loopback(host: str) -> bool:
    if host in LOOPBACK:
        return True
    try:
        return ipaddress.ip_address(host).is_loopback
    except ValueError:
        return False


def check_startup() -> None:
    if mode() not in ("local", "access"):
        raise SystemExit(f"JLPT_AUTH must be local or access, not {mode()!r}")
    if mode() == "access":
        if not team() or not aud():
            raise SystemExit("JLPT_AUTH=access needs JLPT_ACCESS_TEAM and JLPT_ACCESS_AUD")
        __import__("jwt")
    elif not loopback(bind()):
        raise SystemExit(f"JLPT_AUTH=local only binds a loopback address, not {bind()!r}")


@lru_cache(maxsize=4)
def _keys(name: str):
    import jwt
    return jwt.PyJWKClient(issuer(name) + "/cdn-cgi/access/certs", cache_keys=True, lifespan=3600)


def email(token: str | None, name: str, audience: str, keys=None) -> str | None:
    if not token or not name or not audience:
        return None
    try:
        import jwt
        key = (keys or _keys(name)).get_signing_key_from_jwt(token).key
        claims = jwt.decode(token, key, algorithms=["RS256"], audience=audience, issuer=issuer(name), leeway=60,
                            options={"require": ["exp", "iat", "aud", "iss"]})
    except Exception:
        return None
    value = claims.get("email")
    return value.strip().lower() if isinstance(value, str) and "@" in value else None
