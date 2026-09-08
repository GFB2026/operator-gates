"""Replay scar 001 without the CLI — same cards."""

from operator_gates import Posture, check

print("# draft ready, mirror lagging")
print(check("mail_send", Posture(mirror_ok=False, phrase=True, note="draft ready")))

print("# mirror fixed + phrase")
print(check("mail_send", Posture(mirror_ok=True, phrase=True, note="ops reply")))
