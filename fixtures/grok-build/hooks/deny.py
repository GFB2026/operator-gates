"""Control — well-formed deny, exit 2. Expected: tool BLOCKED."""
import sys
import os; sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from _common import read_event, in_scope, log
ev = read_event()
if not in_scope(ev):
    sys.exit(0)
log("deny", ev, "explicit deny")
print('{"decision": "deny", "reason": "operator-gates fixture: NO-GO"}')
sys.exit(2)
