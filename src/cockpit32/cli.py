from __future__ import annotations

import argparse
import sys
from pathlib import Path

from cockpit32.core.doctor import run_doctor
from cockpit32.core.idf_runner import IdfRunner
from cockpit32.core.ports import discover_ports
from cockpit32.core.sessions import SessionStore
from cockpit32.core.summaries import generate_summary


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(prog="cockpit32", description="Cockpit 32 ESP-IDF mission-control CLI")
    sub = parser.add_subparsers(dest="command", required=True)
    doctor = sub.add_parser("doctor")
    doctor.add_argument("--idf-command", default="idf.py")
    sub.add_parser("ports")
    start = sub.add_parser("start-session")
    start.add_argument("--project", type=Path, default=Path.cwd())
    start.add_argument("--port")
    for name in ("build", "flash", "monitor"):
        cmd = sub.add_parser(name)
        cmd.add_argument("--project", type=Path, default=Path.cwd())
        cmd.add_argument("--session-id", required=True)
        cmd.add_argument("--idf-command", default="idf.py")
        if name in {"flash", "monitor"}:
            cmd.add_argument("--port", required=True)
        if name == "monitor":
            cmd.add_argument("--seconds", type=int, default=30)
    note = sub.add_parser("note")
    note.add_argument("--project", type=Path, default=Path.cwd())
    note.add_argument("--session-id", required=True)
    note.add_argument("message")
    summary = sub.add_parser("summarize")
    summary.add_argument("--project", type=Path, default=Path.cwd())
    summary.add_argument("--session-id", required=True)
    sub.add_parser("gui")
    return parser


def main(argv: list[str] | None = None) -> int:
    args = build_parser().parse_args(argv)
    if args.command == "doctor":
        report = run_doctor(args.idf_command)
        for check in report.checks:
            print(f"{'PASS' if check.ok else 'WARN'} {check.name}: {check.detail}")
        if not report.ok:
            print("Doctor found warnings; Stage 4 should run this inside Mike's ESP-IDF PowerShell.", file=sys.stderr)
            return 1
        return 0
    if args.command == "ports":
        ports = discover_ports()
        if not ports:
            print("No serial ports discovered.")
        for port in ports:
            print(f"{port.device}\t{port.description}")
        return 0
    if args.command == "start-session":
        print(SessionStore(args.project).start(port=args.port).to_json(indent=2))
        return 0
    if args.command == "build":
        store = SessionStore(args.project)
        result = IdfRunner(args.idf_command).build(args.project, store.session_dir(args.session_id) / "logs" / "build.log")
        store.add_event(args.session_id, "build_completed", "Build completed", {"status": result.status.value, "returncode": result.returncode})
        print(result.to_json(indent=2))
        return 0 if result.returncode == 0 else 1
    if args.command == "flash":
        store = SessionStore(args.project)
        result = IdfRunner(args.idf_command).flash(args.project, args.port, store.session_dir(args.session_id) / "logs" / "flash.log")
        store.add_event(args.session_id, "flash_completed", "Flash completed", {"status": result.status.value, "returncode": result.returncode})
        print(result.to_json(indent=2))
        return 0 if result.returncode == 0 else 1
    if args.command == "monitor":
        store = SessionStore(args.project)
        result = IdfRunner(args.idf_command).monitor(args.project, args.port, store.session_dir(args.session_id) / "logs" / "monitor.log", seconds=args.seconds)
        store.add_event(args.session_id, "monitor_completed", "Monitor completed", {"status": result.status.value, "returncode": result.returncode})
        print(result.to_json(indent=2))
        return 0
    if args.command == "note":
        print(SessionStore(args.project).add_event(args.session_id, "note", args.message).to_json(indent=2))
        return 0
    if args.command == "summarize":
        print(generate_summary(SessionStore(args.project).session_dir(args.session_id)).to_json(indent=2))
        return 0
    if args.command == "gui":
        from cockpit32.gui.app import run
        return run()
    return 2


if __name__ == "__main__":
    raise SystemExit(main())
