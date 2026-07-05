---
source_type: notion_snapshot
source_title: "Cockpit 32 — ESP32 Mission-Control Tool"
source_url: "https://app.notion.com/p/393850a911d381e48a7acced0f4db0bf"
exported_at: "2026-07-05T18:05:00-05:00"
canonical_source: "Notion"
repo_snapshot_purpose: "Implementation-agent readable source snapshot"
---

# Page Properties

```json
{"Cue":"ESP32 cockpit","Name":"Cockpit 32 — ESP32 Mission-Control Tool","Output":"A local ESP32 development cockpit for build, flash, monitor, timestamped logs, session summaries, and human-AI debugging.","Procedure Type":"Tool","Status":"Draft","Trigger":"Use as the Tool record for Cockpit 32 while designing and building the first v0 through the personal software toolbuilding workflow.","date:Last Tested:start":"2026-07-04","url":"https://app.notion.com/p/393850a911d381e48a7acced0f4db0bf"}
```

# Page Content

# Tool Record
## Current Status
Cockpit 32 is a draft personal software tool concept being used as the first test case for the AI-assisted personal software toolbuilding workflow.
Primary workspace during initial definition: Notion.
Expected primary workspace after commissioning: GitHub, with this page retained as strategic context.
## Page Ownership Rule
Each workflow stage should mostly populate its own section.
Later stages may propose edits to earlier sections when new evidence shows the original definition should change, but they should not silently rewrite the tool's intent.
# 1. Project Brief
## Tool Identity
- Working name: Cockpit 32
- Type: Personal local software tool
- Primary user: Mike
- Related project: Operation Homebound / ESP Dev Kit Lab
- Current stage: Product Definition
## Purpose
Cockpit 32 is intended to become a local ESP32 mission-control tool that helps Mike and AI coding agents build, flash, monitor, test, and debug ESP32 firmware with a shared record of what happened.
The deeper purpose is not merely convenience. The goal is to create a reliable human-AI embedded development loop where code changes, build output, flash output, serial logs, user actions, and session summaries can be understood together.
## Background
The idea arose from ESP32-S3-BOX-3 development work where AI coding agents can write and modify firmware, but interactive serial-monitor workflows are awkward for agents and easy to lose as context.
Cockpit 32 should give both Mike and the coding agent a structured view of the hardware test session.
## Primary User
The primary user is Mike.
This is a personal engineering tool, not production software for a general market.
## Core Use Case
Mike asks an AI coding agent to make an ESP32 firmware change, then uses Cockpit 32 to build, flash, monitor, observe the real device, record user actions, and generate evidence for the next AI debugging pass.
## v0 Definition
The first complete usable version should include a basic GUI and local backend capable of supporting the build-flash-monitor-test loop.
v0 should feel like an early but usable cockpit, not only a command-line backend.
## Desired v0 Experience
Mike should be able to open the tool, run build/flash/monitor actions, see logs, record simple user observations, and preserve a session summary that an AI coding agent can inspect.
## Likely v0 Capabilities
- Select or remember an ESP32 project path.
- Run build command.
- Run flash command.
- Monitor serial output for a controlled session.
- Capture build, flash, and serial logs.
- Record simple user events or notes.
- Save a timestamped session folder.
- Generate a readable session summary.
- Provide a basic GUI shell for the workflow.
## Inputs
- ESP32 project directory
- ESP-IDF environment or configured command path
- Serial port / COM port
- Firmware serial output
- User notes or event markers
- Future GitHub repository context
## Outputs
- Build log
- Flash log
- Serial log
- Timeline or session log
- Session summary
- Notes usable by Claude Code or another implementation agent
## Constraints
- Built for Mike first.
- Should support Windows / PowerShell / ESP-IDF workflow.
- Should remain understandable and maintainable.
- Should avoid production SaaS assumptions.
- Should support AI-readable outputs.
- Should not become so ambitious that v0 never ships.
## Non-Goals for v0
- Full production-grade IDE replacement
- Multi-user support
- Cloud dashboard
- Complex authentication
- Perfect GUI polish
- Full mission management system
- Automatic GitHub issue generation
- PlatformIO support unless architecture recommends it as easy and useful
## Success Criteria
v0 succeeds if Mike can use it during a real ESP32 development session and it improves the feedback loop between local hardware testing and AI-assisted code iteration.
A successful v0 should produce enough structured evidence that an AI coding agent can understand what happened without relying only on Mike's memory.
## Risks and Unknowns
- How Cockpit 32 should launch or inherit the ESP-IDF environment.
- How reliable pyserial behavior is on Mike's Windows setup.
- How COM port detection and port locking should work.
- Which GUI framework best fits v0 and long-term development.
- How much GUI is useful before it becomes distracting.
- Whether the tool should eventually scan or record official BSP/example starting points.
## Future Ideas
- BSP/example scanning and recommendation
- Mission-aware session metadata
- Firmware banner validation
- Diagnostics parser
- Timeline visualization
- GitHub issue helper
- Notion or server logging
- Replayable session history
- Claude Code skill integration
## Handoff Notes for Systems Architect
Focus on a complete but restrained v0.
The architecture should include a GUI, but the GUI should be early and practical rather than polished. The system should be designed so Claude Code or another implementation agent can consume session outputs deterministically.
# 2. Architecture and Build Plan
## Stage 2 Status
Stage 2 Engineering Planning is now active and ready to hand off into implementation harness bring-up.
This plan treats the Project Brief above as accepted product intent. Later stages may flag plan deltas, but should not silently rewrite the Project Brief.
## Executive Recommendation
Build Cockpit 32 as a local-first Python tool with a first-class CLI, a shared core service layer, and a basic PySide6 GUI shell before v0 is considered usable.
Cockpit 32 should not become an IDE replacement. Its job is to wrap the official ESP-IDF build, flash, and monitor loop with project selection, session capture, logs, operator notes, summaries, and AI-readable evidence.
For v0, the target board is ESP32-S3-BOX-3 only. The architecture should leave room for board profiles in v1, but v0 should not implement generic multi-board support.
## Locked v0 Decisions
- Repository: `cockpit32`
- v0 board target: ESP32-S3-BOX-3 only
- Future board support: v1 board profiles
- Implementation agent for current run: Codex, because Claude Code credits are temporarily unavailable
- Long-term agent compatibility: keep the repo agent-neutral so Claude Code can later resume without architecture changes
- Language: Python
- Python environment/tooling: `uv`
- Test framework: `pytest`
- CLI: required from the beginning
- GUI: PySide6 shell required before v0 is considered usable
- ESP-IDF environment: v0 assumes Mike can launch from an already-working ESP-IDF PowerShell environment; Cockpit 32 should first provide a `doctor` command that checks whether `idf.py` is visible
- Monitor strategy: use Espressif / ESP-IDF monitor rather than building a custom raw serial monitor first
- COM-port discovery: pySerial later, starting with doctor/import checks
- Session storage: firmware-project-local `.cockpit32/sessions/`
- Notion integration: no live Notion integration in v0; consider read-only Notion pull in v1
## Recommended Architecture
Cockpit 32 should use a layered architecture:
1. Core domain layer
   - Session models
   - Board profile model
   - Command result model
   - Event/timeline model
   - Summary model
