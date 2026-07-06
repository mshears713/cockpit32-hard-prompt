"""TDD tests for verdict computation logic."""

from cockpit32.core.models import CommandResult, Verdict
from cockpit32.core.summaries import build_summary, compute_verdict, render_markdown


def _result(success: bool) -> CommandResult:
    return CommandResult(
        command="idf.py",
        args=[],
        returncode=0 if success else 1,
        stdout="",
        stderr="",
        started_at="t0",
        ended_at="t1",
    )


def test_no_data_is_unknown():
    assert compute_verdict(None, None, []) == Verdict.UNKNOWN


def test_build_failure_is_failed():
    assert compute_verdict(_result(False), None, []) == Verdict.FAILED


def test_flash_failure_is_failed_even_if_build_passed():
    assert compute_verdict(_result(True), _result(False), []) == Verdict.FAILED


def test_clean_run_is_success():
    assert compute_verdict(_result(True), _result(True), ["I (10) boot: normal"]) == Verdict.SUCCESS


def test_monitor_error_line_after_successful_flash_is_partial():
    lines = ["Guru Meditation Error: Core 0 panic'ed"]
    assert compute_verdict(_result(True), _result(True), lines) == Verdict.PARTIAL


def test_monitor_warning_only_does_not_downgrade_to_partial():
    lines = ["Brownout detector was triggered"]
    assert compute_verdict(_result(True), _result(True), lines) == Verdict.SUCCESS


def test_operator_override_wins_over_computed_verdict():
    assert (
        compute_verdict(_result(True), _result(True), [], override=Verdict.BLOCKED)
        == Verdict.BLOCKED
    )


def test_notable_events_are_labeled_with_severity():
    """Regression test for an AI-readability-test finding: an unlabeled
    notable line left a reader unable to tell a fatal crash apart from a
    routine boot marker without the raw monitor log.
    """
    summary = build_summary(
        session_id="s1",
        generated_at="t0",
        build_result=_result(True),
        flash_result=_result(True),
        monitor_lines=["Guru Meditation Error: Core 0 panic'ed"],
        events=[],
    )
    assert summary.notable_events == ["[error] Guru Meditation Error: Core 0 panic'ed"]


def test_rendered_markdown_calls_monitor_captured_not_pass():
    """Regression test: "monitor: pass" previously implied a health
    judgment the tool never made — monitor only captures, it doesn't
    grade the boot.
    """
    summary = build_summary(
        session_id="s1",
        generated_at="t0",
        build_result=_result(True),
        flash_result=_result(True),
        monitor_lines=["I (10) boot: normal"],
        events=[],
    )
    rendered = render_markdown(summary, [])
    assert "monitor: captured" in rendered
    assert "monitor: pass" not in rendered
