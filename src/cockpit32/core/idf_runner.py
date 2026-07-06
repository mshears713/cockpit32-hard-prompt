from __future__ import annotations

import shutil
import subprocess
from datetime import datetime, timezone
from pathlib import Path

from cockpit32.models import CommandResult


class IdfRunner:
    def __init__(self, idf_command: str = "idf.py"):
        self.idf_command = idf_command

    def visible(self) -> bool:
        return shutil.which(self.idf_command) is not None

    def run(self, args: list[str], cwd: Path, log_path: Path, timeout: float | None = None) -> CommandResult:
        started = datetime.now(timezone.utc)
        command = [self.idf_command, *args]
        proc = subprocess.run(
            command,
            cwd=str(cwd),
            text=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
            timeout=timeout,
            check=False,
        )
        ended = datetime.now(timezone.utc)
        log_path.parent.mkdir(parents=True, exist_ok=True)
        log_path.write_text(proc.stdout, encoding="utf-8")
        return CommandResult(
            command=command,
            cwd=str(cwd),
            returncode=proc.returncode,
            started_at=started,
            ended_at=ended,
            log_path=str(log_path),
        )

    def build(self, cwd: Path, log_path: Path) -> CommandResult:
        return self.run(["build"], cwd, log_path)

    def flash(self, cwd: Path, port: str, log_path: Path) -> CommandResult:
        return self.run(["-p", port, "flash"], cwd, log_path)

    def monitor(self, cwd: Path, port: str, log_path: Path, seconds: int = 30) -> CommandResult:
        return self.run(["-p", port, "monitor"], cwd, log_path, timeout=seconds)
