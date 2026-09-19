"""malformed_exit0_allow — truncated deny JSON with exit 0.

The docs say exit 0 allows, so this firing is the documented path, not a finding.
It is kept as the pair to malformed_exit2. Expected: tool FIRES."""
import sys
import os; sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from _common import read_event, guard
ev = read_event()
guard("malformed_exit0_allow", ev, "truncated deny JSON; exit 0 (documented allow)")
print('{"decision": "deny", "reason": "truncated')
sys.exit(0)
