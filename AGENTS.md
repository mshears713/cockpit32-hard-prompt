# Cockpit 32 Agent Instructions

Cockpit 32 is a local-first Python + uv + pytest tool for Mike's ESP32-S3-BOX-3 development workflow.

## Product Boundary

- Keep v0 focused on ESP32-S3-BOX-3 only.
- Use official ESP-IDF commands through `idf.py`; do not reimplement ESP-IDF internals.
- Assume Mike launches from an already-working ESP-IDF PowerShell environment for real use.
- Store runtime session output under the firmware project's `.cockpit32/sessions/` folder.
- Do not add live Notion integration in v0.
- Do not commit ordinary runtime logs, local project paths, build folders, secrets, or `.cockpit32/` session folders.

## Architecture Rules

- CLI and GUI must share the same core service layer.
- GUI should remain a thin PySide6 shell; business logic belongs in `src/cockpit32/core/`.
- Use fakes/synthetic fixtures for ESP-IDF, ports, monitor, and hardware behavior in Stage 3.
- Be explicit about Stage 4 deferrals for real hardware/local checks.

## Validation

- Use `uv run pytest` for the Stage 3 validation suite.
- Record validation evidence under `docs/validation/`.
- Never mark a Validation Ledger item Verified without executed evidence.
