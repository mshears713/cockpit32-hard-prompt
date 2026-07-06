from cockpit32.core.sessions import SessionStore


def test_start_session_creates_contract_files(tmp_path):
    metadata = SessionStore(tmp_path).start(port="COM7")
    session_dir = tmp_path / ".cockpit32" / "sessions" / metadata.session_id
    assert (session_dir / "session.json").exists()
    assert (session_dir / "events.jsonl").exists()
    assert (session_dir / "logs").is_dir()
    assert (tmp_path / ".cockpit32" / "latest-session.txt").read_text().strip() == metadata.session_id
    assert metadata.board == "esp32-s3-box-3"
