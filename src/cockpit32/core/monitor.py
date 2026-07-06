"""ESP-IDF monitor wrapper: captures a timed serial-monitor session.

Engineering Method Selection: fake-first. A real BOX-3 and a real
`idf.py monitor` process are outside the agent's environment in Stage 3.
``TranscriptMonitorSource`` replays a synthetic transcript fixture;
``SubprocessMonitorSource`` is the real (Deferred) implementation.
"""

from __future__ import annotations

import re
import subprocess
import threading
from dataclasses import dataclass
from pathlib import Path
from typing import Protocol

# Heuristics for "notable" lines worth surfacing in a summary without
# reading the full raw transcript. Order matters: first match wins.
_NOTABLE_PATTERNS: list[tuple[str, re.Pattern]] = [
    ("error", re.compile(r"\bE \(|error|ERROR|Guru Meditation|abort\(\)|assert failed", re.IGNORECASE)),
    ("warning", re.compile(r"\bW \(|brownout|Brownout", re.IGNORECASE)),
    ("boot", re.compile(r"^rst:|^ets |Booting|entry 0x")),
]


class MonitorSource(Protocol):
    def read_lines(self, duration_s: float) -> list[str]: ...


@dataclass
class TranscriptMonitorSource:
    """Fake source: replays a fixed list of lines, ignoring real-time
    pacing (a synthetic-fidelity limit noted in the Validation Ledger).
    """

    lines: list[str]

    def read_lines(self, duration_s: float) -> list[str]:
        return list(self.lines)


@dataclass
class SubprocessMonitorSource:
    """Real source: spawns `idf.py -p <port> monitor` and captures output
    for duration_s before terminating it. Not exercised against real
    hardware in Stage 3 — Deferred to Stage 4.
    """

    port: str

    def read_lines(self, duration_s: float) -> list[str]:
        try:
            proc = subprocess.Popen(
                ["idf.py", "-p", self.port, "monitor"],
                stdout=subprocess.PIPE,
                stderr=subprocess.STDOUT,
                text=True,
            )
        except FileNotFoundError as exc:
            return [f"cockpit32: could not start idf.py monitor: {exc}"]
        lines: list[str] = []

        def _reader():
            assert proc.stdout is not None
            for line in proc.stdout:
                lines.append(line.rstrip("\n"))

        reader_thread = threading.Thread(target=_reader, daemon=True)
        reader_thread.start()
        reader_thread.join(timeout=duration_s)
        proc.terminate()
        try:
            proc.wait(timeout=5)
        except subprocess.TimeoutExpired:
            proc.kill()
        return lines


def classify_line(line: str) -> str | None:
    for label, pattern in _NOTABLE_PATTERNS:
        if pattern.search(line):
            return label
    return None


def notable_lines(lines: list[str]) -> list[str]:
    return [line for line in lines if classify_line(line) is not None]


def run_monitor(
    port: str,
    duration_s: float,
    source: MonitorSource,
    log_dir: Path,
) -> list[str]:
    """Capture a timed monitor session, writing the raw transcript to
    log_dir/monitor.log and returning the captured lines.
    """
    lines = source.read_lines(duration_s)
    log_dir.mkdir(parents=True, exist_ok=True)
    (log_dir / "monitor.log").write_text("\n".join(lines) + "\n", encoding="utf-8")
    return lines
