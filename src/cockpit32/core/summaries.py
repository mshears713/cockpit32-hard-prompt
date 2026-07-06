"""Session summary generation: the AI-readable end product of a session.

Engineering Method Selection: contract-first + golden files for the
generated shapes (summary.json / summary.md); the verdict logic itself
is plain, specifiable logic (TDD-suitable).
"""

from __future__ import annotations

from pathlib import Path

from cockpit32.core.models import CommandResult, Event, Summary, Verdict
from cockpit32.core.monitor import notable_lines

SUMMARY_JSON_FILE = "summary.json"
SUMMARY_MD_FILE = "summary.md"


def compute_verdict(
    build_result: CommandResult | None,
    flash_result: CommandResult | None,
    monitor_lines: list[str],
    override: Verdict | None = None,
) -> Verdict:
    """Derive a verdict from phase results and monitor output.

    An explicit operator override (recorded as a note) always wins —
    Mike's physical observation of the hardware outranks any machine
    signal, since the tool cannot see the screen or hear the device.
    """
    if override is not None:
        return override
    if flash_result is not None and not flash_result.success:
        return Verdict.FAILED
    if build_result is not None and not build_result.success:
        return Verdict.FAILED
    if build_result is None and flash_result is None and not monitor_lines:
        return Verdict.UNKNOWN
    if any(line for line in notable_lines(monitor_lines) if _is_error_line(line)):
        return Verdict.PARTIAL
    return Verdict.SUCCESS


def _is_error_line(line: str) -> bool:
    from cockpit32.core.monitor import classify_line

    return classify_line(line) == "error"


def build_summary(
    session_id: str,
    generated_at: str,
    build_result: CommandResult | None,
    flash_result: CommandResult | None,
    monitor_lines: list[str],
    events: list[Event],
    override: Verdict | None = None,
) -> Summary:
    verdict = compute_verdict(build_result, flash_result, monitor_lines, override)
    return Summary(
        session_id=session_id,
        verdict=verdict,
        generated_at=generated_at,
        phase_results={
            "build": None if build_result is None else build_result.success,
            "flash": None if flash_result is None else flash_result.success,
            "monitor": None if not monitor_lines else True,
        },
        notable_events=_labeled_notable_lines(monitor_lines),
        event_count=len(events),
    )


def _labeled_notable_lines(monitor_lines: list[str]) -> list[str]:
    """Prefix each notable line with its classification (error/warning/boot).

    An AI-readability test (Stage 3 Validation Strategy) against an
    earlier unlabeled version found a reader could not tell a fatal
    crash apart from a routine boot marker without opening the raw
    monitor log — this labels severity inline so the summary is
    self-sufficient.
    """
    from cockpit32.core.monitor import classify_line

    return [f"[{classify_line(line)}] {line}" for line in notable_lines(monitor_lines)]


def render_markdown(summary: Summary, events: list[Event]) -> str:
    lines = [
        f"# Cockpit 32 Session Summary — {summary.session_id}",
        "",
        f"- **Verdict:** {summary.verdict.value}",
        f"- **Generated at:** {summary.generated_at}",
        f"- **Events recorded:** {summary.event_count}",
        "",
        "## Phase Results",
    ]
    for phase, ok in summary.phase_results.items():
        if ok is None:
            status = "not run"
        elif phase == "monitor":
            # Monitor has no pass/fail of its own — it either captured
            # output or it didn't. "pass" here previously misled a reader
            # into thinking the device's boot was judged healthy even
            # when a fatal crash was among the captured lines.
            status = "captured"
        else:
            status = "pass" if ok else "fail"
        lines.append(f"- {phase}: {status}")

    lines.append("")
    lines.append("## Notable Monitor Lines")
    if summary.notable_events:
        for line in summary.notable_events:
            lines.append(f"- `{line}`")
    else:
        lines.append("- none")

    lines.append("")
    lines.append("## Operator Notes")
    if events:
        for event in events:
            lines.append(f"- [{event.timestamp}] ({event.kind}) {event.message}")
    else:
        lines.append("- none")

    return "\n".join(lines) + "\n"


def write_summary(session_dir: Path, summary: Summary, events: list[Event]) -> tuple[Path, Path]:
    import json

    json_path = session_dir / SUMMARY_JSON_FILE
    md_path = session_dir / SUMMARY_MD_FILE
    json_path.write_text(json.dumps(summary.to_dict(), indent=2) + "\n", encoding="utf-8")
    md_path.write_text(render_markdown(summary, events), encoding="utf-8")
    return json_path, md_path


def generate_session_summary(handle, override: Verdict | None = None) -> Summary:
    """Assemble a Summary from a session's on-disk evidence (logs + events).

    This is the single place that reconstructs phase results and monitor
    lines from disk. The CLI's `summary` command and the GUI's summary
    view both call this — neither reimplements the assembly, per the
    Implementation Engineer boundary "GUI must not contain business
    logic unavailable to the CLI."
    """
    from datetime import datetime, timezone

    from cockpit32.core.idf_runner import load_result
    from cockpit32.core.sessions import read_events

    events = read_events(handle)
    build_json = handle.session_dir / "build.json"
    flash_json = handle.session_dir / "flash.json"
    monitor_log = handle.session_dir / "monitor.log"

    build_result = load_result(build_json) if build_json.exists() else None
    flash_result = load_result(flash_json) if flash_json.exists() else None
    monitor_lines = monitor_log.read_text(encoding="utf-8").splitlines() if monitor_log.exists() else []

    return build_summary(
        session_id=handle.meta.session_id,
        generated_at=datetime.now(timezone.utc).isoformat(),
        build_result=build_result,
        flash_result=flash_result,
        monitor_lines=monitor_lines,
        events=events,
        override=override,
    )
