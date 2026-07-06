# AGENTS.md — Cockpit 32

Generated at Stage 3 harness bring-up from the Cockpit 32 Tool page
(Notion). This file is **derived and disposable** — Notion is the
source of truth for intent; if this file disagrees with the Tool page,
the Tool page wins. Refresh at milestone boundaries or when the plan
changes.

## Purpose

Cockpit 32 is a local ESP32 mission-control tool. It wraps the official
ESP-IDF build/flash/monitor loop for the **ESP32-S3-BOX-3** with project
selection, timestamped session capture, operator notes, and an
AI-readable summary — so Mike and a coding agent can debug a hardware
session together without relying only on Mike's memory. It is not an
IDE replacement.

## v0 Boundary

**In scope (v0):**
- `cockpit32 doctor` — checks whether `idf.py` is visible; does not
  install or configure ESP-IDF.
- Project-local session storage at `.cockpit32/sessions/<id>/` inside
  the ESP-IDF project being debugged.
- Build/flash wrappers over `idf.py build` / `idf.py -p <PORT> flash`
  with captured logs and pass/fail summaries.
- A timed `idf.py monitor` capture with notable-line classification
  (errors, warnings, boot markers).
- Operator notes/event markers and a generated `summary.json` +
  `summary.md` with an explicit verdict
  (success/partial/failed/blocked/unknown).
- A CLI first; a thin PySide6 GUI shell over the *same* core services
  (no GUI-only business logic).

**Out of scope (v0 non-goals):** full IDE replacement, multi-board
support (BOX-3 only; board profiles are v1), cloud dashboard, auth,
live Notion sync, GitHub issue generation, BSP/example recommendation
engine, a custom serial monitor (wrap ESP-IDF monitor, don't replace
it), PlatformIO support, packaging/distribution polish.

## Architecture Summary

Layered: **core domain models** (session/event/board/command-result/
summary) → **tooling adapters** (`idf_runner`, `monitor`, `ports`,
`doctor`) → **persistence** (project-local `.cockpit32/sessions/`) →
**presentation** (CLI via `click`, then a PySide6 GUI shell calling the
same core functions). No business logic may live only in the GUI.

## Milestone List (Stage 3 — this build)

M0 harness bring-up · M1 session skeleton · M2 build capture · M3 flash
· M4 monitor capture · M5 operator notes + summary · M6 GUI shell · M7
v0 acceptance session (real hardware — entirely deferred to Stage 4).

Milestones are the implementation agent's organizational units, not
Mike-approval gates (Stage 3 v0.2 autonomous posture).

## Engineering Method Selection (per subsystem)

- Core domain models → TDD.
- File formats (`session.json`, `events.jsonl`, `summary.json/.md`) →
  contract-first + golden files.
- CLI behavior → acceptance-test-first.
- ESP-IDF runner + monitor wrapper → fake-first, synthetic fixtures.
- Port discovery → fake-first.
- GUI shell → timeboxed spike, then test-after with offscreen smoke
  tests over the tested core layer.

## Validation Ledger — see `docs/validation/` for raw evidence

Every item is **Verified** (executed, with evidence) or **Deferred**
(with a written Stage 4 step) — never blank, never bluffed. The
authoritative ledger table lives in the Build Log section of the Tool
page (AVB Report); raw command output/logs live under
`docs/validation/`.

## Stop-and-Flag Rules

Do not re-architect. Stop and escalate only for: product-scope
ambiguity the plan can't resolve, missing credentials/access,
repo/tool access failure, an architecture conflict discovered mid-build,
a contradiction within the approved plan, or a decision that would
materially change Stage 1 intent or the Stage 2 plan. Everything else —
including code-level and mechanical plan-level deviations, and
provisional deltas that preserve approved architecture/intent — proceed
and log in the Build Log; Mike adjudicates provisional deltas at
Stage 4.

## Repo Conventions

- Python + `uv`. `uv sync` (add `--extra gui` for the PySide6 GUI
  extra). `uv run pytest`.
- `src/` layout: `src/cockpit32/core/` (domain + adapters),
  `src/cockpit32/gui/` (PySide6 shell), `src/cockpit32/cli.py`.
- Tests mirror the Test Architecture taxonomy: `tests/unit`,
  `tests/contract` (+ `tests/golden` fixtures), `tests/acceptance`,
  `tests/gui`, `tests/fakes` (fake runners/sources), `tests/fixtures`
  (synthetic idf.py/monitor output).
- GUI offscreen tests require `QT_QPA_PLATFORM=offscreen` and, on a
  bare Linux container, the system libs `libegl1 libgl1 libxkbcommon0
  libfontconfig1 libdbus-1-3` (not needed on Mike's Windows setup).
