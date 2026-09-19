"""Case 2 — hook crashes (exit 1, traceback on stderr). Docs: fail-open. Expected: tool FIRES."""
import sys
import os; sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from _common import read_event, guard
ev = read_event()
guard("crash", ev, "raising before any decision")
raise RuntimeError("gate crashed before deciding")
