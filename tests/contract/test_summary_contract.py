"""Contract-first + golden-file tests for summary.json / summary.md.

These are the AI-readable end product of a session — the thing an
agent is handed to understand what happened without Mike's memory.
"""

import json
from pathlib import Path

from cockpit32.core.models import CommandResult, Event
from cockpit32.core.summaries import build_summary, write_summary

GOLDEN_DIR = Path(__file__).parent.parent / "golden"


def _ok_result() -> CommandResult:
    return CommandResult(
        command="idf.py", args=[], returncode=0, stdout="", stderr="",
        started_at="t0", ended_at="t1",
    )


def test_summary_json_and_markdown_match_golden_files(tmp_path):
    events = [Event(kind="note", message="Screen went black after boot.",
                     timestamp="2026-07-06T01:04:30+00:00")]
    monitor_lines = ["Guru Meditation Error: Core 0 panic'ed (LoadProhibited). Exception was unhandled."]

    summary = build_summary(
        session_id="20260706-010203-deadbeef",
        generated_at="2026-07-06T01:05:00+00:00",
        build_result=_ok_result(),
        flash_result=_ok_result(),
        monitor_lines=monitor_lines,
        events=events,
    )
    json_path, md_path = write_summary(tmp_path, summary, events)

    actual_json = json.loads(json_path.read_text())
    expected_json = json.loads((GOLDEN_DIR / "summary.json").read_text())
    assert actual_json == expected_json

    assert md_path.read_text() == (GOLDEN_DIR / "summary.md").read_text()


def test_summary_json_required_keys_present(tmp_path):
    summary = build_summary(
        session_id="s1",
        generated_at="t0",
        build_result=None,
        flash_result=None,
        monitor_lines=[],
        events=[],
    )
    json_path, _ = write_summary(tmp_path, summary, [])
    data = json.loads(json_path.read_text())
    required = {"session_id", "verdict", "generated_at", "phase_results", "notable_events", "event_count"}
    assert required <= data.keys()
    assert data["verdict"] in {"success", "partial", "failed", "blocked", "unknown"}
