"""Write confidential/analysis/item_health.md: suspect items and per-batch accuracy."""
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from engine import paths
from engine.bank import load_bank
from engine.health import item_health, to_markdown
from engine.model import read_attempts


def main():
    health = item_health(load_bank()[0], read_attempts())
    out = paths.CONFIDENTIAL / "analysis" / "item_health.md"
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(to_markdown(health), encoding="utf-8")
    print(f"{len(health['suspects'])} suspect items; wrote {out}")


if __name__ == "__main__":
    main()
