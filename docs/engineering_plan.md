# Cockpit 32 — Engineering Plan (derived from the Tool page)

Source of truth: the Cockpit 32 Tool page in Notion, section "2.
Architecture and Build Plan" plus the "Stage 2 Addendum — v0.2" that
retrofits it to the autonomous Stage 3 workflow. This file is a
repo-local copy for agent convenience; if it drifts from the Tool page,
the Tool page wins.

## Executive Recommendation

Local-first Python tool: first-class CLI, a shared core service layer,
and a basic PySide6 GUI shell before v0 is considered usable. Wraps the
official ESP-IDF build/flash/monitor loop — it does not reimplement
ESP-IDF internals. v0 board target: **ESP32-S3-BOX-3 only**.

## Locked v0 Decisions

- Repository: `cockpit32`
- v0 board target: ESP32-S3-BOX-3 only; v1 may add board profiles
- Language: Python, managed with `uv`
- Test framework: `pytest`
- CLI required from the start; PySide6 GUI shell required before v0 is
  "usable," but contains no business logic of its own
- ESP-IDF environment: v0 assumes an already-working ESP-IDF shell;
  `cockpit32 doctor` checks whether `idf.py` is visible
- Monitor strategy: wrap/capture ESP-IDF monitor, don't replace it
- COM-port discovery: pySerial-based, fake-first in Stage 3
- Session storage: project-local `.cockpit32/sessions/`
- No live Notion integration in v0

## Recommended Architecture

1. **Core domain layer** — session/event/board-profile/command-result/
   summary models (`cockpit32.core.models`).
2. **Tooling adapter layer** — ESP-IDF command runner (`idf_runner.py`),
   environment doctor (`doctor.py`), port discovery (`ports.py`),
   monitor wrapper (`monitor.py`).
3. **Persistence layer** — project-local `.cockpit32/sessions/<id>/`
   with `session.json`, `events.jsonl`, per-phase logs, and
   `summary.json`/`summary.md`.
4. **Presentation layer** — CLI (`cli.py`) first; PySide6 GUI shell
   (`gui/main_window.py`) over the same core services.

## Implementation Milestones (Stage 3, this build)

| Milestone | Objective |
|---|---|
| M0 | Harness bring-up: repo, env, AGENTS.md/CLAUDE.md, test-architecture skeleton |
| M1 | Session skeleton: domain models, `.cockpit32/sessions/`, `session.json`/`events.jsonl` |
| M2 | Build capture: `idf.py build` wrapper against fake runner + synthetic fixtures |
| M3 | Flash: `idf.py -p <PORT> flash` wrapper, failure-path guidance |
| M4 | Monitor capture: timed capture, notable-line classification against synthetic transcripts |
| M5 | Operator notes + summary: event markers, `summary.json`/`.md`, verdict field |
| M6 | GUI shell: PySide6 window over the same core services, offscreen smoke tests |
| M7 | v0 acceptance session — real BOX-3 hardware — **entirely deferred to Stage 4** |

## Engineering Method Selection

See `AGENTS.md` for the per-subsystem table (TDD / contract-first /
acceptance-test-first / fake-first / test-after+smoke) — unchanged from
the Tool page's Stage 2 Addendum.

## Test Architecture

- **Taxonomy:** unit (`tests/unit`), contract+golden (`tests/contract`,
  `tests/golden`), acceptance (`tests/acceptance`), GUI smoke
  (`tests/gui`). No integration-with-real-hardware tests in Stage 3.
- **Test doubles:** `tests/fakes/fake_runner.py` (`FakeCommandRunner`);
  `TranscriptMonitorSource` for monitor capture. Backed by synthetic
  fixtures in `tests/fixtures/`.
- **Fixture policy:** synthetic/sample fixtures stand in for real
  `idf.py` and monitor output. Stage 4 real captures become regression
  fixtures for later patches/v1.
- **Evidence:** raw command output lives in `docs/validation/`; verdict
  tables and the AVB Report live in the Tool page's Build Log section.
- **CI:** not wired up in this Stage 3 run (see Known Limitations in the
  AVB Report) — `uv run pytest` is the local validation command.

## Risks and Mitigations (carried from the Tool page)

- **ESP-IDF environment uncertainty** — mitigated by `cockpit32 doctor`.
- **GUI overgrowth** — mitigated by building CLI/core first, GUI last,
  GUI containing no business logic.
- **Serial/port confusion** — mitigated by explicit port selection and
  clear error messages; smarter discovery is a later concern.
- **Scope creep into IDE replacement** — mitigated by staying focused on
  session capture, notes, summaries, AI-readable evidence.
- **BOX-3 board complexity** — deferred entirely to Stage 4 real
  hardware; not addressed by Stage 3 fakes.
