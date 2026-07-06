from cockpit32.cli import main


def test_cli_start_session_and_note_and_summarize(tmp_path, capsys):
    assert main(["start-session", "--project", str(tmp_path), "--port", "COM7"]) == 0
    session_id = (tmp_path / ".cockpit32" / "latest-session.txt").read_text().strip()
    assert main(["note", "--project", str(tmp_path), "--session-id", session_id, "Boot looked normal"]) == 0
    assert main(["summarize", "--project", str(tmp_path), "--session-id", session_id]) == 0
    assert "Boot looked normal" in capsys.readouterr().out


def test_cli_doctor_warns_when_idf_missing(capsys):
    assert main(["doctor", "--idf-command", "definitely-missing-idf-command"]) == 1
    assert "idf.py visible" in capsys.readouterr().out
