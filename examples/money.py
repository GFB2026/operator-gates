"""Money path: phrase always; dry/pause holds block."""

from operator_gates import Posture, check

print("--- no phrase ---")
print(check("money", Posture(phrase=False)))

print("--- dry hold ---")
print(check("money", Posture(phrase=True, holds=["stripe_dry_run"])))

print("--- GO ---")
print(check("money", Posture(phrase=True, note="exact charge approve")))