2. Tooling adapter layer
   - ESP-IDF command runner
   - ESP-IDF environment doctor
   - Port discovery adapter
   - Monitor wrapper
   - Artifact collector
3. Persistence layer
   - Project-local `.cockpit32/` folder
   - Timestamped session folders
   - Raw logs plus structured JSON/JSONL summaries
4. Presentation layer
   - CLI first
   - PySide6 GUI shell over the same core services
5. Agent harness layer
   - `AGENTS.md`
   - `docs/engineering_plan.md`
   - `docs/acceptance_v0.md`
   - Small milestone prompts for Codex or Claude Code
The GUI must not contain special business logic unavailable to the CLI. Both CLI and GUI should call the same core services.
## Expected Repo Shape
```plain text
cockpit32/
  pyproject.toml
  README.md
  AGENTS.md
  .gitignore
  docs/
    engineering_plan.md
    acceptance_v0.md
  src/
    cockpit32/
      __init__.py
      cli.py
      doctor.py
      models.py
  tests/
```
Later v0 structure may add:
```plain text
src/cockpit32/
  core/
    config.py
    idf_runner.py
    sessions.py
    summaries.py
    ports.py
    monitor.py
  gui/
    app.py
    main_window.py
```
## v0 Product Scope
v0 should eventually support: select or remember one ESP-IDF project path; check ESP-IDF environment visibility; identify or remember serial port; build; flash; start and capture monitor output; record operator notes or event markers; save timestamped session folder; generate readable AI-consumable session summary; provide a basic GUI shell.
## Explicit v0 Non-Goals
Do not implement: full IDE replacement, generic multi-board system, cloud dashboard, authentication, live Notion sync, GitHub issue generation, BSP/example recommendation engine, custom serial monitor replacing ESP-IDF monitor, PlatformIO support, or packaging/distribution polish.
## Implementation Milestones
### Milestone 0 — Harness Bring-Up
Goal: create the repo runway before feature work.
Deliverables: `pyproject.toml`, package scaffold, CLI entry point, `uv run cockpit32 doctor`, doctor report, `AGENTS.md`, `docs/engineering_plan.md`, `docs/acceptance_v0.md`, `.gitignore`, pytest smoke tests, optional CI.
Validation: `uv sync`, `uv run cockpit32 doctor`, `uv run pytest`.
### Milestone 1 — Project Profile and Session Skeleton
Create project-local `.cockpit32/`, store project path/defaults/session metadata, create timestamped session folders, `session.json`, `events.jsonl`, placeholders, latest-session pointer.
### Milestone 2 — Build and Artifact Capture
Run `idf.py build`, capture logs, pass/fail result, and basic build artifacts where available.
### Milestone 3 — Flash
Wrap `idf.py -p <PORT> flash`, capture logs and pass/fail summary.
### Milestone 4 — Monitor Capture
Use ESP-IDF monitor and capture output into the session; summarize notable boot/output/error lines.
### Milestone 5 — Operator Notes and Summary
Add event markers/notes and generate summary JSON/Markdown with final verdict field.
### Milestone 6 — Basic GUI Shell
PySide6 window with project path, port/status, build/flash/monitor buttons, log display, operator note/event control, latest summary view.
### Milestone 7 — v0 Acceptance Session
Use Cockpit 32 in one real Operation Homebound / ESP Dev Kit Lab session and generate fix-before-commissioning list.
## Agent Harness Specification
Current implementation agent: Codex. Preferred long-term implementation agent may return to Claude Code, but the repo must remain agent-neutral.
Agent rules: do not build beyond requested milestone; do not reimplement ESP-IDF internals; use official ESP-IDF commands; keep ESP32-S3-BOX-3 as only v0 board; keep CLI and GUI on same core layer; no live Notion integration in v0; do not commit runtime logs, sessions, local paths, secrets, or generated build folders; prefer small, testable, readable Python.
## Risks and Mitigations
- ESP-IDF environment uncertainty → begin with `cockpit32 doctor`.
- GUI overgrowth → build CLI/core first, then thin PySide6 shell.
- Serial/port confusion → explicit port selection and clear errors first.
- Scope creep into IDE replacement → focus on session capture, notes, summaries, and AI-readable evidence.
- BOX-3 board complexity → preserve BSP-first development.
## Validation Strategy
Validation happens in layers: no-hardware tests, toolchain visibility tests, real-device tests, and AI-readability test.
## Handoff to Implementation
The first Codex prompt should target Milestone 0 only. The first outcome should be boring but solid:
```plain text
uv sync
uv run cockpit32 doctor
uv run pytest
```
If those pass, move to Milestone 1. Do not start build/flash/monitor until the repo harness and session skeleton are clean.
## Stage 2 Addendum — v0.2 (2026-07-05)
This addendum retrofits the approved plan to the v0.2 workflow: autonomous Stage 3 → Agent-Validated Build. The implementation agent builds all agent-provable milestones autonomously on a feature branch with meaningful commits, ending in a single AVB handoff PR. There is no per-milestone demo or approval; Mike's first hands-on touch is Stage 4.
### Engineering Method Selection
- Core domain models → TDD.
- File formats → contract-first + golden files.
- CLI behavior → acceptance-test-first.
- ESP-IDF runner + monitor wrapper → fake-first with synthetic fixtures.
- Port discovery → fake-first.
- GUI shell → timeboxed spike, then test-after with offscreen smoke tests over the tested core layer.
### Fixture Policy for This Build
Stage 3 uses synthetic/sample fixtures for `idf.py` output, flash output, and monitor transcripts. Stage 4 real-hardware runs capture real logs, which get committed as regression fixtures for later patches and v1.
### Validation Ledger (initial)
| Milestone / checkpoint | Agent-Provable | Deferred to Stage 4 |
|---|---|---|
| M0 — Harness bring-up | uv sync, `cockpit32 doctor`, pytest smoke | — |
| M1 — Session skeleton | Session start without hardware; deterministic AI-readable files | — |
| M2 — Build capture | Runner logic, log capture, pass/fail summarization against fake `idf.py` fixtures | Real `idf.py build` from an ESP-IDF PowerShell environment |
| M3 — Flash | Flash wrapper logic and error-path handling against fake runner | Real flash of the ESP32-S3-BOX-3 |
| M4 — Monitor capture | Monitor log parsing and summarization against synthetic transcripts | Real ESP-IDF monitor capture from the BOX-3 |
| M5 — Notes & summary | Event markers, summary JSON/Markdown, verdict field | Marking a real physical event during a live session |
| M6 — GUI shell | Offscreen instantiation smoke; GUI calls same core services as CLI | Visual/interaction check on Mike's machine |
| M7 — v0 acceptance session | — | Entirely deferred — M7 effectively merges into Stage 4 commissioning |
### Evidence Convention
Raw evidence lives in the repo under `docs/validation/`. Verdict tables and the AVB Report live on this Tool page.
# 3. Commissioning Summary
*To be populated after the first local build/debug/use cycle.*
# 4. Major Engineering Decisions
Locked decisions include Python, uv, ESP32-S3-BOX-3-only v0, basic PySide6 GUI, existing ESP-IDF setup assumption, `cockpit32 doctor`, `.cockpit32/sessions/`, no live Notion integration, wrapped ESP-IDF monitor, current Codex implementation, and agent-neutral repo.
# 5. Current Development
*To become active after commissioning, when GitHub becomes the primary implementation workspace.*
# 6. References
Existing concept notes and ESP32 learning records should be linked or referenced during later cleanup.
