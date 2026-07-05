---
source_type: notion_snapshot
source_title: "Engineering Method Selection & Test Architecture Guide"
source_url: "https://app.notion.com/p/394850a911d3819997d0c00569db089b"
exported_at: "2026-07-05T18:05:00-05:00"
canonical_source: "Notion"
repo_snapshot_purpose: "Implementation-agent readable source snapshot"
---

# Page Properties

```json
{"Cue":"Pick engineering method and test plan","Knowledge Type":"Reference","Name":"Engineering Method Selection & Test Architecture Guide","Standing":"Candidate","Status":"Tentative","date:Last Reviewed:start":"2026-07-05","url":"https://app.notion.com/p/394850a911d3819997d0c00569db089b"}
```

# Page Content

# What This Is

The reusable decision guide Stage 2 (Engineering Planning) uses to select **engineering methods per subsystem** and to specify the **Test Architecture** the implementation agent executes against in Stage 3. The Engineering Plan records the *choices*; this page holds the *reasoning framework* so each plan does not rebuild it from scratch.

Methods are selected per subsystem, never one-method-per-tool.

# Decision Axes

- **Specifiability** — can correct behavior be written down up front?
- **Design uncertainty** — how unknown is the approach, library, or framework?
- **Environmental reach** — can the implementation agent's environment execute it at all?
- **Rework cost** — how expensive is it to be wrong?

# Engineering Method Table

| Method | Best for | Weak / risky when | Example components | Stage 2 selects it when |
|---|---|---|---|---|
| TDD (test-first, unit level) | Pure logic with definable correctness: parsers, state machines, data transforms, domain models | Design still unknown; heavy IO; GUI | Session/summary models, log parsers, config logic | Correctness is specifiable up front AND the code is agent-executable |
| Acceptance-test-first | User-visible behavior contracts: CLI commands, exit codes, output formats | Exploratory features; anything without a stable spec | CLI verbs, doctor-style checks, file outputs a human or AI consumes | The Project Brief's success criteria translate directly into executable checks |
| Contract-first | Data crossing boundaries: JSON/JSONL schemas, module interfaces, AI-readable outputs | Used alone — a contract without tests is a wish | session.json, events.jsonl, summary schemas | Two parties (human/AI/component) must agree on a format; pair with TDD or golden files |
| Spike-first / prototype-first | Killing uncertainty: unfamiliar libraries, GUI frameworks, undocumented behavior | The prototype quietly becomes production code | First GUI window, wrapping an interactive external tool | Design uncertainty is high; spike is timeboxed, then discarded or re-planned under a stricter method |
| Fake-first / simulation-based | Logic wrapping unreachable resources: hardware, local toolchains, external accounts | Fake fidelity — passing against a bad fake proves nothing | Toolchain command runners, serial monitor wrappers, port discovery | The resource is outside the agent's environment; default for all hardware/local-only behavior |
| Golden-file / snapshot | Generated artifacts: reports, summaries, rendered output | Brittle to intentional change; blesses whatever the first output was | Session summary Markdown/JSON regression | Output shape matters more than internal logic; pair with contract-first |
| Test-after + smoke | Thin, low-risk glue and shells over tested cores | Anything with real logic — invites untestable design | GUI shell whose controls call tested core services, wiring code | The component contains no decisions worth proving; a smoke test suffices |

# Compressed Decision Guide

Apply top-down, per subsystem:

1. Agent cannot execute it? Use **fake-first** + evidence + a Deferred entry in the Validation Ledger.
2. Data crosses a boundary? Use **contract-first**, backed by TDD or golden files.
3. Correctness specifiable and user-facing? Use **acceptance-test-first**. Specifiable and internal? Use **TDD**.
4. High design uncertainty? Use a **timeboxed spike**, then re-enter this guide.
5. None of the above (thin glue)? Use **test-after + smoke**.

# Per-Subsystem Output Shape

The Engineering Plan records one line per subsystem:

- Core logic → method + one-line reasoning
- File formats / schemas → method + reasoning
- CLI behavior → method + reasoning
- GUI → method + reasoning
- External integrations → method + reasoning
- Hardware / local-only behavior → method + reasoning

# Test Architecture Framework

A required Engineering Plan section answering, concretely:

- **Taxonomy** — which test types this tool needs (unit / contract-schema / acceptance / integration-with-fakes / golden-file / smoke) and which it deliberately skips.
- **Test doubles plan** — what gets faked or stubbed, and which fixtures back the fakes.
- **Layout** — where tests, fixtures, and golden files live in the repo.
- **CI** — what runs automatically vs. local-only.
- **Validation commands** — the specific invocations that constitute the agent's validation plan. The agent creates and executes a validation plan appropriate to the Engineering Plan, using checks that provide meaningful evidence — not "run everything runnable."
- **Evidence requirements** — raw evidence (command output, results, artifacts) lives in the repo under `docs/validation/`; verdict tables and source-of-truth summaries live in Notion (Build Log / AVB Report).
- **The unreachable list** — everything untestable in the agent environment, each with a written Stage 4 verification step. This is the Deferred half of the Validation Ledger.

# Fixture Policy

Stage 3 does **not** require Mike to record real fixtures before implementation begins. When real fixtures are unavailable, the agent uses synthetic or sample fixtures and notes the fidelity limit in the Validation Ledger. Stage 4 real-hardware runs should capture real fixtures, which are then committed as regression fixtures for later patches or v1 — real evidence flows backward into the test suite over time.

# Meaningful Validation, Defined

Every acceptance criterion and milestone checkpoint ends in exactly one of two states:

- **Verified** — proven by an executed check, with evidence.
- **Deferred** — explicitly deferred, with a written Stage 4 verification step.

There is no third state. An honest Deferred is a pass; a bluffed Verified is the one unforgivable sin of Stage 3.
