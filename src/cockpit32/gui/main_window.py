"""Cockpit 32 GUI shell.

Engineering Method Selection: timeboxed spike, then test-after with
offscreen smoke tests over the tested core layer. This window contains
no decisions worth proving on its own — every button calls the exact
same cockpit32.core / cockpit32.core.summaries functions the CLI calls,
so correctness lives in tests/unit and tests/acceptance, not here.
"""

from __future__ import annotations

from pathlib import Path

from PySide6.QtWidgets import (
    QFileDialog,
    QHBoxLayout,
    QLabel,
    QLineEdit,
    QMainWindow,
    QPushButton,
    QTextEdit,
    QVBoxLayout,
    QWidget,
)

from cockpit32.core.idf_runner import SubprocessCommandRunner
from cockpit32.core.idf_runner import build as run_build
from cockpit32.core.idf_runner import flash as run_flash
from cockpit32.core.models import Event
from cockpit32.core.monitor import SubprocessMonitorSource, TranscriptMonitorSource, run_monitor
from cockpit32.core.sessions import SessionHandle, SessionNotFoundError, append_event, create_session, load_session
from cockpit32.core.summaries import generate_session_summary, write_summary


class MainWindow(QMainWindow):
    """Basic cockpit surface: project path, port, build/flash/monitor
    actions, a log view, an operator-note control, and a summary view —
    the same v0 GUI shell capabilities named in the Project Brief.
    """

    def __init__(self) -> None:
        super().__init__()
        self.setWindowTitle("Cockpit 32")
        self._handle: SessionHandle | None = None

        self.project_edit = QLineEdit(str(Path.cwd()))
        browse_button = QPushButton("Browse…")
        browse_button.clicked.connect(self._on_browse)

        self.status_label = QLabel("No session")
        self.port_edit = QLineEdit()
        self.port_edit.setPlaceholderText("COM3 or /dev/ttyUSB0")

        start_button = QPushButton("Start Session")
        start_button.clicked.connect(self._on_start_session)
        build_button = QPushButton("Build")
        build_button.clicked.connect(self._on_build)
        flash_button = QPushButton("Flash")
        flash_button.clicked.connect(self._on_flash)
        monitor_button = QPushButton("Monitor")
        monitor_button.clicked.connect(self._on_monitor)

        self.note_edit = QLineEdit()
        self.note_edit.setPlaceholderText("Operator note or event marker…")
        note_button = QPushButton("Add Note")
        note_button.clicked.connect(self._on_add_note)

        summary_button = QPushButton("Refresh Summary")
        summary_button.clicked.connect(self._on_refresh_summary)

        self.log_view = QTextEdit(readOnly=True)
        self.summary_view = QTextEdit(readOnly=True)

        project_row = QHBoxLayout()
        project_row.addWidget(QLabel("Project:"))
        project_row.addWidget(self.project_edit)
        project_row.addWidget(browse_button)

        port_row = QHBoxLayout()
        port_row.addWidget(QLabel("Port:"))
        port_row.addWidget(self.port_edit)
        port_row.addWidget(self.status_label)

        action_row = QHBoxLayout()
        for button in (start_button, build_button, flash_button, monitor_button):
            action_row.addWidget(button)

        note_row = QHBoxLayout()
        note_row.addWidget(self.note_edit)
        note_row.addWidget(note_button)
        note_row.addWidget(summary_button)

        layout = QVBoxLayout()
        layout.addLayout(project_row)
        layout.addLayout(port_row)
        layout.addLayout(action_row)
        layout.addLayout(note_row)
        layout.addWidget(QLabel("Log:"))
        layout.addWidget(self.log_view)
        layout.addWidget(QLabel("Latest Summary:"))
        layout.addWidget(self.summary_view)

        container = QWidget()
        container.setLayout(layout)
        self.setCentralWidget(container)

    def _append_log(self, text: str) -> None:
        self.log_view.append(text)

    def _on_browse(self) -> None:
        path = QFileDialog.getExistingDirectory(self, "Select ESP-IDF project", self.project_edit.text())
        if path:
            self.project_edit.setText(path)

    def _project_path(self) -> Path:
        return Path(self.project_edit.text())

    def _ensure_session(self) -> SessionHandle | None:
        if self._handle is not None:
            return self._handle
        try:
            self._handle = load_session(self._project_path())
            self.status_label.setText(f"session: {self._handle.meta.session_id}")
            return self._handle
        except SessionNotFoundError as exc:
            self._append_log(f"ERROR: {exc}")
            return None

    def _on_start_session(self) -> None:
        try:
            self._handle = create_session(self._project_path())
            self.status_label.setText(f"session: {self._handle.meta.session_id}")
            self._append_log(f"Started session {self._handle.meta.session_id}")
        except OSError as exc:
            self._append_log(f"ERROR starting session: {exc}")

    def _on_build(self) -> None:
        handle = self._ensure_session()
        if handle is None:
            return
        result = run_build(self._project_path(), SubprocessCommandRunner(), handle.session_dir)
        self._append_log(f"build: {'PASS' if result.success else 'FAIL'}")

    def _on_flash(self) -> None:
        handle = self._ensure_session()
        if handle is None:
            return
        port = self.port_edit.text().strip()
        if not port:
            self._append_log("ERROR: enter a port before flashing")
            return
        result = run_flash(self._project_path(), port, SubprocessCommandRunner(), handle.session_dir)
        self._append_log(f"flash: {'PASS' if result.success else 'FAIL'}")

    def _on_monitor(self) -> None:
        handle = self._ensure_session()
        if handle is None:
            return
        port = self.port_edit.text().strip()
        if not port:
            self._append_log("ERROR: enter a port before monitoring")
            return
        lines = run_monitor(port, 10.0, SubprocessMonitorSource(port=port), handle.session_dir)
        self._append_log(f"monitor: captured {len(lines)} lines")

    def _on_add_note(self) -> None:
        handle = self._ensure_session()
        if handle is None:
            return
        message = self.note_edit.text().strip()
        if not message:
            return
        append_event(handle, Event(kind="note", message=message))
        self._append_log(f"note: {message}")
        self.note_edit.clear()

    def _on_refresh_summary(self) -> None:
        handle = self._ensure_session()
        if handle is None:
            return
        from cockpit32.core.sessions import read_events

        summary = generate_session_summary(handle)
        write_summary(handle.session_dir, summary, read_events(handle))
        self.summary_view.setPlainText(
            (handle.session_dir / "summary.md").read_text(encoding="utf-8")
        )
