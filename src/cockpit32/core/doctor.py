from __future__ import annotations

import importlib.util
import platform
from dataclasses import dataclass

from cockpit32.core.idf_runner import IdfRunner


@dataclass(frozen=True)
class Check:
    name: str
    ok: bool
    detail: str


@dataclass(frozen=True)
class DoctorReport:
    checks: list[Check]

    @property
    def ok(self) -> bool:
        return all(check.ok for check in self.checks)


def run_doctor(idf_command: str = "idf.py") -> DoctorReport:
    runner = IdfRunner(idf_command)
    checks = [
        Check("python", True, platform.python_version()),
        Check("idf.py visible", runner.visible(), idf_command),
        Check("pyserial import", importlib.util.find_spec("serial") is not None, "serial"),
        Check("PySide6 import", importlib.util.find_spec("PySide6") is not None, "PySide6"),
    ]
    return DoctorReport(checks)
