# Cockpit 32 Validation Ledger

| Checkpoint | Stage 3 status | Evidence | Stage 4 step if deferred |
|---|---|---|---|
| M0 harness bring-up | Verified | `docs/validation/stage3-validation.md`; `uv sync`, `uv run cockpit32 doctor --idf-command definitely-missing-idf-command`, `PYTHONPATH=src pytest` executed | — |
| M1 session skeleton | Verified | `tests/test_sessions.py`, `tests/test_cli.py`, `PYTHONPATH=src pytest` | — |
| M2 build capture wrapper | Verified for wrapper logic with fake `idf.py`, cross-platform (Linux + Windows) | `tests/test_idf_runner.py`, `docs/validation/stage3-validation.md` (Windows re-verification) | Run `uv run cockpit32 build` in Mike's ESP-IDF PowerShell against a real project. |
| M2 real ESP-IDF build | Deferred | Agent environment is not Mike's ESP-IDF PowerShell | Run real `idf.py build` through Cockpit 32 and attach the generated `build.log`. |
| M3 flash wrapper | Verified for wrapper/error handling with fake `idf.py`, cross-platform (Linux + Windows) | `tests/test_idf_runner.py`, `docs/validation/stage3-validation.md` (Windows re-verification) | Run `uv run cockpit32 flash --port <BOX3_PORT>` with the ESP32-S3-BOX-3 connected. |
| M3 real BOX-3 flash | Deferred | Requires Mike's hardware and COM port | Confirm flash success and commit sanitized real fixture/log if useful. |
| M4 monitor capture wrapper/summarization | Verified with synthetic transcript/log behavior | `tests/test_summaries.py`, `PYTHONPATH=src pytest` | Run real ESP-IDF monitor through Cockpit 32 and inspect captured `monitor.log`. |
| M4 real monitor capture | Deferred | Requires BOX-3 serial output | Capture boot transcript and commit a sanitized regression fixture. |
| M5 notes and summary | Verified | `tests/test_summaries.py`, `tests/test_cli.py`, `PYTHONPATH=src pytest` | During a live session, add a physical observation note and confirm it appears in `summary.md`. |
| M6 GUI shell | Verified for offscreen instantiation and shared core import path | `tests/test_gui_smoke.py`, `PYTHONPATH=src pytest` | Launch `uv run cockpit32 gui` on Mike's Windows machine and visually verify controls/workflow. |
| M7 v0 acceptance session | Deferred | Stage 3 cannot commission | Execute the full cold-start commissioning procedure and classify defects. |
