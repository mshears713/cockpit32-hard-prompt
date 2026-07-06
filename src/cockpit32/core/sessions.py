from __future__ import annotations

import json
from datetime import datetime, timezone
from pathlib import Path

from cockpit32.models import EventRecord, SessionMetadata, project_cockpit_dir


def _session_id(now: datetime | None = None) -> str:
    now = now or datetime.now(timezone.utc)
    return now.strftime("%Y%m%dT%H%M%SZ")


class SessionStore:
    def __init__(self, project_path: Path):
        self.project_path = project_path.resolve()
        self.root = project_cockpit_dir(self.project_path)
        self.sessions_root = self.root / "sessions"

    def start(self, port: str | None = None) -> SessionMetadata:
        self.sessions_root.mkdir(parents=True, exist_ok=True)
        metadata = SessionMetadata(
            session_id=_session_id(), project_path=str(self.project_path), port=port
        )
        session_dir = self.session_dir(metadata.session_id)
        session_dir.mkdir(parents=True, exist_ok=False)
        (session_dir / "logs").mkdir()
        self.write_json(session_dir / "session.json", metadata.to_dict())
        (session_dir / "events.jsonl").touch()
        (self.root / "latest-session.txt").write_text(metadata.session_id + "\n", encoding="utf-8")
        self.add_event(metadata.session_id, "session_started", "Session started", {"port": port})
        return metadata

    def session_dir(self, session_id: str) -> Path:
        return self.sessions_root / session_id

    def add_event(self, session_id: str, kind: str, message: str, data: dict | None = None) -> EventRecord:
        event = EventRecord(kind=kind, message=message, data=data or {})
        path = self.session_dir(session_id) / "events.jsonl"
        with path.open("a", encoding="utf-8") as handle:
            handle.write(event.to_json() + "\n")
        return event

    @staticmethod
    def write_json(path: Path, payload: dict) -> None:
        path.write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n", encoding="utf-8")
