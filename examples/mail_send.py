"""Mail-send path: mirror ok + phrase required."""

from operator_gates import Posture, check

print("--- missing phrase ---")
print(check("mail_send", Posture(mirror_ok=True, phrase=False)))

print("--- GO ---")
print(
    check(
        "mail_send",
        Posture(mirror_ok=True, phrase=True, note="ops reply to peer"),
    )
)
