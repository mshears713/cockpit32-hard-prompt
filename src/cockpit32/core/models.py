"""Core domain models for Cockpit 32 sessions.

These models are the in-memory representation behind the AI-readable
session artifacts (session.json, events.jsonl, summary.json). Keep
serialization explicit (to_dict/from_dict) rather than relying on a
schema library, since the JSON shape *is* the contract other tools and
agents read.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime, timezone
from enum import Enum


def utc_now_iso() -> str:
    return datetime.now(timezone.utc).isoformat()


class Verdict(str, Enum):
    SUCCESS = "success"
    PARTIAL = "partial"
    FAILED = "failed"
    BLOCKED = "blocked"
    UNKNOWN = "unknown"


class Phase(str, Enum):
    BUILD = "build"
    FLASH = "flash"
    MONITOR = "monitor"


@dataclass
class BoardProfile:
    """v0 supports exactly one board target: ESP32-S3-BOX-3."""

    name: str = "esp32-s3-box-3"
    default_baud: int = 115200

    def to_dict(self) -> dict:
        return {"name": self.name, "default_baud": self.default_baud}

    @classmethod
    def from_dict(cls, data: dict) -> "BoardProfile":
        return cls(name=data["name"], default_baud=data["default_baud"])


@dataclass
class CommandResult:
    """Outcome of running a single external command (build/flash/etc.)."""

    command: str
    args: list[str]
    returncode: int
    stdout: str
    stderr: str
    started_at: str
    ended_at: str

    @property
    def success(self) -> bool:
        return self.returncode == 0

    def to_dict(self) -> dict:
        return {
            "command": self.command,
            "args": self.args,
            "returncode": self.returncode,
            "stdout": self.stdout,
            "stderr": self.stderr,
            "started_at": self.started_at,
            "ended_at": self.ended_at,
            "success": self.success,
        }

    @classmethod
    def from_dict(cls, data: dict) -> "CommandResult":
        return cls(
            command=data["command"],
            args=list(data["args"]),
            returncode=data["returncode"],
            stdout=data["stdout"],
            stderr=data["stderr"],
            started_at=data["started_at"],
            ended_at=data["ended_at"],
        )


@dataclass
class Event:
    """A single timeline entry: a user note, marker, or system occurrence."""

    kind: str  # "note" | "marker" | "system"
    message: str
    source: str = "user"  # "user" | "system"
    timestamp: str = field(default_factory=utc_now_iso)

    def to_dict(self) -> dict:
        return {
            "timestamp": self.timestamp,
            "kind": self.kind,
            "source": self.source,
            "message": self.message,
        }

    @classmethod
    def from_dict(cls, data: dict) -> "Event":
        return cls(
            timestamp=data["timestamp"],
            kind=data["kind"],
            source=data["source"],
            message=data["message"],
        )


@dataclass
class SessionMeta:
    """Metadata for one build/flash/monitor session, stored as session.json."""

    session_id: str
    project_path: str
    board: BoardProfile
    created_at: str
    port: str | None = None
    baud: int | None = None

    def to_dict(self) -> dict:
        return {
            "session_id": self.session_id,
            "project_path": self.project_path,
            "board": self.board.to_dict(),
            "created_at": self.created_at,
            "port": self.port,
            "baud": self.baud,
        }

    @classmethod
    def from_dict(cls, data: dict) -> "SessionMeta":
        return cls(
            session_id=data["session_id"],
            project_path=data["project_path"],
            board=BoardProfile.from_dict(data["board"]),
            created_at=data["created_at"],
            port=data.get("port"),
            baud=data.get("baud"),
        )


@dataclass
class Summary:
    """Final AI-readable session summary."""

    session_id: str
    verdict: Verdict
    generated_at: str
    phase_results: dict[str, bool | None]
    notable_events: list[str]
    event_count: int

    def to_dict(self) -> dict:
        return {
            "session_id": self.session_id,
            "verdict": self.verdict.value,
            "generated_at": self.generated_at,
            "phase_results": self.phase_results,
            "notable_events": self.notable_events,
            "event_count": self.event_count,
        }

    @classmethod
    def from_dict(cls, data: dict) -> "Summary":
        return cls(
            session_id=data["session_id"],
            verdict=Verdict(data["verdict"]),
            generated_at=data["generated_at"],
            phase_results=data["phase_results"],
            notable_events=list(data["notable_events"]),
            event_count=data["event_count"],
        )
