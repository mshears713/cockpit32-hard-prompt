# Cockpit 32 — Validation Ledger (Stage 3 final state)

Every item is **Verified** (executed, with evidence linked below) or
**Deferred** (with a written Stage 4 step). None are blank. This is the
repo-local copy; the same table is posted to the Tool page's Build Log
(AVB Report) in Notion.

| # | Item | State | Evidence / Stage 4 step |
|---|---|---|---|
| M0.1 | `uv sync` completes, package importable | Verified | `docs/validation/m0_harness_bringup.txt` |
| M0.2 | `cockpit32 doctor` reports env visibility, correct exit code | Verified | `docs/validation/m0_harness_bringup.txt` — exit=1 with idf.py absent, as expected in this agent env |
| M0.3 | Test-architecture skeleton (unit/contract/acceptance/gui/fakes/fixtures/golden) stood up | Verified | repo tree under `tests/`; `pyproject.toml` pytest config |
| M0.4 | Optional CI stub | Verified (stub exists) / Deferred (green run) | `.github/workflows/test.yml` created; **Stage 4 step:** confirm it runs green on GitHub after this PR is opened, since this agent cannot observe Actions runs |
| M1.1 | Domain models round-trip (TDD) | Verified | `docs/validation/m1_session_skeleton.txt` (9 model tests) |
| M1.2 | Session can be created/loaded without hardware | Verified | `docs/validation/m1_session_skeleton.txt` |
| M1.3 | `session.json`/`events.jsonl` match golden-file contract | Verified | `tests/contract/test_session_contract.py`, `tests/golden/session.json` |
| M1.4 | Latest-session pointer correctness | Verified | `test_second_session_updates_latest_pointer` |
| M2.1 | Build runner captures logs, reports pass/fail (fake-first) | Verified | `docs/validation/m2_build_capture.txt` |
| M2.2 | Real `idf.py build` from an ESP-IDF PowerShell environment | Deferred | **Stage 4 step:** run `cockpit32 build` in a real ESP-IDF shell against a real BOX-3 project; confirm build.log/build.json match real output shape |
| M3.1 | Flash wrapper + failure-guidance mapping (fake-first) | Verified | `docs/validation/m3_flash.txt` |
| M3.2 | Real flash of a physical ESP32-S3-BOX-3 | Deferred | **Stage 4 step:** flash a real BOX-3; confirm the failure-guidance strings are actually useful against real failure modes (port busy, no response) |
| M4.1 | Monitor capture + notable-line classification (fake-first) | Verified | `docs/validation/m4_monitor_capture.txt` |
| M4.2 | Real `idf.py monitor` capture, real timing/pacing | Deferred | **Stage 4 step:** run `cockpit32 monitor` against a real BOX-3; note that `TranscriptMonitorSource` ignores real-time pacing (fidelity limit) — confirm `SubprocessMonitorSource`'s duration-bounded capture behaves the same way in practice |
| M5.1 | Event markers recorded and rendered | Verified | `docs/validation/m5_notes_summary.txt` |
| M5.2 | `summary.json`/`summary.md` match golden files; verdict logic (all branches) | Verified | `tests/unit/test_summaries.py`, `tests/contract/test_summary_contract.py` |
| M5.3 | Operator verdict override | Verified | `test_operator_override_wins_over_computed_verdict`, `test_summary_verdict_override` |
| M5.4 | AI-readability test (Validation Strategy layer 4) | Verified | `docs/validation/ai_readability_test.md` — found and fixed a real defect (`monitor: pass` wording, unlabeled severity) |
| M5.5 | Mike marking a real physical event during a live session | Deferred | **Stage 4 step:** during a real BOX-3 session, use `cockpit32 note` to mark an actual observation (touch, reset, screen change, no response) and confirm the summary reads true to what happened |
| M6.1 | GUI shell instantiates, wires controls to core services (offscreen) | Verified | `docs/validation/m6_gui_shell.txt` |
| M6.2 | GUI drives the same start→note→summary flow as the CLI | Verified | `test_add_note_and_refresh_summary_uses_core_services` |
| M6.3 | Visual/interaction check on Mike's machine | Deferred | **Stage 4 step:** run `python -m cockpit32.gui.app` on Mike's Windows machine; confirm layout, readability, and that no offscreen-only assumption broke it |
| M7 | v0 acceptance session (real BOX-3 build/flash/monitor/notes/summary) | Deferred | **Stage 4 step:** this is the commissioning session itself — see `docs/acceptance_v0.md` |

## Summary

- **Verified:** 17
- **Deferred:** 7 (all hardware/local/real-environment items, as scoped)
- **Blank:** 0
