import os
import subprocess
import sys
from pathlib import Path

import pytest

REPO = Path(__file__).resolve().parents[1]
AOP = Path.home() / ".claude/plugins/cache/amarows/ai-oriented-programming/0.1.0/skills/ai-oriented-programming/aop.py"


@pytest.mark.skipif(not AOP.exists(), reason="aop golden runner not installed")
@pytest.mark.parametrize("days", [60, -30])
def test_golden_cases_ignore_the_real_clock(days):
    done = subprocess.run([sys.executable, str(AOP), "--root", str(REPO), "golden"], cwd=REPO, capture_output=True, text=True,
                          env={**os.environ, "GOLDEN_CLOCK_SHIFT_DAYS": str(days)})
    assert done.returncode == 0, done.stdout[-2000:] + done.stderr[-2000:]
