"""malformed_exit2 — truncated deny JSON with exit 2. The row that matters.

deny.py (well-formed JSON, exit 2) blocks. This prints the same truncated body
and exits 2, the documented deny code.

Observed on Windows, Grok Build 1.0.34, 2026-09-19: tool FIRES. Dispatcher:
``gate hook failed; ignoring (fail-open) ... hook_failure=exit code 1``.
The harness saw the exit as 1, the stdout had no parseable deny to fall back
on, and the gate was ignored. Expected: tool FIRES (fail-open).
"""
import sys
import os; sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from _common import read_event, guard
ev = read_event()
guard("malformed_exit2", ev, "truncated deny JSON; exit 2 (the deny code)")
print('{"decision": "deny", "reason": "truncated')
sys.exit(2)
