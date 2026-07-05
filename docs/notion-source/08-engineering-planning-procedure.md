---
source_type: notion_snapshot
source_title: "Engineering Planning — Personal Software Tool"
source_url: "https://app.notion.com/p/394850a911d381c8a5dedf74edc84b41"
exported_at: "2026-07-05T18:05:00-05:00"
canonical_source: "Notion"
repo_snapshot_purpose: "Implementation-agent readable source snapshot"
---

# Page Properties

```json
{"Agents":["https://app.notion.com/p/394850a911d381368e63e346a35c41c5"],"Cue":"Plan tool build","Name":"Engineering Planning — Personal Software Tool","Procedure Type":"Procedure","Status":"Draft","Trigger":"Run after Product Definition is accepted and before implementation begins.","url":"https://app.notion.com/p/394850a911d381c8a5dedf74edc84b41"}
```

# Page Content

## Purpose
Transform an accepted Project Brief into an approved **Engineering Plan** that answers two questions, not one: *what should be built*, and *how an autonomous coding agent should build and prove it before Mike ever touches the code*.

This is Stage 2 of the AI Planned Personal Software Tool workflow.

## Procedure / Agent Split
The procedure defines what happens during the stage. The Systems Architect agent defines the thinking style used while performing it.

## Current Tooling
Stage 2 currently runs as a single continuous **ChatGPT planning thread**, with **Deep Research launched from that same thread** so accumulated context rides along. The procedure is agent-neutral; any planner capable of these phases can run it.

## Trigger
Run after Product Definition is accepted and before implementation begins.

## Inputs
- Tool page (accepted Project Brief)
- This procedure and the workflow page
- Engineering Method Selection & Test Architecture Guide (Knowledge)
- Preferred Agent Harness & MCP Stack (Knowledge)
- Builder Profile (Michael Shears — Working Profile & AI Collaboration Guide)
- Relevant Knowledge, Sources, and related Projects

## Phase A — Context Assembly
1. Read the Tool page and Project Brief.
2. Pull relevant Knowledge, Sources, and related Projects into the planning thread.
3. Build planning context conversationally: validate technical feasibility, pressure-test scope, and move oversized ideas to later roadmap versions.

## Phase B — Mike Guidance Check (required gate)
1. Present the **Pre-Research Framing** — compact but complete:
   - What the tool is supposed to become, in the architect's own words
   - v0 scope and v0 non-goals
   - Known constraints
   - Implementation agent + environment, and what that environment **cannot reach**
   - What Mike will and will not do during Stage 3
   - Draft hardware/local validation boundary
   - Open assumptions, explicitly listed
   - The **Deep Research Brief**: exactly what research will be asked to resolve
2. Ask Mike: *"Before I launch Deep Research — what is wrong, missing, overstated, or underemphasized?"*
3. Incorporate corrections before proceeding. This is Mike's highest-leverage input point.

## Phase C — Deep Research
1. Launch Deep Research from the same thread. Practical note: Mike may need to click/launch Deep Research manually in ChatGPT — remind him when that moment arrives.
2. Treat the Deep Research output as a **major input, not the plan**. The architect synthesizes; research does not write the plan by default.

## Phase D — Synthesis & Approval
1. Synthesize the Engineering Plan using the output shape below.
2. Present to Mike for **intent/scope alignment review**.
3. After approval, populate the Engineering Plan section of the Tool page.
4. Stop before implementation.

## Engineering Plan Output Shape
### 1. Executive Recommendation
Short summary of the recommended build strategy.
### 2. Recommended Architecture
Major components and how they relate.
### 3. Technology Decisions
For each major decision: Recommendation, Reasoning, Alternatives considered, Tradeoffs, Fallback if unavailable.
### 4. Product Roadmap
Vision / V0 / V1 / V2+. Move adventurous or oversized ideas out of v0.
### 5. Implementation Milestones
Buildable engineering checkpoints for the current version — internal organizational units for the agent, with no Mike approval implied per milestone. Each includes Objective, Deliverables, and Validation checkpoint.
### 6. Engineering Method Selection
Per subsystem — core logic, file formats/schemas, CLI behavior, GUI, external integrations, hardware/local-only behavior — select the engineering method using the guide, with one line of reasoning each.
### 7. Test Architecture
Taxonomy, test-doubles and fixture plan, repo layout, CI split, validation commands, evidence requirements, and unreachable list.
### 8. Validation Ledger (initial)
Every acceptance criterion and milestone checkpoint tagged **Agent-Provable** or **Deferred to Stage 4**, each with a planned verification approach.
### 9. Autonomous Build Contract
- Stop conditions for the implementation agent
- Deviation tiers
- Evidence requirements: raw evidence in the repo under `docs/validation/`; verdict tables and summaries in Notion
- Branch convention: feature branch, meaningful commits, single AVB handoff PR
- Definition of Stage 3 done: a complete **Agent-Validated Build**
### 10. Agent Harness Specification
Primary coding agent, required context attachments, recommended MCPs/connectors, optional tools, fallbacks, known limitations, handoff package.
### 11. Risks and Unknowns
Technical issues to verify before or during implementation.
### 12. Handoff Package
What the Implementation Engineer receives before build begins.

## Approval Gates
Two: the **Mike Guidance Check** before Deep Research launches, and **Engineering Plan approval** before it enters the Tool record.

## Tool Page Ownership Rule
This procedure owns the Engineering Plan section after approval. It should not silently rewrite the Project Brief. If planning suggests the Project Brief should change, record the proposed change and explain why.

## Exit Condition
The procedure is complete when the Tool page contains an approved Engineering Plan — including Method Selection, Test Architecture, the initial Validation Ledger, and the Autonomous Build Contract — sufficient for the implementation agent to build to an Agent-Validated Build without Mike testing milestones along the way.
