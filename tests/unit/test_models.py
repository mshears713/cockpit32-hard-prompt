"""TDD unit tests for core domain models (Engineering Method Selection: TDD)."""

from cockpit32.core.models import (
    BoardProfile,
    CommandResult,
    Event,
    SessionMeta,
    Summary,
    Verdict,
)


def test_board_profile_roundtrip():
    board = BoardProfile()
    assert board.name == "esp32-s3-box-3"
    assert BoardProfile.from_dict(board.to_dict()) == board


def test_command_result_success_true_on_zero_returncode():
    result = CommandResult(
        command="idf.py",
        args=["build"],
        returncode=0,
        stdout="done",
        stderr="",
        started_at="2026-01-01T00:00:00+00:00",
        ended_at="2026-01-01T00:00:05+00:00",
    )
    assert result.success is True


def test_command_result_success_false_on_nonzero_returncode():
    result = CommandResult(
        command="idf.py",
        args=["build"],
        returncode=1,
        stdout="",
        stderr="error",
        started_at="2026-01-01T00:00:00+00:00",
        ended_at="2026-01-01T00:00:05+00:00",
    )
    assert result.success is False


def test_command_result_roundtrip_includes_derived_success():
    result = CommandResult(
        command="idf.py",
        args=["-p", "COM3", "flash"],
        returncode=0,
        stdout="ok",
        stderr="",
        started_at="t0",
        ended_at="t1",
    )
    data = result.to_dict()
    assert data["success"] is True
    restored = CommandResult.from_dict(data)
    assert restored == result


def test_event_defaults_kind_source_and_has_timestamp():
    event = Event(kind="note", message="touched screen")
    assert event.source == "user"
    assert event.timestamp  # non-empty ISO string set by default factory


def test_event_roundtrip():
    event = Event(kind="marker", message="reset pressed", source="user", timestamp="t0")
    assert Event.from_dict(event.to_dict()) == event


def test_session_meta_roundtrip():
    meta = SessionMeta(
        session_id="20260706-000000-abcd",
        project_path="/projects/box3-demo",
        board=BoardProfile(),
        created_at="2026-07-06T00:00:00+00:00",
        port="COM3",
        baud=115200,
    )
    assert SessionMeta.from_dict(meta.to_dict()) == meta


def test_session_meta_port_and_baud_default_to_none():
    meta = SessionMeta(
        session_id="s1",
        project_path="/p",
        board=BoardProfile(),
        created_at="t0",
    )
    assert meta.port is None
    assert meta.baud is None


def test_summary_roundtrip_preserves_verdict_enum():
    summary = Summary(
        session_id="s1",
        verdict=Verdict.PARTIAL,
        generated_at="t0",
        phase_results={"build": True, "flash": None, "monitor": None},
        notable_events=["ERROR: brownout detector was triggered"],
        event_count=3,
    )
    restored = Summary.from_dict(summary.to_dict())
    assert restored == summary
    assert restored.verdict is Verdict.PARTIAL
