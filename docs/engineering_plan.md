# Cockpit 32 Engineering Plan Snapshot

Derived from `docs/notion-source/01-cockpit-32-tool-page.md` for Stage 3 implementation.

- Language/tooling: Python, uv, pytest.
- Board: ESP32-S3-BOX-3 only in v0.
- Architecture: core domain, ESP-IDF adapters, project-local persistence, CLI, thin PySide6 GUI, agent-readable docs/evidence.
- Session storage: firmware project `.cockpit32/sessions/<session-id>/`.
- Stage 3 validation: agent-provable fake-first checks; defer real ESP-IDF/COM/hardware checks to Stage 4.
