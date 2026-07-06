# AI-Readability Test (Validation Strategy, layer 4)

Per the Tool page's Validation Strategy: "Give Codex or Claude Code only
the latest session summary and ask what happened. If the agent cannot
understand the result, improve the summary format."

## Method

A fresh subagent (no access to this build's conversation, codebase, or
any context beyond the file contents) was given only the `summary.md`
produced by `docs/validation/e2e_cli_workflow_transcript.txt`'s demo
session, and asked: what happened, what to investigate next, and
whether anything about the format was confusing.

## Round 1 — pre-fix summary.md

```
## Phase Results
- build: fail
- flash: not run
- monitor: pass

## Notable Monitor Lines
- `Guru Meditation Error: Core 0 panic'ed (LoadProhibited). Exception was unhandled.`
```

The agent correctly reconstructed the session narrative, but flagged a
real defect unprompted:

> "How can monitor 'pass' while showing a fatal Guru Meditation crash —
> what does 'pass' mean here? ... No build error text/log excerpt is
> included."

This is a legitimate AI-readability failure: `monitor: pass` implies a
health judgment the tool never made (monitor only captures output; it
doesn't grade the boot), and a fatal crash line was indistinguishable
from a routine boot marker without opening the raw log.

## Fix Applied (code-level deviation, logged in Build Log)

- `render_markdown`: monitor phase now renders as `captured` instead of
  `pass`/`fail`, since monitor has no pass/fail of its own.
- `notable_events` entries are now prefixed with their classification —
  `[error]`, `[warning]`, or `[boot]` — so severity is visible without
  cross-referencing `monitor.log`.
- Golden files (`tests/golden/summary.json`, `summary.md`) and
  `tests/unit/test_summaries.py` updated with regression tests for both
  changes. Full suite re-run green (`docs/validation/full_suite.txt`).

## Result

**Verified.** The test executed, found one real defect, the defect was
fixed, and a regression test now guards it. Not re-run through a second
fresh-agent round after the fix (time-boxed within Stage 3); re-running
this exact check is a cheap, high-value first step for Stage 4 or the
next Stage 3 patch.
