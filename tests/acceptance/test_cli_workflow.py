"""Acceptance tests for the CLI build-flash-monitor-note-summary workflow.

`build`/`flash` use the real SubprocessCommandRunner here (no fake
injected), which exercises the actual no-idf.py-on-PATH failure path in
this agent environment — proving the CLI degrades gracefully rather
than crashing. Real success/failure against a real idf.py is Deferred
to Stage 4.
"""

import json

from click.testing import CliRunner

from cockpit32.cli import main


def test_session_start_and_show(tmp_path):
    runner = CliRunner()
    result = runner.invoke(main, ["session", "start", "--project", str(tmp_path)])
    assert result.exit_code == 0
    assert "Started session" in result.output

    result = runner.invoke(main, ["session", "show", "--project", str(tmp_path)])
    assert result.exit_code == 0
    assert "session_id:" in result.output
    assert "board:        esp32-s3-box-3" in result.output


def test_build_without_session_gives_clear_error(tmp_path):
    runner = CliRunner()
    result = runner.invoke(main, ["build", "--project", str(tmp_path)])
    assert result.exit_code != 0
    assert "session start" in result.output


def test_build_without_idf_py_fails_gracefully(tmp_path):
    runner = CliRunner()
    runner.invoke(main, ["session", "start", "--project", str(tmp_path)])

    result = runner.invoke(main, ["build", "--project", str(tmp_path)])

    assert result.exit_code == 1
    assert "build: FAIL" in result.output


def test_note_is_recorded_in_events(tmp_path):
    runner = CliRunner()
    runner.invoke(main, ["session", "start", "--project", str(tmp_path)])
    result = runner.invoke(main, ["note", "--project", str(tmp_path), "touched the screen"])
    assert result.exit_code == 0
    assert "recorded note: touched the screen" in result.output


def test_monitor_with_transcript_and_summary_end_to_end(tmp_path):
    transcript = "tests/fixtures/monitor_transcripts/boot_guru_meditation.txt"
    runner = CliRunner()
    runner.invoke(main, ["session", "start", "--project", str(tmp_path)])
    runner.invoke(main, ["note", "--project", str(tmp_path), "Screen froze after boot."])

    mon_result = runner.invoke(
        main,
        ["monitor", "--project", str(tmp_path), "--port", "COM3",
         "--transcript", transcript],
    )
    assert mon_result.exit_code == 0
    assert "captured" in mon_result.output

    sum_result = runner.invoke(main, ["summary", "--project", str(tmp_path)])
    assert sum_result.exit_code == 0
    assert "verdict: partial" in sum_result.output

    from cockpit32.core.sessions import load_session

    handle = load_session(tmp_path)
    summary_data = json.loads((handle.session_dir / "summary.json").read_text())
    assert summary_data["verdict"] == "partial"
    assert any("Guru Meditation" in line for line in summary_data["notable_events"])


def test_summary_verdict_override(tmp_path):
    runner = CliRunner()
    runner.invoke(main, ["session", "start", "--project", str(tmp_path)])

    result = runner.invoke(
        main, ["summary", "--project", str(tmp_path), "--verdict", "blocked"]
    )
    assert result.exit_code == 0
    assert "verdict: blocked" in result.output
