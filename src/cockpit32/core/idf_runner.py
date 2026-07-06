"""ESP-IDF command runner: wraps `idf.py build` / `idf.py -p <PORT> flash`.

Engineering Method Selection: fake-first. Real `idf.py` and a real BOX-3
are outside the agent's environment (Stage 3), so this module is built
against an injectable ``CommandRunner`` and validated with synthetic
fixtures. ``SubprocessCommandRunner`` is real, untested-in-CI code —
its real-environment behavior is a Deferred Validation Ledger item for
Stage 4.
"""

from __future__ import annotations

import subprocess
from dataclasses import dataclass
from datetime import datetime, timezone
from pathlib import Path
from typing import Protocol

from cockpit32.core.models import CommandResult


class CommandRunner(Protocol):
    def run(self, args: list[str], cwd: Path) -> CommandResult: ...


@dataclass
class SubprocessCommandRunner:
    """Real runner: executes the command via subprocess. Not exercised
    against real idf.py in Stage 3 — see docs/validation Deferred list.
    """

    timeout_s: float | None = None

    def run(self, args: list[str], cwd: Path) -> CommandResult:
        started = datetime.now(timezone.utc)
        try:
            proc = subprocess.run(
                args,
                cwd=str(cwd),
                capture_output=True,
                text=True,
                timeout=self.timeout_s,
            )
            returncode, stdout, stderr = proc.returncode, proc.stdout, proc.stderr
        except FileNotFoundError as exc:
            returncode, stdout, stderr = 127, "", str(exc)
        except subprocess.TimeoutExpired as exc:
            returncode = 124
            stdout = exc.stdout or ""
            stderr = (exc.stderr or "") + "\ncockpit32: command timed out"
        ended = datetime.now(timezone.utc)
        return CommandResult(
            command=args[0],
            args=list(args[1:]),
            returncode=returncode,
            stdout=stdout,
            stderr=stderr,
            started_at=started.isoformat(),
            ended_at=ended.isoformat(),
        )


# Substrings mapped to human-actionable next steps, checked in order.
_FAILURE_GUIDANCE: list[tuple[str, str]] = [
    ("No such file or directory: 'idf.py'", "idf.py not found — run 'cockpit32 doctor' and launch from an ESP-IDF environment."),
    ("not recognized as an internal or external command", "idf.py not on PATH — run 'cockpit32 doctor' and launch from an ESP-IDF PowerShell environment."),
    ("could not open port", "Could not open the serial port — check the port name and that nothing else (a serial monitor, another cockpit32 session) is holding it open."),
    ("Permission denied", "Permission denied opening the port — on Linux, check you're in the 'dialout' group; on Windows, check no other program has it open."),
    ("A fatal error occurred: Failed to connect", "Board did not respond to the flasher's sync sequence — check the BOX-3 is in the correct boot mode and the USB cable carries data."),
]


def guidance_for_failure(stdout: str, stderr: str) -> str | None:
    combined = f"{stdout}\n{stderr}"
    for needle, advice in _FAILURE_GUIDANCE:
        if needle in combined:
            return advice
    return None


def _write_log(log_dir: Path, stem: str, result: CommandResult) -> Path:
    """Write both a human-readable `<stem>.log` and a machine-readable
    `<stem>.json` (the CommandResult contract) so callers like the CLI's
    `summary` command can recover pass/fail without reparsing log text.
    """
    import json

    log_dir.mkdir(parents=True, exist_ok=True)
    log_path = log_dir / f"{stem}.log"
    lines = [
        f"$ {result.command} {' '.join(result.args)}",
        f"started_at: {result.started_at}",
        f"ended_at:   {result.ended_at}",
        f"returncode: {result.returncode}",
        "--- stdout ---",
        result.stdout,
        "--- stderr ---",
        result.stderr,
    ]
    log_path.write_text("\n".join(lines) + "\n", encoding="utf-8")
    (log_dir / f"{stem}.json").write_text(json.dumps(result.to_dict(), indent=2) + "\n", encoding="utf-8")
    return log_path


def load_result(json_path: Path) -> CommandResult:
    """Load a CommandResult from a `<stem>.json` sidecar written by _write_log.

    Public counterpart of _write_log's JSON output, shared by the CLI's
    and GUI's summary generation so neither reimplements it.
    """
    import json

    return CommandResult.from_dict(json.loads(json_path.read_text(encoding="utf-8")))


def build(project_path: Path, runner: CommandRunner, log_dir: Path) -> CommandResult:
    """Run `idf.py build` in project_path, capturing evidence to log_dir/build.log (+ build.json)."""
    result = runner.run(["idf.py", "build"], cwd=Path(project_path))
    _write_log(log_dir, "build", result)
    return result


def flash(project_path: Path, port: str, runner: CommandRunner, log_dir: Path) -> CommandResult:
    """Run `idf.py -p <port> flash` in project_path, capturing evidence to log_dir/flash.log (+ flash.json)."""
    result = runner.run(["idf.py", "-p", port, "flash"], cwd=Path(project_path))
    _write_log(log_dir, "flash", result)
    return result
