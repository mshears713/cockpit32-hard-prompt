"""Fake-first tests for the build runner against synthetic idf.py fixtures."""

from cockpit32.core.idf_runner import build, guidance_for_failure

from tests.fakes.fake_runner import FakeCommandRunner, load_fixture


def test_build_success_captures_log_and_returns_success(tmp_path):
    stdout = load_fixture("idf_build", "success_stdout.txt")
    runner = FakeCommandRunner(returncode=0, stdout=stdout, stderr="")
    log_dir = tmp_path / "session"

    result = build(project_path=tmp_path, runner=runner, log_dir=log_dir)

    assert result.success is True
    assert runner.calls == [(["idf.py", "build"], tmp_path)]
    log_text = (log_dir / "build.log").read_text()
    assert "Project build complete" in log_text
    assert "returncode: 0" in log_text


def test_build_failure_preserves_stderr_in_log(tmp_path):
    stdout = load_fixture("idf_build", "failure_stdout.txt")
    stderr = load_fixture("idf_build", "failure_stderr.txt")
    runner = FakeCommandRunner(returncode=1, stdout=stdout, stderr=stderr)
    log_dir = tmp_path / "session"

    result = build(project_path=tmp_path, runner=runner, log_dir=log_dir)

    assert result.success is False
    log_text = (log_dir / "build.log").read_text()
    assert "guri_init" in log_text
    assert "ninja: build stopped" in log_text


def test_guidance_for_missing_idf_py():
    stderr = "[Errno 2] No such file or directory: 'idf.py'"
    advice = guidance_for_failure("", stderr)
    assert advice is not None
    assert "cockpit32 doctor" in advice


def test_guidance_is_none_for_unrecognized_failure():
    assert guidance_for_failure("some odd output", "another odd error") is None
