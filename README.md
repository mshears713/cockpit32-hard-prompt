# Cockpit 32

A local ESP32 mission-control tool: build, flash, monitor, and capture
timestamped, AI-readable session evidence for the ESP32-S3-BOX-3.

This is a personal engineering tool (see `AGENTS.md` for the full v0
boundary and intent). v0 targets the ESP32-S3-BOX-3 only, assumes an
already-working ESP-IDF shell, and wraps official `idf.py` commands
rather than reimplementing them.

## Install

```
uv sync                 # CLI only
uv sync --extra gui     # + PySide6 GUI shell
uv sync --extra serial  # + pyserial-based port discovery
```

## Quickstart

```
uv run cockpit32 doctor                 # checks idf.py / pyserial visibility
uv run cockpit32 session start --project /path/to/esp-idf-project
uv run cockpit32 build --project /path/to/esp-idf-project
uv run cockpit32 flash --project /path/to/esp-idf-project --port /dev/ttyUSB0
uv run cockpit32 monitor --project /path/to/esp-idf-project --port /dev/ttyUSB0
uv run cockpit32 note --project /path/to/esp-idf-project "screen went black after boot"
uv run cockpit32 summary --project /path/to/esp-idf-project
```

Session evidence (logs, notes, and a generated `summary.json`/
`summary.md`) is written to `<project>/.cockpit32/sessions/<id>/`.

## GUI shell

```
uv run python -m cockpit32.gui.app
```

Same core services as the CLI — no GUI-only business logic.

## Tests

```
uv run pytest                              # everything except GUI needs no extras
QT_QPA_PLATFORM=offscreen uv run pytest tests/gui   # GUI offscreen smoke tests (needs --extra gui)
```

On a bare Linux container, the offscreen Qt platform plugin additionally
needs system libs: `libegl1 libgl1 libxkbcommon0 libfontconfig1
libdbus-1-3`. Not needed on Windows.

## Repo layout

- `src/cockpit32/core/` — domain models, session storage, ESP-IDF
  runner, monitor wrapper, port discovery, doctor, summaries.
- `src/cockpit32/cli.py` — CLI (the primary v0 interface).
- `src/cockpit32/gui/` — PySide6 shell over the same core services.
- `tests/unit`, `tests/contract` (+ `tests/golden`), `tests/acceptance`,
  `tests/gui` — see `AGENTS.md` for the Engineering Method Selection
  behind this split.
- `tests/fakes`, `tests/fixtures` — synthetic `idf.py`/monitor fixtures
  (fake-first; see Fixture Policy in `docs/engineering_plan.md`).
- `docs/validation/` — raw Stage 3 validation evidence.
- `docs/notion-source/` — snapshots of the Notion pages this build was
  planned from.

## Status

This is a Stage 3 **Agent-Validated Build**: implemented and validated
against synthetic fixtures in this agent's environment. Real hardware
validation (a physical ESP32-S3-BOX-3, a real ESP-IDF environment) is
deferred to Stage 4 — see `docs/acceptance_v0.md`.
