"""Fake-first tests for the flash wrapper and its failure-path guidance."""

from cockpit32.core.idf_runner import flash, guidance_for_failure

from tests.fakes.fake_runner import FakeCommandRunner, load_fixture


def test_flash_success_captures_log(tmp_path):
    stdout = load_fixture("idf_flash", "success_stdout.txt")
    runner = FakeCommandRunner(returncode=0, stdout=stdout, stderr="")
    log_dir = tmp_path / "session"

    result = flash(project_path=tmp_path, port="COM3", runner=runner, log_dir=log_dir)

    assert result.success is True
    assert runner.calls == [(["idf.py", "-p", "COM3", "flash"], tmp_path)]
    log_text = (log_dir / "flash.log").read_text()
    assert "Hash of data verified" in log_text


def test_flash_port_busy_gives_actionable_guidance(tmp_path):
    stderr = load_fixture("idf_flash", "failure_port_busy_stderr.txt")
    runner = FakeCommandRunner(returncode=2, stdout="", stderr=stderr)
    log_dir = tmp_path / "session"

    result = flash(project_path=tmp_path, port="COM3", runner=runner, log_dir=log_dir)

    assert result.success is False
    advice = guidance_for_failure(result.stdout, result.stderr)
    assert advice is not None
    assert "holding it open" in advice


def test_flash_no_response_gives_actionable_guidance(tmp_path):
    stderr = load_fixture("idf_flash", "failure_no_response_stderr.txt")
    runner = FakeCommandRunner(returncode=2, stdout="", stderr=stderr)
    log_dir = tmp_path / "session"

    result = flash(project_path=tmp_path, port="COM3", runner=runner, log_dir=log_dir)

    advice = guidance_for_failure(result.stdout, result.stderr)
    assert advice is not None
    assert "boot mode" in advice
