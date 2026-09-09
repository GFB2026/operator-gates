"""Replay scar 002 — wrong host, wrong truth."""

from operator_gates import Posture, check

print("# identical path, no pin")
print(check("other", Posture(host_pinned=False, note="path exists on multiple boxes")))

print("# host named")
print(check("other", Posture(host_pinned=True, note="machine named")))
