# operator-gates — GitHub Copilot shop-window

This repository is a **forkable GO / NO-GO contract** for agent-operated companies. Not a harness framework. Not a product SKU. Not wired to a live boot plane.

## What it is

- `src/operator_gates/gate.py` emits **one card**.
- **NO-GO** means do not send or charge in the same turn.
- You **pass posture** (flags or JSON). Do not invent greens.
- Scars in `scars/` stay **anonymized**.
- CLI: `operator-gates check|replay|scars`.
- Tests: `python -m pip install -e ".[dev]" && python -m pytest`.
- License: MIT.

## Safe lanes

Stay in these lanes:

- docs (`README.md`, `ANTI_PATTERNS.md`, anonymized `scars/` text)
- tests (`tests/`, `examples/`)
- CLI (`src/operator_gates/`)
- GitHub Copilot config (this file, `.copilotignore`, `.github/workflows/copilot-setup-steps.yml`)

## NEVER

- Read or write secrets, `.env*`, or credentials
- Live send or charge
- Reach `gc-mcp`, fleet, `apps/`, or `ops/`
- Paste or invent real mail bodies
- Include student data
- Name private fleet paths
- Invent a GO card
- Wire this repo to a live boot plane
- Add `COPILOT_MCP` or MCP config that can reach apps / ops / gc-mcp

Pass posture. Do not invent greens.
