"""Case 1 — hook exceeds its timeout (5 s). Docs: fail-open. Expected: tool FIRES."""
import sys, time
import os; sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from _common import read_event, in_scope, log
ev = read_event()
if not in_scope(ev):
    sys.exit(0)
log("timeout", ev, "sleeping 8s against a 5s timeout")
time.sleep(8)
print('{"decision": "deny", "reason": "too late"}')
sys.exit(2)
