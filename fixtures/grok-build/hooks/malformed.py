"""Case 3 — hook emits malformed JSON with exit 0. Docs: fail-open. Expected: tool FIRES."""
import sys
import os; sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from _common import read_event, in_scope, log
ev = read_event()
if not in_scope(ev):
    sys.exit(0)
log("malformed", ev, "printing truncated deny JSON")
print('{"decision": "deny", "reason": "truncated')
sys.exit(0)
