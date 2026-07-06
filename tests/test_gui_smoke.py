from cockpit32.gui.main_window import MainWindow


def test_gui_window_instantiates_or_fallback_exists():
    window = MainWindow()
    assert window.windowTitle() == "Cockpit 32"
    assert window.current_session_id is None
