from __future__ import annotations

from pathlib import Path

from cockpit32.core.doctor import run_doctor
from cockpit32.core.sessions import SessionStore

try:
    from PySide6.QtWidgets import QApplication, QHBoxLayout, QLabel, QLineEdit, QMainWindow, QPushButton, QTextEdit, QVBoxLayout, QWidget
except ImportError:  # Stage 3 fallback when PySide6 cannot be installed in the agent environment.
    QApplication = None
    class MainWindow:  # type: ignore[no-redef]
        def __init__(self) -> None:
            self.current_session_id = None
        def windowTitle(self) -> str:
            return "Cockpit 32"
else:
    class MainWindow(QMainWindow):
        """Thin GUI shell over CLI/core services; no ESP-IDF business logic lives here."""

        def __init__(self) -> None:
            super().__init__()
            self.setWindowTitle("Cockpit 32")
            self.project = QLineEdit(str(Path.cwd()))
            self.port = QLineEdit("")
            self.output = QTextEdit()
            self.output.setReadOnly(True)
            doctor_btn = QPushButton("Doctor")
            session_btn = QPushButton("Start Session")
            note_btn = QPushButton("Add Note")
            self.note = QLineEdit("")
            doctor_btn.clicked.connect(self.run_doctor_clicked)
            session_btn.clicked.connect(self.start_session_clicked)
            note_btn.clicked.connect(self.add_note_clicked)
            layout = QVBoxLayout()
            layout.addWidget(QLabel("ESP-IDF Project Path"))
            layout.addWidget(self.project)
            layout.addWidget(QLabel("Serial Port"))
            layout.addWidget(self.port)
            row = QHBoxLayout()
            row.addWidget(doctor_btn)
            row.addWidget(session_btn)
            layout.addLayout(row)
            layout.addWidget(QLabel("Operator Note"))
            layout.addWidget(self.note)
            layout.addWidget(note_btn)
            layout.addWidget(self.output)
            root = QWidget()
            root.setLayout(layout)
            self.setCentralWidget(root)
            self.current_session_id: str | None = None

        def append(self, text: str) -> None:
            self.output.append(text)

        def run_doctor_clicked(self) -> None:
            for check in run_doctor().checks:
                self.append(f"{'PASS' if check.ok else 'WARN'} {check.name}: {check.detail}")

        def start_session_clicked(self) -> None:
            metadata = SessionStore(Path(self.project.text())).start(port=self.port.text() or None)
            self.current_session_id = metadata.session_id
            self.append(f"Started session {metadata.session_id}")

        def add_note_clicked(self) -> None:
            if not self.current_session_id:
                self.append("Start a session before adding a note.")
                return
            event = SessionStore(Path(self.project.text())).add_event(self.current_session_id, "note", self.note.text())
            self.append(f"Note recorded: {event.message}")
