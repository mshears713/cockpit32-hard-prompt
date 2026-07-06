# Stage 3 Validation Evidence

Using CPython 3.14.4 interpreter at: /root/.pyenv/versions/3.14.4/bin/python3
Creating virtual environment at: .venv
Resolved 1 package in 11ms
   Building cockpit32 @ file:///workspace/cockpit32-hard-prompt
      Built cockpit32 @ file:///workspace/cockpit32-hard-prompt
Prepared 1 package in 312ms
Installed 1 package in 8ms
 + cockpit32==0.1.0 (from file:///workspace/cockpit32-hard-prompt)
Doctor found warnings; Stage 4 should run this inside Mike's ESP-IDF PowerShell.
PASS python: 3.14.4
WARN idf.py visible: definitely-missing-idf-command
WARN pyserial import: serial
WARN PySide6 import: PySide6
============================= test session starts ==============================
platform linux -- Python 3.14.4, pytest-9.0.3, pluggy-1.6.0
rootdir: /workspace/cockpit32-hard-prompt
configfile: pyproject.toml
testpaths: tests
collected 8 items

tests/test_cli.py ..                                                     [ 25%]
tests/test_gui_smoke.py .                                                [ 37%]
tests/test_idf_runner.py ..                                              [ 62%]
tests/test_sessions.py .                                                 [ 75%]
tests/test_summaries.py ..                                               [100%]

============================== 8 passed in 0.21s ===============================

## Windows re-verification (Claude Code, 2026-07-05)

Original evidence above was captured on Linux. Re-running on Mike's actual
target platform (Windows) surfaced a real gap: `IdfRunner.run` passed the
fake `idf.py` fixture straight to `subprocess.run`, which works on Linux via
the shebang line but fails on Windows with `OSError: [WinError 193] %1 is
not a valid Win32 application` because Windows will not execute a `.py` file
directly without going through the interpreter.

Fix: `IdfRunner.run` now prepends `sys.executable` when `idf_command` ends
in `.py`. This does not change architecture or product intent (code-level
deviation per the Implementation procedure) and only affects how a
`.py`-suffixed command is invoked; real `idf.py` on Mike's machine is a
shell-exposed command (not a raw `.py` path) via the ESP-IDF export script,
so this is a robustness fix for the wrapper, not a change to real-world
behavior.

```
uv sync
uv run cockpit32 doctor
uv run pytest -v
```

```
Using CPython 3.13.9 interpreter at: C:\Users\PC\AppData\Local\Programs\Python\Python313\python.exe
Creating virtual environment at: .venv
Resolved 1 package in 26ms
Installed 1 package in 39ms

Doctor found warnings; Stage 4 should run this inside Mike's ESP-IDF PowerShell.
PASS python: 3.13.9
WARN idf.py visible: idf.py
WARN pyserial import: serial
WARN PySide6 import: PySide6

platform win32 -- Python 3.13.9, pytest-9.0.2, pluggy-1.6.0
collected 8 items

tests/test_cli.py::test_cli_start_session_and_note_and_summarize PASSED  [ 12%]
tests/test_cli.py::test_cli_doctor_warns_when_idf_missing PASSED         [ 25%]
tests/test_gui_smoke.py::test_gui_window_instantiates_or_fallback_exists PASSED [ 37%]
tests/test_idf_runner.py::test_build_captures_fake_idf_output PASSED     [ 50%]
tests/test_idf_runner.py::test_flash_failure_is_captured PASSED          [ 62%]
tests/test_sessions.py::test_start_session_creates_contract_files PASSED [ 75%]
tests/test_summaries.py::test_notable_lines_extracts_monitor_signals PASSED [ 87%]
tests/test_summaries.py::test_generate_summary_writes_json_and_markdown PASSED [100%]

8 passed in 0.22s
```

WARN lines for `idf.py`, `pyserial`, and `PySide6` are expected in this
agent environment (no ESP-IDF install, no optional deps installed) and are
already accounted for as Stage 4 deferrals.
