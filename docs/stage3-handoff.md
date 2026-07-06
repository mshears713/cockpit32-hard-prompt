# Stage 3 Handoff

## What was built

Cockpit 32 now has a Python package, uv project config, CLI, core services, PySide6 GUI shell, tests, and validation docs.

## Local Stage 4 start

1. Pull the AVB branch.
2. Run `uv sync`.
3. Open an ESP-IDF PowerShell where `idf.py` works.
4. Run `uv run cockpit32 doctor`.
5. Start a session for the ESP-IDF project and walk build, flash, monitor, note, summarize.

## Deferred commissioning focus

- ESP-IDF visibility in Mike's real shell.
- COM-port discovery and chosen port behavior.
- Real ESP32-S3-BOX-3 flash and monitor behavior.
- GUI usability on Mike's Windows desktop.
