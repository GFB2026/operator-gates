"""Control — well-formed deny, exit 2. Expected: tool BLOCKED."""
import sys
import os; sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from _common import read_event, guard
ev = read_event()
guard("deny", ev, "explicit deny")
print('{"decision": "deny", "reason": "operator-gates fixture: NO-GO"}')
sys.exit(2)
