# v0 Acceptance Boundary

Cockpit 32 v0 is acceptable for Stage 3 when it provides:

- CLI doctor, session start, build, flash, monitor, note, summarize, and GUI launch commands.
- Core service layer used by both CLI and GUI.
- Project-local session folders with `session.json`, `events.jsonl`, logs, and summaries.
- Fake-first tests for ESP-IDF wrapper behavior.
- Offscreen GUI smoke test.
- Validation Ledger with Verified/Deferred status.

Stage 4 must validate real Windows/PowerShell ESP-IDF visibility, real BOX-3 flashing, real monitor capture, physical operator notes, and GUI usability on Mike's machine.
