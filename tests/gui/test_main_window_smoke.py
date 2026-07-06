"""Offscreen smoke tests for the GUI shell.

Engineering Method Selection: test-after + smoke — the window contains
no business logic to prove; we only confirm it instantiates, wires its
controls, and drives the same core services the CLI's acceptance tests
already cover. Runs headless via the Qt "offscreen" platform plugin, so
no real display is required (or available) in the agent's environment.
"""

import os

os.environ.setdefault("QT_QPA_PLATFORM", "offscreen")

import pytest

pytest.importorskip("PySide6")

from PySide6.QtWidgets import QApplication

from cockpit32.gui.main_window import MainWindow


@pytest.fixture(scope="module")
def qapp():
    app = QApplication.instance() or QApplication([])
    yield app


def test_main_window_instantiates_offscreen(qapp):
    window = MainWindow()
    assert window.windowTitle() == "Cockpit 32"
    assert window.status_label.text() == "No session"


def test_start_session_button_creates_session(qapp, tmp_path):
    window = MainWindow()
    window.project_edit.setText(str(tmp_path))

    window._on_start_session()

    assert window._handle is not None
    assert (tmp_path / ".cockpit32" / "sessions" / window._handle.meta.session_id).exists()
    assert "Started session" in window.log_view.toPlainText()


def test_add_note_without_session_reports_error_not_crash(qapp, tmp_path):
    window = MainWindow()
    window.project_edit.setText(str(tmp_path))
    window.note_edit.setText("no session yet")

    window._on_add_note()  # must not raise

    assert "ERROR" in window.log_view.toPlainText()


def test_add_note_and_refresh_summary_uses_core_services(qapp, tmp_path):
    window = MainWindow()
    window.project_edit.setText(str(tmp_path))
    window._on_start_session()

    window.note_edit.setText("touched the screen")
    window._on_add_note()
    window._on_refresh_summary()

    assert (window._handle.session_dir / "summary.json").exists()
    assert "touched the screen" in window.summary_view.toPlainText()


def test_flash_without_port_reports_error_not_crash(qapp, tmp_path):
    window = MainWindow()
    window.project_edit.setText(str(tmp_path))
    window._on_start_session()

    window._on_flash()  # no port entered — must not raise

    assert "enter a port" in window.log_view.toPlainText()
