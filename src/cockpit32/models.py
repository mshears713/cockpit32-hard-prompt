from __future__ import annotations

import json
from dataclasses import asdict, dataclass, field
from datetime import datetime, timezone
from enum import Enum
from pathlib import Path
from typing import Any

BOARD_ID = "esp32-s3-box-3"


def utc_now() -> datetime:
    return datetime.now(timezone.utc)


def to_jsonable(value: Any) -> Any:
    if isinstance(value, datetime):
        return value.isoformat()
    if isinstance(value, Enum):
        return value.value
    if isinstance(value, dict):
        return {k: to_jsonable(v) for k, v in value.items()}
    if isinstance(value, list):
        return [to_jsonable(v) for v in value]
    return value


class JsonMixin:
    def to_dict(self) -> dict[str, Any]:
        return to_jsonable(asdict(self))

    def to_json(self, indent: int | None = None) -> str:
        return json.dumps(self.to_dict(), indent=indent, sort_keys=True)


class CommandStatus(str, Enum):
    passed = "passed"
    failed = "failed"
    not_run = "not_run"


@dataclass(frozen=True)
class CommandResult(JsonMixin):
    command: list[str]
    cwd: str
    returncode: int
    started_at: datetime
    ended_at: datetime
    log_path: str | None = None

    @property
    def status(self) -> CommandStatus:
        return CommandStatus.passed if self.returncode == 0 else CommandStatus.failed


@dataclass(frozen=True)
class SessionMetadata(JsonMixin):
    session_id: str
    project_path: str
    port: str | None = None
    schema_version: int = 1
    board: str = BOARD_ID
    created_at: datetime = field(default_factory=utc_now)
    status: str = "open"

    @classmethod
    def from_json(cls, text: str) -> "SessionMetadata":
        data = json.loads(text)
        data["created_at"] = datetime.fromisoformat(data["created_at"])
        return cls(**data)


@dataclass(frozen=True)
class EventRecord(JsonMixin):
    kind: str
    message: str
    data: dict[str, Any] = field(default_factory=dict)
    schema_version: int = 1
    timestamp: datetime = field(default_factory=utc_now)


@dataclass(frozen=True)
class SessionSummary(JsonMixin):
    session_id: str
    project_path: str
    port: str | None = None
    verdict: str = "inconclusive"
    commands: dict[str, str] = field(default_factory=dict)
    notable_lines: list[str] = field(default_factory=list)
    notes: list[str] = field(default_factory=list)
    schema_version: int = 1
    board: str = BOARD_ID
    generated_at: datetime = field(default_factory=utc_now)


def project_cockpit_dir(project_path: Path) -> Path:
    return project_path / ".cockpit32"
