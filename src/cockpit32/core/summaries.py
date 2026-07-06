from __future__ import annotations

import json
from pathlib import Path

from cockpit32.models import SessionMetadata, SessionSummary

KEYWORDS = ("error", "fail", "warning", "rst:", "abort", "exception", "ESP-ROM")


def notable_lines(text: str) -> list[str]:
    lines: list[str] = []
    for line in text.splitlines():
        if any(key.lower() in line.lower() for key in KEYWORDS):
            lines.append(line[:300])
    return lines[:25]


def load_events(session_dir: Path) -> list[dict]:
    events_path = session_dir / "events.jsonl"
    if not events_path.exists():
        return []
    return [json.loads(line) for line in events_path.read_text(encoding="utf-8").splitlines() if line]


def generate_summary(session_dir: Path) -> SessionSummary:
    metadata = SessionMetadata.from_json((session_dir / "session.json").read_text(encoding="utf-8"))
    commands: dict[str, str] = {}
    notes: list[str] = []
    notable: list[str] = []
    for event in load_events(session_dir):
        if event["kind"] == "note":
            notes.append(event["message"])
        if event["kind"].endswith("_completed"):
            commands[event["kind"].removesuffix("_completed")] = event["data"].get("status", "unknown")
    logs_dir = session_dir / "logs"
    if logs_dir.exists():
        for log in sorted(logs_dir.glob("*.log")):
            notable.extend(notable_lines(log.read_text(encoding="utf-8", errors="replace")))
    verdict = "fail" if any(status == "failed" for status in commands.values()) else "inconclusive"
    summary = SessionSummary(
        session_id=metadata.session_id,
        project_path=metadata.project_path,
        port=metadata.port,
        verdict=verdict,
        commands=commands,
        notable_lines=notable[:25],
        notes=notes,
    )
    (session_dir / "summary.json").write_text(summary.to_json(indent=2) + "\n", encoding="utf-8")
    md = [f"# Cockpit 32 Session {summary.session_id}", "", f"Verdict: **{summary.verdict}**", "", "## Commands"]
    md += [f"- {name}: {status}" for name, status in summary.commands.items()] or ["- None recorded"]
    md += ["", "## Operator Notes"] + ([f"- {note}" for note in summary.notes] or ["- None recorded"])
    md += ["", "## Notable Lines"] + ([f"- `{line}`" for line in summary.notable_lines] or ["- None detected"])
    (session_dir / "summary.md").write_text("\n".join(md) + "\n", encoding="utf-8")
    return summary
