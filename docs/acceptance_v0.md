# Cockpit 32 — v0 Acceptance Criteria

Derived from the Project Brief's Success Criteria and the Engineering
Plan's Validation Ledger. See `docs/validation/` for raw evidence and
the Tool page's Build Log / AVB Report for the authoritative verdict
table.

## From the Project Brief

> v0 succeeds if Mike can use it during a real ESP32 development session
> and it improves the feedback loop between local hardware testing and
> AI-assisted code iteration. A successful v0 should produce enough
> structured evidence that an AI coding agent can understand what
> happened without relying only on Mike's memory.

This is inherently a Stage 4 (real hardware, real Mike) criterion. What
Stage 3 can prove is that every mechanism the criterion depends on
exists, is correct against realistic fixtures, and produces the
promised AI-readable evidence.

## Agent-Provable in Stage 3 (see docs/validation/ for commands + output)

- [x] `uv sync` completes; `cockpit32` imports and runs.
- [x] `cockpit32 doctor` reports Python/package/idf.py/pyserial status
      with a clear message and a non-zero exit code when `idf.py` is
      absent (this environment's real, expected condition).
- [x] A session can be created without hardware; `session.json` and
      `events.jsonl` match the golden-file contract.
- [x] Build/flash wrappers, run against synthetic `idf.py` success and
      failure fixtures, capture logs and report pass/fail correctly;
      flash failures map to actionable next-step guidance.
- [x] Monitor capture, run against synthetic transcripts, classifies
      boot/warning/error lines correctly (normal boot, Guru Meditation
      crash, brownout).
- [x] Operator notes/markers are recorded and appear in
      `events.jsonl` and in the rendered summary.
- [x] `summary.json` / `summary.md` are generated with a verdict field
      populated by explicit logic (or an operator override), matching
      golden files.
- [x] The GUI shell instantiates offscreen, wires its controls to the
      exact same core functions as the CLI, and drives a full
      start-session → note → refresh-summary flow without hardware.

## Deferred to Stage 4 (real hardware / Mike's machine)

- [ ] Real `idf.py build` from an ESP-IDF PowerShell environment.
- [ ] Real flash of a physical ESP32-S3-BOX-3; real-world usefulness of
      the failure-guidance strings.
- [ ] Real `idf.py monitor` capture from the BOX-3, including real
      timing/pacing behavior (Stage 3's `TranscriptMonitorSource`
      ignores real-time pacing — a noted fidelity limit).
- [ ] Mike marking a real physical event (touch, reset, screen change,
      no response) during a live session.
- [ ] Visual/interaction check of the GUI shell on Mike's machine.
- [ ] The M7 v0 acceptance session itself — a real BOX-3 build/flash/
      monitor cycle with captured logs, notes, and a summary Mike and an
      AI agent both find useful. This criterion effectively merges M7
      into Stage 4 commissioning.
