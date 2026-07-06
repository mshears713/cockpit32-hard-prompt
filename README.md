# Cockpit 32

Cockpit 32 is a local ESP32-S3-BOX-3 mission-control tool for Mike's ESP-IDF build / flash / monitor workflow.

Stage 3 produces an **Agent-Validated Build**. Real Windows, ESP-IDF, COM-port, and ESP32-S3-BOX-3 hardware commissioning is deferred to Stage 4.

## Install

```powershell
git pull
uv sync
```

## First commands

Run from an ESP-IDF PowerShell where `idf.py` already works:

```powershell
uv run cockpit32 doctor
uv run cockpit32 start-session --project C:\path\to\esp-idf-project --port COM7
uv run cockpit32 build --project C:\path\to\esp-idf-project --session-id <SESSION_ID>
uv run cockpit32 flash --project C:\path\to\esp-idf-project --session-id <SESSION_ID> --port COM7
uv run cockpit32 monitor --project C:\path\to\esp-idf-project --session-id <SESSION_ID> --port COM7 --seconds 30
uv run cockpit32 note --project C:\path\to\esp-idf-project --session-id <SESSION_ID> "Observed device boot banner"
uv run cockpit32 summarize --project C:\path\to\esp-idf-project --session-id <SESSION_ID>
uv run cockpit32 gui
```

Runtime sessions are stored under the firmware project at `.cockpit32/sessions/` and are ignored by this repo by default.
