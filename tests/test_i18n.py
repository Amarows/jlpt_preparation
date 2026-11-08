import json
import re
from pathlib import Path

WEB = Path(__file__).resolve().parents[1] / "web"
TABLE = json.loads(re.search(r"const I18N=(\{.*?\n\});", (WEB / "i18n.js").read_text(encoding="utf-8"), re.S).group(1))
USED = {k for k in re.findall(r"""\btr(?:Or|In\(l\.ui,)?\(['`]([\w.-]+)['`]""", (WEB / "app.js").read_text(encoding="utf-8")) if not k.endswith(".")}
USED |= set(re.findall(r'data-i18n="([\w.-]+)"', "".join(p.read_text(encoding="utf-8") for p in WEB.glob("*.html"))))


def test_every_language_has_every_key():
    assert set(TABLE["ja"]) == set(TABLE["en"])


def test_placeholders_match_between_languages():
    names = lambda s: sorted(re.findall(r"\{(\w+)\}", s))
    assert {k: names(v) for k, v in TABLE["ja"].items()} == {k: names(v) for k, v in TABLE["en"].items()}


def test_every_key_used_exists():
    assert USED and USED <= set(TABLE["en"])
