---
source_type: notion_snapshot
source_title: "Preferred Agent Harness & MCP Stack"
source_url: "https://app.notion.com/p/394850a911d3816a8b2dc00a7fbb3a36"
exported_at: "2026-07-05T18:05:00-05:00"
canonical_source: "Notion"
repo_snapshot_purpose: "Implementation-agent readable source snapshot"
---

# Page Properties

```json
{"Agents":["https://app.notion.com/p/394850a911d381a494cac6a444c9225e"],"Cue":"Default coding harness setup","Knowledge Type":"Reference","Name":"Preferred Agent Harness & MCP Stack","Notes":"Created 2026-07-04 as part of the AI Planned Personal Software Tool workflow design. This resolves the 'Preferred Agent Harness / MCP Knowledge' future dependency named on the original workflow. Entries marked SEEDED are drawn from Mike's known stack, not from validated runs — promote to Standing: Preferred only after they survive a real implementation.","Procedures":["https://app.notion.com/p/394850a911d381ef8c67da65b7b80e6b"],"Standing":"Candidate","Status":"Tentative","Summary":"Default harness for tool implementation: which coding agent, required context, recommended MCPs/connectors, and fallbacks. Consulted by Engineering Planning (Stage 2) when writing an Agent Harness Specification and by Implementation (Stage 3) at harness bring-up. Seeded from Mike's current stack; individual entries still need verification through real runs.","Tags":["AI"],"Workflows":["https://app.notion.com/p/394850a911d381c6a0fcf78a06637231"],"date:Last Reviewed:is_datetime":0,"date:Last Reviewed:start":"2026-07-04","url":"https://app.notion.com/p/394850a911d3816a8b2dc00a7fbb3a36"}
```

# Page Content

# What This Is
The default answer to "what harness does the coding agent run in?" so each Engineering Plan doesn't rebuild the answer from scratch. Engineering Plans may override any of this per-tool; when they do, the Agent Harness Specification on the Tool page wins.
# Default Harness (SEEDED — verify through real runs)
- **Primary coding agent:** Claude Code
- **Environment:** Windows 11 native + PowerShell (no WSL), VS Code as editor
- **Language default:** Python managed with uv (not pip)
- **Version control:** Git + GitHub
- **Secondary machine:** mini PC (Linux) planned as programmer/server test bed — not yet in service
# Required Context Attachments
Every implementation run starts with:
- The Tool page (Project Brief + Engineering Plan) or its exported handoff package
- A repo-level `CLAUDE.md` generated from the Tool page (see Context Bridge Convention below)
- The Builder Profile (Michael Shears — Working Profile & AI Collaboration Guide)
# Recommended MCPs / Connectors (SEEDED)
- **Notion MCP** — read Tool page context, write Build Log entries at sync points
- **GitHub MCP** — repo operations beyond local git where useful
- Others per-tool as specified in the Engineering Plan
# Context Bridge Convention
Notion is the source of truth for **intent** (why the tool exists, what the architecture is, what done means). The repo is the source of truth for **code**. The bridge:
- At harness bring-up, generate `CLAUDE.md` from the Tool page: purpose, v0 boundary, architecture summary, current milestone, validation checkpoints, and the rule "do not re-architect — flag deltas."
- `CLAUDE.md` is derived and disposable; if it disagrees with the Tool page, the Tool page wins.
- Sync points: end of each milestone and any "run it back" session close — Build Log entry to Notion, `CLAUDE.md` refreshed if the plan changed.
# Fallbacks
- Notion MCP unavailable → work from a pasted/exported handoff package; queue Build Log entries locally and sync later.
- Claude Code unavailable → Claude chat with repo files attached, smaller slices, manual command execution by Mike.
# Open Questions (not yet decided)
- Claude Code hooks (PostToolUse auto-build, Stop auto-flash style) — useful default for software tools or embedded-only?
- Subagents and Plan Mode — when do they earn their place in a personal-tool build?
- Standard repo scaffold (folder layout, smoke-test convention) worth encoding here after 2–3 tools are built.
