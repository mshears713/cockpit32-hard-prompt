"""Cockpit 32 CLI.

The CLI is a thin wrapper over cockpit32.core services — the GUI shell
(M6) calls the same functions, so behavior is defined and tested here.
"""

from __future__ import annotations

import sys
from pathlib import Path

import click

from cockpit32.core.doctor import run_doctor
from cockpit32.core.idf_runner import SubprocessCommandRunner, build as run_build, flash as run_flash
from cockpit32.core.models import BoardProfile, Event, Verdict
from cockpit32.core.monitor import SubprocessMonitorSource, TranscriptMonitorSource, run_monitor
from cockpit32.core.sessions import (
    SessionNotFoundError,
    append_event,
    create_session,
    load_session,
    read_events,
)
from cockpit32.core.summaries import generate_session_summary, write_summary


@click.group()
@click.version_option(package_name="cockpit32")
def main() -> None:
    """Cockpit 32 — local ESP32 mission-control tool."""


@main.command()
def doctor() -> None:
    """Check whether the ESP-IDF environment is visible."""
    report = run_doctor()
    click.echo(report.render())
    sys.exit(0 if report.all_ok else 1)


@main.group()
def session() -> None:
    """Manage build/flash/monitor sessions."""


@session.command("start")
@click.option("--project", "project_path", default=".", show_default=True,
              type=click.Path(exists=True, file_okay=False))
@click.option("--port", default=None, help="Serial port to remember for this session.")
@click.option("--baud", default=None, type=int, help="Baud rate to remember for this session.")
def session_start(project_path: str, port: str | None, baud: int | None) -> None:
    """Start a new timestamped session under PROJECT/.cockpit32/sessions/."""
    handle = create_session(project_path, board=BoardProfile(), port=port, baud=baud)
    click.echo(f"Started session {handle.meta.session_id} in {handle.session_dir}")


@session.command("show")
@click.option("--project", "project_path", default=".", show_default=True,
              type=click.Path(exists=True, file_okay=False))
@click.option("--session-id", "session_id", default=None, help="Defaults to the latest session.")
def session_show(project_path: str, session_id: str | None) -> None:
    """Show metadata and events for a session (defaults to latest)."""
    try:
        handle = load_session(project_path, session_id)
    except SessionNotFoundError as exc:
        raise click.ClickException(str(exc))
    click.echo(f"session_id:   {handle.meta.session_id}")
    click.echo(f"project_path: {handle.meta.project_path}")
    click.echo(f"board:        {handle.meta.board.name}")
    click.echo(f"port:         {handle.meta.port}")
    events = read_events(handle)
    click.echo(f"events:       {len(events)}")


@main.command()
@click.option("--project", "project_path", default=".", show_default=True,
              type=click.Path(exists=True, file_okay=False))
def build(project_path: str) -> None:
    """Run `idf.py build` and capture evidence into the latest session."""
    try:
        handle = load_session(project_path)
    except SessionNotFoundError as exc:
        raise click.ClickException(str(exc))
    result = run_build(Path(project_path), SubprocessCommandRunner(), handle.session_dir)
    click.echo(f"build: {'PASS' if result.success else 'FAIL'} (see {handle.session_dir / 'build.log'})")
    sys.exit(0 if result.success else 1)


@main.command()
@click.option("--project", "project_path", default=".", show_default=True,
              type=click.Path(exists=True, file_okay=False))
@click.option("--port", required=True, help="Serial port, e.g. COM3 or /dev/ttyUSB0.")
def flash(project_path: str, port: str) -> None:
    """Run `idf.py -p PORT flash` and capture evidence into the latest session."""
    try:
        handle = load_session(project_path)
    except SessionNotFoundError as exc:
        raise click.ClickException(str(exc))
    result = run_flash(Path(project_path), port, SubprocessCommandRunner(), handle.session_dir)
    click.echo(f"flash: {'PASS' if result.success else 'FAIL'} (see {handle.session_dir / 'flash.log'})")
    sys.exit(0 if result.success else 1)


@main.command()
@click.option("--project", "project_path", default=".", show_default=True,
              type=click.Path(exists=True, file_okay=False))
@click.option("--port", required=True, help="Serial port, e.g. COM3 or /dev/ttyUSB0.")
@click.option("--duration", default=10.0, show_default=True, help="Seconds to capture.")
@click.option("--transcript", "transcript_path", default=None, type=click.Path(exists=True),
              help="Replay a synthetic transcript file instead of a live device (for dev/testing).")
def monitor(project_path: str, port: str, duration: float, transcript_path: str | None) -> None:
    """Capture a timed monitor session into the latest session."""
    try:
        handle = load_session(project_path)
    except SessionNotFoundError as exc:
        raise click.ClickException(str(exc))
    if transcript_path:
        lines = Path(transcript_path).read_text(encoding="utf-8").splitlines()
        source = TranscriptMonitorSource(lines=lines)
    else:
        source = SubprocessMonitorSource(port=port)
    lines = run_monitor(port, duration, source, handle.session_dir)
    click.echo(f"monitor: captured {len(lines)} lines (see {handle.session_dir / 'monitor.log'})")


@main.command()
@click.argument("message")
@click.option("--project", "project_path", default=".", show_default=True,
              type=click.Path(exists=True, file_okay=False))
@click.option("--kind", default="note", show_default=True, help="note | marker")
def note(message: str, project_path: str, kind: str) -> None:
    """Record an operator note or event marker in the latest session."""
    try:
        handle = load_session(project_path)
    except SessionNotFoundError as exc:
        raise click.ClickException(str(exc))
    append_event(handle, Event(kind=kind, message=message))
    click.echo(f"recorded {kind}: {message}")


@main.command()
@click.option("--project", "project_path", default=".", show_default=True,
              type=click.Path(exists=True, file_okay=False))
@click.option("--verdict", "override_verdict", default=None,
              type=click.Choice([v.value for v in Verdict]),
              help="Force the verdict field (operator's physical observation outranks machine signal).")
def summary(project_path: str, override_verdict: str | None) -> None:
    """Generate summary.json and summary.md for the latest session."""
    try:
        handle = load_session(project_path)
    except SessionNotFoundError as exc:
        raise click.ClickException(str(exc))

    override = Verdict(override_verdict) if override_verdict else None
    summary_obj = generate_session_summary(handle, override=override)
    json_path, md_path = write_summary(handle.session_dir, summary_obj, read_events(handle))
    click.echo(f"verdict: {summary_obj.verdict.value}")
    click.echo(f"summary written to {json_path} and {md_path}")


if __name__ == "__main__":
    main()
