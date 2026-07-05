---
source_type: notion_snapshot
source_title: "Implementation — Personal Software Tool"
source_url: "https://app.notion.com/p/394850a911d381ef8c67da65b7b80e6b"
exported_at: "2026-07-05T18:05:00-05:00"
canonical_source: "Notion"
repo_snapshot_purpose: "Implementation-agent readable source snapshot"
---

# Page Properties

```json
{"Agents":["https://app.notion.com/p/394850a911d381a494cac6a444c9225e"],"Cue":"Build the tool","Knowledge":["https://app.notion.com/p/394850a911d3816a8b2dc00a7fbb3a36","https://app.notion.com/p/393850a911d38031bf98ef1e0dd11d18"],"Name":"Implementation — Personal Software Tool","Procedure Type":"Procedure","Status":"Draft","Trigger":"Run after the Engineering Plan is approved. Executes the current version's Implementation Milestones inside the specified agent harness.","Version":"0.2","url":"https://app.notion.com/p/394850a911d381ef8c67da65b7b80e6b"}
```

# Page Content

## Purpose
Turn an approved Engineering Plan into an **Agent-Validated Build** — autonomously.
This is Stage 3 of the AI Planned Personal Software Tool workflow. Stage 3 does **not** produce a commissioned tool. It produces a build that has been implemented, meaningfully validated within the agent's environment, documented, and handed to Stage 4 with its limits stated honestly.
## Procedure / Agent Split
The procedure defines what happens during the stage.
The Implementation Engineer agent defines the thinking style used while performing it.
## Autonomous Posture
The implementation agent (Codex, Claude Code, or another coding agent) builds the **full planned version** without Mike approving or testing milestones. Milestones are the agent's organizational units, not approval gates. Mike does not add value repeatedly saying "continue" — the plan already said what done means.
Work happens on a **feature branch with meaningful commits**, ending in a **single AVB handoff PR**.
## Trigger
Run after the Engineering Plan is approved, including its Method Selection, Test Architecture, Validation Ledger, and Autonomous Build Contract.
## Inputs
- Tool page (Project Brief + Engineering Plan, including the Agent Harness Specification and handoff package)
- Engineering Method Selection & Test Architecture Guide (Knowledge)
- Preferred Agent Harness & MCP Stack (Knowledge)
- Builder Profile (Michael Shears — Working Profile & AI Collaboration Guide)
- Repo (new or existing)
## Milestone 0 — Harness Bring-Up
Every run starts with a bring-up milestone, even if it takes ten minutes:
1. Create or open the repo; create the feature branch.
2. Set up the environment per the Agent Harness Specification (Python + uv unless the plan says otherwise).
3. Generate `CLAUDE.md` / `AGENTS.md` from the Tool page: purpose, v0 boundary, architecture summary, milestone list, Validation Ledger, and the stop-and-flag rules.
4. Verify MCPs/connectors named in the harness spec; note fallbacks if any are unavailable.
5. Run a smoke test proving the environment executes code at all.
6. **Stand up the Test Architecture skeleton**: test directories, fixture conventions (synthetic fixtures where real ones don't exist), acceptance-suite scaffold, CI stub if planned. The validation machinery exists before feature code does.
Bring-up problems are findings, not annoyances — log them; they feed the harness Knowledge item.
## Autonomous Milestone Loop
For each Implementation Milestone in the Engineering Plan:
1. **Restate** the milestone objective and its Validation Ledger entries.
2. **Build** using the engineering method the plan selected for that subsystem.
3. **Validate** by executing the milestone's validation plan — the checks the Test Architecture specified, providing meaningful evidence. Not "every test the agent can imagine."
4. **Record evidence** in `docs/validation/`: commands run, results, artifacts.
5. **Update the Validation Ledger**: each item becomes **Verified** (with evidence) or **Deferred** (with the Stage 4 verification step written out). Never mark an item Verified without executed evidence — an honest Deferred is a pass; a bluffed Verified is the one unforgivable sin of this stage.
6. **Log** a Build Log entry, **commit** with the branch runnable, and continue. No Mike demo. No approval wait.
## Stop Conditions
The agent halts and asks Mike only for:
- Product-scope ambiguity the plan cannot resolve
- Missing credentials, secrets, or account access
- Repository or tool access failure
- Architecture conflict discovered mid-build
- Contradiction within the approved plan
- Any decision that would materially change Stage 1 intent or the Stage 2 plan
Everything else: continue toward the full planned Stage 3 output.
## Deviation Tiers
- **Code-level** (naming, layout, small refactor): proceed, note in the Build Log.
- **Mechanical plan-level** (oversized milestone split, minor resequencing): proceed, log as a provisional delta.
- **Provisional delta** (substantive plan-level — a stack component fails, a piece is missing): allowed **only when the fix preserves the approved architecture and product intent**. Adopt the least-invasive fix, flag it prominently in the Build Log **and** the AVB Report, and continue. Mike adjudicates at Stage 4.
- **Architecture-changing or product-changing**: **stop and escalate**. Never silently re-architect.
## Evidence Convention
Raw evidence (test output, command logs, artifacts) lives in the repo under `docs/validation/`. Verdict tables, source-of-truth summaries, and the AVB Report live in the Build Log section of the Tool page.
## Output — the Agent-Validated Build
An Agent-Validated Build means:
- The planned version has been implemented on the feature branch.
- The validation plan has been executed, with evidence.
- The Validation Ledger is complete: every item Verified or Deferred, none blank.
- Documentation and handoff are complete; known limitations are stated.
- Anything requiring Mike's machine, local environment, account access, physical device, or hardware is explicitly deferred to Stage 4.
### AVB Report Shape
Appended to the Build Log section of the Tool page:
- Tool, version, branch + commit/tag, date, agent + environment
- Validation summary: commands executed and results
- Validation Ledger final state: Verified items (evidence links) / Deferred items (Stage 4 step each)
- Provisional deltas awaiting adjudication
- Known limitations
- How to pull, install, and run locally — the first thing Mike executes in Stage 4
## Build Log Entry Shape
Each entry (one per milestone, plus any session-close sync) includes:
- Milestone and date
- What was built
- Validation executed and result, with a pointer to the evidence in `docs/validation/`
- Decisions made and **why**
- Deviations from plan (with tier)
- Surprises / things to inspect later
## Context Bridge Rule
Notion is the source of truth for intent; the repo for code. `CLAUDE.md` / `AGENTS.md` are derived from the Tool page and are disposable — refresh whenever the plan changes. Sync points: milestone boundaries and Run It Back session closes.
## Tool Page Ownership Rule
This procedure owns the **Build Log** section of the Tool page (including the AVB Report). It does not edit the Project Brief or Engineering Plan sections; it flags proposed changes instead.
## Approval Gates
None per milestone. The agent escalates only at stop conditions or architecture/product-changing deltas. There is no separate AVB approval gate: **starting Stage 4 is the review**, and the AVB handoff PR plus AVB Report are its entry ticket.
## Exit Condition
The procedure is complete when the planned version is implemented, the validation plan has been executed with evidence, the Validation Ledger is complete with no blank states, the Build Log and AVB Report are current, the branch runs from a clean checkout in the agent's environment, the AVB handoff PR is open, and Mike can begin Stage 4 from the Tool page and repo alone — without replaying build conversations.
