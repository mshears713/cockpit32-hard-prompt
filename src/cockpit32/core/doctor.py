"""`cockpit32 doctor`: checks whether the ESP-IDF environment is visible.

v0 assumes Mike launches from an already-working ESP-IDF PowerShell
environment; this command only reports what it can see, it does not
try to install or configure anything.
"""

from __future__ import annotations

import shutil
import sys
from dataclasses import dataclass

from cockpit32.core.ports import pyserial_available


@dataclass
class DoctorCheck:
    name: str
    ok: bool
    detail: str


@dataclass
class DoctorReport:
    checks: list[DoctorCheck]

    @property
    def all_ok(self) -> bool:
        return all(c.ok for c in self.checks)

    def render(self) -> str:
        lines = ["Cockpit 32 doctor report:"]
        for check in self.checks:
            status = "OK" if check.ok else "MISSING"
            lines.append(f"  [{status}] {check.name}: {check.detail}")
        lines.append("")
        lines.append("All checks passed." if self.all_ok else "Some checks failed — see above.")
        return "\n".join(lines)


def run_doctor() -> DoctorReport:
    checks = [
        DoctorCheck(
            name="python",
            ok=True,
            detail=f"{sys.version.split()[0]} at {sys.executable}",
        ),
        DoctorCheck(
            name="cockpit32 package",
            ok=True,
            detail="import cockpit32 succeeded (this process is running it)",
        ),
        DoctorCheck(
            name="idf.py on PATH",
            ok=shutil.which("idf.py") is not None,
            detail=(shutil.which("idf.py") or "not found — launch from an ESP-IDF PowerShell environment"),
        ),
        DoctorCheck(
            name="pyserial import",
            ok=pyserial_available(),
            detail="available" if pyserial_available() else "not installed (pip install cockpit32[serial])",
        ),
    ]
    return DoctorReport(checks=checks)
