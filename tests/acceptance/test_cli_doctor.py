"""Acceptance tests for `cockpit32 doctor` — success criteria translate
directly into executable CLI checks (exit code + output content).
"""

from click.testing import CliRunner

from cockpit32.cli import main


def test_doctor_runs_and_reports_python():
    runner = CliRunner()
    result = runner.invoke(main, ["doctor"])
    assert "Cockpit 32 doctor report:" in result.output
    assert "python" in result.output


def test_doctor_exit_code_reflects_idf_visibility():
    """In this agent environment idf.py is not installed, so doctor
    should exit non-zero while still printing a clear, actionable report
    (this is the expected/Deferred-to-Stage-4 behavior, not a bug).
    """
    runner = CliRunner()
    result = runner.invoke(main, ["doctor"])
    assert "idf.py on PATH" in result.output
    if "[MISSING] idf.py on PATH" in result.output:
        assert result.exit_code == 1
    else:
        assert result.exit_code == 0
