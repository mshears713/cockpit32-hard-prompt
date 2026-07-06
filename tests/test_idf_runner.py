import os
from pathlib import Path

from cockpit32.core.idf_runner import IdfRunner


def make_fake_idf(tmp_path: Path, body: str) -> Path:
    fake = tmp_path / "idf.py"
    fake.write_text("#!/usr/bin/env python3\n" + body, encoding="utf-8")
    fake.chmod(0o755)
    return fake


def test_build_captures_fake_idf_output(tmp_path):
    fake = make_fake_idf(tmp_path, "import sys\nprint('Project build complete.')\nsys.exit(0)\n")
    log = tmp_path / "build.log"
    result = IdfRunner(str(fake)).build(tmp_path, log)
    assert result.returncode == 0
    assert "Project build complete." in log.read_text(encoding="utf-8")


def test_flash_failure_is_captured(tmp_path):
    fake = make_fake_idf(tmp_path, "import sys\nprint('A fatal error occurred: Failed to connect')\nsys.exit(2)\n")
    log = tmp_path / "flash.log"
    result = IdfRunner(str(fake)).flash(tmp_path, "COM7", log)
    assert result.returncode == 2
    assert "Failed to connect" in log.read_text(encoding="utf-8")
