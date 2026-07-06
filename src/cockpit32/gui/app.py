from __future__ import annotations

import sys

from cockpit32.gui.main_window import QApplication, MainWindow


def run() -> int:
    if QApplication is None:
        raise RuntimeError("PySide6 is not installed. Install PySide6 for the GUI shell before Stage 4 GUI commissioning.")
    app = QApplication.instance() or QApplication(sys.argv)
    window = MainWindow()
    window.show()
    return app.exec()
