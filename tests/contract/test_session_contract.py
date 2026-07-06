"""Contract-first tests for the session.json / events.jsonl on-disk shape.

These are the AI-readability contract: the product's core promise per
the Project Brief. Golden files live in tests/golden/.
"""

import json
from datetime import datetime, timezone
from pathlib import Path

from cockpit32.core.models import BoardProfile, Event
from cockpit32.core.sessions import append_event, create_session

GOLDEN_DIR = Path(__file__).parent.parent / "golden"


def test_session_json_matches_golden_shape(tmp_path):
    handle = create_session(
        tmp_path,
        board=BoardProfile(),
        port="COM7",
        baud=115200,
        now=datetime(2026, 7, 6, 1, 2, 3, tzinfo=timezone.utc),
        session_id="20260706-010203-deadbeef",
    )
    actual = json.loads((handle.session_dir / "session.json").read_text())

    expected = json.loads((GOLDEN_DIR / "session.json").read_text())
    expected["project_path"] = str(Path(tmp_path).resolve())

    assert actual == expected


def test_session_json_required_keys_present(tmp_path):
    handle = create_session(tmp_path)
    data = json.loads((handle.session_dir / "session.json").read_text())
    required_keys = {"session_id", "project_path", "board", "created_at", "port", "baud"}
    assert required_keys <= data.keys()
    assert {"name", "default_baud"} <= data["board"].keys()


def test_events_jsonl_is_one_json_object_per_line(tmp_path):
    handle = create_session(tmp_path)
    append_event(handle, Event(kind="note", message="m1", timestamp="t0"))
    append_event(handle, Event(kind="marker", message="m2", timestamp="t1"))

    lines = handle.events_path.read_text().splitlines()
    assert len(lines) == 2
    for line in lines:
        obj = json.loads(line)  # must not raise
        assert {"timestamp", "kind", "source", "message"} <= obj.keys()
