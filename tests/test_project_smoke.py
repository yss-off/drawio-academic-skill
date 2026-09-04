from __future__ import annotations

import subprocess
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


def test_project_smoke_suites_in_isolated_processes() -> None:
    result = subprocess.run(
        ["make", "test"],
        cwd=ROOT,
        text=True,
        capture_output=True,
        check=False,
    )
    output = "\n".join(part for part in (result.stdout, result.stderr) if part)
    assert result.returncode == 0, output
