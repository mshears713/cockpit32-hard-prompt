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
