"""Project-local session storage: .cockpit32/sessions/<session_id>/.

Contract-first: session.json and events.jsonl are the AI-readable
artifacts other tools/agents read, so their on-disk shape is treated as
a contract (see tests/contract + tests/golden).
"""

from __future__ import annotations

import json
import uuid
from dataclasses import dataclass
from datetime import datetime, timezone
from pathlib import Path

from cockpit32.core.models import BoardProfile, Event, SessionMeta

SESSIONS_DIRNAME = ".cockpit32/sessions"
SESSION_FILE = "session.json"
EVENTS_FILE = "events.jsonl"
LATEST_POINTER_FILE = "latest"
BUILD_LOG_FILE = "build.log"
FLASH_LOG_FILE = "flash.log"
MONITOR_LOG_FILE = "monitor.log"
SUMMARY_JSON_FILE = "summary.json"
SUMMARY_MD_FILE = "summary.md"


class SessionNotFoundError(RuntimeError):
    pass


@dataclass
class SessionHandle:
    """A resolved on-disk session: metadata plus its directory."""

    meta: SessionMeta
    session_dir: Path

    @property
    def events_path(self) -> Path:
        return self.session_dir / EVENTS_FILE


def _sessions_root(project_path: Path) -> Path:
    return Path(project_path) / SESSIONS_DIRNAME


def _new_session_id(now: datetime) -> str:
    return f"{now.strftime('%Y%m%d-%H%M%S')}-{uuid.uuid4().hex[:8]}"


def create_session(
    project_path: str | Path,
    board: BoardProfile | None = None,
    port: str | None = None,
    baud: int | None = None,
    now: datetime | None = None,
    session_id: str | None = None,
) -> SessionHandle:
    """Create a new timestamped session folder and write session.json.

    ``session_id`` is exposed as an override (rather than always derived
    from ``now`` + a random suffix) so contract/golden tests can produce
    deterministic session.json fixtures without mocking uuid4.
    """
    project_path = Path(project_path).resolve()
    now = now or datetime.now(timezone.utc)
    board = board or BoardProfile()

    session_id = session_id or _new_session_id(now)
    root = _sessions_root(project_path)
    session_dir = root / session_id
    session_dir.mkdir(parents=True, exist_ok=False)

    meta = SessionMeta(
        session_id=session_id,
        project_path=str(project_path),
        board=board,
        created_at=now.isoformat(),
        port=port,
        baud=baud,
    )
    (session_dir / SESSION_FILE).write_text(
        json.dumps(meta.to_dict(), indent=2) + "\n", encoding="utf-8"
    )
    (session_dir / EVENTS_FILE).touch()
    _set_latest(project_path, session_id)

    return SessionHandle(meta=meta, session_dir=session_dir)


def _set_latest(project_path: Path, session_id: str) -> None:
    root = _sessions_root(project_path)
    (root / LATEST_POINTER_FILE).write_text(session_id + "\n", encoding="utf-8")


def latest_session_id(project_path: str | Path) -> str | None:
    root = _sessions_root(Path(project_path).resolve())
    pointer = root / LATEST_POINTER_FILE
    if not pointer.exists():
        return None
    return pointer.read_text(encoding="utf-8").strip() or None


def load_session(project_path: str | Path, session_id: str | None = None) -> SessionHandle:
    """Load a session by id, or the latest session if id is omitted."""
    project_path = Path(project_path).resolve()
    session_id = session_id or latest_session_id(project_path)
    if session_id is None:
        raise SessionNotFoundError(
            f"No sessions found under {project_path}. Run 'cockpit32 session start' first."
        )
    session_dir = _sessions_root(project_path) / session_id
    session_file = session_dir / SESSION_FILE
    if not session_file.exists():
        raise SessionNotFoundError(f"Session '{session_id}' not found under {project_path}.")
    meta = SessionMeta.from_dict(json.loads(session_file.read_text(encoding="utf-8")))
    return SessionHandle(meta=meta, session_dir=session_dir)


def append_event(handle: SessionHandle, event: Event) -> None:
    with handle.events_path.open("a", encoding="utf-8") as f:
        f.write(json.dumps(event.to_dict()) + "\n")


def read_events(handle: SessionHandle) -> list[Event]:
    if not handle.events_path.exists():
        return []
    events = []
    for line in handle.events_path.read_text(encoding="utf-8").splitlines():
        line = line.strip()
        if line:
            events.append(Event.from_dict(json.loads(line)))
    return events
