"""Unit tests for session lifecycle: create/load/latest-pointer/events.

Runs entirely without hardware (tmp_path only) — this is the
"session can be started without hardware" validation checkpoint for M1.
"""

from datetime import datetime, timezone

import pytest

from cockpit32.core.models import BoardProfile, Event
from cockpit32.core.sessions import (
    SessionNotFoundError,
    append_event,
    create_session,
    latest_session_id,
    load_session,
    read_events,
)


def test_create_session_without_hardware(tmp_path):
    handle = create_session(tmp_path)
    assert handle.session_dir.exists()
    assert (handle.session_dir / "session.json").exists()
    assert (handle.session_dir / "events.jsonl").exists()
    assert handle.meta.board == BoardProfile()


def test_create_session_sets_latest_pointer(tmp_path):
    handle = create_session(tmp_path)
    assert latest_session_id(tmp_path) == handle.meta.session_id


def test_second_session_updates_latest_pointer(tmp_path):
    first = create_session(tmp_path, now=datetime(2026, 1, 1, tzinfo=timezone.utc))
    second = create_session(tmp_path, now=datetime(2026, 1, 1, 0, 0, 1, tzinfo=timezone.utc))
    assert first.meta.session_id != second.meta.session_id
    assert latest_session_id(tmp_path) == second.meta.session_id


def test_load_session_defaults_to_latest(tmp_path):
    handle = create_session(tmp_path, port="COM7", baud=115200)
    loaded = load_session(tmp_path)
    assert loaded.meta == handle.meta


def test_load_session_by_explicit_id(tmp_path):
    handle = create_session(tmp_path)
    loaded = load_session(tmp_path, session_id=handle.meta.session_id)
    assert loaded.meta.session_id == handle.meta.session_id


def test_load_session_raises_when_none_exist(tmp_path):
    with pytest.raises(SessionNotFoundError):
        load_session(tmp_path)


def test_load_session_raises_for_unknown_id(tmp_path):
    create_session(tmp_path)
    with pytest.raises(SessionNotFoundError):
        load_session(tmp_path, session_id="does-not-exist")


def test_append_and_read_events_roundtrip(tmp_path):
    handle = create_session(tmp_path)
    append_event(handle, Event(kind="note", message="pressed reset", timestamp="t0"))
    append_event(handle, Event(kind="marker", message="screen changed", timestamp="t1"))

    events = read_events(handle)
    assert [e.message for e in events] == ["pressed reset", "screen changed"]


def test_read_events_empty_session_returns_empty_list(tmp_path):
    handle = create_session(tmp_path)
    assert read_events(handle) == []


def test_session_ids_are_deterministic_given_clock(tmp_path):
    now = datetime(2026, 7, 6, 1, 2, 3, tzinfo=timezone.utc)
    handle = create_session(tmp_path, now=now)
    assert handle.meta.session_id.startswith("20260706-010203-")
