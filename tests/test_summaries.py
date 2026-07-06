from cockpit32.core.sessions import SessionStore
from cockpit32.core.summaries import generate_summary, notable_lines


def test_notable_lines_extracts_monitor_signals():
    text = "boot ok\nE (123) app: error opening sensor\nESP-ROM:esp32s3\n"
    assert notable_lines(text) == ["E (123) app: error opening sensor", "ESP-ROM:esp32s3"]


def test_generate_summary_writes_json_and_markdown(tmp_path):
    store = SessionStore(tmp_path)
    meta = store.start(port="COM7")
    store.add_event(meta.session_id, "note", "Pressed reset after flash")
    store.add_event(meta.session_id, "build_completed", "Build completed", {"status": "passed"})
    log = store.session_dir(meta.session_id) / "logs" / "monitor.log"
    log.write_text("ESP-ROM:esp32s3\napp_main started\n", encoding="utf-8")
    summary = generate_summary(store.session_dir(meta.session_id))
    assert summary.notes == ["Pressed reset after flash"]
    assert summary.commands["build"] == "passed"
    assert "ESP-ROM:esp32s3" in summary.notable_lines
    assert (store.session_dir(meta.session_id) / "summary.json").exists()
    assert (store.session_dir(meta.session_id) / "summary.md").exists()
