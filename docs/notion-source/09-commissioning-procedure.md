---
source_type: notion_snapshot
source_title: "Commissioning — Personal Software Tool"
source_url: "https://app.notion.com/p/394850a911d3815aa9b5fae59add050e"
exported_at: "2026-07-05T18:05:00-05:00"
canonical_source: "Notion"
repo_snapshot_purpose: "Implementation-agent readable source snapshot"
---

# Page Properties

```json
{"Name":"Commissioning — Personal Software Tool","Procedure Type":"Review","Status":"Draft","Trigger":"Run after Implementation Milestones are validated, before regular service.","url":"https://app.notion.com/p/394850a911d3815aa9b5fae59add050e"}
```

# Page Content

## Purpose
Prove the built tool actually does what the Project Brief said it should, then put it into service with documentation that survives without the build conversations.

This is Stage 4 of the AI Planned Personal Software Tool workflow.

## Procedure / Agent Split
The procedure defines what happens during the stage. The Commissioning Engineer agent defines the skeptical acceptance-testing style used while performing it.

## Trigger
Run after all Implementation Milestones for the current version have passed, before the tool enters regular use.

## Inputs
- The Agent-Validated Build and repo
- Tool page: Project Brief, Engineering Plan, Build Log with AVB Report
- The Deferred half of the Validation Ledger
- Provisional deltas flagged in the AVB Report
- Documented install/run instructions

## Steps
1. Read the Project Brief success criteria, the Validation Ledger, and the AVB Report. The Deferred Ledger items plus the success criteria are the test spec. Adjudicate provisional deltas early.
2. **Cold-start test**: install and run the tool from its documented instructions alone. If the docs cannot stand alone, that is a fix-before-acceptance finding.
3. Exercise the core use case end to end as the primary user would actually use it, and walk the Deferred Ledger items in the real environment, recording a verdict for each. Where practical, capture real logs and output during these runs; commit them as regression fixtures for later patches or v1.
4. For each success criterion, record **pass / partial / fail** with concrete evidence.
5. Catalog every defect and rough edge, classified: **fix-before-acceptance / accept-as-is / future roadmap**. Criteria that failed because the criterion was wrong are flagged as product-intent findings, not build defects.
6. Present the Commissioning Report. Mike decides: accept, or return fix-before-acceptance items to the Implementation procedure and re-run the affected checks.
7. On acceptance, populate the **Commissioning & Operations** section of the Tool page:
   - How to install and run
   - Dependencies and configuration
   - Known issues
   - Maintenance notes and debugging entry points
   - Acceptance record: date, version, criteria results
   - Mark the tool **In Service**
8. Run the Engineering Debrief & System Evolution Review procedure.

## Commissioning Report Shape
- Tool, version, date
- Cold-start result
- Success criteria table: criterion → verdict → evidence
- Deferred Ledger table: deferred item → verdict → evidence
- Provisional delta adjudications: accepted / rejected, with reasons
- Defect list with classifications
- Product-intent findings, if any
- Acceptance recommendation

## Tool Page Ownership Rule
This procedure owns the **Commissioning & Operations** section. It does not edit the Project Brief, Engineering Plan, or Build Log sections.

## Approval Gate
Acceptance is Mike's decision. The Commissioning Engineer recommends; Mike accepts.

## Exit Condition
The procedure is complete when the tool is accepted, marked In Service, and the Operations section lets future Mike — or a future AI with no memory of the build — run, debug, and maintain the tool from the Tool page alone.
