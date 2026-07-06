# Cockpit 32 Agent-Validated Build Report

- Tool: Cockpit 32
- Version: v0 Agent-Validated Build
- Agent: Codex / Implementation Engineer
- Date: 2026-07-05
- Branch: `feature/stage3-agent-validated-build`

## Validation summary

Stage 3 validation used no-hardware tests, fake-first ESP-IDF wrapper tests, contract checks for session artifacts, CLI acceptance tests, summary/golden-shape tests, and offscreen GUI smoke testing.

See `docs/validation/stage3-validation.md` and `docs/validation-ledger.md`.

## Provisional deltas

- Code-level: GUI build/flash/monitor buttons are not implemented in the first shell; the GUI provides doctor, session, and note workflow over the shared core. CLI contains the full build/flash/monitor path. Stage 4 should decide whether GUI buttons are fix-before-acceptance or acceptable for this AVB iteration.
- Code-level (2026-07-05, Claude Code re-verification): `IdfRunner.run` failed on Windows (`WinError 193`) when invoking the fake `idf.py` fixture directly, because Windows does not execute `.py` files without going through the interpreter. Original AVB evidence was captured on Linux only, where the shebang line masked this. Fixed by prepending `sys.executable` when `idf_command` ends in `.py`; does not change architecture or product intent. Re-verified 8/8 tests passing on Windows. See `docs/validation/stage3-validation.md`.

## Known limitations

- Real ESP-IDF, COM-port, and BOX-3 hardware behavior is not validated in Stage 3.
- Monitor capture currently uses a bounded subprocess timeout and treats timeout output as a wrapper concern for v0; real interactive behavior needs Stage 4 scrutiny.
- GUI is intentionally thin and early.

## First Stage 4 command

```powershell
uv sync
uv run cockpit32 doctor
```
