"""Fake-first tests for monitor capture and notable-line classification."""

from cockpit32.core.monitor import (
    TranscriptMonitorSource,
    classify_line,
    notable_lines,
    run_monitor,
)

from tests.fakes.fake_runner import load_fixture


def _lines(fixture_name: str) -> list[str]:
    text = load_fixture("monitor_transcripts", fixture_name)
    return text.splitlines()


def test_run_monitor_writes_raw_log_and_returns_lines(tmp_path):
    source = TranscriptMonitorSource(lines=_lines("boot_normal.txt"))
    log_dir = tmp_path / "session"

    lines = run_monitor(port="COM3", duration_s=5, source=source, log_dir=log_dir)

    assert lines == _lines("boot_normal.txt")
    log_text = (log_dir / "monitor.log").read_text()
    assert "Application main loop started" in log_text


def test_classify_line_detects_guru_meditation():
    assert classify_line("Guru Meditation Error: Core 0 panic'ed (LoadProhibited).") == "error"


def test_classify_line_detects_brownout_warning():
    assert classify_line("Brownout detector was triggered") == "warning"


def test_classify_line_detects_boot_marker():
    assert classify_line("rst:0x1 (POWERON),boot:0x8 (SPI_FAST_FLASH_BOOT)") == "boot"


def test_classify_line_returns_none_for_plain_output():
    assert classify_line("I (2001) box3_demo: Application main loop started") is None


def test_notable_lines_normal_boot_has_only_boot_markers():
    lines = _lines("boot_normal.txt")
    notable = notable_lines(lines)
    assert any("rst:0x1" in line for line in notable)
    assert not any("Guru Meditation" in line for line in notable)


def test_notable_lines_flags_crash():
    lines = _lines("boot_guru_meditation.txt")
    notable = notable_lines(lines)
    assert any("Guru Meditation" in line for line in notable)


def test_notable_lines_flags_brownout():
    lines = _lines("boot_brownout.txt")
    notable = notable_lines(lines)
    assert any("Brownout" in line for line in notable)
