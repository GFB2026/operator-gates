This repo is a small, forkable GO / NO-GO contract for agent-operated companies.

- Not a harness framework. Not a product SKU. Not wired to a live boot plane.
- `src/operator_gates/gate.py` emits one card. NO-GO means do not send or charge in the same turn.
- You pass posture (flags or JSON). Do not invent greens.
- Scars in `scars/` stay anonymized. No private fleet paths, no student data, no mail bodies.
- CLI: `operator-gates check|replay|scars`. Tests: `python -m pip install -e ".[dev]" && python -m pytest`.
- MIT.
