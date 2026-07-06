"""Fake CommandRunner test double, backed by synthetic idf.py fixtures.

Fixture Policy (Engineering Method Selection & Test Architecture Guide):
Stage 3 uses synthetic fixtures for idf.py output since real idf.py and
a real BOX-3 are outside the agent's environment. Stage 4 real-hardware
captures replace/extend these as regression fixtures.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from pathlib import Path

from cockpit32.core.models import CommandResult

FIXTURES_DIR = Path(__file__).parent.parent / "fixtures"


@dataclass
class FakeCommandRunner:
    """Returns a scripted CommandResult and records the call it received."""

    returncode: int
    stdout: str = ""
    stderr: str = ""
    calls: list[tuple[list[str], Path]] = field(default_factory=list)

    def run(self, args: list[str], cwd: Path) -> CommandResult:
        self.calls.append((list(args), Path(cwd)))
        return CommandResult(
            command=args[0],
            args=list(args[1:]),
            returncode=self.returncode,
            stdout=self.stdout,
            stderr=self.stderr,
            started_at="2026-07-06T00:00:00+00:00",
            ended_at="2026-07-06T00:00:05+00:00",
        )


def load_fixture(*parts: str) -> str:
    return (FIXTURES_DIR.joinpath(*parts)).read_text(encoding="utf-8")
