"""Case 1 — hook exceeds its timeout (5 s). Docs: fail-open. Expected: tool FIRES."""
import sys, time
import os; sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from _common import read_event, guard
ev = read_event()
guard("timeout", ev, "sleeping 8s against a 5s timeout")
time.sleep(8)
print('{"decision": "deny", "reason": "too late"}')
sys.exit(2)
