---
source_type: notion_snapshot
source_title: "AI Planned Personal Software Tool"
source_url: "https://app.notion.com/p/394850a911d381c6a0fcf78a06637231"
exported_at: "2026-07-05T18:05:00-05:00"
canonical_source: "Notion"
repo_snapshot_purpose: "Implementation-agent readable source snapshot"
---

# Page Properties

```json
{"Workflow Name":"AI Planned Personal Software Tool","Status":"Draft","Version":"0.2","Purpose":"Full-lifecycle AI-assisted workflow for taking a personal software tool from idea through definition, planning, implementation, commissioning, and long-term evolution.","url":"https://app.notion.com/p/394850a911d381c6a0fcf78a06637231"}
```

# Page Content

# Overview
This workflow coordinates the procedures that take a meaningful personal software tool from idea to In Service — and keep the record true afterward. The workflow owns the sequence; the procedures own the execution details; the agents own the thinking styles.

It is the AI-designed continuation of Create Personal Software Tool. Stages 1–2 are shared with that workflow and reused unmodified. Stages 3–5 are new.

# Shared Record
The **Tool page** is the persistent record. Each stage owns exactly one section and never silently edits another stage's section:

| Stage | Section Owned |
|---|---|
| 1 — Product Definition | Project Brief |
| 2 — Engineering Planning | Engineering Plan |
| 3 — Implementation | Build Log |
| 4 — Commissioning | Commissioning & Operations |
| 5 — Evolution | Change Log |

Cross-section changes are always flagged, explained, and applied by the owning stage's rules.

One artifact deliberately spans stages: the **Validation Ledger**. Born in Stage 2 (every acceptance criterion and milestone checkpoint tagged Agent-Provable or Deferred), executed and evidenced in Stage 3, and consumed by Stage 4 as its commissioning test spec alongside the cold-start test. Evidence convention: raw evidence lives in the repo under `docs/validation/`; verdict tables and source-of-truth summaries live on the Tool page.

# Stage Contracts

## Stage 1 — Product Definition
**Consumes:** an initial idea, conversation, or note cluster, plus relevant Knowledge, Sources, related Projects, and builder preferences.

**Produces:** an initialized Tool record with an accepted Project Brief. Stops before architecture.

**Approval:** yes — Mike accepts the Project Brief.

## Stage 2 — Engineering Planning
**Consumes:** the Tool page with its accepted Project Brief; the Preferred Agent Harness & MCP Stack Knowledge item when writing the Agent Harness Specification; the Engineering Method Selection & Test Architecture Guide when selecting methods and specifying the Test Architecture.

**Produces:** an approved Engineering Plan v2: architecture, stack, Product Roadmap, Implementation Milestones, per-subsystem Engineering Method Selection, Test Architecture, initial Validation Ledger, Autonomous Build Contract, Agent Harness Specification, risks, handoff package. Current tooling: a ChatGPT planning thread with Deep Research launched from the same thread.

**Approval:** two gates — the **Mike Guidance Check** before Deep Research launches, and Engineering Plan approval before it enters the Tool record.

## Stage 3 — Implementation
**Consumes:** the approved Engineering Plan and its handoff package; the harness and method-selection Knowledge items at bring-up.

**Produces:** an **Agent-Validated Build** — the planned version implemented autonomously on a feature branch with meaningful commits, validated per the plan's Test Architecture with evidence, Validation Ledger complete (every item Verified or Deferred), Build Log and AVB Report current, and a single AVB handoff PR. Explicitly *not* commissioned: hardware/local validation is deferred to Stage 4.

**Updates:** Tool page — Build Log section (including the AVB Report).

**Approval:** none per milestone. The agent escalates only at stop conditions or architecture/product-changing deltas; provisional deltas that preserve approved architecture and product intent proceed flagged, adjudicated in Stage 4. Starting Stage 4 is the AVB review.

## Stage 4 — Commissioning
**Consumes:** the Agent-Validated Build (via its handoff PR), the AVB Report with the Deferred Validation Ledger (the commissioning test spec alongside the Project Brief success criteria), and any provisional deltas awaiting adjudication. Real fixtures captured during commissioning runs should be committed as regression fixtures for later patches or v1.

**Produces:** a Commissioning Report (cold-start test, per-criterion verdicts with evidence, classified defects) and — on acceptance — a Commissioning & Operations section that lets future Mike or a future AI run the tool with zero build context. Ends with an Engineering Debrief & System Evolution Review.

**Approval:** yes — acceptance is Mike's decision.

## Stage 5 — Evolution (steady state)
**Consumes:** any desired change to an In Service tool.

**Produces:** the change classified (Patch / Feature / Rework / Rethink), routed to the stage that owns the decision, executed as a mini-run, and recorded in the Change Log.

**Approval:** inherits the approval gates of whichever stage the change routes through.

# Routing Rules (the loop)
- Patch → Stage 3 (single milestone)
- Feature → Brief/Roadmap check → Stage 2 delta if needed → Stage 3
- Rework → Stage 2 → Stage 3 → re-commission affected criteria
- Rethink → Stage 1 → forward through all stages
- When in doubt, classify upward.

# Context Bridge Principle
Notion is the source of truth for **intent**; the repo is the source of truth for **code**. The bridge is a `CLAUDE.md` generated from the Tool page at harness bring-up — derived and disposable; the Tool page wins on conflict. Sync points: milestone boundaries and Run It Back session closes. This is what keeps engineering intent alive across Claude Code sessions without replaying reasoning.

# Workflow Design Principles
- Workflows orchestrate. Procedures execute. Agents provide reusable thinking style. Knowledge provides long-term context. The Tool page preserves project state.
- Each stage owns exactly one Tool-page section; later stages flag proposed changes to earlier sections rather than silently rewriting them.
- Every handoff must survive a context wipe: the next role starts from the Tool page, never from a replayed conversation.
- The builder never grades his own homework: the Commissioning role is deliberately distinct from the Implementation role even when the same model plays both.
- The workflow is a loop, not a conveyor: commissioned tools re-enter through triage, and the Engineering Debrief feeds lessons back into the AI-OS after every significant run.

# Design Decisions & Rationale
- **Reused, not duplicated:** Stage 1–2 procedures and agents, Engineering Debrief & System Evolution Review, and the Builder Profile.
- **Milestone 0 (harness bring-up) is a formal milestone** because harness friction is where real sessions die, and logging it feeds the harness Knowledge item.
- **Commissioning is a separate stage, not the last implementation milestone,** because the cold-start test only means something when performed against the documentation, not the memory of the build.
- **Stage 5 has no agent** — triage is routing, not a thinking style. Adding a fifth agent would be agent sprawl.
- **Two new agents only.** A dedicated QA/test-writer agent was considered and rejected: test strategy lives in the Engineering Plan and executes inside Implementation; a solo-maker workflow does not need a standing QA department.

# Current Scope & First Run
All five stages are designed; Stages 3–5 are unrun. First live test should be a deliberately small tool so the workflow itself is what is being commissioned — Cockpit 32 is the standing candidate.
